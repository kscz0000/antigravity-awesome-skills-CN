# 运行时一致性方法

运行时一致性把平台兼容性从打包后的补救事项变成发布门槛。

## 用途

当技能被打包到 OpenAI、Claude、Agent Skills、VS Code / Copilot 或通用目标时使用此检查。目的不是证明每个运行时表现完全一致，而是证明该软件包暴露了足够多的元数据、文件和降级说明，以便每个运行时都能安全地消费它。

## V0 检查项

- `SKILL.md` 存在且包含 frontmatter 中的 `name` 与 `description`。
- `description` 长度不超过常见 Agent Skills 客户端使用的 1024 字符限制。
- `manifest.json` 包含 name、version、owner、maturity、status、review cadence 和 target platforms。
- `agents/interface.yaml` 包含展示文本、默认提示词、激活模式、执行上下文、信任元数据、适配器目标和降级策略。
- 技能 IR 存在且与 frontmatter 的 name 和 description 一致。
- 由 Skill IR 命名的资源使用相对路径,且能在软件包内解析到。
- 不被支持或存在信息损失的目标行为用降级说明表示。

## 评审门控

评审者应当能够看到一张目标矩阵,包含通过/失败状态、失败项、警告和产物路径。任何目标失败都会阻塞该目标在 library、governed 或团队分发通道下的发布。