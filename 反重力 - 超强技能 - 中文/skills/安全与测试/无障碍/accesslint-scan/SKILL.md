---
name: accesslint-scan
description: "审计在线页面的可访问性问题，准确定位每项 WCAG 违规，并返回一份基于选择器的修复待办清单，且不进行任何修改。触发词：accesslint、accessibility、a11y、WCAG、accessibility audit、audit a11y。"
risk: safe
source: "https://github.com/AccessLint/skills"
date_added: "2026-06-02"
---

审计在线页面并报告问题位置与具体内容。只定位，不修复。如果 `$ARGUMENTS` 中没有 URL，请向用户索取。

## 适用场景
- 在任务与下列描述匹配时使用本技能：审计在线页面的可访问性问题，准确定位每项 WCAG 违规，并返回一份基于选择器的修复待办清单，且不进行任何修改。

## 1. 审计

```bash
PORT=$(npx -y @accesslint/chrome@latest ensure | node -e 'process.stdin.on("data",d=>process.stdout.write(""+JSON.parse(d).port))')
npx -y @accesslint/cli@latest "<url>" --port "$PORT" --format json
```

按需使用标志：`--selector`、`--wait-for "<selector>"`、`--include-aaa`、`--disable <rules>`。

## 2. 输出报告

先按严重程度统计数量，再逐条列出违规：

- **位置** — 选择器原文 + 若存在 `source` 则附 `file:line (symbol)` —— 严禁编造。若所有违规都没有 `source`，需注明 "source mapping unavailable — located by selector only"。
- **证据** — 对比度、缺失属性、空名称等具体取值
- **修复** — 机械修改即可，或标记 `NEEDS HUMAN`

不要修改代码。修复阶段：先处理机械修改，然后重新审计以验证；批量工作移交给 `accesslint:audit`。

## 3. 关闭

```bash
npx -y @accesslint/chrome@latest stop --all  # 若 ensure 报告 "managed":false 则跳过
```

## 注意事项

- `ensure` 始终决定端口 —— 切勿硬编码 9222。
- CLI 退出码 2 = URL 无效或页面未加载；请检查开发服务器。

## 局限说明
- 仅在任务与上述范围明确匹配时使用本技能。
- 请勿将本技能的输出替代针对具体环境的验证、测试或专家评审。
- 若缺少必要的输入、权限、安全边界或成功标准，应停下来向用户澄清。
