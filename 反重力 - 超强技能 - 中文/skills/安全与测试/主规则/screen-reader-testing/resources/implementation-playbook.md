# Screen Reader 测试实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

# Screen Reader 测试

使用 screen reader 测试 Web 应用程序以进行全面无障碍验证的实用指南。

## 何时使用此技能

- 验证 screen reader 兼容性
- 测试 ARIA 实现
- 调试辅助技术问题
- 验证表单无障碍性
- 测试动态内容公告
- 确保导航无障碍性

## 核心概念

### 1. 主要 Screen Reader

| Screen Reader | 平台      | 浏览器         | 使用率 |
| ------------- | --------- | -------------- | ------ |
| **VoiceOver** | macOS/iOS | Safari         | ~15%   |
| **NVDA**      | Windows   | Firefox/Chrome | ~31%   |
| **JAWS**      | Windows   | Chrome/IE      | ~40%   |
| **TalkBack**  | Android   | Chrome         | ~10%   |
| **Narrator**  | Windows   | Edge           | ~4%    |

### 2. 测试优先级

```
Minimum Coverage:
1. NVDA + Firefox (Windows)
2. VoiceOver + Safari (macOS)
3. VoiceOver + Safari (iOS)

Comprehensive Coverage:
+ JAWS + Chrome (Windows)
+ TalkBack + Chrome (Android)
+ Narrator + Edge (Windows)
```

### 3. Screen Reader 模式

| 模式               | 用途                 | 使用场景          |
| ------------------ | -------------------- | ----------------- |
| **Browse/Virtual** | 阅读内容             | 默认阅读模式      |
| **Focus/Forms**    | 与控件交互           | 填写表单          |
| **Application**    | 自定义小部件         | ARIA 应用程序     |

## VoiceOver (macOS)

### 设置

```
Enable: System Preferences → Accessibility → VoiceOver
Toggle: Cmd + F5
Quick Toggle: Triple-press Touch ID
```

### 基本命令

```
Navigation:
VO = Ctrl + Option (VoiceOver modifier)

VO + Right Arrow   Next element
VO + Left Arrow    Previous element
VO + Shift + Down  Enter group
VO + Shift + Up    Exit group

Reading:
VO + A             Read all from cursor
Ctrl               Stop speaking
VO + B             Read current paragraph

Interaction:
VO + Space         Activate element
VO + Shift + M     Open menu
Tab                Next focusable element
Shift + Tab        Previous focusable element

Rotor (VO + U):
Navigate by: Headings, Links, Forms, Landmarks
Left/Right Arrow   Change rotor category
Up/Down Arrow      Navigate within category
Enter              Go to item

Web Specific:
VO + Cmd + H       Next heading
VO + Cmd + J       Next form control
VO + Cmd + L       Next link
VO + Cmd + T       Next table
```

### 测试检查清单

```markdown
## VoiceOver 测试检查清单

### 页面加载

- [ ] 页面标题已播报
- [ ] 找到主 landmark
- [ ] 跳转链接有效

### 导航

- [ ] 所有标题可通过 rotor 发现
- [ ] 标题层级合理（H1 → H2 → H3）
- [ ] Landmark 已正确标记
- [ ] 跳转链接功能正常

### 链接与按钮

- [ ] 链接用途清晰
- [ ] 按钮操作已描述
- [ ] 新窗口/标签页已播报

### 表单

- [ ] 所有标签与输入框关联读取
- [ ] 必填字段已播报
- [ ] 错误消息已读取
- [ ] 说明信息可用
- [ ] 焦点移至错误处

### 动态内容

- [ ] 警报立即播报
- [ ] 加载状态已传达
- [ ] 内容更新已播报
- [ ] 模态框正确捕获焦点

### 表格

- [ ] 表头与单元格关联
- [ ] 表格导航正常
- [ ] 复杂表格有标题说明
```

### 常见问题与修复

```html
<!-- Issue: Button not announcing purpose -->
<button><svg>...</svg></button>

<!-- Fix -->
<button aria-label="Close dialog"><svg aria-hidden="true">...</svg></button>

<!-- Issue: Dynamic content not announced -->
<div id="results">New results loaded</div>

<!-- Fix -->
<div id="results" role="status" aria-live="polite">New results loaded</div>

<!-- Issue: Form error not read -->
<input type="email" />
<span class="error">Invalid email</span>

<!-- Fix -->
<input type="email" aria-invalid="true" aria-describedby="email-error" />
<span id="email-error" role="alert">Invalid email</span>
```

## NVDA (Windows)

### 设置

```
Download: nvaccess.org
Start: Ctrl + Alt + N
Stop: Insert + Q
```

### 基本命令

```
Navigation:
Insert = NVDA modifier

Down Arrow         Next line
Up Arrow           Previous line
Tab                Next focusable
Shift + Tab        Previous focusable

Reading:
NVDA + Down Arrow  Say all
Ctrl               Stop speech
NVDA + Up Arrow    Current line

Headings:
H                  Next heading
Shift + H          Previous heading
1-6                Heading level 1-6

Forms:
F                  Next form field
B                  Next button
E                  Next edit field
X                  Next checkbox
C                  Next combo box

Links:
K                  Next link
U                  Next unvisited link
V                  Next visited link

Landmarks:
D                  Next landmark
Shift + D          Previous landmark

Tables:
T                  Next table
Ctrl + Alt + Arrows Navigate cells

Elements List (NVDA + F7):
Shows all links, headings, form fields, landmarks
```

### 浏览模式与焦点模式

```
NVDA 自动切换模式：
- Browse Mode：方向键导航内容
- Focus Mode：方向键控制交互元素

手动切换：NVDA + Space

注意事项：
- 导航时播报 "Browse mode"
- 进入表单字段时播报 "Focus mode"
- Application role 强制进入 forms mode
```

### 测试脚本

```markdown
## NVDA 测试脚本

### 初始加载

1. 导航到页面
2. 等待页面加载完成
3. 按 Insert + Down 朗读全部
4. 注意：页面标题、主内容是否已识别？

### Landmark 导航

1. 反复按 D
2. 检查：所有主要区域是否可达？
3. 检查：Landmark 是否正确标记？

### 标题导航

1. 按 Insert + F7 → Headings
2. 检查：标题结构是否合理？
3. 按 H 导航标题
4. 检查：所有章节是否可发现？

### 表单测试

1. 按 F 查找第一个表单字段
2. 检查：标签是否已读取？
3. 填入无效数据
4. 提交表单
5. 检查：错误是否已播报？
6. 检查：焦点是否移至错误处？

### 交互元素

1. 用 Tab 遍历所有交互元素
2. 检查：每个元素是否播报角色和状态
3. 用 Enter/Space 激活按钮
4. 检查：结果是否已播报？

### 动态内容

1. 触发内容更新
2. 检查：变更是否已播报？
3. 打开模态框
4. 检查：焦点是否被捕获？
5. 关闭模态框
6. 检查：焦点是否返回？
```

## JAWS (Windows)

### 基本命令

```
Start: Desktop shortcut or Ctrl + Alt + J
Virtual Cursor: Auto-enabled in browsers

Navigation:
Arrow keys         Navigate content
Tab                Next focusable
Insert + Down      Read all
Ctrl               Stop speech

Quick Keys:
H                  Next heading
T                  Next table
F                  Next form field
B                  Next button
G                  Next graphic
L                  Next list
;                  Next landmark

Forms Mode:
Enter              Enter forms mode
Numpad +           Exit forms mode
F5                 List form fields

Lists:
Insert + F7        Link list
Insert + F6        Heading list
Insert + F5        Form field list

Tables:
Ctrl + Alt + Arrows Table navigation
```

## TalkBack (Android)

### 设置

```
Enable: Settings → Accessibility → TalkBack
Toggle: Hold both volume buttons 3 seconds
```

### 手势操作

```
Explore: Drag finger across screen
Next: Swipe right
Previous: Swipe left
Activate: Double tap
Scroll: Two finger swipe

Reading Controls (swipe up then right):
- Headings
- Links
- Controls
- Characters
- Words
- Lines
- Paragraphs
```

## 常见测试场景

### 1. 模态对话框

```html
<!-- Accessible modal structure -->
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc"
>
  <h2 id="dialog-title">Confirm Delete</h2>
  <p id="dialog-desc">This action cannot be undone.</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>
```

```javascript
// Focus management
function openModal(modal) {
  // Store last focused element
  lastFocus = document.activeElement;

  // Move focus to modal
  modal.querySelector("h2").focus();

  // Trap focus
  modal.addEventListener("keydown", trapFocus);
}

function closeModal(modal) {
  // Return focus
  lastFocus.focus();
}

function trapFocus(e) {
  if (e.key === "Tab") {
    const focusable = modal.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
    );
    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (e.shiftKey && document.activeElement === first) {
      last.focus();
      e.preventDefault();
    } else if (!e.shiftKey && document.activeElement === last) {
      first.focus();
      e.preventDefault();
    }
  }

  if (e.key === "Escape") {
    closeModal(modal);
  }
}
```

### 2. 实时区域

```html
<!-- Status messages (polite) -->
<div role="status" aria-live="polite" aria-atomic="true">
  <!-- Content updates will be announced after current speech -->
</div>

<!-- Alerts (assertive) -->
<div role="alert" aria-live="assertive">
  <!-- Content updates interrupt current speech -->
</div>

<!-- Progress updates -->
<div
  role="progressbar"
  aria-valuenow="75"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-label="Upload progress"
></div>

<!-- Log (additions only) -->
<div role="log" aria-live="polite" aria-relevant="additions">
  <!-- New messages announced, removals not -->
</div>
```

### 3. 标签页界面

```html
<div role="tablist" aria-label="Product information">
  <button role="tab" id="tab-1" aria-selected="true" aria-controls="panel-1">
    Description
  </button>
  <button
    role="tab"
    id="tab-2"
    aria-selected="false"
    aria-controls="panel-2"
    tabindex="-1"
  >
    Reviews
  </button>
</div>

<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  Product description content...
</div>

<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  Reviews content...
</div>
```

```javascript
// Tab keyboard navigation
tablist.addEventListener("keydown", (e) => {
  const tabs = [...tablist.querySelectorAll('[role="tab"]')];
  const index = tabs.indexOf(document.activeElement);

  let newIndex;
  switch (e.key) {
    case "ArrowRight":
      newIndex = (index + 1) % tabs.length;
      break;
    case "ArrowLeft":
      newIndex = (index - 1 + tabs.length) % tabs.length;
      break;
    case "Home":
      newIndex = 0;
      break;
    case "End":
      newIndex = tabs.length - 1;
      break;
    default:
      return;
  }

  tabs[newIndex].focus();
  activateTab(tabs[newIndex]);
  e.preventDefault();
});
```

## 调试技巧

```javascript
// Log what screen reader sees
function logAccessibleName(element) {
  const computed = window.getComputedStyle(element);
  console.log({
    role: element.getAttribute("role") || element.tagName,
    name:
      element.getAttribute("aria-label") ||
      element.getAttribute("aria-labelledby") ||
      element.textContent,
    state: {
      expanded: element.getAttribute("aria-expanded"),
      selected: element.getAttribute("aria-selected"),
      checked: element.getAttribute("aria-checked"),
      disabled: element.disabled,
    },
    visible: computed.display !== "none" && computed.visibility !== "hidden",
  });
}
```

## 最佳实践

### 推荐做法

- **使用真实 screen reader 测试** — 不要仅依赖模拟器
- **优先使用语义化 HTML** — ARIA 是补充手段
- **在浏览模式和焦点模式下测试** — 体验不同
- **验证焦点管理** — 尤其是单页应用
- **先进行纯键盘测试** — 这是 screen reader 测试的基础

### 避免做法

- **不要认为一种 screen reader 就够了** — 需要测试多种
- **不要忽视移动端** — 用户群体在增长
- **不要只测试正常流程** — 需要测试错误状态
- **不要跳过动态内容** — 这是最常见的问题
- **不要依赖视觉测试** — 体验完全不同

## 资源

- [VoiceOver 用户指南](https://support.apple.com/guide/voiceover/welcome/mac)
- [NVDA 用户指南](https://www.nvaccess.org/files/nvda/documentation/userGuide.html)
- [JAWS 文档](https://support.freedomscientific.com/Products/Blindness/JAWS)
- [WebAIM Screen Reader 调查](https://webaim.org/projects/screenreadersurvey/)
