---
name: content-creator
description: "专业级品牌声音分析、SEO 优化和平台专属内容框架。"
category: marketing
risk: unknown
source: community
date_added: "2026-02-27"
---

# Content Creator

专业级品牌声音分析、SEO 优化和平台专属内容框架。

## 何时使用

撰写博客文章、创建社交媒体内容、建立品牌声音、优化 SEO 内容或规划内容日历时使用此技能。

## 关键词

content creation, blog posts, SEO, brand voice, social media, content calendar, marketing content, content strategy, content marketing, brand consistency, content optimization, social media marketing, content planning, blog writing, content frameworks, brand guidelines, social media strategy

## 快速入门

### 品牌声音开发

1. 在现有内容上运行 `scripts/brand_voice_analyzer.py` 建立基线
2. 查看 `references/brand_guidelines.md` 选择声音属性
3. 在所有内容中一致地应用选定的声音

### 博客内容创作

1. 从 `references/content_frameworks.md` 选择模板
2. 研究主题关键词
3. 按照模板结构撰写内容
4. 运行 `scripts/seo_optimizer.py [file] [primary-keyword]` 进行优化
5. 发布前应用优化建议

### 社交媒体内容

1. 查看 `references/social_media_optimization.md` 中的平台最佳实践
2. 使用 `references/content_frameworks.md` 中的适当模板
3. 根据平台专属指南进行优化
4. 使用 `assets/content_calendar_template.md` 安排发布

## 核心工作流

### 建立品牌声音（首次设置）

为新的品牌或客户创建内容时：

1. **分析现有内容**（如果可用）
   ```bash
   python scripts/brand_voice_analyzer.py existing_content.txt
   ```
   
2. **定义声音属性**
   - 查看 `references/brand_guidelines.md` 中的品牌人格原型
   - 选择主要和次要原型
   - 选择 3-5 个语调属性
   - 记录在品牌指南中

3. **创建声音样本**
   - 用选定的声音写 3 个样本内容
   - 使用分析器测试一致性
   - 根据结果进行优化

### 创建 SEO 优化的博客文章

1. **关键词研究**
   - 确定主要关键词（搜索量 500-5000/月）
   - 找到 3-5 个次要关键词
   - 列出 10-15 个 LSI 关键词

2. **内容结构**
   - 使用 `references/content_frameworks.md` 中的博客模板
   - 在标题、首段和 2-3 个 H2 中包含关键词
   - 目标 1,500-2,500 字以实现全面覆盖

3. **优化检查**
   ```bash
   python scripts/seo_optimizer.py blog_post.md "primary keyword" "secondary,keywords,list"
   ```

4. **应用 SEO 建议**
   - 将关键词密度调整至 1-3%
   - 确保正确的标题结构
   - 添加内部和外部链接
   - 优化 meta description

### 社交媒体内容创作

1. **平台选择**
   - 根据受众确定主要平台
   - 查看 `references/social_media_optimization.md` 中的平台专属指南

2. **内容适配**
   - 从博客文章或核心信息开始
   - 使用 `references/content_frameworks.md` 中的复用矩阵
   - 按照模板为每个平台进行适配

3. **优化清单**
   - 平台合适的长度
   - 最佳发布时间
   - 正确的图片尺寸
   - 平台专属标签
   - 互动元素（投票、问题）

### 内容日历规划

1. **月度规划**
   - 复制 `assets/content_calendar_template.md`
   - 设定月度目标和 KPI
   - 确定关键活动/主题

2. **周分布**
   - 遵循 40/25/25/10 内容支柱比例
   - 平衡一周内各平台内容
   - 与最佳发布时间对齐

3. **批量创作**
   - 在一个会话中创建所有周内容
   - 在各内容间保持一致的声音
   - 一起准备所有视觉素材

## 关键脚本

### brand_voice_analyzer.py

分析文本内容的语音特征、可读性和一致性。

**用法**：`python scripts/brand_voice_analyzer.py <file> [json|text]`

**返回**：
- 语音特征（正式度、语调、视角）
- 可读性评分
- 句子结构分析
- 改进建议

### seo_optimizer.py

分析内容的 SEO 优化并提供可操作的建议。

**用法**：`python scripts/seo_optimizer.py <file> [primary_keyword] [secondary_keywords]`

**返回**：
- SEO 评分（0-100）
- 关键词密度分析
- 结构评估
- Meta 标签建议
- 具体优化建议

## 参考指南

### 何时使用各参考文档

**references/brand_guidelines.md**
- 设置新的品牌声音
- 确保内容间的一致性
- 培训新团队成员
- 解决声音/语调问题

**references/content_frameworks.md**
- 开始任何新内容创作
- 构建不同类型的内容
- 创建内容模板
- 规划内容复用

**references/social_media_optimization.md**
- 平台专属优化
- 标签策略开发
- 理解算法因素
- 设置分析追踪

## 最佳实践

### 内容创作流程

1. 始终从受众需求/痛点出发
2. 写作前先研究
3. 使用模板创建大纲
4. 不编辑直接写初稿
5. 进行 SEO 优化
6. 按品牌声音编辑
7. 校对和核实事实
8. 针对平台优化
9. 策略性安排发布

### 质量指标

- SEO 评分高于 75/100
- 可读性适合目标受众
- 全文品牌声音一致
- 清晰的价值主张
- 可操作的要点
- 正确的视觉格式
- 平台优化

### 常见陷阱避免

- 研究关键词前就写作
- 忽视平台专属要求
- 品牌声音不一致
- 过度 SEO 优化（关键词堆砌）
- 缺少清晰的 CTA
- 未经校对就发布
- 忽视分析反馈

## 绩效指标

追踪这些 KPI 以衡量内容成功：

### 内容指标

- 自然流量增长
- 页面平均停留时间
- 跳出率
- 社交分享
- 获得的外链

### 互动指标

- 评论和讨论
- 邮件点击率
- 社交媒体互动率
- 内容下载量
- 表单提交量

### 业务指标

- 产生的线索
- 转化率
- 客户获取成本
- 收入归因
- 每篇内容的 ROI

## 集成点

此技能与以下工具配合效果最佳：
- 分析平台（Google Analytics、社交媒体洞察）
- SEO 工具（用于关键词研究）
- 设计工具（用于视觉内容）
- 排程平台（用于内容分发）
- 邮件营销系统（用于通讯内容）

## 快速命令

```bash
# 分析品牌声音
python scripts/brand_voice_analyzer.py content.txt

# SEO 优化
python scripts/seo_optimizer.py article.md "main keyword"

# 检查内容是否符合品牌指南
grep -f references/brand_guidelines.md content.txt

# 创建月度日历
cp assets/content_calendar_template.md this_month_calendar.md
```

## 限制

- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出作为环境专属验证、测试或专家评审的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
