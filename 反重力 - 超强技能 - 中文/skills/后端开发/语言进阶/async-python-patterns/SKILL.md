---
name: async-python-patterns
description: "使用 asyncio、并发编程模式和 async/await 实现异步 Python 应用的综合指南，用于构建高性能、非阻塞系统。触发词：异步Python、asyncio、async await、协程、并发编程、异步编程、Python异步、事件循环、async patterns、异步模式、并发模式、非阻塞IO。"
risk: safe
source: community
date_added: "2026-02-27"
---

# Async Python Patterns

使用 asyncio、并发编程模式和 async/await 实现异步 Python 应用的综合指南，用于构建高性能、非阻塞系统。

## 使用此技能的场景

- 构建异步 Web API（FastAPI、aiohttp、Sanic）
- 实现并发 I/O 操作（数据库、文件、网络）
- 创建支持并发请求的网络爬虫
- 开发实时应用（WebSocket 服务器、聊天系统）
- 同时处理多个独立任务
- 构建具有异步通信的微服务
- 优化 I/O 密集型工作负载
- 实现异步后台任务和队列

## 不使用此技能的场景

- 工作负载为 CPU 密集型且 I/O 较少
- 简单的同步脚本已足够
- 运行环境无法支持 asyncio/事件循环

## 指导说明

- 明确工作负载特征（I/O vs CPU）、目标和运行时约束
- 选择并发模式（tasks、gather、queues、pools）并设置取消规则
- 添加超时、背压机制和结构化错误处理
- 包含异步代码路径的测试和调试指导
- 如需详细示例，请参阅 `resources/implementation-playbook.md`

详细模式和示例请参阅 `resources/implementation-playbook.md`。

## 资源

- `resources/implementation-playbook.md` 包含详细的模式和示例。

## 局限性

- 仅当任务明确符合上述描述范围时使用此技能
- 输出内容不能替代环境特定的验证、测试或专家评审
- 如缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清
