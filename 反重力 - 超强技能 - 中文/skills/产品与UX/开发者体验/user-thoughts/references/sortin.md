# Sortin 与 Resort 算法

本文档描述原始想法如何转化为有组织的 mdbase 记录。

## 命令

| 命令 | 行为 |
|---|---|
| `/ustht sortin` | 软维护：将新的原始条目追加进 mdbase，不重组现有内容。 |
| `/ustht resort` | 硬维护：审查所有 mdbase 内容，去重、重新分类、合并并更新索引。 |
| `--dry` | 预览将要执行的变更，但不实际写入。 |

## 原始格式

处理前：

```text
- [14:30] Make buttons use 8px radius | suggested-dim:ui/details
- [14:45] Login should use a dark theme | suggested-dim:ui/outline
- [15:10] Use REST APIs, not GraphQL | suggested-dim:dev-stack
```

处理后，文件首行变为：

```text
<!-- processed -->
```

## 软追加格式

原始条目会按日期标题追加到所选维度文件中：

```markdown
## 2026-06-01

- Make buttons use 8px radius
```

规则：

- 保留原始措辞。
- 仅去掉时间戳与 `suggested-dim` 后缀。
- 按原始文件的日期对条目分组。
- 若已存在对应日期小节，则追加到该小节下。
- 如不存在，则新建日期小节。

## 维度管理

仅当想法无法归入现有维度时才创建新维度。维度名必须是 kebab-case 路径段，并必须通过安全校验。

`resort` 发现重叠的维度时，应合并到最清晰的目标维度，并保留来源信息。当某维度不再有用时，将其标记为 `<!-- deprecated -->`，而不是直接删除。

## 分类优先级

1. 用户指定的维度。
2. 与现有维度精确匹配。
3. 语义上最接近的现有维度；若契合度较弱，应加注说明。
4. 兜底放入 `general.md`。

## 导入算法

`/ustht import <path>` 会扫描安全项目本地路径下的 markdown 文件，抽取与项目相关的用户决策、约束和需求。它不应修改源文件。导入的条目应包含来源标记，例如 `[source:docs/design.md]`。

除非明确包含用户决策，否则应跳过普通的技术文档、自动生成的文档、API 参考文本和代码注释。

## 汇总输出

`sortin` 完成后，应汇报已处理的条目数量与目标维度，例如：

```text
Soft maintenance complete. Processed 3 thoughts:
  -> ui/details.md: +1
  -> ui/outline.md: +1
  -> dev-stack.md: +1
LAST_SORTIN updated to 2026-06-01 15:30
```
