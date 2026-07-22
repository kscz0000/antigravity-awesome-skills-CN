---
name: robot-framework-skill
description: '使用 Python 生成 Robot Framework 关键字驱动语法的测试。支持 SeleniumLibrary、RequestsLibrary 和自定义关键字。当用户提到 "Robot Framework"、"*** Test Cases ***"、"SeleniumLibrary"、".robot file" 时使用。触发词：Robot Framework、*** Test Cases ***、SeleniumLibrary、.robot 文件'
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/robot-framework-skill
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# Robot Framework 技能
## 何时使用

当你需要使用 Python 生成 Robot Framework 关键字驱动语法的测试时使用本技能。支持 SeleniumLibrary、RequestsLibrary 和自定义关键字。当用户提到 "Robot Framework"、"*** Test Cases ***"、"SeleniumLibrary"、".robot file" 时使用。触发词：Robot Framework、*** Test Cases ***、SeleniumLibrary、.robot 文件。

**典型使用场景**：编写 Web 自动化用例、接口回归脚本、数据驱动批量验证、与 LambdaTest 云端执行环境集成、为既有 Python 测试代码补充关键字层封装，或者排查 `*** Test Cases ***` 区块内的失败用例。


关于 TestMu AI 云端执行，请参阅 [reference/cloud-integration.md](https://github.com/LambdaTest/agent-skills/tree/main/robot-framework-skill/reference/cloud-integration.md) 和 [shared/testmu-cloud-reference.md](https://github.com/LambdaTest/agent-skills/tree/main/robot-framework-skill/../shared/testmu-cloud-reference.md)。

## 核心模式

### 基础测试 (tests/login.robot)

```robot
*** Settings ***
Library    SeleniumLibrary
Suite Setup    Open Browser    ${BASE_URL}    chrome
Suite Teardown    Close All Browsers

*** Variables ***
${BASE_URL}    http://localhost:3000
${EMAIL}       user@test.com
${PASSWORD}    password123

*** Test Cases ***
Login With Valid Credentials
    Go To    ${BASE_URL}/login
    Wait Until Element Is Visible    id:email    10s
    Input Text    id:email    ${EMAIL}
    Input Text    id:password    ${PASSWORD}
    Click Button    css:button[type='submit']
    Wait Until Element Is Visible    css:.dashboard    10s
    Page Should Contain    Welcome
    Location Should Contain    /dashboard

Login With Invalid Credentials Shows Error
    Go To    ${BASE_URL}/login
    Input Text    id:email    wrong@test.com
    Input Text    id:password    wrong
    Click Button    css:button[type='submit']
    Wait Until Element Is Visible    css:.error    5s
    Element Should Contain    css:.error    Invalid credentials
```

### 自定义关键字

```robot
*** Keywords ***
Login As User
    [Arguments]    ${email}    ${password}
    Go To    ${BASE_URL}/login
    Input Text    id:email    ${email}
    Input Text    id:password    ${password}
    Click Button    css:button[type='submit']

Verify Dashboard Is Displayed
    Wait Until Element Is Visible    css:.dashboard    10s
    Page Should Contain    Welcome

*** Test Cases ***
Valid Login Flow
    Login As User    user@test.com    password123
    Verify Dashboard Is Displayed
```

### 数据驱动测试（模板）

```robot
*** Test Cases ***
Login With Various Users
    [Template]    Login And Verify
    admin@test.com    admin123    Dashboard
    user@test.com     pass123     Dashboard
    bad@test.com      wrong       Error

*** Keywords ***
Login And Verify
    [Arguments]    ${email}    ${password}    ${expected}
    Login As User    ${email}    ${password}
    Page Should Contain    ${expected}
```

### API 测试（RequestsLibrary）

```robot
*** Settings ***
Library    RequestsLibrary

*** Test Cases ***
Get Users Returns 200
    ${response}=    GET    ${API_URL}/users    expected_status=200
    Should Not Be Empty    ${response.json()['users']}

Create User
    ${body}=    Create Dictionary    name=Alice    email=alice@test.com
    ${response}=    POST    ${API_URL}/users    json=${body}    expected_status=201
    Should Be Equal    ${response.json()['name']}    Alice
```

### 云端配置

```robot
*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${REMOTE_URL}    https://%{LT_USERNAME}:%{LT_ACCESS_KEY}@hub.lambdatest.com/wd/hub

*** Keywords ***
Open Cloud Browser
    ${caps}=    Create Dictionary
    ...    browserName=chrome    browserVersion=latest
    ...    LT:Options=${{{"build":"Robot Build","name":"Login Test","platform":"Windows 11","video":True}}}
    Open Browser    ${BASE_URL}    remote_url=${REMOTE_URL}    desired_capabilities=${caps}
```

## 安装：`pip install robotframework robotframework-seleniumlibrary robotframework-requests`
## 运行：`robot tests/` 或 `robot --include smoke tests/`
## 报告：`report.html` 和 `log.html` 自动生成

## 进阶模式

如果示例章节覆盖不到你的真实场景，请阅读 `reference/playbook.md` 中的完整章节。下表简要列出每一章提供的核心要点，便于快速定位所需内容：

| 章节 | 章节标题（中文） | 你将获得的核心要点 |
|------|----------------|--------------------|
| §1 项目设置 | 项目初始化与目录结构 | 标准的 Robot Framework 项目骨架、变量文件的组织方式、常用执行命令、pabot 并行执行接入 |
| §2 Web UI 测试 | 基于 SeleniumLibrary 的浏览器测试 | 使用 Page Objects 模式编写登录流程、处理动态内容与异步等待、模态框与会话管理 |
| §3 API 测试 | 基于 RequestsLibrary 的接口测试 | 完整 CRUD 用例编写、统一错误处理、响应字段校验、Token 认证与会话保持 |
| §4 数据驱动测试 | 多数据集驱动的测试组织 | DataDriver 库读取 CSV、外部数据源接入、FOR 循环与批量断言写法 |
| §5 自定义 Python 库 | 扩展关键字能力 | 使用 `@keyword` 装饰器封装 Python 函数、资源追踪（setup/teardown）、测试数据生成器 |
| §6 Browser Library | 基于 Playwright 的现代浏览器库 | 内置等待与重试机制、网络请求拦截、响应式布局校验、移动端模拟 |
| §7 LambdaTest 集成 | LambdaTest 云端平台对接 | 远程浏览器能力配置、跨浏览器矩阵套件、测试状态实时上报 |
| §8 CI/CD 集成 | 持续集成流水线接入 | GitHub Actions 矩阵策略、pabot 并行执行、报告合并与产物归档 |
| §9 调试速查表 | 常见问题排查指南 | 12 类典型故障的现象、根因与修复方法 |
| §10 最佳实践 | Robot Framework 工程规范 | 14 项自检清单，覆盖命名、复用、稳定性、可维护性 |

## 使用限制

本技能聚焦 Robot Framework 关键字驱动测试场景，并不替代通用的软件工程判断。请在使用时遵循以下边界：

- **适用范围**：仅当任务与上游源码及本地项目上下文明确匹配时，才可使用本技能。若涉及非 Robot Framework 的测试体系（如 pytest、Playwright 原生脚本等），请改用对应技能或直接编写 Python 代码。
- **落地前校验**：在落地变更前，请校验命令、生成的代码、依赖、凭证以及外部服务的行为。尤其要确认 `pip install` 引入的库版本与 Robot Framework 主版本兼容，并验证远程浏览器节点的可用性。
- **示例的边界**：示例代码不能替代面向具体环境的测试、安全审查，也无法替代用户对破坏性或高成本操作的审批。生产环境的密钥、Token、构建产物路径均不可直接复用示例中的占位符。