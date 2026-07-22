---
name: python-patterns
description: "Python 惯用写法、最佳实践与编码规范，用于构建健壮、高效、可维护的 Python 应用程序。适用于 Python 模式、Python 最佳实践、Python 开发、Python 代码规范、Python 惯用写法。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Python Patterns

> 2025 年 Python 开发原则与决策指南。
> **学会思考，而不是背诵模式。**

## 适用场景
在做 Python 架构决策、选择框架、设计异步模式或组织项目结构时使用本技能。

---

## ⚠️ 如何使用本技能

本技能教你**决策原则**，而不是照搬现成代码。

- 拿不准时，先问用户偏好哪个框架
- 根据实际场景选择异步还是同步
- 不要每次都想当然地用同一个框架

---

## 1. 框架选型（2025）

### 决策树

```
你在做什么？
│
├── API 优先 / 微服务
│   └── FastAPI（异步、现代、快）
│
├── 全栈 Web / CMS / 后台管理
│   └── Django（全家桶）
│
├── 简单项目 / 脚本 / 学习
│   └── Flask（轻量、灵活）
│
├── AI/ML API 服务
│   └── FastAPI（Pydantic、异步、uvicorn）
│
└── 后台任务
    └── Celery + 任意框架
```

### 对比原则

| 维度 | FastAPI | Django | Flask |
|------|---------|--------|-------|
| **最适合** | API、微服务 | 全栈、CMS | 简单项目、学习 |
| **异步** | 原生支持 | Django 5.0+ | 通过扩展 |
| **后台管理** | 手动实现 | 内置 | 通过扩展 |
| **ORM** | 自选 | Django ORM | 自选 |
| **学习曲线** | 低 | 中 | 低 |

### 选型时要问的问题：
1. 纯 API 还是全栈？
2. 需要后台管理界面吗？
3. 团队熟不熟异步？
4. 有没有现成的基础设施？

---

## 2. 异步 vs 同步决策

### 何时使用异步

```
async def 更好的场景：
├── I/O 密集操作（数据库、HTTP、文件）
├── 大量并发连接
├── 实时功能
├── 微服务间通信
└── FastAPI/Starlette/Django ASGI

def（同步）更好的场景：
├── CPU 密集操作
├── 简单脚本
├── 老旧代码库
├── 团队不熟悉异步
└── 阻塞式库（没有异步版本）
```

### 黄金法则

```
I/O 密集 → async（等待外部响应）
CPU 密集 → sync + multiprocessing（纯计算）

不要：
├── 随意混用同步和异步
├── 在异步代码里用同步库
└── 对 CPU 密集任务强行异步
```

### 异步库选择

| 需求 | 异步库 |
|------|--------|
| HTTP 客户端 | httpx |
| PostgreSQL | asyncpg |
| Redis | aioredis / redis-py async |
| 文件 I/O | aiofiles |
| 数据库 ORM | SQLAlchemy 2.0 async、Tortoise |

---

## 3. 类型标注策略

### 何时标注类型

```
必须标注：
├── 函数参数
├── 返回值
├── 类属性
├── 公开 API

可以省略：
├── 局部变量（让类型推断自己搞定）
├── 一次性脚本
├── 测试代码（通常）
```

### 常见类型模式

```python
# 这些是模式，理解它们：

# Optional → 可能是 None
from typing import Optional
def find_user(id: int) -> Optional[User]: ...

# Union → 多种类型之一
def process(data: str | dict) -> None: ...

# 泛型集合
def get_items() -> list[Item]: ...
def get_mapping() -> dict[str, int]: ...

# Callable
from typing import Callable
def apply(fn: Callable[[int], str]) -> str: ...
```

### 用 Pydantic 做校验

```
何时使用 Pydantic：
├── API 请求/响应模型
├── 配置/设置
├── 数据校验
├── 序列化

好处：
├── 运行时校验
├── 自动生成 JSON schema
├── 与 FastAPI 原生集成
└── 清晰的错误信息
```

---

## 4. 项目结构原则

### 结构选择

```
小项目 / 脚本：
├── main.py
├── utils.py
└── requirements.txt

中型 API：
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── schemas/
├── tests/
└── pyproject.toml

大型应用：
├── src/
│   └── myapp/
│       ├── core/
│       ├── api/
│       ├── services/
│       ├── models/
│       └── ...
├── tests/
└── pyproject.toml
```

### FastAPI 项目结构原则

```
按功能或分层组织：

按分层：
├── routes/（API 端点）
├── services/（业务逻辑）
├── models/（数据库模型）
├── schemas/（Pydantic 模型）
└── dependencies/（共享依赖）

按功能：
├── users/
│   ├── routes.py
│   ├── service.py
│   └── schemas.py
└── products/
    └── ...
```

---

## 5. Django 原则（2025）

### Django 异步（Django 5.0+）

```
Django 支持异步：
├── 异步视图
├── 异步中间件
├── 异步 ORM（有限）
└── ASGI 部署

何时在 Django 中使用异步：
├── 外部 API 调用
├── WebSocket（Channels）
├── 高并发视图
└── 触发后台任务
```

### Django 最佳实践

```
模型设计：
├── 胖模型、瘦视图
├── 用 Manager 封装常用查询
├── 用抽象基类复用公共字段

视图：
├── 复杂 CRUD 用类视图
├── 简单端点用函数视图
├── 配合 DRF 使用 ViewSet

查询：
├── FK 用 select_related()
├── M2M 用 prefetch_related()
├── 避免 N+1 查询
└── 指定字段用 .only()
```

---

## 6. FastAPI 原则

### FastAPI 中的 async def vs def

```
用 async def 的场景：
├── 使用异步数据库驱动
├── 发起异步 HTTP 调用
├── I/O 密集操作
└── 需要处理并发

用 def 的场景：
├── 阻塞式操作
├── 同步数据库驱动
├── CPU 密集任务
└── FastAPI 会自动放到线程池里跑
```

### 依赖注入

```
用依赖注入处理：
├── 数据库会话
├── 当前用户 / 认证
├── 配置
├── 共享资源

好处：
├── 可测试（mock 依赖）
├── 清晰的职责分离
├── 自动清理（yield）
```

### Pydantic v2 集成

```python
# FastAPI + Pydantic 紧密集成：

# 请求校验
@app.post("/users")
async def create(user: UserCreate) -> UserResponse:
    # user 已经被校验过了
    ...

# 响应序列化
# 返回类型就是响应 schema
```

---

## 7. 后台任务

### 选型指南

| 方案 | 最适合 |
|------|--------|
| **BackgroundTasks** | 简单的进程内任务 |
| **Celery** | 分布式、复杂工作流 |
| **ARQ** | 异步、基于 Redis |
| **RQ** | 简单的 Redis 队列 |
| **Dramatiq** | 基于 Actor，比 Celery 更简单 |

### 各方案适用场景

```
FastAPI BackgroundTasks：
├── 快速操作
├── 不需要持久化
├── 即发即忘
└── 同进程

Celery/ARQ：
├── 长时间运行的任务
├── 需要重试逻辑
├── 分布式 Worker
├── 持久化队列
└── 复杂工作流
```

---

## 8. 错误处理原则

### 异常策略

```
在 FastAPI 中：
├── 创建自定义异常类
├── 注册异常处理器
├── 返回统一的错误格式
└── 记录日志但不暴露内部细节

模式：
├── 在 Service 层抛出领域异常
├── 在 Handler 中捕获并转换
└── 客户端拿到干净的错误响应
```

### 错误响应哲学

```
要包含：
├── 错误码（程序用）
├── 消息（人读的）
├── 详情（适用时给出字段级别信息）
└── 不要给堆栈跟踪（安全问题）
```

---

## 9. 测试原则

### 测试策略

| 类型 | 目的 | 工具 |
|------|------|------|
| **单元测试** | 业务逻辑 | pytest |
| **集成测试** | API 端点 | pytest + httpx/TestClient |
| **端到端测试** | 完整工作流 | pytest + DB |

### 异步测试

```python
# 用 pytest-asyncio 做异步测试

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/users")
        assert response.status_code == 200
```

### Fixture 策略

```
常用 Fixture：
├── db_session → 数据库连接
├── client → 测试客户端
├── authenticated_user → 带 Token 的用户
└── sample_data → 测试数据准备
```

---

## 10. 决策清单

动手写代码之前：

- [ ] **问过用户偏好哪个框架了吗？**
- [ ] **是根据当前场景选的框架吗？**（而不是默认套一个）
- [ ] **决定用异步还是同步了吗？**
- [ ] **规划好类型标注策略了吗？**
- [ ] **确定项目结构了吗？**
- [ ] **规划好错误处理了吗？**
- [ ] **考虑过后台任务了吗？**

---

## 11. 要避免的反模式

### ❌ 别这样：
- 简单 API 也无脑用 Django（FastAPI 可能更合适）
- 在异步代码里用同步库
- 公开 API 不标类型
- 把业务逻辑塞进路由/视图
- 忽视 N+1 查询
- 随意混用异步和同步

### ✅ 要这样：
- 根据场景选框架
- 先问清楚异步需求
- 用 Pydantic 做校验
- 关注点分离（路由 → 服务 → 仓库）
- 测试关键路径

---

> **记住**：Python 模式的核心是根据你的具体场景做决策。不要照搬代码——想想什么对你的应用最有利。

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为对特定环境验证、测试或专家评审的替代。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
