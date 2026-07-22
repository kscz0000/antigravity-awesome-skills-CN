---
name: sast-configuration
description: "静态应用安全测试（SAST）工具的安装、配置与自定义规则创建，支持多种编程语言的全面安全扫描。触发词：SAST配置、静态安全扫描、Semgrep配置、SonarQube配置、CodeQL配置、安全规则创建、CI/CD安全集成、代码安全扫描、安全门禁、合规扫描"
risk: unknown
source: community
date_added: "2026-02-27"
---

# SAST 配置

静态应用安全测试（SAST）工具的安装、配置与自定义规则创建，支持多种编程语言的全面安全扫描。

## 适用场景

- 在 CI/CD 流水线中配置 SAST 扫描
- 为代码库创建自定义安全规则
- 配置质量门禁和合规策略
- 优化扫描性能，减少误报
- 集成多种 SAST 工具实现纵深防御

## 不适用场景

- 仅需要 DAST 或手动渗透测试指导
- 无法访问源代码或 CI/CD 流水线
- 需要组织层面的策略决策而非工具配置

## 操作指引

1. 确认语言、仓库和合规需求。
2. 选择工具并定义基线策略。
3. 将扫描集成到 CI/CD 中，设置门禁阈值。
4. 根据误报情况调优规则和抑制策略。
5. 跟踪修复进度并验证修复效果。

## 安全须知

- 未经批准，避免使用第三方服务扫描敏感仓库。
- 防止扫描产物和日志中泄露密钥信息。

## 概述

本技能提供全面的 SAST 工具配置指导，涵盖 Semgrep、SonarQube 和 CodeQL。

## 核心能力

### 1. Semgrep 配置
- 基于模式匹配的自定义规则创建
- 针对特定语言的安全规则（Python、JavaScript、Go、Java 等）
- CI/CD 集成（GitHub Actions、GitLab CI、Jenkins）
- 误报调优与规则优化
- 组织级策略执行

### 2. SonarQube 配置
- 质量门禁配置
- 安全热点分析
- 代码覆盖率与技术债务跟踪
- 针对各语言的自定义质量配置文件
- 与 LDAP/SAML 的企业级集成

### 3. CodeQL 分析
- GitHub Advanced Security 集成
- 自定义查询开发
- 漏洞变体分析
- 安全研究工作流
- SARIF 结果处理

## 快速开始

### 初始评估
1. 确认代码库中的主要编程语言
2. 确定合规要求（PCI-DSS、SOC 2 等）
3. 根据语言支持和集成需求选择 SAST 工具
4. 审查基线扫描结果，了解当前安全状况

### 基础配置
```bash
# Semgrep quick start
pip install semgrep
semgrep --config=auto --error

# SonarQube with Docker
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest

# CodeQL CLI setup
gh extension install github/gh-codeql
codeql database create mydb --language=python
```

## 参考文档

- Semgrep 规则创建 - 基于模式的安全规则开发
- SonarQube 配置指南 - 质量门禁与配置文件
- CodeQL 配置指南 - 查询开发与工作流

## 模板与资源

- semgrep-config.yml - 生产级 Semgrep 配置
- sonarqube-settings.xml - SonarQube 质量配置模板
- run-sast.sh - 自动化 SAST 执行脚本

## 集成模式

### CI/CD 流水线集成
```yaml
# GitHub Actions example
- name: Run Semgrep
  uses: returntocorp/semgrep-action@v1
  with:
    config: >-
      p/security-audit
      p/owasp-top-ten
```

### Pre-commit 钩子
```bash
# .pre-commit-config.yaml
- repo: https://github.com/returntocorp/semgrep
  rev: v1.45.0
  hooks:
    - id: semgrep
      args: ['--config=auto', '--error']
```

## 最佳实践

1. **从基线开始**
   - 运行初始扫描建立安全基线
   - 优先处理严重和高危发现
   - 制定修复路线图

2. **渐进式采用**
   - 先从安全相关规则开始
   - 逐步添加代码质量规则
   - 仅对严重问题启用阻断

3. **误报管理**
   - 记录合理的抑制原因
   - 为已知安全模式创建白名单
   - 定期审查被抑制的发现

4. **性能优化**
   - 排除测试文件和生成的代码
   - 大型代码库使用增量扫描
   - 在 CI/CD 中缓存扫描结果

5. **团队赋能**
   - 为开发人员提供安全培训
   - 针对常见模式编写内部文档
   - 建立安全冠军计划

## 常见用例

### 新项目配置
```bash
./scripts/run-sast.sh --setup --language python --tools semgrep,sonarqube
```

### 自定义规则开发
```yaml
# See references/semgrep-rules.md for detailed examples
rules:
  - id: hardcoded-jwt-secret
    pattern: jwt.encode($DATA, "...", ...)
    message: JWT secret should not be hardcoded
    severity: ERROR
```

### 合规扫描
```bash
# PCI-DSS focused scan
semgrep --config p/pci-dss --json -o pci-scan-results.json
```

## 故障排查

### 误报率过高
- 审查并调优规则灵敏度
- 添加路径过滤器排除测试文件
- 使用 nostmt 元数据处理噪声模式
- 创建组织专属的规则例外

### 性能问题
- 启用增量扫描
- 跨模块并行扫描
- 优化规则模式提高效率
- 缓存依赖和扫描结果

### 集成失败
- 验证 API 令牌和凭证
- 检查网络连通性和代理设置
- 审查 SARIF 输出格式兼容性
- 验证 CI/CD 运行器权限

## 相关技能

- OWASP Top 10 检查清单
- 容器安全
- 依赖扫描

## 工具对比

| 工具 | 最佳用途 | 语言支持 | 费用 | 集成能力 |
|------|----------|----------|------|----------|
| Semgrep | 自定义规则，快速扫描 | 30+ 种语言 | 免费/企业版 | 优秀 |
| SonarQube | 代码质量 + 安全 | 25+ 种语言 | 免费/商业版 | 良好 |
| CodeQL | 深度分析，安全研究 | 10+ 种语言 | 免费（开源） | GitHub 原生 |

## 后续步骤

1. 完成 SAST 工具的初始配置
2. 运行基线安全扫描
3. 针对组织特定模式创建自定义规则
4. 集成到 CI/CD 流水线
5. 建立安全门禁策略
6. 培训开发团队了解发现和修复方法

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出结果替代特定环境的验证、测试或专家审查。
- 缺少必要输入、权限、安全边界或成功标准时，请停下来请求澄清。