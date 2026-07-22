# Loki Mode 演示

Loki Mode 视频演示 - 多智能体自主创业系统。

## 快速开始

```bash
# 带屏幕录制的完整端到端演示（推荐）
./demo/record-full-demo.sh simple-todo

# 或运行模拟终端演示
./demo/run-demo-auto.sh
```

## 完整端到端演示

`record-full-demo.sh` 脚本创建真实演示，展示：
- Loki Mode 自主运行
- 带智能体和任务的仪表板
- 应用实时构建
- 质量门和代码审查

### 最佳效果设置

运行前按如下方式安排屏幕：

```
+------------------+------------------+
|                  |                  |
|   终端           |   浏览器         |
|   (运行脚本)     |   (仪表板)       |
|                  |                  |
+------------------+------------------+
```

### 运行演示

```bash
# 简单待办应用（5-10 分钟）
./demo/record-full-demo.sh simple-todo

# 静态落地页（3-5 分钟）
./demo/record-full-demo.sh static-landing

# 全栈应用（15-30 分钟）
./demo/record-full-demo.sh full-stack
```

仪表板打开于：http://127.0.0.1:57374/dashboard/index.html

## 演示内容

| 文件 | 用途 |
|------|------|
| `run-demo.sh` | 交互式演示脚本 |
| `record-demo.sh` | 用 asciinema 录制演示 |
| `voice-over-script.md` | 视频旁白脚本 |
| `vhs-tape.tape` | 用于 GIF/视频生成的 VHS 脚本 |

## 录制选项

### 选项 1：Asciinema（终端录制）

```bash
# 录制
./demo/record-demo.sh

# 回放
asciinema play demo/recordings/loki-demo.cast

# 上传到 asciinema.org
asciinema upload demo/recordings/loki-demo.cast
```

### 选项 2：VHS（GIF/视频生成）

```bash
# 安装 VHS
brew install charmbracelet/tap/vhs

# 生成 GIF
vhs demo/vhs-tape.tape

# 输出：demo/loki-demo.gif
```

### 选项 3：屏幕录制

1. 打开终端并运行 `./demo/run-demo.sh`
2. 使用 QuickTime 或 OBS 进行屏幕录制
3. 使用 `voice-over-script.md` 添加配音

## 配音录制

参见 `voice-over-script.md` 获取带时间戳的完整旁白脚本。

### 配音录制技巧

1. 先通读一遍脚本
2. 让您的旁白与终端操作匹配
3. 保持活力但专业
4. 在关键时刻暂停以示强调

## 演示场景

### 简单待办应用（5 分钟）
最适合快速演示。展示核心 Loki Mode 工作流程。

```bash
./demo/run-demo.sh simple-todo
```

### 全栈演示（15-20 分钟）
完整演示包括：
- 看板可视化
- 并行智能体执行
- 代码审查流程
- 质量门

```bash
./demo/run-demo.sh full-stack
```

## 已发布演示

| 演示 | 时长 | 链接 |
|------|------|------|
| 快速开始 | 5 分钟 | [asciinema](https://asciinema.org/a/loki-quick-start) |
| 完整演示 | 15 分钟 | [YouTube](https://youtube.com/watch?v=loki-demo) |

## 创建最终视频

1. 用 asciinema 或屏幕录制录制终端
2. 单独录制配音（更干净的音频）
3. 在视频编辑器中合并（iMovie、DaVinci Resolve）
4. 添加片头/片尾卡片
5. 导出为 MP4
