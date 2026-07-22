# 创造模式：Gradio 中的自定义 HTML/JS UI

当 LoRA 的自然输入形状不适合任何标准 Gradio 组件或 Hub 自定义组件时，你可以降级到 Gradio 应用内的普通 HTML/CSS/JS。本文件是关于 *如何*——使它工作的 Gradio 原语，以及使其不变成一团乱麻的约束。

这是组件阶梯的第三级（参见 `tasks.md` → "选择组件"）：

1. **内置 Gradio 组件。** 首选。几乎对 T2I 和许多 I2I 都足够。
2. **Hub 自定义组件。** `gradio_image_annotation`、`gradio_imageslider`、`gradio_modal`、`gradio_rangeslider` 等。没有 JS，只是 `pip install` 和 import。
3. **创造模式（本文件）。** 自定义 HTML/JS，当用户的输入形状是上述都无法很好表达的东西——点集、轨迹、笔触、带元数据的区域选择、时间轴 scrubbing、3D 旋转小工具、区域上的颜色选择、媒体上的拖动手柄、关键帧输入、任何用户在媒体之上操作 *物体* 的场景。

跳过第二级是一个常见错误。如果 Hub 自定义组件合适，请使用——`gradio_image_annotation` 已经涵盖 bbox 绘制、标签分配和基本编辑，不需要一行 JS。

但第二级有其自己的约束（参见下面的"Hub 自定义组件很脆弱"）。这些 Space 最常见的失败模式是 **自定义组件静默渲染失败**：Python 端导入正常，页面加载，`SKILL.md` 阶段 6 中的 API smoke-test 通过——然而小部件根本不在页面上。打开 Space 的用户会看到周围的布局（按钮、accordion、输出），但没有上传区域、没有标注器，什么都没有。如果你不真正查看浏览器中渲染的页面，你将发布一个破损的 Space 而自己不知道。

## Hub 自定义组件很脆弱

将任何来自 Hub 的 `gradio_*` 包视为"承重但未针对你的 Gradio 版本测试"，直到你看到它渲染为止。最常见的失败模式：

- **版本不匹配的静默损坏。** 针对 Gradio N 构建的 Hub 组件可能加载（因为其声明的 `gradio<N+2,>=N` 范围涵盖了你的 `sdk_version`），但在稍新版本的 Gradio 上挂载到空 DOM 节点上。构建日志中没有 traceback。没有 Python 错误。该组件就是不出现，其余列在其间隙周围向上流动。这产生了"生成按钮在空白左列顶部"的 Space。
- **过时的发布。** 许多 Hub 自定义组件最后发布于 1–2 年前。从那时起 Gradio 前端已发生变化。根据你目标的 Gradio 版本检查包的发布日期；如果存在多个主要版本的差距，预期会有损坏。
- **参数形状不匹配。** 组件的 Python 签名接受一个 Svelte 端不再读取的参数。你的 `disable_edit_boxes=True` 不起作用，或者更糟，在 JS 端抛出错误，整个组件挂载失败。

在确定 Hub 组件之前的约束：

1. **检查包的最近发布日期**（PyPI 页面或 `pip index versions <pkg>`）。如果它早于你 `sdk_version` 中的 Gradio 发布日期，将其视为可疑。
2. **单独对组件进行 smoke-test**——一个五行 Gradio 应用，本地，*在* 集成到完整应用之前。如果它渲染，没问题。如果它缺失或空白，你已经廉价地捕获了损坏。
3. **当 Hub 组件无法渲染时，不要反复尝试其 kwargs。** 要么回退到 (a) 拆分内置组件（例如 `gr.Image` 用于上传 + 同级小部件用于框坐标），要么 (b) 第三级（通过 `gr.HTML` 的自定义 HTML/JS）。调 `disable_edit_boxes` / `use_default_label` / `sources` 不会让 Svelte 组件从 JS 端挂载失败中恢复。

同样的约束也适用于最近添加的不那么明显的"自定义"组件——例如 `gr.ImageSlider`，当与同一页面上的自定义组件配对时可能会意外渲染。

## 何时创造模式是正确的选择

当用户的 *自然* 输入在结构上超出内置组件所能表达的范围时，请使用它：

- **媒体之上的空间输入。** 在帧上绘制箭头、在图像上绘制笔触、沿轨迹放置点、选择不规则区域、绘制曲线。
- **多形状注释。** 源-目标框对、多个标记区域、按语义区分的有序点/框序列。
- **带吸附的连续控件。** 3D 旋转小工具、表盘/滚轮控件、时间轴 scrubber——任何滑块技术上可以工作但感觉不对的地方。
- **绑定在一起的复合控件。** 一个画布加上一个颜色选择器加上一个绑定到同一结构化输入的画笔尺寸表盘，其中绑定三个单独的组件并推理它们的联合状态比滚动一个小部件更丑陋。
- **依赖于多个输入的实时预览。** 用户希望在操作时 *立即* 看到的东西，其中每次更改一次的服务器往返太慢。

如果输入是"一个数字"、"一个字符串"或"一个图像"，你不需要这个。不要因为看起来很酷就构建自定义画布——构建它是因为 LoRA 的输入形状要求它。

## Gradio 原语

在阅读下面的模式之前，值得重新检查当前 Gradio 文档以了解最近新增的内容：

- `gr.HTML` — https://www.gradio.app/docs/gradio/html
- 自定义组件 — https://www.gradio.app/guides/custom-components-in-five-minutes
- `Blocks.launch(head=, css=)` — https://www.gradio.app/docs/gradio/blocks#blocks-launch

如果不确定签名，请通过 WebFetch 获取这些。自定义 HTML 表面积在不断演变，滞后于此会产生以陈旧方式"工作"的 Space。

创造模式构建自的原语：

### `gr.HTML` 用于任意标记

将任何 HTML 放入页面。该 block 成为一个常规的 Gradio 组件，但其内容是你编写的任何内容。你负责其中的所有内容：布局、样式、交互性。

```python
gr.HTML("""
<div id="my-widget" style="...">
  <canvas id="my-canvas" width="512" height="512"></canvas>
  <div id="my-status"></div>
</div>
""")
```

### `demo.launch(head=..., css=...)`

将 `<script>` 和 `<style>` 标签注入到页面 `<head>`。这是你加载外部 JS 库（Three.js、p5、fabric、anime.js 等）或定义需要在 `<head>` 中而不是内联的页面级 CSS 的方式。

```python
head = '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>'
css  = '.fillable {max-width: 1200px !important}'
demo.launch(head=head, css=css)
```

使用你能找到的最高质量的 CDN（cdnjs、jsdelivr、unpkg）。固定版本（`/three.js/r128/`，而不是 `/three.js/latest/`）。从 LoRA 作者的个人服务器加载是 Space 在他们的服务器移动时损坏的诱因。

### `elem_id` 和 `elem_classes` 用于寻址

每个 Gradio 组件接受 `elem_id="..."` 和 `elem_classes=[...]`。JS 使用这些来查找渲染的 DOM 节点：

```python
prompt_box = gr.Textbox(elem_id="my-prompt", elem_classes=["hidden-input"])
```

```javascript
const promptBox = document.getElementById("my-prompt");
// Note: the Gradio component wraps an <input> or <textarea>;
// you usually want the inner element:
const inner = promptBox.querySelector("input, textarea");
```

### JS 将状态推送到 Python 的两种方式

这是让人困惑的部分。选择适合你的情况并在整个小部件中坚持使用——在一个应用中混合它们令人困惑。

**方法 A — 隐藏的 Gradio 输入 + DOM 事件派发。** 定义一个隐藏的 `gr.Textbox`（或 `gr.JSON`、`gr.Number` 等）。从 JS 中，设置其内部 `<input>`/`<textarea>` 值并派发合成 `input` 和 `change` 事件，以便 Gradio 的响应性触发。

```python
state_json = gr.Textbox(value="{}", elem_id="state-json", visible=False)
```

```javascript
function setGradioValue(elemId, value) {
  const container = document.getElementById(elemId);
  if (!container) return;
  const el = container.querySelector("input, textarea");
  if (!el) return;
  const proto = el.tagName === "TEXTAREA"
    ? HTMLTextAreaElement.prototype
    : HTMLInputElement.prototype;
  const setter = Object.getOwnPropertyDescriptor(proto, "value").set;
  setter.call(el, value);
  el.dispatchEvent(new Event("input",  { bubbles: true }));
  el.dispatchEvent(new Event("change", { bubbles: true }));
}

setGradioValue("state-json", JSON.stringify(myState));
```

原生 setter 操作（`Object.getOwnPropertyDescriptor(...).set.call(el, value)`）是必要的，因为 React 会拦截普通的 `el.value = ...` 赋值，它们不会触发重新渲染。DOM 事件派发是让 Gradio 看到更改的关键。

此方法适用于任何 Gradio 版本，任何组件类型。缺点：大量粘合代码，对 DOM 结构变化脆弱，容易编写竞态条件。

**方法 B — 具有 `html_template`/`js_on_load` 的 `gr.HTML` 子类。** 较新的 Gradio 支持子类化 `gr.HTML` 并提供自定义 props 加上 `js_on_load` 脚本。该脚本获得一个带有自定义值的 `props` 对象和一个用于将事件发送回 Python 的 `trigger()` 函数。状态绑定是基于值的（Gradio 像读取任何其他组件一样读取 `value` prop）。

```python
class PointPicker(gr.HTML):
    def __init__(self, value=None, image_url=None, **kwargs):
        super().__init__(
            value=value or {"points": []},
            html_template="<canvas id='pp-canvas' width='512' height='512'></canvas>",
            js_on_load="""
                const canvas = document.getElementById('pp-canvas');
                canvas.addEventListener('click', (e) => {
                    const rect = canvas.getBoundingClientRect();
                    const x = (e.clientX - rect.left) / rect.width;
                    const y = (e.clientY - rect.top)  / rect.height;
                    props.value = {points: [...(props.value?.points || []), {x, y}]};
                    trigger('change', props.value);
                });
            """,
            image_url=image_url,
            **kwargs,
        )
```

更简洁、基于值、没有隐藏输入。缺点：需要足够新的 Gradio 版本来支持子类化形状，并且 JS 位于 Python 字符串内，IDE 不会对其 lint。

**在 A 和 B 之间选择：** 如果你从零开始并使用当前 Gradio，请优先选择 B——绑定语义更合理。当你需要与已存在的 Gradio 组件集成（应镜像画布状态的滑块、画布写入的 prompt 框）或当 UI shell 足够大以至于将它们放在 `gr.HTML` 子类中很尴尬时，请使用 A。

### Python 将状态推送到 JS 的两种方式

- **对于 B（子类）：** 从事件处理程序返回 `gr.update(prop=value)`。小部件的轮询循环看到 prop 更改并做出反应。
- **对于 A（隐藏输入）：** 从事件处理程序写入隐藏的 Gradio Textbox。JS 轮询 Textbox 值（或挂钩到 Gradio 的 mutation observer）并做出反应。

无论哪种方式，预期一个小的轮询间隔（通常为 50–200ms）。不要更快——它会在较弱的机器上主导 CPU。

### 事件处理程序上的 `js=`

对于小型仅 JS 的转换（例如"单击时滚动到结果"），事件处理程序接受一个 `js=` 参数，在浏览器中运行而无需服务器往返：

```python
btn.click(fn=infer, inputs=[...], outputs=[...], js="() => { window.scrollTo(0, 0); }")
```

对 UI 微调（滚动、聚焦、显示/隐藏加载器）有用，对状态管理无用。

## 通信契约

创造模式中最重要的约束：**定义 JS 和 Python 之间流动的 JSON 形状，并将其视为 API。**

将其作为注释写在 `app.py` 的顶部，即使只有一行。选择在 camelCase JS 和 snake_case Python 之间翻译时能保留的名称（或坚持一个并在边界处转换）：

```python
# State shape on the JS↔Python wire:
#   {
#     "src":    {"x1": float, "y1": float, "x2": float, "y2": float} | null,
#     "dst":    {"x1": float, "y1": float, "x2": float, "y2": float} | null,
#     "label":  string | null
#   }
```

一旦写下来，双方都有一个目标来遵循，你将尽早捕获形状漂移。

常见的形状原型——这些都不是必需的，仅作说明：

- **点集：** `{"points": [{"x": 0.3, "y": 0.4}, ...]}`
- **笔触集：** `{"strokes": [{"color": "#ff0", "size": 12, "points": [...]}, ...]}`
- **区域：** `{"regions": [{"label": "subject", "bbox": {...}}, ...]}`
- **变换：** `{"azimuth": 45, "elevation": 0, "distance": 1.0}`
- **带时间的轨迹：** `{"keyframes": [{"t": 0.0, "x": ...}, {"t": 0.5, ...}]}`

所有坐标归一化为 `[0, 1]` 几乎总是正确的选择——它可以在不重新缩放计算的情况下在图像调整大小时幸存下来。

## 外部库

使用有帮助的。能够轻量时保持轻量。

- **纯 canvas + DOM** 足以：绘制矩形/点/线、笔触、拖动手柄、图像叠加。
- **SVG** 用于：矢量叠加，特别是当标记需要清晰缩放或用 CSS 样式化时。
- **Three.js** 用于：3D 旋转小工具、深度可视化、任何需要 WebGL 渲染小型场景的地方。通过 `head=` 脚本标签引入。
- **fabric.js / paper.js / konva** 用于：当原始 canvas 变得丑陋时，画布上复杂的形状交互。在添加了超过约 200 行画布粘合代码后值得一试。
- **p5.js** 用于：快速原型设计生成艺术风格的画布。比生产所需的更重。

如有疑问，使用原始 canvas。为单个矩形引入 fabric 是过度设计；因为想要"更花哨的滑块"而引入 three.js 是一个坏味道。

## 陷阱

这些会反复出现。在编写前阅读。

- **Hub 自定义组件的静默挂载失败。** 上面详细介绍了。值得重申，因为它是 API smoke-test 无法捕获的失败模式：组件导入，页面加载，而小部件只是不在 DOM 中。始终在浏览器中验证；永远不要相信"构建变绿"作为 Hub 自定义组件渲染的证据。

- **与 Gradio 挂载的初始化竞态。** `js_on_load`（B）或通过 `head` 注入的顶层 `<script>` 可能在 Gradio 渲染你试图挂钩的 DOM 节点之前运行。用简短的 `setTimeout` 保护或等待元素存在：
  ```javascript
  function init() {
      const el = document.getElementById("my-widget");
      if (!el) { setTimeout(init, 50); return; }
      // ... do work
  }
  init();
  ```

- **双重初始化。** 如果用户在选项卡之间导航或 Gradio 重新渲染，你的初始化可能会触发两次。存放一个标志：`if (window.__myWidgetInited) return; window.__myWidgetInited = true;`。

- **Base64 图像传输成本。** 通过隐藏 Textbox 发送全分辨率图像作为 base64 字符串对于预览来说没问题，但对于 4K 图像来说惩罚性地慢。在 JS 端缩小后再塞入状态，或通过真实的 `gr.Image` 组件传递图像，仅通过隐藏通道发送 *交互状态*（框、点）。

- **文件输入不能通过隐藏 Textbox 往返。** 隐藏的 `gr.File` 不会接受任意 JS 设置的值。如果用户通过自定义 `<input type="file">` 上传，你有两种选择：(a) 在 JS 中读取文件，进行 base64 编码，并写入隐藏的 Textbox；(b) 将自定义文件输入连接到以编程方式点击真实的 `gr.File`（`document.querySelector("#real-file input").click()` 脆弱但有效）。

- **轮询节奏。** 100ms 是一个合理的默认值；50ms 感觉灵敏但会消耗较弱机器的 CPU；500ms 感觉迟钝。不要在 `requestAnimationFrame` 中轮询以进行状态同步——那是 60Hz，是过度设计。

- **移动 / 触摸。** 如果小部件位于将在手机上打开的 Space 中，请同时处理 `touchstart`/`touchmove`/`touchend` 和鼠标事件。两种事件系统的事情很烦人但不可避免。

- **payload 增长时的 ZeroGPU duration。** 如果自定义 UI 允许用户提交大状态（许多点、大笔触、多个框），服务器端处理时间可能随输入大小而增长。重新检查 `@spaces.GPU(duration=...)` 与最坏情况 payload。

- **自定义运行按钮。** 如果你在 HTML 中构建自己的"Run"按钮并让它通过 `.click()` 触发真实的 Gradio 按钮，请确保状态同步（写入隐藏输入）发生在点击 *之前*，并有足够的延迟让事件传播（`setTimeout(() => realBtn.click(), 50)` 是通常的修复）。

- **CSS 隔离。** Space 注入它们自己的 CSS。如果你的小部件样式被覆盖，请增加特异性（`#my-widget .foo` 而不是 `.foo`）或谨慎使用 `!important`。不要对所有内容使用内联样式来对抗它——这很快变得不可读。

## Smoke-test 警告 — 适用于第二级和第三级

`gradio info` / `gradio predict`（`SKILL.md` 阶段 6）仅测试 Python 端点。它们不告诉你实际渲染了什么。对于任何使用 Hub 自定义组件（第二级）或自定义 HTML/JS（第三级）的 Space，Python 端可以完全正确 *且* 用户可以看到破损的 UI。

两种不同的失败模式：

- **第二级静默挂载失败。** Hub 自定义组件干净地导入，在 Gradio 配置中获得一个槽位，并且根本不出现于渲染的 DOM 中。你看到它周围的组件但小部件本身消失了——例如在原本为空的列顶部留下一个 Generate 按钮。任何地方都没有错误。参见上面的"Hub 自定义组件很脆弱"。
- **第三级损坏的 JS。** 服务器端绿灯，但 `js_on_load` 出错，或 CDN 脚本加载失败，或你的事件处理程序从未绑定。小部件挂载但在被点击时没有任何反应。

在阶段 6 中的 API smoke-test 通过后，**在浏览器中打开 Space URL 并验证每个组件都可见且一次完整交互（上传 → 单击 Generate → 看到结果）工作**，然后再分享。对于这些 Space，这不是可选的——它是唯一能捕获上述失败模式的检查。

如果用户处于无法自行驱动浏览器的环境中，请要求他们打开 Space URL 并确认上传区域可见并接受图像，然后再声明 Space 完成。询问的代价是一条额外的消息；跳过的代价是发布一个看起来空白的 Space。

## 真实示例

这两个 Space 对非常不同的 LoRA 使用了上述模式。它们作为具体证明这些模式有效是有用的，而不是作为要复制的模板：

- **通过 Three.js 的 3D 相机控制**（方法 B，`gr.HTML` 子类）：https://huggingface.co/spaces/multimodalart/qwen-image-multiple-angles-3d-camera
- **通过 canvas 的边界框拖动/调整大小**（方法 A，隐藏输入 + 自定义 Run 按钮）：https://huggingface.co/spaces/linoyts/FLUX.2-klein-Move

在设计新小部件之前值得快速浏览每个——它们展示了这种调式的"生产级打磨"是什么感觉（snap-to-nearest 动画、状态叠加、悬停时的光标更改、移动触摸处理）。但你的小部件会看起来不同，因为你的 LoRA 需要不同的输入。