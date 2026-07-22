---
name: remotion
description: 使用 Remotion 从 Stitch 项目生成演示视频，支持平滑过渡、缩放和文字叠加。当用户要求"创建演示视频"、"生成视频教程"、"制作应用展示视频"、"Stitch 项目视频化"、"Remotion 视频生成"时使用。
allowed-tools:
  - "stitch*:*"
  - "remotion*:*"
  - "Bash"
  - "Read"
  - "Write"
  - "web_fetch"
risk: unknown
source: community
---

# Stitch to Remotion 演示视频

你是一位专注于从应用设计创建引人入胜的演示视频的视频制作专家。你将 Stitch 的屏幕检索能力与 Remotion 的程序化视频生成相结合，制作流畅、专业的演示作品。

## 概述

本技能使你能够创建展示应用屏幕的演示视频，具有专业的过渡效果、缩放特效和上下文文字叠加。工作流程从 Stitch 项目检索屏幕，并将其编排为 Remotion 视频组合。

## 前提条件

**必需：**
- 访问 Stitch MCP Server
- 访问 Remotion MCP Server（或 Remotion CLI）
- 已安装 Node.js 和 npm
- 包含已设计屏幕的 Stitch 项目

**推荐：**
- 熟悉 Remotion 的视频功能
- 理解 React 组件（Remotion 使用 React）

## 检索与网络

### 步骤 1：发现可用的 MCP 服务器

运行 `list_tools` 识别可用的 MCP 服务器及其前缀：
- **Stitch MCP**：查找 `stitch:` 或 `mcp_stitch:` 前缀
- **Remotion MCP**：查找 `remotion:` 或 `mcp_remotion:` 前缀

### 步骤 2：检索 Stitch 项目信息

1. **项目查找**（如果未提供项目 ID）：
   - 调用 `[stitch_prefix]:list_projects`，参数 `filter: "view=owned"`
   - 通过标题识别目标项目（例如 "Calculator App"）
   - 从 `name` 字段提取项目 ID（例如 `projects/13534454087919359824`）

2. **屏幕检索**：
   - 调用 `[stitch_prefix]:list_screens`，传入项目 ID（仅数字）
   - 查看屏幕标题以识别演示所需的所有屏幕
   - 从每个屏幕的 `name` 字段提取屏幕 ID

3. **屏幕元数据获取**：
   对每个屏幕：
   - 调用 `[stitch_prefix]:get_screen`，传入 `projectId` 和 `screenId`
   - 检索：
     - `screenshot.downloadUrl` — 视频的视觉素材
     - `htmlCode.downloadUrl` — 可选：用于提取文本/内容
     - `width`, `height` — 屏幕尺寸，用于正确缩放
     - 屏幕标题和描述，用于文字叠加

4. **素材下载**：
   - 使用 `web_fetch` 或带 `curl` 的 `Bash` 下载截图
   - 保存到暂存目录：`assets/screens/{screen-name}.png`
   - 按预期的演示流程顺序组织素材

### 步骤 3：设置 Remotion 项目

1. **检查现有 Remotion 项目**：
   - 查找 `remotion.config.ts` 或包含 Remotion 依赖的 `package.json`
   - 如果存在，使用现有项目结构

2. **创建新的 Remotion 项目**（如需要）：
   ```bash
   npm create video@latest -- --blank
   ```
   - 选择 TypeScript 模板
   - 在专用的 `video/` 目录中设置

3. **安装依赖**：
   ```bash
   cd video
   npm install @remotion/transitions @remotion/animated-emoji
   ```

## 视频组合策略

### 架构

使用以下组件创建模块化的 Remotion 组合：

1. **`ScreenSlide.tsx`** — 单个屏幕显示组件
   - 属性：`imageSrc`, `title`, `description`, `width`, `height`
   - 功能：缩放动画、淡入淡出过渡
   - 持续时间：可配置（默认每个屏幕 3-5 秒）

2. **`WalkthroughComposition.tsx`** — 主视频组合
   - 编排多个 `ScreenSlide` 组件
   - 处理屏幕间的过渡
   - 添加文字叠加和注释

3. **`config.ts`** — 视频配置
   - 帧率（默认：30 fps）
   - 视频尺寸（匹配 Stitch 屏幕尺寸或适当缩放）
   - 总时长计算

### 过渡效果

使用 Remotion 的 `@remotion/transitions` 实现专业效果：

- **Fade**：屏幕间的平滑交叉淡入淡出
  ```tsx
  import {fade} from '@remotion/transitions/fade';
  ```

- **Slide**：方向性滑动过渡
  ```tsx
  import {slide} from '@remotion/transitions/slide';
  ```

- **Zoom**：用于强调的缩放效果
  - 使用 `spring()` 动画实现平滑缩放
  - 应用于重要的 UI 元素

### 文字叠加

使用 Remotion 的文本渲染添加上下文信息：

1. **屏幕标题**：在每帧的顶部或底部显示
2. **功能标注**：用动画指针高亮特定 UI 元素
3. **描述**：为每个屏幕淡入描述性文字
4. **进度指示器**：显示演示中的当前屏幕位置

## 执行步骤

### 步骤 1：收集屏幕素材

1. 识别目标 Stitch 项目
2. 列出项目中的所有屏幕
3. 下载每个屏幕的截图
4. 按演示流程顺序组织
5. 创建清单文件（`screens.json`）：

```json
{
  "projectName": "Calculator App",
  "screens": [
    {
      "id": "1",
      "title": "Home Screen",
      "description": "Main calculator interface with number pad",
      "imagePath": "assets/screens/home.png",
      "width": 1200,
      "height": 800,
      "duration": 4
    },
    {
      "id": "2",
      "title": "History View",
      "description": "View of previous calculations",
      "imagePath": "assets/screens/history.png",
      "width": 1200,
      "height": 800,
      "duration": 3
    }
  ]
}
```

### 步骤 2：生成 Remotion 组件

遵循 Remotion 最佳实践创建视频组件：

1. **创建 `ScreenSlide.tsx`**：
   - 使用 `useCurrentFrame()` 和 `spring()` 实现动画
   - 实现缩放和淡入淡出效果
   - 添加正确计时的文字叠加

2. **创建 `WalkthroughComposition.tsx`**：
   - 导入屏幕清单
   - 使用 `<Sequence>` 组件编排屏幕
   - 在屏幕间应用过渡
   - 计算正确的计时和偏移

3. **更新 `remotion.config.ts`**：
   - 设置组合 ID
   - 配置视频尺寸
   - 设置帧率和时长

**参考资源：**
- 使用 `resources/screen-slide-template.tsx` 作为起点
- 遵循 `resources/composition-checklist.md` 确保完整性
- 查看 `examples/walkthrough/` 目录中的示例

### 步骤 3：预览和优化

1. **启动 Remotion Studio**：
   ```bash
   npm run dev
   ```
   - 打开基于浏览器的预览
   - 允许实时编辑和优化

2. **调整计时**：
   - 确保每个屏幕有适当的显示时长
   - 验证过渡是否平滑
   - 检查文字叠加的时机

3. **微调动画**：
   - 调整缩放效果的 spring 配置
   - 修改过渡的缓动函数
   - 确保文字始终可读

### 步骤 4：渲染视频

1. **使用 Remotion CLI 渲染**：
   ```bash
   npx remotion render WalkthroughComposition output.mp4
   ```

2. **替代方案：使用 Remotion MCP**（如果可用）：
   - 调用 `[remotion_prefix]:render`，传入组合详情
   - 指定输出格式（MP4、WebM 等）

3. **优化选项**：
   - 设置质量级别（`--quality`）
   - 配置编码器（`--codec h264` 或 `h265`）
   - 启用并行渲染（`--concurrency`）

## 高级功能

### 交互式热点

高亮可点击元素或重要功能：

```tsx
import {interpolate, useCurrentFrame} from 'remotion';

const Hotspot = ({x, y, label}) => {
  const frame = useCurrentFrame();
  const scale = spring({
    frame,
    fps: 30,
    config: {damping: 10, stiffness: 100}
  });
  
  return (
    <div style={{
      position: 'absolute',
      left: x,
      top: y,
      transform: `scale(${scale})`
    }}>
      <div className="pulse-ring" />
      <span>{label}</span>
    </div>
  );
};
```

### 旁白集成

为演示添加解说：

1. 从屏幕描述生成旁白脚本
2. 使用文本转语音或录制音频
3. 使用 `<Audio>` 组件将音频导入 Remotion
4. 将屏幕计时与旁白节奏同步

### 动态文本提取

从 Stitch HTML 代码提取文本以自动生成注释：

1. 下载每个屏幕的 `htmlCode.downloadUrl`
2. 解析 HTML 提取关键文本元素（标题、按钮、标签）
3. 为重要 UI 元素生成自动标注
4. 作为定时文字叠加添加到组合中

## 文件结构

```
project/
├── video/                      # Remotion 项目目录
│   ├── src/
│   │   ├── WalkthroughComposition.tsx
│   │   ├── ScreenSlide.tsx
│   │   ├── components/
│   │   │   ├── Hotspot.tsx
│   │   │   └── TextOverlay.tsx
│   │   └── Root.tsx
│   ├── public/
│   │   └── assets/
│   │       └── screens/        # 下载的 Stitch 截图
│   │           ├── home.png
│   │           └── history.png
│   ├── remotion.config.ts
│   └── package.json
├── screens.json                # 屏幕清单
└── output.mp4                  # 渲染后的视频
```

## 与 Remotion Skills 集成

Remotion 维护自己的 Agent Skills，定义了最佳实践。查看这些内容以获取高级技术：

- **仓库**：https://github.com/remotion-dev/remotion/tree/main/packages/skills
- **安装**：`npx skills add remotion-dev/skills`

可利用的关键 Remotion 技能：
- 动画计时和缓动
- 组合架构模式
- 性能优化
- 音频同步

## 常见模式

### 模式 1：简单幻灯片

带有淡入淡出过渡的基础演示：
- 每个屏幕 3-5 秒
- 交叉淡入淡出过渡
- 底部文字叠加显示屏幕标题
- 顶部进度条

### 模式 2：功能高亮

聚焦特定 UI 元素：
- 缩放到特定区域
- 动画圆圈/箭头指向功能
- 关键交互的慢动作强调
- 并排的前后对比

### 模式 3：用户流程

展示分步用户旅程：
- 带方向性滑动的顺序屏幕流
- 编号步骤叠加
- 高亮用户操作（点击、轻触）
- 用动画路径连接屏幕

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| **截图模糊** | 确保下载的图像为全分辨率；检查 `screenshot.downloadUrl` 质量设置 |
| **文字错位** | 验证屏幕尺寸与组合大小匹配；根据实际屏幕大小调整文字定位 |
| **动画卡顿** | 将帧率提高到 60fps；使用适当的 spring 配置和合适的阻尼 |
| **Remotion 构建失败** | 检查 Node 版本兼容性；确保所有依赖已安装；查阅 Remotion 文档 |
| **时机感觉不对** | 调整清单中每个屏幕的时长；在 Remotion Studio 中预览；与真实用户测试 |

## 最佳实践

1. **保持宽高比**：使用实际的 Stitch 屏幕尺寸或按比例缩放
2. **一致的计时**：除非强调特定屏幕，否则保持屏幕显示时长一致
3. **可读文字**：确保足够的对比度；使用适当的字体大小；避免杂乱的叠加
4. **平滑过渡**：使用 spring 动画实现自然运动；避免生硬的切换
5. **充分预览**：最终渲染前务必在 Remotion Studio 中预览
6. **优化素材**：适当压缩图像；使用高效格式（UI 用 PNG，照片用 JPG）

## 使用示例

**用户提示：**
```
Look up the screens in my Stitch project "Calculator App" and build a remotion video 
that shows a walkthrough of the screens.
```

**智能体工作流：**
1. 列出 Stitch 项目 → 找到 "Calculator App" → 提取项目 ID
2. 列出项目中的屏幕 → 识别所有屏幕（Home、History、Settings）
3. 下载每个屏幕的截图 → 保存到 `assets/screens/`
4. 创建包含屏幕元数据的 `screens.json` 清单
5. 生成 Remotion 组件（`ScreenSlide.tsx`、`WalkthroughComposition.tsx`）
6. 在 Remotion Studio 中预览 → 优化计时和过渡
7. 渲染最终视频 → `calculator-walkthrough.mp4`
8. 报告完成并提供视频预览链接

## 成功提示

- **从简单开始**：在添加复杂动画前，先从基础的淡入淡出过渡开始
- **遵循 Remotion 模式**：利用 Remotion 的官方技能和文档
- **使用清单文件**：将屏幕数据组织在 JSON 中以便轻松更新
- **频繁预览**：使用 Remotion Studio 及早发现问题
- **考虑无障碍**：添加字幕；确保文字可读；使用清晰的视觉效果
- **针对平台优化**：将视频尺寸匹配目标平台（YouTube、社交媒体等）

## 参考资料

- **Stitch 文档**：https://stitch.withgoogle.com/docs/
- **Remotion 文档**：https://www.remotion.dev/docs/
- **Remotion Skills**：https://www.remotion.dev/docs/ai/skills
- **Remotion MCP**：https://www.remotion.dev/docs/ai/mcp
- **Remotion Transitions**：https://www.remotion.dev/docs/transitions


## 使用时机
处理与上述主要领域或功能相关的任务时使用本技能。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
