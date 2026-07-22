---
name: photopea-embedded-editor
description: 使用 photopea.js 在 Web 应用中嵌入 Photopea。涵盖嵌入、文件 I/O、脚本编写、导出、图层、文本、滤镜及完整的 Photoshop 兼容 API。触发词：Photopea嵌入、图片编辑器嵌入、photopea.js、嵌入式Photopea、图像编辑自动化、PS脚本、图层操作、文本编辑、滤镜应用
risk: safe
source: community
source_repo: yikuansun/PhotopeaAPI
source_type: community
license: MIT
license_source: "https://github.com/yikuansun/PhotopeaAPI/blob/master/LICENSE"
date_added: 2026-05-20
---

# Photopea 嵌入式编辑器技能
## 在网站和应用中使用 photopea.js (yikuansun/PhotopeaAPI)

---

## 何时使用此技能

在涉及以下**任何任务**时使用此技能：
- 将 Photopea 作为图片编辑器嵌入到网页或 Web 应用中
- 从 JavaScript 代码控制嵌入的 Photopea 实例
- 从宿主页面自动化图片编辑工作流（打开文件、运行脚本、导出结果）
- 使用 Photopea 作为引擎在产品中构建图片编辑功能
- 编写脚本来操作文档、图层、文本、选区、滤镜、颜色和路径

**禁止**使用原始 `postMessage` 接线方式 — 始终使用 `photopea.js` 作为封装层。

---

## 库：photopea.js

`photopea.js` 是基于 Promise 的 JavaScript 封装库，封装了 Photopea Live Messaging API。
仓库：https://github.com/yikuansun/PhotopeaAPI
npm 包：https://www.npmjs.com/package/photopea

### 安装

**CDN（无需构建步骤）**
```html
<script src="https://cdn.jsdelivr.net/npm/photopea@1.1.1/dist/photopea.min.js"></script>
```

**自托管**
```html
<script src="./photopea.min.js"></script>
```

**npm（Webpack / Vite / Rollup）**
```bash
npm install photopea
```
```js
import Photopea from "photopea";
```

---

## 核心 API：`Photopea` 类

| 方法 | 说明 |
|------|------|
| `Photopea.createEmbed(container)` | 创建并注入 iframe，就绪后 resolve |
| `new Photopea(window.parent)` | 插件模式：封装父窗口 |
| `pea.runScript(script)` | 在 Photopea 内运行 JS 字符串；返回输出数组 |
| `pea.loadAsset(arrayBuffer)` | 加载二进制文件（图片、字体、画笔等） |
| `pea.openFromURL(url, asSmart)` | 以新文档或智能对象图层方式打开远程 URL |
| `pea.exportImage(type)` | 导出当前文档；返回 `Blob`（`"png"` 或 `"jpg"`） |

所有方法均返回 Promise — 始终使用 `await` 或 `.then()`。

---

## 步骤 1 — 嵌入

容器 `<div>` 在调用 `createEmbed` 之前**必须**具有固定的宽度和高度。

```html
<div id="editor" style="width:1000px; height:650px;"></div>
<script src="https://cdn.jsdelivr.net/npm/photopea@1.1.1/dist/photopea.min.js"></script>
<script>
  Photopea.createEmbed(document.getElementById("editor")).then(async (pea) => {
    // pea is ready
  });
</script>
```

**React：**
```jsx
import { useEffect, useRef } from "react";
import Photopea from "photopea";

export default function Editor() {
  const containerRef = useRef(null);
  const peaRef       = useRef(null);

  useEffect(() => {
    if (!containerRef.current || peaRef.current) return;
    Photopea.createEmbed(containerRef.current).then((pea) => {
      peaRef.current = pea;
    });
  }, []);

  return <div ref={containerRef} style={{ width: "100%", height: "650px" }} />;
}
```

---

## 步骤 2 — 打开文件

```js
// Remote URL → new document
await pea.openFromURL("https://example.com/design.psd", false);

// Remote URL → smart object layer inside current document
await pea.openFromURL("https://example.com/overlay.png", true);

// Local file (user input → ArrayBuffer → loadAsset)
document.getElementById("fileInput").addEventListener("change", async (e) => {
  const buf = await e.target.files[0].arrayBuffer();
  await pea.loadAsset(buf);
});

// Base64 data URI via runScript
await pea.runScript(`app.open("data:image/png;base64,iVBORw0...");`);
```

---

## 步骤 3 — 运行脚本

`runScript` 发送 JS 字符串，返回 `app.echoToOE(...)` 的值数组，最后一个是 `"done"`。

```js
const result = await pea.runScript(`app.echoToOE("hello");`);
// result → ["hello", "done"]

// Return structured data
const out = await pea.runScript(`
  app.echoToOE(JSON.stringify({
    width:  app.activeDocument.width,
    height: app.activeDocument.height,
    layers: app.activeDocument.layers.length
  }));
`);
const info = JSON.parse(out[0]);
```

---

## 步骤 4 — 导出

```js
// PNG Blob (via exportImage)
const blob = await pea.exportImage("png");
document.getElementById("preview").src = URL.createObjectURL(blob);

// JPEG Blob
const blob = await pea.exportImage("jpg");

// WebP / PSD / quality-controlled JPEG via saveToOE
const result = await pea.runScript(`app.activeDocument.saveToOE("webp:0.85");`);
const webpBlob = new Blob([result[0]], { type: "image/webp" });

const result = await pea.runScript(`app.activeDocument.saveToOE("psd:true");`);
const psdBlob  = new Blob([result[0]], { type: "application/octet-stream" });

// Trigger download
async function download(pea, filename = "export.png") {
  const blob = await pea.exportImage("png");
  const a    = Object.assign(document.createElement("a"), {
    href:     URL.createObjectURL(blob),
    download: filename
  });
  a.click();
}
```

**`saveToOE` 的导出格式字符串：**

| 字符串 | 格式 |
|--------|------|
| `"png"` | PNG 无损 |
| `"jpg"` | JPEG 默认质量 |
| `"jpg:0.8"` | JPEG 质量 0.0–1.0 |
| `"webp:0.7"` | WebP 质量 0.0–1.0 |
| `"psd"` | 完整 PSD |
| `"psd:true"` | 精简 PSD |
| `"svg:true"` | SVG |

---

## 步骤 5 — 加载资源

```js
// Font
const buf = await (await fetch("https://example.com/MyFont.otf")).arrayBuffer();
await pea.loadAsset(buf);
// Now usable in textItem.font

// Brush
await pea.loadAsset(await (await fetch("Nature.ABR")).arrayBuffer());

// Gradient
await pea.loadAsset(await (await fetch("Gradients.GRD")).arrayBuffer());
```

---

## 步骤 6 — 插件模式

```js
// Your page is inside Photopea's sidebar iframe
const pea = new Photopea(window.parent);

const out = await pea.runScript(`app.echoToOE(app.activeDocument.width);`);
console.log("Width:", out[0]);

// Load an asset from your plugin
const buf = await (await fetch("https://my-assets.com/sticker.png")).arrayBuffer();
await pea.loadAsset(buf);
```

插件配置：
```json
{
  "environment": {
    "plugins": [{
      "name": "My Plugin",
      "url":  "https://my-plugin.example.com",
      "icon": "===https://my-plugin.example.com/icon.png"
    }]
  }
}
```

---

## 实用工具模式

### addImageAndWait — 可靠的异步图层插入
```js
async function addImageAndWait(pea, imgURI) {
  let count = "done";
  while (count === "done")
    count = (await pea.runScript(`app.echoToOE(app.activeDocument.layers.length)`))[0];
  count = parseInt(count);

  const imageUrlLiteral = JSON.stringify(imgURI);
  await pea.runScript(`app.open(${imageUrlLiteral}, null, true);`);

  return new Promise((resolve) => {
    const check = async () => {
      const n = parseInt((await pea.runScript(
        `app.echoToOE(app.activeDocument.layers.length)`
      ))[0]);
      n === count + 1 ? resolve() : setTimeout(check, 50);
    };
    check();
  });
}
```

### getDocumentAsImage — 返回 `<img>` 元素
```js
async function getDocumentAsImage(pea) {
  const result = await pea.runScript(`app.activeDocument.saveToOE('png')`);
  return new Promise((resolve) => {
    const fr = new FileReader();
    fr.addEventListener("load", (e) => {
      const img = new Image(); img.src = e.target.result; resolve(img);
    });
    fr.readAsDataURL(new Blob([result[0]], { type: "image/png" }));
  });
}
```

---

## 实际应用模式

### 模式 A — 打开 + 导出 UI
```html
<input type="file" id="fileInput" accept="image/*,.psd">
<button id="exportBtn">Export PNG</button>
<div id="editor" style="width:100%;height:600px;"></div>
<script src="https://cdn.jsdelivr.net/npm/photopea@1.1.1/dist/photopea.min.js"></script>
<script>
let pea;
Photopea.createEmbed(document.getElementById("editor")).then(p => pea = p);

document.getElementById("fileInput").addEventListener("change", async e => {
  await pea.loadAsset(await e.target.files[0].arrayBuffer());
});
document.getElementById("exportBtn").addEventListener("click", async () => {
  const blob = await pea.exportImage("png");
  const a = Object.assign(document.createElement("a"), {
    href: URL.createObjectURL(blob), download: "export.png"
  });
  a.click();
});
</script>
```

### 模式 B — 模板 + 文本编辑 + 导出
```js
async function generateCard(pea, name, tagline) {
  await pea.openFromURL("https://example.com/card.psd", false);
  const nameLiteral = JSON.stringify(name);
  const taglineLiteral = JSON.stringify(tagline);
  await pea.runScript(`
    app.activeDocument.layers.getByName("Name").textItem.contents    = ${nameLiteral};
    app.activeDocument.layers.getByName("Tagline").textItem.contents = ${taglineLiteral};
  `);
  return await pea.exportImage("png");
}
```

### 模式 C — 批量水印
```js
async function batchWatermark(pea, imageURLs, watermarkURL) {
  const results = [];
  for (const url of imageURLs) {
    await pea.openFromURL(url, false);
    await pea.openFromURL(watermarkURL, true);
    await pea.runScript(`
      var doc = app.activeDocument, wm = doc.activeLayer;
      wm.translate(doc.width - wm.bounds[2] - 20, doc.height - wm.bounds[3] - 20);
      wm.opacity = 70;
    `);
    results.push(await pea.exportImage("png"));
    await pea.runScript(`app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);`);
  }
  return results;
}
```

---

# 完整脚本 API 参考

> 本节所有代码均运行在 `pea.runScript("...")` 字符串**内部**。
> Photopea 实现了 Adobe Photoshop CC 2015 JavaScript 脚本接口。
> 针对该版本的任何 Photoshop 脚本均可在 Photopea 中运行。

---

## `app` — 应用对象

### 属性

| 属性 | 类型 | 读/写 | 说明 |
|------|------|-------|------|
| `app.activeDocument` | Document | 读/写 | 当前活动文档 |
| `app.documents` | Documents | 只读 | 所有打开文档的集合 |
| `app.documents.length` | number | 只读 | 打开文档的数量 |
| `app.documents[i]` | Document | 只读 | 按零基索引访问 |
| `app.foregroundColor` | SolidColor | 读/写 | 当前前景色 |
| `app.backgroundColor` | SolidColor | 读/写 | 当前背景色 |
| `app.preferences.rulerUnits` | Units | 读/写 | `Units.PIXELS`、`Units.CM`、`Units.INCHES`、`Units.MM`、`Units.PICAS`、`Units.POINTS`、`Units.PERCENT` |
| `app.preferences.typeUnits` | TypeUnits | 读/写 | `TypeUnits.PIXELS`、`TypeUnits.MM`、`TypeUnits.POINTS` |
| `app.displayDialogs` | DialogModes | 读/写 | `DialogModes.NO`、`DialogModes.ALL`、`DialogModes.ERROR` |

### 方法

| 方法 | 说明 |
|------|------|
| `app.open(url)` | 以新文档方式打开 URL |
| `app.open(url, null, true)` | 以智能对象图层方式在活动文档中打开 URL |
| `app.echoToOE(string)` | **Photopea 扩展** — 向宿主页面发送字符串（由 `runScript` 捕获） |
| `app.showWindow("magiccut")` | **Photopea 扩展** — 打开 Magic Cut 面板 |
| `app.showWindow("vbitmap")` | **Photopea 扩展** — 打开 Vectorize Bitmap 面板 |
| `app.UI.zoomIn()` | 放大 |
| `app.UI.zoomOut()` | 缩小 |
| `app.UI.fitTheArea()` | 画布适应视口 |
| `app.UI.pixelToPixel()` | 100% 缩放 |
| `app.UI.switchFullscreen()` | 切换全屏 |
| `app.UI.scroll(dx, dy)` | 按增量滚动 |
| `app.UI.scrollTo(x, y)` | 滚动到绝对位置 |

**重要提示：** 在任何使用像素测量的脚本开头，务必将标尺单位设置为像素：
```js
var savedUnits = app.preferences.rulerUnits;
app.preferences.rulerUnits = Units.PIXELS;
// ... your code ...
app.preferences.rulerUnits = savedUnits;
```

---

## `Document` — 文档对象

通过 `app.activeDocument` 或 `app.documents[i]` 访问。

### 属性

| 属性 | 类型 | 读/写 | 说明 |
|------|------|-------|------|
| `width` | number | 只读 | 当前标尺单位下的文档宽度 |
| `height` | number | 只读 | 当前标尺单位下的文档高度 |
| `resolution` | number | 只读 | DPI（每英寸像素数） |
| `name` | string | **读/写** | **Photopea 扩展** — 显示标签（不产生历史步骤） |
| `source` | string | **读/写** | **Photopea 扩展** — 文件来源 URL 或 `"local,X,NAME"` |
| `mode` | DocumentMode | 只读 | `DocumentMode.RGB`、`GRAYSCALE`、`CMYK`、`LAB`、`BITMAP`、`INDEXEDCOLOR`、`MULTICHANNEL` |
| `bitsPerChannel` | BitsPerChannelType | 只读 | `BitsPerChannelType.EIGHT`、`SIXTEEN`、`THIRTYTWO` |
| `colorProfileName` | string | 只读 | 嵌入的颜色配置文件名称 |
| `activeLayer` | Layer/ArtLayer/LayerSet | 读/写 | 设置以激活图层 |
| `currentLayer` | ArtLayer | 读/写 | `activeLayer` 的别名 |
| `layers` | Layers | 只读 | 所有顶层图层（普通图层 + 图层组） |
| `artLayers` | ArtLayers | 只读 | 仅所有顶层普通图层 |
| `layerSets` | LayerSets | 只读 | 仅所有顶层图层组 |
| `selection` | Selection | 只读 | 当前选区 |
| `channels` | Channels | 只读 | 所有通道 |
| `historyStates` | HistoryStates | 只读 | 撤销历史 |
| `activeHistoryState` | HistoryState | 读/写 | 当前历史位置 |
| `layerComps` | LayerComps | 只读 | 图层复合集合 |
| `guides` | Guides | 只读 | 参考线集合 |
| `pathItems` | PathItems | 只读 | 矢量路径 |
| `id` | number | 只读 | 唯一文档 ID |
| `saved` | boolean | 只读 | 文档是否有未保存的更改 |
| `quickMaskMode` | boolean | 只读 | 是否处于快速蒙版模式 |
| `backgroundLayer` | ArtLayer | 只读 | 背景图层 |
| `pixelAspectRatio` | number | 只读 | 自定义像素宽高比（0.1–10.0） |
| `histogram` | array | 只读 | 256 元素直方图数组 |

### 方法

| 方法 | 签名 | 说明 |
|------|------|------|
| `resizeImage` | `(w, h, res, resampleMethod)` | 调整图像像素大小。ResampleMethod：`BICUBIC`、`BILINEAR`、`NEARESTNEIGHBOR`、`NONE`、`BICUBICSHARPER`、`BICUBICSMOOTHER` |
| `resizeCanvas` | `(w, h, anchor)` | 不缩放调整画布大小。AnchorPosition：`TOPLEFT`、`TOPCENTER`、`TOPRIGHT`、`MIDDLELEFT`、`MIDDLECENTER`、`MIDDLERIGHT`、`BOTTOMLEFT`、`BOTTOMCENTER`、`BOTTOMRIGHT` |
| `rotateCanvas` | `(degrees)` | 旋转整个画布。正值 = 顺时针 |
| `flipCanvas` | `(direction)` | `Direction.HORIZONTAL` 或 `Direction.VERTICAL` |
| `crop` | `([x1,y1,x2,y2], angle, w, h)` | 裁切画布。角度和尺寸为可选参数 |
| `trim` | `(trimType, top, left, bottom, right)` | 修剪透明/背景色边框。TrimType：`TRANSPARENT`、`TOPLEFT`、`BOTTOMRIGHT` |
| `revealAll` | `()` | 展开画布以显示被裁剪的内容 |
| `flatten` | `()` | 将所有图层合并为一个 |
| `mergeVisibleLayers` | `()` | 合并所有可见图层 |
| `rasterizeAllLayers` | `()` | 栅格化所有矢量/文本图层 |
| `changeMode` | `(mode, options)` | 转换颜色模式（如 `ChangeMode.GRAYSCALE`） |
| `convertProfile` | `(profileName, renderingIntent, blackPointCompensation, dither)` | 转换颜色配置文件 |
| `duplicate` | `(name, mergedLayers)` | 复制文档 |
| `close` | `(saveOptions)` | 关闭文档。SaveOptions：`DONOTSAVECHANGES`、`SAVECHANGES`、`PROMPTTOSAVECHANGES` |
| `save` | `()` | 保存（嵌入模式下需要服务器配置） |
| `saveToOE` | `(format)` | **Photopea 扩展** — 向宿主发送二进制数据。格式：`"png"`、`"jpg:0.8"`、`"webp:0.7"`、`"psd:true"`、`"svg:true"` |
| `clearHistory` | `()` | **Photopea 扩展** — 清除撤销历史以释放内存 |
| `exportDocument` | `(file, exportType, options)` | 导出到文件系统（触发 ZIP）。ExportType：`SAVEFORWEB` |
| `paste` | `(intoSelection)` | 将剪贴板粘贴到文档 |
| `suspendHistory` | `(historyName, callback)` | 将多个操作合并为一个历史步骤 |

**实际示例：**
```js
var doc = app.activeDocument;

// Resize image to 1920×1080 at 72dpi bicubic
doc.resizeImage(1920, 1080, 72, ResampleMethod.BICUBIC);

// Expand canvas to 2000px wide, keeping content centered
doc.resizeCanvas(2000, doc.height, AnchorPosition.MIDDLECENTER);

// Crop to a region
doc.crop([100, 100, 900, 600]);

// Trim transparent edges
doc.trim(TrimType.TRANSPARENT, true, true, true, true);

// Flip horizontal
doc.flipCanvas(Direction.HORIZONTAL);

// Change to grayscale
doc.changeMode(ChangeMode.GRAYSCALE);

// One undo step for many operations
doc.suspendHistory("Batch Edit", "action");
// (Inside Photopea, all ops become one history state)

// Export PNG to filesystem (triggers ZIP download)
var opts = new ExportOptionsSaveForWeb();
opts.format  = SaveDocumentType.PNG;
opts.PNG8    = false;
opts.quality = 100;
doc.exportDocument(new File("/output.png"), ExportType.SAVEFORWEB, opts);

// Close without saving
doc.close(SaveOptions.DONOTSAVECHANGES);
```

---

## `Layers` / `ArtLayers` / `LayerSets` 集合

这些集合存在于 `Document`、`LayerSet`（组内组）上，可迭代。

```js
var doc = app.activeDocument;

// Access
doc.layers          // all top-level (art + groups)
doc.artLayers       // top-level art layers only
doc.layerSets       // top-level group layers only

// By index (0 = topmost)
doc.layers[0]
doc.layers[doc.layers.length - 1]  // bottommost

// By name (throws if not found)
doc.layers.getByName("Background")
doc.artLayers.getByName("Logo")
doc.layerSets.getByName("Header Group")

// Add
var newLayer  = doc.artLayers.add();         // new blank art layer
var newGroup  = doc.layerSets.add();         // new group
var innerLayer = newGroup.artLayers.add();   // layer inside a group

// Remove
doc.artLayers.getByName("Temp").remove();

// Iterate all layers recursively
function walkLayers(parent) {
  for (var i = 0; i < parent.layers.length; i++) {
    var l = parent.layers[i];
    if (l.typename === "LayerSet") walkLayers(l);
    else /* ArtLayer */ processLayer(l);
  }
}
walkLayers(doc);
```

---

## `ArtLayer` — 单个图层

### 属性

| 属性 | 类型 | 读/写 | 说明 |
|------|------|-------|------|
| `name` | string | 读/写 | 图层名称 |
| `visible` | boolean | 读/写 | 图层可见性 |
| `opacity` | number | 读/写 | 图层不透明度 0–100 |
| `fillOpacity` | number | 只读 | 填充不透明度 0–100 |
| `blendMode` | BlendMode | 读/写 | 混合模式（见下方枚举） |
| `kind` | LayerKind | 读/写 | 图层类型（空图层上可设为 `LayerKind.TEXT`） |
| `textItem` | TextItem | 只读 | 文本对象（仅在 `kind === LayerKind.TEXT` 时可用） |
| `bounds` | array | 只读 | 当前标尺单位下的 `[left, top, right, bottom]` |
| `parent` | Document/LayerSet | 只读 | 包含对象 |
| `typename` | string | 只读 | 始终为 `"ArtLayer"` |
| `selected` | boolean | 只读 | **Photopea 扩展** — 图层在面板中是否高亮 |
| `isBackgroundLayer` | boolean | 只读 | 是否为锁定的背景图层 |
| `grouped` | boolean | 只读 | 是否应用了剪贴蒙版 |
| `pixelsLocked` | boolean | 只读 | 像素是否锁定 |
| `positionLocked` | boolean | 只读 | 位置是否锁定 |
| `transparentPixelsLocked` | boolean | 只读 | 透明像素是否锁定 |
| `layerMaskDensity` | number | 只读 | 图层蒙版密度 0–100 |
| `layerMaskFeather` | number | 只读 | 图层蒙版羽化 0–250 |
| `vectorMaskDensity` | number | 只读 | 矢量蒙版密度 0–100 |
| `vectorMaskFeather` | number | 只读 | 矢量蒙版羽化 0–250 |

### 变换方法

| 方法 | 签名 | 说明 |
|------|------|------|
| `translate` | `(deltaX, deltaY)` | 按偏移量移动图层 |
| `rotate` | `(angle, anchor)` | 按角度旋转。AnchorPosition 可选（默认居中） |
| `resize` | `(widthPct, heightPct, anchor)` | 按当前尺寸百分比缩放 |
| `rasterize` | `(target)` | 栅格化。RasterizeType：`ENTIRE`、`FILLCONTENT`、`LAYERCLIPPINGMASK`、`LINKEDLAYERS`、`SHAPE`、`TEXTCONTENTS`、`VECTORMASK` |

### 图层管理方法

| 方法 | 签名 | 说明 |
|------|------|------|
| `duplicate` | `()` | 复制到同一文档，返回新图层 |
| `duplicate` | `(doc, placement)` | 复制到另一个文档 |
| `remove` | `()` | 删除图层 |
| `merge` | `()` | 向下合并；返回合并后的 ArtLayer |
| `move` | `(relativeLayer, placement)` | 重新排序。ElementPlacement：`PLACEBEFORE`、`PLACEAFTER`、`PLACEATBEGINNING`、`PLACEATEND`、`INSIDE` |
| `copy` | `(merged)` | 复制到剪贴板 |
| `cut` | `()` | 剪切到剪贴板 |
| `clear` | `()` | 剪切但不存入剪贴板 |

### ArtLayer 上的调整方法

| 方法 | 签名 | 说明 |
|------|------|------|
| `adjustBrightnessContrast` | `(brightness, contrast)` | 亮度 -100–100，对比度 -100–100 |
| `adjustColorBalance` | `(shadows, midtones, highlights, preserveLuminosity)` | 每个为 `[青-红, 品红-绿, 黄-蓝]` 数组 |
| `adjustCurves` | `(curveShape)` | 每通道 `[input,output]` 对数组 |
| `adjustLevels` | `(inputRangeStart, inputRangeEnd, gamma, outputRangeStart, outputRangeEnd)` | 色阶调整 |
| `autoLevels` | `()` | 自动色阶 |
| `autoContrast` | `()` | 自动对比度 |
| `desaturate` | `()` | 在当前模式下转换为灰度值 |
| `equalize` | `()` | 均衡亮度分布 |
| `invert` | `()` | 反转像素颜色 |
| `posterize` | `(levels)` | 色调分离（2–255 级） |
| `threshold` | `(level)` | 黑白阈值（1–255） |
| `shadowHighlight` | `(shadowAmount, shadowWidth, shadowRadius, highlightAmount, highlightWidth, highlightRadius, colorCorrection, midtoneContrast, blackClip, whiteClip)` | 阴影/高光 |
| `photoFilter` | `(fillColor, density, luminosity)` | 照片滤镜 |
| `mixChannels` | `(outputChannels, monochrome)` | 通道混合器 |
| `selectiveColor` | `(colors, cyan, magenta, yellow, black, method)` | 可选颜色 |

### ArtLayer 上的滤镜方法

| 方法 | 签名 | 说明 |
|------|------|------|
| `applyGaussianBlur` | `(radius)` | 高斯模糊（0.1–250 px 半径） |
| `applyMotionBlur` | `(angle, distance)` | 动感模糊 |
| `applyRadialBlur` | `(amount, blurMethod, blurQuality)` | 径向模糊 |
| `applySmartBlur` | `(radius, threshold, blurQuality, blurMode)` | 智能模糊 |
| `applyBlur` | `()` | 简单模糊 |
| `applyBlurMore` | `()` | 进一步模糊 |
| `applyUnSharpMask` | `(amount, radius, threshold)` | USM 锐化 |
| `applySharpen` | `()` | 锐化 |
| `applySharpenEdges` | `()` | 锐化边缘 |
| `applySharpenMore` | `()` | 进一步锐化 |
| `applyAddNoise` | `(amount, distribution, monochromatic)` | 添加噪点。NoiseDistribution：`GAUSSIAN`、`UNIFORM` |
| `applyDespeckle` | `()` | 去斑 |
| `applyDustAndScratches` | `(radius, threshold)` | 蒙尘与划痕 |
| `applyMedianNoise` | `(radius)` | 中值降噪 |
| `applyMaximum` | `(radius)` | 最大值滤镜（膨胀） |
| `applyMinimum` | `(radius)` | 最小值滤镜（腐蚀） |
| `applyHighPass` | `(radius)` | 高反差保留 |
| `applyOffset` | `(horizontal, vertical, undefinedAreas)` | 位移。UndefinedAreas：`SETTOBACKGROUND`、`WRAPAROUND`、`REPEATEDGEPIXELS` |
| `applyRipple` | `(amount, size)` | 波纹。RippleSize：`SMALL`、`MEDIUM`、`LARGE` |
| `applyWave` | `(generators, minWavelength, maxWavelength, minAmplitude, maxAmplitude, horizScale, vertScale, waveType, undefinedAreas, randomSeed)` | 波浪滤镜 |
| `applyZigZag` | `(amount, ridges, style)` | 锯齿 |
| `applyTwirl` | `(angle)` | 旋转扭曲 |
| `applyPolarCoordinates` | `(conversion)` | 极坐标 |
| `applySpherize` | `(amount, mode)` | 球面化 |
| `applyPinch` | `(amount)` | 挤压（-100–100） |
| `applyShear` | `(curve, undefinedAreas)` | 切变 |
| `applyDisplace` | `(horizontalScale, verticalScale, displacementType, undefinedAreas, displacementMapFile)` | 置换 |
| `applyClouds` | `()` | 渲染云彩 |
| `applyDifferenceClouds` | `()` | 差值云彩 |
| `applyLensFlare` | `(brightness, flareCenter, lensType)` | 镜头光晕。LensType：`ZOOMWIDE, ZOOMNORMAL, MOVIE` |
| `applyDiffuseGlow` | `(graininess, glowAmount, clearAmount)` | 扩散发光 |
| `applyGlassEffect` | `(distortion, smoothness, scaling, invert, texture, textureFile)` | 玻璃 |
| `applyOceanRipple` | `(size, magnitude)` | 海洋波纹 |
| `applyLensBlur` | `(source, focalDistance, invertDepthMap, shape, radius, bladeCurvature, rotation, brightness, threshold, amount, distribution, monochromatic)` | 镜头模糊 |
| `applyAverage` | `()` | 平均模糊 |
| `applyDeInterlace` | `(eliminateFields, createFields)` | 逐行 |
| `applyNTSC` | `()` | NTSC 颜色 |
| `applyCustomFilter` | `(characteristics, scale, offset)` | 自定义滤镜（5×5 矩阵） |
| `applyTextureFill` | `(textureFile)` | 纹理填充 |
| `applyStyle` | `(styleName)` | 按名称应用图层样式预设 |
| `photoFilter` | `(fillColor, density, luminosity)` | 照片滤镜 |

**实际示例：**
```js
var layer = app.activeDocument.activeLayer;

// Move to absolute position (layer.bounds[0] = current left edge)
layer.translate(200 - layer.bounds[0], 100 - layer.bounds[1]);

// Rotate 45° around center
layer.rotate(45);

// Scale to 50% keeping center
layer.resize(50, 50, AnchorPosition.MIDDLECENTER);

// Gaussian blur radius 10
layer.applyGaussianBlur(10);

// Unsharp mask
layer.applyUnSharpMask(50, 2, 0);

// Levels: input 0–200, gamma 1.2, output 0–255
layer.adjustLevels(0, 200, 1.2, 0, 255);

// Brightness +20, Contrast +10
layer.adjustBrightnessContrast(20, 10);

// Invert
layer.invert();

// Rasterize text
layer.rasterize(RasterizeType.TEXTCONTENTS);

// Duplicate layer
var copy = layer.duplicate();
copy.name = "Layer Copy";

// Move layer below another
var target = doc.layers.getByName("Background");
layer.move(target, ElementPlacement.PLACEAFTER);
```

---

## `LayerSet` — 图层组

LayerSet 是图层面板中的文件夹/组。它与 `Document` 具有相同的图层管理方法。

### 属性

| 属性 | 类型 | 读/写 | 说明 |
|------|------|-------|------|
| `name` | string | 读/写 | 组名称 |
| `visible` | boolean | 读/写 | 组可见性 |
| `opacity` | number | 读/写 | 组不透明度 0–100 |
| `blendMode` | BlendMode | 读/写 | 组混合模式 |
| `bounds` | array | 只读 | 边界框 `[left,top,right,bottom]` |
| `layers` | Layers | 只读 | 此组内的所有图层 |
| `artLayers` | ArtLayers | 只读 | 此组内的普通图层 |
| `layerSets` | LayerSets | 只读 | 此组内的子组 |
| `parent` | Document/LayerSet | 只读 | 父容器 |
| `typename` | string | 只读 | 始终为 `"LayerSet"` |

### 方法
与 Document 相同的图层管理方法：`layers.add()`、`artLayers.add()`、`layerSets.add()`、`.getByName()`，以及 `duplicate()`、`remove()`、`move()`。

```js
// Create group with layers inside
var group = doc.layerSets.add();
group.name = "Product Card";

var bgLayer   = group.artLayers.add(); bgLayer.name = "Background";
var textLayer = group.artLayers.add(); textLayer.kind = LayerKind.TEXT;
textLayer.textItem.contents = "Buy Now";
textLayer.textItem.size     = 36;

// Collapse/expand group (Photopea specific, not in standard DOM)
// Use visibility as workaround

// Get specific layer inside a group
var innerLayer = doc.layerSets.getByName("Header Group").artLayers.getByName("Title");
```

---

## `TextItem` — 文本图层内容

通过 `layer.textItem` 访问任何 `layer.kind === LayerKind.TEXT` 的图层。

### 核心属性（最常用）

| 属性 | 类型 | 读/写 | 说明 |
|------|------|-------|------|
| `contents` | string | 读/写 | 实际文本内容 |
| `font` | string | 读/写 | 字体 PostScript 名称（如 `"ArialMT"`、`"Verdana-Bold"`） |
| `size` | number | 读/写 | 字号（磅） |
| `color` | SolidColor | 读/写 | 文本颜色 |
| `position` | array | 读/写 | 文本原点 `[x, y]`（点文本）或边界框左上角 |
| `justification` | Justification | 读/写 | `Justification.LEFT`、`CENTER`、`RIGHT`、`FULLJUSTIFY` |
| `kind` | TextType | 读/写 | `TextType.POINTTEXT` 或 `TextType.PARAGRAPHTEXT` |
| `width` | number | 读/写 | 边界框宽度（仅段落文本） |
| `height` | number | 读/写 | 边界框高度（仅段落文本） |
| `direction` | Direction | 读/写 | `Direction.HORIZONTAL` 或 `Direction.VERTICAL` |

### 排版属性

| 属性 | 类型 | 读/写 | 说明 |
|------|------|-------|------|
| `leading` | number | 读/写 | 行间距（磅） |
| `tracking` | number | 读/写 | 字间距 -1000–10000（1000 = 1 em） |
| `horizontalScale` | number | 读/写 | 水平缩放 0–1000% |
| `verticalScale` | number | 读/写 | 垂直缩放 0–1000% |
| `baselineShift` | number | 读/写 | 基线偏移（磅） |
| `capitalization` | Case | 读/写 | `Case.NORMAL`、`ALLCAPS`、`SMALLCAPS` |
| `fauxBold` | boolean | 读/写 | 伪粗体 |
| `fauxItalic` | boolean | 读/写 | 伪斜体 |
| `underline` | UnderlineType | 读/写 | `UnderlineType.NONE`、`UNDERLINELEFT`、`UNDERLINERIGHT` |
| `strikeThru` | StrikeThruType | 读/写 | `StrikeThruType.NONE`、`STRIKEBOX`、`STRIKEHEIGHT` |
| `antiAliasMethod` | AntiAlias | 读/写 | `AntiAlias.NONE`、`SHARP`、`CRISP`、`STRONG`、`SMOOTH` |
| `autoKerning` | AutoKernType | 读/写 | `AutoKernType.MANUAL`、`METRICS`、`OPTICAL` |
| `language` | Language | 读/写 | `Language.ENGLISH` 等 |
| `ligatures` | boolean | 读/写 | 启用连字 |
| `alternateLigatures` | boolean | 读/写 | 启用替代连字 |
| `oldStyle` | boolean | 读/写 | 旧式数字 |
| `noBreak` | boolean | 读/写 | 阻止此文本换行 |
| `useAutoLeading` | boolean | 读/写 | 使用字体内置行距 |
| `autoLeadingAmount` | number | 读/写 | 自动行距百分比 0.01–5000 |
| `hyphenation` | boolean | 读/写 | 启用连字符 |

### 段落属性

| 属性 | 类型 | 读/写 | 说明 |
|------|------|-------|------|
| `leftIndent` | number | 读/写 | 左缩进 -1296–1296 |
| `rightIndent` | number | 读/写 | 右缩进 -1296–1296 |
| `firstLineIndent` | number | 读/写 | 首行缩进 -1296–1296 |
| `spaceBefore` | number | 读/写 | 段前间距 -1296–1296 |
| `spaceAfter` | number | 读/写 | 段后间距 -1296–1296 |
| `hangingPuntuation` | boolean | 读/写 | 罗马悬挂标点 |
| `textComposer` | TextComposer | 读/写 | `TextComposer.ADOBEEVERYLINE`、`ADOBESINGLELINE` |

### 变形属性

| 属性 | 类型 | 读/写 | 说明 |
|------|------|-------|------|
| `warpStyle` | WarpStyle | 读/写 | `WarpStyle.NONE`、`ARC`、`ARCH`、`BULGE`、`SHELLLOWER`、`SHELLUPPER`、`FLAG`、`WAVE`、`FISH`、`RISE`、`FISHEYE`、`INFLATE`、`SQUEEZE`、`TWIST` |
| `warpDirection` | Direction | 读/写 | `Direction.HORIZONTAL` 或 `Direction.VERTICAL` |
| `warpBend` | number | 读/写 | 变形弯曲 -100–100 |
| `warpHorizontalDistortion` | number | 读/写 | 水平扭曲 -100–100 |
| `warpVerticalDistortion` | number | 读/写 | 垂直扭曲 -100–100 |

### Photopea 扩展

| 属性 | 类型 | 说明 |
|------|------|------|
| `totalTextStyle` | string | 包含文本所有样式参数的 JSON 字符串 |
| `transform` | string | JSON 数组 — 文本的仿射变换矩阵 |

### 方法

| 方法 | 说明 |
|------|------|
| `convertToShape()` | 将文本转换为以文本为剪贴路径的填充形状图层 |
| `createPath()` | 从文本轮廓创建工作路径 |

**实际示例：**
```js
var layer = doc.layers.getByName("Headline");
var text  = layer.textItem;

// Set content
text.contents = "Hello World";

// Style
text.font   = "Verdana-Bold";
text.size   = 72;
text.color.rgb.hexValue = "FF0000";    // red

// Position point text at (50, 100)
text.position = [50, 100];

// Center align
text.justification = Justification.CENTER;

// Paragraph text with bounding box
text.kind   = TextType.PARAGRAPHTEXT;
text.width  = new UnitValue("400 pixels");
text.height = new UnitValue("200 pixels");

// Letter spacing
text.tracking = 100;   // 10% spacing

// Scale text horizontally to 80%
text.horizontalScale = 80;

// Warp arc
text.warpStyle = WarpStyle.ARC;
text.warpBend  = 30;

// Read all text styles as JSON (Photopea extension)
var styles = JSON.parse(text.totalTextStyle);
app.echoToOE(JSON.stringify(styles));
```

---

## 从零创建文本图层

```js
app.preferences.rulerUnits = Units.PIXELS;

var layer = doc.artLayers.add();
layer.kind = LayerKind.TEXT;      // Convert blank layer to text
layer.name = "My Title";

var text = layer.textItem;
text.contents      = "Welcome";
text.font          = "ArialMT";
text.size          = 48;
text.justification = Justification.CENTER;
text.position      = [doc.width / 2, 100];

var color = new SolidColor();
color.rgb.red   = 255;
color.rgb.green = 255;
color.rgb.blue  = 255;
text.color = color;
```

---

## `SolidColor` — 颜色对象

```js
// RGB (most common in Photopea)
var c = new SolidColor();
c.rgb.red   = 255;      // 0–255
c.rgb.green = 128;
c.rgb.blue  = 0;
c.rgb.hexValue = "FF8000";   // Set via hex string (no #)

// CMYK
var c2 = new SolidColor();
c2.cmyk.cyan    = 0;    // 0–100
c2.cmyk.magenta = 50;
c2.cmyk.yellow  = 100;
c2.cmyk.black   = 0;

// Grayscale
var c3 = new SolidColor();
c3.gray.gray = 50;    // 0–100

// HSB
var c4 = new SolidColor();
c4.hsb.hue        = 30;    // 0–360
c4.hsb.saturation = 100;   // 0–100
c4.hsb.brightness = 100;   // 0–100

// Lab
var c5 = new SolidColor();
c5.lab.l = 50;   // 0–100
c5.lab.a = 20;   // -128–127
c5.lab.b = 40;   // -128–127

// Set as foreground color
app.foregroundColor = c;

// Use with selection fill
doc.selection.selectAll();
doc.selection.fill(c);
doc.selection.deselect();
```

---

## `Selection` — 选区对象

通过 `doc.selection` 访问。

### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `bounds` | array | `[left, top, right, bottom]` 边界矩形 |
| `solid` | boolean | 选区是否为实心矩形 |

### 方法

| 方法 | 签名 | 说明 |
|------|------|------|
| `selectAll` | `()` | 选择整个文档 |
| `deselect` | `()` | 取消选择 |
| `invert` | `()` | 反转选区 |
| `select` | `(region, type, feather, antiAlias)` | 选择多边形区域。region 为 `[x,y]` 点数组。SelectionType：`REPLACE`、`ADD`、`SUBTRACT`、`INTERSECT` |
| `feather` | `(radius)` | 羽化选区边缘 |
| `contract` | `(radius)` | 收缩选区 |
| `expand` | `(radius)` | 扩展选区 |
| `grow` | `(tolerance, antiAlias)` | 扩展选区至相似相邻像素 |
| `similar` | `(tolerance, antiAlias)` | 选择整个文档中的相似像素 |
| `smooth` | `(radius)` | 平滑选区边缘 |
| `selectBorder` | `(width)` | 仅选择当前选区的边框 |
| `resize` | `(widthPct, heightPct, anchor)` | 调整选区边界大小 |
| `rotate` | `(angle, anchor)` | 旋转选区边界 |
| `translate` | `(deltaX, deltaY)` | 移动选区边界 |
| `fill` | `(fillWith, mode, opacity, preserveTransparency)` | 用颜色或内容填充选区。fillWith 为 SolidColor 或字符串 |
| `stroke` | `(strokeColor, width, location, mode, opacity, preserveTransparency)` | 描边选区边框。StrokeLocation：`INSIDE`、`OUTSIDE`、`CENTER` |
| `copy` | `(merged)` | 复制选区到剪贴板 |
| `cut` | `()` | 剪切选区到剪贴板 |
| `clear` | `()` | 删除选区内容 |
| `load` | `(from, type, invert)` | 从通道载入选区 |
| `store` | `(into, type)` | 将选区存储为通道 |
| `makeWorkPath` | `(tolerance)` | 转换为工作路径 |

**实际示例：**
```js
var sel = doc.selection;

// Rectangle select (top-left to bottom-right)
sel.select([[0,0],[500,0],[500,300],[0,300]]);

// Select all
sel.selectAll();

// Add to existing selection
sel.select([[600,0],[900,0],[900,300],[600,300]], SelectionType.ADD);

// Feather 10px
sel.feather(10);

// Contract by 5px
sel.contract(5);

// Fill with red
var red = new SolidColor();
red.rgb.red = 255; red.rgb.green = 0; red.rgb.blue = 0;
sel.fill(red);

// Stroke selection with black, 3px, inside
var black = new SolidColor();
black.rgb.hexValue = "000000";
sel.stroke(black, 3, StrokeLocation.INSIDE);

// Copy, paste as new layer
sel.copy();
doc.paste();

// Invert and delete (remove background)
sel.invert();
sel.clear();
sel.deselect();
```

---

## `BlendMode` 枚举 — 所有值

在 `layer.blendMode`（Photopea 中的字符串形式）和 `BlendMode` 常量（标准形式）中使用：

| `BlendMode` 常量 | Photopea 字符串 | 名称 |
|------------------|-----------------|------|
| `BlendMode.NORMAL` | `"norm"` | 正常 |
| `BlendMode.DISSOLVE` | `"diss"` | 溶解 |
| `BlendMode.DARKEN` | `"dark"` | 变暗 |
| `BlendMode.MULTIPLY` | `"mul "` | 正片叠底 |
| `BlendMode.COLORBURN` | `"idiv"` | 颜色加深 |
| `BlendMode.LINEARBURN` | `"lbrn"` | 线性加深 |
| `BlendMode.DARKERCOLOR` | `"dkCl"` | 深色 |
| `BlendMode.LIGHTEN` | `"lite"` | 变亮 |
| `BlendMode.SCREEN` | `"scrn"` | 滤色 |
| `BlendMode.COLORDODGE` | `"div "` | 颜色减淡 |
| `BlendMode.LINEARDODGE` | `"lddg"` | 线性减淡（添加） |
| `BlendMode.LIGHTERCOLOR` | `"lgCl"` | 浅色 |
| `BlendMode.OVERLAY` | `"over"` | 叠加 |
| `BlendMode.SOFTLIGHT` | `"sLit"` | 柔光 |
| `BlendMode.HARDLIGHT` | `"hLit"` | 强光 |
| `BlendMode.VIVIDLIGHT` | `"vLit"` | 亮光 |
| `BlendMode.LINEARLIGHT` | `"lLit"` | 线性光 |
| `BlendMode.PINLIGHT` | `"pLit"` | 点光 |
| `BlendMode.HARDMIX` | `"hMix"` | 实色混合 |
| `BlendMode.DIFFERENCE` | `"diff"` | 差值 |
| `BlendMode.EXCLUSION` | `"smud"` | 排除 |
| `BlendMode.SUBTRACT` | `"fsub"` | 减去 |
| `BlendMode.DIVIDE` | `"fdiv"` | 划分 |
| `BlendMode.HUE` | `"hue "` | 色相 |
| `BlendMode.SATURATION` | `"sat "` | 饱和度 |
| `BlendMode.COLOR` | `"colr"` | 颜色 |
| `BlendMode.LUMINOSITY` | `"lum "` | 明度 |
| `BlendMode.PASSTHROUGH` | `"pass"` | 穿透（仅图层组） |

```js
// Use either form:
layer.blendMode = BlendMode.SCREEN;     // constant
layer.blendMode = "scrn";               // string (Photopea internal form)
```

---

## `LayerKind` 枚举

| 常量 | 说明 |
|------|------|
| `LayerKind.NORMAL` | 普通像素图层 |
| `LayerKind.TEXT` | 文本图层 |
| `LayerKind.SMARTOBJECT` | 智能对象/链接图层 |
| `LayerKind.SOLIDFILL` | 纯色填充图层 |
| `LayerKind.GRADIENTFILL` | 渐变填充图层 |
| `LayerKind.PATTERNFILL` | 图案填充图层 |
| `LayerKind.BRIGHTNESSCONTRAST` | 亮度/对比度调整图层 |
| `LayerKind.CURVES` | 曲线调整图层 |
| `LayerKind.LEVELS` | 色阶调整图层 |
| `LayerKind.HUESATURATION` | 色相/饱和度调整图层 |
| `LayerKind.COLORBALANCE` | 色彩平衡调整图层 |
| `LayerKind.CHANNELMIXER` | 通道混合器调整图层 |
| `LayerKind.GRADIENTMAP` | 渐变映射调整图层 |
| `LayerKind.INVERSION` | 反相调整图层 |
| `LayerKind.POSTERIZE` | 色调分离调整图层 |
| `LayerKind.THRESHOLD` | 阈值调整图层 |
| `LayerKind.SELECTIVECOLOR` | 可选颜色调整图层 |
| `LayerKind.PHOTOFILTER` | 照片滤镜调整图层 |
| `LayerKind.EXPOSURE` | 曝光调整图层 |
| `LayerKind.VIBRANCE` | 自然饱和度调整图层 |
| `LayerKind.COLORLOOKUP` | 颜色查找调整图层 |
| `LayerKind.LAYER3D` | 3D 图层（在 Photopea 中通常不可用） |
| `LayerKind.VIDEO` | 视频图层 |

```js
// Identify layer type
var layer = doc.activeLayer;
if (layer.kind === LayerKind.TEXT)         /* text layer */;
if (layer.kind === LayerKind.SMARTOBJECT)  /* smart object */;
if (layer.typename === "LayerSet")         /* group */;

// Filter: collect all text layers recursively
var textLayers = [];
function collectText(parent) {
  for (var i = 0; i < parent.layers.length; i++) {
    var l = parent.layers[i];
    if (l.typename === "LayerSet") collectText(l);
    else if (l.kind === LayerKind.TEXT) textLayers.push(l);
  }
}
collectText(doc);
```

---

## `AnchorPosition` 枚举

| 常量 | 位置 |
|------|------|
| `AnchorPosition.TOPLEFT` | 左上 |
| `AnchorPosition.TOPCENTER` | 上中 |
| `AnchorPosition.TOPRIGHT` | 右上 |
| `AnchorPosition.MIDDLELEFT` | 左中 |
| `AnchorPosition.MIDDLECENTER` | 居中 |
| `AnchorPosition.MIDDLERIGHT` | 右中 |
| `AnchorPosition.BOTTOMLEFT` | 左下 |
| `AnchorPosition.BOTTOMCENTER` | 下中 |
| `AnchorPosition.BOTTOMRIGHT` | 右下 |

---

## `ElementPlacement` 枚举

与 `layer.move(relativeObject, placement)` 一起使用：

| 常量 | 效果 |
|------|------|
| `ElementPlacement.PLACEBEFORE` | 在面板中位于目标图层上方 |
| `ElementPlacement.PLACEAFTER` | 在面板中位于目标图层下方 |
| `ElementPlacement.PLACEATBEGINNING` | 图层栈顶部 |
| `ElementPlacement.PLACEATEND` | 图层栈底部 |
| `ElementPlacement.INSIDE` | 放入 LayerSet（成为子图层） |

---

## `ResampleMethod` 枚举

与 `doc.resizeImage()` 一起使用：

| 常量 | 说明 |
|------|------|
| `ResampleMethod.BICUBIC` | 高质量，适合平滑渐变 |
| `ResampleMethod.BICUBICSHARPER` | 最适合缩小 |
| `ResampleMethod.BICUBICSMOOTHER` | 最适合放大 |
| `ResampleMethod.BILINEAR` | 中等质量 |
| `ResampleMethod.NEARESTNEIGHBOR` | 无抗锯齿，最快 |
| `ResampleMethod.NONE` | 不重采样（仅更改分辨率） |

---

## `SaveOptions` 枚举

与 `doc.close(saveOption)` 一起使用：

| 常量 | 含义 |
|------|------|
| `SaveOptions.DONOTSAVECHANGES` | 丢弃所有更改并关闭 |
| `SaveOptions.SAVECHANGES` | 保存后关闭 |
| `SaveOptions.PROMPTTOSAVECHANGES` | 显示对话框（无头模式下可能阻塞） |

---

## `ExportOptionsSaveForWeb` — 导出到文件系统

与 `doc.exportDocument()` 一起使用，将文件写入 Photopea 打包为 ZIP 的输出。

```js
// Export PNG
var pngOpts = new ExportOptionsSaveForWeb();
pngOpts.format      = SaveDocumentType.PNG;
pngOpts.PNG8        = false;    // PNG-24
pngOpts.quality     = 100;
pngOpts.transparency = true;
doc.exportDocument(new File("/export.png"), ExportType.SAVEFORWEB, pngOpts);

// Export JPEG
var jpgOpts = new ExportOptionsSaveForWeb();
jpgOpts.format  = SaveDocumentType.JPEG;
jpgOpts.quality = 80;    // 0–100
doc.exportDocument(new File("/export.jpg"), ExportType.SAVEFORWEB, jpgOpts);

// Export GIF
var gifOpts = new ExportOptionsSaveForWeb();
gifOpts.format     = SaveDocumentType.GIF;
gifOpts.colors     = 256;
gifOpts.dither     = 100;
gifOpts.transparency = true;
doc.exportDocument(new File("/export.gif"), ExportType.SAVEFORWEB, gifOpts);
```

---

## `executeAction` — 高级操作

用于标准 DOM 未暴露的操作（作为调整图层应用的调整、Smart Object 编辑等）。采用 Photoshop Action Manager 方式。

```js
// Open Smart Object for editing
var l = doc.layers.getByName("SmartObj");
doc.activeLayer = l;
executeAction(stringIDToTypeID("placedLayerEditContents"));
// Smart Object is now the active document
doc.activeLayer.rotate(90);
doc.save();
doc.close();

// Apply Hue/Saturation as destructive adjustment
var desc = new ActionDescriptor();
var list = new ActionList();
var channel = new ActionDescriptor();
channel.putEnumerated(stringIDToTypeID("presetKind"), stringIDToTypeID("presetKindType"), stringIDToTypeID("presetKindDefault"));
channel.putInteger(stringIDToTypeID("hue"),        20);   // hue shift
channel.putInteger(stringIDToTypeID("saturation"), 30);   // saturation
channel.putInteger(stringIDToTypeID("lightness"),  0);
list.putObject(stringIDToTypeID("hueSaturationAdjustmentV2Layer"), channel);
desc.putList(stringIDToTypeID("adjustment"), list);
executeAction(stringIDToTypeID("hueSaturation"), desc, DialogModes.NO);

// Select a layer by name using AM
function selectLayerByName(name) {
  var desc = new ActionDescriptor();
  var ref  = new ActionReference();
  ref.putName(charIDToTypeID("Lyr "), name);
  desc.putReference(charIDToTypeID("null"), ref);
  desc.putBoolean(charIDToTypeID("MkVs"), false);
  executeAction(charIDToTypeID("slct"), desc, DialogModes.NO);
}
```

---

## 完整实际脚本示例

### 1. 根据内容重命名所有文本图层
```js
app.preferences.rulerUnits = Units.PIXELS;
var doc = app.activeDocument;

function processLayers(parent) {
  for (var i = 0; i < parent.layers.length; i++) {
    var l = parent.layers[i];
    if (l.typename === "LayerSet") processLayers(l);
    else if (l.kind === LayerKind.TEXT) {
      l.name = l.textItem.contents.substring(0, 30);
    }
  }
}
processLayers(doc);
app.echoToOE("done");
```

### 2. 将每个图层导出为单独的 PNG
```js
app.preferences.rulerUnits = Units.PIXELS;
var doc = app.activeDocument;

for (var i = 0; i < doc.layers.length; i++) {
  // Hide all layers
  for (var j = 0; j < doc.layers.length; j++) doc.layers[j].visible = false;
  // Show only this layer
  doc.layers[i].visible = true;
  // Export
  var opts = new ExportOptionsSaveForWeb();
  opts.format  = SaveDocumentType.PNG;
  opts.PNG8    = false;
  opts.quality = 100;
  doc.exportDocument(
    new File("/" + doc.layers[i].name + ".png"),
    ExportType.SAVEFORWEB, opts
  );
}

// Restore visibility
for (var i = 0; i < doc.layers.length; i++) doc.layers[i].visible = true;
```

### 3. 在所有文本图层中查找和替换文本
```js
var searchText   = "2024";
var replaceText  = "2025";

function findReplaceText(parent) {
  for (var i = 0; i < parent.layers.length; i++) {
    var l = parent.layers[i];
    if (l.typename === "LayerSet") findReplaceText(l);
    else if (l.kind === LayerKind.TEXT) {
      var t = l.textItem;
      if (t.contents.indexOf(searchText) !== -1) {
        t.contents = t.contents.split(searchText).join(replaceText);
      }
    }
  }
}
findReplaceText(app.activeDocument);
app.echoToOE("Find & Replace complete");
```

### 4. 复制图层网格排列
```js
app.preferences.rulerUnits = Units.PIXELS;
var doc   = app.activeDocument;
var layer = doc.activeLayer;
var cols  = 4, rows = 3;
var padX  = 20, padY = 20;
var w = layer.bounds[2] - layer.bounds[0];
var h = layer.bounds[3] - layer.bounds[1];

for (var r = 0; r < rows; r++) {
  for (var c = 0; c < cols; c++) {
    if (r === 0 && c === 0) continue; // skip original
    var copy = layer.duplicate();
    var targetX = layer.bounds[0] + c * (w + padX);
    var targetY = layer.bounds[1] + r * (h + padY);
    copy.translate(targetX - copy.bounds[0], targetY - copy.bounds[1]);
    copy.opacity = 100 - (r * cols + c) * 5;
  }
}
```

### 5. 从 URL 应用水印
```js
app.preferences.rulerUnits = Units.PIXELS;
var doc = app.activeDocument;

// Open watermark as smart object layer
app.open("https://example.com/watermark.png", null, true);
var wm = doc.activeLayer;

// Resize to 20% of document width
var wmW = wm.bounds[2] - wm.bounds[0];
var targetW = doc.width * 0.2;
var scalePct = (targetW / wmW) * 100;
wm.resize(scalePct, scalePct, AnchorPosition.TOPLEFT);

// Move to bottom-right with 20px margin
var wmNewW = wm.bounds[2] - wm.bounds[0];
var wmNewH = wm.bounds[3] - wm.bounds[1];
wm.translate(
  doc.width  - wmNewW - 20 - wm.bounds[0],
  doc.height - wmNewH - 20 - wm.bounds[1]
);
wm.opacity = 60;
app.echoToOE("watermark applied");
```

### 6. 获取所有图层信息为 JSON
```js
function getLayerInfo(parent, depth) {
  depth = depth || 0;
  var result = [];
  for (var i = 0; i < parent.layers.length; i++) {
    var l = parent.layers[i];
    var info = {
      name:    l.name,
      type:    l.typename,
      visible: l.visible,
      opacity: l.opacity,
      depth:   depth
    };
    if (l.typename === "ArtLayer") {
      info.kind   = l.kind.toString();
      info.bounds = [l.bounds[0], l.bounds[1], l.bounds[2], l.bounds[3]];
      if (l.kind === LayerKind.TEXT) {
        info.text = l.textItem.contents;
        info.font = l.textItem.font;
        info.size = l.textItem.size;
      }
    } else if (l.typename === "LayerSet") {
      info.children = getLayerInfo(l, depth + 1);
    }
    result.push(info);
  }
  return result;
}
app.echoToOE(JSON.stringify(getLayerInfo(app.activeDocument)));
```

---

## 常见错误与陷阱

| 问题 | 原因 | 修复方法 |
|------|------|----------|
| `createEmbed` 永远不 resolve | 容器没有尺寸 | 给容器 `<div>` 添加 `width` + `height` CSS |
| `runScript` 返回 `["done"]` 但没有数据 | 脚本中没有 `echoToOE` | 对需要返回的任何值添加 `app.echoToOE(value)` |
| `result[0]` 是 `"done"` 而不是预期值 | `echoToOE` 未被执行 | 检查脚本逻辑是否有提前退出或错误 |
| 图片无法加载（网络错误） | CORS | 服务器必须响应 `Access-Control-Allow-Origin: *` |
| `openFromURL(url, true)` 图层未就绪 | 异步加载延迟 | 使用 `addImageAndWait` 工具函数 |
| `exportImage` 仅支持 PNG/JPG | `exportImage` 限制 | 使用 `runScript("saveToOE('webp:0.85')")` 导出其他格式 |
| 像素坐标行为异常 | 标尺单位错误 | 始终先设置 `app.preferences.rulerUnits = Units.PIXELS` |
| 文本 `size` 已设置但看起来不同 | 类型单位错误 | 设置 `app.preferences.typeUnits = TypeUnits.PIXELS` |
| 按名称找不到图层 | 图层层级错误 | 图层有作用域；对嵌套图层使用递归搜索 |
| `layer.bounds[0]` 返回 UnitValue 而非数字 | 标尺单位问题 | 读取 bounds 前强制设置 `Units.PIXELS` |
| Smart Object 编辑挂起 | 缺少 `doc.save(); doc.close()` | 编辑完 SO 后务必保存并关闭 |
| React 开发模式双重挂载 | Strict Mode | 在 `useEffect` 中使用 `if (peaRef.current) return` 守卫 |

---

## 限制

- 本技能涵盖宿主页面集成模式；不替代 Photopea 自身的条款、API 文档或许可指引。
- 远程 URL 加载取决于浏览器 CORS 行为、网络可用性以及用户的 Photopea 账户/会话状态。
- `runScript` 在嵌入的 Photopea 文档上下文中执行脚本。仅运行你理解的脚本，且仅对用户批准的文件操作。
- 在将动态值嵌入 `runScript` 字符串之前，请使用 `JSON.stringify` 序列化。禁止将用户提供的 URL、图层名称或文本直接拼接到 Photopea 脚本源码中。
- 导出行为可能因文档大小、浏览器内存限制以及当前 Photopea 运行时支持的格式而异。

---

## 来源

- photopea.js：https://github.com/yikuansun/PhotopeaAPI
- npm：https://www.npmjs.com/package/photopea
- Photopea Live Messaging API：https://www.photopea.com/api/live
- Photopea 脚本参考：https://www.photopea.com/learn/scripts
- Photoshop JS 脚本参考（兼容）：https://theiviaxx.github.io/photoshop-docs/Photoshop/index.html
- 插件开发 gists（addImageAndWait、getDocumentAsImage）：https://gist.github.com/yikuansun/c0f1a602b4e9d4e344a41c4f49ded3bf
