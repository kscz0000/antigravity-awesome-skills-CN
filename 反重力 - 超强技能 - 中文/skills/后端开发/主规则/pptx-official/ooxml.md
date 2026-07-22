# Office Open XML 技术参考（PowerPoint）

**重要：在开始之前请通读本文档。** 文档中涵盖了关键的 XML 模式规则和格式要求。错误的实现可能导致创建无法被 PowerPoint 打开的无效 PPTX 文件。

## 技术规范

### 模式合规性
- **`<p:txBody>` 中的元素顺序**：`<a:bodyPr>`、`<a:lstStyle>`、`<a:p>`
- **空白字符**：对包含前导/尾随空格的 `<a:t>` 元素添加 `xml:space='preserve'`
- **Unicode**：在 ASCII 内容中转义字符：`"` 变为 `&#8220;`
- **图片**：添加到 `ppt/media/`，在幻灯片 XML 中引用，设置尺寸以适应幻灯片边界
- **关系**：为每个幻灯片的资源更新 `ppt/slides/_rels/slideN.xml.rels`
- **dirty 属性**：向 `<a:rPr>` 和 `<a:endParaRPr>` 元素添加 `dirty="0"` 以指示干净状态

## 演示文稿结构

### 基本幻灯片结构
```xml
<!-- ppt/slides/slide1.xml -->
<p:sld>
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr>...</p:nvGrpSpPr>
      <p:grpSpPr>...</p:grpSpPr>
      <!-- Shapes go here -->
    </p:spTree>
  </p:cSld>
</p:sld>
```

### 文本框 / 带文本的形状
```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="2" name="Title"/>
    <p:cNvSpPr>
      <a:spLocks noGrp="1"/>
    </p:cNvSpPr>
    <p:nvPr>
      <p:ph type="ctrTitle"/>
    </p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="838200" y="365125"/>
      <a:ext cx="7772400" cy="1470025"/>
    </a:xfrm>
  </p:spPr>
  <p:txBody>
    <a:bodyPr/>
    <a:lstStyle/>
    <a:p>
      <a:r>
        <a:t>Slide Title</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

### 文本格式化
```xml
<!-- Bold -->
<a:r>
  <a:rPr b="1"/>
  <a:t>Bold Text</a:t>
</a:r>

<!-- Italic -->
<a:r>
  <a:rPr i="1"/>
  <a:t>Italic Text</a:t>
</a:r>

<!-- Underline -->
<a:r>
  <a:rPr u="sng"/>
  <a:t>Underlined</a:t>
</a:r>

<!-- Highlight -->
<a:r>
  <a:rPr>
    <a:highlight>
      <a:srgbClr val="FFFF00"/>
    </a:highlight>
  </a:rPr>
  <a:t>Highlighted Text</a:t>
</a:r>

<!-- Font and Size -->
<a:r>
  <a:rPr sz="2400" typeface="Arial">
    <a:solidFill>
      <a:srgbClr val="FF0000"/>
    </a:solidFill>
  </a:rPr>
  <a:t>Colored Arial 24pt</a:t>
</a:r>

<!-- Complete formatting example -->
<a:r>
  <a:rPr lang="en-US" sz="1400" b="1" dirty="0">
    <a:solidFill>
      <a:srgbClr val="FAFAFA"/>
    </a:solidFill>
  </a:rPr>
  <a:t>Formatted text</a:t>
</a:r>
```

### 列表
```xml
<!-- Bullet list -->
<a:p>
  <a:pPr lvl="0">
    <a:buChar char="•"/>
  </a:pPr>
  <a:r>
    <a:t>First bullet point</a:t>
  </a:r>
</a:p>

<!-- Numbered list -->
<a:p>
  <a:pPr lvl="0">
    <a:buAutoNum type="arabicPeriod"/>
  </a:pPr>
  <a:r>
    <a:t>First numbered item</a:t>
  </a:r>
</a:p>

<!-- Second level indent -->
<a:p>
  <a:pPr lvl="1">
    <a:buChar char="•"/>
  </a:pPr>
  <a:r>
    <a:t>Indented bullet</a:t>
  </a:r>
</a:p>
```

### 形状
```xml
<!-- Rectangle -->
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="3" name="Rectangle"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="1000000" y="1000000"/>
      <a:ext cx="3000000" cy="2000000"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="FF0000"/>
    </a:solidFill>
    <a:ln w="25400">
      <a:solidFill>
        <a:srgbClr val="000000"/>
      </a:solidFill>
    </a:ln>
  </p:spPr>
</p:sp>

<!-- Rounded Rectangle -->
<p:sp>
  <p:spPr>
    <a:prstGeom prst="roundRect">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>
</p:sp>

<!-- Circle/Ellipse -->
<p:sp>
  <p:spPr>
    <a:prstGeom prst="ellipse">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>
</p:sp>
```

### 图片
```xml
<p:pic>
  <p:nvPicPr>
    <p:cNvPr id="4" name="Picture">
      <a:hlinkClick r:id="" action="ppaction://media"/>
    </p:cNvPr>
    <p:cNvPicPr>
      <a:picLocks noChangeAspect="1"/>
    </p:cNvPicPr>
    <p:nvPr/>
  </p:nvPicPr>
  <p:blipFill>
    <a:blip r:embed="rId2"/>
    <a:stretch>
      <a:fillRect/>
    </a:stretch>
  </p:blipFill>
  <p:spPr>
    <a:xfrm>
      <a:off x="1000000" y="1000000"/>
      <a:ext cx="3000000" cy="2000000"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>
</p:pic>
```

### 表格
```xml
<p:graphicFrame>
  <p:nvGraphicFramePr>
    <p:cNvPr id="5" name="Table"/>
    <p:cNvGraphicFramePr>
      <a:graphicFrameLocks noGrp="1"/>
    </p:cNvGraphicFramePr>
    <p:nvPr/>
  </p:nvGraphicFramePr>
  <p:xfrm>
    <a:off x="1000000" y="1000000"/>
    <a:ext cx="6000000" cy="2000000"/>
  </p:xfrm>
  <a:graphic>
    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">
      <a:tbl>
        <a:tblGrid>
          <a:gridCol w="3000000"/>
          <a:gridCol w="3000000"/>
        </a:tblGrid>
        <a:tr h="500000">
          <a:tc>
            <a:txBody>
              <a:bodyPr/>
              <a:lstStyle/>
              <a:p>
                <a:r>
                  <a:t>Cell 1</a:t>
                </a:r>
              </a:p>
            </a:txBody>
          </a:tc>
          <a:tc>
            <a:txBody>
              <a:bodyPr/>
              <a:lstStyle/>
              <a:p>
                <a:r>
                  <a:t>Cell 2</a:t>
                </a:r>
              </a:p>
            </a:txBody>
          </a:tc>
        </a:tr>
      </a:tbl>
    </a:graphicData>
  </a:graphic>
</p:graphicFrame>
```

### 幻灯片版式

```xml
<!-- Title Slide Layout -->
<p:sp>
  <p:nvSpPr>
    <p:nvPr>
      <p:ph type="ctrTitle"/>
    </p:nvPr>
  </p:nvSpPr>
  <!-- Title content -->
</p:sp>

<p:sp>
  <p:nvSpPr>
    <p:nvPr>
      <p:ph type="subTitle" idx="1"/>
    </p:nvPr>
  </p:nvSpPr>
  <!-- Subtitle content -->
</p:sp>

<!-- Content Slide Layout -->
<p:sp>
  <p:nvSpPr>
    <p:nvPr>
      <p:ph type="title"/>
    </p:nvPr>
  </p:nvSpPr>
  <!-- Slide title -->
</p:sp>

<p:sp>
  <p:nvSpPr>
    <p:nvPr>
      <p:ph type="body" idx="1"/>
    </p:nvPr>
  </p:nvSpPr>
  <!-- Content body -->
</p:sp>
```

## 文件更新

添加内容时，需要更新以下文件：

**`ppt/_rels/presentation.xml.rels`：**
```xml
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
```

**`ppt/slides/_rels/slide1.xml.rels`：**
```xml
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.png"/>
```

**`[Content_Types].xml`：**
```xml
<Default Extension="png" ContentType="image/png"/>
<Default Extension="jpg" ContentType="image/jpeg"/>
<Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
```

**`ppt/presentation.xml`：**
```xml
<p:sldIdLst>
  <p:sldId id="256" r:id="rId1"/>
  <p:sldId id="257" r:id="rId2"/>
</p:sldIdLst>
```

**`docProps/app.xml`：** 更新幻灯片计数和统计信息
```xml
<Slides>2</Slides>
<Paragraphs>10</Paragraphs>
<Words>50</Words>
```

## 幻灯片操作

### 添加新幻灯片
在演示文稿末尾添加幻灯片时：

1. **创建幻灯片文件**（`ppt/slides/slideN.xml`）
2. **更新 `[Content_Types].xml`**：为新幻灯片添加 Override
3. **更新 `ppt/_rels/presentation.xml.rels`**：为新幻灯片添加关系
4. **更新 `ppt/presentation.xml`**：在 `<p:sldIdLst>` 中添加幻灯片 ID
5. **创建幻灯片关系**（`ppt/slides/_rels/slideN.xml.rels`）（如需要）
6. **更新 `docProps/app.xml`**：递增幻灯片计数并更新统计信息（如存在）

### 复制幻灯片
1. 复制源幻灯片 XML 文件并使用新名称
2. 更新新幻灯片中的所有 ID 以确保唯一性
3. 按照上述"添加新幻灯片"的步骤操作
4. **关键**：删除或更新 `_rels` 文件中的演讲者备注幻灯片引用
5. 删除未使用媒体文件的引用

### 重新排序幻灯片
1. **更新 `ppt/presentation.xml`**：重新排列 `<p:sldIdLst>` 中的 `<p:sldId>` 元素
2. `<p:sldId>` 元素的顺序决定幻灯片顺序
3. 保持幻灯片 ID 和关系 ID 不变

示例：
```xml
<!-- Original order -->
<p:sldIdLst>
  <p:sldId id="256" r:id="rId2"/>
  <p:sldId id="257" r:id="rId3"/>
  <p:sldId id="258" r:id="rId4"/>
</p:sldIdLst>

<!-- After moving slide 3 to position 2 -->
<p:sldIdLst>
  <p:sldId id="256" r:id="rId2"/>
  <p:sldId id="258" r:id="rId4"/>
  <p:sldId id="257" r:id="rId3"/>
</p:sldIdLst>
```

### 删除幻灯片
1. **从 `ppt/presentation.xml` 中移除**：删除 `<p:sldId>` 条目
2. **从 `ppt/_rels/presentation.xml.rels` 中移除**：删除关系
3. **从 `[Content_Types].xml` 中移除**：删除 Override 条目
4. **删除文件**：移除 `ppt/slides/slideN.xml` 和 `ppt/slides/_rels/slideN.xml.rels`
5. **更新 `docProps/app.xml`**：递减幻灯片计数并更新统计信息
6. **清理未使用的媒体**：从 `ppt/media/` 中删除孤立的图片

注意：不要重新编号剩余的幻灯片——保持其原始 ID 和文件名。


## 常见错误

- **编码**：在 ASCII 内容中转义 Unicode 字符：`"` 变为 `&#8220;`
- **图片**：添加到 `ppt/media/` 并更新关系文件
- **列表**：从列表标题中省略项目符号
- **ID**：对 UUID 使用有效的十六进制值
- **主题**：检查 `theme` 目录中的所有主题颜色

## 基于模板的演示文稿验证清单

### 打包前必须检查：
- **清理未使用的资源**：删除未引用的媒体、字体和备注目录
- **修复 Content_Types.xml**：声明包中存在的所有幻灯片、版式和主题
- **修复关系 ID**：
   - 如果不使用嵌入字体，删除字体嵌入引用
- **删除损坏的引用**：检查所有 `_rels` 文件中对已删除资源的引用

### 常见模板复制陷阱：
- 复制后多个幻灯片引用同一个演讲者备注幻灯片
- 来自模板幻灯片的图片/媒体引用已不存在
- 字体未包含时的字体嵌入引用
- 版式 12-25 缺少 slideLayout 声明
- docProps 目录可能不会解包——这是可选的
