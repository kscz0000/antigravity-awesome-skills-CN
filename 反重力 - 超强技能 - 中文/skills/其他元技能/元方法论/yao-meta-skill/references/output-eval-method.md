# Output Eval Method

Output Eval Lab 证明一个技能是否提升了最终面向用户的结果，而不仅是是否正确路由。

## When To Use

对 production、library、governed 或团队分发的技能使用 output evals。scaffold 类技能可以先从一个 smoke 用例起步，但 production 及以上应在晋升前展示 with-skill 相对 baseline 的正向信号。

## Case Design

每个用例应包含：

- 真实的 prompt 或任务形态
- 任何必需的输入文件
- baseline 输出，代表不使用技能完成该任务的结果
- with-skill 输出，代表技能引导下的行为
- 可在不靠主观猜测的前提下检查的断言
- 可选的 human review 备注，用于风格、完整性或判断

## Assertion Rules

优先选择能抓住实质质量的断言：

- 必需的交付物路径
- 必需的章节或契约
- 必需的边界或排除用语
- 必需的证据路径
- 禁止的通用占位符
- 禁止的不安全动作

避免只奖励措辞记忆的断言。如果一个用例能靠复读一句话通过却没完成实际工作，这条断言就太窄了。

## Score Reading

第一版 v0 评分卡报告：

- baseline pass rate
- with-skill pass rate
- absolute delta
- 失败断言及其失败分类
- 当生成 `reports/output_execution_runs.md` 时的执行模式、用时与 token 证据
- 盲评 A/B 复核包数量
- 推荐的下一步修复

production 晋升应要求 with-skill pass rate 优于 baseline，并对每条失败断言给出解释。

## Execution Evidence

在评分卡之后运行执行证据：

```bash
python3 scripts/yao.py output-exec
```

默认情况下，这会把当前用例输出记为 `recorded_fixture`。这有利于复现，但不是模型执行证据。要采集真实的运行证据，需传入 `--runner-command` 加一条命令或 JSON 字符串列表。runner 从 stdin 接收 JSON 请求，并应返回包含以下字段的 JSON：

- `output`
- 可选 `execution_kind`：`command` 或 `model`
- 可选 `provider` 和 `model`
- 可选 `usage.input_tokens`、`usage.output_tokens` 和 `usage.total_tokens`

只有返回了 provider/model 元数据或 `execution_kind: "model"` 的运行，才应计为模型执行。若缺少 token 用量，报告可估算 token，但必须标注为估算值。

在没有外部模型凭据的情况下，要做本地发布门 smoke 证据，请使用确定性 runner：

```bash
python3 scripts/yao.py output-exec --runner-command '["python3","scripts/local_output_eval_runner.py"]'
```

它验证 command-runner 契约、用时采集、评分路径与失败处理。不应把它描述为 provider 支持的模型证据。

要做 provider 支持的证据，请使用打包好的 provider runner 并配真实凭据：

```bash
YAO_OUTPUT_EVAL_MODEL=gpt-4.1-mini \
OPENAI_API_KEY=... \
python3 scripts/yao.py output-exec --provider-runner openai
```

provider runner 调用兼容 OpenAI Responses API 的端点，相对 `evals/output/` 读取输入文件，返回 `execution_kind: "model"`，并在 provider 返回 usage 字段时记录观测到的 token 用量。若缺少 API key 或 model，runner 必须失败，不得回退到 fixture 或假装存在模型证据。`--provider-base-url` 仅可用于已审核的兼容端点；非默认 HTTPS 主机需要 `--allow-custom-base-url`，明文 HTTP 仅在本地测试服务器场景下配合 `--allow-insecure-localhost` 才允许。

## Blind A/B Review

每次 output eval 运行还应生成：

- `reports/output_blind_review_pack.md`
- `reports/output_blind_review_pack.json`
- `reports/output_blind_answer_key.json`

复核包必须隐藏 Variant A 或 Variant B 究竟来自 baseline 还是技能引导输出。answer key 是独立的审计证据，应仅在评审者已做出判断后再打开。

## Reviewer Adjudication

盲评结束后，在 `reports/output_review_decisions.json` 中记录评审者选择，包含 `reviewer`、`reviewed_at`、`winner_variant`、可选的 `confidence` 与必需的基于评分标准的 `reason`，然后运行：

```bash
python3 scripts/adjudicate_output_review.py --write-template
python3 scripts/yao.py output-review
```

裁定报告会写入：

- `reports/output_review_decisions.json`
- `reports/output_review_adjudication.json`
- `reports/output_review_adjudication.md`

当不存在评审者决策时，报告应说明用例处于 pending 状态，Review Studio 应链接到决策模板。不要把 pending 用例算作人类一致。只有具备评审者元数据且 `reason` 非空的真实 `winner_variant` 为 `A` 或 `B` 的决策，才应纳入一致率、不一致计数和评审判断计数。

裁定报告必须保持盲评完整性：pending 和无效决策应将 expected winner 显示为隐藏。仅当某用例存在带理由的有效评审者决策后，才可揭示 `expected_winner_variant`。

## Anti-Overfitting

保留一个小型公共 smoke 集和一个独立的 holdout 集。把真实失败轮换加入分类法，而不是只去编辑那条失败的 prompt。只要输出看起来不错但边界仍不清楚，就补充近邻用例。
