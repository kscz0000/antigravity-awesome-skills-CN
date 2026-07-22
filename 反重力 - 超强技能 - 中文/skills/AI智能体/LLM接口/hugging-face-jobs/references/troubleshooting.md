# 故障排除指南

Hugging Face Jobs 的常见问题与解决方案。

## 认证问题

### 错误：401 Unauthorized

**症状：**
```
401 Client Error: Unauthorized for url: https://huggingface.co/api/...
```

**原因：**
- 任务中缺少 Token
- Token 无效或过期
- Token 未正确传递

**解决方案：**
1. 将 Token 添加到 secrets：`hf_jobs` MCP 使用 `"$HF_TOKEN"`（自动替换）；`HfApi().run_uv_job()` **必须**使用 `huggingface_hub` 中的 `get_token()`（字面字符串 `"$HF_TOKEN"` 在 Python API 中**不**可用）
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
- Token 缺少所需权限
- 无权访问私有仓库
- 组织权限不足

**解决方案：**
1. 确保 Token 具有写入权限
2. 在 https://huggingface.co/settings/tokens 检查 Token 类型
3. 验证对目标仓库的访问权限
4. 必要时使用组织 Token

### 错误：环境中未找到 Token

**症状：**
```
KeyError: 'HF_TOKEN'
ValueError: HF_TOKEN not found
```

**原因：**
- 任务配置中未传递 `secrets`
- 键名错误（应为 `HF_TOKEN`）
- 使用了 `env` 而非 `secrets`

**解决方案：**
1. 使用 `secrets`（而非 `env`）—— `hf_jobs` MCP 使用 `"$HF_TOKEN"`；`HfApi().run_uv_job()` 使用 `get_token()`
2. 验证键名准确为 `HF_TOKEN`
3. 检查任务配置语法

## 任务执行问题

### 错误：任务超时

**症状：**
- 任务意外停止
- 状态显示 "TIMEOUT"
- 仅部分结果

**原因：**
- 超过默认 30 分钟超时
- 任务耗时超出预期
- 未指定超时

**解决方案：**
1. 检查日志了解实际运行时间
2. 增加超时并添加缓冲： `"timeout": "3h"`
3. 优化代码加快执行
4. 分块处理数据
5. 在预估时间上添加 20-30% 缓冲

**MCP 工具示例：**
```python
hf_jobs("uv", {
    "script": "...",
    "timeout": "2h"  # 设置合适的超时
})
```

**Python API 示例：**
```python
from huggingface_hub import run_uv_job, inspect_job, fetch_job_logs

job = run_uv_job("script.py", timeout="4h")

# 检查任务是否失败
job_info = inspect_job(job_id=job.id)
if job_info.status.stage == "ERROR":
    print(f"任务失败：{job_info.status.message}")
    # 检查日志获取详情
    for log in fetch_job_logs(job_id=job.id):
        print(log)
```

### 错误：内存不足（OOM）

**症状：**
```
RuntimeError: CUDA out of memory
MemoryError: Unable to allocate array
```

**原因：**
- 批处理大小过大
- 模型超出硬件容量
- GPU 内存不足

**解决方案：**
1. 减小批处理大小
2. 分更小的块处理数据
3. 升级硬件： cpu → t4 → a10g → a100
4. 使用更小的模型或量化
5. 启用梯度检查点（用于训练）

**示例：**
```python
# 减小批处理大小
batch_size = 1

# 分块处理
for chunk in chunks:
    process(chunk)
```

### 错误：缺少依赖

**症状：**
```
ModuleNotFoundError: No module named 'package_name'
ImportError: cannot import name 'X'
```

**原因：**
- 包不在依赖中
- 包名错误
- 版本不匹配

**解决方案：**
1. 添加到 PEP 723 头部：
   ```python
   # /// script
   # dependencies = ["package-name>=1.0.0"]
   # ///
   ```
2. 检查包名拼写
3. 必要时指定版本
4. 检查包可用性

### 错误：脚本未找到

**症状：**
```
FileNotFoundError: script.py not found
```

**原因：**
- 使用了本地文件路径（不支持）
- URL 错误
- 脚本无法访问

**解决方案：**
1. 使用内联脚本（推荐）
2. 使用可公开访问的 URL
3. 先将脚本上传到 Hub
4. 检查 URL 是否正确

**正确做法：**
```python
# ✅ 内联代码
hf_jobs("uv", {"script": "# /// script\n# dependencies = [...]\n# ///\n\n<code>"})

# ✅ 从 URL
hf_jobs("uv", {"script": "https://huggingface.co/user/repo/resolve/main/script.py"})
```

## Hub 推送问题

### 错误：推送失败

**症状：**
```
Error pushing to Hub
Upload failed
```

**原因：**
- 网络问题
- Token 缺失或无效
- 仓库访问被拒绝
- 文件过大

**解决方案：**
1. 检查 Token： `assert "HF_TOKEN" in os.environ`
2. 验证仓库存在或可创建
3. 在日志中检查网络连接
4. 重试推送操作
5. 将大文件拆分为多个块

### 错误：仓库未找到

**症状：**
```
404 Client Error: Not Found
Repository not found
```

**原因：**
- 仓库不存在
- 仓库名称错误
- 无权访问私有仓库

**解决方案：**
1. 先创建仓库：
   ```python
   from huggingface_hub import HfApi
   api = HfApi()
   api.create_repo("username/repo-name", repo_type="dataset")
   ```
2. 检查仓库名称格式
3. 验证命名空间存在
4. 检查仓库可见性

### 错误：结果未保存

**症状：**
- 任务成功完成
- Hub 上看不到结果
- 文件未持久化

**原因：**
- 脚本中没有持久化代码
- 推送代码未执行
- 推送静默失败

**解决方案：**
1. 在脚本中添加持久化代码
2. 验证推送成功执行
3. 检查日志中的推送错误
4. 在推送周围添加错误处理

**示例：**
```python
try:
    dataset.push_to_hub("username/dataset")
    print("✅ 推送成功")
except Exception as e:
    print(f"❌ 推送失败：{e}")
    raise
```

## 硬件问题

### 错误：GPU 不可用

**症状：**
```
CUDA not available
No GPU found
```

**原因：**
- 使用了 CPU 规格而非 GPU
- 未请求 GPU
- 镜像中未安装 CUDA

**解决方案：**
1. 使用 GPU 规格： `"flavor": "a10g-large"`
2. 检查镜像支持 CUDA
3. 在日志中验证 GPU 可用性

### 错误：性能缓慢

**症状：**
- 任务耗时超出预期
- GPU 利用率低
- CPU 瓶颈

**原因：**
- 硬件选择错误
- 代码效率低
- 数据加载瓶颈

**解决方案：**
1. 升级硬件
2. 优化代码
3. 使用批处理
4. 分析代码以找出瓶颈

## 常规问题

### 错误：任务状态未知

**症状：**
- 无法检查任务状态
- 状态 API 返回错误

**解决方案：**
1. 使用任务 URL： `https://huggingface.co/jobs/username/job-id`
2. 查看日志： `hf_jobs("logs", {"job_id": "..."})`
3. 检查任务： `hf_jobs("inspect", {"job_id": "..."})`

### 错误：日志不可用

**症状：**
- 看不到日志
- 日志延迟

**原因：**
- 任务刚启动（日志延迟 30-60 秒）
- 任务在记录前失败
- 日志尚未生成

**解决方案：**
1. 任务启动后等待 30-60 秒
2. 先检查任务状态
3. 使用任务 URL 访问网页界面

### 错误：成本意外过高

**症状：**
- 任务成本超出预期
- 运行时间长于估计

**原因：**
- 任务运行时间超过超时
- 硬件选择错误
- 代码效率低

**解决方案：**
1. 监控任务运行时间
2. 设置合适的超时
3. 优化代码
4. 选择合适的硬件
5. 运行前检查成本估算

## 调试技巧

### 1. 添加日志

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("开始处理...")
logger.info(f"已处理 {count} 项")
```

### 2. 验证环境

```python
import os
print(f"Python 版本：{os.sys.version}")
print(f"CUDA 可用：{torch.cuda.is_available()}")
print(f"HF_TOKEN 存在：{'HF_TOKEN' in os.environ}")
```

### 3. 先在本地测试

在提交前先在本地运行脚本以尽早捕获错误：
```bash
python script.py
# 或使用 uv
uv run script.py
```

### 4. 检查任务日志

**MCP 工具：**
```python
# 查看日志
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

**或使用任务 URL：** `https://huggingface.co/jobs/username/job-id`

### 5. 添加错误处理

```python
try:
    # 您的代码
    process_data()
except Exception as e:
    print(f"错误：{e}")
    import traceback
    traceback.print_exc()
    raise
```

### 6. 以编程方式检查任务状态

```python
from huggingface_hub import inspect_job, fetch_job_logs

job_info = inspect_job(job_id="your-job-id")
print(f"状态：{job_info.status.stage}")
print(f"消息：{job_info.status.message}")

if job_info.status.stage == "ERROR":
    print("任务失败！日志：")
    for log in fetch_job_logs(job_id="your-job-id"):
        print(log)
```

## 快速参考

### 常见错误代码

| 代码 | 含义 | 解决方案 |
|------|---------|----------|
| 401 | Unauthorized | 将 Token 添加到 secrets：MCP 使用 `"$HF_TOKEN"`，Python API 使用 `get_token()` |
| 403 | Forbidden | 检查 Token 权限 |
| 404 | Not Found | 验证仓库存在 |
| 500 | Server Error | 重试或联系支持 |

### 提交前检查清单

- [ ] Token 已配置：MCP 使用 `secrets={"HF_TOKEN": "$HF_TOKEN"}`，Python API 使用 `secrets={"HF_TOKEN": get_token()}`
- [ ] 脚本检查 Token： `assert "HF_TOKEN" in os.environ`
- [ ] 超时设置合适
- [ ] 硬件选择正确
- [ ] 依赖在 PEP 723 头部列出
- [ ] 包含持久化代码
- [ ] 添加了错误处理
- [ ] 添加了日志用于调试

## 获取帮助

如果问题持续存在：

1. **查看日志** - 大多数错误包含详细消息
2. **查阅文档** - 参见主 SKILL.md
3. **检查 Hub 状态** - https://status.huggingface.co
4. **社区论坛** - https://discuss.huggingface.co
5. **GitHub issues** - 用于 huggingface_hub 中的 bug

## 关键要点

1. **始终包含 Token** - MCP： `secrets={"HF_TOKEN": "$HF_TOKEN"}`，Python API： `secrets={"HF_TOKEN": get_token()}`
2. **设置合适的超时** - 默认 30 分钟可能不足
3. **验证持久化** - 没有代码结果不会持久化
4. **查看日志** - 大多数问题在任务日志中可见
5. **本地测试** - 在提交前捕获错误
6. **添加错误处理** - 更好的调试信息
7. **监控成本** - 设置超时以避免意外费用
