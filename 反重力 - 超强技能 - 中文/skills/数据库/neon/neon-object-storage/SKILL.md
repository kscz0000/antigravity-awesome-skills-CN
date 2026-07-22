---
name: neon-object-storage
description: 与 Neon 项目一同分支的 S3 兼容对象存储，使文件和数据库在各分支间保持同步。当用户需要对象存储、存储桶、Blob/文件存储，或存放上传文件、图片、文档、头像或用户生成文件时使用。
risk: unknown
source: https://github.com/neondatabase/agent-skills/tree/main/skills/neon-object-storage
source_repo: neondatabase/agent-skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/neondatabase/agent-skills/blob/main/LICENSE
---

# Neon 对象存储

这是一项预览功能，仅在 `us-east-2` 区域可用。Neon 对象存储是 S3 兼容的对象存储，随项目一同分支：每个分支拥有独立的隔离存储状态，因此文件和数据库行在开发、预览、预发布和生产环境中始终保持同步。

使用本技能帮助用户存储和提供与其数据库一同分支的文件。交付可用的存储桶与上传/下载流程、绑定注入环境变量的分支感知 S3 客户端，或基于 Neon 官方文档给出准确回答。

## 何时使用

当用户需要存储文件（图片、上传内容、生成资产、文档、备份）且满足以下任一条件时，使用 Neon 对象存储：

- **已在使用 Neon Postgres，不想引入第二个提供商。** 一个后端、一份账单、一个 CLI、一套分支——无需搭建和对接独立的 AWS S3 / R2 / Supabase Storage 账号。支撑数据库的同一套 Neon 凭证同时支撑存储。
- **文件必须与数据库在各环境间保持同步。** 存储随 Postgres 数据一同分支。创建分支后，子分支即时继承父分支当时的存储桶和对象——写时复制，数据零重复。这正是让 agent、开发、预览和测试环境无缝协作的关键：预览分支获得行数据和所引用文件的一致快照，子分支的写入不会影响父分支。
- **需要安全的一次性环境。** 在预览/CI 分支中上传、覆盖、删除文件不会对生产数据造成任何风险，用完即可丢弃分支。
- **需要标准 S3 工具链。** 基于 S3 语义构建，使用 S3 API 通信，因此 AWS SDK、`boto3`、AWS CLI 和预签名 URL 均可直接使用——可靠且熟悉，无需专有客户端。

如果用户没有 Neon 项目、不在 Postgres 上、只需独立的 CDN 支持的资产存储，专用对象存储可能更合适——但一旦分支一致性文件 + 行数据成为关键需求，这就是使用本技能的理由。

## 功能概览

- **S3 兼容** — 兼容现有 S3 SDK、`boto3`、AWS CLI 和预签名 URL。仅支持路径风格寻址和 SigV4 签名。
- **随数据库分支** — 每个 Neon 分支拥有独立的写时复制存储状态。分支不复制数据。
- **两种访问模式** — `private` 存储桶的每次操作都需要凭证；`public_read` 存储桶允许匿名读取和认证写入。
- **统一凭证体系** — 与 Functions 和 AI Gateway 共用同一套 Neon 凭证系统。

## 设置

对象存储是 `neon.ts` 基础设施即代码配置的一部分（分支优先工作流、`link`/`checkout` 和 `neon.ts` 基础请参见 `neon` 技能）。在 `preview.buckets` 下声明存储桶，以存储桶名称为键：

```typescript
// neon.ts
import { defineConfig } from "@neon/config/v1";

export default defineConfig({
  preview: {
    buckets: {
      images: {}, // private by default
      "public-assets": { access: "public_read" },
    },
  },
});
```

在已链接的分支上配置声明的存储桶：

```bash
neon deploy   # alias for `neon config apply`
```

## Neon 基础设施即代码（`neon.ts`）

上文的 `preview.buckets` 块是 `neon.ts` 的一部分——Neon 的基础设施即代码文件，一个 TypeScript 文件即可声明存储桶及分支应有的所有其他服务（完整参考请参见 `neon` 技能）。以 Terraform 的方式将声明与分支进行对账：

```bash
neon config status   # print the branch's live config (which buckets exist)
neon config plan     # dry-run diff of what apply would change
neon config apply    # create the declared buckets  (neon deploy is an alias)
```

存储桶是**分支作用域**的：当存在 `neon.ts` 时，`neon checkout` 在_创建_分支时即应用策略，因此新的预览/CI 分支启动时存储桶已配置完毕（并从父分支继承写时复制对象）。检出_已有_分支不会对其进行对账——需运行 `neon deploy` 来应用变更。配置操作（`config apply` / `deploy`）、`link` 和 `checkout` 还会将分支的 S3 凭证拉取到本地 `.env.local`，因此下文展示的 `env pull` 步骤在这些命令中会自动完成。

如需对注入的 S3 凭证进行类型化、校验后的访问，将同一配置对象传给 `@neon/env` 的 `parseEnv`——它返回从 `neon.ts` 派生的 `env.storage` 命名空间（`accessKeyId`、`secretAccessKey`、`endpoint`、`region`）。

## 环境变量

当声明了 `preview.buckets` 时，Neon 注入**AWS 标准** S3 环境变量，使 AWS SDK 无需额外配置即可从环境变量中工作。在已部署的 Neon Function 中这些变量自动注入；在本地，通过 CLI 将其拉取到磁盘（或在运行时注入）：

```bash
neon env pull            # writes the branch's vars into .env (or .env.local)
# or, without writing a file, inject at runtime:
neon-env run -- <your dev command>
```

| 变量                    | 含义                                               |
| ----------------------- | -------------------------------------------------- |
| `AWS_ACCESS_KEY_ID`     | S3 Access Key ID（分支凭证的 token id）            |
| `AWS_SECRET_ACCESS_KEY` | S3 Secret Access Key                               |
| `AWS_ENDPOINT_URL_S3`   | 分支 S3 端点 URL                                   |
| `AWS_REGION`            | 区域，例如 `us-east-2`                             |

由于变量名遵循 AWS 标准，AWS SDK 会自动从环境中获取凭证、端点和区域。凭证是分支作用域的，对该分支及其所有子分支有效。

## 操作对象：Files SDK（推荐）

读写对象最简单、最可移植的方式是使用 [Files SDK](https://files-sdk.dev) 及其 `neon` 适配器——一个基于 Web 标准 I/O 的轻量统一存储 API（`upload`、`download`、`url`、`list`、`exists`、`copy`、`delete`、`signedUploadUrl`）。它在底层使用 AWS S3 客户端，为 Neon 做了适当配置，并将错误重新标记为 `Neon error`——因此不会出现配置错误。优先使用此方案。

安装它及适配器内部使用的 AWS S3 对等依赖：

```bash
npm install files-sdk @aws-sdk/client-s3 @aws-sdk/s3-presigned-post @aws-sdk/s3-request-presigner
```

适配器从注入的 `AWS_*` 环境变量中解析端点、区域和凭证——只需传入存储桶名称：

```typescript
import { Files } from "files-sdk";
import { neon } from "files-sdk/neon";

const files = new Files({ adapter: neon({ bucket: "images" }) });

// Upload — body may be a Buffer, Uint8Array, Blob, File, ReadableStream, or string
await files.upload("generated/cat.jpg", fileBuffer, { contentType: "image/jpeg" });

// Download
const file = await files.download("generated/cat.jpg");
const bytes = new Uint8Array(await file.arrayBuffer());

// Presigned GET — share without exposing credentials (defaults to a 1h expiry)
const url = await files.url("generated/cat.jpg", { expiresIn: 3600 });

// Plus: files.exists(), files.list({ prefix }), files.copy(), files.delete(), files.signedUploadUrl()
```

更换适配器导入（`files-sdk/s3`、`files-sdk/r2`、`files-sdk/gcs` 等）后，其余代码无需修改。

## 操作对象：AWS S3 客户端（备选）

Neon 直接使用 S3 API，因此当你更偏好原生客户端或已依赖 AWS SDK 时，可以直接使用底层 SDK。凭证、端点和区域从标准 AWS 环境链中读取，唯一需要设置的参数是 `forcePathStyle: true`——Neon 要求路径风格寻址，因此 S3 客户端**必须**设置此项：

```typescript
import { S3Client } from "@aws-sdk/client-s3";

const s3 = new S3Client({
  forcePathStyle: true, // required: Neon uses path-style addressing
});
```

如果你更偏好类型化访问而非直接读取 `process.env`，`parseEnv`（来自 `@neon/env`）返回从 `neon.ts` 派生的、经过校验的 `env.storage` 命名空间（`accessKeyId`、`secretAccessKey`、`endpoint`、`region`）——参见 `neon` 技能。

然后使用原始命令对象进行上传、下载和预签名：

```typescript
import { PutObjectCommand, GetObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const BUCKET = "images";

// Upload
await s3.send(
  new PutObjectCommand({
    Bucket: BUCKET,
    Key: "generated/cat.jpg",
    Body: fileBuffer,
    ContentType: "image/jpeg",
  }),
);

// Download
const res = await s3.send(
  new GetObjectCommand({ Bucket: BUCKET, Key: "generated/cat.jpg" }),
);
const bytes = await res.Body?.transformToByteArray();

// Presigned GET — share without exposing credentials
const url = await getSignedUrl(
  s3,
  new GetObjectCommand({ Bucket: BUCKET, Key: "generated/cat.jpg" }),
  { expiresIn: 3600 },
);
```

在分支上将存储与数据库配对的典型模式：agent 生成图片 → `PutObject` 写入 `images` 存储桶 → Postgres 插入一行 → 读取时返回预签名 URL。在 Postgres 列中存储存储桶的 **key**（而非字节），读取时进行预签名。由于行和对象位于同一分支，它们一同分支且永不漂移。

`neon` 还提供一流的存储桶/对象命令（`neon bucket create|list|delete`、`neon bucket object put|get|list|delete`），用于脚本编写和一次性操作。

## 可用性

Neon 对象存储是一项预览（早期访问）功能，仅对 `us-east-2` 区域的新项目可用。继续操作前请确认用户的 Neon 项目是 `us-east-2` 的新项目；无法在现有项目上启用。如果用户尚未获得访问权限，请指向私有测试注册页面：https://neon.com/blog/were-building-backends#access

## Neon 文档

Neon 文档是权威信息源，且对象存储正在快速演进，因此务必对照官方文档进行验证。任何文档页面都可通过在 URL 后附加 `.md` 或请求 `Accept: text/markdown` 获取 Markdown 格式。从文档索引（https://neon.com/docs/llms.txt）和更新日志公告中找到正确的页面。

## 延伸阅读

- https://neon.com/docs/storage/overview.md
- https://neon.com/docs/storage/get-started.md
- https://neon.com/docs/storage/buckets.md
- https://neon.com/docs/storage/objects.md
- https://neon.com/docs/storage/authentication.md
- https://neon.com/docs/storage/s3-compatibility.md
- https://neon.com/docs/storage/troubleshooting.md
- https://files-sdk.dev — Files SDK 文档（`neon` 适配器）

## 限制

- 仅当任务明确匹配其上游产品或 API 范围时使用本技能。
- 在执行变更前，务必对照当前官方文档验证命令、API 行为、定价、配额、凭证和部署影响。
- 勿将生成的示例替代环境特定的测试、安全审查，或用户对破坏性或高成本操作的审批。
