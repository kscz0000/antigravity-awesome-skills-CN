---
name: makepad-platform
description: |
  Makepad 跨平台支持。当用户要求'makepad平台'、'makepad跨平台'、'makepad macos/windows/linux/android/ios/web'、'makepad metal/d3d11/opengl/webgl'、'OsType'、'CxOs'、'makepad平台支持'时使用。
risk: unknown
source: community
---

# Makepad 平台技能

> **版本：** makepad-widgets (dev 分支) | **最后更新：** 2026-01-19
>
> 检查更新：https://crates.io/crates/makepad-widgets

你是 Makepad 跨平台开发专家。帮助用户：
- **理解平台**：解释支持的平台和图形后端
- **平台特定代码**：协助条件编译和平台 API

## 适用场景
- 需要了解或针对 Makepad 中的特定平台和图形后端进行开发
- 涉及平台兼容性、条件编译，或桌面/移动/Web 间的系统特定行为
- 需要了解 Metal、D3D11、OpenGL、WebGL 等后端差异或平台模块

## 文档

详细文档请参考本地文件：
- `./references/platform-support.md` - 平台详情和 OsType

## 重要：文档完整性检查

**回答问题前，Claude 必须：**

1. 读取上方列出的相关参考文件
2. 如果文件读取失败或为空：
   - 告知用户："本地文档不完整，建议运行 `/sync-crate-skills makepad --force` 更新文档"
   - 仍基于 SKILL.md 模式和内置知识回答
3. 如果参考文件存在，将其内容纳入回答

## 支持的平台

| 平台 | 图形后端 | OS 模块 |
|------|----------|---------|
| macOS | Metal | `apple/metal_*.rs`, `apple/cocoa_*.rs` |
| iOS | Metal | `apple/metal_*.rs`, `apple/ios_*.rs` |
| Windows | D3D11 | `mswindows/d3d11_*.rs`, `mswindows/win32_*.rs` |
| Linux | OpenGL | `linux/opengl_*.rs`, `linux/x11*.rs`, `linux/wayland*.rs` |
| Web | WebGL2 | `web/*.rs`, `web_browser/*.rs` |
| Android | OpenGL ES | `android/*.rs` |
| OpenHarmony | OHOS | `open_harmony/*.rs` |
| OpenXR | VR/AR | `open_xr/*.rs` |

## OsType 枚举

```rust
pub enum OsType {
    Unknown,
    Windows,
    Macos,
    Linux { custom_window_chrome: bool },
    Ios,
    Android(AndroidParams),
    OpenHarmony,
    Web(WebParams),
    OpenXR,
}

// Check platform in code
fn handle_event(&mut self, cx: &mut Cx, event: &Event) {
    match cx.os_type() {
        OsType::Macos => { /* macOS-specific */ }
        OsType::Windows => { /* Windows-specific */ }
        OsType::Web(_) => { /* Web-specific */ }
        _ => {}
    }
}
```

## 平台检测

```rust
// In Cx
impl Cx {
    pub fn os_type(&self) -> OsType;
    pub fn gpu_info(&self) -> &GpuInfo;
    pub fn xr_capabilities(&self) -> &XrCapabilities;
    pub fn cpu_cores(&self) -> usize;
}
```

## 条件编译

```rust
// Compile-time platform detection
#[cfg(target_os = "macos")]
fn macos_only() { }

#[cfg(target_os = "windows")]
fn windows_only() { }

#[cfg(target_os = "linux")]
fn linux_only() { }

#[cfg(target_arch = "wasm32")]
fn web_only() { }

#[cfg(target_os = "android")]
fn android_only() { }

#[cfg(target_os = "ios")]
fn ios_only() { }
```

## 平台特定功能

### 桌面端（macOS/Windows/Linux）
- 窗口管理（调整大小、最小化、最大化）
- 文件对话框
- 系统菜单
- 拖放
- 多显示器

### 移动端（iOS/Android）
- 触摸输入
- 虚拟键盘
- 屏幕方向
- 应用生命周期（前台/后台）

### Web（WebGL2）
- DOM 集成
- 浏览器事件
- 本地存储
- HTTP 请求

## 入口点

```rust
// App entry macro
app_main!(App);

pub struct App {
    ui: WidgetRef,
}

impl LiveRegister for App {
    fn live_register(cx: &mut Cx) {
        // Register components
        crate::makepad_widgets::live_design(cx);
    }
}

impl AppMain for App {
    fn handle_event(&mut self, cx: &mut Cx, event: &Event) {
        // Handle app events
        self.ui.handle_event(cx, event, &mut Scope::empty());
    }
}
```

## 回答问题时

1. Makepad 为每个平台编译为原生代码（无运行时解释器）
2. 着色器在构建时为每个图形后端编译
3. 平台特定代码位于 `platform/src/os/` 目录
4. 使用 `cx.os_type()` 进行运行时平台检测
5. 使用 `#[cfg(target_os = "...")]` 进行编译时平台检测

## 限制
- 仅在任务明确匹配上述范围时使用本技能
- 输出不能替代环境特定的验证、测试或专家审查
- 缺少必要输入、权限、安全边界或成功标准时，停下来请求澄清