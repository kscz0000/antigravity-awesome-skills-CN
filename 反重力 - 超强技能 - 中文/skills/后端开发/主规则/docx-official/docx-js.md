# DOCX 库教程

使用 JavaScript/TypeScript 生成 .docx 文件。

**重要：开始前请通读本文档。** 关键的格式规则和常见陷阱贯穿全文——跳过某些章节可能导致文件损坏或渲染问题。

## 安装
假设 docx 已经全局安装
如果未安装：`npm install -g docx`

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, Media,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        InternalHyperlink, TableOfContents, HeadingLevel, BorderStyle, WidthType, TabStopType,
        TabStopPosition, UnderlineType, ShadingType, VerticalAlign, SymbolRun, PageNumber,
        FootnoteReferenceRun, Footnote, PageBreak } = require('docx');

// 创建与保存
const doc = new Document({ sections: [{ children: [/* 内容 */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer)); // Node.js
Packer.toBlob(doc).then(blob => { /* 下载逻辑 */ }); // 浏览器
```

## 文本与格式
```javascript
// 重要：永远不要使用 \n 作为换行符 - 务必使用独立的 Paragraph 元素
// ❌ 错误：new TextRun("Line 1\nLine 2")
// ✅ 正确：new Paragraph({ children: [new TextRun("Line 1")] }), new Paragraph({ children: [new TextRun("Line 2")] })

// 包含所有格式选项的基础文本
new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 200, after: 200 },
  indent: { left: 720, right: 720 },
  children: [
    new TextRun({ text: "粗体", bold: true }),
    new TextRun({ text: "斜体", italics: true }),
    new TextRun({ text: "下划线", underline: { type: UnderlineType.DOUBLE, color: "FF0000" } }),
    new TextRun({ text: "彩色", color: "FF0000", size: 28, font: "Arial" }), // Arial 默认
    new TextRun({ text: "高亮", highlight: "yellow" }),
    new TextRun({ text: "删除线", strike: true }),
    new TextRun({ text: "x2", superScript: true }),
    new TextRun({ text: "H2O", subScript: true }),
    new TextRun({ text: "小型大写", smallCaps: true }),
    new SymbolRun({ char: "2022", font: "Symbol" }), // 项目符号 •
    new SymbolRun({ char: "00A9", font: "Arial" })   // 版权 © - 符号使用 Arial
  ]
})
```

## 样式与专业格式

```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 12pt 默认
    paragraphStyles: [
      // 文档标题样式 - 覆盖内置的 Title 样式
      { id: "Title", name: "Title", basedOn: "Normal",
        run: { size: 56, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, alignment: AlignmentType.CENTER } },
      // 重要：使用精确的 ID 覆盖内置标题样式
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, color: "000000", font: "Arial" }, // 16pt
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } }, // 目录需要
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, color: "000000", font: "Arial" }, // 14pt
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
      // 自定义样式使用自己的 ID
      { id: "myStyle", name: "My Style", basedOn: "Normal",
        run: { size: 28, bold: true, color: "000000" },
        paragraph: { spacing: { after: 120 }, alignment: AlignmentType.CENTER } }
    ],
    characterStyles: [{ id: "myCharStyle", name: "My Char Style",
      run: { color: "FF0000", bold: true, underline: { type: UnderlineType.SINGLE } } }]
  },
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children: [
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("文档标题")] }), // 使用被覆盖的 Title 样式
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("标题 1")] }), // 使用被覆盖的 Heading1 样式
      new Paragraph({ style: "myStyle", children: [new TextRun("自定义段落样式")] }),
      new Paragraph({ children: [
        new TextRun("普通文本配合 "),
        new TextRun({ text: "自定义字符样式", style: "myCharStyle" })
      ]})
    ]
  }]
});
```

**专业字体组合：**
- **Arial（标题）+ Arial（正文）** - 通用性最强，简洁专业
- **Times New Roman（标题）+ Arial（正文）** - 经典衬线标题配现代无衬线正文
- **Georgia（标题）+ Verdana（正文）** - 优化屏幕阅读，雅致对比

**关键样式原则：**
- **覆盖内置样式**：使用精确 ID（如 "Heading1"、"Heading2"、"Heading3"）覆盖 Word 的内置标题样式
- **HeadingLevel 常量**：`HeadingLevel.HEADING_1` 使用 "Heading1" 样式，`HeadingLevel.HEADING_2` 使用 "Heading2" 样式，依此类推
- **包含 outlineLevel**：为 H1 设置 `outlineLevel: 0`，H2 设置 `outlineLevel: 1`，以此类推，确保目录正常工作
- **使用自定义样式** 而非内联格式以保持一致性
- **设置默认字体** 使用 `styles.default.document.run.font` - Arial 通用支持最佳
- **建立视觉层次** 通过不同的字体大小（标题 > 章节标题 > 正文）
- **添加合适的间距** 使用段落的 `before` 和 `after` 间距
- **谨慎使用颜色**：标题和章节标题默认使用黑色（000000）和灰色系
- **设置一致的边距**（1440 = 1 英寸为标准）


## 列表（务必使用规范列表 - 永远不要使用 Unicode 项目符号）
```javascript
// 项目符号 - 务必使用编号配置，而不是 Unicode 符号
// 关键：使用 LevelFormat.BULLET 常量，而不是字符串 "bullet"
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullet-list",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "first-numbered-list",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "second-numbered-list", // 不同的 reference = 从 1 重新开始
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }
    ]
  },
  sections: [{
    children: [
      // 项目符号列表项
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("第一个项目符号")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("第二个项目符号")] }),
      // 编号列表项
      new Paragraph({ numbering: { reference: "first-numbered-list", level: 0 },
        children: [new TextRun("第一个编号项")] }),
      new Paragraph({ numbering: { reference: "first-numbered-list", level: 0 },
        children: [new TextRun("第二个编号项")] }),
      // ⚠️ 关键：不同的 reference = 独立的列表，从 1 重新开始
      // 相同的 reference = 继续之前的编号
      new Paragraph({ numbering: { reference: "second-numbered-list", level: 0 },
        children: [new TextRun("再次从 1 开始（因为 reference 不同）")] })
    ]
  }]
});

// ⚠️ 关键编号规则：每个 reference 创建一个独立的编号列表
// - 相同 reference = 继续编号（1, 2, 3... 然后 4, 5, 6...）
// - 不同 reference = 从 1 重新开始（1, 2, 3... 然后 1, 2, 3...）
// 为每个独立的编号部分使用唯一的 reference 名称！

// ⚠️ 关键：永远不要使用 Unicode 项目符号 - 它们会创建无法正常工作的假列表
// new TextRun("• Item")           // 错误
// new SymbolRun({ char: "2022" }) // 错误
// ✅ 务必使用带 LevelFormat.BULLET 的编号配置以获得真正的 Word 列表
```

## 表格
```javascript
// 完整的表格包含边距、边框、表头和项目符号
const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };

new Table({
  columnWidths: [4680, 4680], // ⚠️ 关键：在表格级别设置列宽 - 单位为 DXA（1/20 磅）
  margins: { top: 100, bottom: 100, left: 180, right: 180 }, // 为所有单元格统一设置
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // 同时在每个单元格上设置宽度
          // ⚠️ 关键：始终使用 ShadingType.CLEAR 防止 Word 中出现黑色背景。
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: "表头", bold: true, size: 22 })]
          })]
        }),
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // 同时在每个单元格上设置宽度
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: "项目符号", bold: true, size: 22 })]
          })]
        })
      ]
    }),
    new TableRow({
      children: [
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // 同时在每个单元格上设置宽度
          children: [new Paragraph({ children: [new TextRun("常规数据")] })]
        }),
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // 同时在每个单元格上设置宽度
          children: [
            new Paragraph({
              numbering: { reference: "bullet-list", level: 0 },
              children: [new TextRun("第一个项目符号")]
            }),
            new Paragraph({
              numbering: { reference: "bullet-list", level: 0 },
              children: [new TextRun("第二个项目符号")]
            })
          ]
        })
      ]
    })
  ]
})
```

**重要：表格宽度与边框**
- 同时使用 `columnWidths: [width1, width2, ...]` 数组和每个单元格上的 `width: { size: X, type: WidthType.DXA }`
- 单位为 DXA（1/20 磅）：1440 = 1 英寸，Letter 纸可用宽度 = 9360 DXA（1 英寸边距）
- 将边框应用到各个 `TableCell` 元素，而不是 `Table` 本身

**预设列宽（Letter 纸 1 英寸边距 = 9360 DXA 总宽）：**
- **2 列：** `columnWidths: [4680, 4680]`（等宽）
- **3 列：** `columnWidths: [3120, 3120, 3120]`（等宽）

## 链接与导航
```javascript
// 目录（需要标题） - 关键：仅使用 HeadingLevel，不要使用自定义样式
// ❌ 错误：new Paragraph({ heading: HeadingLevel.HEADING_1, style: "customHeader", children: [new TextRun("Title")] })
// ✅ 正确：new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Title")] })
new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }),

// 外部链接
new Paragraph({
  children: [new ExternalHyperlink({
    children: [new TextRun({ text: "Google", style: "Hyperlink" })],
    link: "https://www.google.com"
  })]
}),

// 内部链接与书签
new Paragraph({
  children: [new InternalHyperlink({
    children: [new TextRun({ text: "Go to Section", style: "Hyperlink" })],
    anchor: "section1"
  })]
}),
new Paragraph({
  children: [new TextRun("Section Content")],
  bookmark: { id: "section1", name: "section1" }
}),
```

## 图像与媒体
```javascript
// 带尺寸和定位的基础图像
// 关键：务必指定 'type' 参数 - ImageRun 必需
new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new ImageRun({
    type: "png", // 新要求：必须指定图像类型（png, jpg, jpeg, gif, bmp, svg）
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150, rotation: 0 }, // 旋转角度
    altText: { title: "Logo", description: "Company logo", name: "Name" } // 重要：三个字段都必需
  })]
})
```

## 分页符
```javascript
// 手动分页符
new Paragraph({ children: [new PageBreak()] }),

// 段落前的分页符
new Paragraph({
  pageBreakBefore: true,
  children: [new TextRun("This starts on a new page")]
})

// ⚠️ 关键：永远不要单独使用 PageBreak - 会产生 Word 无法打开的非法 XML
// ❌ 错误：new PageBreak()
// ✅ 正确：new Paragraph({ children: [new PageBreak()] })
```

## 页眉/页脚与页面设置
```javascript
const doc = new Document({
  sections: [{
    properties: {
      page: {
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }, // 1440 = 1 英寸
        size: { orientation: PageOrientation.LANDSCAPE },
        pageNumbers: { start: 1, formatType: "decimal" } // "upperRoman", "lowerRoman", "upperLetter", "lowerLetter"
      }
    },
    headers: {
      default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun("Header Text")]
      })] })
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun("Page "), new TextRun({ children: [PageNumber.CURRENT] }), new TextRun(" of "), new TextRun({ children: [PageNumber.TOTAL_PAGES] })]
      })] })
    },
    children: [/* 内容 */]
  }]
});
```

## 制表位
```javascript
new Paragraph({
  tabStops: [
    { type: TabStopType.LEFT, position: TabStopPosition.MAX / 4 },
    { type: TabStopType.CENTER, position: TabStopPosition.MAX / 2 },
    { type: TabStopType.RIGHT, position: TabStopPosition.MAX * 3 / 4 }
  ],
  children: [new TextRun("Left\tCenter\tRight")]
})
```

## 常量与速查
- **下划线：** `SINGLE`、`DOUBLE`、`WAVY`、`DASH`
- **边框：** `SINGLE`、`DOUBLE`、`DASHED`、`DOTTED`
- **编号：** `DECIMAL`（1,2,3）、`UPPER_ROMAN`（I,II,III）、`LOWER_LETTER`（a,b,c）
- **制表位：** `LEFT`、`CENTER`、`RIGHT`、`DECIMAL`
- **符号：** `"2022"`（•）、`"00A9"`（©）、`"00AE"`（®）、`"2122"`（™）、`"00B0"`（°）、`"F070"`（✓）、`"F0FC"`（✗）

## 关键问题与常见错误
- **关键：PageBreak 必须始终放在 Paragraph 内部** - 单独的 PageBreak 会产生 Word 无法打开的非法 XML
- **务必使用 ShadingType.CLEAR 进行表格单元格底纹** - 永远不要使用 ShadingType.SOLID（会导致黑色背景）。
- 测量单位为 DXA（1440 = 1 英寸）| 每个表格单元格至少需要 1 个 Paragraph | 目录仅支持 HeadingLevel 样式
- **务必使用自定义样式** 配合 Arial 字体以获得专业外观和合适的视觉层次
- **务必设置默认字体** 使用 `styles.default.document.run.font` - 推荐 Arial
- **务必为表格设置 columnWidths 数组** + 单个单元格宽度以确保兼容性
- **永远不要使用 Unicode 符号作为项目符号** - 务必使用 `LevelFormat.BULLET` 常量（而不是字符串 "bullet"）的编号配置
- **永远不要使用 \n 作为换行符** - 务必为每行使用独立的 Paragraph 元素
- **务必在 Paragraph children 中使用 TextRun 对象** - 永远不要直接在 Paragraph 上使用 text 属性
- **图像关键**：ImageRun 需要 `type` 参数 - 务必指定 "png"、"jpg"、"jpeg"、"gif"、"bmp" 或 "svg"
- **项目符号关键**：必须使用 `LevelFormat.BULLET` 常量而不是字符串 "bullet"，并包含 `text: "•"` 作为项目符号字符
- **编号关键**：每个编号 reference 创建一个独立的列表。相同 reference = 继续编号（1,2,3 然后 4,5,6）。不同 reference = 从 1 重新开始（1,2,3 然后 1,2,3）。为每个独立的编号部分使用唯一的 reference 名称！
- **目录关键**：使用 TableOfContents 时，标题必须仅使用 HeadingLevel - 不要在标题段落上添加自定义样式，否则目录会损坏
- **表格**：设置 `columnWidths` 数组 + 单个单元格宽度，将边框应用到单元格而非表格
- **在 TABLE 级别设置表格边距** 以保持一致的单元格内边距（避免每个单元格重复设置）
