# 智能体导航结果（第 2 层）

每行：一个**全新智能体**被给予该技能和一个来自 [`cases.jsonl`](cases.jsonl) 的场景 `prompt`，要求**仅从 SKILL.md 出发**导航（遵循文档记载的路由，禁止盲目 grep），并评估它是否在约 2 跳内到达了一个正确的、具体的答案，覆盖该场景的 `must_cover` 要点。

**方法论 / 诚实声明**（以便读者正确权重这些结果）：
- 迄今为止的运行是**在开发期间**收集的，使用开发模型（Claude Opus 级别），作为子智能体调度 — 不是独立第三方，也**尚未**进行 Anthropic 最佳实践所推荐的 Haiku/Sonnet/Opus 扫描。请视为*作者自运行的冒烟评估*，而非中立基准。
- 这些证明了技能内部的**路由 + 检索**，而非平台事实在真实机器上的真实性（仅 AutoDL 经过实战验证 — 见仓库 README 的"验证状态"）。
- 每个场景仅运行一次；尚无对抗性/变体措辞测试。

## 结果 — 2026-06

| 场景 | 判定 | 跳数 | 观察到的导航路径 |
|---|---|---|---|
| convergence-frozen-resnet | **通过** | 1 | SKILL.md "When training breaks" → `convergence-debugging.md` O1（单批次过拟合）+ O2（参数不在优化器中）+ O17（冻结但仍在优化器中）+ O18（冻结 BN 漂移）+ O6（Adam vs AdamW） |
| data-worker-rng-dup | **通过** | 1 | SKILL.md "When training breaks" → `data-pipeline.md` DP1（numpy fork-RNG 重复；worker_init_fn 修复） |
| oom-on-step-2 | **通过** | ≤2 | SKILL.md "When training breaks" → `oom-memory.md`（适配阶梯 + step-2 OOM / Adam 惰性状态） |
| nccl-one-rank-hang | **通过** | ≤2 | SKILL.md → `distributed-launch.md`（反同步工具包 D19 / 单 rank 脱离 D20） |
| diffusion-loss-low-samples-bad | **通过** | ≤2 | SKILL.md → `by-domain.md` 扩散章节（DF1 loss≠质量，DF2 EMA 权重） |
| nan-loss-spike-bf16 | **通过** | ≤2 | SKILL.md "When training breaks" → `precision-stability.md` P8/P12/P15（NaN 来源 + warmup 尖峰 + z-loss） |
| resume-epoch-reset | **通过** | 1 | SKILL.md → `checkpoint-resume.md` C1/C12/C14（保存完整状态：epoch/step/scheduler/RNG/scaler） |
| throughput-gpu-starved | **通过** | ≤2 | SKILL.md → `throughput-profiling.md` T1/T4（GPU 受限 vs 数据受限；num_workers/prefetch） |
| runpod-spot-resume-teardown | **通过** | ≤2 | SKILL.md → `profiles/runpod.md` §4/§5 → `spot-resilience.md` → `checkpoint-resume.md` C3 |
| vastai-teardown-billing | **通过** | ≤2 | SKILL.md → `profiles/vastai.md` §5 → `lifecycle_checklist.md` Phase 5 |
| autodl-inode-disk-full | **通过** | ≤2 | SKILL.md → inode/磁盘陷阱（原则 #5 / `gotchas_universal.md` U7） |
| china-hf-download-stall | **通过** | ≤2 | SKILL.md → `references/china-network.md`（HF_ENDPOINT=hf-mirror，hf_transfer 注意事项） |
| lambda-stop-vs-terminate | **通过** | ≤2 | SKILL.md → `profiles/lambda.md`（无停止状态；terminate 不可逆） |
| autodl-first-contact-15day | **通过** | 1 | SKILL.md 原则 #10 → `profiles/autodl.md` Surface 阻断 + AD-DANGER（关机 15 天后自动释放） |

**汇总：14/14 场景路由正确**（9 个经由工作流 `w2r1t7mm9`，5 个独立运行），每个均在 ≤2 跳内到达正确且具体的答案。第 1 层结构检查（`run_evals.py`）运行全部 14 个用例，是 CI 中保持绿色的回归守卫。

## 已知缺口（这些结果尚未覆盖的内容）

- 无多模型扫描（Haiku/Sonnet/Opus）— 声称达到最佳实践测试标准所必需。
- 无对抗性/改写提示词（例如用户用非标准措辞描述症状）。
- 无实机平台验证（智能体检索的事实是否正确 — 即验证状态说明中的注意事项）。
