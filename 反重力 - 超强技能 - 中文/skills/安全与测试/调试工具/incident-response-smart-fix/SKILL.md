---
name: incident-response-smart-fix
description: "基于多智能体编排的智能问题排查与修复工作流，结合AI辅助调试工具和可观测性平台系统性诊断和解决生产问题。当用户要求'智能问题排查'、'多智能体调试'、'生产问题修复'、'根因分析'、'事件响应'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 基于多智能体编排的智能问题排查与修复

[Extended thinking: This workflow implements a sophisticated debugging and resolution pipeline that leverages AI-assisted debugging tools and observability platforms to systematically diagnose and resolve production issues. The intelligent debugging strategy combines automated root cause analysis with human expertise, using modern 2024/2025 practices including AI code assistants (GitHub Copilot, Claude Code), observability platforms (Sentry, DataDog, OpenTelemetry), git bisect automation for regression tracking, and production-safe debugging techniques like distributed tracing and structured logging. The process follows a rigorous four-phase approach: (1) Issue Analysis Phase - error-detective and debugger agents analyze error traces, logs, reproduction steps, and observability data to understand the full context of the failure including upstream/downstream impacts, (2) Root Cause Investigation Phase - debugger and code-reviewer agents perform deep code analysis, automated git bisect to identify introducing commit, dependency compatibility checks, and state inspection to isolate the exact failure mechanism, (3) Fix Implementation Phase - domain-specific agents (python-pro, typescript-pro, rust-expert, etc.) implement minimal fixes with comprehensive test coverage including unit, integration, and edge case tests while following production-safe practices, (4) Verification Phase - test-automator and performance-engineer agents run regression suites, performance benchmarks, security scans, and verify no new issues are introduced. Complex issues spanning multiple systems require orchestrated coordination between specialist agents (database-optimizer → performance-engineer → devops-troubleshooter) with explicit context passing and state sharing. The workflow emphasizes understanding root causes over treating symptoms, implementing lasting architectural improvements, automating detection through enhanced monitoring and alerting, and preventing future occurrences through ty[... 241 chars omitted ...]

## 使用此技能的场景

- 处理基于多智能体编排的智能问题排查与修复任务或工作流
- 需要相关指导、最佳实践或检查清单

## 不使用此技能的场景

- 任务与多智能体编排的智能问题排查无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 资源

- `resources/implementation-playbook.md` 包含详细的模式和示例。

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 输出不能替代针对特定环境的验证、测试或专家评审。
- 若缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
