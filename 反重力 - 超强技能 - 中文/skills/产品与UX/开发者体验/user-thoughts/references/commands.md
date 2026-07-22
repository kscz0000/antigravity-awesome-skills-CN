# 命令参考

`user-thoughts` 同时接受 `/user-thoughts` 和 `/ustht`，两者等价。

## 命令汇总

| 命令 | 含义 |
|---|---|
| `/ustht init` | 在当前项目中初始化 `.ustht/`。 |
| `/ustht status` | 展示技能状态、即时状态、原始条数以及维度条数。 |
| `/ustht skill` | 展示 `SKILL_STATUS`。 |
| `/ustht skill on|off` | 启用或禁用写入操作。 |
| `/ustht instant` | 展示 `INSTANT_STATUS`。 |
| `/ustht instant on|off` | 启用或禁用即时捕获。 |
| `/ustht sortin [--dry]` | 将原始条目追加进 mdbase。 |
| `/ustht resort [--dry]` | 以语义方式重组所有 mdbase 内容。 |
| `/ustht raw` | 展示未处理的原始条目。 |
| `/ustht mdbase show [--all|--dimension]` | 展示索引、所有维度或单个维度。 |
| `/ustht mdbase export [--all|--dimension]` | 导出 mdbase 内容。 |
| `/ustht import <path>` | 从 markdown 文件导入与项目相关的决策。 |
| `/ustht ignore start|end` | 开始或结束一段临时忽略间隔。 |
| `/ustht ignore --last` | 移除最后一条原始条目并记录为已忽略。 |
| `/ustht ignore show` | 展示被忽略的条目。 |

## 自然语言映射

智能体可以将明确的用户意图映射为命令：

- "开启项目记忆" -> `/ustht skill on && instant on`
- "先别记录这条" -> `/ustht ignore start`
- "继续记录" -> `/ustht ignore end`
- "整理一下我说的话" -> `/ustht sortin`
- "展示你记住的内容" -> `/ustht mdbase show`
- "忽略最后一条" -> `/ustht ignore --last`

当意图不明确时，简短地提问澄清，不要去猜测。

## 串联命令

命令可以用 `&&` 串联，并应按从左到右的顺序执行。仅当某个命令失败且导致后续命令不安全时才停止。

示例：

```text
/ustht skill on && instant on && status
```

## 维度参数

维度名称必须通过校验：

- 仅小写字母、数字和连字符；
- 允许使用 `/` 表示子目录，例如 `ui/outline`；
- 不允许空格、`..`、反斜杠、绝对路径或保留名。