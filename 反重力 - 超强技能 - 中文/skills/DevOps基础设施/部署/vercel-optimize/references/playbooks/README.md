# 剧本

应用画像特定的建议，决定建议如何措辞和排序。剧本从不捏造声明——每条建议仍必须追溯到已验证的候选或发现。它们告诉推荐器当项目匹配某个画像时强调什么。

## 剧本如何被应用

1. 第 1 步检测项目的栈 + 依赖。
2. 推荐器启发式推断一个应用画像（从框架 + 依赖信号中最佳猜测）。
3. 匹配的剧本被包含在推荐器的上下文中。
4. 建议被塑形：排序倾向于画像的优先级列表；措辞倾向于画像特定的关注点。

## 画像检测（尽力而为的启发式）

| 信号 → | 画像 |
|---|---|
| `@vercel/sandbox`、`@ai-sdk/*`、`ai`、`openai`、`@anthropic-ai/sdk` 依赖 OR `usage.services` 中 AI Gateway / Sandbox SKU 激活 | `ai-application` |
| `stripe`、`@shopify/*`、`react-stripe-js`、"cart"/"checkout" 路由 | `ecommerce` |
| `next-auth`、`clerk`、仪表板路由、多租户头 | `saas` |
| 仅 `pages/api/**` 或 `app/api/**`，没有 UI 路由 | `api-service` |
| 大量 MDX / markdown，大多为静态路由 | `content-site` |
| 大量 `/(marketing)/` 路由组，A/B 测试依赖 | `marketing` |

`ai-application` 首先检查——AI 形态的客户常常与 SaaS/ecommerce 表面共享路由，但成本杠杆（AI Gateway 主导）和修复集合（提供者故障转移、sandbox 复用、OIDC 无密钥）属于该画像。

当检测不确定时，不应用任何剧本。推荐器在没有剧本的情况下也能正常工作——剧本是倾斜，不是必需。

## 剧本 schema

每个剧本都是一个具有固定形状的 Markdown 文件，以便推荐器能可靠地解析它。必需部分：

```markdown
# {Profile name}

## Typical billing shape
(Which dimensions dominate — e.g., "Edge Requests > Function Duration > Image Optimization")

## Priority patterns
(Ordered list of patterns this profile particularly benefits from)

## Frequent gotchas
(Anti-patterns specific to this profile)

## Cross-references
(Rec IDs from recommendations.md or rule names from vercel-react-best-practices)
```

## 贡献新剧本

1. 识别一个清晰的应用画像和一两个代表性的项目画像作为示例。
2. 创建匹配 schema 的 `references/playbooks/<profile>.md`。
3. 将检测信号添加到上表（启发式位于推荐器代码中；在此处文档化）。
4. 更新 `references/scoring.md` 中的剧本选择矩阵。
5. 运行 `node --test packages/vercel-optimize-tests/test/support-topics.test.mjs packages/vercel-optimize-tests/test/investigation-brief.test.mjs`。没有测试直接覆盖剧本（它们是内容），但 schema 验证器在 CI 中运行。