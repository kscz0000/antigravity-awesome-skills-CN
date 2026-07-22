---
name: linkedin-cli
description: "通过 CLI 自动化 LinkedIn 操作：获取档案、搜索人员/公司、发送消息、管理人脉、创建帖子和 Sales Navigator。当用户要求'LinkedIn自动化'、'获取LinkedIn档案'、'搜索LinkedIn'、'发送LinkedIn消息'、'管理LinkedIn人脉'、'创建LinkedIn帖子'、'LinkedIn CLI'时使用。"
risk: safe
source: community
date_added: "2026-02-27"
---

## 何时使用
需要通过 CLI 自动化 LinkedIn 任务时使用，如获取档案、管理人脉、创建帖子，尤其适用于集成到自动化工作流中。

# LinkedIn 技能

你可以使用 `linkedin`——一个 LinkedIn 自动化 CLI 工具。支持获取档案、搜索人员和公司、发送消息、管理人脉、创建帖子、点赞、评论等。

每条命令向 Linked API 发送请求，后者在云端运行真实浏览器执行操作。操作**并非即时**——根据复杂度，预计需要 30 秒到数分钟。

如果 `linkedin` 不可用，安装：

```bash
npm install -g @linkedapi/linkedin-cli
```

## 认证

如果命令以退出码 2 失败（认证错误），请用户设置账户：

1. 前往 [app.linkedapi.io](https://app.linkedapi.io) 注册或登录
2. 关联 LinkedIn 账户
3. 从控制台复制 **Linked API Token** 和 **Identification Token**

用户提供令牌后，运行：

```bash
linkedin setup --linked-api-token=TOKEN --identification-token=TOKEN
```

## 何时使用
需要**从脚本或 AI 智能体编排 LinkedIn 操作**而非在网页界面点击时使用：

- 构建依赖 LinkedIn 数据和消息的外联、调研或招聘工作流。
- 批量获取人员和公司档案以丰富线索或客户信息。
- 协调多步骤 Sales Navigator 或工作流运行，需要 JSON 输出和退出码。

使用自动化操作真实账户时，务必遵守 LinkedIn 服务条款、当地法规和组织合规政策。

## 全局标志

始终使用 `--json` 和 `-q` 获取机器可读输出：

```bash
linkedin <command> --json -q
```

| 标志                    | 说明                             |
| ----------------------- | -------------------------------- |
| `--json`                | 结构化 JSON 输出                 |
| `--quiet` / `-q`        | 抑制 stderr 进度消息             |
| `--fields name,url,...` | 选择输出中的特定字段             |
| `--no-color`            | 禁用颜色                         |
| `--account "Name"`      | 使用指定账户执行命令             |

## 输出格式

成功：

```json
{ "success": true, "data": { "name": "John Doe", "headline": "Engineer" } }
```

失败：

```json
{
  "success": false,
  "error": { "type": "personNotFound", "message": "Person not found" }
}
```

退出码 0 表示 API 调用成功——务必检查 `success` 字段确认操作结果。非零退出码表示基础设施错误：

| 退出码 | 含义                                                             |
| ------ | ---------------------------------------------------------------- |
| 0      | 成功（检查 `success` 字段——操作可能返回"person not found"等错误） |
| 1      | 通用/意外错误                                                    |
| 2      | 令牌缺失或无效                                                   |
| 3      | 需要订阅/套餐                                                    |
| 4      | LinkedIn 账户问题                                                |
| 5      | 参数无效                                                         |
| 6      | 触发速率限制                                                     |
| 7      | 网络错误                                                         |
| 8      | 工作流超时（返回 workflowId 用于恢复）                            |

## 命令

### 获取人员档案

```bash
linkedin person fetch <url> [flags] --json -q
```

可选标志，用于包含额外数据：

- `--experience` – 工作经历
- `--education` – 教育经历
- `--skills` – 技能列表
- `--languages` – 语言
- `--posts` – 近期帖子（配合 `--posts-limit N`、`--posts-since TIMESTAMP`）
- `--comments` – 近期评论（配合 `--comments-limit N`、`--comments-since TIMESTAMP`）
- `--reactions` – 近期互动（配合 `--reactions-limit N`、`--reactions-since TIMESTAMP`）

仅在需要时请求额外数据——每个标志都会增加执行时间。

```bash
# 基本档案
linkedin person fetch https://www.linkedin.com/in/username --json -q

# 含工作经历和教育经历
linkedin person fetch https://www.linkedin.com/in/username --experience --education --json -q

# 含最近 5 条帖子
linkedin person fetch https://www.linkedin.com/in/username --posts --posts-limit 5 --json -q
```

### 搜索人员

```bash
linkedin person search [flags] --json -q
```

| 标志                   | 说明                           |
| ---------------------- | ------------------------------ |
| `--term`               | 搜索关键词或短语               |
| `--limit`              | 最大结果数                     |
| `--first-name`         | 按名筛选                       |
| `--last-name`          | 按姓筛选                       |
| `--position`           | 按职位筛选                     |
| `--locations`          | 逗号分隔的地区                 |
| `--industries`         | 逗号分隔的行业                 |
| `--current-companies`  | 逗号分隔的当前公司名           |
| `--previous-companies` | 逗号分隔的过往公司名           |
| `--schools`            | 逗号分隔的学校名               |

```bash
linkedin person search --term "product manager" --locations "San Francisco" --json -q
linkedin person search --current-companies "Google" --position "Engineer" --limit 20 --json -q
```

### 获取公司信息

```bash
linkedin company fetch <url> [flags] --json -q
```

可选标志：

- `--employees` – 包含员工
- `--dms` – 包含决策者
- `--posts` – 包含公司帖子

员工筛选（需 `--employees`）：

| 标志                     | 说明                   |
| ------------------------ | ---------------------- |
| `--employees-limit`      | 最大员工检索数         |
| `--employees-first-name` | 按名筛选               |
| `--employees-last-name`  | 按姓筛选               |
| `--employees-position`   | 按职位筛选             |
| `--employees-locations`  | 逗号分隔的地区         |
| `--employees-industries` | 逗号分隔的行业         |
| `--employees-schools`    | 逗号分隔的学校名       |

| 标志            | 说明                                       |
| --------------- | ------------------------------------------ |
| `--dms-limit`   | 最大决策者检索数（需 `--dms`）             |
| `--posts-limit` | 最大帖子检索数（需 `--posts`）             |
| `--posts-since` | ISO 时间戳之后的帖子（需 `--posts`）       |

```bash
# 基本公司信息
linkedin company fetch https://www.linkedin.com/company/name --json -q

# 含按职位筛选的员工
linkedin company fetch https://www.linkedin.com/company/name --employees --employees-position "Engineer" --json -q

# 含决策者和帖子
linkedin company fetch https://www.linkedin.com/company/name --dms --posts --posts-limit 10 --json -q
```

### 搜索公司

```bash
linkedin company search [flags] --json -q
```

| 标志           | 说明                                                                                                        |
| -------------- | ----------------------------------------------------------------------------------------------------------- |
| `--term`       | 搜索关键词                                                                                                  |
| `--limit`      | 最大结果数                                                                                                  |
| `--sizes`      | 逗号分隔的规模：`1-10`、`11-50`、`51-200`、`201-500`、`501-1000`、`1001-5000`、`5001-10000`、`10001+`      |
| `--locations`  | 逗号分隔的地区                                                                                              |
| `--industries` | 逗号分隔的行业                                                                                              |

```bash
linkedin company search --term "fintech" --sizes "11-50,51-200" --json -q
```

### 发送消息

```bash
linkedin message send <person-url> '<text>' --json -q
```

文本最多 1900 字符。用单引号包裹消息内容以避免 shell 解析问题。

```bash
linkedin message send https://www.linkedin.com/in/username 'Hey, loved your latest post!' --json -q
```

### 获取对话

```bash
linkedin message get <person-url> [--since TIMESTAMP] --json -q
```

首次获取对话会触发后台同步，耗时较长。后续调用更快。

```bash
linkedin message get https://www.linkedin.com/in/username --json -q
linkedin message get https://www.linkedin.com/in/username --since 2024-01-15T10:30:00Z --json -q
```

### 人脉管理

#### 查看人脉状态

```bash
linkedin connection status <url> --json -q
```

#### 发送人脉请求

```bash
linkedin connection send <url> [--note 'text'] [--email user@example.com] --json -q
```

#### 列出人脉

```bash
linkedin connection list [flags] --json -q
```

| 标志                   | 说明                                                         |
| ---------------------- | ------------------------------------------------------------ |
| `--limit`              | 最大返回人脉数                                               |
| `--since`              | 仅返回此 ISO 时间戳之后建立的人脉（仅在无筛选标志时生效）   |
| `--first-name`         | 按名筛选                                                     |
| `--last-name`          | 按姓筛选                                                     |
| `--position`           | 按职位筛选                                                   |
| `--locations`          | 逗号分隔的地区                                               |
| `--industries`         | 逗号分隔的行业                                               |
| `--current-companies`  | 逗号分隔的当前公司名                                         |
| `--previous-companies` | 逗号分隔的过往公司名                                         |
| `--schools`            | 逗号分隔的学校名                                             |

```bash
linkedin connection list --limit 50 --json -q
linkedin connection list --current-companies "Google" --position "Engineer" --json -q
linkedin connection list --since 2024-01-01T00:00:00Z --json -q
```

#### 列出待处理的发出请求

```bash
linkedin connection pending --json -q
```

#### 撤回待处理请求

```bash
linkedin connection withdraw <url> [--no-unfollow] --json -q
```

默认撤回时同时取消关注。使用 `--no-unfollow` 保留关注。

#### 移除人脉

```bash
linkedin connection remove <url> --json -q
```

### 帖子

#### 获取帖子

```bash
linkedin post fetch <url> [flags] --json -q
```

| 标志                 | 说明                                                         |
| -------------------- | ------------------------------------------------------------ |
| `--comments`         | 包含评论                                                     |
| `--reactions`        | 包含互动                                                     |
| `--comments-limit`   | 最大评论检索数（需 `--comments`）                            |
| `--comments-sort`    | 排序方式：`mostRelevant` 或 `mostRecent`（需 `--comments`）  |
| `--comments-replies` | 包含评论回复（需 `--comments`）                              |
| `--reactions-limit`  | 最大互动检索数（需 `--reactions`）                           |

```bash
linkedin post fetch https://www.linkedin.com/posts/username_activity-123 --json -q

# 含按最新排序的评论及回复
linkedin post fetch https://www.linkedin.com/posts/username_activity-123 \
  --comments --comments-sort mostRecent --comments-replies --json -q
```

#### 创建帖子

```bash
linkedin post create '<text>' [flags] --json -q
```

| 标志            | 说明                                                                                                          |
| --------------- | ------------------------------------------------------------------------------------------------------------- |
| `--company-url` | 以公司页面身份发帖（需管理员权限）                                                                             |
| `--attachments` | 附件格式为 `url:type` 或 `url:type:name`。类型：`image`、`video`、`document`。可多次指定。                    |

附件限制：最多 9 张图片，或 1 个视频，或 1 个文档。不可混合类型。

```bash
linkedin post create 'Excited to share our latest update!' --json -q

# 含文档
linkedin post create 'Our Q4 report' \
  --attachments "https://example.com/report.pdf:document:Q4 Report" --json -q

# 以公司身份发帖
linkedin post create 'Company announcement' \
  --company-url https://www.linkedin.com/company/name --json -q
```

#### 点赞帖子

```bash
linkedin post react <url> --type <reaction> [--company-url <url>] --json -q
```

互动类型：`like`、`love`、`support`、`celebrate`、`insightful`、`funny`。

```bash
linkedin post react https://www.linkedin.com/posts/username_activity-123 --type like --json -q

# 以公司身份点赞
linkedin post react https://www.linkedin.com/posts/username_activity-123 --type celebrate \
  --company-url https://www.linkedin.com/company/name --json -q
```

#### 评论帖子

```bash
linkedin post comment <url> '<text>' [--company-url <url>] --json -q
```

文本最多 1000 字符。

```bash
linkedin post comment https://www.linkedin.com/posts/username_activity-123 'Great insights!' --json -q

# 以公司身份评论
linkedin post comment https://www.linkedin.com/posts/username_activity-123 'Well said!' \
  --company-url https://www.linkedin.com/company/name --json -q
```

### 统计

```bash
# 社交销售指数
linkedin stats ssi --json -q

# 绩效分析（档案浏览量、帖子曝光量、搜索出现次数）
linkedin stats performance --json -q

# 指定日期范围的 API 用量
linkedin stats usage --start 2024-01-01T00:00:00Z --end 2024-01-31T00:00:00Z --json -q
```

### Sales Navigator

需要 LinkedIn Sales Navigator 订阅。使用哈希 URL 进行人员/公司查询。

#### 获取人员

```bash
linkedin navigator person fetch <hashed-url> --json -q
```

#### 搜索人员

```bash
linkedin navigator person search [flags] --json -q
```

| 标志                    | 说明                                                                                  |
| ----------------------- | ------------------------------------------------------------------------------------- |
| `--term`                | 搜索关键词或短语                                                                      |
| `--limit`               | 最大结果数                                                                            |
| `--first-name`          | 按名筛选                                                                              |
| `--last-name`           | 按姓筛选                                                                              |
| `--position`            | 按职位筛选                                                                            |
| `--locations`           | 逗号分隔的地区                                                                        |
| `--industries`          | 逗号分隔的行业                                                                        |
| `--current-companies`   | 逗号分隔的当前公司名                                                                  |
| `--previous-companies`  | 逗号分隔的过往公司名                                                                  |
| `--schools`             | 逗号分隔的学校名                                                                      |
| `--years-of-experience` | 逗号分隔的经验范围：`lessThanOne`、`oneToTwo`、`threeToFive`、`sixToTen`、`moreThanTen` |

```bash
linkedin navigator person search --term "VP Marketing" --locations "United States" --json -q
linkedin navigator person search --years-of-experience "moreThanTen" --position "CEO" --json -q
```

#### 获取公司

```bash
linkedin navigator company fetch <hashed-url> [flags] --json -q
```

可选标志：

- `--employees` – 包含员工
- `--dms` – 包含决策者

员工筛选（需 `--employees`）：

| 标志                              | 说明                                   |
| --------------------------------- | -------------------------------------- |
| `--employees-limit`               | 最大员工检索数                         |
| `--employees-first-name`          | 按名筛选                               |
| `--employees-last-name`           | 按姓筛选                               |
| `--employees-positions`           | 逗号分隔的职位                         |
| `--employees-locations`           | 逗号分隔的地区                         |
| `--employees-industries`          | 逗号分隔的行业                         |
| `--employees-schools`             | 逗号分隔的学校名                       |
| `--employees-years-of-experience` | 逗号分隔的经验范围                     |
| `--dms-limit`                     | 最大决策者检索数（需 `--dms`）         |

```bash
linkedin navigator company fetch https://www.linkedin.com/sales/company/97ural --employees --dms --json -q
linkedin navigator company fetch https://www.linkedin.com/sales/company/97ural \
  --employees --employees-positions "Engineer,Designer" --employees-locations "Europe" --json -q
```

#### 搜索公司

```bash
linkedin navigator company search [flags] --json -q
```

| 标志            | 说明                                                                                                        |
| --------------- | ----------------------------------------------------------------------------------------------------------- |
| `--term`        | 搜索关键词                                                                                                  |
| `--limit`       | 最大结果数                                                                                                  |
| `--sizes`       | 逗号分隔的规模：`1-10`、`11-50`、`51-200`、`201-500`、`501-1000`、`1001-5000`、`5001-10000`、`10001+`      |
| `--locations`   | 逗号分隔的地区                                                                                              |
| `--industries`  | 逗号分隔的行业                                                                                              |
| `--revenue-min` | 最低年收入（百万美元）：`0`、`0.5`、`1`、`2.5`、`5`、`10`、`20`、`50`、`100`、`500`、`1000`                |
| `--revenue-max` | 最高年收入（百万美元）：`0.5`、`1`、`2.5`、`5`、`10`、`20`、`50`、`100`、`500`、`1000`、`1000+`            |

```bash
linkedin navigator company search --term "fintech" --sizes "11-50,51-200" --json -q
linkedin navigator company search --revenue-min 10 --revenue-max 100 --locations "United States" --json -q
```

#### 发送 InMail

```bash
linkedin navigator message send <person-url> '<text>' --subject '<subject>' --json -q
```

文本最多 1900 字符。主题最多 80 字符。

```bash
linkedin navigator message send https://www.linkedin.com/in/username \
  'Would love to chat about API integrations' --subject 'Partnership Opportunity' --json -q
```

#### 获取 Sales Navigator 对话

```bash
linkedin navigator message get <person-url> [--since TIMESTAMP] --json -q
```

### 自定义工作流

从文件、标准输入或内联执行自定义工作流定义：

```bash
# 从文件
linkedin workflow run --file workflow.json --json -q

# 从标准输入
cat workflow.json | linkedin workflow run --json -q

# 内联
echo '{"actions":[...]}' | linkedin workflow run --json -q
```

检查工作流状态或等待完成：

```bash
linkedin workflow status <id> --json -q
linkedin workflow status <id> --wait --json -q
```

工作流 JSON 格式参见 [Building Workflows](https://linkedapi.io/docs/building-workflows/)。

### 账户管理

```bash
linkedin account list                            # 列出账户（* = 活跃）
linkedin account switch "Name"                   # 切换活跃账户
linkedin account rename "Name" --name "New Name" # 重命名账户
linkedin reset                                   # 移除活跃账户
linkedin reset --all                             # 移除所有账户
```

## 重要行为

- **顺序执行。** 同一账户的所有操作逐一运行，多个请求排队等待。
- **非即时。** 真实浏览器操作 LinkedIn——每个操作预计 30 秒到数分钟。
- **时间戳为 UTC。** 所有日期和时间使用 UTC。
- **文本参数用单引号。** 消息、帖子和评论文本用单引号包裹，避免特殊字符的 shell 解析问题。
- **操作限制。** 每账户限制可在平台配置。`limitExceeded` 错误表示已达上限。
- **URL 规范化。** 响应中所有 LinkedIn URL 统一为 `https://www.linkedin.com/...` 格式，无尾部斜杠。
- **空值字段。** 不可用的字段返回 `null` 或 `[]`，不会省略。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 输出不能替代针对具体环境的验证、测试或专家审查。
- 如缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清。
