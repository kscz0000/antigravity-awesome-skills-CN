---
name: burp-suite-testing
description: "使用 Burp Suite 集成工具集执行全面的 Web 应用安全测试，包括 HTTP 流量拦截与修改、请求分析与重放、自动化漏洞扫描和手动测试工作流。当用户要求'使用 Burp Suite 进行安全测试'、'Web 应用渗透测试'、'HTTP 流量拦截'、'漏洞扫描'、'Burp Suite 测试'时使用。"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> 仅限授权使用：仅在授权的安全评估、防御性验证或受控教育环境中使用本技能。

# Burp Suite Web 应用测试

## 目的

使用 Burp Suite 集成工具集执行全面的 Web 应用安全测试，包括 HTTP 流量拦截与修改、请求分析与重放、自动化漏洞扫描和手动测试工作流。本技能通过基于代理的测试方法论，实现系统化的 Web 应用漏洞发现与利用。

## 输入 / 前置条件

### 所需工具
- 已安装 Burp Suite 社区版或专业版
- Burp 内置浏览器或已配置的外部浏览器
- 目标 Web 应用 URL
- 用于认证测试的有效凭据（如适用）

### 环境配置
- Burp Suite 已启动，使用临时或命名项目
- 代理监听器在 127.0.0.1:8080 上运行（默认）
- 浏览器已配置使用 Burp 代理（或使用 Burp 内置浏览器）
- 已安装 CA 证书以支持 HTTPS 拦截

### 版本对比
| 功能 | 社区版 | 专业版 |
|------|--------|--------|
| Proxy | ✓ | ✓ |
| Repeater | ✓ | ✓ |
| Intruder | 受限 | 完整 |
| Scanner | ✗ | ✓ |
| Extensions | ✓ | ✓ |

## 输出 / 交付物

### 主要输出
- 拦截和修改的 HTTP 请求/响应
- 包含修复建议的漏洞扫描报告
- HTTP 历史记录和站点地图文档
- 已识别漏洞的概念验证利用

## 核心工作流

### 阶段 1：拦截 HTTP 流量

#### 启动 Burp 内置浏览器
导航到集成浏览器以实现无缝代理集成：

1. 打开 Burp Suite 并创建/打开项目
2. 进入 **Proxy > Intercept** 选项卡
3. 点击 **Open Browser** 启动预配置浏览器
4. 调整窗口位置，同时查看 Burp 和浏览器

#### 配置拦截
控制哪些请求被捕获：

```
Proxy > Intercept > Intercept is on/off toggle

When ON: Requests pause for review/modification
When OFF: Requests pass through, logged to history
```

#### 拦截和转发请求
处理拦截的流量：

1. 将拦截开关设为 **Intercept on**
2. 在浏览器中导航到目标 URL
3. 在 Proxy > Intercept 选项卡中观察被拦截的请求
4. 检查请求内容（请求头、参数、请求体）
5. 点击 **Forward** 将请求发送到服务器
6. 继续转发后续请求直到页面加载完成

#### 查看 HTTP 历史
访问完整的流量日志：

1. 进入 **Proxy > HTTP history** 选项卡
2. 点击任意条目查看完整的请求/响应
3. 点击列标题排序（# 为时间顺序）
4. 使用过滤器聚焦相关流量

### 阶段 2：修改请求

#### 拦截并修改
在转发前修改请求参数：

1. 启用拦截：**Intercept on**
2. 在浏览器中触发目标请求
3. 在拦截的请求中定位要修改的参数
4. 在请求编辑器中直接编辑值
5. 点击 **Forward** 发送修改后的请求

#### 常见修改目标
| 目标 | 示例 | 目的 |
|------|------|------|
| 价格参数 | `price=1` | 测试业务逻辑 |
| 用户 ID | `userId=admin` | 测试访问控制 |
| 数量值 | `qty=-1` | 测试输入验证 |
| 隐藏字段 | `isAdmin=true` | 测试权限提升 |

#### 示例：价格篡改

```http
POST /cart HTTP/1.1
Host: target.com
Content-Type: application/x-www-form-urlencoded

productId=1&quantity=1&price=100

# Modify to:
productId=1&quantity=1&price=1
```

结果：商品以修改后的价格添加到购物车。

### 阶段 3：设置目标范围

#### 定义范围
将测试聚焦于特定目标：

1. 进入 **Target > Site map**
2. 在左侧面板中右键点击目标主机
3. 选择 **Add to scope**
4. 出现提示时，点击 **Yes** 排除范围外的流量

#### 按范围过滤
从 HTTP 历史中移除噪音：

1. 点击 HTTP 历史上方的显示过滤器
2. 选择 **Show only in-scope items**
3. 历史记录现在仅显示目标站点流量

#### 范围设定的好处
- 减少第三方请求的干扰
- 防止意外测试范围外的站点
- 提高扫描效率
- 生成更整洁的报告

### 阶段 4：使用 Burp Repeater

#### 发送请求到 Repeater
为手动测试准备请求：

1. 在 HTTP 历史中识别感兴趣的请求
2. 右键点击请求并选择 **Send to Repeater**
3. 进入 **Repeater** 选项卡访问请求

#### 修改并重发
高效测试不同输入：

```
1. View request in Repeater tab
2. Modify parameter values
3. Click Send to submit request
4. Review response in right panel
5. Use navigation arrows to review request history
```

#### Repeater 测试工作流

```
Original Request:
GET /product?productId=1 HTTP/1.1

Test 1: productId=2    → Valid product response
Test 2: productId=999  → Not Found response  
Test 3: productId='    → Error/exception response
Test 4: productId=1 OR 1=1 → SQL injection test
```

#### 分析响应
寻找漏洞指标：

- 暴露堆栈跟踪的错误消息
- 框架/版本信息泄露
- 不同响应长度暗示逻辑缺陷
- 时间差异暗示盲注注入
- 响应中的意外数据

### 阶段 5：运行自动化扫描

#### 启动新扫描
发起漏洞扫描（仅限专业版）：

1. 进入 **Dashboard** 选项卡
2. 点击 **New scan**
3. 在 **URLs to scan** 字段中输入目标 URL
4. 配置扫描设置

#### 扫描配置选项

| 模式 | 说明 | 持续时间 |
|------|------|----------|
| Lightweight | 高层概览 | 约 15 分钟 |
| Fast | 快速漏洞检查 | 约 30 分钟 |
| Balanced | 标准全面扫描 | 约 1-2 小时 |
| Deep | 深度测试 | 数小时 |

#### 监控扫描进度
跟踪扫描活动：

1. 在 **Dashboard** 中查看任务状态
2. 观察 **Target > Site map** 实时更新
3. 在 **Issues** 选项卡中检查发现的漏洞

#### 审查已识别的问题
分析扫描发现：

1. 在 Dashboard 中选择扫描任务
2. 进入 **Issues** 选项卡
3. 点击问题查看：
   - **Advisory**：描述和修复建议
   - **Request**：触发漏洞的 HTTP 请求
   - **Response**：显示漏洞的服务器响应

### 阶段 6：Intruder 攻击

#### 配置 Intruder
设置自动化攻击：

1. 发送请求到 Intruder（右键 > Send to Intruder）
2. 进入 **Intruder** 选项卡
3. 使用 § 标记定义 payload 位置
4. 选择攻击类型

#### 攻击类型

| 类型 | 说明 | 使用场景 |
|------|------|----------|
| Sniper | 单位置，遍历 payload | 模糊测试单个参数 |
| Battering ram | 所有位置使用相同 payload | 凭据测试 |
| Pitchfork | 并行 payload 迭代 | 用户名:密码对 |
| Cluster bomb | 所有 payload 组合 | 完整暴力破解 |

#### 配置 Payload

```
Positions Tab:
POST /login HTTP/1.1
...
username=§admin§&password=§password§

Payloads Tab:
Set 1: admin, user, test, guest
Set 2: password, 123456, admin, letmein
```

#### 分析结果
审查攻击输出：

- 按响应长度排序以发现异常
- 按状态码过滤成功的尝试
- 使用 grep 搜索特定字符串
- 导出结果用于文档记录

## 快速参考

### 键盘快捷键
| 操作 | Windows/Linux | macOS |
|------|---------------|-------|
| 转发请求 | Ctrl+F | Cmd+F |
| 丢弃请求 | Ctrl+D | Cmd+D |
| 发送到 Repeater | Ctrl+R | Cmd+R |
| 发送到 Intruder | Ctrl+I | Cmd+I |
| 切换拦截 | Ctrl+T | Cmd+T |

### 常用测试 Payload

```
# SQL Injection
' OR '1'='1
' OR '1'='1'--
1 UNION SELECT NULL--

# XSS
<script>alert(1)</script>
"><img src=x onerror=alert(1)>
javascript:alert(1)

# Path Traversal
../../../etc/passwd
..\..\..\..\windows\win.ini

# Command Injection
; ls -la
| cat /etc/passwd
`whoami`
```

### 请求修改技巧
- 右键点击获取上下文菜单选项
- 使用解码器进行编码/解码
- 使用 Comparer 工具比较请求
- 将感兴趣的请求保存到项目

## 约束与护栏

### 操作边界
- 仅测试已授权的应用
- 配置范围以防止意外测试范围外目标
- 限制扫描速率以避免拒绝服务
- 记录所有发现和操作

### 技术限制
- 社区版缺少自动化扫描器
- 某些站点可能阻止代理流量
- HSTS/证书固定可能需要额外配置
- 大量扫描可能触发 WAF 拦截

### 最佳实践
- 在大规模测试前始终设置目标范围
- 使用 Burp 内置浏览器确保可靠拦截
- 定期保存项目以保留工作
- 手动审查扫描结果以排除误报

## 示例

### 示例 1：业务逻辑测试

**场景**：电商价格篡改

1. 正常添加商品到购物车，拦截请求
2. 在 POST 请求体中识别 `price=9999` 参数
3. 修改为 `price=1`
4. 转发请求
5. 以篡改后的价格完成结账

**发现**：服务器信任客户端提供的价格值。

### 示例 2：认证绕过

**场景**：测试登录表单

1. 提交有效凭据，在 Repeater 中捕获请求
2. 发送到 Repeater 进行测试
3. 尝试：`username=admin' OR '1'='1'--`
4. 观察成功登录的响应

**发现**：认证中存在 SQL 注入。

### 示例 3：信息泄露

**场景**：基于错误的信息收集

1. 导航到产品页面，观察 `productId` 参数
2. 发送请求到 Repeater
3. 将 `productId=1` 改为 `productId=test`
4. 观察泄露框架版本的详细错误信息

**发现**：堆栈跟踪中暴露了 Apache Struts 2.5.12。

## 故障排除

### 浏览器无法通过代理连接
- 验证代理监听器是否活跃（Proxy > Options）
- 检查浏览器代理设置是否指向 127.0.0.1:8080
- 确保没有防火墙阻止本地连接
- 使用 Burp 内置浏览器确保可靠配置

### HTTPS 拦截失败
- 在浏览器/系统中安装 Burp CA 证书
- 导航到 http://burp 下载证书
- 将证书添加到受信任根证书
- 安装后重启浏览器

### 性能缓慢
- 限制范围以减少处理量
- 禁用不必要的扩展
- 在启动选项中增加 Java 堆内存
- 关闭未使用的 Burp 选项卡和功能

### 请求未被拦截
- 验证 "Intercept on" 是否已启用
- 检查拦截规则是否过滤了目标
- 确保浏览器正在使用 Burp 代理
- 验证目标是否使用了不支持的协议

## 何时使用
本技能适用于执行概述中描述的工作流或操作。
