# Claude 模型目录

**仅使用本文件中列出的确切模型 ID。** 切勿猜测或构造模型 ID — 错误的 ID 会导致 API 错误。尽可能使用别名。获取最新信息，请 WebFetch `shared/live-sources.md` 中的 Models Overview URL。

## 当前模型（推荐）

| Friendly Name     | Alias (use this)    | Full ID                       | Context        | Max Output | Status |
|-------------------|---------------------|-------------------------------|----------------|------------|--------|
| Claude Opus 4.6   | `claude-opus-4-6`   | —                             | 200K (1M beta) | 128K       | Active |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | -                             | 200K (1M beta) | 64K        | Active |
| Claude Haiku 4.5  | `claude-haiku-4-5`  | `claude-haiku-4-5-20251001`   | 200K           | 64K        | Active |

### 模型描述

- **Claude Opus 4.6** — 我们最智能的模型，用于构建 Agent 和编码。支持自适应思考（推荐）、128K 最大输出 token（大输出需要流式传输）。通过 `context-1m-2025-08-07` 请求头可在 beta 中使用 1M 上下文窗口。
- **Claude Sonnet 4.6** — 速度和智能的最佳组合。支持自适应思考（推荐）。通过 `context-1m-2025-08-07` 请求头可在 beta 中使用 1M 上下文窗口。64K 最大输出 token。
- **Claude Haiku 4.5** — 最快、最具成本效益的模型，适用于简单任务。

## 旧模型（仍活跃）

| Friendly Name     | Alias (use this)    | Full ID                       | Status |
|-------------------|---------------------|-------------------------------|--------|
| Claude Opus 4.5   | `claude-opus-4-5`   | `claude-opus-4-5-20251101`    | Active |
| Claude Opus 4.1   | `claude-opus-4-1`   | `claude-opus-4-1-20250805`    | Active |
| Claude Sonnet 4.5 | `claude-sonnet-4-5` | `claude-sonnet-4-5-20250929`  | Active |
| Claude Sonnet 4   | `claude-sonnet-4-0` | `claude-sonnet-4-20250514`    | Active |
| Claude Opus 4     | `claude-opus-4-0`   | `claude-opus-4-20250514`      | Active |

## 已弃用模型（即将退役）

| Friendly Name     | Alias (use this)    | Full ID                       | Status     |
|-------------------|---------------------|-------------------------------|------------|
| Claude Haiku 3    | —                   | `claude-3-haiku-20240307`     | Deprecated |

## 已退役模型（不再可用）

| Friendly Name     | Full ID                       | Retired     |
|-------------------|-------------------------------|-------------|
| Claude Sonnet 3.7 | `claude-3-7-sonnet-20250219`  | Feb 19, 2026 |
| Claude Haiku 3.5  | `claude-3-5-haiku-20241022`   | Feb 19, 2026 |
| Claude Opus 3     | `claude-3-opus-20240229`      | Jan 5, 2026 |
| Claude Sonnet 3.5 | `claude-3-5-sonnet-20241022`  | Oct 28, 2025 |
| Claude Sonnet 3.5 | `claude-3-5-sonnet-20240620`  | Oct 28, 2025 |
| Claude Sonnet 3   | `claude-3-sonnet-20240229`    | Jul 21, 2025 |
| Claude 2.1        | `claude-2.1`                  | Jul 21, 2025 |
| Claude 2.0        | `claude-2.0`                  | Jul 21, 2025 |

## 解析用户请求

当用户按名称请求模型时，使用此表查找正确的模型 ID：

| User says...                              | Use this model ID              |
|-------------------------------------------|--------------------------------|
| "opus", "most powerful"                   | `claude-opus-4-6`              |
| "opus 4.6"                                | `claude-opus-4-6`              |
| "opus 4.5"                                | `claude-opus-4-5`              |
| "opus 4.1"                                | `claude-opus-4-1`              |
| "opus 4", "opus 4.0"                      | `claude-opus-4-0`              |
| "sonnet", "balanced"                      | `claude-sonnet-4-6`            |
| "sonnet 4.6"                              | `claude-sonnet-4-6`            |
| "sonnet 4.5"                              | `claude-sonnet-4-5`            |
| "sonnet 4", "sonnet 4.0"                  | `claude-sonnet-4-0`            |
| "sonnet 3.7"                              | Retired — suggest `claude-sonnet-4-5` |
| "sonnet 3.5"                              | Retired — suggest `claude-sonnet-4-5` |
| "haiku", "fast", "cheap"                  | `claude-haiku-4-5`             |
| "haiku 4.5"                               | `claude-haiku-4-5`             |
| "haiku 3.5"                               | Retired — suggest `claude-haiku-4-5` |
| "haiku 3"                                 | Deprecated — suggest `claude-haiku-4-5` |
