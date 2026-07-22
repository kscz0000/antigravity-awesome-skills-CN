# 认证架构

## 概述

此技能使用**混合认证方法**，结合了两者的优点：

1. **持久浏览器配置文件**（`user_data_dir`）用于一致的浏览器指纹识别
2. **手动 Cookie 注入**，从 `state.json` 获取可靠的会话 cookie 持久化

## 为什么采用这种方法？

### 问题

Playwright/Patchright 有一个已知问题（[#36139](https://github.com/microsoft/playwright/issues/36139)），当使用 `launch_persistent_context()` 配合 `user_data_dir` 时，**会话 cookie**（没有 `Expires` 属性的 cookie）无法正确持久化。

**发生的情况：**
- ✅ 持久 cookie（有 `Expires` 日期）→ 正确保存到浏览器配置文件
- ❌ 会话 cookie（没有 `Expires`）→ **浏览器重启后丢失**

**影响：**
- 部分 Google 认证 cookie 是会话 cookie
- 用户遇到随机认证失败
- 「在我机器上能工作」综合症（取决于 Google 使用哪些 cookie）

### TypeScript vs Python

**MCP 服务器**（TypeScript）可以通过传递 `storage_state` 参数来解决这个问题：

```typescript
// TypeScript - 可行！
const context = await chromium.launchPersistentContext(userDataDir, {
  storageState: "state.json",  // ← 加载 cookie 包括会话 cookie
  channel: "chrome"
});
```

但 **Python 的 Playwright API 不支持这个**（[#14949](https://github.com/microsoft/playwright/issues/14949)）：

```python
# Python - 不支持！
context = playwright.chromium.launch_persistent_context(
    user_data_dir=profile_dir,
    storage_state="state.json",  # ← Python 中此参数不可用！
    channel="chrome"
)
```

## 我们的解决方案：混合方法

我们使用**两阶段认证系统**：

### 阶段 1：设置（`auth_manager.py setup`）

1. 使用 `user_data_dir` 启动持久上下文
2. 用户手动登录
3. **将状态保存到两个位置：**
   - 浏览器配置文件目录（自动，用于指纹 + 持久 cookie）
   - `state.json` 文件（显式保存，用于会话 cookie）

```python
context = playwright.chromium.launch_persistent_context(
    user_data_dir="browser_profile/",
    channel="chrome"
)
# 用户登录...
context.storage_state(path="state.json")  # 保存所有 cookie
```

### 阶段 2：运行时（`ask_question.py`）

1. 使用 `user_data_dir` 启动持久上下文（加载指纹 + 持久 cookie）
2. **手动注入 cookie** 从 `state.json`（添加会话 cookie）

```python
# 步骤 1：使用浏览器配置文件启动
context = playwright.chromium.launch_persistent_context(
    user_data_dir="browser_profile/",
    channel="chrome"
)

# 步骤 2：从 state.json 手动注入 cookie
with open("state.json", 'r') as f:
    state = json.load(f)
    context.add_cookies(state['cookies'])  # ← 会话 cookie 的解决方案！
```

## 优势

| 特性 | 我们的方法 | 纯 `user_data_dir` | 纯 `storage_state` |
|------|-----------|-------------------|-------------------|
| **浏览器指纹一致性** | ✅ 重启后相同 | ✅ 相同 | ❌ 每次变化 |
| **会话 Cookie 持久化** | ✅ 手动注入 | ❌ 丢失（问题） | ✅ 原生支持 |
| **持久 Cookie 持久化** | ✅ 自动 | ✅ 自动 | ✅ 原生支持 |
| **Google 信任** | ✅ 高（相同浏览器） | ✅ 高 | ❌ 低（新浏览器） |
| **跨平台可靠性** | ✅ 需要 Chrome | ⚠️ Chromium 问题 | ✅ 可移植 |
| **缓存性能** | ✅ 保留缓存 | ✅ 保留缓存 | ❌ 无缓存 |

## 文件结构

```
~/.claude/skills/notebooklm/data/
├── auth_info.json              # 关于认证的元数据
├── browser_state/
│   ├── state.json             # Cookie + localStorage（用于手动注入）
│   └── browser_profile/       # Chrome 用户配置文件（用于指纹 + 缓存）
│       ├── Default/
│       │   ├── Cookies        # 仅持久 cookie（会话 cookie 缺失！）
│       │   ├── Local Storage/
│       │   └── Cache/
│       └── ...
```

## 为什么 `state.json` 至关重要

即使我们使用 `user_data_dir`，我们**仍然需要 `state.json`**，因为：

1. **会话 cookie** 不会保存到浏览器配置文件（Playwright 问题）
2. **手动注入**是加载会话 cookie 的唯一可靠方式
3. **验证** - 我们可以在启动前检查 cookie 是否过期

## 代码参考

**设置：** `scripts/auth_manager.py:94-120`
- 第 100-113 行：使用 `channel="chrome"` 启动持久上下文
- 第 167 行：通过 `context.storage_state()` 保存到 `state.json`

**运行时：** `scripts/ask_question.py:77-118`
- 第 86-99 行：启动持久上下文
- 第 101-118 行：手动 cookie 注入解决方案

**验证：** `scripts/auth_manager.py:236-298`
- 第 262-275 行：启动持久上下文
- 第 277-287 行：用于验证的手动 cookie 注入

## 相关问题

- [microsoft/playwright#36139](https://github.com/microsoft/playwright/issues/36139) - 会话 cookie 不持久化
- [microsoft/playwright#14949](https://github.com/microsoft/playwright/issues/14949) - 持久上下文的存储状态
- [StackOverflow 问题](https://stackoverflow.com/questions/79641481/) - 会话 cookie 持久化问题

## 未来改进

如果 Playwright 在 Python 的 `launch_persistent_context()` 中添加对 `storage_state` 参数的支持，我们可以简化为：

```python
# 未来（当 Python API 支持时）：
context = playwright.chromium.launch_persistent_context(
    user_data_dir="browser_profile/",
    storage_state="state.json",  # ← 会自动处理所有内容！
    channel="chrome"
)
```

在此之前，我们的混合方法是最可靠的解决方案。
