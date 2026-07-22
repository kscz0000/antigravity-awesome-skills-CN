# 详细提取协议

压缩前从会话中提取所有关键信息的分步指南。按顺序执行——每一节都依赖前一节。

## 第一步：文件清单

列出所有以下文件：
- **已创建**：绝对路径、用途、大致大小
- **已修改**：路径、变更节（行号）、变更性质
- **已读取**（作为参考）：路径、读取原因、提取的信息
- **已删除**：路径、原因

格式：

```markdown
### 接触过的文件
| 文件 | 操作 | 详情 |
|---------|------|----------|
| C:\path\file.py | EDIT L40-119 | 向 CAPABILITY_KEYWORDS 添加了 5 个类别 |
| C:\path\new.md | CREATE | 含 14 个模块的新技能 |
| C:\path\old.bak | DELETE | 过时的备份 |
```

## 第二步：决策及其原因

针对会话中做出的每个技术决策：

```markdown
### 决策
- **决策内容**: [决策描述]
  **原因**: [技术原因]
  **放弃的替代方案**: [未选择的选项及原因]
  **影响**: [该决策改变了什么]
```

决策包括：技术选型、代码模式、架构、命名约定、测试策略、任务优先级。

## 第三步：缺陷与修复

针对每个发现并修复的缺陷：

```markdown
### 修复
- **症状**: [缺陷如何表现]
  **根因**: [为何会发生]
  **文件**: [路径:行号]
  **修复**: [所做的事情，如相关附 1-2 行代码]
  **验证**: [如何确认已修复]
```

## 第四步：进度状态

```markdown
### 进度
- 任务总数：X
- 已完成：Y（列表）
- 进行中：Z（列表含 % 与下一步）
- 待办：W（列表含优先级与依赖）
- 阻塞：V（列表含阻塞原因）
```

## 第五步：关键代码

对理解项目至关重要的代码片段。不要复制整个文件——只复制能代表决策或非显而易见逻辑的片段。

```markdown
### 关键片段
**match_skills.py:40-119** — 能力类别：
- legal：约 70 个关键字，覆盖巴西法律的全部领域
- auction：司法/司法外拍卖
- security：owasp、渗透测试、漏洞
- image-generation：stable diffusion、comfyui、midjourney
- monitoring：health、status、audit、sentinel
```

## 第六步：模式与约定

```markdown
### 观察到的模式
- [模式]：[描述] — [适用位置]
```

示例："ZIP 必须包含 {skill-name}/ 与 .claude/skills/{skill-name}/"，"SQL 使用 ? 占位符，绝不用 f-string"，"令牌用 [:8]...masked 掩码"。

## 第七步：关键依赖

并非显而易见的组件间连接：

```markdown
### 依赖
- scan_registry.py CAPABILITY_MAP === match_skills.py CAPABILITY_KEYWORDS
  （必须完全一致，否则匹配会失效）
- SKILL.md frontmatter 必须包含：name、version、description
  （scan_registry.py 校验这些字段）
```

## 第八步：用户上下文

```markdown
### 上下文
- 用户目标：[宏观上想达成什么]
- 技术水平：[如何交互、使用哪些术语]
- 偏好：[语言、格式、详细程度]
- 预期下一步：[用户可能要求的动作]
```

## 最终快照格式

文件 `snapshot-YYYYMMDD-HHMMSS.md` 必须按上述顺序包含全部节，并以头部开头：

```markdown
# Context Guardian 快照 — YYYY-MM-DD HH:MM:SS
**会话**: [标识符或 slug]
**项目**: [项目名]
**模型**: [claude-opus-4-6 等]
**上下文已消耗**: ~X%（估算）

[第一步到第八步的全部节]

---
*快照由 context-guardian v1.0.0 生成*
*恢复方式：读取本文件 + MEMORY.md + context_manager.py load*
```
