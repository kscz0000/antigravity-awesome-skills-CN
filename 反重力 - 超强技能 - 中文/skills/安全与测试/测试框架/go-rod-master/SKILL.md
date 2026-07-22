---
name: go-rod-master
description: "基于 Chrome DevTools Protocol 的 go-rod 浏览器自动化与网页抓取完整指南，包含 stealth 反机器人检测模式。当用户要求使用 Go 进行网页抓取、自动化、测试、绕过机器人检测、处理动态内容、拦截网络请求时使用。"
risk: safe
source: "https://github.com/go-rod/rod"
date_added: "2026-02-27"
---

# Go-Rod 浏览器自动化精通

## 概述

[Rod](https://github.com/go-rod/rod) 是直接基于 [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) 构建的高级 Go 驱动器，用于浏览器自动化和网页抓取。与其他工具的封装不同，Rod 通过 CDP 与浏览器原生通信，提供线程安全操作、链式上下文设计（支持超时/取消）、元素自动等待、正确的 iframe/shadow DOM 处理，以及零僵尸浏览器进程。

配套库 [go-rod/stealth](https://github.com/go-rod/stealth) 基于 [puppeteer-extra stealth](https://github.com/nichochar/puppeteer-extra/tree/master/packages/extract-stealth-evasions) 注入反机器人检测规避脚本，向检测系统隐藏无头浏览器指纹。

## 何时使用此技能

- 用户要求使用 Go **抓取**、**自动化**或**测试**网站时使用。
- 用户需要**无头浏览器**处理动态/SPA 内容（React、Vue、Angular）时使用。
- 用户提到**stealth**、**反机器人**、**规避检测**、**Cloudflare** 或**绕过机器人检测**时使用。
- 用户希望直接从 Go 操作 **Chrome DevTools Protocol (CDP)** 时使用。
- 用户需要在浏览器上下文中**拦截**或**劫持**网络请求时使用。
- 用户询问 Go 中的**并发浏览器抓取**或**页面池**时使用。
- 用户从 **chromedp** 或 **Playwright Go** 迁移并希望获得更简洁的 API 时使用。

## 安全与风险

**风险等级：🔵 安全**

- **默认只读：** 默认行为是导航和读取页面内容（抓取/测试）。
- **隔离上下文：** 浏览器上下文是沙箱化的；Cookie 和存储不会持久化，除非显式保存。
- **资源清理：** 基于 Go 的 `defer` 模式设计——浏览器和页面自动关闭。
- **无外部变更：** 不会修改外部状态，除非脚本显式提交表单或发送 POST 数据。

## 安装

```bash
# Core rod library
go get github.com/go-rod/rod@latest

# Stealth anti-detection plugin (ALWAYS include for production scraping)
go get github.com/go-rod/stealth@latest
```

Rod 首次运行时自动下载兼容的 Chromium 二进制文件。如需预下载：

```bash
go run github.com/nichochar/go-rod.github.io/cmd/launcher@latest
```

## 核心概念

### 浏览器生命周期

Rod 管理三个层级：**Browser → Page → Element**。

```go
// Launch and connect to a browser
browser := rod.New().MustConnect()
defer browser.MustClose()

// Create a page (tab)
page := browser.MustPage("https://example.com")

// Find an element
el := page.MustElement("h1")
fmt.Println(el.MustText())
```

### Must 与 Error 模式

Rod 为每个操作提供两种 API 风格：

| 风格 | 方法 | 使用场景 |
|:------|:-------|:---------|
| **Must** | `MustElement()`, `MustClick()`, `MustText()` | 脚本编写、调试、原型开发。出错时 panic。 |
| **Error** | `Element()`, `Click()`, `Text()` | 生产代码。返回 `error` 供显式处理。 |

**生产模式：**

```go
el, err := page.Element("#login-btn")
if err != nil {
    return fmt.Errorf("login button not found: %w", err)
}
if err := el.Click(proto.InputMouseButtonLeft, 1); err != nil {
    return fmt.Errorf("click failed: %w", err)
}
```

**带 Try 的脚本模式：**

```go
err := rod.Try(func() {
    page.MustElement("#login-btn").MustClick()
})
if errors.Is(err, context.DeadlineExceeded) {
    log.Println("timeout finding login button")
}
```

### Context 与超时

Rod 使用 Go 的 `context.Context` 进行取消和超时控制。上下文递归传播到所有子操作。

```go
// Set a 5-second timeout for the entire operation chain
page.Timeout(5 * time.Second).
    MustWaitLoad().
    MustElement("title").
    CancelTimeout(). // subsequent calls are not bound by the 5s timeout
    Timeout(30 * time.Second).
    MustText()
```

### 元素选择器

Rod 支持多种选择器策略：

```go
// CSS selector (most common)
page.MustElement("div.content > p.intro")

// CSS selector with text regex matching
page.MustElementR("button", "Submit|Send")

// XPath
page.MustElementX("//div[@class='content']//p")

// Search across iframes and shadow DOM (like DevTools Ctrl+F)
page.MustSearch(".deeply-nested-element")
```

### 自动等待

Rod 自动重试元素查询，直到元素出现或上下文超时。无需手动休眠：

```go
// This will automatically wait until the element exists
el := page.MustElement("#dynamic-content")

// Wait until the element is stable (position/size not changing)
el.MustWaitStable().MustClick()

// Wait until page has no pending network requests
wait := page.MustWaitRequestIdle()
page.MustElement("#search").MustInput("query")
wait()
```

---

## Stealth 与反机器人检测 (go-rod/stealth)

> **重要：** 对于任何针对真实网站的生产抓取或自动化，**务必**使用 `stealth.MustPage()` 而非 `browser.MustPage()`。这是规避机器人检测最关键的一步。

### Stealth 工作原理

`go-rod/stealth` 包向每个新页面注入 JavaScript 规避脚本：

- **移除 `navigator.webdriver`** — 主要的无头检测信号。
- **伪装 WebGL vendor/renderer** — 呈现真实 GPU 信息（如 "Intel Inc." / "Intel Iris OpenGL Engine"），而非 "Google SwiftShader" 等无头标记。
- **修复 Chrome 插件数组** — 报告正确的 `PluginArray` 类型和真实的插件数量。
- **修补权限 API** — 返回 `"prompt"` 而非暴露机器人的值。
- **设置真实语言** — 报告 `en-US,en` 而非空数组。
- **修复损坏的图片尺寸** — 无头浏览器报告 0x0；stealth 修复为 16x16。

### 用法

**创建 stealth 页面（推荐所有生产环境使用）：**

```go
import (
    "github.com/go-rod/rod"
    "github.com/go-rod/stealth"
)

browser := rod.New().MustConnect()
defer browser.MustClose()

// Use stealth.MustPage instead of browser.MustPage
page := stealth.MustPage(browser)
page.MustNavigate("https://bot.sannysoft.com")
```

**带错误处理：**

```go
page, err := stealth.Page(browser)
if err != nil {
    return fmt.Errorf("failed to create stealth page: %w", err)
}
page.MustNavigate("https://example.com")
```

**直接使用 stealth.JS（高级用法——用于自定义页面创建）：**

```go
// If you need to create the page yourself (e.g., with specific options),
// inject stealth.JS manually via EvalOnNewDocument
page := browser.MustPage()
page.MustEvalOnNewDocument(stealth.JS)
page.MustNavigate("https://example.com")
```

### 验证 Stealth

导航到机器人检测测试页面验证规避效果：

```go
page := stealth.MustPage(browser)
page.MustNavigate("https://bot.sannysoft.com")
page.MustScreenshot("stealth_test.png")
```

正确配置 stealth 的浏览器预期结果：
- **WebDriver**: `missing (passed)`
- **Chrome**: `present (passed)`
- **Plugins Length**: `3` (not `0`)
- **Languages**: `en-US,en`

---

## 实现指南

### 1. Launcher 配置

使用 `launcher` 包自定义浏览器启动标志：

```go
import "github.com/go-rod/rod/lib/launcher"

url := launcher.New().
    Headless(true).             // false for debugging
    Proxy("127.0.0.1:8080").    // upstream proxy
    Set("disable-gpu", "").     // custom Chrome flag
    Delete("use-mock-keychain"). // remove a default flag
    MustLaunch()

browser := rod.New().ControlURL(url).MustConnect()
defer browser.MustClose()
```

**调试模式（可见浏览器 + 慢动作）：**

```go
l := launcher.New().
    Headless(false).
    Devtools(true)
defer l.Cleanup()

browser := rod.New().
    ControlURL(l.MustLaunch()).
    Trace(true).
    SlowMotion(2 * time.Second).
    MustConnect()
```

### 2. 代理支持

```go
// Set proxy at launch
url := launcher.New().
    Proxy("socks5://127.0.0.1:1080").
    MustLaunch()

browser := rod.New().ControlURL(url).MustConnect()

// Handle proxy authentication
go browser.MustHandleAuth("username", "password")()

// Ignore SSL certificate errors (for MITM proxies)
browser.MustIgnoreCertErrors(true)
```

### 3. 输入模拟

```go
import "github.com/go-rod/rod/lib/input"

// Type into an input field (replaces existing value)
page.MustElement("#email").MustInput("user@example.com")

// Simulate keyboard keys
page.Keyboard.MustType(input.Enter)

// Press key combinations
page.Keyboard.MustPress(input.ControlLeft)
page.Keyboard.MustType(input.KeyA)
page.Keyboard.MustRelease(input.ControlLeft)

// Mouse click at coordinates
page.Mouse.MustClick(input.MouseLeft)
page.Mouse.MustMoveTo(100, 200)
```

### 4. 网络请求拦截（劫持）

```go
router := browser.HijackRequests()
defer router.MustStop()

// Block all image requests
router.MustAdd("*.png", func(ctx *rod.Hijack) {
    ctx.Response.Fail(proto.NetworkErrorReasonBlockedByClient)
})

// Modify request headers
router.MustAdd("*api.example.com*", func(ctx *rod.Hijack) {
    ctx.Request.Req().Header.Set("Authorization", "Bearer token123")
    ctx.MustLoadResponse()
})

// Modify response body
router.MustAdd("*.js", func(ctx *rod.Hijack) {
    ctx.MustLoadResponse()
    ctx.Response.SetBody(ctx.Response.Body() + "\n// injected")
})

go router.Run()
```

### 5. 等待策略

```go
// Wait for page load event
page.MustWaitLoad()

// Wait for no pending network requests (AJAX idle)
wait := page.MustWaitRequestIdle()
page.MustElement("#search").MustInput("query")
wait()

// Wait for element to be stable (not animating)
page.MustElement(".modal").MustWaitStable().MustClick()

// Wait for element to become invisible
page.MustElement(".loading").MustWaitInvisible()

// Wait for JavaScript condition
page.MustWait(`() => document.title === 'Ready'`)

// Wait for specific navigation/event
wait := page.WaitEvent(&proto.PageLoadEventFired{})
page.MustNavigate("https://example.com")
wait()
```

### 6. 竞争选择器（多种结果）

处理可能出现多种结果的页面（如登录成功 vs 错误）：

```go
page.MustElement("#username").MustInput("user")
page.MustElement("#password").MustInput("pass").MustType(input.Enter)

// Race between success and error selectors
elm := page.Race().
    Element(".dashboard").MustHandle(func(e *rod.Element) {
        fmt.Println("Login successful:", e.MustText())
    }).
    Element(".error-message").MustDo()

if elm.MustMatches(".error-message") {
    log.Fatal("Login failed:", elm.MustText())
}
```

### 7. 截图与 PDF

```go
// Full-page screenshot
page.MustScreenshot("page.png")

// Custom screenshot (JPEG, specific region)
img, _ := page.Screenshot(true, &proto.PageCaptureScreenshot{
    Format:  proto.PageCaptureScreenshotFormatJpeg,
    Quality: gson.Int(90),
    Clip: &proto.PageViewport{
        X: 0, Y: 0, Width: 1280, Height: 800, Scale: 1,
    },
})
utils.OutputFile("screenshot.jpg", img)

// Scroll screenshot (captures full scrollable page)
img, _ := page.MustWaitStable().ScrollScreenshot(nil)
utils.OutputFile("full_page.jpg", img)

// PDF export
page.MustPDF("output.pdf")
```

### 8. 并发页面池

```go
pool := rod.NewPagePool(5) // max 5 concurrent pages

create := func() *rod.Page {
    return browser.MustIncognito().MustPage()
}

var wg sync.WaitGroup
for _, url := range urls {
    wg.Add(1)
    go func(u string) {
        defer wg.Done()

        page := pool.MustGet(create)
        defer pool.Put(page)

        page.MustNavigate(u).MustWaitLoad()
        fmt.Println(page.MustInfo().Title)
    }(url)
}
wg.Wait()

pool.Cleanup(func(p *rod.Page) { p.MustClose() })
```

### 9. 事件处理

```go
// Listen for console.log output
go page.EachEvent(func(e *proto.RuntimeConsoleAPICalled) {
    if e.Type == proto.RuntimeConsoleAPICalledTypeLog {
        fmt.Println(page.MustObjectsToJSON(e.Args))
    }
})()

// Wait for a specific event before proceeding
wait := page.WaitEvent(&proto.PageLoadEventFired{})
page.MustNavigate("https://example.com")
wait()
```

### 10. 文件下载

```go
wait := browser.MustWaitDownload()

page.MustElementR("a", "Download PDF").MustClick()

data := wait()
utils.OutputFile("downloaded.pdf", data)
```

### 11. JavaScript 执行

```go
// Execute JS on the page
page.MustEval(`() => console.log("hello")`)

// Pass parameters and get return value
result := page.MustEval(`(a, b) => a + b`, 1, 2)
fmt.Println(result.Int()) // 3

// Eval on a specific element ("this" = the DOM element)
title := page.MustElement("title").MustEval(`() => this.innerText`).String()

// Direct CDP calls for features Rod doesn't wrap
proto.PageSetAdBlockingEnabled{Enabled: true}.Call(page)
```

### 12. 加载 Chrome 扩展

```go
extPath, _ := filepath.Abs("./my-extension")

u := launcher.New().
    Set("load-extension", extPath).
    Headless(false). // extensions require headed mode
    MustLaunch()

browser := rod.New().ControlURL(u).MustConnect()
```

---

## 示例

参见 `examples/` 目录中的完整可运行 Go 文件：
- `examples/basic_scrape.go` — 最简抓取示例
- `examples/stealth_page.go` — 使用 go-rod/stealth 反检测
- `examples/request_hijacking.go` — 拦截和修改网络请求
- `examples/concurrent_pages.go` — 并发抓取页面池

---

## 最佳实践

- ✅ 针对真实网站，**务必使用 `stealth.MustPage(browser)`** 而非 `browser.MustPage()`。
- ✅ 连接后**务必立即 `defer browser.MustClose()`**。
- ✅ 生产代码中使用返回错误的 API（而非 `Must*`）。
- ✅ 使用 `.Timeout()` 设置显式超时——生产环境绝不依赖默认值。
- ✅ 使用 `browser.MustIncognito().MustPage()` 创建隔离会话。
- ✅ 使用 `PagePool` 进行并发抓取，而非无限制创建页面。
- ✅ 点击可能正在动画的元素前使用 `MustWaitStable()`。
- ✅ 触发 AJAX 调用的操作后使用 `MustWaitRequestIdle()`。
- ✅ 调试时使用 `launcher.New().Headless(false).Devtools(true)`。
- ❌ **绝不**使用 `time.Sleep()` 等待——使用 Rod 内置的等待方法。
- ❌ **绝不**为每个任务创建新的 `Browser`——创建一个 Browser，使用多个 `Page` 实例。
- ❌ **绝不**在生产抓取中使用 `browser.MustPage()`——使用 `stealth.MustPage()`。
- ❌ **绝不**在生产环境中忽略错误——始终显式处理。
- ❌ **绝不**忘记 defer-close 浏览器、页面和劫持路由器。

## 常见陷阱

- **问题：** 元素明明存在却找不到。
  **解决方案：** 元素可能在 iframe 或 shadow DOM 内。使用 `page.MustSearch()` 而非 `page.MustElement()`——它会搜索所有 iframe 和 shadow DOM。

- **问题：** 点击无效，因为元素正在动画。
  **解决方案：** 在 `el.MustClick()` 前调用 `el.MustWaitStable()`。

- **问题：** 使用 stealth 后仍被机器人检测。
  **解决方案：** 将 `stealth.MustPage()` 与以下措施结合：随机视口尺寸、真实的 User-Agent 字符串、按键间类人的输入延迟、随机空闲行为（滚动、悬停）。

- **问题：** 浏览器进程泄漏（僵尸进程）。
  **解决方案：** 始终 `defer browser.MustClose()`。Rod 使用 [leakless](https://github.com/ysmood/leakless) 在主进程崩溃后杀死僵尸进程，但显式清理更佳。

- **问题：** 慢页面超时错误。
  **解决方案：** 使用链式上下文：`page.Timeout(30 * time.Second).MustWaitLoad()`。对于 AJAX 密集型页面，使用 `MustWaitRequestIdle()` 而非 `MustWaitLoad()`。

- **问题：** HijackRequests 路由器未拦截请求。
  **解决方案：** 设置路由后必须调用 `go router.Run()`，并 `defer router.MustStop()` 进行清理。

## 局限性

- **验证码：** Rod 不包含验证码解决功能。必须单独集成外部服务（2captcha 等）。
- **极端反机器人：** 虽然 `go-rod/stealth` 处理常见检测（WebDriver、插件指纹、WebGL），极端严格的系统（部分 Cloudflare 配置、Akamai Bot Manager）可能仍能检测自动化。可能需要额外措施（住宅代理、类人行为模式）。
- **DRM 内容：** 无法与受 DRM 保护的媒体交互（如 Widevine）。
- **资源占用：** 每个浏览器实例消耗大量内存（约 100-300MB+）。在内存受限系统上使用 `PagePool` 并限制并发。
- **无头模式扩展：** Chrome 扩展在无头模式下不工作。服务器环境需使用 `Headless(false)` 配合 XVFB。
- **平台：** 需要兼容 Chromium 的浏览器。不支持 Firefox 或 Safari。

## 文档参考

- [官方文档](https://go-rod.github.io/) — 指南、教程、FAQ
- [Go API 参考](https://pkg.go.dev/github.com/go-rod/rod) — 完整类型和方法文档
- [go-rod/stealth](https://github.com/go-rod/stealth) — 反机器人检测插件
- [示例源码](https://github.com/go-rod/rod/blob/main/examples_test.go) — 官方示例测试
- [Rod vs Chromedp 对比](https://github.com/nichochar/go-rod.github.io/blob/main/lib/examples/compare-chromedp) — 迁移参考
- [Chrome DevTools Protocol 文档](https://chromedevtools.github.io/devtools-protocol/) — 底层协议参考
- [Chrome CLI 标志参考](https://peter.sh/experiments/chromium-command-line-switches) — Launcher 标志文档
- `references/api-reference.md` — 快速参考速查表
