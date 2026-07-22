---
name: pptx-official
description: "用户可能要求你创建、编辑或分析 .pptx 文件的内容。.pptx 文件本质上是一个包含 XML 文件和其他资源的 ZIP 归档，你可以读取或编辑这些内容。针对不同任务有不同的工具和工作流可供使用。当用户要求创建、编辑或分析 PowerPoint 文件时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# PPTX 创建、编辑与分析

## 概述

用户可能要求你创建、编辑或分析 .pptx 文件的内容。.pptx 文件本质上是一个包含 XML 文件和其他资源的 ZIP 归档，你可以读取或编辑这些内容。针对不同任务有不同的工具和工作流可供使用。

## 读取与分析内容

### 文本提取
如果只需要读取演示文稿的文本内容，应将文档转换为 Markdown：

```bash
# Convert document to markdown
python -m markitdown path-to-file.pptx
```

### 原始 XML 访问
以下场景需要原始 XML 访问：批注、演讲者备注、幻灯片版式、动画、设计元素和复杂格式。对于这些功能，需要解包演示文稿并读取其原始 XML 内容。

#### 解包文件
`python ooxml/scripts/unpack.py <office_file> <output_dir>`

**注意**：unpack.py 脚本位于项目根目录的 `skills/pptx/ooxml/scripts/unpack.py`。如果该路径不存在，请使用 `find . -name "unpack.py"` 查找。

#### 关键文件结构
* `ppt/presentation.xml` - 主演示文稿元数据和幻灯片引用
* `ppt/slides/slide{N}.xml` - 各幻灯片内容（slide1.xml、slide2.xml 等）
* `ppt/notesSlides/notesSlide{N}.xml` - 各幻灯片的演讲者备注
* `ppt/comments/modernComment_*.xml` - 特定幻灯片的批注
* `ppt/slideLayouts/` - 幻灯片版式模板
* `ppt/slideMasters/` - 母版幻灯片模板
* `ppt/theme/` - 主题和样式信息
* `ppt/media/` - 图片和其他媒体文件

#### 排版与颜色提取
**当需要模仿示例设计时**：始终先使用以下方法分析演示文稿的排版和颜色：
1. **读取主题文件**：检查 `ppt/theme/theme1.xml` 中的颜色（`<a:clrScheme>`）和字体（`<a:fontScheme>`）
2. **采样幻灯片内容**：查看 `ppt/slides/slide1.xml` 中实际使用的字体（`<a:rPr>`）和颜色
3. **搜索模式**：使用 grep 在所有 XML 文件中查找颜色（`<a:solidFill>`、`<a:srgbClr>`）和字体引用

## 从零创建新的 PowerPoint 演示文稿（不使用模板）

从零创建新的 PowerPoint 演示文稿时，使用 **html2pptx** 工作流将 HTML 幻灯片转换为 PowerPoint，实现精确定位。

### 设计原则

**关键**：在创建任何演示文稿之前，先分析内容并选择合适的设计元素：
1. **考虑主题内容**：这个演示文稿关于什么？它暗示了什么调性、行业或氛围？
2. **检查品牌标识**：如果用户提到了公司/组织，考虑其品牌颜色和视觉标识
3. **匹配配色与内容**：选择能反映主题的颜色
4. **说明你的方案**：在编写代码之前解释你的设计选择

**要求**：
- ✅ 在编写代码之前说明基于内容的设计方案
- ✅ 仅使用 Web 安全字体：Arial、Helvetica、Times New Roman、Georgia、Courier New、Verdana、Tahoma、Trebuchet MS、Impact
- ✅ 通过大小、粗细和颜色建立清晰的视觉层次
- ✅ 确保可读性：强对比度、适当大小的文本、整齐的对齐
- ✅ 保持一致性：在幻灯片之间重复使用相同的模式、间距和视觉语言

#### 配色方案选择

**创造性地选择颜色**：
- **跳出默认思维**：什么颜色真正匹配这个特定主题？避免惯性选择。
- **多角度考虑**：主题、行业、氛围、能量级别、目标受众、品牌标识（如提到）
- **大胆尝试**：尝试意想不到的组合——医疗演示不一定要用绿色，金融不一定要用海军蓝
- **构建配色方案**：选择 3-5 种协调的颜色（主色 + 辅助色 + 强调色）
- **确保对比度**：文本在背景上必须清晰可读

**示例配色方案**（用于激发创意——选择一个、改编或自行创建）：

1. **经典蓝**：深海军蓝 (#1C2833)、石板灰 (#2E4053)、银色 (#AAB7B8)、米白 (#F4F6F6)
2. **青色与珊瑚色**：青色 (#5EA8A7)、深青 (#277884)、珊瑚色 (#FE4447)、白色 (#FFFFFF)
3. **大胆红**：红色 (#C0392B)、亮红 (#E74C3C)、橙色 (#F39C12)、黄色 (#F1C40F)、绿色 (#2ECC71)
4. **温暖粉**：淡紫 (#A49393)、腮红粉 (#EED6D3)、玫瑰 (#E8B4B8)、奶油白 (#FAF7F2)
5. **勃艮第奢华**：勃艮第红 (#5D1D2E)、深红 (#951233)、铁锈色 (#C15937)、金色 (#997929)
6. **深紫与祖母绿**：紫色 (#B165FB)、深蓝 (#181B24)、祖母绿 (#40695B)、白色 (#FFFFFF)
7. **奶油白与森林绿**：奶油白 (#FFE1C7)、森林绿 (#40695B)、白色 (#FCFCFC)
8. **粉色与紫色**：粉色 (#F8275B)、珊瑚色 (#FF574A)、玫瑰 (#FF737D)、紫色 (#3D2F68)
9. **青柠与梅色**：青柠 (#C5DE82)、梅色 (#7C3A5F)、珊瑚色 (#FD8C6E)、蓝灰 (#98ACB5)
10. **黑金**：金色 (#BF9A4A)、黑色 (#000000)、奶油白 (#F4F6F6)
11. **鼠尾草与赤陶**：鼠尾草绿 (#87A96B)、赤陶色 (#E07A5F)、奶油白 (#F4F1DE)、炭灰 (#2C2C2C)
12. **炭灰与红色**：炭灰 (#292929)、红色 (#E33737)、浅灰 (#CCCBCB)
13. **活力橙**：橙色 (#F96D00)、浅灰 (#F2F2F2)、炭灰 (#222831)
14. **森林绿**：黑色 (#191A19)、绿色 (#4E9F3D)、深绿 (#1E5128)、白色 (#FFFFFF)
15. **复古彩虹**：紫色 (#722880)、粉色 (#D72D51)、橙色 (#EB5C18)、琥珀色 (#F08800)、金色 (#DEB600)
16. **复古大地色**：芥末黄 (#E3B448)、鼠尾草绿 (#CBD18F)、森林绿 (#3A6B35)、奶油白 (#F4F1DE)
17. **海岸玫瑰**：旧玫瑰色 (#AD7670)、海狸棕 (#B49886)、蛋壳白 (#F3ECDC)、灰绿 (#BFD5BE)
18. **橙色与绿松石**：浅橙 (#FC993E)、灰绿松石 (#667C6F)、白色 (#FCFCFC)

#### 视觉细节选项

**几何图案**：
- 对角线分段分隔符替代水平线
- 不对称列宽（30/70、40/60、25/75）
- 90° 或 270° 旋转的文本标题
- 图片使用圆形/六边形框架
- 角落使用三角形装饰形状
- 重叠形状营造深度感

**边框与框架处理**：
- 单侧粗单色边框（10-20pt）
- 双线边框配对比色
- 角括号替代完整框架
- L 形边框（上+左 或 下+右）
- 标题下方下划线装饰（3-5pt 粗）

**排版处理**：
- 极端大小对比（72pt 标题 vs 11pt 正文）
- 全大写标题配宽字间距
- 超大展示字体的编号章节
- 等宽字体（Courier New）用于数据/统计/技术内容
- 紧缩字体（Arial Narrow）用于密集信息
- 描边文本用于强调

**图表与数据样式**：
- 单色图表配单强调色标注关键数据
- 水平条形图替代垂直条形图
- 散点图替代条形图
- 最少网格线或无网格线
- 数据标签直接标注在元素上（无图例）
- 关键指标使用超大数字

**布局创新**：
- 全出血图片配文本叠加
- 侧边栏列（20-30% 宽度）用于导航/上下文
- 模块化网格系统（3×3、4×4 区块）
- Z 形或 F 形内容流
- 彩色形状上的浮动文本框
- 杂志风格多栏布局

**背景处理**：
- 占幻灯片 40-60% 的纯色块
- 渐变填充（仅限垂直或对角线方向）
- 分割背景（双色、对角线或垂直）
- 从边缘到边缘的色带
- 留白作为设计元素

### 布局技巧
**创建包含图表或表格的幻灯片时：**
- **双栏布局（首选）**：使用全宽标题，下方分两栏——一栏放文本/要点，另一栏放特色内容。这样平衡感更好，图表/表格更易读。使用不等宽 flexbox 列（如 40%/60% 分割）以优化各内容类型的空间。
- **全幻灯片布局**：让特色内容（图表/表格）占据整张幻灯片，获得最大冲击力和可读性
- **切勿垂直堆叠**：不要将图表/表格放在文本下方的单栏中——这会导致可读性差和布局问题

### 工作流
1. **强制要求 - 通读全文**：从头到尾完整阅读 [`html2pptx.md`](html2pptx.md)。**读取此文件时绝不要设置任何范围限制。** 在开始创建演示文稿之前，完整阅读详细语法、关键格式规则和最佳实践。
2. 为每张幻灯片创建一个 HTML 文件，使用正确的尺寸（如 16:9 使用 720pt × 405pt）
   - 使用 `<p>`、`<h1>`-`<h6>`、`<ul>`、`<ol>` 放置所有文本内容
   - 使用 `class="placeholder"` 标记将要添加图表/表格的区域（渲染为灰色背景以便查看）
   - **关键**：先使用 Sharp 将渐变和图标栅格化为 PNG 图片，再在 HTML 中引用
   - **布局**：对于包含图表/表格/图片的幻灯片，使用全幻灯片布局或双栏布局以提高可读性
3. 使用 [`html2pptx.js`](scripts/html2pptx.js) 库创建并运行 JavaScript 文件，将 HTML 幻灯片转换为 PowerPoint 并保存演示文稿
   - 使用 `html2pptx()` 函数处理每个 HTML 文件
   - 使用 PptxGenJS API 向占位区域添加图表和表格
   - 使用 `pptx.writeFile()` 保存演示文稿
4. **视觉验证**：生成缩略图并检查布局问题
   - 创建缩略图网格：`python scripts/thumbnail.py output.pptx workspace/thumbnails --cols 4`
   - 读取并仔细检查缩略图：
     - **文本截断**：文本被标题栏、形状或幻灯片边缘截断
     - **文本重叠**：文本与其他文本或形状重叠
     - **定位问题**：内容离幻灯片边界或其他元素太近
     - **对比度问题**：文本与背景之间对比度不足
   - 如发现问题，调整 HTML 的 margin/spacing/colors 并重新生成演示文稿
   - 重复直到所有幻灯片在视觉上正确

## 编辑现有的 PowerPoint 演示文稿

编辑现有 PowerPoint 演示文稿中的幻灯片时，需要使用原始 Office Open XML (OOXML) 格式。这涉及解包 .pptx 文件、编辑 XML 内容并重新打包。

### 工作流
1. **强制要求 - 通读全文**：从头到尾完整阅读 [`ooxml.md`](ooxml.md)（约 500 行）。**读取此文件时绝不要设置任何范围限制。** 在编辑任何演示文稿之前，完整阅读 OOXML 结构和编辑工作流的详细指南。
2. 解包演示文稿：`python ooxml/scripts/unpack.py <office_file> <output_dir>`
3. 编辑 XML 文件（主要是 `ppt/slides/slide{N}.xml` 及相关文件）
4. **关键**：每次编辑后立即验证，在继续之前修复所有验证错误：`python ooxml/scripts/validate.py <dir> --original <file>`
5. 打包最终演示文稿：`python ooxml/scripts/pack.py <input_directory> <office_file>`

## 使用模板创建新的 PowerPoint 演示文稿

需要创建遵循现有模板设计的演示文稿时，需要先复制和重新排列模板幻灯片，然后替换占位内容。

### 工作流
1. **提取模板文本并创建可视化缩略图网格**：
   * 提取文本：`python -m markitdown template.pptx > template-content.md`
   * 阅读 `template-content.md`：完整阅读文件以了解模板演示文稿的内容。**读取此文件时绝不要设置任何范围限制。**
   * 创建缩略图网格：`python scripts/thumbnail.py template.pptx`
   * 详见[创建缩略图网格](#创建缩略图网格)章节

2. **分析模板并保存清单到文件**：
   * **视觉分析**：查看缩略图网格以了解幻灯片布局、设计模式和视觉结构
   * 创建并保存模板清单文件 `template-inventory.md`，包含：
     ```markdown
     # Template Inventory Analysis
     **Total Slides: [count]**
     **IMPORTANT: Slides are 0-indexed (first slide = 0, last slide = count-1)**

     ## [Category Name]
     - Slide 0: [Layout code if available] - Description/purpose
     - Slide 1: [Layout code] - Description/purpose
     - Slide 2: [Layout code] - Description/purpose
     [... EVERY slide must be listed individually with its index ...]
     ```
   * **使用缩略图网格**：参考可视化缩略图以识别：
     - 布局模式（标题幻灯片、内容布局、分节符）
     - 图片占位符位置和数量
     - 幻灯片组间的设计一致性
     - 视觉层次和结构
   * 此清单文件是下一步选择合适模板的必要条件

3. **基于模板清单创建演示文稿大纲**：
   * 查看第 2 步中的可用模板。
   * 为第一张幻灯片选择标题或封面模板。这应该是靠前的模板之一。
   * 为其他幻灯片选择安全的、以文本为主的布局。
   * **关键：匹配布局结构与实际内容**：
     - 单栏布局：用于统一叙述或单一主题
     - 双栏布局：仅当有恰好 2 个不同项目/概念时使用
     - 三栏布局：仅当有恰好 3 个不同项目/概念时使用
     - 图片+文本布局：仅当有实际图片需要插入时使用
     - 引用布局：仅用于真实的人物引言（附出处），不用于强调
     - 切勿使用占位符数量超过实际内容的布局
     - 如果有 2 个项目，不要强行放入三栏布局
     - 如果有 4 个以上项目，考虑拆分为多张幻灯片或使用列表格式
   * 在选择布局之前先统计实际内容条数
   * 验证所选布局中的每个占位符都会被有意义的内容填充
   * 为每个内容部分选择一个代表**最佳**布局的选项。
   * 保存 `outline.md`，包含内容和可利用可用设计的模板映射
   * 示例模板映射：
     ```
     # Template slides to use (0-based indexing)
     # WARNING: Verify indices are within range! Template with 73 slides has indices 0-72
     # Mapping: slide numbers from outline -> template slide indices
     template_mapping = [
         0,   # Use slide 0 (Title/Cover)
         34,  # Use slide 34 (B1: Title and body)
         34,  # Use slide 34 again (duplicate for second B1)
         50,  # Use slide 50 (E1: Quote)
         54,  # Use slide 54 (F2: Closing + Text)
     ]
     ```

4. **使用 `rearrange.py` 复制、重排和删除幻灯片**：
   * 使用 `scripts/rearrange.py` 脚本创建按所需顺序排列的新演示文稿：
     ```bash
     python scripts/rearrange.py template.pptx working.pptx 0,34,34,50,52
     ```
   * 脚本自动处理重复幻灯片的复制、未使用幻灯片的删除和重新排序
   * 幻灯片索引从 0 开始（第一张为 0，第二张为 1，依此类推）
   * 同一幻灯片索引可出现多次以复制该幻灯片

5. **使用 `inventory.py` 脚本提取所有文本**：
   * **运行清单提取**：
     ```bash
     python scripts/inventory.py working.pptx text-inventory.json
     ```
   * **阅读 text-inventory.json**：完整阅读 text-inventory.json 文件以了解所有形状及其属性。**读取此文件时绝不要设置任何范围限制。**

   * 清单 JSON 结构：
     ```json
       {
         "slide-0": {
           "shape-0": {
             "placeholder_type": "TITLE",  // or null for non-placeholders
             "left": 1.5,                  // position in inches
             "top": 2.0,
             "width": 7.5,
             "height": 1.2,
             "paragraphs": [
               {
                 "text": "Paragraph text",
                 // Optional properties (only included when non-default):
                 "bullet": true,           // explicit bullet detected
                 "level": 0,               // only included when bullet is true
                 "alignment": "CENTER",    // CENTER, RIGHT (not LEFT)
                 "space_before": 10.0,     // space before paragraph in points
                 "space_after": 6.0,       // space after paragraph in points
                 "line_spacing": 22.4,     // line spacing in points
                 "font_name": "Arial",     // from first run
                 "font_size": 14.0,        // in points
                 "bold": true,
                 "italic": false,
                 "underline": false,
                 "color": "FF0000"         // RGB color
               }
             ]
           }
         }
       }
     ```

   * 关键特性：
     - **幻灯片**：命名为 "slide-0"、"slide-1" 等
     - **形状**：按视觉位置排序（从上到下、从左到右）为 "shape-0"、"shape-1" 等
     - **占位符类型**：TITLE、CENTER_TITLE、SUBTITLE、BODY、OBJECT 或 null
     - **默认字体大小**：从版式占位符提取的 `default_font_size`（以 pt 为单位，如可用）
     - **幻灯片编号已过滤**：SLIDE_NUMBER 占位符类型的形状会自动排除在清单之外
     - **项目符号**：当 `bullet: true` 时，`level` 始终包含（即使为 0）
     - **间距**：`space_before`、`space_after` 和 `line_spacing` 以 pt 为单位（仅在设置时包含）
     - **颜色**：`color` 为 RGB（如 "FF0000"），`theme_color` 为主题颜色（如 "DARK_1"）
     - **属性**：仅输出非默认值

6. **生成替换文本并保存数据到 JSON 文件**
   基于上一步的文本清单：
   - **关键**：先验证清单中存在哪些形状——仅引用实际存在的形状
   - **验证**：replace.py 脚本会验证替换 JSON 中的所有形状是否存在于清单中
     - 如果引用了不存在的形状，会显示错误及可用形状
     - 如果引用了不存在的幻灯片，会显示错误表明该幻灯片不存在
     - 所有验证错误在脚本退出前一次性显示
   - **重要**：replace.py 脚本内部使用 inventory.py 识别所有文本形状
   - **自动清除**：清单中的所有文本形状都会被清除，除非你为其提供 "paragraphs"
   - 需要内容的形状添加 "paragraphs" 字段（不是 "replacement_paragraphs"）
   - 替换 JSON 中没有 "paragraphs" 的形状将自动清除文本
   - 包含项目符号的段落会自动左对齐。当 `"bullet": true` 时不要设置 `alignment` 属性
   - 为占位文本生成合适的替换内容
   - 使用形状大小确定合适的内容长度
   - **关键**：从原始清单中包含段落属性——不要只提供文本
   - **重要**：当 bullet: true 时，不要在文本中包含项目符号（•、-、*）——它们会自动添加
   - **基本格式规则**：
     - 标题通常应有 `"bold": true`
     - 列表项应有 `"bullet": true, "level": 0`（当 bullet 为 true 时 level 必填）
     - 保留所有对齐属性（如居中文本的 `"alignment": "CENTER"`）
     - 与默认值不同时包含字体属性（如 `"font_size": 14.0`、`"font_name": "Lora"`）
     - 颜色：使用 `"color": "FF0000"` 表示 RGB 或 `"theme_color": "DARK_1"` 表示主题颜色
     - 替换脚本需要**格式正确的段落**，而非纯文本字符串
     - **重叠形状**：优先选择 default_font_size 更大或 placeholder_type 更合适的形状
   * 将包含替换内容的更新清单保存为 `replacement-text.json`
   - **警告**：不同模板布局的形状数量不同——在创建替换内容之前始终检查实际清单

   示例段落字段，展示正确的格式：
   ```json
   "paragraphs": [
     {
       "text": "New presentation title text",
       "alignment": "CENTER",
       "bold": true
     },
     {
       "text": "Section Header",
       "bold": true
     },
     {
       "text": "First bullet point without bullet symbol",
       "bullet": true,
       "level": 0
     },
     {
       "text": "Red colored text",
       "color": "FF0000"
     },
     {
       "text": "Theme colored text",
       "theme_color": "DARK_1"
     },
     {
       "text": "Regular paragraph text without special formatting"
     }
   ]
   ```

   **未在替换 JSON 中列出的形状会自动清除**：
   ```json
   {
     "slide-0": {
       "shape-0": {
         "paragraphs": [...] // This shape gets new text
       }
       // shape-1 and shape-2 from inventory will be cleared automatically
     }
   }
   ```

   **演示文稿常见格式模式**：
   - 标题幻灯片：加粗文本，有时居中
   - 幻灯片内的章节标题：加粗文本
   - 项目列表：每项需要 `"bullet": true, "level": 0`
   - 正文：通常不需要特殊属性
   - 引用：可能有特殊对齐或字体属性

7. **使用 `replace.py` 脚本应用替换**
   ```bash
   python scripts/replace.py working.pptx replacement-text.json output.pptx
   ```

   该脚本将：
   - 首先使用 inventory.py 的功能提取所有文本形状的清单
   - 验证替换 JSON 中的所有形状是否存在于清单中
   - 清除清单中识别的所有形状的文本
   - 仅对替换 JSON 中定义了 "paragraphs" 的形状应用新文本
   - 通过应用 JSON 中的段落属性来保留格式
   - 自动处理项目符号、对齐、字体属性和颜色
   - 保存更新后的演示文稿

   示例验证错误：
   ```
   ERROR: Invalid shapes in replacement JSON:
     - Shape 'shape-99' not found on 'slide-0'. Available shapes: shape-0, shape-1, shape-4
     - Slide 'slide-999' not found in inventory
   ```

   ```
   ERROR: Replacement text made overflow worse in these shapes:
     - slide-0/shape-2: overflow worsened by 1.25" (was 0.00", now 1.25")
   ```

## 创建缩略图网格

为 PowerPoint 幻灯片创建可视化缩略图网格，便于快速分析和参考：

```bash
python scripts/thumbnail.py template.pptx [output_prefix]
```

**功能**：
- 生成：`thumbnails.jpg`（大型幻灯片组会生成 `thumbnails-1.jpg`、`thumbnails-2.jpg` 等）
- 默认：5 列，每网格最多 30 张幻灯片（5×6）
- 自定义前缀：`python scripts/thumbnail.py template.pptx my-grid`
  - 注意：如需输出到特定目录，输出前缀应包含路径（如 `workspace/my-grid`）
- 调整列数：`--cols 4`（范围：3-6，影响每网格幻灯片数）
- 网格限制：3 列 = 12 张/网格，4 列 = 20 张，5 列 = 30 张，6 列 = 42 张
- 幻灯片从 0 开始索引（Slide 0、Slide 1 等）

**使用场景**：
- 模板分析：快速了解幻灯片布局和设计模式
- 内容审查：整个演示文稿的可视化概览
- 导航参考：通过视觉外观查找特定幻灯片
- 质量检查：验证所有幻灯片格式正确

**示例**：
```bash
# Basic usage
python scripts/thumbnail.py presentation.pptx

# Combine options: custom name, columns
python scripts/thumbnail.py template.pptx analysis --cols 4
```

## 将幻灯片转换为图片

要视觉分析 PowerPoint 幻灯片，使用两步流程将其转换为图片：

1. **将 PPTX 转换为 PDF**：
   ```bash
   soffice --headless --convert-to pdf template.pptx
   ```

2. **将 PDF 页面转换为 JPEG 图片**：
   ```bash
   pdftoppm -jpeg -r 150 template.pdf slide
   ```
   这会生成 `slide-1.jpg`、`slide-2.jpg` 等文件。

选项：
- `-r 150`：设置分辨率为 150 DPI（根据质量/大小平衡调整）
- `-jpeg`：输出 JPEG 格式（如需 PNG 可用 `-png`）
- `-f N`：转换的起始页（如 `-f 2` 从第 2 页开始）
- `-l N`：转换的结束页（如 `-l 5` 到第 5 页停止）
- `slide`：输出文件前缀

指定范围的示例：
```bash
pdftoppm -jpeg -r 150 -f 2 -l 5 template.pdf slide  # Converts only pages 2-5
```

## 代码风格指南
**重要**：生成 PPTX 操作代码时：
- 编写简洁的代码
- 避免冗长的变量名和冗余操作
- 避免不必要的 print 语句

## 依赖项

必需依赖（应该已安装）：

- **markitdown**：`pip install "markitdown[pptx]"`（用于从演示文稿提取文本）
- **pptxgenjs**：`npm install -g pptxgenjs`（用于通过 html2pptx 创建演示文稿）
- **playwright**：`npm install -g playwright`（用于 html2pptx 中的 HTML 渲染）
- **react-icons**：`npm install -g react-icons react react-dom`（用于图标）
- **sharp**：`npm install -g sharp`（用于 SVG 栅格化和图片处理）
- **LibreOffice**：`sudo apt-get install libreoffice`（用于 PDF 转换）
- **Poppler**：`sudo apt-get install poppler-utils`（用于 pdftoppm 将 PDF 转换为图片）
- **defusedxml**：`pip install defusedxml`（用于安全 XML 解析）

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
