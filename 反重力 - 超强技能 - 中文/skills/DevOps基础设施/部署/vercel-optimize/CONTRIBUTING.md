# 为 `vercel-optimize` 贡献

保持改动小、以指标为基础、并使用固定数据进行测试。运行时代码位于 `skills/vercel-optimize`；测试和固定数据位于 `packages/vercel-optimize-tests`，以保持已安装的技能小巧。

## 常见改动

| 改动 | 编辑位置 | 测试 |
|---|---|---|
| 闸门 | `lib/gates/<id>.mjs`、`lib/gates/index.mjs` | `node --test packages/vercel-optimize-tests/test/*gate*.test.mjs` |
| 扫描器 | `lib/scanners/<id>.mjs`、`lib/scanners/index.mjs` | `packages/vercel-optimize-tests/test/` 中对应的扫描器测试 |
| 引用 | `references/docs-library.json` | `node skills/vercel-optimize/scripts/check-citations.mjs` |
| 支持主题 | `references/support-topics/<id>.md` | `node --test packages/vercel-optimize-tests/test/support-topics.test.mjs` |
| 剧本 | `references/playbooks/<profile>.md` 以及 `references/scoring.md` 中的选择矩阵 | `node --test packages/vercel-optimize-tests/test/support-topics.test.mjs packages/vercel-optimize-tests/test/investigation-brief.test.mjs` |
| 渲染器或验证器 | `lib/render-report.mjs`、`lib/verify-claim.mjs` 或相关模块 | 专项测试加完整测试套件 |

生成文档：

```bash
node skills/vercel-optimize/scripts/build-docs.mjs
node skills/vercel-optimize/scripts/check-docs-fresh.mjs
```

完整测试循环：

```bash
node --test packages/vercel-optimize-tests/test/*.test.mjs
node skills/vercel-optimize/scripts/check-docs-fresh.mjs
node skills/vercel-optimize/scripts/check-citations.mjs
```

## 规则

- 无运行时依赖。脚本仅使用 Node.js 20+ 内置模块和 Vercel CLI。
- 没有 Vercel 指标信号、提出代码改动时的代码证据、以及白名单引用，就不要给出建议。
- 不要杜撰 URL、精确节省金额、或版本不匹配的框架 API。
- 固定数据中不得包含内部仓库路径、服务名、客户名或捕获的私有输出。
- 生成的报告文案保持面向客户。调试细节放在 `--debug-out` 之后。

## 输出契约

每个输出 JSON 的脚本都必须确定性：键顺序稳定、排序稳定、2 空格缩进、文件末尾换行。如果消费的 schema 发生变更，请在同一个 PR 中更新 schema 版本和固定数据测试。