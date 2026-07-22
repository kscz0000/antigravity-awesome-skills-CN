# 评估 — 技能是否真正路由到正确答案？

一个技能的好坏取决于智能体在真实问题下*找到并应用*正确条目的能力。这些评估分两个层级，针对一组固定的现实场景（[`cases.jsonl`](cases.jsonl)）进行测试，场景覆盖技能的两半内容（各平台族的远程 GPU 运维 + DL 训练调试层，包括 `convergence-debugging` 和 `data-pipeline` 文件）。

## 第 1 层 — 结构可达性（可运行，无需 API 密钥）

```bash
python evals/run_evals.py        # 任意用例回归则非零退出
```

对每个场景，它断言答案是**存在的、在文档记载的位置、包含预期的条目 ID / 关键词**：每个 `expect_files` 存在，每个 `expect_ids` 仍是该处的 `### <ID>` 标题，每个 `expect_grep` 术语仍在文本中。这是一个**漂移守卫** — 它能捕获被重命名/删除的条目、被移动的章节、被删除的文件，或事实被改写后丢失关键术语的情况。在 CI 中运行；只需 Python 3。

它**不能**证明：智能体确实*导航*到了那里（第 2 层），或者平台*事实*在真实机器上是正确的（见验证状态）。

## 第 2 层 — 智能体导航（金标准）

真正的测试：给一个**全新智能体**该技能和一个场景的 `prompt`，让它**仅从 SKILL.md 出发**导航（遵循文档记载的路由，而非盲目 grep），检查它是否在约 2 跳内到达一个正确的、具体的答案，覆盖该用例的 `must_cover` 要点。每个用例在 `agentic` 字段中记录了最近一次此类运行；收集的运行结果在 [`RESULTS.md`](RESULTS.md) 中。

用任意智能体/线束重新运行第 2 层：加载技能，粘贴用例 `prompt`，根据 `expect_files` / `expect_ids` / `must_cover` 对答案评分。（Anthropic 的技能最佳实践建议跨 Haiku/Sonnet/Opus 进行 ≥3 次评估 — 按模型重新运行这些用例是满足该标准的方式；迄今为止的结果是在开发模型上收集的，并已标注。）

## 添加用例

向 `cases.jsonl` 追加一行一个 JSON 对象：

```json
{"id": "kebab-id", "prompt": "the user's situation, verbatim-ish",
 "expect_files": ["references/training/<file>.md"], "expect_ids": ["O7"],
 "expect_grep": ["lr finder"], "must_cover": "the key points a correct answer must hit",
 "agentic": "PASS/FAIL (date): the navigation path observed"}
```

训练目录使用 `expect_ids`（它们有 `### O7 / DP1 / M17 …` 标题），平台配置使用 `expect_grep`（它们是章节结构的）。然后运行 `python evals/run_evals.py`。

## 验证状态（重要）

这些评估测试的是**技能内部的检索和路由** — 而非平台事实在真实实例上的真实性。仅 AutoDL 配置经过作者实战验证；其他六个平台配置基于官方文档 + 社区报告研究而得，**尚未经过实机验证**（见仓库 README 的"验证状态"和 `references/self-improvement.md` §5）。一个用例在此通过意味着"技能引导智能体到达*此文档记载的答案*"，而非"此答案在租用的机器上已被确认"。
