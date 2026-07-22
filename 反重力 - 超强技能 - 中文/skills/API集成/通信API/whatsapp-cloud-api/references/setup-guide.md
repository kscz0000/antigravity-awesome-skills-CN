# 完整设置指南 - WhatsApp Business Cloud API

> 从零开始到在生产环境中发送第一条消息。
> 预计时间：1-2 小时（不进行企业验证）| 3-7 天（含验证）

---

## 前置条件

- 有效的电子邮件（建议使用企业邮箱）
- 个人身份证件
- **未注册**到个人 WhatsApp 的电话号码
- CNPJ 或公司文件（用于企业验证）
- 更新后的浏览器（推荐使用 Chrome）

---

## 步骤 1 - 在 Meta Business Suite 中创建账户

### URL
```
https://business.facebook.com/overview
```

### 操作流程

1. 访问 `https://business.facebook.com/overview`
2. 点击 **"创建账户"**
3. 如果您已有个人 Facebook 账号，请先登录。否则将提示您创建一个
4. 填写以下字段：
   - **公司名称**：使用您业务的正式/商号名称
   - **您的姓名**：账户管理员的姓名
   - **企业邮箱**：建议使用企业邮箱（例如：`contato@suaempresa.com.br`）
5. 点击 **"提交"**
6. 访问您的邮箱，点击 Meta 发送的确认链接
7. 确认后，您将被重定向到 Meta Business Suite 控制面板

### 常见错误

| 错误 | 解决方案 |
|------|---------|
| "此邮箱已关联到另一个账户" | 使用其他邮箱或在 `business.facebook.com/settings` 恢复现有账户的访问权限 |
| "无法创建账户" | 禁用广告拦截扩展（uBlock、AdBlock）后重试 |
| 未收到确认邮件 | 检查垃圾邮件文件夹。5 分钟后尝试重新发送。如果仍有问题，请使用其他邮箱 |
| 账户创建后立即被封禁 | 在新创建的 Facebook 个人资料上的账户可能会被标记。请等待 24 小时后重试 |

### 完成

您应该拥有：
- 访问 `business.facebook.com` 控制面板的权限
- 在 `Business Settings > Business Info` 中可见的 **Business ID**（类似 `123456789012345` 的数字）
- 已确认的邮箱

---

## 步骤 2 - 在 Meta for Developers 中创建应用

### URL
```
https://developers.facebook.com/apps
```

### 操作流程

1. 访问 `https://developers.facebook.com/apps`
2. 如果是首次使用，请点击 **"开始"** 并接受开发者条款
3. 点击 **"创建应用"** 按钮
4. 选择应用类型：**"企业"**（Business）
   - 不要选择 "无"、"消费者" 或 "游戏"
5. 填写：
   - **应用名称**：例如 `我的应用 WhatsApp API`
   - **联系邮箱**：您的企业邮箱
   - **企业账户**：选择在步骤 1 中创建的账户
6. 点击 **"创建应用"**
7. 系统可能会要求您再次输入 Facebook 密码

### 常见错误

| 错误 | 解决方案 |
|------|---------|
| "您已达到应用程序数量上限" | 新账户有上限。请在 `developers.facebook.com/apps` 中删除旧的测试应用 |
| "企业"类型未显示 | 确保在步骤 1 中正确创建了企业账户 |
| "未找到企业账户" | 返回步骤 1 验证企业账户是否处于活动状态。尝试在 Business Settings > Accounts > Apps 中手动链接 |
| 创建时权限错误 | 验证您是企业账户的管理员 |

### 完成

您应该拥有：
- 在 `developers.facebook.com/apps` 中可见的已创建应用
- **App ID**（类似 `1234567890123456` 的数字）
- 应用状态为 **"开发中"**

---

## 步骤 3 - 添加 WhatsApp 产品

### URL
```
https://developers.facebook.com/apps/{您的_APP_ID}/dashboard/
```

### 操作流程

1. 在应用控制面板中，向下滚动到 **"向您的应用添加产品"** 部分
2. 找到 **"WhatsApp"** 卡片并点击 **"设置"**
3. 接受 **WhatsApp Business 服务条款**
4. 选择链接的 **企业账户**（与步骤 1 中相同）
5. 点击 **"继续"**
6. 您将被重定向到您应用中的 WhatsApp 面板

### 常见错误

| 错误 | 解决方案 |
|------|---------|
| WhatsApp 卡片未显示 | 验证应用类型为 "企业"。如果不是，请使用正确的类型创建新应用 |
| "您没有权限" | 确认您是链接的企业账户的管理员 |
| 服务条款无法加载 | 清除浏览器缓存或尝试在隐身窗口中操作 |
| "无法创建 WhatsApp Business 账户" | 您的企业账户可能受到限制。请在 `business.facebook.com` 中检查通知 |

### 完成

您应该拥有：
- 侧边栏菜单中带有 **"WhatsApp > 配置"**（或 "Getting Started"）选项
- 自动创建的 **WhatsApp Business Account (WABA)**
- 访问 WhatsApp 的 Getting Started 页面

---

## 步骤 4 - 获取 Phone Number ID 和 WABA ID

### URL
```
https://developers.facebook.com/apps/{您的_APP_ID}/whatsapp-business/wa-dev-console/
```

### 操作流程

1. 在应用侧边栏菜单中，点击 **"WhatsApp" > "API 配置"**（或 "API Setup"）
2. 在 **"电话号码信息"** 部分，您将找到：
   - **Phone Number ID**：号码的唯一标识符（例如：`109876543210987`）
   - **WhatsApp Business Account ID (WABA ID)**：WhatsApp Business 账户的标识符（例如：`102345678901234`）
3. 记下这两个值。您将在所有 API 调用中需要它们

### 查找每个 ID 的位置

```
App Dashboard
  └── WhatsApp
       └── API 配置 (API Setup)
            ├── Phone Number ID .... "Phone number ID" 或 "ID do numero" 字段
            └── WABA ID ........... "WhatsApp Business Account ID" 字段
```

WABA ID 的替代查找方式：
```
https://business.facebook.com/settings/whatsapp-business-accounts/
```
点击账户时，ID 出现在 URL 中或详情列中。

### 常见错误

| 错误 | 解决方案 |
|------|---------|
| Phone Number ID 未显示 | 确认已完成步骤 3。尝试刷新页面 |
| WABA ID 不可见 | 通过 Business Settings > Accounts > WhatsApp Business Accounts 访问 |
| 不同页面显示不同值 | 始终使用应用 API Setup 页面中显示的 ID |
| "No phone numbers" | 测试号码尚未配置。请等待几分钟后重新加载 |

### 完成

您应该已经记下：
- **Phone Number ID**：`___________________________`
- **WABA ID**：`___________________________`
- **App ID**：`___________________________`（来自步骤 2）

---

## 步骤 5 - 生成临时测试 Token

### URL
```
https://developers.facebook.com/apps/{您的_APP_ID}/whatsapp-business/wa-dev-console/
```

### 操作流程

1. 在 **"API 配置"** 页面，找到 **"临时访问 Token"** 部分
2. 点击 **"生成访问 Token"**（或 Token 字段旁边的按钮）
3. 系统可能会要求额外登录或确认
4. Token 将显示 - **立即复制**

### 关于临时 Token

```
重要提示：
- 24 小时后过期（有时为 1 小时）
- 仅用于初始测试
- 不要在生产环境中使用
- 有关永久 Token，请参阅步骤 9
```

### 通过 cURL 测试 Token

```bash
curl -X GET \
  "https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}" \
  -H "Authorization: Bearer {您的临时TOKEN}"
```

预期响应（摘要）：
```json
{
  "id": "109876543210987",
  "display_phone_number": "+1 555-XXX-XXXX",
  "verified_name": "Seu Nome de Teste"
}
```

### 常见错误

| 错误 | 解决方案 |
|------|---------|
| 点击后 Token 不显示 | 禁用弹窗拦截程序。尝试其他浏览器 |
| "Error validating access token" | Token 已过期。生成新的 |
| "Invalid OAuth access token" | 重新复制 Token，确保首尾没有多余空格 |
| 生成按钮被禁用 | 验证 WhatsApp 产品已正确添加（步骤 3） |

### 完成

您应该拥有：
- 复制并保存到安全位置的 **临时访问 Token**
- 通过 cURL 确认 Token 有效

---

## 步骤 6 - 使用测试号码（沙盒）进行测试

### URL
```
https://developers.facebook.com/apps/{您的_APP_ID}/whatsapp-business/wa-dev-console/
```

### 操作流程

Meta 提供 **测试号码**，以便您在不需要真实号码的情况下发送消息。

1. 在 API Setup 页面，找到 **"发送和接收消息"** 部分
2. **"发件人"** 字段应已显示 Meta 的测试号码
3. 在 **"收件人"** 部分，点击 **"管理电话号码列表"**（或 "Manage phone number list"）
4. 点击 **"添加电话号码"**
5. 输入带国家代码的收件人号码（例如：`+5511999998888`）
6. 您将在该号码上通过 WhatsApp 收到 **验证码**
7. 输入代码进行确认
8. 然后通过点击 **"发送消息"** 发送测试消息

### 通过 cURL 发送

```bash
curl -X POST \
  "https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages" \
  -H "Authorization: Bearer {您的TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "5511999998888",
    "type": "template",
    "template": {
      "name": "hello_world",
      "language": {
        "code": "en_US"
      }
    }
  }'
```

预期响应：
```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "5511999998888",
      "wa_id": "5511999998888"
    }
  ],
  "messages": [
    {
      "id": "wamid.XXXXXXXXXXXXXXXX"
    }
  ]
}
```

### 沙盒限制

- 最多注册 **5 个收件人号码**
- 仅限预先批准的模板（如 `hello_world`）
- 发件人号码为 Meta 的测试号码（不可自定义）
- 消息可能需要 1 分钟才能到达

### 常见错误

| 错误 | 解决方案 |
|------|---------|
| `131030` - "User's phone number is part of an experiment" | 收件人号码可能受到限制。尝试其他号码 |
| `131026` - "Message failed to send" | 验证收件人号码是否有活跃的 WhatsApp 账户 |
| `100` - "Invalid parameter" | 检查号码格式：仅数字，含国家代码，JSON 中不带 `+` |
| `130429` - "Rate limit hit" | 等待 1 分钟后重试。沙盒有严格的限制 |
| 未收到验证码 | 目标号码必须安装并激活 WhatsApp |
| 未找到模板 `hello_world` | 验证语言设置为 `en_US`。此模板已预装 |

### 完成

您应该拥有：
- 在收件人的 WhatsApp 中收到的测试消息
- API 返回的 `message_id`（wamid）
- 对 API 正常工作的信心

---

## 步骤 7 - 添加真实电话号码

### URL
```
https://business.facebook.com/settings/whatsapp-business-accounts/{WABA_ID}/phone-numbers
```

或通过应用控制面板：
```
https://developers.facebook.com/apps/{您的_APP_ID}/whatsapp-business/wa-dev-console/
```

### 关键前置条件

```
您要添加的电话号码必须：
  - 未注册到个人 WhatsApp
  - 未注册到 WhatsApp Business App
  - 能够接收短信或语音通话
  - 可以是固定电话（通过电话验证）或移动电话（短信或电话）

如果该号码已在个人 WhatsApp 中：
  1. 在手机上打开 WhatsApp
  2. 进入 设置 > 账户 > 删除我的账户
  3. 确认删除
  4. 等待 5 分钟后再继续
```

### 操作流程

1. 在 API Setup 页面，点击 **"添加电话号码"**（或通过 Business Settings URL 访问）
2. 填写商业资料信息：
   - **显示名称**：在 WhatsApp 中显示的名称（例如：`我的公司`）
   - **类别**：选择您业务的类别
   - **描述**（可选）：公司的简要描述
3. 点击 **"下一步"**
4. 输入带国家代码的号码：`+55 11 99999-8888`
5. 选择验证方式（步骤 8）

### 显示名称规则

- 必须清晰地代表您的公司
- 不能仅包含通用字符（"测试"、"管理员"）
- 不能侵犯注册商标
- 必须介于 3 到 512 个字符之间
- Meta 可能会拒绝并要求修改

### 常见错误

| 错误 | 解决方案 |
|------|---------|
| "此号码已注册" | 该号码仍注册在个人 WhatsApp 中。按上述说明删除账户后等待 |
| "号码无效" | 使用含国家代码的完整国际格式 |
| "显示名称被拒绝" | 使用公司正式名称。避免过度缩写 |
| "已达到号码上限" | 未验证的账户只能有 2 个号码。完成步骤 10 |
| 固定电话不被接受 | 固定电话可被接受。选择 "语音通话" 作为验证方法 |

### 完成

您应该拥有：
- 已添加到 WABA 电话列表的号码
- 下一步：通过 OTP 验证（步骤 8）

---

## 步骤 8 - 通过 OTP 验证号码

### 操作流程

直接从步骤 7 继续：

1. 选择验证方式：
   - **短信（SMS）**：推荐用于移动电话
   - **语音通话**：固定电话必需
2. 点击 **"发送代码"**
3. 等待接收 6 位数代码
4. 在验证字段中输入代码
5. 点击 **"验证"**

### 通过 API 验证（替代方法）

请求代码：
```bash
curl -X POST \
  "https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/request_code" \
  -H "Authorization: Bearer {您的TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "code_method": "SMS",
    "language": "pt_BR"
  }'
```

确认代码：
```bash
curl -X POST \
  "https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/verify_code" \
  -H "Authorization: Bearer {您的TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "123456"
  }'
```

### 常见错误

| 错误 | 解决方案 |
|------|---------|
| 未通过短信收到代码 | 尝试 "语音通话"。验证该号码未屏蔽服务类消息 |
| "代码无效" | 验证输入是否正确。代码在 10 分钟后过期 |
| "尝试次数过多" | 等待 1 小时后重试。每段时间有尝试次数限制 |
| 未收到语音通话 | 验证该号码是否接受国际电话 |
| "电话号码验证失败" | 确保该号码未在其他 WhatsApp Business 账户中 |

### 完成

您应该拥有：
- 在面板中状态为 **"已验证"**（或 "Connected"）的号码
- 真实号码的新 **Phone Number ID**（与测试号码不同）
- 能够使用您自己的号码发送消息

---

## 步骤 9 - 创建 System User 和永久 Token

### URL
```
https://business.facebook.com/settings/system-users
```

### 为什么要用 System User？

步骤 5 中的临时 Token 过期很快。对于生产环境，您需要一个链接到 **System User** 的 **永久 Token**，它不依赖于个人登录。

### 操作流程

#### 9.1 - 创建 System User

1. 访问 `https://business.facebook.com/settings`
2. 在侧边栏菜单中，点击 **"用户" > "系统用户"**（System Users）
3. 点击 **"添加"**
4. 填写：
   - **名称**：例如 `whatsapp-api-bot`
   - **角色**：选择 **"管理员"**（需要完整权限）
5. 点击 **"创建系统用户"**

#### 9.2 - 为 System User 分配资产

1. 点击已创建的 System User
2. 点击 **"分配资产"**（Assign Assets）
3. 在侧边栏中选择 **"应用"**
4. 找到您的应用（在步骤 2 中创建）并选择
5. 启用 **"完全控制"**（Full Control）
6. 点击 **"保存更改"**
7. 对 **"WhatsApp 账户"** 重复操作：
   - 选择您的 WABA
   - 启用 **"完全控制"**
   - 保存

#### 9.3 - 生成永久 Token

1. 在 System User 页面，点击 **"生成新 Token"**
2. 选择 **应用**（在步骤 2 中创建）
3. 在 **"可用权限"** 中，勾选：
   - `whatsapp_business_messaging` - 用于发送和接收消息
   - `whatsapp_business_management` - 用于管理账户、模板和配置
4. 点击 **"生成 Token"**
5. **立即复制 TOKEN** - 它只会显示一次
6. 存储在安全位置（密码管理器、环境变量、密钥保险库）

### Token 安全

```
注意：
- Token 绝不能提交到 Git 仓库
- 使用环境变量（.env）或密钥管理服务
- 定期轮换 Token
- 如果 Token 泄露，请立即在 Business Settings 中撤销
```

### 测试永久 Token

```bash
curl -X GET \
  "https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}" \
  -H "Authorization: Bearer {永久TOKEN}"
```

### 常见错误

| 错误 | 解决方案 |
|------|---------|
| 菜单中不显示"系统用户" | 您需要是企业账户的管理员。验证您的权限 |
| 权限列表中不显示 `whatsapp_*` | 您的应用未添加 WhatsApp 产品（返回步骤 3） |
| 使用 Token 时出现 "权限不足" | 验证资产（App + WABA）是否已正确分配给 System User |
| 生成后 Token 无效 | 等待 1-2 分钟以完成传播。然后重试 |
| "User does not have permission" | 验证 System User 是否有 "Admin" 角色和对资产的完全控制权限 |

### 完成

您应该拥有：
- 使用描述性名称创建的 System User
- 资产（App + WABA）已分配完全控制权限
- 已复制并安全存储的 **永久 Token**
- 通过 API 调用验证有效的 Token

---

## 步骤 10 - 企业验证

### URL
```
https://business.facebook.com/settings/security
```

### 为什么要验证？

未进行企业验证时：
- 限制为每个企业每 24 小时 **250 个发起的对话**
- 无法申请提高限额
- 某些功能受到限制

进行验证后：
- 限额可逐步提高到 **无限制**
- 访问高级功能
- 在 Meta 面前具有更高的可信度

### 操作流程

1. 访问 `https://business.facebook.com/settings`
2. 在侧边栏菜单中，点击 **"安全中心"**（Security Center）
3. 找到 **"企业验证"** 部分，点击 **"开始验证"**
4. 填写公司信息：
   - **公司法定名称**：与 CNPJ 上的一致
   - **地址**：公司的官方地址
   - **公司电话**：商务电话号码
   - **网站**：公司网站的 URL
   - **CNPJ**：国家注册号
5. 上传 **证明文件**（至少一份）：
   - CNPJ 登记证
   - 以公司名义开具的水电费账单
   - 包含公司名称和地址的银行对账单
   - 营业执照
   - 公司章程
6. 选择 **联系验证方式**：
   - 公司域名的邮箱（更快）
   - 公司电话
   - 附加文件
7. 点击 **"提交"**

### 快速审批的提示

- 使用公司域名的邮箱（例如：`admin@suaempresa.com.br`）而不是 Gmail/Hotmail
- 确保 Meta 中的公司名称与文件中的名称**完全**一致
- 公司网站必须处于活跃且可访问状态
- 文件必须清晰可读，采用 PDF 或图像格式
- 文件签发时间应少于 90 天（对账单和银行账单而言）

### 时间表

| 场景 | 预计时间 |
|---------|---------------|
| 文件齐全 + 企业邮箱 | 1-3 个工作日 |
| 文件齐全 + 电话验证 | 3-5 个工作日 |
| 文件不完整 / 拒绝后重新提交 | 5-14 个工作日 |

### 常见错误

| 错误 | 解决方案 |
|------|---------|
| "文件被拒绝" | 验证文件上的名称是否与注册名称一致。提交更新的文件 |
| "无法验证" | 尝试其他类型的文件。添加更多文件 |
| 验证超过 7 天仍未完成 | 在 `business.facebook.com/help` 提交支持工单 |
| "域名未验证" | 在您域名的 DNS 中添加验证 TXT 记录 |
| 未收到验证邮件 | 检查垃圾邮件。尝试电话方式 |

### 完成

您应该拥有：
- 在安全中心中状态为 **"已验证"**（绿色徽章）
- 可访问渐进式消息限额
- 可以升级到 1K、10K、100K 和无限制

---

## 验证后消息限额等级

| 等级 | 发起的对话（24 小时） | 如何达到 |
|-------|---------------------------|---------------|
| 未验证 | 250 | 默认初始值 |
| 等级 1 | 1,000 | 完成企业验证 |
| 等级 2 | 10,000 | 7 天内发送 2 倍当前限额且质量良好 |
| 等级 3 | 100,000 | 保持质量和数量 |
| 等级 4 | 无限制 | 保持质量一致 |

---

## 设置后检查清单

完成所有 10 个步骤后，您应拥有以下值。填写并存储在 `.env` 文件中：

```bash
# ===================================
# WhatsApp Cloud API - 环境变量
# ===================================

# 步骤 1 - Meta Business Suite
META_BUSINESS_ID=          # Business 账户 ID（15 位数字）

# 步骤 2 - Meta for Developers 中的应用
META_APP_ID=               # 应用 ID
META_APP_SECRET=           # 应用密钥（在 App Settings > Basic 中）

# 步骤 4 - WhatsApp ID
WHATSAPP_PHONE_NUMBER_ID=  # Phone Number ID（真实号码，非测试号码）
WHATSAPP_WABA_ID=          # WhatsApp Business Account ID

# 步骤 9 - 永久 Token
WHATSAPP_API_TOKEN=        # System User 的 Token（永久）

# API 配置
WHATSAPP_API_VERSION=v21.0
WHATSAPP_API_URL=https://graph.facebook.com

# Webhook（单独配置）
WEBHOOK_VERIFY_TOKEN=      # 您为验证 webhook 而定义的 Token
WEBHOOK_URL=               # 您服务器的公共 URL（必须使用 HTTPS）
```

### 最终验证

运行此命令以验证一切正常工作：

```bash
# 将变量替换为您的实际值
curl -X POST \
  "https://graph.facebook.com/v21.0/${WHATSAPP_PHONE_NUMBER_ID}/messages" \
  -H "Authorization: Bearer ${WHATSAPP_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "收件人号码",
    "type": "template",
    "template": {
      "name": "hello_world",
      "language": {
        "code": "en_US"
      }
    }
  }'
```

如果您收到包含 `"messages": [{"id": "wamid.XXXX"}]` 的 JSON，则您的设置已完成。

---

## 实用链接

| 资源 | URL |
|---------|-----|
| 官方文档 | `https://developers.facebook.com/docs/whatsapp/cloud-api` |
| API 参考 | `https://developers.facebook.com/docs/whatsapp/cloud-api/reference` |
| 平台状态 | `https://metastatus.com` |
| 商家支持 | `https://business.facebook.com/help` |
| 开发者社区 | `https://developers.facebook.com/community` |
| API 更新日志 | `https://developers.facebook.com/docs/whatsapp/cloud-api/changelog` |
| 模板指南 | `https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates` |
| Webhook 指南 | `https://developers.facebook.com/docs/whatsapp/cloud-api/guides/set-up-webhooks` |

---

> **下一步**：配置 webhook 以接收消息。请参阅项目文档中的 webhook 指南。
