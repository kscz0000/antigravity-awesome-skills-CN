# 已知的技能检测位置

`detect_skills.py` 会扫描以下位置以发现未安装的技能：

## 默认位置（始终扫描）

| 位置 | 原因 |
|-------|--------|
| `%USERPROFILE%\Desktop` | 用户可能在桌面创建了技能 |
| `%USERPROFILE%\Downloads` | 从网络下载的技能 |
| `%USERPROFILE%\Documents` | 手动创建的文档中的技能 |
| `%TEMP%` | skill-creator 可能在临时目录留下工作区 |

## 扩展位置（使用 --all）

| 位置 | 原因 |
|-------|--------|
| `%USERPROFILE%` | 用户根目录 |
| `%USERPROFILE%\Projects` | 常见项目目录 |
| `%USERPROFILE%\dev` | 开发目录 |
| `%USERPROFILE%\repos` | Git 仓库 |
| `%USERPROFILE%\workspace` | 工作区 |
| `%USERPROFILE%\code` | 源代码目录 |
| `C:\temp` | 备用临时目录 |
| `C:\projects` | 根目录下的项目 |

## 识别模式

- `*-workspace/v*/skill/SKILL.md` — skill-creator 工作区
- 包含有效 YAML frontmatter 的 `SKILL.md` 的任意目录

## 忽略的位置

- `C:\Users\renat\skills\`（已安装）
- `.git/`、`__pycache__/`、`node_modules/`、`.venv/`、`venv/`
- 最大深度：5 层

## 添加新位置

要扫描特定位置：

```bash
python detect_skills.py --path "C:\meu\diretorio"
```
