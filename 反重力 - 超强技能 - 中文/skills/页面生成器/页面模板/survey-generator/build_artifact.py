"""通过 Fireworks 上的 Kimi K2.6 生成综述论文风格的 HTML 制品。

研究合集与分类体系（research_bundle.json）以及从 RAG 综述中提取的样式规范
（style_spec.json）由 Claude Code 智能体准备。本脚本将该数据包发送到
Fireworks 上的 Kimi K2.6，并将返回的单文件 HTML 制品写入 output/survey_v{N}.html。

用法：
    export FIREWORKS_API_KEY=...  # 已在 zshrc 中配置
    python build_artifact.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import urllib.request
import urllib.error

HERE = Path(__file__).parent
BUNDLE_PATH = HERE / "research_bundle.json"
STYLE_PATH = HERE / "style_spec.json"
OUTPUT_DIR = HERE / "output"
RESULTS_PATH = HERE / "results.md"

DEFAULT_MODEL = "accounts/fireworks/models/kimi-k2p6"
MODEL = os.environ.get("FIREWORKS_MODEL", DEFAULT_MODEL)
ENDPOINT = "https://api.fireworks.ai/inference/v1/chat/completions"


def model_slug(model: str) -> str:
    """将模型路径（如 accounts/fireworks/models/kimi-k2p5）转换为 'kimi-k2p5'。"""
    return model.rsplit("/", 1)[-1]


SYSTEM_PROMPT = """你是一位资深技术撰稿人和 HTML 设计师，负责生成单文件学术综述制品。

你将收到两个 JSON 数据：
1. 一个 research_bundle，包含综述的标题、分类体系、章节和固定的真实论文参考文献。
2. 一个 style_spec，描述布局、排版、所需图表、所需表格、配色方案和硬性规则。

你的任务是生成一个自包含的 HTML 文档，该文档：
- 在风格和结构上读起来像一篇学术综述论文。
- 仅使用提供的参考文献条目。不要编造引用。
- 严格遵循 research_bundle 中的章节列表。
- 将所有所需图表渲染为内联 SVG。
- 遵守 style_spec.hard_rules_for_generation 中的每一条规则。

仅输出 HTML 文档。不要在 HTML 之前或之后包含说明、markdown 围栏或注释。你回复的第一个字符必须是 <!DOCTYPE html>，最后一个字符必须是 </html>。
"""


USER_TEMPLATE = """现在生成综述制品。

=== research_bundle.json ===
{bundle}

=== style_spec.json ===
{style}

要求提醒：
- 单个自包含 HTML 文件。仅内联 CSS 和内联 SVG。无外部资源。
- 正文目标长度：所有章节合计 5000 至 6500 词。每个章节应有实质性讨论（至少 3 段）并整合多篇引用文献。保持图表精致但简洁。优先完成所有章节和参考文献列表，而非图表精雕细琢。
- 仅引用上述参考文献条目，使用括号引用格式如 (Yao et al., 2022)。
- 按 style_spec.required_figures 将图 1（分类体系树）、图 2（三种范式面板）和图 3（工具栈）渲染为内联 SVG。
- 按 style_spec.required_tables 包含表 1（代表性系统）。
- 结尾附编号参考文献列表，列出每条参考文献条目。
- 正文中不使用破折号或箭头符号。

现在输出 HTML 文档。"""


def load_inputs() -> tuple[dict, dict]:
    if not BUNDLE_PATH.exists():
        raise SystemExit(
            "未在 build_artifact.py 旁边找到 research_bundle.json。
"
            "请先复制 templates/research_bundle_template.json 并填入内容，
"
            "或以 examples/agentic-engineering/research_bundle.json 为起点进行改编。"
        )
    bundle = json.loads(BUNDLE_PATH.read_text())
    style = json.loads(STYLE_PATH.read_text())
    return bundle, style


def build_messages(bundle: dict, style: dict) -> list[dict]:
    user = USER_TEMPLATE.format(
        bundle=json.dumps(bundle, indent=2),
        style=json.dumps(style, indent=2),
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]


def call_fireworks(messages: list[dict], api_key: str) -> dict:
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.4,
        "top_p": 0.95,
        "max_tokens": 81920,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTPError {e.code}: {body}", file=sys.stderr)
        raise
    elapsed = time.time() - t0
    data = json.loads(raw)
    data["_elapsed_sec"] = elapsed
    return data


def extract_html(content: str) -> str:
    """去除 HTML 周围意外的 markdown 围栏或多余的正文。"""
    text = content.strip()
    # 去除开头的 ```html 或 ``` 围栏
    text = re.sub(r"^```(?:html)?\s*", "", text)
    text = re.sub(r"\s*```\s*$", "", text)
    # 如果存在 <!DOCTYPE html> 起始位置，则从该处截取；否则保持原样
    start = text.lower().find("<!doctype html")
    if start > 0:
        text = text[start:]
    return text.strip()


def next_version_path() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    slug = model_slug(MODEL)
    # 向后兼容：如果存在未 slug 化的文件，保留它们，后续使用 slug 化的文件名。
    existing = sorted(OUTPUT_DIR.glob(f"survey_{slug}_v*.html"))
    n = len(existing) + 1
    return OUTPUT_DIR / f"survey_{slug}_v{n}.html"


def append_results(entry: str) -> None:
    header = "# Kimi K2.6 智能体工具综述 - 运行日志\n\n" if not RESULTS_PATH.exists() else ""
    with RESULTS_PATH.open("a") as f:
        if header:
            f.write(header)
        f.write(entry)


def main() -> int:
    api_key = os.environ.get("FIREWORKS_API_KEY")
    if not api_key:
        print("环境中未设置 FIREWORKS_API_KEY。", file=sys.stderr)
        return 2

    bundle, style = load_inputs()
    messages = build_messages(bundle, style)

    print(f"正在调用 Fireworks 模型 {MODEL}...")
    print(f"提示词大小：{sum(len(m['content']) for m in messages)} 字符")

    data = call_fireworks(messages, api_key)

    choice = data["choices"][0]
    content = choice["message"]["content"]
    html = extract_html(content)

    out_path = next_version_path()
    out_path.write_text(html)

    usage = data.get("usage", {})
    elapsed = data.get("_elapsed_sec", 0.0)

    entry = (
        f"\n## 运行时间 {datetime.now().isoformat(timespec='seconds')}\n"
        f"- 输出：`{out_path.relative_to(HERE)}`\n"
        f"- 模型：`{MODEL}`\n"
        f"- 耗时：{elapsed:.1f}s\n"
        f"- 提示词 token：{usage.get('prompt_tokens', 'n/a')}\n"
        f"- 补全 token：{usage.get('completion_tokens', 'n/a')}\n"
        f"- 总 token：{usage.get('total_tokens', 'n/a')}\n"
        f"- 完成原因：{choice.get('finish_reason', 'n/a')}\n"
        f"- HTML 长度：{len(html)} 字符\n"
        f"- HTML 开头：`{html[:60].replace(chr(10), ' ')}`\n"
    )
    append_results(entry)

    print(f"\n已写入 {out_path}")
    print(f"耗时 {elapsed:.1f}s，补全 token {usage.get('completion_tokens', 'n/a')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
