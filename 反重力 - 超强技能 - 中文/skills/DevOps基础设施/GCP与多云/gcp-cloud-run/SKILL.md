---
name: gcp-cloud-run
description: 在 GCP 上构建生产级无服务器应用的专项技能。涵盖 Cloud Run 服务（容器化）、Cloud Run Functions（事件驱动）、冷启动优化以及与 Pub/Sub 的事件驱动架构。当用户要求部署 Cloud Run、构建无服务器应用、容器化部署到 GCP、事件驱动处理时使用。
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# GCP Cloud Run

在 GCP 上构建生产级无服务器应用的专项技能。
涵盖 Cloud Run 服务（容器化）、Cloud Run Functions（事件驱动）、冷启动优化以及与 Pub/Sub 的事件驱动架构。

## 原则

- Cloud Run 用于容器，Functions 用于简单事件处理
- 通过启动 CPU 加速和最小实例数优化冷启动
- 根据工作负载设置并发（从 8 开始，按需调整）
- 内存包含 /tmp 文件系统 — 需提前规划
- 仅在必要时使用 VPC Connector（会增加延迟）
- 容器应快速启动且无状态
- 优雅处理信号以实现干净关闭

## 模式

### Cloud Run 服务模式

Cloud Run 上的容器化 Web 服务

**适用场景**：Web 应用和 API、需要任意运行时或库、具有多个端点的复杂服务、无状态容器化工作负载

```dockerfile
# Dockerfile - 多阶段构建以减小镜像体积
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-slim
WORKDIR /app

# 仅复制生产依赖
COPY --from=builder /app/node_modules ./node_modules
COPY src ./src
COPY package.json ./

# Cloud Run 使用 PORT 环境变量
ENV PORT=8080
EXPOSE 8080

# 以非 root 用户运行
USER node

CMD ["node", "src/index.js"]
```

```javascript
// src/index.js
const express = require('express');
const app = express();

app.use(express.json());

// 健康检查端点
app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

// API 路由
app.get('/api/items/:id', async (req, res) => {
  try {
    const item = await getItem(req.params.id);
    res.json(item);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// 优雅关闭
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});

const PORT = process.env.PORT || 8080;
const server = app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
```

```yaml
# cloudbuild.yaml
steps:
  # 构建容器镜像
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/my-service:$COMMIT_SHA', '.']

  # 推送容器镜像
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/my-service:$COMMIT_SHA']

  # 部署到 Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'my-service'
      - '--image=gcr.io/$PROJECT_ID/my-service:$COMMIT_SHA'
      - '--region=us-central1'
      - '--platform=managed'
      - '--allow-unauthenticated'
      - '--memory=512Mi'
      - '--cpu=1'
      - '--min-instances=1'
      - '--max-instances=100'
      - '--concurrency=80'
      - '--cpu-boost'

images:
  - 'gcr.io/$PROJECT_ID/my-service:$COMMIT_SHA'
```

### 结构

project/
├── Dockerfile
├── .dockerignore
├── src/
│   ├── index.js
│   └── routes/
├── package.json
└── cloudbuild.yaml

### Gcloud_deploy

# 直接使用 gcloud 部署
gcloud run deploy my-service \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 1 \
  --max-instances 100 \
  --concurrency 80 \
  --cpu-boost

### Cloud Run Functions 模式

事件驱动函数（原 Cloud Functions）

**适用场景**：简单事件处理、Pub/Sub 消息处理、Cloud Storage 触发器、HTTP webhook

```javascript
// HTTP 函数
// index.js
const functions = require('@google-cloud/functions-framework');

functions.http('helloHttp', (req, res) => {
  const name = req.query.name || req.body.name || 'World';
  res.send(`Hello, ${name}!`);
});
```

```javascript
// Pub/Sub 函数
const functions = require('@google-cloud/functions-framework');

functions.cloudEvent('processPubSub', (cloudEvent) => {
  // 解码 Pub/Sub 消息
  const message = cloudEvent.data.message;
  const data = message.data
    ? JSON.parse(Buffer.from(message.data, 'base64').toString())
    : {};

  console.log('Received message:', data);

  // 处理消息
  processMessage(data);
});
```

```javascript
// Cloud Storage 函数
const functions = require('@google-cloud/functions-framework');

functions.cloudEvent('processStorageEvent', async (cloudEvent) => {
  const file = cloudEvent.data;

  console.log(`Event: ${cloudEvent.type}`);
  console.log(`Bucket: ${file.bucket}`);
  console.log(`File: ${file.name}`);

  if (cloudEvent.type === 'google.cloud.storage.object.v1.finalized') {
    await processUploadedFile(file.bucket, file.name);
  }
});
```

```bash
# 部署 HTTP 函数
gcloud functions deploy hello-http \
  --gen2 \
  --runtime nodejs20 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1

# 部署 Pub/Sub 函数
gcloud functions deploy process-messages \
  --gen2 \
  --runtime nodejs20 \
  --trigger-topic my-topic \
  --region us-central1

# 部署 Cloud Storage 函数
gcloud functions deploy process-uploads \
  --gen2 \
  --runtime nodejs20 \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=my-bucket" \
  --region us-central1
```

### 冷启动优化模式

最小化 Cloud Run 的冷启动延迟

**适用场景**：延迟敏感应用、面向用户的 API、高流量服务

## 1. 启用启动 CPU 加速

```bash
gcloud run deploy my-service \
  --cpu-boost \
  --region us-central1
```

## 2. 设置最小实例数

```bash
gcloud run deploy my-service \
  --min-instances 1 \
  --region us-central1
```

## 3. 优化容器镜像

```dockerfile
# 使用 distroless 以获得最小镜像
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM gcr.io/distroless/nodejs20-debian12
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY src ./src
CMD ["src/index.js"]
```

## 4. 延迟初始化重型依赖

```javascript
// 延迟加载重型库
let bigQueryClient = null;

function getBigQueryClient() {
  if (!bigQueryClient) {
    const { BigQuery } = require('@google-cloud/bigquery');
    bigQueryClient = new BigQuery();
  }
  return bigQueryClient;
}

// 仅在需要时初始化
app.get('/api/analytics', async (req, res) => {
  const client = getBigQueryClient();
  const results = await client.query({...});
  res.json(results);
});
```

## 5. 增加内存（更多 CPU）

```bash
# 更高内存 = 启动时更多 CPU
gcloud run deploy my-service \
  --memory 1Gi \
  --cpu 2 \
  --region us-central1
```

### Optimization_impact

- Startup_cpu_boost: 冷启动快 50%
- Min_instances: 消除流量突增时的冷启动
- Distroless_image: 更小的攻击面，更快的拉取
- Lazy_init: 将重型加载延迟到首次请求

### 并发配置模式

Cloud Run 的正确并发设置

**适用场景**：需要优化实例利用率、高效处理流量突增、减少冷启动

## 理解并发

```bash
# 默认并发为 80
# 根据工作负载调整

# 对于 I/O 密集型工作负载（大多数 Web 应用）
gcloud run deploy my-service \
  --concurrency 80 \
  --cpu 1

# 对于 CPU 密集型工作负载
gcloud run deploy my-service \
  --concurrency 1 \
  --cpu 1

# 对于内存密集型工作负载
gcloud run deploy my-service \
  --concurrency 10 \
  --memory 2Gi
```

## Node.js 并发

```javascript
// Node.js 是单线程的，但可以并发处理 I/O
// 对所有 I/O 操作使用 async/await

// 好 - 异步 I/O
app.get('/api/data', async (req, res) => {
  const [users, products] = await Promise.all([
    fetchUsers(),
    fetchProducts()
  ]);
  res.json({ users, products });
});

// 坏 - 阻塞操作
app.get('/api/compute', (req, res) => {
  const result = heavyCpuOperation(); // 阻塞其他请求！
  res.json(result);
});
```

## Python 使用 Gunicorn 实现并发

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# 4 个 worker 实现并发
CMD exec gunicorn --bind :$PORT --workers 4 --threads 2 main:app
```

```python
# main.py
from flask import Flask
app = Flask(__name__)

@app.route('/api/data')
def get_data():
    return {'status': 'ok'}
```

### Concurrency_guidelines

- Concurrency=1: 仅用于 CPU 密集型或不安全代码
- Concurrency=8-20: 内存密集型工作负载
- Concurrency=80: 默认值，适合 I/O 密集型
- Concurrency=250: 最大值，用于非常轻量的处理程序

### Pub/Sub 集成模式

使用 Cloud Pub/Sub 进行事件驱动处理

**适用场景**：异步消息处理、解耦微服务、事件驱动架构

## 推送订阅到 Cloud Run

```bash
# 创建主题
gcloud pubsub topics create orders

# 创建到 Cloud Run 的推送订阅
gcloud pubsub subscriptions create orders-push \
  --topic orders \
  --push-endpoint https://my-service-xxx.run.app/pubsub \
  --ack-deadline 600
```

```javascript
// 处理 Pub/Sub 推送消息
const express = require('express');
const app = express();
app.use(express.json());

app.post('/pubsub', async (req, res) => {
  // 验证请求来自 Pub/Sub
  if (!req.body.message) {
    return res.status(400).send('Invalid Pub/Sub message');
  }

  try {
    // 解码消息数据
    const message = req.body.message;
    const data = message.data
      ? JSON.parse(Buffer.from(message.data, 'base64').toString())
      : {};

    console.log('Processing order:', data);

    await processOrder(data);

    // 返回 200 确认
    res.status(200).send('OK');
  } catch (error) {
    console.error('Processing failed:', error);
    // 返回 500 触发重试
    res.status(500).send('Processing failed');
  }
});
```

## 发布消息

```javascript
const { PubSub } = require('@google-cloud/pubsub');
const pubsub = new PubSub();

async function publishOrder(order) {
  const topic = pubsub.topic('orders');
  const messageBuffer = Buffer.from(JSON.stringify(order));

  const messageId = await topic.publishMessage({
    data: messageBuffer,
    attributes: {
      type: 'order_created',
      priority: 'high'
    }
  });

  console.log(`Published message ${messageId}`);
  return messageId;
}
```

## 死信队列

```bash
# 创建 DLQ 主题
gcloud pubsub topics create orders-dlq

# 更新订阅添加 DLQ
gcloud pubsub subscriptions update orders-push \
  --dead-letter-topic orders-dlq \
  --max-delivery-attempts 5
```

### Cloud SQL 连接模式

安全地将 Cloud Run 连接到 Cloud SQL

**适用场景**：需要关系型数据库、迁移现有应用、复杂查询和事务

```bash
# 部署时添加 Cloud SQL 连接
gcloud run deploy my-service \
  --add-cloudsql-instances PROJECT:REGION:INSTANCE \
  --set-env-vars INSTANCE_CONNECTION_NAME="PROJECT:REGION:INSTANCE" \
  --set-env-vars DB_NAME="mydb" \
  --set-env-vars DB_USER="myuser"
```

```javascript
// 使用 Unix socket 连接
const { Pool } = require('pg');

const pool = new Pool({
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME,
  // Cloud SQL connector 使用 Unix socket
  host: `/cloudsql/${process.env.INSTANCE_CONNECTION_NAME}`,
  max: 5,  // 连接池大小
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 10000,
});

app.get('/api/users', async (req, res) => {
  const client = await pool.connect();
  try {
    const result = await client.query('SELECT * FROM users LIMIT 100');
    res.json(result.rows);
  } finally {
    client.release();
  }
});
```

```python
# Python 使用 SQLAlchemy
import os
from sqlalchemy import create_engine

def get_engine():
    instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]

    engine = create_engine(
        f"postgresql+pg8000://{db_user}:{db_pass}@/{db_name}",
        connect_args={
            "unix_sock": f"/cloudsql/{instance_connection_name}/.s.PGSQL.5432"
        },
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,
    )
    return engine
```

### Best_practices

- 使用连接池（每个实例最多 5-10 个）
- 设置适当的空闲超时
- 优雅处理连接错误
- 本地开发考虑使用 Cloud SQL Proxy

### Secret Manager 集成

在 Cloud Run 中安全管理密钥

**适用场景**：API 密钥、数据库密码、服务账号密钥、任何敏感配置

```bash
# 创建密钥
echo -n "my-secret-value" | gcloud secrets create my-secret --data-file=-

# 挂载为环境变量
gcloud run deploy my-service \
  --update-secrets=API_KEY=my-secret:latest

# 挂载为文件卷
gcloud run deploy my-service \
  --update-secrets=/secrets/api-key=my-secret:latest
```

```javascript
// 访问挂载为环境变量的密钥
const apiKey = process.env.API_KEY;

// 访问挂载为文件的密钥
const fs = require('fs');
const apiKey = fs.readFileSync('/secrets/api-key', 'utf8');

// 通过 Secret Manager API 访问（未挂载时）
const { SecretManagerServiceClient } = require('@google-cloud/secret-manager');
const client = new SecretManagerServiceClient();

async function getSecret(name) {
  const [version] = await client.accessSecretVersion({
    name: `projects/${projectId}/secrets/${name}/versions/latest`
  });
  return version.payload.data.toString();
}
```

## 陷阱与风险

### /tmp 文件系统计入内存

严重程度：高

场景：在 Cloud Run 中向 /tmp 目录写入文件

症状：
容器因 OOM 错误被终止。
内存使用意外飙升。
文件操作导致容器重启。
日志中出现 "Container memory limit exceeded"。

原因分析：
Cloud Run 使用内存文件系统作为 /tmp。任何写入 /tmp 的文件都会消耗容器的内存配额。

常见场景：
- 临时下载文件
- 创建临时处理文件
- 库缓存到 /tmp
- 大型日志缓冲区

一个 512MB 的容器如果向 /tmp 下载 200MB 文件，应用只剩约 300MB 可用内存。

推荐修复：

## 计算内存时包含 /tmp 使用量

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'my-service'
      - '--memory=1Gi'  # 包含 /tmp 开销
      - '--image=gcr.io/$PROJECT_ID/my-service'
```

## 使用流式处理而非缓冲

```python
# 坏 - 将整个文件缓冲到 /tmp
def process_large_file(bucket_name, blob_name):
    blob = bucket.blob(blob_name)
    blob.download_to_filename('/tmp/large_file')
    with open('/tmp/large_file', 'rb') as f:
        process(f.read())

# 好 - 流式处理
def process_large_file(bucket_name, blob_name):
    blob = bucket.blob(blob_name)
    with blob.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            process_chunk(chunk)
```

## 使用 Cloud Storage 处理大文件

```python
from google.cloud import storage

def process_with_gcs(bucket_name, input_blob, output_blob):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # 直接在 GCS 之间处理
    input_blob = bucket.blob(input_blob)
    output_blob = bucket.blob(output_blob)

    with input_blob.open('rb') as reader:
        with output_blob.open('wb') as writer:
            for chunk in iter(lambda: reader.read(65536), b''):
                processed = transform(chunk)
                writer.write(processed)
```

## 监控内存使用

```python
import psutil
import logging

def log_memory():
    memory = psutil.virtual_memory()
    logging.info(f"Memory: {memory.percent}% used, "
                f"{memory.available / 1024 / 1024:.0f}MB available")
```

### Concurrency=1 导致扩展瓶颈

严重程度：高

场景：将并发设置为 1 以实现请求隔离

症状：
自动扩缩创建大量容器实例。
流量突增时延迟升高。
冷启动增加。
更多实例导致成本上升。

原因分析：
将并发设置为 1 意味着每个容器一次只处理一个请求。在流量突增时：

- 100 个并发请求 = 100 个容器实例
- 每个实例都有冷启动开销
- 更多实例 = 更高成本
- 扩展需要时间，请求排队

仅应在以下情况使用：
- 处理确实是单线程的
- 每请求内存消耗大
- 使用线程不安全的库

推荐修复：

## 设置适当的并发

```bash
# 对于 I/O 密集型工作负载（大多数 Web 应用）
gcloud run deploy my-service \
  --concurrency=80 \
  --max-instances=100

# 对于 CPU 密集型工作负载
gcloud run deploy my-service \
  --concurrency=4 \
  --cpu=2

# 仅在绝对必要时使用 1
gcloud run deploy my-service \
  --concurrency=1 \
  --max-instances=1000  # 准备好大量实例
```

## Node.js - 正确使用异步

```javascript
// 高并发时，确保异步操作
const express = require('express');
const app = express();

app.get('/api/data', async (req, res) => {
  // 所有 I/O 应该是异步的
  const data = await fetchFromDatabase();
  const enriched = await enrichData(data);
  res.json(enriched);
});

// 并发 80+ 对异步 I/O 工作负载是安全的
```

## Python - 使用异步框架

```python
from fastapi import FastAPI
import asyncio
import httpx

app = FastAPI()

@app.get("/api/data")
async def get_data():
    # 异步 I/O 允许高并发
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()

# 使用异步框架时并发 80+ 是安全的
```

## 计算并发

```
concurrency = memory_limit / per_request_memory

示例：
- 512MB 容器
- 每请求 20MB 开销
- 安全并发：约 25
```

### 非请求处理期间 CPU 被限流

严重程度：高

场景：运行后台任务或在请求之间进行处理

症状：
后台任务运行极慢。
计划工作无法完成。
指标收集失败。
连接保活中断。

原因分析：
默认情况下，Cloud Run 在不主动处理请求时将 CPU 限流到接近零。这是"仅在请求期间提供 CPU"模式。

受影响的操作：
- 后台线程
- 连接池维护
- 指标/遥测发送
- 容器内的计划任务
- 响应后的清理操作

推荐修复：

## 启用 CPU 始终分配

```bash
# 即使在请求之外也分配 CPU
gcloud run deploy my-service \
  --cpu-throttling=false \
  --min-instances=1

# 注意：这会增加成本但启用后台工作
```

## 使用启动 CPU 加速进行初始化

```bash
# 仅在冷启动时加速 CPU
gcloud run deploy my-service \
  --cpu-boost \
  --cpu-throttling=true  # 默认，请求后限流
```

## 将后台工作移至 Cloud Tasks

```python
from google.cloud import tasks_v2
import json

def create_background_task(payload):
    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(
        "my-project", "us-central1", "my-queue"
    )

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": "https://my-service.run.app/process",
            "body": json.dumps(payload).encode(),
            "headers": {"Content-Type": "application/json"}
        }
    }

    client.create_task(parent=parent, task=task)

# 立即处理响应，后台通过 Cloud Tasks
@app.post("/api/order")
async def create_order(order: Order):
    order_id = await save_order(order)

    # 排队后台处理
    create_background_task({"order_id": order_id})

    return {"order_id": order_id, "status": "processing"}
```

## 使用 Pub/Sub 进行异步处理

```yaml
# 将重型处理移至独立服务
steps:
  # 主服务 - 快速响应
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'api-service',
           '--cpu-throttling=true']

  # Worker 服务 - 处理消息
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'worker-service',
           '--cpu-throttling=false',
           '--min-instances=1']
```

### VPC Connector 10 分钟空闲超时

严重程度：中

场景：Cloud Run 服务连接到 VPC 资源

症状：
一段时间不活动后出现连接错误。
"Connection reset" 或 "Connection refused" 错误。
VPC 资源间歇性失败。
数据库连接意外断开。

原因分析：
Cloud Run 的 VPC connector 对连接有 10 分钟空闲超时。如果连接空闲 10 分钟，会被静默关闭。

影响：
- 数据库连接池
- Redis 连接
- 内部 API 连接
- 任何持久的 VPC 连接

推荐修复：

## 配置带保活的连接池

```python
# SQLAlchemy 连接回收
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=2,
    pool_recycle=300,  # 每 5 分钟回收连接
    pool_pre_ping=True  # 使用前验证连接
)
```

## 自定义连接的 TCP 保活

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 60)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
```

## Redis 连接验证

```python
import redis

pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=6379,
    socket_keepalive=True,
    socket_keepalive_options={
        socket.TCP_KEEPIDLE: 60,
        socket.TCP_KEEPINTVL: 60,
        socket.TCP_KEEPCNT: 5
    },
    health_check_interval=30
)
client = redis.Redis(connection_pool=pool)
```

## 使用 Cloud SQL Proxy sidecar

```yaml
# 使用 Cloud SQL connector 处理重连
# requirements.txt
cloud-sql-python-connector[pg8000]
```

```python
from google.cloud.sql.connector import Connector
import sqlalchemy

connector = Connector()

def getconn():
    return connector.connect(
        "project:region:instance",
        "pg8000",
        user="user",
        password="password",
        db="database"
    )

engine = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn
)
```

### 容器启动超时（最大 4 分钟）

严重程度：高

场景：部署初始化缓慢的容器

症状：
部署失败，提示 "Container failed to start"。
服务永远无法变为健康状态。
"Revision failed to become ready" 错误。
本地正常但在 Cloud Run 上失败。

原因分析：
Cloud Run 期望容器在 4 分钟（240 秒）内开始监听 PORT。如果未做到，实例会被终止。

常见原因：
- 重型框架初始化（ML 模型等）
- 启动时等待外部依赖
- 大量依赖加载
- 启动时数据库迁移

推荐修复：

## 启用启动 CPU 加速

```bash
gcloud run deploy my-service \
  --cpu-boost \
  --startup-cpu-boost
```

## 延迟初始化

```python
from functools import lru_cache
from fastapi import FastAPI

app = FastAPI()

# 不要在导入时加载
model = None

@lru_cache()
def get_model():
    global model
    if model is None:
        # 在首次请求时加载，而非启动时
        model = load_heavy_model()
    return model

@app.get("/predict")
async def predict(data: dict):
    model = get_model()  # 仅在首次调用时加载
    return model.predict(data)

# 启动快速 - 模型在首次请求时加载
```

## 立即开始监听

```python
import asyncio
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# 异步初始化的全局状态
initialized = asyncio.Event()

@app.on_event("startup")
async def startup():
    # 启动后台初始化
    asyncio.create_task(async_init())

async def async_init():
    # 服务器启动后进行重型初始化
    await load_models()
    await warm_up_connections()
    initialized.set()

@app.get("/ready")
async def ready():
    if not initialized.is_set():
        raise HTTPException(503, "Still initializing")
    return {"status": "ready"}

@app.get("/health")
async def health():
    # 始终响应 - 健康检查通过
    return {"status": "healthy"}
```

## 使用多阶段构建

```dockerfile
# 构建阶段 - 慢
FROM python:3.11 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# 运行时阶段 - 快速启动
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## 单独运行迁移

```bash
# 不要在启动时迁移 - 使用 Cloud Build
steps:
  # 先运行迁移
  - name: 'gcr.io/cloud-builders/gcloud'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        gcloud run jobs execute migrate-job --wait

  # 然后部署
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'my-service', ...]
```

### 第二代执行环境差异

严重程度：中

场景：迁移到或使用 Cloud Run 第二代执行环境

症状：
网络行为变化。
不同的 syscall 支持。
文件系统行为差异。
容器行为与第一代不同。

原因分析：
Cloud Run 的第二代执行环境使用不同的沙箱（gVisor），具有不同特性：

- 支持更多 Linux syscalls
- 完整的 /proc 和 /sys 访问
- 不同的网络栈
- 无自动 HTTPS 重定向
- 不同的 tmp 文件系统行为

推荐修复：

## 显式设置执行环境

```bash
# 第一代（传统）
gcloud run deploy my-service \
  --execution-environment=gen1

# 第二代（推荐大多数情况使用）
gcloud run deploy my-service \
  --execution-environment=gen2
```

## 处理网络差异

```python
# 第二代不会自动将 HTTP 重定向到 HTTPS
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.middleware("http")
async def redirect_https(request: Request, call_next):
    # 检查 X-Forwarded-Proto 头
    if request.headers.get("X-Forwarded-Proto") == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url, status_code=301)
    return await call_next(request)
```

## GPU 访问（仅第二代）

```bash
# GPU 仅在第二代可用
gcloud run deploy ml-service \
  --execution-environment=gen2 \
  --gpu=1 \
  --gpu-type=nvidia-l4
```

## 检查执行环境

```python
import os

def get_execution_environment():
    # 第二代有不同的 /proc 结构
    try:
        with open('/proc/version', 'r') as f:
            version = f.read()
            if 'gVisor' in version:
                return 'gen2'
    except:
        pass
    return 'gen1'
```

### 请求超时配置不匹配

严重程度：中

场景：长时间运行的请求或后台处理

症状：
请求在完成前被终止。
504 Gateway Timeout 错误。
处理意外停止。
超时行为不一致。

原因分析：
Cloud Run 有多个必须对齐的超时配置：
- 请求超时（默认 300s，HTTP 最大 3600s，gRPC 最大 60m）
- 客户端超时
- 下游服务超时
- 负载均衡器超时（外部访问时）

推荐修复：

## 设置一致的超时

```bash
# 增加请求超时（HTTP 最大 3600s）
gcloud run deploy my-service \
  --timeout=900  # 15 分钟
```

## 使用 webhook 处理长时间运行

```python
from fastapi import FastAPI, BackgroundTasks
import httpx

app = FastAPI()

@app.post("/process")
async def process(data: dict, background_tasks: BackgroundTasks):
    task_id = create_task_id()

    # 启动后台处理
    background_tasks.add_task(
        long_running_process,
        task_id,
        data,
        data.get("callback_url")
    )

    # 立即返回
    return {"task_id": task_id, "status": "processing"}

async def long_running_process(task_id, data, callback_url):
    result = await heavy_computation(data)

    # 完成时回调
    if callback_url:
        async with httpx.AsyncClient() as client:
            await client.post(callback_url, json={
                "task_id": task_id,
                "result": result
            })
```

## 使用 Cloud Tasks 实现可靠的长时间运行

```python
from google.cloud import tasks_v2

def create_long_running_task(data):
    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(PROJECT, REGION, "long-tasks")

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": "https://worker.run.app/process",
            "body": json.dumps(data).encode(),
            "headers": {"Content-Type": "application/json"}
        },
        "dispatch_deadline": {"seconds": 1800}  # 30 分钟
    }

    return client.create_task(parent=parent, task=task)
```

## 长响应的流式传输

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

@app.get("/large-report")
async def large_report():
    async def generate():
        for chunk in process_large_data():
            yield chunk

    return StreamingResponse(generate(), media_type="text/plain")
```

## 验证检查

### 硬编码 GCP 凭证

严重程度：错误

GCP 凭证绝不能硬编码在源代码中

消息：硬编码的 GCP 服务账号凭证。请使用 Secret Manager 或 Workload Identity。

### 源代码中的 GCP API 密钥

严重程度：错误

API 密钥应使用 Secret Manager

消息：硬编码的 GCP API 密钥。请使用 Secret Manager。

### 仓库中的凭证 JSON 文件

严重程度：错误

服务账号 JSON 文件不应在源代码控制中

消息：检测到凭证文件。添加到 .gitignore 并使用 Secret Manager。

### 以 Root 用户运行

严重程度：警告

容器不应以 root 运行以确保安全

消息：Dockerfile 以 root 运行。添加 USER 指令以确保安全。

### Dockerfile 中缺少健康检查

严重程度：信息

Cloud Run 使用 HTTP 健康检查，Dockerfile HEALTHCHECK 是可选的

消息：Dockerfile 中无 HEALTHCHECK。Cloud Run 使用自己的健康检查。

### 应用中硬编码端口

严重程度：警告

端口应来自 PORT 环境变量

消息：硬编码端口。请使用 PORT 环境变量以适配 Cloud Run。

### 向 /tmp 写入大文件

严重程度：警告

/tmp 使用容器内存，大文件写入可能导致 OOM

消息：/tmp 写入消耗内存。大文件请考虑使用 Cloud Storage。

### 同步文件操作

严重程度：警告

同步文件操作会阻塞异步应用的事件循环

消息：同步文件操作。请使用异步版本以获得更好的并发性。

### 全局可变状态

严重程度：警告

全局状态在并发请求时可能出问题

消息：全局可变状态可能在并发请求时引发问题。

### 线程不安全的单例模式

严重程度：警告

单例在并发 > 1 时需要线程安全

消息：单例模式 - 如果使用并发 > 1，请确保线程安全。

## 协作

### 委托触发

- 用户需要 AWS 无服务器 -> aws-serverless (Lambda, API Gateway, SAM)
- 用户需要 Azure 容器 -> azure-functions (Azure Container Apps, Functions)
- 用户需要数据库设计 -> postgres-wizard (Cloud SQL 设计, AlloyDB)
- 用户需要身份验证 -> auth-specialist (Firebase Auth, Identity Platform)
- 用户需要 AI 集成 -> llm-architect (Vertex AI, Cloud Run + LLM)
- 用户需要工作流编排 -> workflow-automation (Cloud Workflows, Eventarc)

## 何时使用
当请求明显匹配上述能力和模式时使用此技能。

## 局限性
- 仅当任务明显匹配上述范围时使用此技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
