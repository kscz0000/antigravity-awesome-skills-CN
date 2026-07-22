---
name: screenstudio-alt
description: "开源无界面 Screen Studio 替代方案：自动加速空闲片段、点击簇自动缩放、按键叠加芯片、平滑合成光标、以及跟随动作的 9:16 竖屏导出 — 基于 CLI 的屏幕录制后期制作。"
risk: critical
source: community
source_type: community
source_repo: connerkward/screenstudio-alternative-skill
date_added: "2026-06-16"
author: Conner K Ward
license: MIT
tags:
  - screen-recording
  - video
  - post-production
  - auto-zoom
  - vertical-video
  - ffmpeg
tools:
  - claude-code
  - antigravity
  - cursor
  - gemini-cli
  - codex-cli
plugin:
  targets:
    codex: blocked
    claude: blocked
  setup:
    type: manual
    summary: "屏幕/输入捕获需要敏感的本地权限；不要放入插件安全捆绑包。"
    docs: SKILL.md
---
## 何时使用

当需要为分享而精修屏幕录制/演示视频时使用；当用户提到 Screen Studio、自动缩放、空闲加速、或竖屏/社交视频（来自屏幕捕获）时使用；以及任何面向社交的演示（竖屏输出为默认模式）时使用。

_来源：[connerkward/screenstudio-alternative-skill](https://github.com/connerkward/screenstudio-alternative-skill)（MIT）。_

# screenstudio-alt 替代方案

本技能的代码位于此目录（`polish.py`、`render.py`、`studio.py`、`events-log.swift`、测试固件等）。通过 publish-skill 技能以 `connerkward/screen-studio-alternative` 公开发布。

两个组件：

- `events-log`（Swift）— 捕获端输入记录器（光标 60Hz、点击、按键；在 macOS 安全输入期间丢弃按键）。仅在录制时运行。需要终端的辅助功能/输入监控权限。**自动缩放/按键/光标需要在捕获时获取此数据 — 无法从像素事后恢复。**
- `polish.py`（Python，ffmpeg + PIL）— 后期处理通道：

```bash
python3 src/polish.py in.mp4 --events in.events.jsonl \
  --speedup            # 压缩空闲段（输入间隔 ∩ 像素冻结；动画保持 1x 速度）
  --zoom               # 点击簇上的缓动自动缩放（zoompan）
  --keys               # 累积按键芯片（PIL 叠加，不依赖 drawtext）
  --smooth-cursor      # 合成缓动光标（配合 sck-record --no-cursor 效果最佳）
  --vertical           # 同时输出跟随动作的 1080x1920 竖屏
```

`--speedup` 无需事件数据即可工作（仅用 freezedetect）— 可用于整个现有的日常素材库。

- `render.py` — **高质量非破坏性渲染器**（首选）：单次通过弹簧物理相机，在原始高分辨率帧上运行，LANCZOS 缩放到较小目标（锐利缩放，比 ffmpeg 放大路径清晰约 1.3 倍），60fps，横屏 + 9:16 竖屏。可调 `--freq`/`--zeta`（弹簧参数）、`--fps`、`--target-w`。接受显式 `--regions [{t0,t1,z,cx,cy}]`。`polish.py` 是较旧的 ffmpeg 滤镜回退方案。
- `studio.py [recording.mp4]` — 本地 Web UI，**NLE 风格固定标尺时间线**（条 = 源时长，永不重缩放 → 上游始终锚定）：缩放区域为可拖拽块（移动/重定时边缘/点击添加/双击删除）；空闲段为**仅速率编辑的速度块** — 源范围锁定，速率通过选中时的检查器滑块或右边缘**速率拉伸**拖拽设置（类似 FCP 重定时 / Premiere 速率拉伸）；速率变更仅向下游涟漪传播。可调余弦缓动斜坡、默认缩放、画面比例、帧样式。始终平滑的合成光标 + 点击涟漪 + 真实录制点击音效（CC0 #735771）。导出使用 render.py。空闲端口，本地运行。（按键叠加在引擎中存在但默认关闭。）

## 简易路径

`screencast.sh --demo`（screencast 技能）完成整个链路：启动事件记录器、录制、然后自动精修 + 输出 9:16 竖屏。竖屏是面向社交演示的默认模式。

## 踩坑记录（经验教训，记录于此以免重蹈覆辙）

- ffmpeg 无法做动画 `scale=eval=frame` → `crop`（链接重初始化会卡死 crop 的逐帧表达式）。因此缩放使用 `zoompan`（其中没有 `t` 变量 — 使用 `on/FPS`）。
- 本机 ffmpeg 缺少 `drawtext`；所有文字/光标叠加都是 PIL 渲染的 PNG + `overlay`。
- 测试装置：`make-fixture.py` 合成伪造屏幕录制 + 真实事件 events.jsonl — 信任真实素材前先用它验证任何变更。

## 局限性

- 本工作流假设 FFmpeg 及配套脚本在本地可用；它不是托管式视频编辑器。
- 精修光标、点击和按键效果依赖录制时捕获的事件日志；缺少日志将限制可重建的内容。
- 自动缩放和空闲加速仍需人工审核节奏、构图和平台特定的审美偏好。
