# ComfyUI Gateway — 故障排查指南

ComfyUI Gateway 问题诊断和解决的综合参考。每个章节遵循**症状 → 原因 → 解决方案**格式，附带可立即执行的具体命令。

---

## 目录

1. [ComfyUI 不可达](#1-comfyui-不可达)
2. [OOM（内存不足）错误](#2-oom内存不足错误)
3. [生成缓慢](#3-生成缓慢)
4. [Webhook 失败](#4-webhook-失败)
5. [Redis 连接问题](#5-redis-连接问题)
6. [存储错误](#6-存储错误)
7. [数据库问题](#7-数据库问题)
8. [任务卡在"running"状态](#8-任务卡在running状态)
9. [限流问题](#9-限流问题)
10. [认证问题](#10-认证问题)

---

## 1. ComfyUI 不可达

网关返回 `COMFYUI_UNREACHABLE`，`/health` 端点显示 `comfyui.reachable: false`。

### 1a. COMFYUI_URL 配置错误

**症状**：网关启动正常但每个任务都失败，返回 `COMFYUI_UNREACHABLE`。健康端点返回 `{ ok: false, comfyui: { reachable: false } }`。

**原因**：`.env` 中的 `COMFYUI_URL` 未指向运行中的 ComfyUI 实例。

**解决方案**：

```bash
# 1. 检查当前配置
grep COMFYUI_URL .env

# 2. 从网关主机测试连通性
curl -s http://127.0.0.1:8188/
# 预期：ComfyUI 的 HTML 页面或 JSON

# 3. 如果 ComfyUI 在不同端口或主机，更新 .env
# 示例：COMFYUI_URL=http://192.168.1.50:8188

# 4. 修改 .env 后重启网关
npm run dev
```

### 1b. 防火墙阻止端口

**症状**：`curl` 到 ComfyUI URL 超时或返回 `Connection refused`，但 ComfyUI 确认在该机器上运行。

**原因**：主机防火墙（Windows Defender、iptables、ufw）阻止了端口。

**解决方案**：

```bash
# Linux (ufw)
sudo ufw allow 8188/tcp
sudo ufw reload

# Linux (iptables)
sudo iptables -A INPUT -p tcp --dport 8188 -j ACCEPT

# Windows (PowerShell，以管理员身份运行)
New-NetFirewallRule -DisplayName "ComfyUI" -Direction Inbound -Port 8188 -Protocol TCP -Action Allow

# 验证端口正在监听
# Linux
ss -tlnp | grep 8188
# Windows
netstat -an | findstr 8188
```

### 1c. Docker 网络

**症状**：Docker 内运行的网关无法连接 `127.0.0.1:8188` 上的 ComfyUI。

**原因**：Docker 容器内的 `127.0.0.1` 指向容器本身，而非主机。

**解决方案**：

```bash
# 方案 A：使用 Docker 的特殊主机 DNS（Linux + Docker Desktop）
COMFYUI_URL=http://host.docker.internal:8188

# 方案 B：使用 host 网络模式
docker run --network host comfyui-gateway

# 方案 C：将两个容器放在同一 Docker 网络
docker network create comfy-net
docker run --name comfyui --network comfy-net ...
docker run --name gateway --network comfy-net -e COMFYUI_URL=http://comfyui:8188 ...

# 从网关容器内验证
docker exec -it gateway sh -c "wget -qO- http://comfyui:8188/ || echo FAIL"
```

### 1d. WSL2 网络

**症状**：Windows/WSL2 上运行的网关无法连接另一侧的 ComfyUI（主机 vs WSL）。

**原因**：WSL2 使用虚拟网络适配器。WSL2 客户机和 Windows 主机有不同的 IP 地址。

**解决方案**：

```bash
# 从 WSL2 获取 Windows 主机 IP
cat /etc/resolv.conf | grep nameserver | awk '{print $2}'
# 示例输出：172.25.192.1

# 设置 COMFYUI_URL 为该 IP
COMFYUI_URL=http://172.25.192.1:8188

# 或者，如果 ComfyUI 在 WSL2 内运行而网关在 Windows 上：
# 查找 WSL2 IP
wsl hostname -I
# 示例输出：172.25.198.5
# 设置：COMFYUI_URL=http://172.25.198.5:8188

# 确保 ComfyUI 监听 0.0.0.0，而非仅 127.0.0.1
# 启动 ComfyUI 时使用：python main.py --listen 0.0.0.0
```

### 1e. ComfyUI 未启动或崩溃

**症状**：端口完全没有监听。

**原因**：ComfyUI 进程未运行。

**解决方案**：

```bash
# 检查进程是否运行
# Linux
ps aux | grep "main.py"
# Windows
tasklist | findstr python

# 启动 ComfyUI
cd /path/to/ComfyUI
python main.py --listen 0.0.0.0 --port 8188

# 检查启动错误日志
python main.py --listen 0.0.0.0 --port 8188 2>&1 | tail -50

# 验证正在接受连接
curl -s http://127.0.0.1:8188/ && echo "OK" || echo "NOT REACHABLE"
```

---

## 2. OOM（内存不足）错误

网关将这些分类为 `COMFYUI_OOM`，`retryable: false`。

### 2a. 分辨率或批次大小过大

**症状**：任务失败，错误包含 "CUDA out of memory"、"allocator backend out of memory" 或 "failed to allocate"。

**原因**：请求的图片尺寸或批次大小超过可用显存。

**解决方案**：

```bash
# 1. 在任务请求中降低分辨率
# 不要用 2048x2048，尝试 1024x1024 或 768x768
curl -X POST http://localhost:3000/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{
    "workflowId": "sdxl_realism_v1",
    "inputs": {
      "prompt": "a mountain landscape",
      "width": 1024,
      "height": 1024
    }
  }'

# 2. 将批次大小降为 1
# 在任务输入中设置："batch_size": 1

# 3. 在 .env 中降低网关级别限制
MAX_IMAGE_SIZE=1024
MAX_BATCH_SIZE=2
```

### 2b. 步数过多

**症状**：OOM 发生在生成中途，而非提交时。

**原因**：采样器在许多步骤中累积中间张量。

**解决方案**：

```bash
# 在任务输入中减少步数
# 不要用 50 步，尝试 20-30 步
curl -X POST http://localhost:3000/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{
    "workflowId": "sdxl_realism_v1",
    "inputs": {
      "prompt": "a portrait photo",
      "steps": 20,
      "width": 1024,
      "height": 1024
    }
  }'
```

### 2c. 模型量化

**症状**：即使低分辨率也出现 OOM 错误，因为模型对 GPU 来说太大（8GB 显卡使用 SDXL 常见）。

**原因**：全精度（fp32）或半精度（fp16）模型权重超过可用显存。

**解决方案**：

```bash
# 在 ComfyUI 中使用 fp8 或量化检查点
# 更新工作流模板使用量化模型：
# 例如，"ckpt_name": "sdxl_base_1.0_fp8.safetensors"

# 或在启动 ComfyUI 时添加 --fp8_e4m3fn-unet 标志
python main.py --listen 0.0.0.0 --fp8_e4m3fn-unet

# 监控显存使用
nvidia-smi -l 2
```

### 2d. VAE 分块

**症状**：OOM 发生在 VAE 解码步骤（采样完成后）。

**原因**：VAE 解码器一次处理整个潜空间，高分辨率时非常消耗内存。

**解决方案**：

```
在 ComfyUI 工作流中启用 VAE 分块，添加 "VAEDecodeTiled" 节点
而非 "VAEDecode"。分块大小 512 是不错的默认值。

在工作流 JSON 模板中：
{
  "10": {
    "class_type": "VAEDecodeTiled",
    "inputs": {
      "samples": ["3", 0],
      "vae": ["4", 2],
      "tile_size": 512
    }
  }
}
```

---

## 3. 生成缓慢

### 3a. GPU 未被利用

**症状**：任务完成但耗时远超预期。GPU 利用率接近 0%。

**原因**：ComfyUI 回退到 CPU 推理，或选择了错误的 GPU。

**解决方案**：

```bash
# 1. 在任务期间检查 GPU 利用率
nvidia-smi -l 1
# 查看 "GPU-Util" 列——采样期间应为 80-100%

# 2. 验证 ComfyUI 中 CUDA 可用
# 检查 ComfyUI 启动日志中的 "Using device: cuda"

# 3. 强制 GPU 选择（多 GPU 系统）
CUDA_VISIBLE_DEVICES=0 python main.py --listen 0.0.0.0

# 4. 验证 PyTorch 能看到 GPU
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

### 3b. 每次任务都加载模型

**症状**：第一个任务慢，相同工作流的后续任务更快，但切换工作流会导致长延迟。

**原因**：ComfyUI 每次请求不同检查点时从磁盘加载模型。每次模型加载可能需要 10-30 秒。

**解决方案**：

```bash
# 1. 增加 ComfyUI 的模型缓存
# 启动 ComfyUI 时使用更大的缓存（默认为 1 个模型）：
python main.py --listen 0.0.0.0 --cache-size 3

# 2. 尽可能在工作流间使用相同检查点
# 标准化一个检查点（如 sdxl_base_1.0.safetensors）

# 3. 将模型放在 SSD 而非 HDD 上
# 将 ComfyUI/models/ 移动到 NVMe 驱动器以加快加载速度
```

### 3c. 队列深度/并发

**症状**：任务排队很长时间才开始。任务在 `status: "queued"` 状态停留数分钟。

**原因**：Worker 并发设置为 1（默认），多个任务排队，或单个槽位被长任务占用。

**解决方案**：

```bash
# 1. 检查当前队列状态
curl -s http://localhost:3000/jobs?status=queued | jq '.count'
curl -s http://localhost:3000/jobs?status=running | jq '.count'

# 2. 如果 GPU 能处理，增加并发（多批次）
# 编辑 .env：
MAX_CONCURRENCY=2

# 警告：仅在显存足够并行任务时增加。
# 两个并发的 1024x1024 SDXL 任务需要约 20+ GB 显存。

# 3. 对于多 GPU 设置，运行多个 Worker 进程
# 终端 1：CUDA_VISIBLE_DEVICES=0 npm run start:worker
# 终端 2：CUDA_VISIBLE_DEVICES=1 npm run start:worker
# 两者连接到同一 Redis 队列
```

### 3d. ComfyUI 启动时间

**症状**：ComfyUI 启动后的第一个任务即使简单生成也需要 30-60 秒。

**原因**：ComfyUI 在第一个提示时执行初始化（加载节点、编译、CUDA 预热）。

**解决方案**：

```bash
# 1. ComfyUI 启动后立即发送预热任务
# 这是一个微小的 64x64 生成，强制初始化
curl -X POST http://localhost:3000/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{
    "workflowId": "sdxl_realism_v1",
    "inputs": {
      "prompt": "test",
      "width": 64,
      "height": 64,
      "steps": 1
    }
  }'

# 2. 增加网关超时以应对冷启动
COMFYUI_TIMEOUT_MS=600000
```

---

## 4. Webhook 失败

Webhook 错误在日志中显示为 `WEBHOOK_DELIVERY_FAILED`。

### 4a. DNS 解析失败

**症状**：Webhook 失败，显示 "getaddrinfo ENOTFOUND" 或 "DNS lookup failed"。

**原因**：回调 URL 主机名无法解析。

**解决方案**：

```bash
# 1. 从网关主机测试 DNS 解析
nslookup your-webhook-domain.com
dig your-webhook-domain.com

# 2. 如果使用本地主机名（如 Docker 内），确保可解析
# 如需要，添加到 /etc/hosts：
echo "192.168.1.50 my-webhook-server" | sudo tee -a /etc/hosts

# 3. 验证任务请求中的回调 URL 正确
curl -X POST http://localhost:3000/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{
    "workflowId": "sdxl_realism_v1",
    "inputs": { "prompt": "test" },
    "callbackUrl": "https://your-valid-domain.com/webhook"
  }'
```

### 4b. SSL 证书错误

**症状**：Webhook 失败，显示 "self signed certificate"、"CERT_HAS_EXPIRED" 或 "unable to verify the first certificate"。

**原因**：Webhook 接收器使用无效、过期或自签名 SSL 证书。

**解决方案**：

```bash
# 1. 手动测试证书
openssl s_client -connect your-webhook-domain.com:443 -servername your-webhook-domain.com < /dev/null 2>&1 | head -20

# 2. 检查过期时间
echo | openssl s_client -connect your-webhook-domain.com:443 2>/dev/null | openssl x509 -noout -dates

# 3. 对于使用自签名证书的开发环境，设置 NODE_TLS_REJECT_UNAUTHORIZED
# 警告：生产环境不要使用此设置
NODE_TLS_REJECT_UNAUTHORIZED=0 npm run dev

# 4. 对于生产环境，修复证书（使用 Let's Encrypt 或有效 CA）
```

### 4c. Webhook 超时

**症状**：Webhook 日志显示 "AbortError" 或 "Webhook POST timed out"。

**原因**：Webhook 接收器响应时间超过 10 秒。网关有硬编码的 10 秒超时，3 次重试和指数退避。

**解决方案**：

```bash
# 1. 确保 webhook 接收器快速响应
# 接收器应立即返回 200 并异步处理
# 错误：app.post("/webhook", async (req, res) => { await longProcess(); res.send("ok"); })
# 正确：app.post("/webhook", (req, res) => { res.send("ok"); enqueueWork(req.body); })

# 2. 测试接收器响应时间
time curl -s -o /dev/null -w "%{time_total}" -X POST https://your-webhook.com/callback \
  -H "Content-Type: application/json" -d '{"test": true}'
# 应小于 2 秒
```

### 4d. 域名不在白名单

**症状**：任务创建失败，显示 `Callback domain "example.com" is not in the allowed domains list`。

**原因**：配置了 `WEBHOOK_ALLOWED_DOMAINS` 但不包含回调 URL 的域名。

**解决方案**：

```bash
# 1. 检查当前设置
grep WEBHOOK_ALLOWED_DOMAINS .env

# 2. 添加域名（逗号分隔列表）
WEBHOOK_ALLOWED_DOMAINS=your-app.com,n8n.your-domain.com,*.internal.company.com

# 3. 或允许所有域名（安全性较低，适合开发环境）
WEBHOOK_ALLOWED_DOMAINS=*

# 4. 重启网关
npm run dev
```

### 4e. HMAC 签名不匹配

**症状**：你的 webhook 接收器收到 POST 但 HMAC 验证失败。

**原因**：网关配置的 `WEBHOOK_SECRET` 与接收器验证签名使用的密钥不匹配，或签名计算方式不同。

**解决方案**：

```bash
# 1. 验证两边的 WEBHOOK_SECRET 匹配
grep WEBHOOK_SECRET .env

# 2. 网关发送：X-Signature: sha256=<hex>
# 计算方式：HMAC-SHA256(secret, raw_body_string)
# 在 Node.js 中验证：
node -e "
const crypto = require('crypto');
const secret = 'your-webhook-secret';
const body = '{\"jobId\":\"test\",\"status\":\"succeeded\"}';
const sig = crypto.createHmac('sha256', secret).update(body, 'utf8').digest('hex');
console.log('Expected header: sha256=' + sig);
"

# 3. 常见错误：
# - 计算 HMAC 前解析了 body（必须使用原始字符串）
# - 使用了不同编码（网关使用 utf8）
# - 字符串比较区分大小写（hex 是小写）
```

---

## 5. Redis 连接问题

### 5a. 无法连接 Redis

**症状**：网关启动时崩溃，显示 "Redis connection error" 或指向 Redis 端口的 "ECONNREFUSED"。

**原因**：Redis 服务器未运行，或 `REDIS_URL` 错误。

**解决方案**：

```bash
# 1. 检查 Redis 是否运行
redis-cli ping
# 预期：PONG

# 2. 验证 URL 格式
# 正确格式：
#   redis://localhost:6379
#   redis://:yourpassword@redis-host:6379/0
#   rediss://user:password@host:6380/0  (TLS)

# 3. 测试连通性
redis-cli -u "redis://localhost:6379" ping

# 4. 如果不需要 Redis，删除 REDIS_URL 使用内存队列
# 编辑 .env：
REDIS_URL=
# 网关自动回退到内存队列
```

### 5b. Redis 认证失败

**症状**：错误消息包含 "NOAUTH Authentication required" 或 "ERR invalid password"。

**原因**：Redis 需要密码但 `REDIS_URL` 未包含，或密码错误。

**解决方案**：

```bash
# 1. 在 URL 中包含密码
REDIS_URL=redis://:your_redis_password@localhost:6379/0

# 2. 用 redis-cli 测试
redis-cli -a "your_redis_password" ping

# 3. 检查 Redis 配置中的 requirepass
redis-cli CONFIG GET requirepass
```

### 5c. 回退到内存队列

**症状**：日志显示 "No Redis URL configured, using in-memory queue" 但你期望使用 BullMQ。

**原因**：`.env` 中 `REDIS_URL` 为空或未设置。

**解决方案**：

```bash
# 1. 在 .env 中设置 REDIS_URL
REDIS_URL=redis://localhost:6379

# 2. 验证 Redis 运行
redis-cli ping

# 3. 重启网关
npm run dev

# 4. 在日志中确认：应显示 "Redis URL configured, using BullMQ worker"
```

> **注意**：内存队列适合单实例开发部署。对于需要多 Worker 或持久性的生产环境，使用 Redis + BullMQ。

---

## 6. 存储错误

### 6a. 本地磁盘权限拒绝

**症状**：任务在输出存储步骤失败，显示 "EACCES: permission denied" 或 `STORAGE_READ_ERROR`。

**原因**：网关进程没有 `STORAGE_LOCAL_PATH` 的写入权限。

**解决方案**：

```bash
# 1. 检查配置的路径
grep STORAGE_LOCAL_PATH .env
# 默认：./data/outputs

# 2. 确保目录存在且可写
mkdir -p ./data/outputs
chmod 755 ./data/outputs

# 3. 检查所有权
ls -la ./data/

# 4. 如果以不同用户运行（如 Docker 中）
chown -R node:node ./data/outputs

# 5. 对于 Docker，挂载具有正确权限的卷
# docker run -v /host/path/outputs:/app/data/outputs ...
```

### 6b. S3 凭证无效

**症状**：任务失败，显示 `STORAGE_S3_PUT_ERROR`，底层错误提到 "InvalidAccessKeyId"、"SignatureDoesNotMatch" 或 "AccessDenied"。

**原因**：`S3_ACCESS_KEY` / `S3_SECRET_KEY` 错误、过期，或 IAM 策略未授予 `s3:PutObject` 权限。

**解决方案**：

```bash
# 1. 验证凭证已设置
grep S3_ACCESS_KEY .env
grep S3_SECRET_KEY .env
grep S3_BUCKET .env

# 2. 用 AWS CLI 测试
aws s3 ls s3://your-bucket/ \
  --endpoint-url http://your-minio:9000 \
  --region us-east-1

# 3. 测试 put 操作
echo "test" > /tmp/test.txt
aws s3 cp /tmp/test.txt s3://your-bucket/test.txt \
  --endpoint-url http://your-minio:9000

# 4. 网关最低 IAM 策略：
# {
#   "Version": "2012-10-17",
#   "Statement": [{
#     "Effect": "Allow",
#     "Action": ["s3:PutObject", "s3:GetObject", "s3:DeleteObject", "s3:ListBucket"],
#     "Resource": ["arn:aws:s3:::your-bucket", "arn:aws:s3:::your-bucket/*"]
#   }]
# }
```

### 6c. MinIO 配置

**症状**：S3 存储失败，显示 "socket hang up"、"ECONNREFUSED" 或 "Bucket does not exist"。

**原因**：MinIO 端点错误、存储桶未创建，或 `forcePathStyle` 未启用（网关自动处理）。

**解决方案**：

```bash
# 1. 验证 MinIO 运行
curl http://localhost:9000/minio/health/live
# 预期：HTTP 200

# 2. 在 .env 中设置正确端点
S3_ENDPOINT=http://localhost:9000
S3_BUCKET=comfyui-outputs
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_REGION=us-east-1

# 3. 如果存储桶不存在则创建
# 使用 mc（MinIO Client）
mc alias set local http://localhost:9000 minioadmin minioadmin
mc mb local/comfyui-outputs

# 或使用 AWS CLI
aws s3 mb s3://comfyui-outputs --endpoint-url http://localhost:9000
```

---

## 7. 数据库问题

### 7a. SQLite WAL 锁错误

**症状**：并发负载下间歇性 "SQLITE_BUSY" 或 "database is locked" 错误。

**原因**：多个进程或线程同时写入 SQLite 数据库。SQLite WAL 模式支持并发读取但只能一个写入者。

**解决方案**：

```bash
# 1. 网关已设置最优 pragma：
#    journal_mode = WAL
#    synchronous = NORMAL
#    busy_timeout = 5000 (5 秒)

# 2. 如果运行多个网关实例，切换到 Postgres
DATABASE_URL=postgresql://user:password@localhost:5432/comfyui_gateway

# 3. 如果必须使用 SQLite 单实例，增加 busy timeout
# （需要代码更改或环境覆盖）：
# 默认 5000ms 对大多数单实例用例足够

# 4. 检查卡住的 WAL 文件
ls -la ./data/gateway.db*
# 应看到：gateway.db, gateway.db-wal, gateway.db-shm

# 5. 如果数据库损坏，尝试恢复
sqlite3 ./data/gateway.db "PRAGMA integrity_check;"
# 如果报告错误，备份并重建：
cp ./data/gateway.db ./data/gateway.db.bak
sqlite3 ./data/gateway.db ".recover" | sqlite3 ./data/gateway_recovered.db
```

### 7b. Postgres 连接池

**症状**：错误如 "too many clients already"、"remaining connection slots are reserved"，或间歇性 "Connection terminated unexpectedly"。

**原因**：网关打开过多 Postgres 连接，超过 `max_connections`，或连接未正确归还池。

**解决方案**：

```bash
# 1. 检查 Postgres 当前连接数
psql -c "SELECT count(*) FROM pg_stat_activity WHERE datname = 'comfyui_gateway';"

# 2. 检查 max_connections 设置
psql -c "SHOW max_connections;"

# 3. 使用连接池如 PgBouncer
# 安装 PgBouncer 并将 DATABASE_URL 指向它
DATABASE_URL=postgresql://user:password@localhost:6432/comfyui_gateway

# 4. 如果运行多个网关实例，确保所有实例的池大小总和
# 不超过 Postgres max_connections
```

### 7c. 数据库 URL 格式

**症状**：网关启动时崩溃，显示 "Invalid connection string"，或你想要 Postgres 却使用了 SQLite。

**原因**：`DATABASE_URL` 格式错误。网关检查 URL 是否以 `postgres://` 或 `postgresql://` 开头来选择 Postgres 后端。

**解决方案**：

```bash
# SQLite 格式（都有效）：
DATABASE_URL=./data/gateway.db
DATABASE_URL=/absolute/path/to/gateway.db

# Postgres 格式（必须以 postgres:// 或 postgresql:// 开头）：
DATABASE_URL=postgresql://user:password@localhost:5432/comfyui_gateway
DATABASE_URL=postgres://user:password@host:5432/dbname?sslmode=require
```

---

## 8. 任务卡在"running"状态

### 8a. ComfyUI 执行期间崩溃

**症状**：任务无限期显示 `status: "running"`。无进度更新。网关健康端点可能显示 `comfyui.reachable: false`。

**原因**：ComfyUI 在处理任务时崩溃（段错误、CUDA 错误、被 OOM killer 杀死），网关的 WebSocket 连接断开。

**解决方案**：

```bash
# 1. 检查任务状态
curl -s http://localhost:3000/jobs/<jobId> | jq '.status'

# 2. 检查 ComfyUI 是否仍在运行
curl -s http://localhost:3000/health | jq '.comfyui.reachable'

# 3. 如果 ComfyUI 崩溃，重启它
cd /path/to/ComfyUI
python main.py --listen 0.0.0.0

# 4. 卡住的任务最终会超时（COMFYUI_TIMEOUT_MS，默认 5 分钟）
# 并被标记为失败，错误码 COMFYUI_TIMEOUT

# 5. 立即取消卡住的任务
curl -X POST http://localhost:3000/jobs/<jobId>/cancel \
  -H "X-API-Key: your-key"

# 6. 减少超时以更快检测失败
COMFYUI_TIMEOUT_MS=120000
```

### 8b. WebSocket 断开

**症状**：任务保持"running"但 ComfyUI 实际已完成。输出存在于 ComfyUI 历史中。

**原因**：WebSocket 连接在执行中途断开，轮询回退未能获取结果。

**解决方案**：

```bash
# 1. 直接检查 ComfyUI 历史
curl -s http://127.0.0.1:8188/history | jq 'keys | length'

# 2. 如果 WebSocket 失败，网关自动回退到 HTTP 轮询。
# 如果轮询也失败，任务会超时。

# 3. 重启网关重置连接
npm run dev

# 4. 检查网关和 ComfyUI 之间的网络稳定性
ping -c 10 <comfyui-host>
```

### 8c. 重启恢复

**症状**：重启网关后，之前"running"的任务永久保持该状态。

**原因**：内存队列在进程重启时丢失运行中任务的跟踪。内存队列的任务没有自动恢复机制。

**解决方案**：

```bash
# 1. 对于生产环境，使用 Redis（BullMQ）获得持久任务队列
REDIS_URL=redis://localhost:6379

# 2. 通过数据库手动将卡住的任务标记为失败
sqlite3 ./data/gateway.db \
  "UPDATE jobs SET status='failed', errorJson='{\"code\":\"GATEWAY_RESTART\",\"message\":\"Job interrupted by gateway restart\"}', completedAt=datetime('now') WHERE status='running';"

# 3. 验证
sqlite3 ./data/gateway.db "SELECT id, status FROM jobs WHERE status='running';"
```

---

## 9. 限流问题

### 9a. 确认被限流

**症状**：API 返回 HTTP 429，body 为 `{ "error": "RATE_LIMITED" }`，带 `Retry-After` 头。

**原因**：你在 `RATE_LIMIT_WINDOW_MS` 窗口内超过了 `RATE_LIMIT_MAX` 请求数。限制按 API key 或 IP 应用。

**解决方案**：

```bash
# 1. 检查响应头
curl -v http://localhost:3000/health -H "X-API-Key: your-key" 2>&1 | grep -i "x-ratelimit"
# X-RateLimit-Limit: 100
# X-RateLimit-Remaining: 0
# Retry-After: 42

# 2. 等待 Retry-After 时间后重试

# 3. 在客户端实现指数退避
```

### 9b. 调整限流设置

**症状**：合法使用被限流。

**原因**：默认限制（100 请求/分钟）对你的工作负载来说太低。

**解决方案**：

```bash
# 1. 在 .env 中增加限制
RATE_LIMIT_MAX=500
RATE_LIMIT_WINDOW_MS=60000

# 2. 对于突发工作负载，扩大窗口
RATE_LIMIT_MAX=1000
RATE_LIMIT_WINDOW_MS=300000

# 3. 重启网关
npm run dev

# 4. 注意：限流按 API key（如已认证）或 IP。
# 不同 API key 有独立计数器。
```

### 9c. 按 API Key vs 按 IP 限流

**症状**：共享同一 IP 的不同客户端互相干扰限流。

**原因**：没有 API key 时，来自同一 IP 的所有请求共享一个限流桶。

**解决方案**：

```bash
# 1. 为每个客户端分配唯一 API key
API_KEYS=client1-key:user,client2-key:user,admin-key:admin

# 2. 每个客户端使用自己的 X-API-Key 头
# 客户端 1：-H "X-API-Key: client1-key"
# 客户端 2：-H "X-API-Key: client2-key"

# 3. 每个 key 获得独立的限流计数器
```

---

## 10. 认证问题

### 10a. API Key 不被接受

**症状**：每个请求返回 HTTP 401，body 为 `{ "error": "AUTH_FAILED", "message": "Invalid API key" }`。

**原因**：`X-API-Key` 头值不匹配 `API_KEYS` 中的任何条目。

**解决方案**：

```bash
# 1. 检查配置的 key
grep API_KEYS .env
# 格式：key1:admin,key2:user

# 2. 确保请求使用精确的 key（无额外空格）
curl -H "X-API-Key: mykey123" http://localhost:3000/health

# 3. Key 区分大小写且精确匹配

# 4. 如果 API_KEYS 为空，认证被禁用（开发模式）
# 所有请求视为管理员。生产环境请设置 key：
API_KEYS=sk-prod-abc123:admin,sk-user-xyz789:user
```

### 10b. JWT Token 过期

**症状**：请求返回 `{ "error": "AUTH_FAILED", "message": "JWT token has expired" }`。

**原因**：JWT `exp` 声明已过期。

**解决方案**：

```bash
# 1. 解码 JWT 检查过期时间（不验证）
echo "<your-token>" | cut -d'.' -f2 | base64 -d 2>/dev/null | jq '.exp'

# 2. 与当前时间比较
date +%s

# 3. 用更长 TTL 生成新 token
# 示例使用 Node.js：
node -e "
const crypto = require('crypto');
const secret = 'your-jwt-secret';
const header = Buffer.from(JSON.stringify({alg:'HS256',typ:'JWT'})).toString('base64url');
const payload = Buffer.from(JSON.stringify({
  sub: 'user-1',
  role: 'admin',
  iat: Math.floor(Date.now()/1000),
  exp: Math.floor(Date.now()/1000) + 86400  // 24 hours
})).toString('base64url');
const sig = crypto.createHmac('sha256', secret).update(header+'.'+payload).digest('base64url');
console.log(header+'.'+payload+'.'+sig);
"
```

### 10c. JWT 签名无效

**症状**：请求返回 `{ "error": "AUTH_FAILED", "message": "Invalid JWT signature" }`。

**原因**：JWT 用不同的密钥签名，与 `JWT_SECRET` 配置的不匹配。

**解决方案**：

```bash
# 1. 验证 token 签发方和网关方的密钥匹配
grep JWT_SECRET .env

# 2. 网关仅使用 HMAC-SHA256 (HS256)
# 确保 token 签发方也使用相同密钥的 HS256

# 3. 用正确密钥重新生成 token
```

### 10d. 未提供认证头

**症状**：请求返回 `{ "error": "AUTH_FAILED", "message": "Authentication required. Provide X-API-Key header or Authorization: Bearer token." }`。

**原因**：请求无 `X-API-Key` 头且无 `Authorization: Bearer` 头，且认证已启用（设置了 API_KEYS 或 JWT_SECRET）。

**解决方案**：

```bash
# 方案 A：使用 API Key
curl -H "X-API-Key: your-key" http://localhost:3000/health

# 方案 B：使用 JWT Bearer token
curl -H "Authorization: Bearer your.jwt.token" http://localhost:3000/health

# 方案 C：开发环境禁用认证（生产环境不要用）
# 从 .env 的 API_KEYS 和 JWT_SECRET 中删除所有值：
API_KEYS=
JWT_SECRET=
```

### 10e. 权限不足（禁止访问）

**症状**：请求返回 HTTP 403，body 为 `{ "error": "FORBIDDEN", "message": "Admin role required for this operation" }`。

**原因**：你使用 `user` 角色 key 执行仅管理员操作（工作流 CRUD）。

**解决方案**：

```bash
# 1. 检查你的 key 拥有哪个角色
grep API_KEYS .env
# 示例：sk-user-key:user,sk-admin-key:admin

# 2. 使用管理员 key 进行工作流管理
curl -H "X-API-Key: sk-admin-key" -X POST http://localhost:3000/workflows ...

# 3. user 角色可以：创建任务、读取自己的任务、查看健康/能力
# admin 角色可以：user 能做的所有事 + 工作流 CRUD + 查看所有任务
```

---

## 快速诊断命令

```bash
# 网关健康
curl -s http://localhost:3000/health | jq .

# ComfyUI 直接连通性
curl -s http://127.0.0.1:8188/ | head -5

# 队列状态
curl -s http://localhost:3000/jobs?status=queued -H "X-API-Key: KEY" | jq '.count'
curl -s http://localhost:3000/jobs?status=running -H "X-API-Key: KEY" | jq '.count'

# GPU 内存
nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader

# Redis 连通性
redis-cli -u "$REDIS_URL" ping

# SQLite 完整性
sqlite3 ./data/gateway.db "PRAGMA integrity_check;"

# 日志（如使用 pino-pretty）
npm run dev 2>&1 | npx pino-pretty

# 检查所有配置的环境变量
grep -v '^#' .env | grep -v '^$'
```
