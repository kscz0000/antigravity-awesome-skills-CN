# Go-Rod API 快速参考

`go-rod/rod` 和 `go-rod/stealth` 最常用 API 速查表。
每个 `Must*` 方法都有对应的返回错误版本（去掉 `Must` 前缀）。

---

## Browser (`rod.Browser`)

| 方法 | 说明 |
|:-------|:------------|
| `rod.New().MustConnect()` | 启动新浏览器并连接 |
| `rod.New().ControlURL(url).MustConnect()` | 通过 WebSocket URL 连接现有浏览器 |
| `browser.MustClose()` | 关闭浏览器及所有页面 |
| `browser.MustPage(url)` | 创建新页面（标签页）并导航 |
| `browser.MustPage()` | 创建空白页面 |
| `browser.MustIncognito()` | 创建隔离的隐身上下文 |
| `browser.MustIgnoreCertErrors(true)` | 忽略 SSL 证书错误 |
| `browser.MustHandleAuth(user, pass)` | 处理 HTTP 基础/代理认证 |
| `browser.HijackRequests()` | 创建请求拦截路由器 |
| `browser.MustWaitDownload()` | 等待文件下载完成 |
| `browser.ServeMonitor("")` | 启动可视化监控服务器 |
| `browser.Trace(true)` | 启用详细追踪 |
| `browser.SlowMotion(duration)` | 在操作间添加延迟 |
| `rod.NewPagePool(n)` | 创建最多 `n` 个可复用页面的池 |
| `rod.NewBrowserPool(n)` | 创建最多 `n` 个可复用浏览器的池 |

## Page (`rod.Page`)

| 方法 | 说明 |
|:-------|:------------|
| `page.MustNavigate(url)` | 导航到 URL |
| `page.MustWaitLoad()` | 等待 `load` 事件 |
| `page.MustWaitStable()` | 等待页面 DOM 稳定 |
| `page.MustWaitRequestIdle()` | 等待无待处理网络请求 |
| `page.MustWaitIdle()` | 等待加载和网络空闲 |
| `page.MustWait(js)` | 等待 JS 表达式返回真值 |
| `page.MustElement(selector)` | 通过 CSS 选择器查找元素（自动等待） |
| `page.MustElementR(selector, regex)` | 通过 CSS + 文本正则查找元素 |
| `page.MustElementX(xpath)` | 通过 XPath 查找元素 |
| `page.MustElements(selector)` | 查找所有匹配元素 |
| `page.MustSearch(query)` | 跨 iframe + shadow DOM 搜索 |
| `page.MustEval(js, args...)` | 在页面上执行 JavaScript |
| `page.MustEvalOnNewDocument(js)` | 在任何页面脚本运行前注入 JS |
| `page.MustScreenshot(path)` | 截取 PNG 截图 |
| `page.MustPDF(path)` | 将页面导出为 PDF |
| `page.ScrollScreenshot(opts)` | 全页滚动截图 |
| `page.MustInfo()` | 获取页面信息（标题、URL） |
| `page.Timeout(duration)` | 为链式操作设置超时 |
| `page.CancelTimeout()` | 移除后续操作的超时 |
| `page.Race()` | 启动竞争选择器（多种结果） |
| `page.Keyboard` | 访问键盘控制器 |
| `page.Mouse` | 访问鼠标控制器 |
| `page.WaitEvent(proto)` | 等待特定 CDP 事件 |
| `page.EachEvent(handler)` | 持续订阅事件 |
| `page.Event()` | 基于通道的事件流 |

## Element (`rod.Element`)

| 方法 | 说明 |
|:-------|:------------|
| `el.MustClick()` | 点击元素 |
| `el.MustInput(text)` | 清空并输入文本 |
| `el.MustType(keys...)` | 模拟按键 |
| `el.MustText()` | 获取文本内容 |
| `el.MustHTML()` | 获取外部 HTML |
| `el.MustProperty(name)` | 获取 JS 属性值 |
| `el.MustAttribute(name)` | 获取 HTML 属性值 |
| `el.MustWaitStable()` | 等待位置/尺寸稳定 |
| `el.MustWaitVisible()` | 等待元素可见 |
| `el.MustWaitInvisible()` | 等待元素隐藏 |
| `el.MustParents(selector)` | 查找匹配选择器的父元素 |
| `el.MustElements(selector)` | 查找子元素 |
| `el.MustMatches(selector)` | 检查元素是否匹配选择器 |
| `el.MustEval(js)` | 执行 JS，`this` = 元素 |
| `el.MustScreenshot(path)` | 仅截取该元素 |

## Input (`rod/lib/input`)

| 常量 | 说明 |
|:---------|:------------|
| `input.Enter` | 回车键 |
| `input.Escape` | Esc 键 |
| `input.Tab` | Tab 键 |
| `input.Slash` | `/` 键 |
| `input.ControlLeft` | 左 Ctrl |
| `input.ShiftLeft` | 左 Shift |
| `input.KeyA` — `input.KeyZ` | 字母键 |
| `input.MouseLeft` | 鼠标左键 |

## Launcher (`rod/lib/launcher`)

| 方法 | 说明 |
|:-------|:------------|
| `launcher.New()` | 创建新 launcher |
| `l.Headless(bool)` | 启用/禁用无头模式 |
| `l.Devtools(bool)` | 自动打开 DevTools |
| `l.Proxy(addr)` | 设置代理服务器 |
| `l.Set(flag, value)` | 设置 Chrome CLI 标志 |
| `l.Delete(flag)` | 移除 Chrome CLI 标志 |
| `l.MustLaunch()` | 启动浏览器，返回控制 URL |
| `l.Cleanup()` | 终止浏览器进程 |
| `launcher.NewBrowser().MustGet()` | 下载浏览器二进制文件 |
| `launcher.Open(url)` | 在系统浏览器中打开 URL |

## Stealth (`go-rod/stealth`)

| API | 说明 |
|:----|:------------|
| `stealth.MustPage(browser)` | 创建 stealth 页面（出错时 panic） |
| `stealth.Page(browser)` | 创建 stealth 页面（返回错误） |
| `stealth.JS` | 包含所有 stealth 规避的原始 JS 字符串 |

**stealth.JS 注入内容：**
- 移除 `navigator.webdriver` 检测
- 伪装 WebGL vendor/renderer 为真实 GPU 值
- 修复 Chrome 插件数组（`PluginArray` 类型，数量=3）
- 修补权限 API（返回 `"prompt"`）
- 设置真实语言（`en-US,en`）
- 修复损坏的图片尺寸（16x16 而非 0x0）

## 网络劫持 (`rod.Hijack`)

| 方法 | 说明 |
|:-------|:------------|
| `router.MustAdd(pattern, handler)` | 添加 URL 模式处理器 |
| `router.Run()` | 开始拦截（用 `go` 调用） |
| `router.MustStop()` | 停止拦截 |
| `ctx.Request.Req()` | 访问 `*http.Request` |
| `ctx.Request.URL()` | 获取请求 URL |
| `ctx.LoadResponse(client, true)` | 从服务器加载响应 |
| `ctx.MustLoadResponse()` | 加载响应（出错时 panic） |
| `ctx.Response.Body()` | 获取响应体 |
| `ctx.Response.SetBody(s)` | 修改响应体 |
| `ctx.Response.Fail(reason)` | 阻止请求 |
| `ctx.Response.Payload()` | 获取响应元数据 |

## 直接 CDP (`rod/lib/proto`)

```go
// Call any CDP method directly
proto.PageSetAdBlockingEnabled{Enabled: true}.Call(page)

// Or via generic JSON API
page.Call(ctx, "", "Page.setAdBlockingEnabled", map[string]bool{"enabled": true})
```

完整 CDP 协议参考：https://chromedevtools.github.io/devtools-protocol/
