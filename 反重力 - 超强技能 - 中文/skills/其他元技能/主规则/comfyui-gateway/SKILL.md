---
name: comfyui-gateway
description: ComfyUI 服务器的 REST API 网关。支持工作流管理、任务队列、webhook 回调、缓存、认证、限流和图片交付（URL + base64）。当用户要求"comfyui网关"、"comfyui api"、"stable diffusion api gateway"、"图片生成队列"时使用。
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- comfyui
- api-gateway
- image-generation
- typescript
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# ComfyUI Gateway

## 概述

ComfyUI 服务器的 REST API 网关。支持工作流管理、任务队列、webhook 回调、缓存、认证、限流和图片交付（URL + base64）。

## 何时使用此技能

- 当用户提到 "comfyui" 或相关话题时
- 当用户提到 "comfy ui" 或相关话题时
- 当用户提到 "stable diffusion api gateway" 或相关话题时
- 当用户提到 "gateway comfyui" 或相关话题时
- 当用户提到 "api gateway imagens" 或相关话题时
- 当用户提到 "queue imagens" 或相关话题时

## 何时不使用此技能

- 任务与 comfyui 网关无关
- 更简单、更专用的工具可以处理请求
- 用户需要无领域专业知识的通用帮助

## 工作原理

生产级 REST API 网关，将任意 ComfyUI 服务器转换为通用、安全、可扩展的服务。支持带占位符的工作流模板、优先级任务队列、webhook 回调、结果缓存和多种存储后端。

## 架构概览

```
┌─────────────┐     ┌──────────────────────────────────┐     ┌──────────┐
│   Clients    │────▶│        ComfyUI Gateway           │────▶│ ComfyUI  │
│ (curl, n8n,  │     │                                  │     │ Server   │
│  Claude,     │     │  ┌─────────┐  ┌──────────────┐  │     │ (local/  │
│  Lovable,    │     │  │ Fastify │  │ BullMQ Queue │  │     │  remote) │
│  Supabase)   │     │  │ API     │──│ (or in-mem)  │  │     └──────────┘
│              │◀────│  └─────────┘  └──────────────┘  │
│              │     │  ┌─────────┐  ┌──────────────┐  │     ┌──────────┐
│              │     │  │ Auth +  │  │ Storage      │  │────▶│ S3/MinIO │
│              │     │  │ RateL.  │  │ (local/S3)   │  │     │(optional)│
│              │     │  └─────────┘  └──────────────┘  │     └──────────┘
└─────────────┘     └──────────────────────────────────┘
```

## 组件

| 组件 | 用途 | 文件 |
|------|------|------|
| **API Gateway** | REST 端点、验证、CORS | `src/api/` |
| **Worker** | 处理任务、与 ComfyUI 通信 | `src/worker/` |
| **ComfyUI Client** | HTTP + WebSocket 连接 ComfyUI | `src/comfyui/` |
| **Workflow Manager** | 模板存储、占位符渲染 | `src/workflows/` |
| **Storage Provider** | 本地磁盘 + S3 兼容存储 | `src/storage/` |
| **Cache** | 基于哈希的去重 | `src/cache/` |
| **Notifier** | 带 HMAC 签名的 Webhook | `src/notifications/` |
| **Auth** | API key + JWT + 限流 | `src/auth/` |
| **DB** | SQLite (better-sqlite3) 或 Postgres | `src/db/` |
| **CLI** | init、add-workflow、run、worker | `src/cli/` |

## 快速开始

```bash

## 1. 安装

cd comfyui-gateway
npm install

## 2. 配置

cp .env.example .env

## 3. 初始化

npx tsx src/cli/index.ts init

## 4. 添加工作流

npx tsx src/cli/index.ts add-workflow ./workflows/sdxl_realism_v1.json \
  --id sdxl_realism_v1 --schema ./workflows/sdxl_realism_v1.schema.json

## 5. 启动（API + Worker 单进程）

npm run dev

## 或分开启动：

npm run start:api   # 仅 API
npm run start:worker # 仅 Worker
```

## 环境变量

所有配置通过 `.env` 完成——无硬编码：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PORT` | `3000` | API 服务器端口 |
| `HOST` | `0.0.0.0` | API 绑定地址 |
| `COMFYUI_URL` | `http://127.0.0.1:8188` | ComfyUI 服务器 URL |
| `COMFYUI_TIMEOUT_MS` | `300000` | ComfyUI 最大等待时间（5分钟） |
| `API_KEYS` | `""` | 逗号分隔的 API keys（`key:role`） |
| `JWT_SECRET` | `""` | JWT 签名密钥（空则禁用 JWT） |
| `REDIS_URL` | `""` | Redis URL（空则使用内存队列） |
| `DATABASE_URL` | `./data/gateway.db` | SQLite 路径或 Postgres URL |
| `STORAGE_PROVIDER` | `local` | `local` 或 `s3` |
| `STORAGE_LOCAL_PATH` | `./data/outputs` | 本地输出目录 |
| `S3_ENDPOINT` | `""` | S3/MinIO 端点 |
| `S3_BUCKET` | `""` | S3 存储桶名称 |
| `S3_ACCESS_KEY` | `""` | S3 访问密钥 |
| `S3_SECRET_KEY` | `""` | S3 密钥 |
| `S3_REGION` | `us-east-1` | S3 区域 |
| `WEBHOOK_SECRET` | `""` | Webhook HMAC 签名密钥 |
| `WEBHOOK_ALLOWED_DOMAINS` | `*` | 逗号分隔的允许回调域名 |
| `MAX_CONCURRENCY` | `1` | 每 GPU 并行任务数 |
| `MAX_IMAGE_SIZE` | `2048` | 最大尺寸（宽或高） |
| `MAX_BATCH_SIZE` | `4` | 最大批次大小 |
| `CACHE_ENABLED` | `true` | 启用结果缓存 |
| `CACHE_TTL_SECONDS` | `86400` | 缓存 TTL（24小时） |
| `RATE_LIMIT_MAX` | `100` | 时间窗口内请求数 |
| `RATE_LIMIT_WINDOW_MS` | `60000` | 限流窗口（1分钟） |
| `LOG_LEVEL` | `info` | Pino 日志级别 |
| `PRIVACY_MODE` | `false` | 从日志中脱敏提示词 |
| `CORS_ORIGINS` | `*` | 允许的 CORS 来源 |
| `NODE_ENV` | `development` | 环境 |

## 健康检查与能力

```
GET /health
→ { ok: true, version, comfyui: { reachable, url, models? }, uptime }

GET /capabilities
→ { workflows: [...], maxSize, maxBatch, formats, storageProvider }
```

## 工作流（CRUD）

```
GET    /workflows            → 列出所有工作流
POST   /workflows            → 注册新工作流
GET    /workflows/:id        → 工作流详情 + 输入 schema
PUT    /workflows/:id        → 更新工作流
DELETE /workflows/:id        → 删除工作流
```

## 任务

```
POST   /jobs                 → 创建任务（立即返回 jobId）
GET    /jobs/:jobId          → 状态 + 进度 + 输出
GET    /jobs/:jobId/logs     → 清理后的执行日志
POST   /jobs/:jobId/cancel   → 请求取消
GET    /jobs                 → 列出任务（过滤：status, workflowId, after, before, limit）
```

## 输出

```
GET    /outputs/:jobId       → 列出输出文件 + 元数据
GET    /outputs/:jobId/:file → 下载/流式传输文件
```

## 任务生命周期

```
queued → running → succeeded
                 → failed
                 → canceled
```

1. 客户端 POST 到 `/jobs`，携带 workflowId + inputs
2. Gateway 验证、检查缓存、检查幂等性
3. 若缓存命中 → 立即返回已有输出（status: `cache_hit`）
4. 否则 → 入队任务，返回 `jobId` + `pollUrl`
5. Worker 取出任务，渲染工作流模板，提交到 ComfyUI
6. Worker 轮询 ComfyUI 获取进度（或通过 WebSocket 监听）
7. 完成后 → 下载输出、存储、更新数据库
8. 若有 callbackUrl → 发送签名的 webhook POST
9. 客户端轮询 `/jobs/:jobId` 或接收 webhook

## 工作流模板

工作流是带 `{{placeholder}}` 标记的 ComfyUI JSON。Gateway 在运行时使用任务的 `inputs` 和 `params` 解析这些标记：

```json
{
  "3": {
    "class_type": "KSampler",
    "inputs": {
      "seed": "{{seed}}",
      "steps": "{{steps}}",
      "cfg": "{{cfg}}",
      "sampler_name": "{{sampler}}",
      "scheduler": "normal",
      "denoise": 1,
      "model": ["4", 0],
      "positive": ["6", 0],
      "negative": ["7", 0],
      "latent_image": ["5", 0]
    }
  },
  "6": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "{{prompt}}",
      "clip": ["4", 1]
    }
  }
}
```

每个工作流有一个 `inputSchema`（Zod），验证客户端发送的内容。

## 安全模型

- **API Keys**：`X-API-Key` 头；通过 `API_KEYS` 环境变量配置，格式为 `key1:admin,key2:user`
- **JWT**：可选；设置 `JWT_SECRET` 后，接受 `Authorization: Bearer <token>`
- **角色**：`admin`（工作流和任务的完整 CRUD），`user`（创建任务、读取自己的任务）
- **限流**：按 key + 按 IP，可配置窗口和最大请求数
- **Webhook 安全**：`X-Signature` 头中的 HMAC-SHA256 签名
- **回调白名单**：仅批准的域名接收 webhook
- **隐私模式**：启用后，提示词从日志和数据库中脱敏
- **幂等性**：`metadata.requestId` 防止重复处理
- **CORS**：可配置允许的来源
- **输入验证**：每个端点的 Zod schema；强制执行最大尺寸/批次

## ComfyUI 集成

Gateway 通过 ComfyUI 原生 HTTP API 与其通信：

| ComfyUI 端点 | Gateway 用途 |
|--------------|--------------|
| `POST /prompt` | 提交渲染后的工作流 |
| `GET /history/{id}` | 轮询任务完成状态 |
| `GET /view?filename=...` | 下载生成的图片 |
| `GET /object_info` | 发现可用节点/模型 |
| `WS /ws?clientId=...` | 实时进度（可选） |

客户端自动检测 ComfyUI 版本并适配：
- 优先尝试 WebSocket 获取进度，失败则回退到轮询
- 处理两种 `/history` 响应格式
- 检测 OOM 错误并分类提供建议

## 缓存策略

缓存键 = `workflowId + sorted(inputs) + sorted(params) + checkpoint` 的 SHA-256。
缓存命中时，Gateway 返回一个"虚拟"任务，包含已有输出——无需 GPU 计算。缓存与任务数据一起存储在数据库中，TTL 可配置。

## 错误分类

| 错误码 | 含义 | 可重试？ |
|--------|------|----------|
| `COMFYUI_UNREACHABLE` | 无法连接 ComfyUI | 是（带回退） |
| `COMFYUI_OOM` | GPU 内存不足 | 否（降低分辨率） |
| `COMFYUI_TIMEOUT` | 执行超时 | 可能（增加超时） |
| `COMFYUI_NODE_ERROR` | 节点执行失败 | 否（检查工作流） |
| `VALIDATION_ERROR` | 输入无效 | 否（修正请求） |
| `WORKFLOW_NOT_FOUND` | 未知的 workflowId | 否（注册工作流） |
| `RATE_LIMITED` | 请求过多 | 是（等待） |
| `AUTH_FAILED` | 凭证无效/缺失 | 否（修正认证） |
| `CACHE_HIT` | （非错误）从缓存提供 | 不适用 |

## 内置工作流

包含三个生产就绪的工作流模板：

## 1. `Sdxl_Realism_V1` — 照片级真实生成

- Checkpoint：SDXL base
- 优化用于：人像、风景、产品图
- 默认：1024x1024，30 步，cfg 7.0

## 2. `Sprite_Transparent_Bg` — 带 Alpha 的游戏精灵

- Checkpoint：SD 1.5 或 SDXL
- 优化用于：2D 游戏素材、透明背景
- 默认：512x512，25 步，cfg 7.5

## 3. `Icon_512` — 带可选放大的应用图标

- Checkpoint：SDXL base
- 优化用于：方形图标、清晰边缘
- 默认：512x512，20 步，cfg 6.0，可选 2x 放大

## 可观测性

- **结构化日志**：Pino JSON 日志，每个请求带 `correlationId`
- **指标**：任务排队/运行/成功/失败数、平均处理时间、缓存命中率
- **审计日志**：管理员操作（工作流 CRUD、密钥管理）带时间戳 + 操作者记录

## CLI 参考

```bash
npx tsx src/cli/index.ts init                    # 创建目录、.env.example
npx tsx src/cli/index.ts add-workflow <file>      # 注册工作流模板
  --id <id> --name <name> --schema <schema.json>
npx tsx src/cli/index.ts list-workflows           # 显示已注册工作流
npx tsx src/cli/index.ts run                      # 启动 API 服务器
npx tsx src/cli/index.ts worker                   # 启动任务 Worker
npx tsx src/cli/index.ts health                   # 检查 ComfyUI 连通性
```

## 故障排查

阅读 `references/troubleshooting.md` 获取详细指导：
- ComfyUI 不可达（防火墙、错误端口、Docker 网络）
- OOM 错误（降低分辨率、批次或步数）
- 生成缓慢（GPU 利用率、队列深度、模型加载）
- Webhook 失败（DNS、SSL、超时、域名白名单）
- Redis 连接问题（回退到内存队列）
- 存储权限错误（本地路径、S3 凭证）

## 集成示例

阅读 `references/integration.md` 获取即用示例：
- 每个端点的 curl 命令
- n8n webhook 工作流
- Supabase Edge Function 调用器
- Claude Code / Claude.ai 集成
- Python requests 客户端
- JavaScript fetch 客户端

## 文件结构

```
comfyui-gateway/
├── SKILL.md
├── package.json
├── tsconfig.json
├── .env.example
├── src/
│   ├── api/
│   │   ├── server.ts          # Fastify 设置 + 插件
│   │   ├── routes/
│   │   │   ├── health.ts      # GET /health, /capabilities
│   │   │   ├── workflows.ts   # CRUD /workflows
│   │   │   ├── jobs.ts        # CRUD /jobs
│   │   │   └── outputs.ts     # GET /outputs
│   │   ├── middleware/
│   │   │   └── error-handler.ts
│   │   └── plugins/
│   │       ├── auth.ts        # API key + JWT
│   │       ├── rate-limit.ts
│   │       └── cors.ts
│   ├── worker/
│   │   └── processor.ts       # 任务处理器
│   ├── comfyui/
│   │   └── client.ts          # ComfyUI HTTP + WS 客户端
│   ├── storage/
│   │   ├── index.ts           # Provider 工厂
│   │   ├── local.ts           # 本地文件系统
│   │   └── s3.ts              # S3 兼容
│   ├── workflows/
│   │   └── manager.ts         # 模板 CRUD + 渲染
│   ├── cache/
│   │   └── index.ts           # 基于哈希的缓存
│   ├── notifications/
│   │   └── webhook.ts         # HMAC 签名回调
│   ├── auth/
│   │   └── index.ts           # Key/JWT 验证 + 角色
│   ├── db/
│   │   ├── index.ts           # DB 工厂（SQLite/Postgres）
│   │   └── migrations.ts      # Schema 创建
│   ├── cli/
│   │   └── index.ts           # CLI 命令
│   ├── utils/
│   │   ├── config.ts          # 环境加载 + 验证
│   │   ├── errors.ts          # 错误类
│   │   ├── logger.ts          # Pino 设置
│   │   └── hash.ts            # SHA-256 哈希
│   └── index.ts               # 主入口
├── config/
│   └── workflows/             # 内置工作流模板
│       ├── sdxl_realism_v1.json
│       ├── sdxl_realism_v1.schema.json
│       ├── sprite_transparent_bg.json
│       ├── sprite_transparent_bg.schema.json
│       ├── icon_512.json
│       └── icon_512.schema.json
├── data/
│   ├── outputs/               # 生成的图片
│   ├── workflows/             # 用户添加的工作流
```
