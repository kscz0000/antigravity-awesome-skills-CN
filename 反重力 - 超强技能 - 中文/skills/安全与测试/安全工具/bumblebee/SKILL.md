---
name: bumblebee
description: "在 macOS/Linux 上运行 Bumblebee 供应链清点与暴露面扫描，以检测受损的包、扩展及 MCP 宿主配置。供应链安全、暴露面审计、事件响应、供应链清点、暴露目录匹配、Bumblebee 扫描、NDJSON 报告。"
category: security
risk: safe
source: community
source_repo: mycelos-ai/bumblebee-skill
source_type: community
date_added: "2026-05-27"
author: stefan-kp
tags: [security, supply-chain, incident-response, npm, pypi, tooling]
tools: [claude]
license: "MIT"
license_source: "https://github.com/mycelos-ai/bumblebee-skill/blob/main/LICENSE"
---

# Bumblebee 安全扫描

Bumblebee（https://github.com/perplexityai/bumblebee）是一个只读清点收集器，能够在开发者终端上呈现包、扩展以及开发工具的元数据。它回答的是一个聚焦的供应链问题：当某条告警指出一个包或版本时，本机上此刻是否真的存在匹配项？

本技能负责端到端地驱动一次完整的 Bumblebee 扫描：

1. 确认 `go` 已加入 `PATH`（缺失时给出安装指引）。
2. 检查或安装 `bumblebee` 可执行文件。
3. 运行指定的扫描画像（`baseline`、`project` 或 `deep`）。
4. 将原始 NDJSON 输出与 Markdown 报告一起保存到用户的工作区。
5. 在对话回复中总结结论——尤其是与暴露目录匹配的部分。

与用户交流时使用其当前使用的语言（Stefan 使用德语）。代码、提交信息以及落盘的文件内容保持英文，以贴合现有项目规范。

## 何时使用本技能

当告警、事件报告或暴露目录提及了可能存在于本地 macOS 或 Linux 开发者终端上的受损包、开发工具、浏览器/编辑器扩展，或者 MCP 宿主配置时，使用本技能。

仅将其用于只读的清点与暴露面核查。不要用它去修补、卸载、隔离或以其他方式改动被扫描的机器。

## 步骤一 —— 明确扫描请求

在动手之前，除非消息中已明确说明，否则通过 `AskUserQuestion` 与用户确认两点：

- **画像（Profile）**：`baseline`（全局包根目录）、`project`（特定的开发目录，例如 `~/code`），或 `deep`（显式 `--root` 路径，可在事件响应中包含 `$HOME`）。
- **根目录（Roots）**：对于 `project` 和 `deep` 画像，询问要扫描哪些目录。`deep` 是唯一允许使用裸家目录根的画像。

如果用户手头已经有告警或暴露目录文件，还需询问是否通过 `--exposure-catalog` 传入。本技能不自带目录——若用户问到，可以引导他们去 Bumblebee 仓库中的 `threat_intel/` 寻找现成的目录。

对于"lauf mal ne Baseline-Scan"这种一句话请求，可以跳过提问，直接跑 baseline。

## 步骤二 —— 检查 Go

在 bash 中执行 `command -v go && go version`。三种结果：

- **Go ≥ 1.25 已就绪** → 继续。
- **Go 已安装但 < 1.25** → 告知用户当前的版本，解释 Bumblebee 要求 Go 1.25+ 并停下，直到用户完成升级。
- **Go 缺失** → 不要自动安装 Go。给出与平台匹配的安装指引后停下：
  - macOS：`brew install go`（或从 https://go.dev/dl/ 下载）。
  - Debian/Ubuntu：首选 https://go.dev/dl/ 的官方压缩包，因为发行版仓库往往滞后；`sudo apt install golang-go` 仅作备选。
  - Fedora/RHEL：`sudo dnf install golang` 或使用官方压缩包。

安装完成后，用户必须确保 `$GOBIN`（或 `$HOME/go/bin`）已加入 `$PATH`，以便后续能定位到 `bumblebee`。

## 步骤三 —— 检查或安装 Bumblebee

执行 `command -v bumblebee && bumblebee version`。如果缺失：

```bash
go install github.com/perplexityai/bumblebee/cmd/bumblebee@latest
```

随后再次执行 `bumblebee version`。如果仍然找不到该可执行文件，很可能是用户的 `GOBIN`/`PATH` 配置有误——此时要输出解析后的 `go env GOPATH` 和 `go env GOBIN`，便于用户自行排查。不要静默退回到通过绝对路径运行该二进制；应明确告知用户发生了什么。

安装完成后，还需执行 `bumblebee selftest` 作为健全性检查。如果退出码非零，说明本地安装已损坏，此时不应继续扫描。

## 步骤四 —— 运行扫描

所有扫描都把 NDJSON 写入文件中。请使用工作目录作为输出位置，方便用户事后查看。

输出文件名（请使用用户工作区路径；下面的示例假设已设置 `$OUT`）：

- `bumblebee-<profile>-<UTC-timestamp>.ndjson` —— 原始记录。
- `bumblebee-<profile>-<UTC-timestamp>.report.md` —— Markdown 报告（在步骤五生成）。

为 `--max-duration` 设定一个合理的值，避免失控的扫描长时间挂起会话。经验性的默认值为：

- `baseline`：5m
- `project`：10m
- `deep`：15m（提醒用户扫描 `$HOME` 仍可能耗时更长，并主动询问是否上调上限）

始终将 stderr 重定向到一个同名的 `.log` 文件——Bumblebee 会向其中输出诊断性的 NDJSON，对解释不完整的扫描非常有帮助。

### Baseline

```bash
bumblebee scan --profile baseline \
  --max-duration 5m \
  > "$OUT/bumblebee-baseline-$TS.ndjson" \
  2> "$OUT/bumblebee-baseline-$TS.log"
```

可选项：当用户只关心 npm 和 PyPI 这类特定生态时，可限定范围：

```bash
bumblebee scan --profile baseline --ecosystem npm,pypi ...
```

### Project

每个 `--root` 都必须是一个已存在的绝对路径。该画像下拒绝使用裸 `$HOME`（Bumblebee 自身也会拒绝——需把报错信息清楚地反馈给用户）。

```bash
bumblebee scan --profile project \
  --root "$HOME/code" \
  --root "$HOME/Developer" \
  --max-duration 10m \
  > "$OUT/bumblebee-project-$TS.ndjson" \
  2> "$OUT/bumblebee-project-$TS.log"
```

### Deep

用于事件响应——允许使用范围更广的根目录，但应尽量搭配一个暴露目录以及 `--findings-only`，让输出保持聚焦。

```bash
bumblebee scan --profile deep \
  --root "$HOME" \
  --exposure-catalog "$CATALOG" \
  --findings-only \
  --max-duration 15m \
  > "$OUT/bumblebee-deep-$TS.ndjson" \
  2> "$OUT/bumblebee-deep-$TS.log"
```

如果用户没有可用的目录，请在不附加 `--findings-only` 的情况下执行 deep，并提醒他们 NDJSON 文件可能很大（在开发者机器上可达数百 MB）。

## 步骤五 —— 生成 Markdown 报告

运行自带的辅助脚本，把 NDJSON 转成人类可读的报告。该辅助脚本应从已安装的 Bumblebee 技能目录中解析得到；切勿从被扫描项目中以工作区相对路径运行 `scripts/render_report.py`。

```bash
BUMBLEBEE_SKILL_DIR="/absolute/path/to/the/bumblebee-skill-directory"
test -f "$BUMBLEBEE_SKILL_DIR/scripts/render_report.py"
python3 "$BUMBLEBEE_SKILL_DIR/scripts/render_report.py" \
  "$OUT/bumblebee-<profile>-$TS.ndjson" \
  "$OUT/bumblebee-<profile>-$TS.report.md"
```

该辅助脚本会按记录类型与生态进行分组，列出每条 `finding` 记录及其对应的目录条目和严重等级，并嵌入 `scan_summary` 以便追溯。它只依赖 Python 3 标准库——无需 `pip install`。

如果 `render_report.py` 退出码非零（例如 NDJSON 格式损坏、缺少 summary），应把 stderr 反馈给用户，而不是默默产出一份空报告。

## 步骤六 —— 呈现结果

在本次回复的结尾给出：

- 聊天中的简短总结：画像、根目录、记录数量，以及最重要的——任何带有严重等级的发现。如果发现数为零，必须明确说明；对发现保持沉默很容易被误读。
- 提供 `computer://` 链接，分别指向 NDJSON 和 Markdown 报告，便于用户直接打开。
- 如果 `.log` 文件中的诊断信息表明存在被跳过的根目录或读取错误，请一并提及并附上日志链接。

不要在聊天中粘贴大段 NDJSON——它噪声很大，也不利于用户阅读。

## 安全与隐私注意事项

- Bumblebee 在设计上就是只读的。请不要在本技能内部提议修补、删除或执行 `npm uninstall` 之类的动作；用户在清楚哪些东西受到影响后，会自行执行修复。
- MCP 宿主配置中的 `env` 字段可能携带密钥。Bumblebee 不会输出这些值，但 `.log` 文件中仍可能包含敏感配置文件的路径。请把这些输出文件当作含清点数据的资产对待，未经用户明确同意，不要上传到第三方服务（与 DSGVO 相关）。
- 切勿以提升后的权限运行 `bumblebee`（即使用 `sudo`）。它用于检视当前用户的开发环境，而非整个系统。

## 需关注的失败模式

- 在 `go install` 之后出现 `bumblebee: command not found` → 几乎总是 `PATH`/`GOBIN` 问题。可输出 `go env GOPATH GOBIN PATH` 来协助排查。
- `refusing to scan bare home with profile baseline` → 把 `$HOME` 改用 `deep` 画像，或为 `project` 选用一个子目录。
- 扫描超时 → 应收窄 `--root` 范围、按 `--ecosystem` 限定或上调 `--max-duration`，不要盲目循环重试。
- 暴露目录被拒收 → 检查 JSON 是否同时包含 `schema_version` 和 `entries`（裸顶层数组会被拒收），并确认 `schema_version` 是 Bumblebee 能识别的版本。

## 局限性

- 本技能只汇报本地的清点结果与暴露匹配项，并不会对受影响的包、扩展或配置执行修复。
- 扫描覆盖范围取决于 Bumblebee 所支持的生态、所选的根目录以及当前用户的文件系统权限。
- 结果是某一时刻的证据，在包安装、依赖更新或事件响应变更之后需要重新扫描。

## 参考

报告的版式可参考 `scripts/render_report.py`。Bumblebee 自身的文档位于 https://github.com/perplexityai/bumblebee——当问题超出本技能覆盖范围时，可查阅 `docs/inventory-sources.md`、`docs/transport.md` 与 `docs/state-model.md`。

## 致谢

Bumblebee 由 Perplexity 开发（https://github.com/perplexityai/bumblebee，Apache-2.0）。其扫描逻辑、输出格式以及暴露目录的语义均归该上游项目所有。本仓库只是在官方 `bumblebee` CLI 之上封装的一个轻量 Claude 技能；包装层本身采用 MIT 许可（详见 `LICENSE`）。
