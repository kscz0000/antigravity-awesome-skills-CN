---
name: github-actions-debugger
description: "专用技能，通过解析运行日志与流水线定义，对失败的 GitHub Actions workflow 进行诊断、分析与修复。触发词：GitHub Actions、CI/CD、workflow 调试、流水线失败、Actions 排错、CI 排障、run 日志诊断、YAML 修复。"
category: devops
risk: safe
source: community
source_type: community
date_added: "2026-06-25"
author: Owais
tags: [github-actions, ci-cd, devops, debugging, workflows]
tools: [claude, cursor, gemini, antigravity]
---

# GitHub Actions 流水线调试器

## 概览

本技能扮演一名专家级的 CI/CD 诊断师角色。它专注于读取失败的 GitHub Actions 原始日志、定位崩溃或失败的根因，并输出精确的 YAML 或代码修改方案以修复流水线。

## 适用场景

- GitHub Actions workflow 意外失败，且错误日志冗长、晦涩或具有误导性时使用。
- CI 中排查依赖版本不匹配、缺失密钥、缓存问题或 runner 环境故障时使用。
- 识别 workflow 步骤中的瓶颈以优化慢流水线时使用。
- 更新和升级已弃用的 action 或 workflow 语法时使用。

## 工作机制

1. **日志接入与脱敏：** 分析所提供的 GitHub Actions workflow 日志（通常以原始文本文件导出或直接粘贴）。**关键安全要求：** 用户/智能体必须在粘贴或上传日志之前，对其中所有敏感凭据、密钥、token、私钥以及内部系统路径进行脱敏处理。
2. **上下文映射：** 将失败点与 `.github/workflows/*.yml` 定义中对应的具体 step 和 job 进行交叉对照。
3. **根因分析：** 判定失败是否由以下原因导致：
   - 密钥缺失或配置错误（`${{ secrets.API_KEY }}`）。
   - Node/Python/OS 环境版本不匹配。
   - 不稳定的测试或超时限制过短。
   - 在 `run:` 块中执行的 bash 脚本存在语法错误。
   - action 版本失效或已弃用。
4. **修复方案：** 针对需要修改的 `.yml` 文件或底层脚本，给出直接的 `diff`。

## 最佳实践

- **提供完整上下文：** 始终同时审阅 workflow 定义文件（`.yml`）和失败日志，以确保诊断准确。
- **检查 Action 版本：** 许多失败源于老旧第三方 action 中已弃用的运行时版本（例如老版 `actions/checkout@v2` 仍使用 Node.js 16）。应一律建议升级到最新的主版本（例如 `v4`）。
- **权限审计：** 若 workflow 需要向仓库、包或部署环境执行写入操作，确保其包含正确的 `permissions:` 块。
- **可复现性：** 若测试在 CI 中失败但本地通过，需排查环境差异，例如时区、无头浏览器状态、内存限制或并发执行中的竞态条件。

## 示例

### 示例 1：修复已弃用的 Node.js Action 版本错误
**失败日志：**
```text
Warning: The Go/Node.js/Python version used by this action is deprecated.
Error: Node.js 16 actions are deprecated. Please update to use Node.js 20.
```

**建议修复 Diff：**
```diff
      - name: Checkout Code
-        uses: actions/checkout@v2
+        uses: actions/checkout@v4
```

### 示例 2：诊断并修复缺失的仓库密钥
**失败日志：**
```text
Run npm run deploy
  npm run deploy
  shell: /usr/bin/bash -e {0}
Error: API Key is required for deployment. Process exited with code 1.
```

**建议修复 Diff：**
```diff
      - name: Deploy App
        run: npm run deploy
+        env:
+          DEPLOY_API_KEY: ${{ secrets.DEPLOY_API_KEY }}
```

## 安全注意事项

- **凭据泄露与原始日志脱敏：** 任何情况下，未经预先脱敏处理的原始日志（包括未掩码的密钥、私有 URL、部署目标或 token）都不得被处理。务必在接入前由用户或智能体完成全部敏感信息脱敏。
- **试运行模式：** 当建议修改 workflow 中的 bash 脚本步骤时，应当推荐增加 `--dry-run` 等标志，或在可能的情况下采用预演执行，以防止调试过程对下游环境产生非预期的副作用。

## 功能局限

- 该技能无法安全地读取仓库密钥。只有当日志中提示未定义的环境变量或身份验证失败时，才能反推出密钥缺失或格式错误。
- 技能本身无法直接执行 GitHub action 来验证修复；确认修复正确性需要将修改推送到仓库并触发一次 workflow 运行。
- 与网络相关的瞬时故障（例如包镜像站暂时不可用）若不仔细甄别，可能被误判为 workflow 结构性问题。

## 常见陷阱

- **忽视瞬时故障：** 将偶发的网络抖动或镜像站宕机（例如 npm 或 pip install 报错）误判为代码或配置缺陷。在进行大幅修改之前，应先观察重跑是否能够成功。
- **硬编码 Token：** 在修复身份验证错误时，直接将密钥或 API token 写死在 YAML 文件中，而不是使用 GitHub Secrets（`${{ secrets.SECRET_NAME }}`）。
- **忽略缓存副作用：** 忘记过期的缓存键可能持续加载已损坏的依赖。若依赖安装反复失败，可尝试在禁用 action 缓存的情况下重新执行一次 job。

## 相关技能

- `@devops-troubleshooter` —— 通用的 DevOps 与基础设施问题排查。
- `@cicd-automation-workflow-automate` —— 用于从零搭建全新的 CI/CD 流水线。
