---
name: computer-use-agents
description: 构建像人类一样与计算机交互的 AI 智能体 -
  查看屏幕、移动光标、点击按钮和输入文本。涵盖
  Anthropic 的 Computer Use、OpenAI 的 Operator/CUA 以及开源替代方案。
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 计算机使用智能体

构建像人类一样与计算机交互的 AI 智能体 - 查看屏幕、移动光标、点击按钮和输入文本。涵盖 Anthropic 的 Computer Use、OpenAI 的 Operator/CUA 以及开源替代方案。重点关注沙箱化、安全性以及处理基于视觉控制的独特挑战。

## 模式

### 感知-推理-行动循环

计算机使用智能体的基础架构：观察屏幕，推理下一步行动，执行行动，重复。该循环通过迭代管道将视觉模型与行动执行集成。

关键组件：
1. 感知：截图捕获当前屏幕状态
2. 推理：视觉-语言模型分析并规划
3. 行动：执行鼠标/键盘操作
4. 反馈：观察结果，继续或纠正

关键洞察：视觉智能体在"思考"阶段（1-5秒）完全静止，形成可检测的暂停模式。

**何时使用**：从零构建任何计算机使用智能体，将视觉模型与桌面控制集成，理解智能体行为模式

from anthropic import Anthropic
from PIL import Image
import base64
import pyautogui
import time

class ComputerUseAgent:
    """
    感知-推理-行动循环实现。
    基于 Anthropic Computer Use 模式。
    """

    def __init__(self, client: Anthropic, model: str = "claude-sonnet-4-20250514"):
        self.client = client
        self.model = model
        self.max_steps = 50  # 防止无限循环
        self.action_delay = 0.5  # 操作间隔秒数

    def capture_screenshot(self) -> str:
        """捕获屏幕并返回 base64 编码图像。"""
        screenshot = pyautogui.screenshot()
        # 调整大小以节省 token（1280x800 是较好的平衡）
        screenshot = screenshot.resize((1280, 800), Image.LANCZOS)

        import io
        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

    def execute_action(self, action: dict) -> dict:
        """在计算机上执行鼠标/键盘操作。"""
        action_type = action.get("type")

        if action_type == "click":
            x, y = action["x"], action["y"]
            button = action.get("button", "left")
            pyautogui.click(x, y, button=button)
            return {"success": True, "action": f"clicked at ({x}, {y})"}

        elif action_type == "type":
            text = action["text"]
            pyautogui.typewrite(text, interval=0.02)
            return {"success": True, "action": f"typed {len(text)} chars"}

        elif action_type == "key":
            key = action["key"]
            pyautogui.press(key)
            return {"success": True, "action": f"pressed {key}"}

        elif action_type == "scroll":
            direction = action.get("direction", "down")
            amount = action.get("amount", 3)
            scroll = -amount if direction == "down" else amount
            pyautogui.scroll(scroll)
            return {"success": True, "action": f"scrolled {direction}"}

        elif action_type == "move":
            x, y = action["x"], action["y"]
            pyautogui.moveTo(x, y)
            return {"success": True, "action": f"moved to ({x}, {y})"}

        else:
            return {"success": False, "error": f"Unknown action: {action_type}"}

    def run(self, task: str) -> dict:
        """
        运行感知-推理-行动循环直到任务完成。

        循环流程：
        1. 截图当前状态
        2. 发送至视觉模型并附带任务上下文
        3. 从响应中解析行动
        4. 执行行动
        5. 重复直到完成或达到最大步数
        """
        messages = []
        step_count = 0

        system_prompt = """你是一个计算机使用智能体。你可以看到屏幕
        并控制鼠标/键盘。

        可用操作（以 JSON 响应）：
        - {"type": "click", "x": 100, "y": 200, "button": "left"}
        - {"type": "type", "text": "hello world"}
        - {"type": "key", "key": "enter"}
        - {"type": "scroll", "direction": "down", "amount": 3}
        - {"type": "done", "result": "task completed successfully"}

        始终仅以 JSON 操作对象响应。
        坐标要精确 - 准确点击所需位置。
        如果发现错误，尝试恢复。
        """

        while step_count < self.max_steps:
            step_count += 1

            # 1. 感知：捕获当前屏幕
            screenshot_b64 = self.capture_screenshot()

            # 2. 推理：发送至视觉模型
            user_content = [
                {"type": "text", "text": f"Task: {task}\n\nStep {step_count}. What action should I take?"},
                {"type": "image", "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": screenshot_b64
                }}
            ]

            messages.append({"role": "user", "content": user_content})

            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=messages
            )

            assistant_message = response.content[0].text
            messages.append({"role": "assistant", "content": assistant_message})

            # 3. 从响应中解析行动
            import json
            try:
                action = json.loads(assistant_message)
            except json.JSONDecodeError:
                # 尝试从响应中提取 JSON
                import re
                match = re.search(r'\{[^}]+\}', assistant_message)
                if match:
                    action = json.loads(match.group())
                else:
                    continue

            # 检查是否完成
            if action.get("type") == "done":
                return {
                    "success": True,
                    "result": action.get("result"),
                    "steps": step_count
                }

            # 4. 行动：执行
            result = self.execute_action(action)

            # 短暂延迟等待 UI 更新
            time.sleep(self.action_delay)

        return {
            "success": False,
            "error": "Max steps reached",
            "steps": step_count
        }

# 使用示例
agent = ComputerUseAgent(Anthropic())
result = agent.run("Open Chrome and search for 'weather today'")

### 反模式

- 不设步数限制运行（无限循环）
- 操作之间无延迟（UI 来不及响应）
- 全分辨率截图（token 爆炸）
- 忽略操作失败（无恢复机制）

### 沙箱化环境模式

计算机使用智能体必须在隔离的沙箱环境中运行。
切勿让智能体直接访问你的主系统 - 安全风险太高。使用带有虚拟桌面的 Docker 容器。

关键隔离要求：
1. 网络：仅限必要的端点
2. 文件系统：只读或限定在临时目录
3. 凭证：无法访问主机凭证
4. 系统调用：过滤危险系统调用
5. 资源：限制 CPU、内存、时间

目标是"爆炸半径最小化" - 如果智能体出错，损害仅限于沙箱内。

**何时使用**：部署任何计算机使用智能体，安全测试智能体行为，运行不受信任的自动化任务

# 沙箱化计算机使用环境的 Dockerfile
# 基于 Anthropic 参考实现模式

FROM ubuntu:22.04

# 安装桌面环境
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    fluxbox \
    xterm \
    firefox \
    python3 \
    python3-pip \
    supervisor

# 安全：创建非 root 用户
RUN useradd -m -s /bin/bash agent && \
    mkdir -p /home/agent/.vnc

# 安装 Python 依赖
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

# 安全：移除能力
RUN apt-get install -y --no-install-recommends libcap2-bin && \
    setcap -r /usr/bin/python3 || true

# 复制智能体代码
COPY --chown=agent:agent . /app
WORKDIR /app

# 虚拟显示器 + VNC 的 Supervisor 配置
COPY supervisord.conf /etc/supervisor/conf.d/

# 仅暴露 VNC 端口（不直接暴露桌面）
EXPOSE 5900

# 以非 root 用户运行
USER agent

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

---

# 带安全约束的 docker-compose.yml
version: '3.8'

services:
  computer-use-agent:
    build: .
    ports:
      - "5900:5900"  # VNC 用于观察
      - "8080:8080"  # API 用于控制

    # 安全约束
    security_opt:
      - no-new-privileges:true
      - seccomp:seccomp-profile.json

    # 资源限制
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '0.5'
          memory: 1G

    # 网络隔离
    networks:
      - agent-network

    # 无法访问主机文件系统
    volumes:
      - agent-tmp:/tmp

    # 只读根文件系统
    read_only: true
    tmpfs:
      - /run
      - /var/run

    # 环境变量
    environment:
      - DISPLAY=:99
      - NO_PROXY=localhost

networks:
  agent-network:
    driver: bridge
    internal: true  # 默认无互联网访问

volumes:
  agent-tmp:

---

# 带额外运行时沙箱化的 Python 封装
import subprocess
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class SandboxConfig:
    """智能体沙箱配置。"""
    network_allowed: list[str] = None  # 允许的域名
    max_runtime_seconds: int = 300
    max_memory_mb: int = 2048
    allow_downloads: bool = False
    allow_clipboard: bool = False

class SandboxedAgent:
    """
    在 Docker 沙箱中运行计算机使用智能体。
    """

    def __init__(self, config: SandboxConfig):
        self.config = config
        self.container_id: Optional[str] = None

    def start(self):
        """启动沙箱化环境。"""
        # 构建网络规则
        network_rules = ""
        if self.config.network_allowed:
            for domain in self.config.network_allowed:
                network_rules += f"--add-host={domain}:$(dig +short {domain}) "
        else:
            network_rules = "--network=none"

        cmd = f"""
        docker run -d \
            --name computer-use-sandbox-$$ \
            --security-opt no-new-privileges \
            --cap-drop ALL \
            --memory {self.config.max_memory_mb}m \
            --cpus 2 \
            --read-only \
            --tmpfs /tmp \
            {network_rules} \
            computer-use-agent:latest
        """

        result = subprocess.run(cmd, shell=True, capture_output=True)
        self.container_id = result.stdout.decode().strip()

        # 设置终止计时器
        subprocess.Popen([
            "sh", "-c",
            f"sleep {self.config.max_runtime_seconds} && docker kill {self.container_id}"
        ])

        return self.container_id

    def execute_task(self, task: str) -> dict:
        """在沙箱中执行任务。"""
        if not self.container_id:
            self.start()

        # 通过 API 发送任务给智能体
        import requests
        response = requests.post(
            f"http://localhost:8080/task",
            json={"task": task},
            timeout=self.config.max_runtime_seconds
        )

        return response.json()

    def stop(self):
        """停止并移除沙箱。"""
        if self.container_id:
            subprocess.run(f"docker rm -f {self.container_id}", shell=True)
            self.container_id = None

### 反模式

- 直接在主机系统上运行智能体
- 给沙箱完整的网络访问权限
- 在容器中以 root 运行
- 无资源限制（拒绝服务风险）
- 持久化存储（数据可能在运行间泄露）

### Anthropic Computer Use 实现

使用 Claude 计算机使用能力的官方实现模式。
Claude 3.5 Sonnet 是首个提供计算机使用能力的前沿模型。
Claude Opus 4.5 现在是"世界上最好的计算机使用模型"。

关键能力：
- screenshot：捕获当前屏幕状态
- mouse：点击、移动、拖拽操作
- keyboard：输入文本、按键
- bash：运行 shell 命令
- text_editor：查看和编辑文件

工具版本：
- computer_20251124（Opus 4.5）：新增缩放操作用于详细检查
- computer_20250124（所有其他模型）：标准能力

关键限制："某些 UI 元素（如下拉菜单和滚动条）对 Claude 来说可能难以操作" - Anthropic 文档

**何时使用**：构建生产级计算机使用智能体，需要最高质量的视觉理解，完整的桌面控制（不仅是浏览器）

from anthropic import Anthropic
from anthropic.types.beta import (
    BetaToolComputerUse20241022,
    BetaToolBash20241022,
    BetaToolTextEditor20241022,
)
import subprocess
import base64
from PIL import Image
import io

class AnthropicComputerUse:
    """
    官方 Anthropic Computer Use 实现。

    需要：
    - 带虚拟显示器的 Docker 容器
    - 用于查看智能体操作的 VNC
    - 正确的工具实现
    """

    def __init__(self):
        self.client = Anthropic()
        self.model = "claude-sonnet-4-20250514"  # 最适合计算机使用
        self.screen_size = (1280, 800)

    def get_tools(self) -> list:
        """定义计算机使用工具。"""
        return [
            BetaToolComputerUse20241022(
                type="computer_20241022",
                name="computer",
                display_width_px=self.screen_size[0],
                display_height_px=self.screen_size[1],
            ),
            BetaToolBash20241022(
                type="bash_20241022",
                name="bash",
            ),
            BetaToolTextEditor20241022(
                type="text_editor_20241022",
                name="str_replace_editor",
            ),
        ]

    def execute_tool(self, name: str, input: dict) -> dict:
        """执行工具并返回结果。"""

        if name == "computer":
            return self._handle_computer_action(input)
        elif name == "bash":
            return self._handle_bash(input)
        elif name == "str_replace_editor":
            return self._handle_editor(input)
        else:
            return {"error": f"Unknown tool: {name}"}

    def _handle_computer_action(self, input: dict) -> dict:
        """处理计算机控制操作。"""
        action = input.get("action")

        if action == "screenshot":
            # 通过 xdotool/scrot 捕获
            subprocess.run(["scrot", "/tmp/screenshot.png"])

            with open("/tmp/screenshot.png", "rb") as f:
                img_data = f.read()

            # 调整大小以提高效率
            img = Image.open(io.BytesIO(img_data))
            img = img.resize(self.screen_size, Image.LANCZOS)

            buffer = io.BytesIO()
            img.save(buffer, format="PNG")

            return {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": base64.b64encode(buffer.getvalue()).decode()
                }
            }

        elif action == "mouse_move":
            x, y = input.get("coordinate", [0, 0])
            subprocess.run(["xdotool", "mousemove", str(x), str(y)])
            return {"success": True}

        elif action == "left_click":
            subprocess.run(["xdotool", "click", "1"])
            return {"success": True}

        elif action == "right_click":
            subprocess.run(["xdotool", "click", "3"])
            return {"success": True}

        elif action == "double_click":
            subprocess.run(["xdotool", "click", "--repeat", "2", "1"])
            return {"success": True}

        elif action == "type":
            text = input.get("text", "")
            # 使用 xdotool type 并加延迟以提高可靠性
            subprocess.run(["xdotool", "type", "--delay", "50", text])
            return {"success": True}

        elif action == "key":
            key = input.get("key", "")
            # 映射常见键名
            key_map = {
                "return": "Return",
                "enter": "Return",
                "tab": "Tab",
                "escape": "Escape",
                "backspace": "BackSpace",
            }
            xdotool_key = key_map.get(key.lower(), key)
            subprocess.run(["xdotool", "key", xdotool_key])
            return {"success": True}

        elif action == "scroll":
            direction = input.get("direction", "down")
            amount = input.get("amount", 3)
            button = "5" if direction == "down" else "4"
            for _ in range(amount):
                subprocess.run(["xdotool", "click", button])
            return {"success": True}

        return {"error": f"Unknown action: {action}"}

    def _handle_bash(self, input: dict) -> dict:
        """执行 bash 命令。"""
        command = input.get("command", "")

        # 安全：清理和限制命令
        dangerous_patterns = ["rm -rf", "mkfs", "dd if=", "> /dev/"]
        for pattern in dangerous_patterns:
            if pattern in command:
                return {"error": "Dangerous command blocked"}

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "stdout": result.stdout[:10000],  # 限制输出
                "stderr": result.stderr[:1000],
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out"}

    def _handle_editor(self, input: dict) -> dict:
        """处理文本编辑器操作。"""
        command = input.get("command")
        path = input.get("path")

        if command == "view":
            try:
                with open(path, "r") as f:
                    content = f.read()
                return {"content": content[:50000]}  # 限制大小
            except Exception as e:
                return {"error": str(e)}

        elif command == "str_replace":
            old_str = input.get("old_str")
            new_str = input.get("new_str")
            try:
                with open(path, "r") as f:
                    content = f.read()
                if old_str not in content:
                    return {"error": "old_str not found in file"}
                content = content.replace(old_str, new_str, 1)
                with open(path, "w") as f:
                    f.write(content)
                return {"success": True}
            except Exception as e:
                return {"error": str(e)}

        return {"error": f"Unknown editor command: {command}"}

    def run_task(self, task: str, max_steps: int = 50) -> dict:
        """以智能体循环运行计算机使用任务。"""
        messages = [{"role": "user", "content": task}]
        tools = self.get_tools()

        for step in range(max_steps):
            response = self.client.beta.messages.create(
                model=self.model,
                max_tokens=4096,
                tools=tools,
                messages=messages,
                betas=["computer-use-2024-10-22"]
            )

            # 检查是否完成
            if response.stop_reason == "end_turn":
                return {
                    "success": True,
                    "result": response.content[0].text if response.content else "",
                    "steps": step + 1
                }

            # 处理工具使用
            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = self.execute_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        })

                messages.append({"role": "user", "content": tool_results})

        return {"success": False, "error": "Max steps reached"}

### 反模式

- 不使用 betas=['computer-use-2024-10-22'] 标志
- 全分辨率截图（浪费资源）
- bash 工具无命令清理
- 无限执行时间

### 浏览器使用模式（基于 Playwright）

对于仅浏览器的自动化，使用结构化 DOM 访问比基于像素的计算机使用更高效。Playwright MCP 允许 LLM 使用无障碍快照而非截图来控制浏览器。

相比基于视觉的优势：
- 更快：无需图像处理
- 更便宜：文本 token vs 图像 token
- 更精确：直接元素定位
- 更可靠：无坐标漂移

何时使用视觉 vs 结构化：
- 视觉：桌面应用、复杂 UI、视觉验证
- 结构化：Web 自动化、表单填写、数据提取

**何时使用**：仅浏览器自动化任务，表单填写和 Web 交互，速度和成本比视觉理解更重要时

from playwright.async_api import async_playwright
from dataclasses import dataclass
from typing import Optional
import asyncio

@dataclass
class BrowserAction:
    """结构化浏览器操作。"""
    action: str  # click, type, navigate, scroll, extract
    selector: Optional[str] = None
    text: Optional[str] = None
    url: Optional[str] = None

class BrowserUseAgent:
    """
    使用 Playwright 和结构化命令的浏览器自动化。
    对于 Web 任务比基于像素的方式更高效。
    """

    def __init__(self):
        self.browser = None
        self.page = None

    async def start(self, headless: bool = True):
        """启动浏览器会话。"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.page = await self.browser.new_page()

    async def get_page_snapshot(self) -> dict:
        """
        获取页面的结构化快照供 LLM 使用。
        使用无障碍树提高效率。
        """
        # 获取无障碍树
        snapshot = await self.page.accessibility.snapshot()

        # 获取简化的 DOM 信息
        elements = await self.page.evaluate('''() => {
            const interactable = [];
            const selector = 'a, button, input, select, textarea, [role="button"]';
            document.querySelectorAll(selector).forEach((el, i) => {
                const rect = el.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    interactable.push({
                        index: i,
                        tag: el.tagName.toLowerCase(),
                        text: el.textContent?.trim().slice(0, 100),
                        type: el.type,
                        placeholder: el.placeholder,
                        name: el.name,
                        id: el.id,
                        class: el.className
                    });
                }
            });
            return interactable;
        }''')

        return {
            "url": self.page.url,
            "title": await self.page.title(),
            "accessibility_tree": snapshot,
            "interactable_elements": elements[:50]  # 限制以节省 token
        }

    async def execute_action(self, action: BrowserAction) -> dict:
        """执行结构化浏览器操作。"""

        try:
            if action.action == "navigate":
                await self.page.goto(action.url, wait_until="domcontentloaded")
                return {"success": True, "url": self.page.url}

            elif action.action == "click":
                await self.page.click(action.selector, timeout=5000)
                await self.page.wait_for_load_state("networkidle", timeout=5000)
                return {"success": True}

            elif action.action == "type":
                await self.page.fill(action.selector, action.text)
                return {"success": True}

            elif action.action == "scroll":
                direction = action.text or "down"
                distance = 500 if direction == "down" else -500
                await self.page.evaluate(f"window.scrollBy(0, {distance})")
                return {"success": True}

            elif action.action == "extract":
                # 提取文本内容
                if action.selector:
                    text = await self.page.text_content(action.selector)
                else:
                    text = await self.page.text_content("body")
                return {"success": True, "text": text[:5000]}

            elif action.action == "screenshot":
                # 需要时回退到视觉方式
                screenshot = await self.page.screenshot(type="png")
                import base64
                return {
                    "success": True,
                    "image": base64.b64encode(screenshot).decode()
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

        return {"success": False, "error": f"Unknown action: {action.action}"}

    async def run_with_llm(self, task: str, llm_client, max_steps: int = 20):
        """
        使用 LLM 决策运行浏览器任务。
        使用结构化 DOM 而非截图。
        """

        system_prompt = """你是一个浏览器自动化智能体。你接收
        包含可交互元素的页面快照并决定操作。

        以 JSON 操作响应：
        - {"action": "navigate", "url": "https://..."}
        - {"action": "click", "selector": "button.submit"}
        - {"action": "type", "selector": "input[name='email']", "text": "..."}
        - {"action": "scroll", "text": "down"}
        - {"action": "extract", "selector": ".results"}
        - {"action": "done", "result": "task completed"}

        根据提供的元素信息使用 CSS 选择器。
        选择器优先级：id > name > class > 文本内容。
        """

        messages = []

        for step in range(max_steps):
            # 获取当前页面状态
            snapshot = await self.get_page_snapshot()

            user_message = f"""Task: {task}

            Current page:
            URL: {snapshot['url']}
            Title: {snapshot['title']}

            Interactable elements:
            {snapshot['interactable_elements']}

            What action should I take?"""

            messages.append({"role": "user", "content": user_message})

            # 获取 LLM 决策
            response = llm_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=system_prompt,
                messages=messages
            )

            assistant_text = response.content[0].text
            messages.append({"role": "assistant", "content": assistant_text})

            # 解析并执行
            import json
            action_dict = json.loads(assistant_text)

            if action_dict.get("action") == "done":
                return {"success": True, "result": action_dict.get("result")}

            action = BrowserAction(**action_dict)
            result = await self.execute_action(action)

            if not result.get("success"):
                messages.append({
                    "role": "user",
                    "content": f"Action failed: {result.get('error')}"
                })

            await asyncio.sleep(0.5)  # 速率限制

        return {"success": False, "error": "Max steps reached"}

    async def close(self):
        """清理浏览器。"""
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()

# 使用示例
async def main():
    agent = BrowserUseAgent()
    await agent.start(headless=False)

    from anthropic import Anthropic
    result = await agent.run_with_llm(
        "Go to weather.com and find the weather for New York",
        Anthropic()
    )

    print(result)
    await agent.close()

asyncio.run(main())

### 反模式

- DOM 访问可用时仍使用截图
- 不等待页面加载
- 使用会失效的硬编码选择器
- 对过期元素无错误恢复

### 用户确认模式

对于敏感操作，智能体应暂停并请求人工确认。
"ChatGPT 智能体在执行购买等敏感步骤前也会暂停并请求确认。"

敏感级别：
1. 低：导航、读取（自动批准）
2. 中：表单填写、点击（记录日志，可能确认）
3. 高：购买、认证、文件操作（始终确认）
4. 关键：凭证输入、金融交易（确认 + 审查）

**何时使用**：具有现实后果的操作，金融交易，认证流程，文件修改

from enum import Enum
from dataclasses import dataclass
from typing import Callable, Optional
import asyncio

class ActionSeverity(Enum):
    LOW = "low"           # 自动批准
    MEDIUM = "medium"     # 记录日志，可选确认
    HIGH = "high"         # 始终确认
    CRITICAL = "critical" # 确认 + 审查详情

@dataclass
class SensitiveAction:
    """可能需要用户确认的操作。"""
    action_type: str
    description: str
    severity: ActionSeverity
    details: dict

class ConfirmationGate:
    """
    通过用户确认来门控敏感操作。
    """

    # 操作类型 -> 敏感级别映射
    ACTION_SEVERITY = {
        # 低 - 自动批准
        "navigate": ActionSeverity.LOW,
        "scroll": ActionSeverity.LOW,
        "read": ActionSeverity.LOW,
        "screenshot": ActionSeverity.LOW,

        # 中 - 记录日志并可能确认
        "click": ActionSeverity.MEDIUM,
        "type": ActionSeverity.MEDIUM,
        "search": ActionSeverity.MEDIUM,

        # 高 - 始终确认
        "download": ActionSeverity.HIGH,
        "submit_form": ActionSeverity.HIGH,
        "login": ActionSeverity.HIGH,
        "file_write": ActionSeverity.HIGH,

        # 关键 - 确认并完整审查
        "purchase": ActionSeverity.CRITICAL,
        "enter_password": ActionSeverity.CRITICAL,
        "enter_credit_card": ActionSeverity.CRITICAL,
        "send_money": ActionSeverity.CRITICAL,
        "delete": ActionSeverity.CRITICAL,
    }

    def __init__(
        self,
        confirm_callback: Callable[[SensitiveAction], bool] = None,
        auto_confirm_low: bool = True,
        auto_confirm_medium: bool = False
    ):
        self.confirm_callback = confirm_callback or self._default_confirm
        self.auto_confirm_low = auto_confirm_low
        self.auto_confirm_medium = auto_confirm_medium
        self.action_log = []

    def _default_confirm(self, action: SensitiveAction) -> bool:
        """通过 CLI 提示进行默认确认。"""
        print(f"\n{'='*60}")
        print(f"ACTION CONFIRMATION REQUIRED")
        print(f"{'='*60}")
        print(f"Type: {action.action_type}")
        print(f"Severity: {action.severity.value.upper()}")
        print(f"Description: {action.description}")
        print(f"Details: {action.details}")
        print(f"{'='*60}")

        while True:
            response = input("Allow this action? [y/n]: ").lower().strip()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False

    def classify_action(self, action_type: str, context: dict) -> ActionSeverity:
        """分类操作敏感级别，考虑上下文。"""
        base_severity = self.ACTION_SEVERITY.get(action_type, ActionSeverity.MEDIUM)

        # 根据上下文升级
        if context.get("involves_credentials"):
            return ActionSeverity.CRITICAL
        if context.get("involves_money"):
            return ActionSeverity.CRITICAL
        if context.get("irreversible"):
            return max(base_severity, ActionSeverity.HIGH, key=lambda x: x.value)

        return base_severity

    def check_action(
        self,
        action_type: str,
        description: str,
        details: dict = None
    ) -> tuple[bool, str]:
        """
        检查操作是否应继续。
        返回 (是否批准, 原因)。
        """
        details = details or {}
        severity = self.classify_action(action_type, details)

        action = SensitiveAction(
            action_type=action_type,
            description=description,
            severity=severity,
            details=details
        )

        # 记录所有操作
        self.action_log.append({
            "action": action,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })

        # 自动批准低敏感级别
        if severity == ActionSeverity.LOW and self.auto_confirm_low:
            return True, "auto-approved (low severity)"

        # 可能自动批准中敏感级别
        if severity == ActionSeverity.MEDIUM and self.auto_confirm_medium:
            return True, "auto-approved (medium severity)"

        # 请求确认
        approved = self.confirm_callback(action)

        if approved:
            return True, "user approved"
        else:
            return False, "user rejected"

class ConfirmedComputerUseAgent:
    """
    带确认门控的计算机使用智能体。
    """

    def __init__(self, base_agent, confirmation_gate: ConfirmationGate):
        self.agent = base_agent
        self.gate = confirmation_gate

    def execute_action(self, action: dict) -> dict:
        """带确认检查的操作执行。"""
        action_type = action.get("type", "unknown")

        # 构建描述
        if action_type == "click":
            desc = f"Click at ({action.get('x')}, {action.get('y')})"
        elif action_type == "type":
            text = action.get('text', '')
            # 如果看起来像密码则遮蔽
            if self._looks_sensitive(text):
                desc = f"Type sensitive text ({len(text)} chars)"
            else:
                desc = f"Type: {text[:50]}..."
        else:
            desc = f"Execute: {action_type}"

        # 用于敏感级别分类的上下文
        context = {
            "involves_credentials": self._looks_sensitive(action.get("text", "")),
            "involves_money": self._mentions_money(action),
        }

        # 通过门控检查
        approved, reason = self.gate.check_action(
            action_type, desc, context
        )

        if not approved:
            return {
                "success": False,
                "error": f"Action blocked: {reason}",
                "action": action_type
            }

        # 批准后执行
        return self.agent.execute_action(action)

    def _looks_sensitive(self, text: str) -> bool:
        """检查文本是否看起来像敏感数据。"""
        if not text:
            return False
        # 常见模式
        patterns = [
            r'\b\d{16}\b',  # 信用卡
            r'\b\d{3,4}\b.*\b\d{3,4}\b',  # 类似 CVV
            r'password',
            r'secret',
            r'api.?key',
            r'token'
        ]
        import re
        return any(re.search(p, text.lower()) for p in patterns)

    def _mentions_money(self, action: dict) -> bool:
        """检查操作是否涉及金钱。"""
        text = str(action)
        money_patterns = [
            r'\$\d+', r'pay', r'purchase', r'buy', r'checkout',
            r'credit', r'debit', r'invoice', r'payment'
        ]
        import re
        return any(re.search(p, text.lower()) for p in money_patterns)

# 使用示例
gate = ConfirmationGate(
    auto_confirm_low=True,
    auto_confirm_medium=False  # 确认点击、输入等操作
)

agent = ConfirmedComputerUseAgent(base_agent, gate)
result = agent.execute_action({"type": "click", "x": 500, "y": 300})

### 反模式

- 自动批准所有操作
- 不记录被拒绝的操作
- 在确认中显示完整密码
- 确认无超时（永远挂起）

### 操作日志模式

所有计算机使用智能体的操作都应记录，用于：
1. 调试失败的自动化
2. 安全审计
3. 可复现性
4. 合规要求

日志格式应捕获：
- 时间戳
- 操作类型和参数
- 操作前/后截图
- 成功/失败状态
- 模型推理（如可用）

**何时使用**：生产级计算机使用部署，调试自动化失败，安全敏感环境

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any
import json
import os

@dataclass
class ActionLogEntry:
    """单条操作日志条目。"""
    timestamp: datetime
    action_type: str
    parameters: dict
    success: bool
    error: Optional[str] = None
    screenshot_before: Optional[str] = None  # 截图路径
    screenshot_after: Optional[str] = None
    model_reasoning: Optional[str] = None
    duration_ms: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "action_type": self.action_type,
            "parameters": self._sanitize_params(self.parameters),
            "success": self.success,
            "error": self.error,
            "screenshot_before": self.screenshot_before,
            "screenshot_after": self.screenshot_after,
            "model_reasoning": self.model_reasoning,
            "duration_ms": self.duration_ms
        }

    def _sanitize_params(self, params: dict) -> dict:
        """从参数中移除敏感数据。"""
        sanitized = {}
        sensitive_keys = ['password', 'secret', 'token', 'key', 'credit_card']

        for k, v in params.items():
            if any(s in k.lower() for s in sensitive_keys):
                sanitized[k] = "[REDACTED]"
            elif isinstance(v, str) and len(v) > 100:
                sanitized[k] = v[:100] + "...[truncated]"
            else:
                sanitized[k] = v

        return sanitized

@dataclass
class TaskSession:
    """完整的任务执行会话。"""
    session_id: str
    task: str
    start_time: datetime
    end_time: Optional[datetime] = None
    actions: list[ActionLogEntry] = field(default_factory=list)
    success: bool = False
    final_result: Optional[str] = None

class ActionLogger:
    """
    计算机使用智能体的全面操作日志记录。
    """

    def __init__(self, log_dir: str = "./agent_logs"):
        self.log_dir = log_dir
        self.screenshot_dir = os.path.join(log_dir, "screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)

        self.current_session: Optional[TaskSession] = None

    def start_session(self, task: str) -> str:
        """启动新的任务会话。"""
        import uuid
        session_id = str(uuid.uuid4())[:8]

        self.current_session = TaskSession(
            session_id=session_id,
            task=task,
            start_time=datetime.now()
        )

        return session_id

    def log_action(
        self,
        action_type: str,
        parameters: dict,
        success: bool,
        error: Optional[str] = None,
        screenshot_before: bytes = None,
        screenshot_after: bytes = None,
        model_reasoning: str = None,
        duration_ms: int = None
    ):
        """记录单条操作。"""
        if not self.current_session:
            raise RuntimeError("No active session")

        # 保存截图（如提供）
        screenshot_paths = {}
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        if screenshot_before:
            path = os.path.join(
                self.screenshot_dir,
                f"{self.current_session.session_id}_{timestamp_str}_before.png"
            )
            with open(path, "wb") as f:
                f.write(screenshot_before)
            screenshot_paths["before"] = path

        if screenshot_after:
            path = os.path.join(
                self.screenshot_dir,
                f"{self.current_session.session_id}_{timestamp_str}_after.png"
            )
            with open(path, "wb") as f:
                f.write(screenshot_after)
            screenshot_paths["after"] = path

        # 创建日志条目
        entry = ActionLogEntry(
            timestamp=datetime.now(),
            action_type=action_type,
            parameters=parameters,
            success=success,
            error=error,
            screenshot_before=screenshot_paths.get("before"),
            screenshot_after=screenshot_paths.get("after"),
            model_reasoning=model_reasoning,
            duration_ms=duration_ms
        )

        self.current_session.actions.append(entry)

        # 同时追加到运行中的日志文件
        self._append_to_log(entry)

    def _append_to_log(self, entry: ActionLogEntry):
        """追加条目到 JSONL 日志文件。"""
        log_file = os.path.join(
            self.log_dir,
            f"session_{self.current_session.session_id}.jsonl"
        )

        with open(log_file, "a") as f:
            f.write(json.dumps(entry.to_dict()) + "\n")

    def end_session(self, success: bool, result: str = None):
        """结束当前会话。"""
        if not self.current_session:
            return

        self.current_session.end_time = datetime.now()
        self.current_session.success = success
        self.current_session.final_result = result

        # 写入会话摘要
        summary_file = os.path.join(
            self.log_dir,
            f"session_{self.current_session.session_id}_summary.json"
        )

        summary = {
            "session_id": self.current_session.session_id,
            "task": self.current_session.task,
            "start_time": self.current_session.start_time.isoformat(),
            "end_time": self.current_session.end_time.isoformat(),
            "duration_seconds": (
                self.current_session.end_time -
                self.current_session.start_time
            ).total_seconds(),
            "total_actions": len(self.current_session.actions),
            "successful_actions": sum(
                1 for a in self.current_session.actions if a.success
            ),
            "failed_actions": sum(
                1 for a in self.current_session.actions if not a.success
            ),
            "success": success,
            "final_result": result
        }

        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        self.current_session = None

    def get_session_replay(self, session_id: str) -> list[dict]:
        """获取会话的所有操作用于回放/调试。"""
        log_file = os.path.join(self.log_dir, f"session_{session_id}.jsonl")

        actions = []
        with open(log_file, "r") as f:
            for line in f:
                actions.append(json.loads(line))

        return actions

# 与智能体集成
class LoggedComputerUseAgent:
    """带全面日志记录的计算机使用智能体。"""

    def __init__(self, base_agent, logger: ActionLogger):
        self.agent = base_agent
        self.logger = logger

    def run_task(self, task: str) -> dict:
        """带完整日志记录运行任务。"""
        session_id = self.logger.start_session(task)

        try:
            result = self._run_with_logging(task)
            self.logger.end_session(
                success=result.get("success", False),
                result=result.get("result")
            )
            return result
        except Exception as e:
            self.logger.end_session(success=False, result=str(e))
            raise

    def _run_with_logging(self, task: str) -> dict:
        """带操作日志记录的内部运行。"""
        # 这将封装基础智能体的 run 方法
        # 并记录每个操作
        pass

### 反模式

- 日志中未清理敏感数据
- 无限期存储截图（存储成本）
- 不轮转日志文件
- 同步日志记录（阻塞智能体）

## 关键陷阱

### Web 内容可以劫持你的智能体

严重程度：关键

场景：计算机使用智能体浏览网页

症状：
智能体突然执行意外操作。点击恶意链接。在钓鱼网站上输入凭证。下载不该下载的文件。忽略你的指令而遵循嵌入的命令。

为什么会出问题：
"虽然所有处理不受信任内容的智能体都面临提示注入风险，但浏览器使用以两种方式放大了这一风险。首先，攻击面非常广泛：每个网页、嵌入的文档、广告和动态加载的脚本都代表潜在的恶意指令载体。其次，浏览器智能体可以执行许多不同的操作——导航到 URL、填写表单、点击按钮、下载文件——攻击者可以利用这些操作。"

实际攻击已经发生：
- "Microsoft Copilot 智能体被包含恶意指令的电子邮件劫持，攻击者借此提取了整个 CRM 数据库。"
- "Google 的 Workspace 服务被操纵——日历邀请和电子邮件中隐藏的提示欺骗了 Gemini 智能体删除事件和暴露敏感消息。"

即使 1% 的攻击成功率在大规模下也意味着重大风险。

推荐修复方案：

## 纵深防御 - 没有单一解决方案有效

1. 沙箱化（最有效）：
   ```python
   # 带严格隔离的 Docker
   docker run \
       --security-opt no-new-privileges \
       --cap-drop ALL \
       --network none \  # 无互联网！
       --read-only \
       computer-use-agent
   ```

2. 基于分类器的检测：
   ```python
   def scan_for_injection(content: str) -> bool:
       """检测提示注入尝试。"""
       patterns = [
           r"ignore.*instructions",
           r"disregard.*previous",
           r"new.*instructions",
           r"you are now",
           r"act as if",
           r"pretend to be",
       ]
       return any(re.search(p, content.lower()) for p in patterns)

   # 处理前检查页面内容
   page_text = await page.text_content("body")
   if scan_for_injection(page_text):
       return {"error": "Potential injection detected"}
   ```

3. 敏感操作的用户确认：
   ```python
   SENSITIVE_ACTIONS = {"download", "submit", "login", "purchase"}

   if action_type in SENSITIVE_ACTIONS:
       if not await get_user_confirmation(action):
           return {"error": "User rejected action"}
   ```

4. 限定范围凭证：
   - 永远不要给智能体访问所有凭证的权限
   - 使用临时的、有限制的令牌
   - 任务完成后撤销

### 视觉智能体点击精确中心

严重程度：中

场景：智能体点击 UI 元素

症状：
智能体的点击可被检测为非人类。网站可能阻止智能体或弹出 CAPTCHA。反机器人系统标记交互。

为什么会出问题：
"当视觉模型识别一个按钮时，它计算中心点。点击坐标落在数学上精确的位置——通常是精确的元素中心或网格对齐的像素值。人类不会点击中心；他们的点击分布遵循目标周围的高斯模式。"

截图循环也产生可检测的模式：
"可预测的暂停。视觉智能体在'思考'阶段完全静止。模式看起来像：操作 → 完全静止（1-5秒）→ 操作 → 完全静止 → 操作。"

复杂的反机器人系统检测：
- 完美的中心点击
- "思考"期间无鼠标移动
- 操作间一致的时间间隔
- 缺乏微移动和犹豫

推荐修复方案：

## 为操作添加类人随机性

```python
import random
import time

def humanized_click(x: int, y: int) -> tuple[int, int]:
    """为点击坐标添加类人随机性。"""
    # 目标周围的高斯分布
    # 人类通常落在目标 ~10px 范围内
    x_offset = int(random.gauss(0, 5))
    y_offset = int(random.gauss(0, 5))

    return (x + x_offset, y + y_offset)

def humanized_delay():
    """添加类人操作间延迟。"""
    # 人类有可变的反应时间
    base_delay = random.uniform(0.3, 0.8)
    # 偶尔更长的停顿（阅读、思考）
    if random.random() < 0.2:
        base_delay += random.uniform(0.5, 2.0)
    time.sleep(base_delay)

def humanized_movement(from_pos: tuple, to_pos: tuple):
    """像人类一样沿曲线路径移动鼠标。"""
    # 贝塞尔曲线或类似方法
    # 人类不会沿直线移动
    steps = random.randint(10, 20)
    for i in range(steps):
        t = i / steps
        # 简单曲线近似
        x = from_pos[0] + (to_pos[0] - from_pos[0]) * t
        y = from_pos[1] + (to_pos[1] - from_pos[1]) * t
        # 添加抖动
        x += random.gauss(0, 2)
        y += random.gauss(0, 2)
        pyautogui.moveTo(int(x), int(y))
        time.sleep(0.01)
```

## 轮换用户代理和指纹

```python
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/...",
    # ... 更多真实用户代理
]

await page.set_extra_http_headers({
    "User-Agent": random.choice(USER_AGENTS)
})
```

### 下拉菜单、滚动条和拖拽不可靠

严重程度：高

场景：智能体与复杂 UI 元素交互

症状：
智能体无法选择下拉选项。滚动不如预期。拖放完全失败。悬停菜单在点击前消失。

为什么会出问题：
"Computer Use 目前在处理某些界面交互时存在困难，特别是滚动、拖拽和缩放操作。某些 UI 元素（如下拉菜单和滚动条）对 Claude 来说可能难以操作。"
- Anthropic 文档

为什么这些很难：
1. 下拉菜单：选项在点击后出现，需要第二次点击来选择
2. 滚动条：目标很小，需要精确定位
3. 拖拽：需要协调的鼠标按下、移动、鼠标释放
4. 悬停菜单：鼠标移开时消失
5. Canvas 元素：无语义信息可见

视觉模型看到的是像素，不是 DOM 结构。它们不"知道"下拉菜单是下拉菜单——必须从视觉线索推断。

推荐修复方案：

## 尽可能使用键盘替代方案

```python
# 不点击下拉菜单，改用键盘
async def select_dropdown_option(page, dropdown_selector, option_text):
    # 聚焦下拉菜单
    await page.click(dropdown_selector)
    await asyncio.sleep(0.3)

    # 使用键盘查找选项
    await page.keyboard.type(option_text[:3])  # 输入前几个字母
    await asyncio.sleep(0.2)
    await page.keyboard.press("Enter")
```

## 将复杂操作分解为步骤

```python
# 替代拖放
async def reliable_drag(page, source, target):
    # 步骤 1：点击并按住
    await page.mouse.move(source["x"], source["y"])
    await page.mouse.down()
    await asyncio.sleep(0.2)

    # 步骤 2：分步移动
    steps = 10
    for i in range(steps):
        x = source["x"] + (target["x"] - source["x"]) * i / steps
        y = source["y"] + (target["y"] - source["y"]) * i / steps
        await page.mouse.move(x, y)
        await asyncio.sleep(0.05)

    # 步骤 3：释放
    await page.mouse.move(target["x"], target["y"])
    await asyncio.sleep(0.1)
    await page.mouse.up()
```

## Web 场景回退到 DOM 访问

```python
# 如果视觉方式失败，尝试直接 DOM 操作
async def robust_select(page, select_selector, value):
    try:
        # 先尝试视觉方式
        await vision_agent.select(select_selector, value)
    except Exception:
        # 回退到直接 DOM
        await page.select_option(select_selector, value=value)
```

## 操作后添加验证

```python
async def verified_scroll(page, direction):
    # 获取当前滚动位置
    before = await page.evaluate("window.scrollY")

    # 尝试滚动
    await page.mouse.wheel(0, 500 if direction == "down" else -500)
    await asyncio.sleep(0.3)

    # 验证是否生效
    after = await page.evaluate("window.scrollY")
    if before == after:
        # 尝试替代方法
        await page.keyboard.press("PageDown" if direction == "down" else "PageUp")
```

### 智能体比人类慢 2-5 倍

严重程度：中

场景：自动化任何计算机任务

症状：
人类 1 分钟完成的任务智能体需要 3-5 分钟。用户抱怨速度慢。出现超时。

为什么会出问题：
"与人类操作员相比，该技术可能很慢，通常需要多次截图和分析循环。"

为什么这么慢：
1. 截图捕获：100-500ms
2. 视觉模型推理：每张截图 1-5 秒
3. 操作执行：200-500ms
4. 等待 UI 更新：500-1000ms
5. 每次操作总计：2-7 秒

需要 20 次操作的任务至少需要 40-140 秒。
人类完成相同操作需要 20-30 秒。

推荐修复方案：

## 接受这个权衡

计算机使用适用于：
- 人类不想做的任务（重复性）
- 可以在后台运行的任务
- 准确性 > 速度的任务

## 尽可能优化

```python
# 1. 降低截图分辨率
SCREEN_SIZE = (1280, 800)  # 不是 4K

# 2. 批量处理相似操作
# 替代：type "hello"，等待，type " world"
await page.type("hello world")

# 3. 并行化独立任务
# 同时运行多个沙箱化智能体

# 4. 缓存重复计算
# 如果截图相同，复用分析结果

# 5. 简单决策使用更小的模型
simple_model = "claude-haiku-..."  # 用于"任务是否完成？"
complex_model = "claude-sonnet-..."  # 用于复杂推理
```

## 设定合理预期

```python
# 估算任务时长
def estimate_duration(task_complexity: str) -> int:
    """估算任务时长（秒）。"""
    estimates = {
        "simple": 30,    # 单页，少量操作
        "medium": 120,   # 多页，中等操作
        "complex": 300,  # 多页，复杂交互
    }
    return estimates.get(task_complexity, 120)

# 通知用户
estimated = estimate_duration("medium")
print(f"Estimated completion: {estimated // 60}m {estimated % 60}s")
```

### 截图快速填满上下文窗口

严重程度：高

场景：长时间运行的计算机使用任务

症状：
智能体遗忘早期步骤。开始重复操作。随着任务推进错误增加。成本暴增。

为什么会出问题：
每张截图约 1500-3000 token。30 张截图的任务仅图片就使用 45,000-90,000 token——还不包括任何文本。

Claude 的上下文窗口是有限的。当满了时：
- 较早的上下文被丢弃
- 智能体失去对早期步骤的记忆
- 任务连贯性下降

"让智能体在多个上下文窗口中保持一致的进展仍然是一个开放问题。核心挑战是它们必须在离散会话中工作，每个新会话开始时都没有之前的记忆。" - Anthropic 工程博客

推荐修复方案：

## 实现上下文管理

```python
class ContextManager:
    """管理计算机使用的上下文窗口使用。"""

    MAX_SCREENSHOTS = 10  # 仅保留最近的截图
    MAX_TOKENS = 100000

    def __init__(self):
        self.messages = []
        self.screenshot_count = 0

    def add_screenshot(self, screenshot_b64: str, description: str):
        """添加截图并自动修剪。"""
        self.screenshot_count += 1

        # 仅保留最近的截图
        if self.screenshot_count > self.MAX_SCREENSHOTS:
            self._prune_old_screenshots()

        # 带描述存储以提供上下文
        self.messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": description},
                {"type": "image", "source": {...}}
            ]
        })

    def _prune_old_screenshots(self):
        """移除旧截图，保留文本摘要。"""
        new_messages = []
        screenshots_kept = 0

        for msg in reversed(self.messages):
            if self._has_image(msg):
                if screenshots_kept < self.MAX_SCREENSHOTS:
                    new_messages.insert(0, msg)
                    screenshots_kept += 1
                else:
                    # 转换为文本摘要
                    summary = self._summarize_screenshot(msg)
                    new_messages.insert(0, {
                        "role": msg["role"],
                        "content": summary
                    })
            else:
                new_messages.insert(0, msg)

        self.messages = new_messages

    def _summarize_screenshot(self, msg) -> str:
        """将截图摘要为文本。"""
        # 提取任何文本描述
        for content in msg.get("content", []):
            if content.get("type") == "text":
                return f"[Previous screenshot: {content['text']}]"
        return "[Previous screenshot - details pruned]"

    def add_checkpoint(self):
        """创建检查点摘要。"""
        summary = self._create_progress_summary()
        self.messages.append({
            "role": "user",
            "content": f"CHECKPOINT: {summary}"
        })
```

## 长任务使用检查点

```python
async def run_with_checkpoints(task: str, checkpoint_every: int = 10):
    """带周期性检查点运行任务。"""
    context = ContextManager()
    step = 0

    while not task_complete:
        step += 1

        # 执行操作...

        if step % checkpoint_every == 0:
            # 创建检查点
            context.add_checkpoint()

            # 可选：持久化到磁盘
            save_checkpoint(context, step)
```

## 分解为子任务

```python
# 替代一个 50 步的任务：
subtasks = [
    "Navigate to the website and login",
    "Find the settings page",
    "Update the email address to ...",
    "Save and verify the change"
]

for subtask in subtasks:
    result = await agent.run(subtask)
    if not result["success"]:
        handle_error(subtask, result)
        break
```

### 成本可能快速爆炸

严重程度：高

场景：大规模运行计算机使用

症状：
API 账单比预期高 10 倍。单个任务花费 $5+ 而非 $0.50。月度成本快速达到数千美元。

为什么会出问题：
视觉 token 很贵。每张截图：
- 每张图片约 2000-3000 token
- 以 $10/百万 token 计，每张截图 $0.02-0.03
- 30 张截图的任务 = 仅图片就 $0.60-0.90

但它是复合增长的：
- 截图在上下文中累积
- 模型每轮看到所有之前的截图
- 第 10 轮处理 10 张截图 = $0.20-0.30
- 第 20 轮处理 20 张截图 = $0.40-0.60
- 二次增长！

复杂任务：50 轮 × 平均 25 张图片在上下文中 = 1250 个图片 token
加上文本 = 每个任务可能轻松达到 $5-10。

推荐修复方案：

## 监控和限制成本

```python
class CostTracker:
    """跟踪和限制计算机使用成本。"""

    # Anthropic 定价（近似）
    INPUT_COST_PER_1K = 0.003   # 文本
    OUTPUT_COST_PER_1K = 0.015
    IMAGE_COST_PER_1K = 0.01    # 大致

    def __init__(self, max_cost_per_task: float = 1.0):
        self.max_cost = max_cost_per_task
        self.current_cost = 0.0
        self.total_tokens = 0

    def add_turn(
        self,
        input_tokens: int,
        output_tokens: int,
        image_tokens: int
    ):
        """跟踪单轮成本。"""
        cost = (
            input_tokens / 1000 * self.INPUT_COST_PER_1K +
            output_tokens / 1000 * self.OUTPUT_COST_PER_1K +
            image_tokens / 1000 * self.IMAGE_COST_PER_1K
        )
        self.current_cost += cost
        self.total_tokens += input_tokens + output_tokens + image_tokens

        if self.current_cost > self.max_cost:
            raise CostLimitExceeded(
                f"Cost limit exceeded: ${self.current_cost:.2f} > ${self.max_cost:.2f}"
            )

        return cost

class CostLimitExceeded(Exception):
    pass

# 使用示例
tracker = CostTracker(max_cost_per_task=2.0)

try:
    for turn in turns:
        tracker.add_turn(turn.input, turn.output, turn.images)
except CostLimitExceeded:
    print("Task aborted due to cost limit")
```

## 降低图像成本

```python
# 1. 降低分辨率
SCREEN_SIZE = (1024, 768)  # 更小 = 更少 token

# 2. 用 JPEG 替代 PNG（质量可接受时）
screenshot.save(buffer, format="JPEG", quality=70)

# 3. 裁剪到相关区域
def crop_relevant(screenshot: Image, focus_area: tuple):
    """裁剪到关注区域。"""
    return screenshot.crop(focus_area)

# 4. 不必每轮都包含截图
if not needs_visual_update:
    # 仅文本轮次
    messages.append({"role": "user", "content": "Continue..."})
```

## 策略性使用更便宜的模型

```python
async def tiered_model_selection(task_complexity: str):
    """根据任务使用适当的模型。"""
    if task_complexity == "simple":
        return "claude-haiku-..."  # 最便宜
    elif task_complexity == "medium":
        return "claude-sonnet-4-20250514"  # 平衡
    else:
        return "claude-opus-4-5-..."  # 最好但最贵
```

### 在你的真实计算机上运行智能体

严重程度：关键

场景：测试或部署计算机使用

症状：
智能体删除重要文件。从你的账户发送电子邮件。在社交媒体上发帖。访问敏感文档。

为什么会出问题：
计算机使用智能体会犯错。它们可能：
- 误解指令
- 点击错误的按钮
- 在错误的字段输入
- 遵循提示注入攻击

没有沙箱化，这些错误发生在你的真实系统上。
"智能体向所有联系人发送电子邮件"或"智能体删除项目文件夹"是无法撤销的。

"能够访问外部系统和 API 的自主智能体引入了新的安全风险。它们可能容易受到提示注入攻击、对敏感数据的未授权访问或恶意行为者的操纵。"

推荐修复方案：

## 始终使用沙箱化

```python
# 最低可行沙箱：带限制的 Docker

docker run -it --rm \
    --security-opt no-new-privileges \
    --cap-drop ALL \
    --network none \
    --read-only \
    --tmpfs /tmp \
    --memory 2g \
    --cpus 1 \
    computer-use-sandbox
```

## 分层防御

```python
# 防御 1：Docker 隔离
# 防御 2：非 root 用户
# 防御 3：网络限制
# 防御 4：文件系统限制
# 防御 5：资源限制
# 防御 6：操作确认
# 防御 7：操作日志

@dataclass
class SandboxConfig:
    docker_image: str = "computer-use-sandbox:latest"
    network: str = "none"  # 或特定白名单
    readonly_root: bool = True
    max_memory_mb: int = 2048
    max_cpu: float = 1.0
    max_runtime_seconds: int = 300
    require_confirmation: list = field(default_factory=lambda: [
        "download", "submit", "login", "delete"
    ])
    log_all_actions: bool = True
```

## 先在隔离环境中测试

```python
class SandboxedTestRunner:
    """在一次性容器中运行测试。"""

    async def run_test(self, test_task: str) -> dict:
        # 启动全新容器
        container_id = await self.create_container()

        try:
            # 运行任务
            result = await self.execute_in_container(container_id, test_task)

            # 捕获状态用于验证
            state = await self.capture_container_state(container_id)

            return {
                "result": result,
                "final_state": state,
                "logs": await self.get_logs(container_id)
            }
        finally:
            # 始终销毁容器
            await self.destroy_container(container_id)
```

## 验证检查

### 无沙箱的计算机使用

严重程度：错误

计算机使用智能体必须在沙箱化环境中运行

消息：检测到无沙箱化的计算机使用。请使用带限制的 Docker 容器。

### 沙箱具有完整网络访问权限

严重程度：错误

沙箱化智能体应具有受限的网络访问权限

消息：沙箱具有完整的网络访问权限。请使用 --network=none 或特定白名单。

### 在容器中以 root 运行

严重程度：错误

容器智能体应以非 root 用户运行

消息：容器以 root 运行。请在 Dockerfile 中添加 --user 标志或 USER 指令。

### 容器未移除能力

严重程度：警告

容器应移除不必要的能力

消息：容器具有完整能力。请添加 --cap-drop ALL。

### 容器未使用 Seccomp 配置文件

严重程度：警告

容器应使用 seccomp 配置文件进行系统调用过滤

消息：未设置安全选项。考虑 --security-opt seccomp:profile.json

### 无最大步数限制

严重程度：警告

计算机使用循环应有最大步数限制

消息：无限循环风险。请添加 max_steps 限制（推荐：50）。

### 无执行超时

严重程度：警告

计算机使用应有超时限制

消息：执行无超时。请添加超时（推荐：5-10 分钟）。

### 容器无内存限制

严重程度：警告

容器应有内存限制以防止拒绝服务

消息：容器无内存限制。请添加 --memory 2g 或类似设置。

### 无成本跟踪

严重程度：警告

计算机使用应跟踪 API 成本

消息：无成本跟踪。请监控 token 使用量以防止账单意外。

### 无最大成本限制

严重程度：信息

考虑为每个任务添加成本限制

消息：考虑添加 max_cost_per_task 以防止昂贵的失控任务。

## 协作

### 委派触发条件

- 用户需要仅 Web 自动化 -> browser-automation（Playwright/Selenium 对 Web 更高效）
- 用户需要安全审查 -> security-specialist（审查沙箱化、提示注入防御）
- 用户需要容器编排 -> devops（Kubernetes、Docker Swarm 用于扩展）
- 用户需要视觉模型优化 -> llm-architect（模型选择、提示工程）
- 用户需要多智能体协调 -> multi-agent-orchestration（多个计算机使用智能体协同工作）

## 何时使用
- 用户提到或暗示：计算机使用
- 用户提到或暗示：桌面自动化智能体
- 用户提到或暗示：屏幕控制 AI
- 用户提到或暗示：基于视觉的智能体
- 用户提到或暗示：GUI 自动化
- 用户提到或暗示：Claude computer
- 用户提到或暗示：OpenAI Operator
- 用户提到或暗示：浏览器智能体
- 用户提到或暗示：视觉智能体
- 用户提到或暗示：AI RPA

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出替代为环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
