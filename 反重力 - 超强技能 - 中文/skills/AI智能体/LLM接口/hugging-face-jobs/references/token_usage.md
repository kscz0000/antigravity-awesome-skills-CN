# Hugging Face Jobs 的 Token 使用指南

**⚠️ 关键：** 正确的 Token 使用对于任何与 Hugging Face Hub 交互的任务都至关重要。

## 概述

Hugging Face Token 是允许您的任务与 Hub 交互的认证凭证。在以下情况需要 Token：
- 推送模型/数据集到 Hub
- 访问私有仓库
- 创建新仓库
- 以编程方式使用 Hub API
- 任何需要认证的 Hub 操作

## Token 类型

### 读取 Token
- **权限：** 下载模型/数据集，读取私有仓库
- **适用场景：** 仅需要下载/读取内容的任务
- **创建：** https://huggingface.co/settings/tokens

### 写入 Token
- **权限：** 推送模型/数据集，创建仓库，修改内容
- **适用场景：** 需要上传结果的任务（最常见）
- **创建：** https://huggingface.co/settings/tokens
- **⚠️ 以下操作必需：** 推送模型、数据集或任何上传操作

### 组织 Token
- **权限：** 代表组织执行操作
- **适用场景：** 在组织命名空间下运行的任务
- **创建：** 组织设置 → Tokens

## 向任务提供 Token

### 方法一：`hf_jobs` MCP 工具配合 `$HF_TOKEN`（推荐）⭐

```python
hf_jobs("uv", {
    "script": "your_script.py",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # ✅ 自动替换
})
```

**工作原理：**
1. `$HF_TOKEN` 是一个占位符，会被替换为您的实际 Token
2. 使用您已登录会话中的 Token（`hf auth login`）
3. 作为 secret 传递时 Token 在服务端加密
4. 最安全便捷的方法

**优点：**
- ✅ 代码中不暴露 Token
- ✅ 使用您当前的登录会话
- ✅ 重新登录后自动更新
- ✅ 与 MCP 工具无缝配合
- ✅ Token 在服务端加密

**要求：**
- 必须已登录： `hf auth login` 或 `hf_whoami()` 能正常工作
- Token 必须具有所需权限

**⚠️ 关键：** `$HF_TOKEN` 自动替换**仅**是 `hf_jobs` MCP 工具的功能。它**不**适用于 `HfApi().run_uv_job()` —— 参见下方方法 1b。

### 方法 1b：`HfApi().run_uv_job()` 配合 `get_token()`（Python API 必需）

```python
from huggingface_hub import HfApi, get_token
api = HfApi()
api.run_uv_job(
    script="your_script.py",
    secrets={"HF_TOKEN": get_token()},  # ✅ 传入实际 Token 值
)
```

**工作原理：**
1. `get_token()` 从您已登录的会话中检索 Token
2. 实际 Token 值被传递给 `secrets` 参数
3. Token 在服务端加密

**为什么 `"$HF_TOKEN"` 在 `HfApi().run_uv_job()` 中会失败：**
- Python API 将字面字符串 `"$HF_TOKEN"`（9 个字符）作为 Token 传递
- Jobs 服务器接收到的是无效字符串而非真实 Token
- 结果：脚本尝试认证时出现 `401 Unauthorized` 错误
- 您**必须**使用 `huggingface_hub` 中的 `get_token()` 来获取真实 Token

### 方法二：显式 Token（不推荐）

```python
hf_jobs("uv", {
    "script": "your_script.py",
    "secrets": {"HF_TOKEN": "hf_abc123..."}  # ⚠️ 硬编码 Token
})
```

**使用场景：**
- 仅当自动 Token 不工作时
- 使用特定 Token 测试
- 组织 Token（谨慎使用）

**安全隐患：**
- ❌ Token 在代码/日志中可见
- ❌ Token 轮换时需手动更新
- ❌ Token 泄露风险
- ❌ 不推荐用于生产环境

### 方法三：环境变量（安全性较低）

```python
hf_jobs("uv", {
    "script": "your_script.py",
    "env": {"HF_TOKEN": "hf_abc123..."}  # ⚠️ 安全性低于 secrets
})
```

**与 secrets 的区别：**
- `env` 变量在任务日志中可见
- `secrets` 在服务端加密
- 始终优先使用 `secrets` 传递 Token

**使用场景：**
- 仅用于非敏感配置
- 绝不用于 Token（改用 `secrets`）

## 在脚本中使用 Token

### 访问 Token

通过 `secrets` 传递的 Token 可在脚本中作为环境变量访问：

```python
import os

# 从环境变量获取 Token
token = os.environ.get("HF_TOKEN")

# 验证 Token 存在
if not token:
    raise ValueError("环境中未找到 HF_TOKEN！")
```

### 配合 Hugging Face Hub 使用

**选项一：显式 Token 参数**
```python
from huggingface_hub import HfApi

api = HfApi(token=os.environ.get("HF_TOKEN"))
api.upload_file(...)
```

**选项二：自动检测（推荐）**
```python
from huggingface_hub import HfApi

# 自动使用 HF_TOKEN 环境变量
api = HfApi()  # ✅ 更简单，使用环境中的 Token
api.upload_file(...)
```

**选项三：配合 transformers/datasets 使用**
```python
from transformers import AutoModel
from datasets import load_dataset

# 自动从环境变量检测 HF_TOKEN
model = AutoModel.from_pretrained("username/model")
dataset = load_dataset("username/dataset")

# 推送操作时，Token 自动检测
model.push_to_hub("username/new-model")
dataset.push_to_hub("username/new-dataset")
```

### 完整示例

```python
# /// script
# dependencies = ["huggingface-hub", "datasets"]
# ///

import os
from huggingface_hub import HfApi
from datasets import Dataset

# 验证 Token 可用
assert "HF_TOKEN" in os.environ, "Hub 操作需要 HF_TOKEN！"

# 使用 Token 进行 Hub 操作
api = HfApi()  # 自动检测 HF_TOKEN

# 创建并推送数据集
data = {"text": ["Hello", "World"]}
dataset = Dataset.from_dict(data)

# 推送到 Hub（Token 自动检测）
dataset.push_to_hub("username/my-dataset")

print("✅ 数据集推送成功！")
```

## Token 验证

### 本地检查认证状态

```python
from huggingface_hub import whoami

try:
    user_info = whoami()
    print(f"✅ 已登录为：{user_info['name']}")
except Exception as e:
    print(f"❌ 未认证：{e}")
```

### 在任务中验证 Token

```python
import os

# 检查 Token 存在
if "HF_TOKEN" not in os.environ:
    raise ValueError("环境中未找到 HF_TOKEN！")

token = os.environ["HF_TOKEN"]

# 验证 Token 格式（应以 "hf_" 开头）
if not token.startswith("hf_"):
    raise ValueError(f"无效的 Token 格式：{token[:10]}...")

# 测试 Token 可用
from huggingface_hub import whoami
try:
    user_info = whoami(token=token)
    print(f"✅ Token 对用户有效：{user_info['name']}")
except Exception as e:
    raise ValueError(f"Token 验证失败：{e}")
```

## 常见 Token 问题

### 错误：401 Unauthorized

**症状：**
```
401 Client Error: Unauthorized for url: https://huggingface.co/api/...
```

**原因：**
1. 任务中缺少 Token
2. Token 无效或过期
3. Token 未正确传递

**解决方案：**
1. 在任务配置中添加 `secrets={"HF_TOKEN": "$HF_TOKEN"}`
2. 验证本地 `hf_whoami()` 能正常工作
3. 重新登录： `hf auth login`
4. 检查 Token 未过期

**验证：**
```python
# 在您的脚本中
import os
assert "HF_TOKEN" in os.environ, "缺少 HF_TOKEN！"
```

### 错误：403 Forbidden

**症状：**
```
403 Client Error: Forbidden for url: https://huggingface.co/api/...
```

**原因：**
1. Token 缺少所需权限（写操作使用了只读 Token）
2. 无权访问私有仓库
3. 组织权限不足

**解决方案：**
1. 确保 Token 具有写入权限
2. 在 https://huggingface.co/settings/tokens 检查 Token 类型
3. 验证对目标仓库的访问权限
4. 必要时使用组织 Token

**检查 Token 权限：**
```python
from huggingface_hub import whoami

user_info = whoami()
print(f"用户：{user_info['name']}")
print(f"类型：{user_info.get('type', 'user')}")
```

### 错误：环境中未找到 Token

**症状：**
```
KeyError: 'HF_TOKEN'
ValueError: HF_TOKEN not found
```

**原因：**
1. 任务配置中未传递 `secrets`
2. 键名错误（应为 `HF_TOKEN`）
3. 使用了 `env` 而非 `secrets`

**解决方案：**
1. 使用 `secrets={"HF_TOKEN": "$HF_TOKEN"}`（而非 `env`）
2. 验证键名准确为 `HF_TOKEN`
3. 检查任务配置语法

**正确配置：**
```python
# ✅ 正确
hf_jobs("uv", {
    "script": "...",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})

# ❌ 错误 - 使用了 env 而非 secrets
hf_jobs("uv", {
    "script": "...",
    "env": {"HF_TOKEN": "$HF_TOKEN"}  # 安全性较低
})

# ❌ 错误 - 键名错误
hf_jobs("uv", {
    "script": "...",
    "secrets": {"TOKEN": "$HF_TOKEN"}  # 错误的键
})
```

### 错误：仓库访问被拒绝

**症状：**
```
403 Client Error: Forbidden
Repository not found or access denied
```

**原因：**
1. Token 无法访问私有仓库
2. 仓库不存在且无法创建
3. 命名空间错误

**解决方案：**
1. 使用有访问权限的账户的 Token
2. 验证仓库可见性（公开 vs 私有）
3. 检查命名空间是否与 Token 所有者匹配
4. 必要时先创建仓库

**检查仓库访问：**
```python
from huggingface_hub import HfApi

api = HfApi()
try:
    repo_info = api.repo_info("username/repo-name")
    print(f"✅ 访问已授权：{repo_info.id}")
except Exception as e:
    print(f"❌ 访问被拒绝：{e}")
```

## Token 安全最佳实践

### 1. 永不提交 Token

**❌ 不良：**
```python
# 永远不要这样做！
token = "hf_abc123xyz..."
api = HfApi(token=token)
```

**✅ 良好：**
```python
# 使用环境变量
token = os.environ.get("HF_TOKEN")
api = HfApi(token=token)
```

### 2. 使用 Secrets 而非环境变量

**❌ 不良：**
```python
hf_jobs("uv", {
    "script": "...",
    "env": {"HF_TOKEN": "$HF_TOKEN"}  # 在日志中可见
})
```

**✅ 良好：**
```python
hf_jobs("uv", {
    "script": "...",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # 服务端加密
})
```

### 3. 使用自动 Token 替换

**❌ 不良：**
```python
hf_jobs("uv", {
    "script": "...",
    "secrets": {"HF_TOKEN": "hf_abc123..."}  # 硬编码
})
```

**✅ 良好：**
```python
hf_jobs("uv", {
    "script": "...",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # 自动
})
```

### 4. 定期轮换 Token

- 周期性生成新 Token
- 撤销旧 Token
- 更新任务配置
- 监控 Token 使用

### 5. 使用最小权限

- 仅创建所需权限的 Token
- 不需要写入时使用读取 Token
- 常规任务不要使用管理员 Token

### 6. 不共享 Token

- 每个用户应使用自己的 Token
- 不要将 Token 提交到仓库
- 不要在日志或消息中共享 Token

### 7. 监控 Token 使用

- 在 Hub 设置中检查 Token 活动
- 审查任务日志中的 Token 问题
- 设置未授权访问告警

## Token 工作流示例

### 示例一：推送模型到 Hub

```python
hf_jobs("uv", {
    "script": """
# /// script
# dependencies = ["transformers"]
# ///

import os
from transformers import AutoModel, AutoTokenizer

# 验证 Token
assert "HF_TOKEN" in os.environ, "需要 HF_TOKEN！"

# 加载并处理模型
model = AutoModel.from_pretrained("base-model")
# ... 处理模型 ...

# 推送到 Hub（Token 自动检测）
model.push_to_hub("username/my-model")
print("✅ 模型已推送！")
""",
    "flavor": "a10g-large",
    "timeout": "2h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # ✅ 已提供 Token
})
```

### 示例二：访问私有数据集

```python
hf_jobs("uv", {
    "script": """
# /// script
# dependencies = ["datasets"]
# ///

import os
from datasets import load_dataset

# 验证 Token
assert "HF_TOKEN" in os.environ, "需要 HF_TOKEN！"

# 加载私有数据集（Token 自动检测）
dataset = load_dataset("private-org/private-dataset")
print(f"✅ 已加载 {len(dataset)} 个样本")
""",
    "flavor": "cpu-basic",
    "timeout": "30m",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # ✅ 已提供 Token
})
```

### 示例三：创建并推送数据集

```python
hf_jobs("uv", {
    "script": """
# /// script
# dependencies = ["datasets", "huggingface-hub"]
# ///

import os
from datasets import Dataset
from huggingface_hub import HfApi

# 验证 Token
assert "HF_TOKEN" in os.environ, "需要 HF_TOKEN！"

# 创建数据集
data = {"text": ["Sample 1", "Sample 2"]}
dataset = Dataset.from_dict(data)

# 推送到 Hub
api = HfApi()  # 自动检测 HF_TOKEN
dataset.push_to_hub("username/my-dataset")
print("✅ 数据集已推送！")
""",
    "flavor": "cpu-basic",
    "timeout": "30m",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # ✅ 已提供 Token
})
```

## 快速参考

### Token 检查清单

在提交使用 Hub 的任务前：

- [ ] 任务包含 `secrets={"HF_TOKEN": "$HF_TOKEN"}`
- [ ] 脚本检查 Token： `assert "HF_TOKEN" in os.environ`
- [ ] Token 具有所需权限（读取/写入）
- [ ] 用户已登录： `hf_whoami()` 能正常工作
- [ ] Token 未在脚本中硬编码
- [ ] Token 使用 `secrets` 而非 `env`

### 常见模式

**模式一：自动检测 Token**
```python
from huggingface_hub import HfApi
api = HfApi()  # 使用环境中的 HF_TOKEN
```

**模式二：显式 Token**
```python
import os
from huggingface_hub import HfApi
api = HfApi(token=os.environ.get("HF_TOKEN"))
```

**模式三：验证 Token**
```python
import os
assert "HF_TOKEN" in os.environ, "需要 HF_TOKEN！"
```

## 关键要点

1. **始终使用 `secrets={"HF_TOKEN": "$HF_TOKEN"}`** 进行 Hub 操作
2. **永不硬编码 Token** 在脚本或任务配置中
3. **验证 Token 存在** 在 Hub 操作前的脚本中
4. **使用自动检测** 当可能时（`HfApi()` 不带 Token 参数）
5. **检查权限** - 确保 Token 具有所需访问权限
6. **监控 Token 使用** - 定期审查活动
7. **轮换 Token** - 周期性生成新 Token
