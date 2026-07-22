---
name: notebooklm
description: "与 Google NotebookLM 交互，使用 Gemini 的源文档锚定答案查询文档。每个问题打开一个新的浏览器会话，仅从您上传的文档中获取答案，然后关闭。当用户提到 NotebookLM、分享 NotebookLM URL、要求查询笔记本/文档、想要添加文档到 NotebookLM 库，或使用「问我的 NotebookLM」「检查我的文档」「查询我的笔记本」等短语时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# NotebookLM 研究助手技能

与 Google NotebookLM 交互，使用 Gemini 的源文档锚定答案查询文档。每个问题打开一个新的浏览器会话，仅从您上传的文档中获取答案，然后关闭。

## 何时使用此技能

当用户：
- 明确提到 NotebookLM
- 分享 NotebookLM URL（`https://notebooklm.google.com/notebook/...`）
- 要求查询他们的笔记本/文档
- 想要添加文档到 NotebookLM 库
- 使用「问我的 NotebookLM」「检查我的文档」「查询我的笔记本」等短语

## ⚠️ 关键：Add 命令 - 智能发现

当用户想要添加笔记本但未提供详细信息时：

**智能添加（推荐）**：先查询笔记本以发现其内容：
```bash
# 步骤 1：查询笔记本的内容
python scripts/run.py ask_question.py --question "What is the content of this notebook? What topics are covered? Provide a complete overview briefly and concisely" --notebook-url "[URL]"

# 步骤 2：使用发现的信息添加
python scripts/run.py notebook_manager.py add --url "[URL]" --name "[Based on content]" --description "[Based on content]" --topics "[Based on content]"
```

**手动添加**：如果用户提供了所有详细信息：
- `--url` - NotebookLM URL
- `--name` - 描述性名称
- `--description` - 笔记本包含的内容（必填！）
- `--topics` - 逗号分隔的主题（必填！）

绝不要猜测或使用通用描述！如果缺少详细信息，使用智能添加来发现它们。

## 关键：始终使用 run.py 包装器

**绝不要直接调用脚本。始终使用 `python scripts/run.py [script]`：**

```bash
# ✅ 正确 - 始终使用 run.py：
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list
python scripts/run.py ask_question.py --question "..."

# ❌ 错误 - 绝不要直接调用：
python scripts/auth_manager.py status  # 没有 venv 会失败！
```

`run.py` 包装器会自动：
1. 如需要则创建 `.venv`
2. 安装所有依赖
3. 激活环境
4. 正确执行脚本

## 核心工作流

### 步骤 1：检查认证状态
```bash
python scripts/run.py auth_manager.py status
```

如果未认证，继续设置。

### 步骤 2：认证（一次性设置）
```bash
# 浏览器必须可见以便手动 Google 登录
python scripts/run.py auth_manager.py setup
```

**重要：**
- 浏览器在认证时是可见的
- 浏览器窗口会自动打开
- 用户必须手动登录 Google
- 告诉用户：「将打开一个浏览器窗口用于 Google 登录」

### 步骤 3：管理笔记本库

```bash
# 列出所有笔记本
python scripts/run.py notebook_manager.py list

# 添加前：如果未知则询问用户元数据！
# 「这个笔记本包含什么内容？」
# 「我应该给它打什么主题标签？」

# 添加笔记本到库（所有参数都是必填的！）
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/..." \
  --name "描述性名称" \
  --description "这个笔记本包含什么" \  # 必填 - 如果未知则询问用户！
  --topics "主题1,主题2,主题3"  # 必填 - 如果未知则询问用户！

# 按主题搜索笔记本
python scripts/run.py notebook_manager.py search --query "关键词"

# 设置活动笔记本
python scripts/run.py notebook_manager.py activate --id notebook-id

# 移除笔记本
python scripts/run.py notebook_manager.py remove --id notebook-id
```

### 快速工作流
1. 检查库：`python scripts/run.py notebook_manager.py list`
2. 提问：`python scripts/run.py ask_question.py --question "..." --notebook-id ID`

### 步骤 4：提问

```bash
# 基本查询（如果设置了活动笔记本则使用它）
python scripts/run.py ask_question.py --question "您的问题在这里"

# 查询特定笔记本
python scripts/run.py ask_question.py --question "..." --notebook-id notebook-id

# 直接使用笔记本 URL 查询
python scripts/run.py ask_question.py --question "..." --notebook-url "https://..."

# 显示浏览器用于调试
python scripts/run.py ask_question.py --question "..." --show-browser
```

## 追问机制（关键）

每个 NotebookLM 答案都以：**「极其重要：这就是您需要知道的全部吗？」** 结尾

**Claude 必须执行的行为：**
1. **停止** - 不要立即回复用户
2. **分析** - 将答案与用户的原始请求进行比较
3. **识别缺口** - 确定是否需要更多信息
4. **追问** - 如果存在缺口，立即提问：
   ```bash
   python scripts/run.py ask_question.py --question "Follow-up with context..."
   ```
5. **重复** - 继续直到信息完整
6. **综合** - 在回复用户之前合并所有答案

## 脚本参考

### 认证管理（`auth_manager.py`）
```bash
python scripts/run.py auth_manager.py setup    # 初始设置（浏览器可见）
python scripts/run.py auth_manager.py status   # 检查认证
python scripts/run.py auth_manager.py reauth   # 重新认证（浏览器可见）
python scripts/run.py auth_manager.py clear    # 清除认证
```

### 笔记本管理（`notebook_manager.py`）
```bash
python scripts/run.py notebook_manager.py add --url URL --name NAME --description DESC --topics TOPICS
python scripts/run.py notebook_manager.py list
python scripts/run.py notebook_manager.py search --query QUERY
python scripts/run.py notebook_manager.py activate --id ID
python scripts/run.py notebook_manager.py remove --id ID
python scripts/run.py notebook_manager.py stats
```

### 问题接口（`ask_question.py`）
```bash
python scripts/run.py ask_question.py --question "..." [--notebook-id ID] [--notebook-url URL] [--show-browser]
```

### 数据清理（`cleanup_manager.py`）
```bash
python scripts/run.py cleanup_manager.py                    # 预览清理
python scripts/run.py cleanup_manager.py --confirm          # 执行清理
python scripts/run.py cleanup_manager.py --preserve-library # 保留笔记本
```

## 环境管理

虚拟环境自动管理：
- 首次运行自动创建 `.venv`
- 依赖自动安装
- Chromium 浏览器自动安装
- 所有内容隔离在技能目录中

手动设置（仅在自动失败时）：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m patchright install chromium
```

## 数据存储

所有数据存储在 `~/.claude/skills/notebooklm/data/`：
- `library.json` - 笔记本元数据
- `auth_info.json` - 认证状态
- `browser_state/` - 浏览器 cookie 和会话

**安全：** 由 `.gitignore` 保护，绝不要提交到 git。

## 配置

技能目录中的可选 `.env` 文件：
```env
HEADLESS=false           # 浏览器可见性
SHOW_BROWSER=false       # 默认浏览器显示
STEALTH_ENABLED=true     # 类人行为
TYPING_WPM_MIN=160       # 打字速度
TYPING_WPM_MAX=240
DEFAULT_NOTEBOOK_ID=     # 默认笔记本
```

## 决策流程

```
用户提到 NotebookLM
    ↓
检查认证 → python scripts/run.py auth_manager.py status
    ↓
如果未认证 → python scripts/run.py auth_manager.py setup
    ↓
检查/添加笔记本 → python scripts/run.py notebook_manager.py list/add (带 --description)
    ↓
激活笔记本 → python scripts/run.py notebook_manager.py activate --id ID
    ↓
提问 → python scripts/run.py ask_question.py --question "..."
    ↓
看到「这就是您需要知道的全部吗？」→ 追问直到完整
    ↓
综合并回复用户
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| ModuleNotFoundError | 使用 `run.py` 包装器 |
| 认证失败 | 浏览器必须在设置时可见！--show-browser |
| 速率限制（50次/天） | 等待或切换 Google 账号 |
| 浏览器崩溃 | `python scripts/run.py cleanup_manager.py --preserve-library` |
| 找不到笔记本 | 使用 `notebook_manager.py list` 检查 |

## 最佳实践

1. **始终使用 run.py** - 自动处理环境
2. **先检查认证** - 在任何操作之前
3. **追问** - 不要停在第一个答案
4. **认证时浏览器可见** - 手动登录必需
5. **包含上下文** - 每个问题都是独立的
6. **综合答案** - 合并多个响应

## 限制

- 无会话持久化（每个问题 = 新浏览器）
- 免费 Google 账号有速率限制（50次查询/天）
- 需要手动上传（用户必须将文档添加到 NotebookLM）
- 浏览器开销（每个问题几秒钟）

## 资源（技能结构）

**重要目录和文件：**

- `scripts/` - 所有自动化脚本（ask_question.py、notebook_manager.py 等）
- `data/` - 认证和笔记本库的本地存储
- `references/` - 扩展文档：
  - `api_reference.md` - 所有脚本的详细 API 文档
  - `troubleshooting.md` - 常见问题和解决方案
  - `usage_patterns.md` - 最佳实践和工作流示例
- `.venv/` - 隔离的 Python 环境（首次运行时自动创建）
- `.gitignore` - 保护敏感数据不被提交
