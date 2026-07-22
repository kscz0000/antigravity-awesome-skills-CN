---
name: webapp-testing
description: "用于测试本地 Web 应用程序，编写原生 Python Playwright 脚本。触发词：Web 应用测试、Playwright、本地应用、自动化测试、网页测试、E2E 测试、浏览器自动化"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Web 应用程序测试

用于测试本地 Web 应用程序，编写原生 Python Playwright 脚本。

**可用辅助脚本**：
- `scripts/with_server.py` - 管理服务器生命周期（支持多服务器）

**始终先使用 `--help` 运行脚本** 以查看用法。在你尝试运行脚本并发现确实需要定制方案之前，请勿阅读源码。这些脚本体量很大，容易污染你的上下文窗口。它们的存在目的是作为黑盒脚本直接调用，而不是被加载到你的上下文窗口中。

## 决策树：选择你的方法

```
用户任务 → 是否为静态 HTML？
    ├─ 是 → 直接读取 HTML 文件以识别选择器
    │         ├─ 成功 → 使用选择器编写 Playwright 脚本
    │         └─ 失败/不完整 → 按动态页面处理（见下方）
    │
    └─ 否（动态 Web 应用）→ 服务器是否已在运行？
        ├─ 否 → 运行：python scripts/with_server.py --help
        │        然后使用辅助脚本 + 编写简化的 Playwright 脚本
        │
        └─ 是 → 侦察后行动：
            1. 导航并等待 networkidle
            2. 截图或检查 DOM
            3. 从渲染状态中识别选择器
            4. 使用发现的选择器执行操作
```

## 示例：使用 with_server.py

要启动服务器，请先运行 `--help`，然后使用辅助脚本：

**单个服务器：**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**多个服务器（例如后端 + 前端）：**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

要创建自动化脚本，只需包含 Playwright 逻辑（服务器会自动管理）：
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # 始终以 headless 模式启动 chromium
    page = browser.new_page()
    page.goto('http://localhost:5173') # 服务器已运行并就绪
    page.wait_for_load_state('networkidle') # 关键：等待 JS 执行完成
    # ... 你的自动化逻辑
    browser.close()
```

## 侦察后行动模式

1. **检查渲染后的 DOM**：
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **从检查结果中识别选择器**

3. **使用发现的选择器执行操作**

## 常见陷阱

❌ **不要** 在动态应用上等待 `networkidle` 之前就检查 DOM
✅ **应当** 在检查之前等待 `page.wait_for_load_state('networkidle')`

## 最佳实践

- **将打包的脚本作为黑盒使用** - 要完成任务，先考虑 `scripts/` 中可用的脚本是否能提供帮助。这些脚本能够可靠地处理常见、复杂的工作流，而不会污染上下文窗口。使用 `--help` 查看用法，然后直接调用。
- 对同步脚本使用 `sync_playwright()`
- 完成后始终关闭浏览器
- 使用描述性的选择器：`text=`、`role=`、CSS 选择器或 ID
- 添加适当的等待：`page.wait_for_selector()` 或 `page.wait_for_timeout()`

## 参考文件

- **examples/** - 展示常见模式的示例：
  - `element_discovery.py` - 发现页面上的按钮、链接和输入框
  - `static_html_automation.py` - 使用 file:// URL 处理本地 HTML
  - `console_logging.py` - 在自动化过程中捕获控制台日志

## 何时使用
本技能适用于执行上述概览中描述的工作流或操作。

## 局限性
- 仅当任务明确匹配上述范围时才使用本技能。
- 请勿将输出视为针对特定环境的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来主动寻求澄清。
