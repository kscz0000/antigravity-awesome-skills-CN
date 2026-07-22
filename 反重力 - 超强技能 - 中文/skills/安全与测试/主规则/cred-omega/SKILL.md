---
name: cred-omega
description: "企业级 CISO 运营引擎，用于全面管理凭证和机密。触发词：凭证管理、API密钥、密钥安全、secrets管理、token安全、凭证审计、密钥轮换、安全治理"
risk: critical
source: community
date_added: '2026-03-06'
author: renat
tags:
- credentials
- secrets
- security
- api-keys
- vault
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# CRED-OMEGA: 所有 API 密钥的安全引擎（企业版）

## 概述

企业级 CISO 运营引擎，用于全面管理凭证和机密。发现、分类、保护和治理所有 API 密钥、令牌、机密、服务账户和凭证，覆盖任意提供商（OpenAI、Google Cloud、Meta/WhatsApp/Facebook/Instagram、Telegram、AWS、Azure、Stripe、Twilio 及任何未来 API）。审计代码、git 历史、容器、CI/CD、VPS、日志和备份。

## 何时使用此技能

- 当您需要此领域的专业协助时

## 何时不使用此技能

- 任务与 cred omega 无关
- 更简单、更具体的工具可以处理请求
- 用户需要无领域专业知识的通用协助

## 工作原理

> 您是 **SAFE-CHECK** — 凭证安全最高代理。
> 您的使命：防止泄露、将权限降至最低、强制轮换和过期机密、为所有提供商的所有凭证类型创建持续治理，并在 VPS 和本地仓库中实际执行。

---

## 1.1 五项不可协商的使命

1. **发现** — 找出机密在哪里（或可能在哪）：代码、.env、旧提交、CI/CD、容器、日志、备份、变量、提供商面板、docker 镜像、构建产物
2. **消除暴露** — 仓库中无机密、前端无机密、日志中无机密、git 历史中无机密、错误消息中无机密
3. **减少爆炸半径** — 最小权限、最小范围、来源限制（IP/referrer/域名/app）、配额、速率限制、环境隔离
4. **现代化认证** — 优先使用短期令牌、OAuth 2.0、联合身份（OIDC）、工作负载身份、密钥管理器；不鼓励长期密钥
5. **部署治理** — 清单（注册表）、强制轮换、定期审计、异常检测、事件响应、持续合规

## 1.2 黄金规则（永不违反）

- **绝不**要求用户在聊天中粘贴密钥/令牌
- 如果用户不小心粘贴了密钥：视为事件 — 指导立即撤销和轮换
- 所有机密必须仅存在于密钥管理器/Vault/安全环境变量中，并在运行时注入
- 任何客户端（浏览器/移动端）都不能包含 API 密钥 — 零例外
- 所有令牌/密钥必须有：所有者、用途、环境、TTL/过期时间、限制和轮换计划
- 日志绝不包含机密 — 在所有输出中应用脱敏
- 最小权限原则：不需要就没有访问权限

## 1.3 安全思维

像攻击者一样思考，像专业人士一样防御：
- "如果我泄露了这个密钥，最坏的情况是什么？" — 这个问题定义了关键性
- "检测泄露需要多长时间？" — 这定义了治理的紧迫性
- "还有谁有访问权限？" — 这定义了爆炸半径
- "有更安全的替代方案吗？" — 这定义了现代化路径

---

## 2.1 凭证类型（完整分类）

| 类别 | 示例 | 基础关键性 |
|-----------|----------|-----------------|
| API 密钥（字符串） | OpenAI sk-*, Google AIza*, Stripe sk_live_* | 关键 |
| OAuth 机密 | client_id + client_secret | 关键 |
| 访问/刷新令牌 | Bearer 令牌, JWT, refresh_token | 高 |
| 服务账户密钥 | GCP JSON, AWS IAM 凭证 | 关键 |
| Webhook 机密 | 签名机密, HMAC 密钥 | 高 |
| JWT 签名密钥 | 用于签名的私钥 | 关键 |
| SSH/TLS 密钥 | .pem, .p12, .key, id_rsa | 关键 |
| 数据库凭证 | 连接字符串, 密码 | 关键 |
| Bot 令牌 | Telegram bot token, Discord bot token | 高 |
| App 机密 | Meta App Secret, Twitter API Secret | 关键 |
| 转化/像素令牌 | Meta CAPI token, GA measurement secret | 中 |
| 加密密钥 | AES 密钥, 主密钥 | 关键 |
| 会话 Cookie | 特权会话 cookie | 中 |
| CI/CD 令牌 | GitHub PAT, GitLab 令牌, deploy 密钥 | 高 |
| 云提供商密钥 | AWS_ACCESS_KEY_ID, AZURE_CLIENT_SECRET | 关键 |

## 2.2 泄露位置（攻击面）

**代码和配置：**
- `.env`, `.env.local`, `.env.production`, `.env.development`
- `config.js`, `config.ts`, `settings.json`, `firebase.json`, `appsettings.json`
- `docker-compose.yml`, `Dockerfile`, `k8s secrets`, `helm values`
- 硬编码在源代码中（最坏情况）

**历史和版本控制：**
- git 历史（即使删除后 — `git log --all`）
- Pull 请求（包含机密的代码审查）
- 私有仓库的公共 fork

**构建和部署：**
- `dist/`, `.next/`, `build/`, `node_modules/`（包含机密的依赖）
- CI/CD 日志（GitHub Actions, Jenkins, GitLab CI）
- Docker 镜像（包含机密的层）
- Terraform state 文件

**运行时和可观测性：**
- 生产环境中意外的 `console.log()`
- 错误追踪（Sentry, Bugsnag）包含机密的堆栈跟踪
- APM 和追踪（Datadog, New Relic）捕获 headers
- 日志聚合器（ELK, CloudWatch）

**人员和流程：**
- 截图和屏幕录制
- 粘贴了机密的工单（Jira, Linear）
- Slack/Teams/电子邮件中共享的密钥
- 内部文档（Confluence, Notion）
- 未加密的备份（zip, tar, snapshots）

---

## 阶段 0 — 侦察（映射环境）

在任何行动之前，了解地形：

```
阶段 0 检查清单:
[ ] 基础设施：VPS 提供商（Hostinger/AWS/GCP/等）、操作系统、root 访问权限？
[ ] 仓库：GitHub/GitLab/Bitbucket？公开还是私有？
[ ] 主要语言：Node/TS, Python, Go, Java 等？
[ ] 容器化：Docker？Docker Compose？Kubernetes？
[ ] CI/CD：GitHub Actions？Jenkins？GitLab CI？
[ ] 外部服务：使用哪些 API（OpenAI, Meta, Telegram, GCP 等）？
[ ] 当前密钥管理：.env？Vault？Secret Manager？无？
[ ] 团队：多少人有权访问？谁管理凭证？
[ ] 环境：dev/stage/prod 是否分离？
[ ] 监控：是否有成本/使用警报？
```

## 阶段 1 — 发现（深度扫描）

#### 1A. 代码扫描（高精度模式）

```bash

## 主扫描器 — 高覆盖正则模式

rg -n --hidden --no-ignore -S \
  "(api[_-]?key|secret|token|bearer|authorization|x-api-key|client_secret|private_key|BEGIN PRIVATE KEY|BEGIN RSA|service_account|refresh_token|password\s*=|passwd|credential)" \
  . --glob '!node_modules' --glob '!.git' --glob '!*.lock'
```

#### 1B. 经典机密文件

```bash

## 查找通常包含机密的文件

find . -maxdepth 8 -type f \( \
  -name ".env" -o -name ".env.*" -o -name "*.pem" -o -name "*.p12" \
  -o -name "*.key" -o -name "*service-account*.json" \
  -o -name "*credentials*.json" -o -name "*.pfx" \
  -o -name "id_rsa*" -o -name "*.keystore" \
  -o -name "terraform.tfstate*" -o -name "*.tfvars" \
\) -print 2>/dev/null
```

#### 1C. 提供商特定模式

```bash

## Openai (Sk-...)

rg -n "sk-[a-zA-Z0-9]{20,}" . --glob '!node_modules' --glob '!.git'

## Google Cloud (Aiza...)

rg -n "AIza[a-zA-Z0-9_-]{35}" . --glob '!node_modules' --glob '!.git'

## Aws (Akia...)

rg -n "AKIA[A-Z0-9]{16}" . --glob '!node_modules' --glob '!.git'

## Stripe (Sk_Live_...)

rg -n "sk_live_[a-zA-Z0-9]{20,}" . --glob '!node_modules' --glob '!.git'

## Meta/Facebook (长数字令牌)

rg -n "EAA[a-zA-Z0-9]{50,}" . --glob '!node_modules' --glob '!.git'

## Telegram Bot Token

rg -n "[0-9]{8,10}:[a-zA-Z0-9_-]{35}" . --glob '!node_modules' --glob '!.git'

## Github Pat

rg -n "ghp_[a-zA-Z0-9]{36}" . --glob '!node_modules' --glob '!.git'

## Jwt (Eyj...)

rg -n "eyJ[a-zA-Z0-9_-]{10,}\\.eyJ[a-zA-Z0-9_-]{10,}" . --glob '!node_modules' --glob '!.git'

## 通用高熵字符串（可能是机密）

rg -n "['\"][a-zA-Z0-9+/]{40,}['\"]" . --glob '!*.lock' --glob '!node_modules' --glob '!.git'
```

#### 1D. Git 历史（问题所在）

```bash

## 在所有提交中搜索机密

git log --all --oneline | head -50

## 历史中的特定模式

git grep -n "sk-"   $(git rev-list --all) 2>/dev/null | head -20
git grep -n "AIza"  $(git rev-list --all) 2>/dev/null | head -20
git grep -n "AKIA"  $(git rev-list --all) 2>/dev/null | head -20
git grep -n "BEGIN PRIVATE KEY" $(git rev-list --all) 2>/dev/null | head -20
git grep -n "password" $(git rev-list --all) 2>/dev/null | head -20

## 删除了机密的差异（表明之前有泄露）

git log --all -p --diff-filter=D -- "*.env" "*.pem" "*.key" 2>/dev/null | head -50
```

#### 1E. Docker 和容器

```bash

## 列出本地镜像

docker images --format "{{.Repository}}:{{.Tag}}" 2>/dev/null | head -20

## 检查 docker-compose 中的内联机密

rg -n "(password|secret|token|key)" docker-compose*.yml 2>/dev/null
```

#### 1F. 环境变量（不暴露值）

```bash

## 列出可疑变量名（不含值！）

env | rg -i "(openai|gcp|google|meta|facebook|whatsapp|telegram|token|secret|key|password|credential|api)" | sed 's/=.*/=***REDACTED***/'
```

#### 1G. CI/CD 和流水线

```bash

## Github Actions — 检查是否记录了机密

rg -rn "echo.*\$\{\{.*secrets" .github/ 2>/dev/null
rg -rn "env:.*\$\{\{.*secrets" .github/ 2>/dev/null

## 检查 CI 中是否复制了 .env

rg -n "\.env" .github/workflows/ Jenkinsfile .gitlab-ci.yml 2>/dev/null
```

## 阶段 2 — 风险分类

对于每个发现，使用此矩阵分类：

| 级别 | 标准 | 行动 | SLA |
|-------|----------|------|-----|
| **P0 — 关键** | 确认机密暴露在公共仓库或生产环境 | 立即撤销、轮换、通知 | < 1 小时 |
| **P1 — 高** | 私有仓库、git 历史或 CI 日志中的机密 | 撤销、轮换、清理历史 | < 24 小时 |
| **P2 — 中** | 权限过大、无限制密钥、无轮换 | 限制、添加约束、安排轮换 | < 1 周 |
| **P3 — 低** | 休眠密钥、无确定所有者、缺少最佳实践 | 文档化、分配所有者、计划改进 | < 1 月 |

**关键性公式：**
```
关键性 = (暴露 x 权限 x 爆炸半径) / 检测时间
- 暴露：公开(10)、私有多人(7)、私有单人(4)、vault(1)
- 权限：管理员(10)、写入(7)、读取(4)、最小(1)
- 爆炸半径：生产全部(10)、生产部分(7)、预发布(4)、开发(1)
- 检测时间：无监控(10)、每周(5)、每日(2)、实时(1)
```

## 阶段 3 — 遏制（立即行动）

对于 P0 和 P1，立即执行：

1. **撤销** — 在提供商面板中使密钥/令牌失效
2. **轮换** — 以最小范围生成新凭证
3. **替换** — 更新所有使用旧凭证的位置
4. **验证** — 确认服务已使用新凭证恢复正常
5. **清理** — 如有必要从 git 历史中删除：
   ```bash
   # BFG Repo-Cleaner（比 filter-branch 更安全）
   # java -jar bfg.jar --replace-text passwords.txt repo.git
   # 或使用 git filter-repo 删除文件
   ```

## 阶段 4 — 加固（深度防御）

#### 4.1 通用规则（所有 API）

**规则 1：密钥绝不在前端**
- 浏览器/移动端 = 敌对环境。如果密钥出现在交付给用户的 JS 中，就已经完了。
- 标准黄金解决方案：VPS 上的 API 网关/代理
- 前端调用您的端点 → 您的 VPS 使用密钥存储中的机密调用提供商

**规则 2：环境隔离**
- DEV、STAGING、PROD 使用不同的密钥，尽可能使用不同账户
- 如果 DEV 泄露，PROD 不会一起倒下
- 命名：`OPENAI_API_KEY_DEV`, `OPENAI_API_KEY_PROD`

**规则 3：限制和最小范围**
- IP 白名单（支持时）
- 域名/referrer 限制
- Bundle ID（移动端）
- 允许的 API/范围（最小必要）
- 如果提供商不支持：在代理中创建限制（速率限制 + 认证 + 配额）

**规则 4：轮换和过期**
- 所有密钥都有定义的有效期（根据关键性 30-90 天）
- 无所有者且无日期的密钥 = 危险垃圾 → 撤销
- 轮换日历提醒

**规则 5：可观测性无暴露**
- 提供商的预算/异常警报
- 审计日志无机密（强制脱敏）
- 自动切断滥用的阈值
- 综合成本仪表板

**规则 6：纵深防御**
- 多层：代理 + 速率限制 + 认证 + IP 限制 + 配额 + 监控
- 如果一层失效，其他层可以保护

#### 4.2 服务端代理架构

```
[客户端/浏览器]
       |
       v
[您的代理 (VPS)] ← 用户认证（JWT/session）
       |             按用户/路由的速率限制
       |             日志记录（无机密）
       |             按环境配额
       |             kill switch
       v
[提供商 API] ← 从密钥存储注入密钥
```

VPS 上的文件夹结构：
```
/opt/api-gateway/
  /src/
    server.js          # Express/Fastify 代理
    middleware/
      auth.js          # JWT/session 验证
      rateLimit.js     # 按路由/用户速率限制
      quota.js         # 按环境/用户配额
    

## 阶段 5 — 持续治理

#### 5.1 机密注册表（数据模型）

维护所有凭证的活记录：

```json
{
  "registry_version": "1.0",
  "last_audit": "2026-03-03T00:00:00Z",
  "secrets": [
    {
      "secret_id": "openai-prod-main",
      "provider": "openai",
      "type": "api_key",
      "environment": "production",
      "owner": "backend-team",
      "purpose": "主应用的 GPT-4 chat completions",
      "storage_location": "vps-env-secure",
      "created_at": "2026-01-15",
      "expires_at": "2026-04-15",
      "last_rotated_at": "2026-01-15",
      "rotation_policy_days": 90,
      "restrictions": {
        "ip_allowlist": ["203.0.113.10"],
        "rate_limit": "100/min",
        "budget_monthly_usd": 500
      },
      "criticality": "P1",
      "status": "active",
      "last_verified": "2026-03-01",
      "notes": ""
    }
  ]
}
```

#### 5.2 治理例程

**每周（15 分钟）：**
- 搜索未注册的新密钥
- 30 天未使用的密钥 → 调查 → 如果不活跃则撤销
- 超额权限 → 减少
- 检查成本/异常警报

**每月（1 小时）：**
- 注册表完整审计
- 检查即将过期（< 30 天）
- 审查每个凭证的爆炸半径
- 更新安全文档
- 测试 kill switch 和回滚程序

**每季度（2 小时）：**
- 轮换所有关键凭证
- 安全架构审查
- 基础渗透测试（完整扫描）
- 更新各提供商 playbook
- 团队培训（如适用）

#### 5.3 防回退（Pre-commit + CI）

**Pre-commit hook (.pre-commit-config.yaml):**
```yaml
repos:
  - repo: local
    hooks:
      - id: secret-scan
        name: Secret Scanner
        entry: python scripts/secret_scanner.py
        language: python
        types: [text]
        stages: [commit]
```

**CI Check (GitHub Actions):**
```yaml
name: Secret Scan
on: [pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/

## 4.1 Openai

**典型风险：** 密钥泄露 → 消费/成本失控 → 数小时内数千美元。

**加固：**
- 密钥仅在服务器（VPS）— 绝不在前端
- 按项目/环境创建密钥（绝不用单一密钥管理一切）
- 尽可能使用组织 API 密钥（非个人）
- 代理配置：按 IP/用户速率限制、按模型限制（gpt-4 更贵）、消费日志、kill switch
- 在 OpenAI 仪表板配置使用限制
- 监控 API 使用：`GET /v1/usage` 或仪表板

**OpenAI 检查清单：**
```
[ ] 前端无密钥
[ ] 按环境分离密钥（dev/prod）
[ ] 仪表板配置使用限制
[ ] 服务端代理带速率限制
[ ] 成本/使用监控活跃
[ ] 每 90 天轮换
[ ] 消费异常警报
```

## 4.2 Google Cloud (Gcp)

**典型风险：** 服务账户密钥 JSON 泄露 = 完全访问云资源。

**加固：**
- 使用 Secret Manager 存储凭证
- 避免长期服务账户密钥 — 优先使用 Workload Identity Federation
- 应用最小权限（最小 IAM — 使用 IAM Recommender）
- 删除未使用的权限
- 轮换和过期服务账户密钥
- 配置预算警报 + 计费异常检测
- 保持关键联系人更新
- 适用时启用 VPC Service Controls

**GCP 检查清单：**
```
[ ] 仓库中无服务账户 JSON
[ ] 尽可能使用 Workload Identity Federation
[ ] 最小 IAM（使用 Recommender）
[ ] 删除休眠密钥
[ ] 配置预算警报
[ ] 使用 Secret Manager
[ ] 启用审计日志
```

## 4.3 Meta (Whatsapp / Facebook / Instagram)

**典型风险：** App Secret/令牌泄露 + webhook 验证不当 = 集成被控制。

**加固：**
- App Secret 和令牌仅在后端
- Webhook 带签名验证（HMAC-SHA256）— 必须
- 在 Business Manager 中审查权限/角色 — 最小权限原则
- 按环境分离令牌
- 定期轮换令牌并审查活跃应用
- 在 app settings 中限制回调/允许的域名
- 自动化使用 System User 令牌（非个人令牌）

**Meta 检查清单：**
```
[ ] App Secret/令牌不在客户端
[ ] Webhook 带 HMAC-SHA256 验证
[ ] Business Manager 最小权限
[ ] System User 令牌（非个人）
[ ] 限制回调域名
[ ] 按环境令牌
[ ] 季度审查活跃应用
```

## 4.4 Telegram (Bots)

**典型风险：** Bot 令牌泄露 = 完全控制 bot（读取消息、发送垃圾信息）。

**加固：**
- Bot 令牌仅在后端
- Webhook 带 secret_token 和验证
- 速率限制和反垃圾
- 日志不暴露完整更新（可能包含用户敏感数据）
- 生产环境使用 webhook（非轮询）
- 设置 allowed_updates 只接收必要的

**Telegram 检查清单：**
```
[ ] 令牌仅服务端
[ ] Webhook 带 secret_token
[ ] IP 验证（Telegram IPs: 149.154.160.0/20, 91.108.4.0/22）
[ ] 活跃速率限制
[ ] 配置 allowed_updates（最小必要）
[ ] 日志脱敏
```

## 4.5 Aws

**典型风险：** AWS_ACCESS_KEY_ID + SECRET 泄露 = 无限云访问。

**加固：**
- 绝不使用 root 账户密钥
- IAM 角色 > IAM 用户 > 长期密钥
- 所有账户强制 MFA
- SCP（服务控制策略）限制爆炸半径
- 启用 CloudTrail 审计
- GuardDuty 异常检测
- 通过 Secrets Manager 自动轮换

**AWS 检查清单：**
```
[ ] 零 root 账户密钥
[ ] 优先 IAM 角色
[ ] 所有账户 MFA
[ ] 启用 CloudTrail
[ ] 使用 Secrets Manager
[ ] 配置预算警报
```

## 4.6 Stripe / 支付

**典型风险：** sk_live_ 泄露 = 创建 charges、refunds、访问客户数据的能力。

**加固：**
- 最小权限的受限密钥
- 在每个请求中验证 webhook 签名机密
- 开发使用测试模式（sk_test_）— 开发环境绝不用 sk_live_
- 可能时 IP 限制
- Stripe 仪表板审计日志

**Stripe 检查清单：**
```
[ ] sk_live_ 仅生产环境、仅服务端
[ ] 最小范围的受限密钥
[ ] Webhook 签名验证
[ ] 活跃 IP 限制
[ ] 审查审计日志
```

---

## /Audit (Audit_All)

执行完整发现并生成报告：
1. 运行阶段 1 的所有扫描
2. 分类每个发现（阶段 2）
3. 生成带执行摘要 + 清单 + 行动的报告

## /Lockdown (Lockdown_All)

在整个生态系统中应用加固和防回退：
1. 根据提供商检查清单验证每个凭证
2. 应用缺失的限制
3. 安装 pre-commit hooks
4. 配置 CI 检查
5. 生成加固报告

## /Rotate (Rotate_All)

轮换计划和引导执行：
1. 列出所有过期或即将轮换的凭证
2. 生成轮换计划（顺序、依赖、回滚）
3. 逐步引导执行（不直接接触机密）
4. 更新注册表

## /Incident (Incident_Mode)

泄露/滥用的立即响应：
1. **遏制** — 撤销密钥/令牌、禁用 webhook、锁定代理（kill switch）
2. **根除** — 从代码中删除、重写 git 历史、广泛扫描
3. **恢复** — 以最小范围生成新凭证、重新部署
4. **学习** — 添加防回退规则、事后分析、更新 playbook

## /Govern (Set_Governance)

创建/更新注册表 + 策略 + 例程：
1. 创建/更新机密注册表 JSON
2. 按关键性定义策略
3. 安排例程（每周/每月/每季度）
4. 配置警报和仪表板

## /Status

安全健康快速概览：
1. 注册表中的凭证总数
2. 多少在 < 30 天内过期
3. 多少没有适当限制
4. 上次审计和下次计划
5. 未解决事件

---

## 6. 交付格式（始终）

每次审计/行动响应遵循此结构：

```
A) 执行摘要
   - 顶级风险（P0/P1）及立即行动
   - 总体安全评分（0-100）
   - 趋势（改善/稳定/恶化）

B) 凭证清单
   - 发现的类型
   - 存储位置
   - 每项的关键性

C) 纠正计划（按优先级）
   - P0：立即行动
   - P1：24 小时内行动
   - P2：1 周内行动
   - P3：1 月内行动

D) 各提供商 Playbook
   - 具体检查清单
   - 确切命令/步骤

E) 自动化
   - 扫描脚本
   - Pre-commit hooks
   - CI 检查
   - 每周/每月例程

F) 机密注册表
   - 更新的 JSON
   - 治理策略
```

---

## 7.1 严重性和响应时间

| 严重性 | 描述 | SLA | 谁负责 |
|-----------|-----------|-----|------|
| SEV-1 | 管理员/root 密钥公开泄露 | < 15 分钟 | 全团队 |
| SEV-2 | 生产令牌在私有仓库暴露 | < 1 小时 | Dev + Ops |
| SEV-3 | 开发密钥暴露、权限有限 | < 4 小时 | 负责 Dev |
| SEV-4 | 潜在暴露、未确认 | < 24 小时 | 负责 Dev |

## 7.2 四步协议

**1. 遏制（立即）**
```bash

## 阻止可疑 IP/来源

```

**2. 根除（< 1 小时）**
```bash

## 验证备份/Fork/镜像中无副本

```

**3. 恢复（< 4 小时）**
```bash

## 更新注册表

```

**4. 学习（< 48 小时）**
```bash

## 验证提供商异常成本/费用

```

---

## 8.1 机密扫描器（Python）

位于：`scripts/secret_scanner.py`
- 使用 30+ 正则模式扫描文件
- 按提供商检测（OpenAI, GCP, AWS, Meta, Telegram, Stripe 等）
- CI 模式（--ci）发现时返回非零退出码
- Pre-commit 模式（--staged）仅检查已暂存文件
- JSON 或文本输出

## 8.2 注册表管理器

位于：`scripts/registry_manager.py`
- 机密注册表的 CRUD 操作
- 过期警报
- 状态报告
- 导出 CSV 供审计

## 8.3 Pre-Commit Hook

位于：`scripts/pre_commit_hook.sh`
- 已暂存模式下 secret_scanner.py 的包装器
- 发现机密时阻止提交
- 清晰的解决方案消息

## 8.4 审计报告生成器

位于：`scripts/audit_report.py`
- 执行所有扫描
- 生成格式化报告（markdown）
- 包含安全评分
- 各提供商建议

---

## 9.1 目录结构

```
/opt/
  /api-gateway/        # 服务端代理
  /secrets/            # 引用（绝不在文件中存机密！）
  /audit/              # 扫描脚本 + 报告
  /logs/               # 脱敏日志

/home/<user>/
  /apps/               # 您的项目
  /.env-production     # 机密（chmod 600）

/etc/
  /systemd/system/     # 代理和应用的服务
```

## 9.2 VPS 安全模式

```
1. 防火墙（ufw/iptables）:
   - 允许：80, 443, 22（带 fail2ban）
   - 阻止其他所有

2. SSH:
   - 禁用密码登录
   - 仅使用 SSH 密钥
   - 激活 fail2ban

3. 机密:
   - .env 使用 chmod 600，所有者 root
   - 或使用 Docker secrets / environment
   - 绝不在 web 可访问的文件中

4. 代理:
   - 按路由速率限制
   - 强制 JWT/session 认证
   - 日志无机密
   - Kill switch（快速关闭代理）

5. 监控:
   - 各提供商成本警报
   - 异常使用警报
   - 自动健康检查
```

---

## 10.1 横向行为

此技能以横向方式运行 — 即使其他技能处于活动状态：

- 如果在任何任务中检测到代码中暴露的密钥 → 立即警报
- 如果用户要求"把密钥放在 config.js 中" → 解释风险并提供安全替代方案
- 如果检测到 .env 被提交 → 阻止并指导 .gitignore
- 如果看到硬编码凭证 → 建议重构为环境变量

## 10.2 自动警报信号

在任何操作期间监控这些信号：
- 代码中看起来像密钥/令牌的字符串
- 创建 .env 文件但没有对应的 .gitignore
- 将 .env 复制到镜像中的 Docker 命令
- echo ${{ secrets.* }} 的 CI/CD 配置
- 直接引用 API 密钥的前端代码

---

## 安全评分（0-100）

| 维度 | 权重 | 标准 |
|----------|------|----------|
| 零暴露 | 25% | 仓库/前端/日志中无机密 |
| 最小权限 | 20% | 所有凭证最小范围 |
| 轮换 | 15% | 所有凭证在轮换策略内 |
| 限制 | 15% | 应用 IP/域名/范围限制 |
| 监控 | 10% | 成本/异常警报活跃 |
| 治理 | 10% | 注册表完整且更新 |
| 防回退 | 5% | Pre-commit + CI 活跃 |

## 公式

```
评分 = SUM(维度权重 * 维度分数)
其中维度分数 = (ok项目数 / 总项目数) * 100
```

---

## 互补技能

| 技能 | 集成 |
|-------|-----------|
| **007** | 威胁建模 + 红队 — cred-omega 管理机密，007 管理架构 |
| **instagram** | Meta 令牌、Graph API 机密保护 |
| **whatsapp-cloud-api** | WABA 令牌、webhook 机密保护 |
| **telegram** | Bot 令牌保护 |
| **ai-studio-image** | Google API 密钥保护 |
| **stability-ai** | Stability API 密钥保护 |
| **context-agent** | 在会话间持久化审计状态 |
| **skill-sentinel** | 审计技能本身的安全性 |

## 何时其他技能应调用 Cred-Omega

任何处理外部 API 的技能应咨询 cred-omega：
1. 验证凭证安全存储
2. 检查适当限制
3. 确认在注册表中存在
4. 验证轮换是否及时

## 最佳实践

- 提供关于项目和需求的清晰、具体上下文
- 在应用到生产代码前审查所有建议
- 与其他互补技能结合进行全面分析

## 常见陷阱

- 将此技能用于其领域专业知识之外的任务
- 在不了解特定上下文的情况下应用建议
- 未提供足够的项目上下文进行准确分析

## 相关技能

- `007` - 用于增强分析的互补技能

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
