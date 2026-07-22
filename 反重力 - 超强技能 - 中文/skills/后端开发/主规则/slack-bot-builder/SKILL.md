---
name: slack-bot-builder
description: 使用 Bolt 框架构建 Slack 应用，支持 Python、JavaScript 和 Java。涵盖 Block Kit 丰富 UI、交互组件、斜杠命令、事件处理、OAuth 安装流程和 Workflow Builder 集成。触发词：Slack 机器人、Slack 应用、Bolt 框架、Block Kit、斜杠命令、Slack webhook、Slack 工作流
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Slack 机器人构建器

使用 Bolt 框架构建 Slack 应用，支持 Python、JavaScript 和 Java。
涵盖 Block Kit 丰富 UI、交互组件、斜杠命令、
事件处理、OAuth 安装流程和 Workflow Builder 集成。
专注于生产级 Slack 应用的最佳实践。

## 模式

### Bolt 应用基础模式

Bolt 框架是 Slack 推荐的应用构建方式。
它处理认证、事件路由、请求验证和
HTTP 请求处理，让你专注于应用逻辑。

核心优势：
- 几行代码即可处理事件
- 内置安全检查和载荷验证
- 组织化、一致的模式
- 适用于实验和生产环境

支持语言：Python、JavaScript（Node.js）、Java

**使用场景**：开始任何新的 Slack 应用、从旧版 Slack API 迁移、构建生产级 Slack 集成

```python
# Python Bolt 应用
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os

# 使用环境变量中的令牌初始化
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

# 处理包含 "hello" 的消息
@app.message("hello")
def handle_hello(message, say):
    """响应包含 'hello' 的消息。"""
    user = message["user"]
    say(f"Hey there <@{user}>!")

# 处理斜杠命令
@app.command("/ticket")
def handle_ticket_command(ack, body, client):
    """处理 /ticket 斜杠命令。"""
    # 立即确认（3 秒内）
    ack()

    # 打开创建工单的模态框
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "ticket_modal",
            "title": {"type": "plain_text", "text": "Create Ticket"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "title_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "title_input"
                    },
                    "label": {"type": "plain_text", "text": "Title"}
                },
                {
                    "type": "input",
                    "block_id": "desc_block",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "desc_input"
                    },
                    "label": {"type": "plain_text", "text": "Description"}
                },
                {
                    "type": "input",
                    "block_id": "priority_block",
                    "element": {
                        "type": "static_select",
                        "action_id": "priority_select",
                        "options": [
                            {"text": {"type": "plain_text", "text": "Low"}, "value": "low"},
                            {"text": {"type": "plain_text", "text": "Medium"}, "value": "medium"},
                            {"text": {"type": "plain_text", "text": "High"}, "value": "high"}
                        ]
                    },
                    "label": {"type": "plain_text", "text": "Priority"}
                }
            ]
        }
    )

# 处理模态框提交
@app.view("ticket_modal")
def handle_ticket_submission(ack, body, client, view):
    """处理工单模态框提交。"""
    ack()

    # 从视图中提取值
    values = view["state"]["values"]
    title = values["title_block"]["title_input"]["value"]
    desc = values["desc_block"]["desc_input"]["value"]
    priority = values["priority_block"]["priority_select"]["selected_option"]["value"]
    user_id = body["user"]["id"]

    # 在系统中创建工单
    ticket_id = create_ticket(title, desc, priority, user_id)

    # 通知用户
    client.chat_postMessage(
        channel=user_id,
        text=f"Ticket #{ticket_id} created: {title}"
    )

# 处理按钮点击
@app.action("approve_button")
def handle_approval(ack, body, client):
    """处理审批按钮点击。"""
    ack()

    # 从操作中获取上下文
    user = body["user"]["id"]
    action_value = body["actions"][0]["value"]

    # 更新消息以移除交互元素
    # （最佳实践：防止重复点击）
    client.chat_update(
        channel=body["channel"]["id"],
        ts=body["message"]["ts"],
        text=f"Approved by <@{user}>",
        blocks=[]  # 移除交互块
    )

# 监听 app_home_opened 事件
@app.event("app_home_opened")
def update_home_tab(client, event):
    """用户打开主页标签时更新。"""
    client.views_publish(
        user_id=event["user"],
        view={
            "type": "home",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Welcome to the Ticket Bot!*"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Create Ticket"},
                            "action_id": "create_ticket_button"
                        }
                    ]
                }
            ]
        }
    )

# Socket 模式用于开发（无需公网 URL）
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

# 生产环境请使用 HTTP 模式配合 Web 服务器
# from flask import Flask, request
# from slack_bolt.adapter.flask import SlackRequestHandler
#
# flask_app = Flask(__name__)
# handler = SlackRequestHandler(app)
#
# @flask_app.route("/slack/events", methods=["POST"])
# def slack_events():
#     return handler.handle(request)
```

### 反模式

- 未在 3 秒内确认请求
- 在 ack 处理器中执行阻塞操作
- 在源代码中硬编码令牌
- 开发时未使用 Socket 模式

### Block Kit UI 模式

Block Kit 是 Slack 的 UI 框架，用于构建丰富的交互式消息。
使用块（sections、actions、inputs）和元素
（按钮、菜单、文本输入）组合消息。

限制：
- 每条消息最多 50 个块
- 模态框/主页标签最多 100 个块
- 块文本限制为 3000 个字符

使用 Block Kit Builder 原型设计：https://app.slack.com/block-kit-builder

**使用场景**：构建丰富的消息布局、为消息添加交互组件、在模态框中创建表单、构建主页标签体验

```python
from slack_bolt import App
import os

app = App(token=os.environ["SLACK_BOT_TOKEN"])

def build_notification_blocks(incident: dict) -> list:
    """为事件通知构建 Block Kit 块。"""
    severity_emoji = {
        "critical": ":red_circle:",
        "high": ":large_orange_circle:",
        "medium": ":large_yellow_circle:",
        "low": ":white_circle:"
    }

    return [
        # 头部
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{severity_emoji.get(incident['severity'], '')} Incident Alert"
            }
        },
        # 详情部分
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Incident:*\n{incident['title']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Severity:*\n{incident['severity'].upper()}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Service:*\n{incident['service']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Reported:*\n<!date^{incident['timestamp']}^{date_short} {time}|{incident['timestamp']}>"
                }
            ]
        },
        # 描述
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Description:*\n{incident['description'][:2000]}"
            }
        },
        # 分隔线
        {"type": "divider"},
        # 操作按钮
        {
            "type": "actions",
            "block_id": f"incident_actions_{incident['id']}",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Acknowledge"},
                    "style": "primary",
                    "action_id": "acknowledge_incident",
                    "value": incident['id']
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Resolve"},
                    "style": "danger",
                    "action_id": "resolve_incident",
                    "value": incident['id'],
                    "confirm": {
                        "title": {"type": "plain_text", "text": "Resolve Incident?"},
                        "text": {"type": "mrkdwn", "text": "Are you sure this incident is resolved?"},
                        "confirm": {"type": "plain_text", "text": "Yes, Resolve"},
                        "deny": {"type": "plain_text", "text": "Cancel"}
                    }
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "View Details"},
                    "action_id": "view_incident",
                    "value": incident['id'],
                    "url": f"https://incidents.example.com/{incident['id']}"
                }
            ]
        },
        # 上下文页脚
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Incident ID: {incident['id']} | <https://runbook.example.com/{incident['service']}|View Runbook>"
                }
            ]
        }
    ]

def send_incident_notification(channel: str, incident: dict):
    """使用 Block Kit 发送事件通知。"""
    blocks = build_notification_blocks(incident)

    app.client.chat_postMessage(
        channel=channel,
        text=f"Incident: {incident['title']}",  # 通知的回退文本
        blocks=blocks
    )

# 处理按钮操作
@app.action("acknowledge_incident")
def handle_acknowledge(ack, body, client):
    """处理事件确认。"""
    ack()

    incident_id = body["actions"][0]["value"]
    user = body["user"]["id"]

    # 更新你的系统
    acknowledge_incident(incident_id, user)

    # 更新消息显示确认状态
    original_blocks = body["message"]["blocks"]

    # 在上下文中添加确认信息
    original_blocks[-1]["elements"].append({
        "type": "mrkdwn",
        "text": f":white_check_mark: Acknowledged by <@{user}>"
    })

    # 移除确认按钮（防止重复点击）
    action_block = next(b for b in original_blocks if b.get("block_id", "").startswith("incident_actions"))
    action_block["elements"] = [e for e in action_block["elements"] if e["action_id"] != "acknowledge_incident"]

    client.chat_update(
        channel=body["channel"]["id"],
        ts=body["message"]["ts"],
        blocks=original_blocks
    )

# 交互式选择菜单
def build_user_selector_blocks():
    """构建带用户选择器的块。"""
    return [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Assign this task:"},
            "accessory": {
                "type": "users_select",
                "action_id": "assign_user",
                "placeholder": {"type": "plain_text", "text": "Select assignee"}
            }
        }
    ]

# 溢出菜单用于更多选项
def build_task_blocks(task: dict):
    """构建带溢出菜单的任务块。"""
    return [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*{task['title']}*"},
            "accessory": {
                "type": "overflow",
                "action_id": "task_overflow",
                "options": [
                    {
                        "text": {"type": "plain_text", "text": "Edit"},
                        "value": f"edit_{task['id']}"
                    },
                    {
                        "text": {"type": "plain_text", "text": "Delete"},
                        "value": f"delete_{task['id']}"
                    },
                    {
                        "text": {"type": "plain_text", "text": "Share"},
                        "value": f"share_{task['id']}"
                    }
                ]
            }
        }
    ]
```

### 反模式

- 超过每条消息 50 个块的限制
- 未提供回退文本以支持无障碍
- 硬编码 action_id（需要时使用动态 ID）
- 未对按钮点击进行幂等处理

### OAuth 安装模式

让用户通过 OAuth 2.0 在其工作区安装你的应用。
Bolt 处理大部分 OAuth 流程，但你需要配置它
并安全存储令牌。

核心 OAuth 概念：
- Scopes 定义权限（只请求需要的最小权限）
- 令牌是工作区特定的
- 安装数据必须持久化存储
- 用户可以后续添加 scopes（增量式）

70% 的用户在面对过多权限请求时会放弃安装 — 只请求你需要的！

**使用场景**：将应用分发到多个工作区、构建公开的 Slack 应用、企业级集成

```python
from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore
import os

# 生产环境请使用数据库支持的存储
# 例如：PostgreSQL、MongoDB、Redis

class DatabaseInstallationStore:
    """在数据库中存储安装数据。"""

    async def save(self, installation):
        """用户完成 OAuth 时保存安装数据。"""
        await db.installations.upsert({
            "team_id": installation.team_id,
            "enterprise_id": installation.enterprise_id,
            "bot_token": encrypt(installation.bot_token),
            "bot_user_id": installation.bot_user_id,
            "bot_scopes": installation.bot_scopes,
            "user_id": installation.user_id,
            "installed_at": installation.installed_at
        })

    async def find_installation(self, *, enterprise_id, team_id, user_id=None, is_enterprise_install=False):
        """查找工作区的安装数据。"""
        record = await db.installations.find_one({
            "team_id": team_id,
            "enterprise_id": enterprise_id
        })

        if record:
            return Installation(
                bot_token=decrypt(record["bot_token"]),
                # ... 其他字段
            )
        return None

# 初始化支持 OAuth 的应用
app = App(
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    oauth_settings=OAuthSettings(
        client_id=os.environ["SLACK_CLIENT_ID"],
        client_secret=os.environ["SLACK_CLIENT_SECRET"],
        scopes=[
            "channels:history",
            "channels:read",
            "chat:write",
            "commands",
            "users:read"
        ],
        user_scopes=[],  # 如需要则设置用户令牌 scopes
        installation_store=DatabaseInstallationStore(),
        state_store=FileOAuthStateStore(expiration_seconds=600)
    )
)

# OAuth 路由由 Bolt 自动处理
# /slack/install - 发起 OAuth 流程
# /slack/oauth_redirect - 处理回调

# Flask 集成
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/install", methods=["GET"])
def install():
    return handler.handle(request)

@flask_app.route("/slack/oauth_redirect", methods=["GET"])
def oauth_redirect():
    return handler.handle(request)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# 处理安装成功/失败
@app.oauth_success
def handle_oauth_success(args):
    """OAuth 成功完成时调用。"""
    installation = args["installation"]

    # 发送欢迎消息
    app.client.chat_postMessage(
        token=installation.bot_token,
        channel=installation.user_id,
        text="Thanks for installing! Type /help to get started."
    )

    return "Installation successful! You can close this window."

@app.oauth_failure
def handle_oauth_failure(args):
    """OAuth 失败时调用。"""
    error = args.get("error", "Unknown error")
    return f"Installation failed: {error}"

# Scope 管理 - 需要时请求额外的 scopes
def request_additional_scopes(team_id: str, new_scopes: list):
    """
    生成 URL 让用户添加 scopes。
    注意：现有令牌保留旧的 scopes。
    用户必须重新授权以获取新的 scopes。
    """
    base_url = "https://slack.com/oauth/v2/authorize"
    params = {
        "client_id": os.environ["SLACK_CLIENT_ID"],
        "scope": ",".join(new_scopes),
        "team": team_id
    }
    return f"{base_url}?{urlencode(params)}"
```

### 反模式

- 提前请求不必要的 scopes
- 以明文存储令牌
- 未验证 OAuth state 参数（CSRF 风险）
- 假设配置更改后令牌自动获得新的 scopes

### Socket 模式

Socket 模式允许你的应用通过 WebSocket 而非
公网 HTTP 端点接收事件。非常适合开发和
位于防火墙后的应用。

优势：
- 无需公网 URL
- 可在企业防火墙后工作
- 更简单的本地开发
- 实时双向通信

限制：不推荐用于高流量生产应用。

**使用场景**：本地开发、企业防火墙后的应用、有安全约束的内部工具、原型设计和测试

```python
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os

# Socket 模式需要应用级令牌（xapp-...）
# 在 App Settings > Basic Information > App-Level Tokens 中创建
# 需要 'connections:write' scope

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.message("hello")
def handle_hello(message, say):
    say(f"Hey <@{message['user']}>!")

@app.command("/status")
def handle_status(ack, say):
    ack()
    say("All systems operational!")

@app.event("app_mention")
def handle_mention(event, say):
    say(f"You mentioned me, <@{event['user']}>!")

if __name__ == "__main__":
    # SocketModeHandler 管理 WebSocket 连接
    handler = SocketModeHandler(
        app,
        os.environ["SLACK_APP_TOKEN"]  # xapp-... 令牌
    )

    print("Starting Socket Mode...")
    handler.start()

# 异步应用
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
import asyncio

async_app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])

@async_app.message("hello")
async def handle_hello_async(message, say):
    await say(f"Hey <@{message['user']}>!")

async def main():
    handler = AsyncSocketModeHandler(async_app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()

if __name__ == "__main__":
    asyncio.run(main())
```

### 反模式

- 在高流量生产应用中使用 Socket 模式
- 未处理 WebSocket 断开连接
- 忘记创建应用级令牌
- 使用机器人令牌而非应用令牌

### Workflow Builder 步骤模式

使用你的应用驱动的自定义步骤扩展 Slack 的 Workflow Builder。
用户可以在其无代码工作流中包含你的自定义步骤。

工作流步骤可以：
- 从用户收集输入
- 执行自定义逻辑
- 为后续步骤输出数据

**使用场景**：与 Workflow Builder 集成、让非技术用户使用你的功能、构建可复用的自动化组件

```python
from slack_bolt import App
from slack_bolt.workflows.step import WorkflowStep
import os

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

# 定义工作流步骤
def edit(ack, step, configure):
    """用户在 Workflow Builder 中添加/编辑步骤时调用。"""
    ack()

    # 显示配置模态框
    blocks = [
        {
            "type": "input",
            "block_id": "ticket_type",
            "element": {
                "type": "static_select",
                "action_id": "type_select",
                "options": [
                    {"text": {"type": "plain_text", "text": "Bug"}, "value": "bug"},
                    {"text": {"type": "plain_text", "text": "Feature"}, "value": "feature"},
                    {"text": {"type": "plain_text", "text": "Task"}, "value": "task"}
                ]
            },
            "label": {"type": "plain_text", "text": "Ticket Type"}
        },
        {
            "type": "input",
            "block_id": "title_input",
            "element": {
                "type": "plain_text_input",
                "action_id": "title"
            },
            "label": {"type": "plain_text", "text": "Title"}
        },
        {
            "type": "input",
            "block_id": "assignee_input",
            "element": {
                "type": "users_select",
                "action_id": "assignee"
            },
            "label": {"type": "plain_text", "text": "Assignee"}
        }
    ]

    configure(blocks=blocks)

def save(ack, view, update):
    """用户保存步骤配置时调用。"""
    ack()

    values = view["state"]["values"]

    # 定义输入（来自用户的配置）
    inputs = {
        "ticket_type": {
            "value": values["ticket_type"]["type_select"]["selected_option"]["value"]
        },
        "title": {
            "value": values["title_input"]["title"]["value"]
        },
        "assignee": {
            "value": values["assignee_input"]["assignee"]["selected_user"]
        }
    }

    # 定义输出（供后续步骤使用）
    outputs = [
        {
            "name": "ticket_id",
            "type": "text",
            "label": "Created Ticket ID"
        },
        {
            "name": "ticket_url",
            "type": "text",
            "label": "Ticket URL"
        }
    ]

    update(inputs=inputs, outputs=outputs)

def execute(step, complete, fail):
    """步骤在工作流中运行时调用。"""
    inputs = step["inputs"]

    try:
        # 获取输入值
        ticket_type = inputs["ticket_type"]["value"]
        title = inputs["title"]["value"]
        assignee = inputs["assignee"]["value"]

        # 在系统中创建工单
        ticket = create_ticket(
            type=ticket_type,
            title=title,
            assignee=assignee
        )

        # 完成并输出结果
        complete(outputs={
            "ticket_id": ticket["id"],
            "ticket_url": ticket["url"]
        })

    except Exception as e:
        fail(error={"message": str(e)})

# 注册工作流步骤
create_ticket_step = WorkflowStep(
    callback_id="create_ticket_step",
    edit=edit,
    save=save,
    execute=execute
)

app.step(create_ticket_step)
```

### 反模式

- 在 execute 中未调用 complete() 或 fail()
- 长时间运行的操作没有进度更新
- 在 execute 中未验证输入
- 在输出中暴露敏感数据

## 关键陷阱

### 缺少 3 秒确认（超时）

严重程度：CRITICAL

场景：处理斜杠命令、快捷方式或交互组件

症状：
用户看到"This command timed out"或"Something went wrong。"
即使你的代码运行了，操作也永远不会完成。
开发环境正常但生产环境失败。

原因：
Slack 要求所有交互请求在 3 秒内确认：
- 斜杠命令
- 按钮/选择菜单点击
- 模态框提交
- 快捷方式

如果你在响应之前做了任何慢操作（数据库、API 调用、LLM），
你会错过窗口期。即使你的机器人最终正确处理了请求，Slack 也会显示错误。

推荐修复：

```python
## 立即确认，稍后处理

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import threading

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.command("/slow-task")
def handle_slow_task(ack, command, client, respond):
    # 立即确认 - 在任何处理之前
    ack("Processing your request...")

    # 在后台执行慢操作
    def do_work():
        result = call_slow_api(command["text"])  # 耗时 10 秒
        respond(f"Done! Result: {result}")

    threading.Thread(target=do_work).start()

@app.view("modal_submission")
def handle_modal(ack, body, client, view):
    # 模态框使用 response_action 确认
    ack(response_action="clear")  # 或使用 "update" 更新视图

    # 在后台处理
    user_id = body["user"]["id"]
    values = view["state"]["values"]
    # ... 慢处理
```

```python
## 对于 Bolt 框架 - 使用懒监听器

# Bolt 通过懒监听器自动处理 ack()
@app.command("/slow-task")
def handle_slow_task(ack, command, respond):
    ack()  # 仍然先调用 ack()！

@handle_slow_task.lazy
def process_slow_task(command, respond):
    # 在 ack 之后运行，可以任意长时间
    result = slow_operation(command["text"])
    respond(result)
```

### 未验证 OAuth State 参数（CSRF）

严重程度：CRITICAL

场景：实现 OAuth 安装流程

症状：
机器人似乎正常工作，但你容易受到 CSRF 攻击。
攻击者可以诱骗用户安装恶意配置。

原因：
OAuth state 参数防止 CSRF 攻击。流程：
1. 你生成随机 state，存储它，发送给 Slack
2. 用户在 Slack 中授权
3. Slack 使用 code + state 重定向回来
4. 你必须验证 state 与你存储的匹配

没有这个，攻击者可以制作恶意 OAuth URL 并诱骗
管理员使用攻击者的授权码完成流程。

推荐修复：

```python
## 正确的 state 验证

import secrets
from flask import Flask, request, session, redirect
from slack_sdk.oauth import AuthorizeUrlGenerator
from slack_sdk.oauth.state_store import FileOAuthStateStore

app = Flask(__name__)
app.secret_key = os.environ["SESSION_SECRET"]

# 使用 Slack SDK 的 state 存储（生产环境推荐 Redis）
state_store = FileOAuthStateStore(
    expiration_seconds=300,  # 5 分钟
    base_dir="./oauth_states"
)

@app.route("/slack/install")
def install():
    # 生成加密安全的 state
    state = state_store.issue()

    # 存储在会话中用于验证
    session["oauth_state"] = state

    authorize_url = AuthorizeUrlGenerator(
        client_id=os.environ["SLACK_CLIENT_ID"],
        scopes=["channels:history", "chat:write"],
        user_scopes=[]
    ).generate(state)

    return redirect(authorize_url)

@app.route("/slack/oauth/callback")
def oauth_callback():
    # 关键：验证 state
    received_state = request.args.get("state")
    stored_state = session.get("oauth_state")

    if not received_state or received_state != stored_state:
        return "Invalid state parameter - possible CSRF attack", 403

    # 同时使用 state_store.consume() 确保一次性使用
    if not state_store.consume(received_state):
        return "State already used or expired", 403

    # 现在可以安全地用 code 换取令牌
    code = request.args.get("code")
    # ... 完成 OAuth 流程
```

### 暴露机器人/用户令牌

严重程度：CRITICAL

场景：存储或记录 Slack 令牌

症状：
你的机器人发送了未授权的消息。攻击者读取私有
频道。令牌在日志、git 历史或客户端代码中被发现。

原因：
Slack 令牌提供其 scopes 范围内的完全访问权限：
- 机器人令牌（xoxb-*）：访问已安装的工作区
- 用户令牌（xoxp-*）：以该特定用户身份访问
- 应用级令牌（xapp-*）：Socket 模式连接

常见暴露点：
- 硬编码在源代码中
- 在错误消息中记录
- 发送到前端/客户端
- 在数据库中未加密存储

推荐修复：

```python
## 永远不要硬编码或记录令牌

# 错误 - 永远不要这样做
client = WebClient(token="xoxb-12345-...")

# 正确 - 使用环境变量
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

# 错误 - 记录令牌
logger.error(f"API call failed with token {token}")

# 正确 - 永远不要记录令牌
logger.error(f"API call failed for team {team_id}")

# 错误 - 将令牌发送到前端
return {"token": bot_token}

# 正确 - 只发送前端需要的内容
return {"channels": channel_list}
```

```python
## 在数据库中加密令牌

from cryptography.fernet import Fernet

class TokenStore:
    def __init__(self, encryption_key: str):
        self.cipher = Fernet(encryption_key)

    def save_token(self, team_id: str, token: str):
        encrypted = self.cipher.encrypt(token.encode())
        db.execute(
            "INSERT INTO installations (team_id, encrypted_token) VALUES (?, ?)",
            (team_id, encrypted)
        )

    def get_token(self, team_id: str) -> str:
        row = db.execute(
            "SELECT encrypted_token FROM installations WHERE team_id = ?",
            (team_id,)
        ).fetchone()
        return self.cipher.decrypt(row[0]).decode()
```

```bash
## 如果令牌泄露则轮换
1. Slack API > Your App > OAuth & Permissions
2. 点击泄露令牌的 "Rotate"
3. 立即更新所有部署
4. 检查 Slack 审计日志是否有未授权访问
```

### 请求不必要的 OAuth Scopes

严重程度：HIGH

场景：为你的应用配置 OAuth scopes

症状：
用户因可怕的权限警告而犹豫安装。
安装率降低。安全部门阻止部署。
应用被 Slack App Directory 拒绝。

原因：
每个 OAuth scope 授予特定权限。请求超过
你需要的：
- 使安装同意屏幕看起来很可怕
- 如果令牌泄露会增加攻击面
- 可能违反企业安全策略
- 可能导致你的应用被 App Directory 拒绝

常见的过度请求：
- 只需要 `chat:write` 却请求了 `admin`
- 只向一个频道发消息却请求了 `channels:read`
- 不需要邮箱却请求了 `users:read.email`

推荐修复：

```python
## 请求最小必需的 scopes

# 对于简单的通知机器人
MINIMAL_SCOPES = [
    "chat:write",        # 发布消息
    "channels:join",     # 加入公开频道（如需要）
]

# 基本通知不需要：
# - channels:read（除非你列出频道）
# - users:read（除非你查找用户）
# - channels:history（除非你读取消息）

# 对于斜杠命令机器人
SLASH_COMMAND_SCOPES = [
    "commands",          # 注册斜杠命令
    "chat:write",        # 响应命令
]

# 对于响应 @提及的机器人
MENTION_BOT_SCOPES = [
    "app_mentions:read", # 接收 @提及
    "chat:write",        # 回复提及
]
```

```python
## 按用例分类的 scope 参考

# | 用例 | 必需的 Scopes |
# |----------|-----------------|
# | 发布消息 | `chat:write` |
# | 斜杠命令 | `commands` |
# | 响应 @提及 | `app_mentions:read`, `chat:write` |
# | 读取频道消息 | `channels:history`（公开）, `groups:history`（私有） |
# | 读取用户信息 | `users:read` |
# | 打开模态框 | `commands` 或从事件触发 |
# | 添加表情回应 | `reactions:write` |
# | 上传文件 | `files:write` |

## 渐进式 scope 请求

# 从最小 scopes 开始
INITIAL_SCOPES = ["chat:write", "commands"]

# 仅在需要时请求额外的 scopes
@app.command("/enable-reactions")
def enable_reactions(ack, client, command):
    ack()

    # 检查是否已有该 scope
    auth_result = client.auth_test()
    # 如果缺少 reactions:write，提示重新授权
    if needs_additional_scope:
        # 发送用户去重新授权以获取额外 scope
        pass
```

### 超出 Block Kit 限制

严重程度：MEDIUM

场景：使用 Block Kit 构建复杂的消息 UI

症状：
消息发送失败并显示"invalid_blocks"错误。
模态框无法打开。消息被意外截断。

原因：
Block Kit 有严格的限制，但并不总是显而易见：
- 每条消息/模态框 50 个块
- 每个文本块 3000 个字符
- 每个 actions 块 10 个元素
- 每个选择菜单 100 个选项
- 模态框：50 个块，总计 24KB
- 主页标签：100 个块

超出这些限制会导致静默失败或晦涩的错误。

推荐修复：

```python
## 了解并遵守限制

# Block Kit 限制常量
BLOCK_KIT_LIMITS = {
    "blocks_per_message": 50,
    "blocks_per_modal": 50,
    "blocks_per_home": 100,
    "text_block_chars": 3000,
    "elements_per_actions": 10,
    "options_per_select": 100,
    "modal_total_bytes": 24 * 1024,  # 24KB
}

def validate_blocks(blocks: list) -> tuple[bool, str]:
    """发送前验证块。"""
    if len(blocks) > BLOCK_KIT_LIMITS["blocks_per_message"]:
        return False, f"Too many blocks: {len(blocks)} > 50"

    for block in blocks:
        if block.get("type") == "section":
            text = block.get("text", {}).get("text", "")
            if len(text) > BLOCK_KIT_LIMITS["text_block_chars"]:
                return False, f"Text too long: {len(text)} > 3000"

        if block.get("type") == "actions":
            elements = block.get("elements", [])
            if len(elements) > BLOCK_KIT_LIMITS["elements_per_actions"]:
                return False, f"Too many actions: {len(elements)} > 10"

    return True, "OK"

# 对长内容分页
def paginate_blocks(blocks: list, page: int = 0, per_page: int = 45):
    """对块进行分页并添加导航。"""
    start = page * per_page
    end = start + per_page
    page_blocks = blocks[start:end]

    # 添加分页控件
    if len(blocks) > per_page:
        page_blocks.append({
            "type": "actions",
            "elements": [
                {"type": "button", "text": {"type": "plain_text", "text": "Previous"},
                 "action_id": f"page_{page-1}", "disabled": page == 0},
                {"type": "button", "text": {"type": "plain_text", "text": "Next"},
                 "action_id": f"page_{page+1}",
                 "disabled": end >= len(blocks)}
            ]
        })

    return page_blocks
```

### 在生产环境使用 Socket 模式

严重程度：HIGH

场景：将 Slack 机器人部署到生产环境

症状：
机器人在开发环境正常但生产环境不可靠。
事件丢失。连接断开。无法水平扩展。

原因：
Socket 模式是为开发设计的：
- 每个应用单个 WebSocket 连接
- 无法扩展到多个实例
- 连接可能断开（需要重连逻辑）
- 没有内置负载均衡

对于多实例或高流量的生产环境，
HTTP webhook 更可靠。

推荐修复：

```python
## Socket 模式：仅用于开发

if os.environ.get("ENVIRONMENT") == "development":
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
```

```python
## 生产环境：使用 HTTP 端点

# 生产环境使用 HTTP（Flask 示例）
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@flask_app.route("/slack/commands", methods=["POST"])
def slack_commands():
    return handler.handle(request)

@flask_app.route("/slack/interactions", methods=["POST"])
def slack_interactions():
    return handler.handle(request)
```

```python
## 如果必须在生产环境使用 Socket 模式

from slack_bolt.adapter.socket_mode import SocketModeHandler
import time

class RobustSocketHandler:
    def __init__(self, app, app_token):
        self.app = app
        self.app_token = app_token
        self.handler = None

    def start(self):
        while True:
            try:
                self.handler = SocketModeHandler(self.app, self.app_token)
                self.handler.start()
            except Exception as e:
                logger.error(f"Socket Mode disconnected: {e}")
                time.sleep(5)  # 重连前退避
```

### 未验证请求签名

严重程度：CRITICAL

场景：从 Slack 接收 webhook

症状：
攻击者可以向你的 webhook 端点发送伪造请求。
伪造的斜杠命令。处理了伪造的事件通知。

原因：
Slack 使用你的签名密钥通过 X-Slack-Signature 头对所有请求签名。没有验证，任何知道你 webhook
URL 的人都可以发送伪造请求。

这与 OAuth 令牌不同 - 签名验证的是请求
来自 Slack，而不是你有权调用 Slack。

推荐修复：

```python
## Bolt 自动处理

from slack_bolt import App

# 提供 signing_secret 时 Bolt 自动验证签名
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)
# 你处理器中的所有请求都已验证
```

```python
## 手动验证（如果不使用 Bolt）

import hmac
import hashlib
import time
from flask import Flask, request, abort

SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]

def verify_slack_signature(request):
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    signature = request.headers.get("X-Slack-Signature", "")

    # 拒绝旧时间戳（防止重放攻击）
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False

    # 计算预期签名
    sig_basestring = f"v0:{timestamp}:{request.get_data(as_text=True)}"
    expected_sig = "v0=" + hmac.new(
        SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    # 恒定时间比较
    return hmac.compare_digest(expected_sig, signature)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    if not verify_slack_signature(request):
        abort(403)
    # 安全处理
```

## 验证检查

### 硬编码 Slack 令牌

严重程度：ERROR

Slack 令牌绝不应硬编码

消息：检测到硬编码的 Slack 令牌。请使用环境变量。

### 源代码中的签名密钥

严重程度：ERROR

签名密钥应在环境变量中

消息：硬编码的签名密钥。请使用 os.environ['SLACK_SIGNING_SECRET']。

### 未验证签名的 Webhook

严重程度：ERROR

Slack webhook 必须验证 X-Slack-Signature

消息：Webhook 未验证签名。请使用 Bolt 或手动验证。

### 客户端代码中的 Slack 令牌

严重程度：ERROR

永远不要向浏览器暴露 Slack 令牌

消息：Slack 凭证在客户端暴露。请仅在服务端使用。

### 确认前的慢操作

严重程度：WARNING

ack() 必须在慢操作之前调用

消息：ack() 之前有慢操作。请先调用 ack()，然后处理。

### 缺少确认调用

严重程度：WARNING

交互处理器必须调用 ack()

消息：处理器缺少 ack() 调用。必须在 3 秒内确认。

### 未验证 State 的 OAuth

严重程度：ERROR

OAuth 回调必须验证 state 参数

消息：OAuth 未验证 state。容易受到 CSRF 攻击。

### 未加密的令牌存储

严重程度：WARNING

令牌应加密存储

消息：令牌未加密存储。请加密静态令牌。

### 请求 Admin Scopes

严重程度：WARNING

除非绝对必要，否则避免使用 admin scopes

消息：请求了 admin scope。请使用最小必需的 scopes。

### 可能未使用的 Scope

严重程度：INFO

检查所有请求的 scopes 是否都被使用

消息：请求了 users:read.email 但可能未使用邮箱。请验证必要性。

## 协作

### 委派触发器

- 用户需要 AI 驱动的 Slack 机器人 -> llm-architect（集成 LLM 构建对话式 Slack 机器人）
- 用户需要语音通知 -> twilio-communications（将 Slack 告警升级为短信或语音通话）
- 用户需要工作流自动化 -> workflow-automation（Slack 作为 n8n/Temporal 工作流的触发器/动作）
- 用户需要 Discord 机器人 -> discord-bot-architect（跨平台机器人架构）
- 用户需要完整认证系统 -> auth-specialist（OAuth、工作区管理、企业 SSO）
- 用户需要机器人数据的数据库 -> postgres-wizard（存储安装数据、用户偏好、消息历史）
- 用户需要高可用性 -> devops（扩展 webhook、监控、告警）

## 使用场景
- 用户提到或暗示：slack bot
- 用户提到或暗示：slack app
- 用户提到或暗示：bolt framework
- 用户提到或暗示：block kit
- 用户提到或暗示：slash command
- 用户提到或暗示：slack webhook
- 用户提到或暗示：slack workflow
- 用户提到或暗示：slack interactive
- 用户提到或暗示：slack oauth

## 局限性
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来要求澄清。
