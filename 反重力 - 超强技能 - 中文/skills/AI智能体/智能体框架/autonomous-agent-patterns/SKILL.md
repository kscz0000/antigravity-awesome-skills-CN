---
name: autonomous-agent-patterns
description: "构建自主编程智能体的设计模式，灵感来自 [Cline](https://github.com/cline/cline) 和 [OpenAI Codex](https://github.com/openai/codex)。触发词：自主智能体、autonomous agent、智能体设计模式、工具调用API、权限审批系统、浏览器自动化、人机协作工作流"
risk: critical
source: community
date_added: "2026-02-27"
---

# 🕹️ 自主智能体模式

> 构建自主编程智能体的设计模式，灵感来自 [Cline](https://github.com/cline/cline) 和 [OpenAI Codex](https://github.com/openai/codex)。

## 何时使用此技能

在以下场景使用此技能：

- 构建自主 AI 智能体
- 设计工具/函数调用 API
- 实现权限和审批系统
- 为智能体创建浏览器自动化
- 设计人机协作工作流

---

## 1. 核心智能体架构

### 1.1 智能体循环

```
┌─────────────────────────────────────────────────────────────┐
│                     智能体循环                               │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │   思考   │───▶│   决策   │───▶│   行动   │              │
│  │ (推理)   │    │ (规划)   │    │ (执行)   │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│       ▲                               │                     │
│       │         ┌──────────┐          │                     │
│       └─────────│   观察   │◀─────────┘                     │
│                 │ (结果)   │                                │
│                 └──────────┘                                │
└─────────────────────────────────────────────────────────────┘
```

```python
class AgentLoop:
    def __init__(self, llm, tools, max_iterations=50):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
        self.max_iterations = max_iterations
        self.history = []

    def run(self, task: str) -> str:
        self.history.append({"role": "user", "content": task})

        for i in range(self.max_iterations):
            # 思考：获取带有工具选项的 LLM 响应
            response = self.llm.chat(
                messages=self.history,
                tools=self._format_tools(),
                tool_choice="auto"
            )

            # 决策：检查智能体是否想使用工具
            if response.tool_calls:
                for tool_call in response.tool_calls:
                    # 行动：执行工具
                    result = self._execute_tool(tool_call)

                    # 观察：将结果添加到历史记录
                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })
            else:
                # 没有更多工具调用 = 任务完成
                return response.content

        return "已达到最大迭代次数"

    def _execute_tool(self, tool_call) -> Any:
        tool = self.tools[tool_call.name]
        args = json.loads(tool_call.arguments)
        return tool.execute(**args)
```

### 1.2 多模型架构

```python
class MultiModelAgent:
    """
    为不同目的使用不同的模型：
    - 快速模型用于规划
    - 强大模型用于复杂推理
    - 专用模型用于代码生成
    """

    def __init__(self):
        self.models = {
            "fast": "gpt-3.5-turbo",      # 快速决策
            "smart": "gpt-4-turbo",        # 复杂推理
            "code": "claude-3-sonnet",     # 代码生成
        }

    def select_model(self, task_type: str) -> str:
        if task_type == "planning":
            return self.models["fast"]
        elif task_type == "analysis":
            return self.models["smart"]
        elif task_type == "code":
            return self.models["code"]
        return self.models["smart"]
```

---

## 2. 工具设计模式

### 2.1 工具模式

```python
class Tool:
    """智能体工具的基类"""

    @property
    def schema(self) -> dict:
        """工具的 JSON Schema"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": self._get_parameters(),
                "required": self._get_required()
            }
        }

    def execute(self, **kwargs) -> ToolResult:
        """执行工具并返回结果"""
        raise NotImplementedError

class ReadFileTool(Tool):
    name = "read_file"
    description = "从文件系统读取文件内容"

    def _get_parameters(self):
        return {
            "path": {
                "type": "string",
                "description": "文件的绝对路径"
            },
            "start_line": {
                "type": "integer",
                "description": "开始读取的行号（从1开始）"
            },
            "end_line": {
                "type": "integer",
                "description": "停止读取的行号（包含）"
            }
        }

    def _get_required(self):
        return ["path"]

    def execute(self, path: str, start_line: int = None, end_line: int = None) -> ToolResult:
        try:
            with open(path, 'r') as f:
                lines = f.readlines()

            if start_line and end_line:
                lines = lines[start_line-1:end_line]

            return ToolResult(
                success=True,
                output="".join(lines)
            )
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error=f"文件未找到: {path}"
            )
```

### 2.2 核心智能体工具

```python
CODING_AGENT_TOOLS = {
    # 文件操作
    "read_file": "读取文件内容",
    "write_file": "创建或覆盖文件",
    "edit_file": "对文件进行针对性编辑",
    "list_directory": "列出文件和文件夹",
    "search_files": "按模式搜索文件",

    # 代码理解
    "search_code": "搜索代码模式 (grep)",
    "get_definition": "查找函数/类定义",
    "get_references": "查找符号的所有引用",

    # 终端
    "run_command": "执行 shell 命令",
    "read_output": "读取命令输出",
    "send_input": "向运行中的命令发送输入",

    # 浏览器（可选）
    "open_browser": "在浏览器中打开 URL",
    "click_element": "点击页面元素",
    "type_text": "在输入框中输入文本",
    "screenshot": "截取屏幕截图",

    # 上下文
    "ask_user": "向用户提问",
    "search_web": "在网上搜索信息"
}
```

### 2.3 编辑工具设计

```python
class EditFileTool(Tool):
    """
    精确的文件编辑，带有冲突检测。
    使用搜索/替换模式进行可靠的编辑。
    """

    name = "edit_file"
    description = "通过替换特定内容来编辑文件"

    def execute(
        self,
        path: str,
        search: str,
        replace: str,
        expected_occurrences: int = 1
    ) -> ToolResult:
        """
        参数:
            path: 要编辑的文件
            search: 要查找的确切文本（必须完全匹配，包括空白）
            replace: 要替换成的文本
            expected_occurrences: 搜索内容应该出现的次数（验证）
        """
        with open(path, 'r') as f:
            content = f.read()

        # 验证
        actual_occurrences = content.count(search)
        if actual_occurrences != expected_occurrences:
            return ToolResult(
                success=False,
                error=f"预期 {expected_occurrences} 次出现，找到 {actual_occurrences} 次"
            )

        if actual_occurrences == 0:
            return ToolResult(
                success=False,
                error="在文件中未找到搜索文本"
            )

        # 应用编辑
        new_content = content.replace(search, replace)

        with open(path, 'w') as f:
            f.write(new_content)

        return ToolResult(
            success=True,
            output=f"已替换 {actual_occurrences} 处"
        )
```

---

## 3. 权限与安全模式

### 3.1 权限级别

```python
class PermissionLevel(Enum):
    # 完全自动 - 无需用户审批
    AUTO = "auto"

    # 每个会话询问一次
    ASK_ONCE = "ask_once"

    # 每次都询问
    ASK_EACH = "ask_each"

    # 永不允许
    NEVER = "never"

PERMISSION_CONFIG = {
    # 低风险 - 可以自动审批
    "read_file": PermissionLevel.AUTO,
    "list_directory": PermissionLevel.AUTO,
    "search_code": PermissionLevel.AUTO,

    # 中等风险 - 询问一次
    "write_file": PermissionLevel.ASK_ONCE,
    "edit_file": PermissionLevel.ASK_ONCE,

    # 高风险 - 每次都询问
    "run_command": PermissionLevel.ASK_EACH,
    "delete_file": PermissionLevel.ASK_EACH,

    # 危险 - 永不自动审批
    "sudo_command": PermissionLevel.NEVER,
    "format_disk": PermissionLevel.NEVER
}
```

### 3.2 审批 UI 模式

```python
class ApprovalManager:
    def __init__(self, ui, config):
        self.ui = ui
        self.config = config
        self.session_approvals = {}

    def request_approval(self, tool_name: str, args: dict) -> bool:
        level = self.config.get(tool_name, PermissionLevel.ASK_EACH)

        if level == PermissionLevel.AUTO:
            return True

        if level == PermissionLevel.NEVER:
            self.ui.show_error(f"工具 '{tool_name}' 不被允许")
            return False

        if level == PermissionLevel.ASK_ONCE:
            if tool_name in self.session_approvals:
                return self.session_approvals[tool_name]

        # 显示审批对话框
        approved = self.ui.show_approval_dialog(
            tool=tool_name,
            args=args,
            risk_level=self._assess_risk(tool_name, args)
        )

        if level == PermissionLevel.ASK_ONCE:
            self.session_approvals[tool_name] = approved

        return approved

    def _assess_risk(self, tool_name: str, args: dict) -> str:
        """分析特定调用的风险级别"""
        if tool_name == "run_command":
            cmd = args.get("command", "")
            if any(danger in cmd for danger in ["rm -rf", "sudo", "chmod"]):
                return "HIGH"
        return "MEDIUM"
```

### 3.3 沙箱执行

```python
class SandboxedExecution:
    """
    在隔离环境中执行代码/命令
    """

    def __init__(self, workspace_dir: str):
        self.workspace = workspace_dir
        self.allowed_commands = ["npm", "python", "node", "git", "ls", "cat"]
        self.blocked_paths = ["/etc", "/usr", "/bin", os.path.expanduser("~")]

    def validate_path(self, path: str) -> bool:
        """确保路径在工作区内"""
        real_path = os.path.realpath(path)
        workspace_real = os.path.realpath(self.workspace)
        return real_path.startswith(workspace_real)

    def validate_command(self, command: str) -> bool:
        """检查命令是否被允许"""
        cmd_parts = shlex.split(command)
        if not cmd_parts:
            return False

        base_cmd = cmd_parts[0]
        return base_cmd in self.allowed_commands

    def execute_sandboxed(self, command: str) -> ToolResult:
        if not self.validate_command(command):
            return ToolResult(
                success=False,
                error=f"命令不被允许: {command}"
            )

        # 在隔离环境中执行
        result = subprocess.run(
            command,
            shell=True,
            cwd=self.workspace,
            capture_output=True,
            timeout=30,
            env={
                **os.environ,
                "HOME": self.workspace,  # 隔离 home 目录
            }
        )

        return ToolResult(
            success=result.returncode == 0,
            output=result.stdout.decode(),
            error=result.stderr.decode() if result.returncode != 0 else None
        )
```

---

## 4. 浏览器自动化

### 4.1 浏览器工具模式

```python
class BrowserTool:
    """
    使用 Playwright/Puppeteer 的智能体浏览器自动化。
    支持可视化调试和 Web 测试。
    """

    def __init__(self, headless: bool = True):
        self.browser = None
        self.page = None
        self.headless = headless

    async def open_url(self, url: str) -> ToolResult:
        """导航到 URL 并返回页面信息"""
        if not self.browser:
            self.browser = await playwright.chromium.launch(headless=self.headless)
            self.page = await self.browser.new_page()

        await self.page.goto(url)

        # 捕获状态
        screenshot = await self.page.screenshot(type='png')
        title = await self.page.title()

        return ToolResult(
            success=True,
            output=f"已加载: {title}",
            metadata={
                "screenshot": base64.b64encode(screenshot).decode(),
                "url": self.page.url
            }
        )

    async def click(self, selector: str) -> ToolResult:
        """点击元素"""
        try:
            await self.page.click(selector, timeout=5000)
            await self.page.wait_for_load_state("networkidle")

            screenshot = await self.page.screenshot()
            return ToolResult(
                success=True,
                output=f"已点击: {selector}",
                metadata={"screenshot": base64.b64encode(screenshot).decode()}
            )
        except TimeoutError:
            return ToolResult(
                success=False,
                error=f"元素未找到: {selector}"
            )

    async def type_text(self, selector: str, text: str) -> ToolResult:
        """在输入框中输入文本"""
        await self.page.fill(selector, text)
        return ToolResult(success=True, output=f"已输入到 {selector}")

    async def get_page_content(self) -> ToolResult:
        """获取页面的可访问文本内容"""
        content = await self.page.evaluate("""
            () => {
                // 获取可见文本
                const walker = document.createTreeWalker(
                    document.body,
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );

                let text = '';
                while (walker.nextNode()) {
                    const node = walker.currentNode;
                    if (node.textContent.trim()) {
                        text += node.textContent.trim() + '\\n';
                    }
                }
                return text;
            }
        """)
        return ToolResult(success=True, output=content)
```

### 4.2 视觉智能体模式

```python
class VisualAgent:
    """
    使用屏幕截图理解网页的智能体。
    可以在无需选择器的情况下视觉识别元素。
    """

    def __init__(self, llm, browser):
        self.llm = llm
        self.browser = browser

    async def describe_page(self) -> str:
        """使用视觉模型描述当前页面"""
        screenshot = await self.browser.screenshot()

        response = self.llm.chat([
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "描述这个网页。列出你看到的所有交互元素。"},
                    {"type": "image", "data": screenshot}
                ]
            }
        ])

        return response.content

    async def find_and_click(self, description: str) -> ToolResult:
        """通过视觉描述查找元素并点击"""
        screenshot = await self.browser.screenshot()

        # 请求视觉模型查找元素
        response = self.llm.chat([
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
                        查找匹配此描述的元素: "{description}"
                        以 JSON 格式返回近似坐标: {{"x": number, "y": number}}
                        """
                    },
                    {"type": "image", "data": screenshot}
                ]
            }
        ])

        coords = json.loads(response.content)
        await self.browser.page.mouse.click(coords["x"], coords["y"])

        return ToolResult(success=True, output=f"已点击位置 ({coords['x']}, {coords['y']})")
```

---

## 5. 上下文管理

### 5.1 上下文注入模式

````python
class ContextManager:
    """
    管理提供给智能体的上下文。
    灵感来自 Cline 的 @-提及模式。
    """

    def __init__(self, workspace: str):
        self.workspace = workspace
        self.context = []

    def add_file(self, path: str) -> None:
        """@file - 将文件内容添加到上下文"""
        with open(path, 'r') as f:
            content = f.read()

        self.context.append({
            "type": "file",
            "path": path,
            "content": content
        })

    def add_folder(self, path: str, max_files: int = 20) -> None:
        """@folder - 添加文件夹中的所有文件"""
        for root, dirs, files in os.walk(path):
            for file in files[:max_files]:
                file_path = os.path.join(root, file)
                self.add_file(file_path)

    def add_url(self, url: str) -> None:
        """@url - 获取并添加 URL 内容"""
        response = requests.get(url)
        content = html_to_markdown(response.text)

        self.context.append({
            "type": "url",
            "url": url,
            "content": content
        })

    def add_problems(self, diagnostics: list) -> None:
        """@problems - 添加 IDE 诊断"""
        self.context.append({
            "type": "diagnostics",
            "problems": diagnostics
        })

    def format_for_prompt(self) -> str:
        """格式化所有上下文以供 LLM 提示"""
        parts = []
        for item in self.context:
            if item["type"] == "file":
                parts.append(f"## 文件: {item['path']}\n```\n{item['content']}\n```")
            elif item["type"] == "url":
                parts.append(f"## URL: {item['url']}\n{item['content']}")
            elif item["type"] == "diagnostics":
                parts.append(f"## 问题:\n{json.dumps(item['problems'], indent=2)}")

        return "\n\n".join(parts)
````

### 5.2 检查点/恢复

```python
class CheckpointManager:
    """
    为长时间运行的任务保存和恢复智能体状态。
    """

    def __init__(self, storage_dir: str):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save_checkpoint(self, session_id: str, state: dict) -> str:
        """保存当前智能体状态"""
        checkpoint = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "history": state["history"],
            "context": state["context"],
            "workspace_state": self._capture_workspace(state["workspace"]),
            "metadata": state.get("metadata", {})
        }

        path = os.path.join(self.storage_dir, f"{session_id}.json")
        with open(path, 'w') as f:
            json.dump(checkpoint, f, indent=2)

        return path

    def restore_checkpoint(self, checkpoint_path: str) -> dict:
        """从检查点恢复智能体状态"""
        with open(checkpoint_path, 'r') as f:
            checkpoint = json.load(f)

        return {
            "history": checkpoint["history"],
            "context": checkpoint["context"],
            "workspace": self._restore_workspace(checkpoint["workspace_state"]),
            "metadata": checkpoint["metadata"]
        }

    def _capture_workspace(self, workspace: str) -> dict:
        """捕获相关的工作区状态"""
        # Git 状态、文件哈希等
        return {
            "git_ref": subprocess.getoutput(f"cd {workspace} && git rev-parse HEAD"),
            "git_dirty": subprocess.getoutput(f"cd {workspace} && git status --porcelain")
        }
```

---

## 6. MCP (Model Context Protocol) 集成

### 6.1 MCP 服务器模式

```python
from mcp import Server, Tool

class MCPAgent:
    """
    可以动态发现和使用 MCP 工具的智能体。
    来自 Cline 的"添加一个工具..."模式。
    """

    def __init__(self, llm):
        self.llm = llm
        self.mcp_servers = {}
        self.available_tools = {}

    def connect_server(self, name: str, config: dict) -> None:
        """连接到 MCP 服务器"""
        server = Server(config)
        self.mcp_servers[name] = server

        # 发现工具
        tools = server.list_tools()
        for tool in tools:
            self.available_tools[tool.name] = {
                "server": name,
                "schema": tool.schema
            }

    async def create_tool(self, description: str) -> str:
        """
        根据用户描述创建新的 MCP 服务器。
        "添加一个获取 Jira 工单的工具"
        """
        # 生成 MCP 服务器代码
        code = self.llm.generate(f"""
        创建一个 Python MCP 服务器，包含一个执行以下功能的工具:
        {description}

        使用 FastMCP 框架。包含适当的错误处理。
        仅返回 Python 代码。
        """)

        # 保存并安装
        server_name = self._extract_name(description)
        path = f"./mcp_servers/{server_name}/server.py"

        with open(path, 'w') as f:
            f.write(code)

        # 热重载
        self.connect_server(server_name, {"path": path})

        return f"已创建工具: {server_name}"
```

---

## 最佳实践清单

### 智能体设计

- [ ] 清晰的任务分解
- [ ] 适当的工具粒度
- [ ] 每一步都有错误处理
- [ ] 向用户提供进度可见性

### 安全

- [ ] 已实现权限系统
- [ ] 已阻止危险操作
- [ ] 对不受信任的代码使用沙箱
- [ ] 已启用审计日志

### 用户体验

- [ ] 审批 UI 清晰
- [ ] 提供进度更新
- [ ] 可用撤销/回滚
- [ ] 解释操作内容

---

## 资源

- [Cline](https://github.com/cline/cline)
- [OpenAI Codex](https://github.com/openai/codex)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Anthropic Tool Use](https://docs.anthropic.com/claude/docs/tool-use)

## 限制
- 仅当任务明确符合上述描述的范围时才使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
