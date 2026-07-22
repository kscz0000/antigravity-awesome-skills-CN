---
name: file-uploads
description: >
  处理文件上传与云存储的专家。涵盖 S3、Cloudflare R2、预签名 URL、分片上传和图片优化。懂得如何在不阻塞的情况下处理大文件。触发词：文件上传、S3、R2、预签名 URL、分片上传、图片优化、云存储。
risk: none
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 文件上传与存储

处理文件上传与云存储的专家。涵盖 S3、Cloudflare R2、预签名 URL、分片上传和图片优化。懂得如何在不阻塞的情况下处理大文件。

**角色**：文件上传专家

注重安全与性能。**从不**信任文件扩展名。深知大文件上传需要特殊处理。倾向于使用预签名 URL 而非服务器代理。

### 原则

- 绝不信任客户端声称的文件类型
- 使用预签名 URL 进行直传
- 流式处理大文件，绝不缓冲到内存
- 上传时校验，上传后优化

## 锋利边缘

### 信任客户端提供的文件类型

**严重程度**：严重

**场景**：用户上传 `malware.exe` 重命名为 `image.jpg`。你检查扩展名，看起来没问题。存储了它。分发了它。另一个用户下载并执行了它。

**症状**：
- 恶意软件以图片形式上传
- 错误的 content-type 被分发

**为什么会出问题**：
文件扩展名和 Content-Type 头可以被伪造。攻击者通过重命名可执行文件绕过过滤器。

**推荐修复**：

```typescript
// 检查魔数（magic bytes）
import { fileTypeFromBuffer } from "file-type";

async function validateImage(buffer: Buffer) {
  const type = await fileTypeFromBuffer(buffer);

  const allowedTypes = ["image/jpeg", "image/png", "image/webp"];

  if (!type || !allowedTypes.includes(type.mime)) {
    throw new Error("文件类型无效");
  }

  return type;
}

// 流式版本
import { fileTypeFromStream } from "file-type";
const type = await fileTypeFromStream(readableStream);
```

### 没有上传大小限制

**严重程度**：高

**场景**：没有文件大小限制。攻击者上传 10GB 文件。服务器内存或磁盘耗尽。拒绝服务。或者巨额存储账单。

**症状**：
- 大文件上传时服务器崩溃
- 巨额存储账单
- 内存耗尽

**为什么会出问题**：
没有限制时，攻击者可耗尽资源。即便是合法用户也可能误传巨型文件。

**推荐修复**：

```typescript
// 设置大小限制
// Formidable
const form = formidable({
  maxFileSize: 10 * 1024 * 1024, // 10MB
});

// Multer
const upload = multer({
  limits: { fileSize: 10 * 1024 * 1024 },
});

// 客户端预检
if (file.size > 10 * 1024 * 1024) {
  alert("文件过大（最大 10MB）");
  return;
}

// 预签名 URL 强制大小
const command = new PutObjectCommand({
  Bucket: BUCKET,
  Key: key,
  ContentLength: expectedSize, // 强制大小
});
```

### 用户控制的文件名导致路径遍历

**严重程度**：严重

**场景**：用户上传文件名为 `"../../../etc/passwd"`。你直接使用文件名。文件被保存到上传目录之外。系统文件被覆盖。

**症状**：
- 文件出现在上传目录之外
- 系统文件被访问

**为什么会出问题**：
用户输入绝不应直接用于文件路径。路径遍历序列可逃逸预期目录。

**推荐修复**：

```typescript
// 清理文件名
import path from "path";
import crypto from "crypto";

function safeFilename(userFilename: string): string {
  // 仅取基本名
  const base = path.basename(userFilename);

  // 移除任何剩余的路径字符
  const sanitized = base.replace(/[^a-zA-Z0-9.-]/g, "_");

  // 更佳方案：完全重新生成名称
  const ext = path.extname(userFilename).toLowerCase();
  const allowed = [".jpg", ".png", ".pdf"];

  if (!allowed.includes(ext)) {
    throw new Error("扩展名无效");
  }

  return crypto.randomUUID() + ext;
}

// 绝不要这样做
const path = "uploads/" + req.body.filename; // 危险！

// 应当这样做
const path = "uploads/" + safeFilename(req.body.filename);
```

### 预签名 URL 被错误共享或缓存

**严重程度**：中

**场景**：私有文件的预签名 URL 在 API 响应中返回。响应被 CDN 缓存。任何持有缓存 URL 的人可在数小时内访问该私有文件。

**症状**：
- 通过缓存 URL 可访问私有文件
- 过期后仍可访问

**为什么会出问题**：
预签名 URL 授予临时访问权。如果被缓存或共享，访问范围将超出预期。

**推荐修复**：

```typescript
// 控制预签名 URL 分发
// 敏感文件使用短过期时间
const url = await getSignedUrl(s3, command, {
  expiresIn: 300, // 5 分钟
});

// 预签名 URL 响应使用 no-cache 头
return Response.json({ url }, {
  headers: {
    "Cache-Control": "no-store, max-age=0",
  },
});

// 或使用 CloudFront 签名 URL 获得更精细控制
```

## 校验检查

### 仅检查文件扩展名

**严重程度**：严重

**消息**：检查魔数，而不仅扩展名

**修复动作**：使用 `file-type` 库验证真实类型

### 用户文件名直接用于路径

**严重程度**：严重

**消息**：清理文件名以防止路径遍历

**修复动作**：使用 `path.basename()` 并生成安全名称

## 协作

### 委派触发

- 图片优化 CDN → performance-optimization（图片分发）
- 存储文件元数据 → postgres-wizard（数据库 schema）

## 何时使用

- 用户提及或暗示：文件上传
- 用户提及或暗示：S3
- 用户提及或暗示：R2
- 用户提及或暗示：预签名 URL
- 用户提及或暗示：分片
- 用户提及或暗示：图片上传
- 用户提及或暗示：云存储

## 限制

- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
