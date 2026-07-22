# Battle Card — 格式规范

Battle 赛道是 deep/deeper 模式下的**第 6 个**子代理赛道。它在 Step 5c 事实核查完成之后运行 —— 仅读取已有 partials 和已事实核查的 `matrix.json`，**绝不发起新的 `browse cloud` 调用**。这是一个纯合成赛道。

输出文件：`{OUTPUT_DIR}/partials/{slug}.battle.md`。`merge_partials.mjs` 将其 `## Battle Card` 章节合并到汇总的 `{slug}.md` 中。`compile_report.mjs` 在每个竞品的 HTML 页面中将其渲染为带品牌强调色的卡片。

## 三个章节

### Landmines（3-5 项）

关于竞品的具体、可核实的事实，这些事实**会在交易中伤害他们**。每条都必须引用来自已有 partial（Mentions、Benchmarks 或 Research Findings）的 URL。优先使用第三方证据（基准测试、评论、新闻），而非竞品自己的营销——营销主张是软武器。

格式：
```
### Landmines

- **{one-line factual claim}** — {how an AE uses it in the call}. (source: {url})
```

示例：
```
- **Rival Co placed 4th of 7 on the Nov 2025 search-bench retrieval leaderboard (73% nDCG@10)** — use if prospect cares about relevance, but only after confirming their volume tier; Rival Co's reranking add-on is paywalled behind Scale ($499/mo). (source: https://github.com/example-org/search-bench)
```

### Objection Handlers（3-5 项）

格式："若客户说 X → 你回答 Y，引用来自 `userCompany.winningSummary` 的真实用户护城河"。每条回答必须引用事实核查矩阵确认用户拥有的功能/集成。绝不能用与事实核查矩阵单元格相矛盾的声明来回应。

格式：
```
### Objection Handlers

- If they say: "{objection verbatim}"
  You say: {response citing user's moat} (evidence: {url})
```

示例：
```
- If they say: "Rival Co is $99/mo cheaper than your Scale tier"
  You say: "Rival Co's reranking is a paid add-on you'll need for production relevance — once you add it the price gap closes. Our Scale tier includes neural reranking and a research endpoint; matrix.json confirms Rival Co's feature set doesn't cover the research API." (evidence: https://docs.rivalco.com/changelog)
```

### Talk Tracks（2-3 项）

1-2 句开场白，AE 可以背诵。以用户 winningSummary 中的差异化优势打头；点出竞品的具体短板。不夸大、不引用未在事实核查矩阵中落地的声明。

格式：
```
### Talk Tracks

1. {1-2 sentence pitch}
```

示例：
```
1. For production RAG, Exa is the only provider in the category with BOTH a first-party neural index AND a dedicated research/answer endpoint — Rival Co shipped neither, Serper shipped neither, and one competitor replaced its answer endpoint with a thin LLM wrapper last quarter.
```

## Markdown 文件形态

```markdown
---
competitor_name: Rival Co
lane: battle
generated_at: 2026-04-24
---

## Battle Card

### Landmines
- **Fact 1** — usage. (source: url)
- **Fact 2** — usage. (source: url)

### Objection Handlers
- If they say: "..."
  You say: ... (evidence: url)

### Talk Tracks
1. Pitch 1
2. Pitch 2
```

## 质量门槛 — 对抗性自查（子代理必须在写入前执行）

- [ ] 每个 landmine 引用的 URL 都出现在某个输入 partial（Mentions / Benchmarks / Research Findings）中。没有编造的 URL。
- [ ] 没有任何声明与 `matrix.json` 中已事实核查的单元格相矛盾（单元格必须包含 `sources` URL 才算可信）。
- [ ] 没有任何 talk track 声称用户拥有某项功能，而 `matrix.json` 显示 `userCompany.features[X] = false`。
- [ ] 异议是真实的——它们基于竞品最强营销话术，是潜在客户实际会提出的反对点，而非稻草人。
- [ ] 第三方证据优先于竞品自己的营销（基准、评论、新闻 > 他们的文档/定价）。

若某条潜在 landmine 在 partials 中找不到证据，则**省略**。发布 3 条有引用的 landmines 优于 5 条半编造的内容。