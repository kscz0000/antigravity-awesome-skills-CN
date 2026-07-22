---
name: bilig-workpaper
description: "面向智能体的电子表格任务，使用由公式驱动的 WorkPaper JSON 与 MCP 工具，无需驱动 Excel 或浏览器界面。"
risk: critical
source: community
date_added: "2026-05-21"
tags:
  - spreadsheets
  - formulas
  - mcp
  - xlsx
  - typescript
plugin:
  targets:
    codex: blocked
    claude: blocked
---

# Bilig WorkPaper

## 概述

Bilig WorkPaper 为智能体提供一种"代码优先"的工作簿运行时，用于处理电子表格式的业务逻辑。当任务更容易用工作表与公式来建模，但更稳妥的路径是通过 API 编辑单元格、重新计算、回读计算结果、并以 JSON 工作簿文档的形式持久化时，使用本技能。

其主要用途是以确定性工具调用替代脆弱的电子表格 UI 自动化。它适用于报价计算器、分润模型、预算校验、导入校验，以及减少 XLSX 公式缺陷上报等场景。

## 何时使用本技能

在用户需要以下能力时使用本技能：

- 在 Node.js 服务、路由、测试或智能体工具中处理电子表格公式；
- 写入工作簿输入并通过回读证明校验计算输出；
- 将公式工作簿以可审阅的 WorkPaper JSON 形式持久化；
- 通过 MCP 工具对外暴露基于文件的工作簿；
- 在不自动化 Excel、LibreOffice 或浏览器表格的前提下，调查 XLSX 公式重算问题。

请勿用于以下场景：手动编辑电子表格、VBA/宏、数据透视表、图表、COM 自动化，或要求与桌面 Excel 严格一致的行为——除非用户明确要求以 Excel 为基准进行对照。

## 更安全的命令模式

在 MCP/客户端配置中，优先使用参数数组。请勿将用户提供的路径、工作表名、公式或单元格地址进行 shell 拼接。在将其用于命令之前，拒绝包含换行符、反引号、`$(`、`;`、`&`、`|`、`<`、`>` 的路径或单元格输入。

上述 MCP 示例会执行公共 npm 包 `@bilig/workpaper`。请将其视为第三方代码执行：固定你已审查过的包版本，仅在受信项目中运行，并在启动可写 MCP 服务器之前获得用户明确同意。

## 快速 MCP 配置

首先验证包自带的挑战命令可用：

```json
{
  "command": "npm",
  "args": ["exec", "--package", "@bilig/workpaper@<reviewed-version>", "--", "bilig-mcp-challenge"]
}
```

随后启动一个可写的、基于文件的 MCP 服务器：

```json
{
  "command": "npm",
  "args": [
    "exec",
    "--package",
    "@bilig/workpaper@<reviewed-version>",
    "--",
    "bilig-workpaper-mcp",
    "--workpaper",
    "./pricing.workpaper.json",
    "--init-demo-workpaper",
    "--writable"
  ]
}
```

MCP 服务器对外暴露的常用工具包括：

- `list_sheets`
- `read_range`
- `read_cell`
- `set_cell_contents`
- `get_cell_display_value`
- `export_workpaper_document`
- `validate_formula`

每次写入之后，都要读取相关输出单元格并导出 WorkPaper 文档。不得仅凭写入调用就声称操作成功。

## TypeScript 直连模式

当工作簿逻辑应当归属于应用代码内部时，直接使用该包：

```ts
import {
  WorkPaper,
  exportWorkPaperDocument,
  serializeWorkPaperDocument,
} from "@bilig/workpaper";

const workbook = WorkPaper.buildFromSheets({
  Inputs: [
    ["Metric", "Value"],
    ["Customers", 20],
    ["Average revenue", 1200],
  ],
  Summary: [
    ["Metric", "Value"],
    ["Revenue", "=Inputs!B2*Inputs!B3"],
  ],
});

const inputs = workbook.getSheetId("Inputs");
const summary = workbook.getSheetId("Summary");
if (inputs === undefined || summary === undefined) {
  throw new Error("Workbook is missing required sheets");
}

workbook.setCellContents({ sheet: inputs, row: 1, col: 1 }, 32);
const revenue = workbook.getCellDisplayValue({ sheet: summary, row: 1, col: 1 });
const saved = serializeWorkPaperDocument(
  exportWorkPaperDocument(workbook, { includeConfig: true }),
);

console.log({ revenue, savedBytes: saved.length });
```

## 必需的验证步骤

合格的智能体回复应当包含：

- 被编辑的工作表名与 A1 单元格地址（精确给出）；
- 重要输入与受其影响的输出在改动前的取值；
- 从重算后的工作簿回读得到的改动后取值；
- 通过导出或序列化 WorkPaper JSON 形成的持久化证据；
- 当涉及文件边界时，应给出还原或重新导入的证明；
- 对不支持的公式或 Excel 专有行为，应清楚列出其局限。

如果任一证据环节失败，请直接报告该阻塞点，而不是声称工作簿已更新。

## 局限性

- WorkPaper 行为并不能完全替代桌面 Excel、VBA、数据透视表、图表或 UI 自动化。
- 公式兼容性取决于 Bilig 运行时；当要求严格等价时，应以 Excel 为基准进行验证。
- MCP 写入应当严格限定在受信工作簿路径范围内，并且其后必须进行回读校验。

## 参考资料

- 代码仓库：https://github.com/proompteng/bilig
- 精简文档地图：https://proompteng.github.io/bilig/llms.txt
- 智能体手册：https://proompteng.github.io/bilig/headless-workpaper-agent-handbook.html
- MCP 服务器指南：https://proompteng.github.io/bilig/mcp-workpaper-tool-server.html
- XLSX 公式诊所：https://proompteng.github.io/bilig/formula-bug-clinic.html
- 兼容性限制：https://proompteng.github.io/bilig/where-bilig-is-not-excel-compatible-yet.html
