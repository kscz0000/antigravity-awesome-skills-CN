# 将结果保存到 Hugging Face Hub

**⚠️ 关键：** 任务环境是临时的。除非将结果持久化到 Hub 或外部存储，否则任务完成后所有结果都会丢失。

## 为什么需要持久化

在 Hugging Face Jobs 上运行时：
- 环境是临时的
- 任务完成后所有文件被删除
- 无本地磁盘持久化
- 任务结束后无法访问结果

**不进行持久化，所有工作将永久丢失。**

## 持久化选项

### 选项一：推送到 Hugging Face Hub（推荐）

**模型：**
```python
from transformers import AutoModel
model.push_to_hub("username/model-name", token=os.environ.get("HF_TOKEN"))
```

**数据集：**
```python
from datasets import Dataset
dataset.push_to_hub("username/dataset-name", token=os.environ.get("HF_TOKEN"))
```

**文件/产物：**
```python
from huggingface_hub import HfApi
api = HfApi(token=os.environ.get("HF_TOKEN"))
api.upload_file(
    path_or_fileobj="results.json",
    path_in_repo="results.json",
    repo_id="username/results",
    repo_type="dataset"
)
```

### 选项二：外部存储

**S3：**
```python
import boto3
s3 = boto3.client('s3')
s3.upload_file('results.json', 'my-bucket', 'results.json')
```

**Google Cloud Storage：**
```python
from google.cloud import storage
client = storage.Client()
bucket = client.bucket('my-bucket')
blob = bucket.blob('results.json')
blob.upload_from_filename('results.json')
```

### 选项三：API 端点

```python
import requests
requests.post("https://your-api.com/results", json=results)
```

## Hub 推送所需配置

### 任务配置

**始终包含 HF_TOKEN：**
```python
hf_jobs("uv", {
    "script": "your_script.py",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # ✅ Hub 操作必需
})
```

### 脚本配置

**验证 Token 存在：**
```python
import os
assert "HF_TOKEN" in os.environ, "Hub 操作需要 HF_TOKEN！"
```

**使用 Token 进行 Hub 操作：**
```python
from huggingface_hub import HfApi

# 自动从环境变量检测 HF_TOKEN
api = HfApi()

# 或显式传入 Token
api = HfApi(token=os.environ.get("HF_TOKEN"))
```

## 完整示例

### 示例一：推送数据集

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

# 处理数据
data = {"text": ["Sample 1", "Sample 2"]}
dataset = Dataset.from_dict(data)

# 推送到 Hub
dataset.push_to_hub("username/my-dataset")
print("✅ 数据集已推送！")
""",
    "flavor": "cpu-basic",
    "timeout": "30m",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

### 示例二：推送模型

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
tokenizer = AutoTokenizer.from_pretrained("base-model")
# ... 处理模型 ...

# 推送到 Hub
model.push_to_hub("username/my-model")
tokenizer.push_to_hub("username/my-model")
print("✅ 模型已推送！")
""",
    "flavor": "a10g-large",
    "timeout": "2h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

### 示例三：推送产物

```python
hf_jobs("uv", {
    "script": """
# /// script
# dependencies = ["huggingface-hub", "pandas"]
# ///

import os
import json
import pandas as pd
from huggingface_hub import HfApi

# 验证 Token
assert "HF_TOKEN" in os.environ, "需要 HF_TOKEN！"

# 生成结果
results = {"accuracy": 0.95, "loss": 0.05}
df = pd.DataFrame([results])

# 保存文件
with open("results.json", "w") as f:
    json.dump(results, f)
df.to_csv("results.csv", index=False)

# 推送到 Hub
api = HfApi()
api.upload_file("results.json", "results.json", "username/results", repo_type="dataset")
api.upload_file("results.csv", "results.csv", "username/results", repo_type="dataset")
print("✅ 结果已推送！")
""",
    "flavor": "cpu-basic",
    "timeout": "30m",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

## 认证方法

### 方法一：自动 Token（推荐）

```python
"secrets": {"HF_TOKEN": "$HF_TOKEN"}
```

自动使用您已登录的 Hugging Face Token。

### 方法二：显式 Token

```python
"secrets": {"HF_TOKEN": "hf_abc123..."}
```

显式提供 Token（出于安全考虑不推荐）。

### 方法三：环境变量

```python
"env": {"HF_TOKEN": "hf_abc123..."}
```

作为常规环境变量传递（安全性低于 secrets）。

**出于安全性和便利性考虑，始终优先使用方法一。**

## 验证检查清单

在提交任何保存到 Hub 的任务前，验证：

- [ ] 任务配置中包含 `secrets={"HF_TOKEN": "$HF_TOKEN"}`
- [ ] 脚本检查 Token： `assert "HF_TOKEN" in os.environ`
- [ ] 脚本中包含 Hub 推送代码
- [ ] 仓库名称不与现有仓库冲突
- [ ] 您对目标命名空间有写入权限

## 仓库设置

### 自动创建

如果仓库不存在，首次推送时会自动创建（前提是 Token 具有写入权限）。

### 手动创建

在推送前创建仓库：

```python
from huggingface_hub import HfApi

api = HfApi()
api.create_repo(
    repo_id="username/repo-name",
    repo_type="model",  # 或 "dataset"
    private=False,  # 或 True 表示私有仓库
)
```

### 仓库命名

**合法名称：**
- `username/my-model`
- `username/model-name`
- `organization/model-name`

**非法名称：**
- `model-name`（缺少用户名）
- `username/model name`（不允许空格）
- `username/MODEL`（不推荐大写）

## 故障排除

### 错误：401 Unauthorized

**原因：** HF_TOKEN 未提供或无效

**解决方案：**
1. 验证任务配置中包含 `secrets={"HF_TOKEN": "$HF_TOKEN"}`
2. 检查是否已登录： `hf_whoami()`
3. 重新登录： `hf auth login`

### 错误：403 Forbidden

**原因：** 对仓库没有写入权限

**解决方案：**
1. 检查仓库命名空间是否与您的用户名匹配
2. 验证您是组织成员（如果使用组织命名空间）
3. 检查 Token 具有写入权限

### 错误：仓库未找到

**原因：** 仓库不存在且自动创建失败

**解决方案：**
1. 手动先创建仓库
2. 检查仓库名称格式
3. 验证命名空间存在

### 错误：推送失败

**原因：** 网络问题或 Hub 不可用

**解决方案：**
1. 检查日志中的具体错误
2. 验证 Token 有效
3. 重试推送操作

## 最佳实践

1. **始终验证 Token 存在** 在 Hub 操作前
2. **使用描述性仓库名称**（如 `my-experiment-results` 而非 `results`）
3. **增量推送** 大型结果（使用检查点）
4. **验证推送成功** 在任务完成前查看日志
5. **使用合适的仓库类型**（model vs dataset）
6. **添加 README** 描述结果
7. **为仓库打标签** 标记相关标签

## 监控推送进度

通过日志检查推送进度：

**MCP 工具：**
```python
hf_jobs("logs", {"job_id": "your-job-id"})
```

**CLI：**
```bash
hf jobs logs <job-id>
```

**Python API：**
```python
from huggingface_hub import fetch_job_logs
for log in fetch_job_logs(job_id="your-job-id"):
    print(log)
```

**查找：**
```
Pushing to username/repo-name...
Upload file results.json: 100%
✅ Push successful
```

## 关键要点

**没有 `secrets={"HF_TOKEN": "$HF_TOKEN"}` 和持久化代码，所有结果将永久丢失。**

在提交任何产生结果的任务前，始终验证两者都已配置。
