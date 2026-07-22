---
name: go-playwright
description: "使用 Playwright Go 实现健壮、隐蔽、高效的浏览器自动化。当用户要求'用Go抓取网页'、'Go浏览器自动化'、'Playwright Go测试'时使用。"
risk: safe
source: "https://github.com/playwright-community/playwright-go"
date_added: "2026-02-27"
---

# Playwright Go 自动化专家

## 概述
本技能提供使用 `github.com/playwright-community/playwright-go` 编写高性能、生产级浏览器自动化脚本的完整框架。强制执行架构最佳实践（上下文优于实例）、健壮的错误处理、结构化日志（Zap），以及高级人类模拟技术来绑过反机器人系统。

## 何时使用
- 用户要求用 Go "抓取"、"自动化" 或 "测试" 网站时
- 目标网站有复杂动态内容（SPA、React、Vue）需要真实浏览器时
- 用户提到 "隐蔽"、"绕过检测"、"Cloudflare" 或 "拟人行为" 时
- 调试现有 Playwright 脚本时

## 安全与风险
**风险等级：🔵 安全**

- **沙箱执行：** 浏览器上下文相互隔离；除非显式保存，否则不会向主机持久化数据。
- **资源管理：** 通过 `defer` 关闭浏览器和上下文，防止内存泄漏。
- **无外部状态变更：** 默认行为为只读（抓取/测试），除非脚本显式设计为提交表单或修改数据。

## 限制
- **环境依赖：** 需要安装 Playwright 驱动和浏览器（`go run github.com/playwright-community/playwright-go/cmd/playwright@latest install --with-deps`）。
- **资源消耗：** 启动完整浏览器实例（即使无头模式）会消耗大量内存/CPU。采用单浏览器/多上下文架构。
- **机器人检测：** 虽然本技能包含隐蔽技术，但极严格的反机器人系统（如严格的 Cloudflare 设置）仍可能检测到自动化。
- **验证码：** 不包含内置验证码破解能力。

## 战略实施指南

### 1. 架构：上下文 vs 浏览器
**关键：** 绝不要为每个任务启动新的 `Browser` 实例。
- **模式：** 只启动一次 `Browser`（单例）。为每个独立会话或任务创建新的 `BrowserContext`。
- **原因：** 上下文轻量，毫秒级创建。浏览器启动需要数秒。
- **隔离：** 上下文提供完全隔离（cookies、缓存、存储），无需新进程的开销。

### 2. 日志与可观测性
- **库：** 只使用 `go.uber.org/zap`。
- **规则：** 不要使用 `fmt.Println`。
- **模式：**
  - **开发：** `zap.NewDevelopment()`（控制台友好）
  - **生产：** `zap.NewProduction()`（JSON 结构化）
- **可追溯性：** 记录每次导航、点击和输入，附带上下文字段（如 `logger.Info("clicking button", zap.String("selector", sel))`）。

### 3. 错误处理与稳定性
- **优雅关闭：** 始终使用 `defer` 关闭 Page、Context 和 Browser。
- **Panic 恢复：** 将关键自动化例程包装在安全运行器中，恢复 panic 并记录堆栈跟踪。
- **超时：** 绝不依赖默认超时。设置显式超时（如 `playwright.PageClickOptions{Timeout: playwright.Float(5000)}`）。

### 4. 隐蔽与拟人行为
要绑过反机器人系统（Cloudflare、Akamai），生成的代码必须**模仿人类生理特征**：
- **非线性鼠标移动：** 绝不瞬移鼠标。实现沿贝塞尔曲线移动并带随机抖动的辅助函数。
- **输入延迟：** 绝不使用 `Fill()`。使用 `Type()` 并在按键间加入随机延迟（50ms–200ms）。
- **视口随机化：** 轻微随机化视口大小（如 1920x1080 ± 15px）以避免指纹识别。
- **行为噪声：** 在长时间等待期间随机滚动、聚焦/失焦窗口或悬停无关元素（"空闲"行为）。
- **User-Agent：** 为每个新上下文轮换 User-Agent。

### 5. 文档使用
- **主要来源：** 优先依靠内部 API 知识以节省 token。
- **备选：** 仅在以下情况参考官方文档 [playwright-go documentation](https://pkg.go.dev/github.com/playwright-community/playwright-go#section-documentation)：
  - 遇到未知错误。
  - 需要实现复杂的网络拦截或认证流程。
  - API 发生重大变更。

## 资源
- `resources/implementation-playbook.md` 提供详细代码示例和实现模式。

### Agent 检查清单
 - 是否开启调试模式？ -> `Headless=false`，`SlowMo=100+`。
 - 是否为新用户身份？ -> `NewContext`，应用新代理，轮换 `User-Agent`。
 - 操作是否关键？ -> 包装在带 Zap 日志的 `SafeAction` 中。
 - 目标是否有防护（Cloudflare/Akamai）？ -> 启用 `HumanType`、`BezierMouse` 和隐蔽脚本。
