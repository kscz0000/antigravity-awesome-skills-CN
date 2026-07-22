# 设置指南 — Meta App 和 OAuth

## 前提条件

1. Instagram Business 或 Creator 账号
2. 与 IG 账号关联的 Facebook 主页（Business 必需，Creator 推荐）
3. Meta 开发者账号（developers.facebook.com）

## 步骤 1：创建 Meta App

1. 访问 [Meta for Developers](https://developers.facebook.com/apps/)
2. 点击 "Create App"
3. 选择 "Business" 作为类型
4. 填写：
   - **App name**: 应用名称（例如："我的 Instagram 管理器"）
   - **Contact email**: 你的邮箱
   - **Business account**: 选择或创建
5. 点击 "Create App"

## 步骤 2：添加 Instagram API

1. 在应用仪表板中，进入 "Add Products"
2. 找到 "Instagram" 并点击 "Set Up"
3. 在 "Instagram Graph API" 下，点击 "Configure"

## 步骤 3：配置 OAuth

### 重定向 URI
1. 进入 Settings → Basic
2. 在 "Valid OAuth Redirect URIs" 中添加：
   ```
   http://localhost:8765/callback
   ```
   （这是 auth.py 的默认端口）

### 获取凭证
1. 记下 **App ID**（在仪表板顶部可见）
2. 进入 Settings → Basic → **App Secret**（点击 "Show"）
3. 保存两者 — 设置时会用到

## 步骤 4：添加测试用户（开发模式）

在开发模式下，只有测试用户可以使用应用：

1. App Dashboard → Roles → Roles
2. 点击 "Add Testers"
3. 添加要管理的 Instagram 账号
4. 测试用户需要通过 Instagram 的 Settings → Apps and Websites 接受邀请

## 步骤 5：配置权限

1. App Dashboard → App Review → Permissions and Features
2. 请求以下权限：
   - `instagram_basic`
   - `instagram_content_publish`
   - `instagram_manage_comments`
   - `instagram_manage_insights`
   - `instagram_manage_messages`
   - `pages_show_list`
   - `pages_read_engagement`

**注意：** 在开发模式下，权限对测试用户有效，无需正式审批。

## 步骤 6：运行 auth.py

准备好 App ID 和 App Secret 后：

```bash
python C:\Users\renat\skills\instagram\scripts\auth.py --setup
```

脚本会：
1. 请求 App ID 和 App Secret
2. 在浏览器中打开 Facebook 授权页面
3. 你授权应用和权限
4. 浏览器重定向到 `localhost:8765/callback`
5. 脚本捕获代码，交换为短期令牌，然后是长期令牌
6. 通过 Facebook Pages API 发现关联的 IG 账号
7. 将所有内容保存到 SQLite 数据库

### 预期结果：
```json
{
  "status": "success",
  "account": {
    "ig_user_id": "17841400000000",
    "username": "你的账号",
    "account_type": "BUSINESS",
    "token_expires_at": "2026-04-26T..."
  }
}
```

## 步骤 7：验证

```bash
# 验证令牌和账号
python C:\Users\renat\skills\instagram\scripts\auth.py --status

# 测试读取个人资料
python C:\Users\renat\skills\instagram\scripts\profile.py --view

# 测试列出媒体
python C:\Users\renat\skills\instagram\scripts\media.py --list --limit 3
```

## 故障排除

### "No Instagram Business Account found"
- 验证 IG 账号是 Business 或 Creator（不是 Personal）
- 验证 Facebook 主页已关联到 IG 账号
- 运行：`python scripts/account_setup.py --check`

### "Invalid OAuth redirect_uri"
- 确认 `http://localhost:8765/callback` 在应用的重定向 URI 中
- 检查 URL 中是否有多余空格

### "App not approved"
- 在开发模式下，将你的个人资料添加为测试用户
- 对于生产环境，提交 App Review

### 令牌过期
```bash
python C:\Users\renat\skills\instagram\scripts\auth.py --refresh
```
长期令牌有效期为 60 天，在剩余 7 天时自动刷新。

### "Permission denied"（代码 10/200）
- 验证是否授权了所需的权限范围
- 查看 `references/permissions.md` 了解正确的权限范围
- 可能需要重新授权：`python scripts/auth.py --setup`

## 环境变量（可选）

可以不使用输入，而是使用环境变量：
```bash
export INSTAGRAM_APP_ID="你的_app_id"
export INSTAGRAM_APP_SECRET="你的_app_secret"
export IMGUR_CLIENT_ID="你的_imgur_client_id"
```

`config.py` 会在请求输入之前检查环境变量。
