---
name: seo-image-gen
description: "生成 SEO 相关图片，如 OG 卡片、头图、Schema 资产、产品视觉图和信息图。当图片生成是 SEO 工作流或内容发布任务的一部分时使用。触发词：SEO图片生成、OG图片、头图生成、产品图片、信息图、Schema图片"
risk: unknown
source: "https://github.com/AgriciDaniel/claude-seo"
date_added: "2026-03-21"
argument-hint: "[og|hero|product|infographic|custom|batch] <description>"
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# SEO 图片生成：SEO 资产的 AI 图片生成（扩展）

使用 Gemini 的图片生成功能，通过 banana Creative Director 流水线生成用于 SEO 场景的生产级图片。将 SEO 需求映射为优化的领域模式、宽高比和分辨率默认值。

## 适用场景
- 生成 OG 图片、头图、Schema 视觉图、信息图或类似 SEO 资产时使用
- 图片生成是更广泛的 SEO 或发布工作流的一部分时使用
- 仅在所需图片生成扩展可用时使用

## 架构说明

此技能有两个组件，各司其职：
- **SKILL.md**（本文件）：处理交互式 `/seo image-gen` 命令以生成图片
- **智能体**（`agents/seo-image-gen.md`）：在 `/seo audit` 期间生成的仅审计分析器，用于评估现有的 OG/社交图片并制定生成计划（不会自动生成）

## 前置条件

此技能需要安装 banana 扩展：
```bash
./extensions/banana/install.sh
```

**检查可用性：** 使用任何图片生成工具前，先检查 MCP 服务器是否已连接，确认 `gemini_generate_image` 或 `set_aspect_ratio` 工具是否可用。如工具不可用，告知用户扩展未安装并提供安装说明。

## 快速参考

| 命令 | 功能 |
|------|------|
| `/seo image-gen og <description>` | 生成 OG/社交预览图（1200x630 效果） |
| `/seo image-gen hero <description>` | 博客头图（宽屏、戏剧化） |
| `/seo image-gen product <description>` | 产品摄影（简洁、白色背景） |
| `/seo image-gen infographic <description>` | 信息图视觉（竖版、数据密集） |
| `/seo image-gen custom <description>` | 自定义图片，完整 Creative Director 流水线 |
| `/seo image-gen batch <description> [N]` | 生成 N 个变体（默认：3） |

## SEO 图片用例

每个用例映射到预配置的 banana 参数：

| 用例 | 宽高比 | 分辨率 | 领域模式 | 说明 |
|------|--------|--------|----------|------|
| **OG/社交预览** | `16:9` | `1K` | Product 或 UI/Web | 简洁、专业、文字友好 |
| **博客头图** | `16:9` | `2K` | Cinema 或 Editorial | 戏剧化、有氛围、编辑级质量 |
| **Schema 图片** | `4:3` | `1K` | Product | 简洁、描述性强、Schema ImageObject |
| **社交方形图** | `1:1` | `1K` | UI/Web | 平台优化的方形图 |
| **产品照片** | `4:3` | `2K` | Product | 白色背景、影棚灯光 |
| **信息图** | `2:3` | `4K` | Infographic | 数据密集、竖版布局 |
| **Favicon/图标** | `1:1` | `512` | Logo | 简约、可缩放、辨识度高 |
| **Pinterest Pin** | `2:3` | `2K` | Editorial | 竖版长卡片 |

## 生成流水线

每个生成请求的流程：

1. **识别用例**：从命令或上下文中确定（og、hero、product 等）
2. **应用 SEO 默认值**：使用上方用例表中的参数
3. **设置宽高比**：通过 `set_aspect_ratio` MCP 工具
4. **构建推理简报**：使用 banana Creative Director 流水线：
   - 加载 `references/prompt-engineering.md` 获取 6 组件系统
   - 应用领域模式权重（主题 30%、风格 25%、背景 15% 等）
   - 必须具体且有画面感：描述镜头看到的内容
5. **生成**：通过 `gemini_generate_image` MCP 工具
6. **生成后 SEO 检查清单**（见下方）

### 检查预设

如用户提及品牌或已配置 SEO 预设：
```bash
python3 ~/.claude/skills/seo-image-gen/scripts/presets.py list
```
加载匹配的预设并作为默认值应用。同时查看 `references/seo-image-presets.md` 获取 SEO 专属预设模板。

## 生成后 SEO 检查清单

每次成功生成后，引导用户完成：

1. **Alt 文本**：为生成的图片编写描述性、包含关键词的 alt 文本
2. **文件命名**：重命名为 SEO 友好格式：`keyword-description-widthxheight.webp`
3. **WebP 转换**：转换为 WebP 以优化页面速度：
   ```bash
   magick output.png -quality 85 output.webp
   ```
4. **文件大小**：头图目标 200KB 以下，缩略图目标 100KB 以下
5. **Schema 标记**：为生成的图片建议 `ImageObject` Schema：
   ```json
   {
     "@type": "ImageObject",
     "url": "https://example.com/images/keyword-description.webp",
     "width": 1200,
     "height": 630,
     "caption": "包含目标关键词的描述性说明"
   }
   ```
6. **OG meta 标签**：对于社交预览图，提醒添加：
   ```html
   <meta property="og:image" content="https://example.com/images/og-image.webp" />
   <meta property="og:image:width" content="1200" />
   <meta property="og:image:height" content="630" />
   <meta property="og:image:alt" content="描述性 alt 文本" />
   ```

## 成本意识

图片生成会产生费用，请保持透明：
- 生成前显示预估成本（尤其是批量生成时）
- 记录每次生成：`python3 ~/.claude/skills/seo-image-gen/scripts/cost_tracker.py log --model MODEL --resolution RES --prompt "brief"`
- 用户询问用量时运行 `cost_tracker.py summary`

大致成本（gemini-3.1-flash）：
- 512：约 $0.02/张
- 1K 分辨率：约 $0.04/张
- 2K 分辨率：约 $0.08/张
- 4K 分辨率：约 $0.16/张

## 模型路由

| 场景 | 模型 | 原因 |
|------|------|------|
| OG 图片、社交预览 | `gemini-3.1-flash-image-preview` @ 1K | 快速、性价比高 |
| 头图、产品照片 | `gemini-3.1-flash-image-preview` @ 2K | 质量 + 细节 |
| 带文字的信息图 | `gemini-3.1-flash-image-preview` @ 2K, thinking: high | 文字渲染更佳 |
| 快速草稿 | `gemini-2.5-flash-image` @ 512 | 快速迭代 |

## 错误处理

| 错误 | 解决方案 |
|------|----------|
| MCP 未配置 | 运行 `./extensions/banana/install.sh` |
| API 密钥无效 | 在 https://aistudio.google.com/apikey 获取新密钥 |
| 速率限制（429） | 等待 60 秒后重试。免费层：约 10 RPM / 约 500 RPD |
| `IMAGE_SAFETY` | 重新措辞提示词 - 参见 `references/prompt-engineering.md` 安全部分 |
| MCP 不可用 | 回退方案：`python3 ~/.claude/skills/seo-image-gen/scripts/generate.py --prompt "..." --aspect-ratio "16:9"` |
| 扩展未安装 | 显示安装说明：`./extensions/banana/install.sh` |

## 跨技能集成

- **seo-images**（分析）输入到 **seo-image-gen**（生成）：`/seo images` 的审计结果识别缺失或低质量图片；用这些发现驱动 `/seo image-gen` 命令
- **seo-audit** 生成 seo-image-gen **智能体**（非本技能）来分析全站的 OG/社交图片并制定优先级排序的生成计划
- **seo-schema** 可使用生成的图片：生成后建议指向新资产的 `ImageObject` Schema 标记

## 参考文档

按需加载，不要在启动时全部加载：
- `references/prompt-engineering.md`：6 组件系统、领域模式、模板
- `references/gemini-models.md`：模型规格、速率限制、能力
- `references/mcp-tools.md`：MCP 工具参数和响应
- `references/post-processing.md`：ImageMagick/FFmpeg 流水线方案
- `references/cost-tracking.md`：定价、用量追踪
- `references/presets.md`：品牌预设管理
- `references/seo-image-presets.md`：SEO 专属预设模板

## 响应格式

生成后，始终提供：
1. **图片路径**：保存位置
2. **构造的提示词**：展示发送给 API 的内容（具有教育意义）
3. **设置**：模型、宽高比、分辨率
4. **SEO 检查清单**：alt 文本建议、文件命名、WebP 转换
5. **Schema 代码片段**：如适用，提供 ImageObject 或 og:image 标记

## 限制条件
- 仅在任务明确匹配上述范围时使用此技能
- 不要将输出视为环境特定验证、测试或专家评审的替代品
- 如缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清
