# App Store 优化（ASO）技能

**版本**：1.0.0
**最后更新**：2025 年 11 月 7 日
**作者**：Claude Skills Factory

## 概述

一个综合性的 App Store 优化（ASO）技能，提供完整的研究、优化和追踪移动应用在 Apple App Store 和 Google Play Store 上表现的能力。本技能帮助应用开发者和营销人员在竞争激烈的应用市场中最大化应用的可见性、下载量和成功率。

## 本技能的功能

本技能在七个关键领域提供端到端的 ASO 能力：

1. **研究与分析**：关键词研究、竞品分析、市场趋势、评论情感
2. **元数据优化**：标题、描述、关键词，支持平台专属字符限制
3. **转化优化**：A/B 测试框架、视觉素材优化
4. **评分与评论管理**：情感分析、回复策略、问题识别
5. **上线与更新策略**：上线前检查清单、时机优化、更新规划
6. **分析与追踪**：ASO 评分、关键词排名、绩效基准对比
7. **本地化**：多语言策略、翻译管理、ROI 分析

## 核心功能

### 全面的关键词研究
- 搜索量和竞争度分析
- 长尾关键词发现
- 竞品关键词提取
- 关键词难度评分
- 策略性优先级排序

### 平台专属元数据优化
- **Apple App Store**：
  - 标题（30 字符）
  - 副标题（30 字符）
  - 推广文本（170 字符）
  - 描述（4000 字符）
  - 关键词字段（100 字符）
- **Google Play Store**：
  - 标题（50 字符）
  - 简短描述（80 字符）
  - 完整描述（4000 字符）
- 字符限制验证
- 关键词密度分析
- 多种优化策略

### 竞品情报
- 自动竞品发现
- 元数据策略分析
- 视觉素材评估
- 差距识别
- 竞争定位

### ASO 健康评分
- 0-100 总分
- 四分类细分（元数据、评分、关键词、转化）
- 优势和劣势识别
- 优先行动建议
- 预期影响估算

### 科学 A/B 测试
- 测试设计和假设制定
- 样本量计算
- 统计显著性分析
- 时长估算
- 实施建议

### 全球本地化
- 市场优先级排序（第一/二/三层级）
- 翻译成本估算
- 各语言字符限制适配
- 文化关键词考量
- ROI 分析

### 评论情报
- 情感分析
- 常见主题提取
- Bug 和问题识别
- 功能需求聚类
- 专业回复模板

### 上线规划
- 平台专属检查清单
- 时间线生成
- 合规性验证
- 最佳时机建议
- 季节性活动规划

## Python 模块

本技能包含 8 个强大的 Python 模块：

### 1. keyword_analyzer.py
**用途**：分析关键词的搜索量、竞争度和相关性

**核心函数**：
- `analyze_keyword()`：单个关键词分析
- `compare_keywords()`：多关键词比较和排名
- `find_long_tail_opportunities()`：生成长尾变体
- `calculate_keyword_density()`：分析文本中的关键词使用
- `extract_keywords_from_text()`：从评论/描述中提取关键词

### 2. metadata_optimizer.py
**用途**：优化标题、描述、关键词，支持字符限制验证

**核心函数**：
- `optimize_title()`：生成最优标题选项
- `optimize_description()`：创建以转化为导向的描述
- `optimize_keyword_field()`：最大化 Apple 的 100 字符关键词字段
- `validate_character_limits()`：确保平台合规
- `calculate_keyword_density()`：分析关键词整合

### 3. competitor_analyzer.py
**用途**：分析竞品 ASO 策略

**核心函数**：
- `analyze_competitor()`：单个竞品深入分析
- `compare_competitors()`：多竞品分析
- `identify_gaps()`：发现竞争机会
- `_calculate_competitive_strength()`：评分竞品 ASO 质量

### 4. aso_scorer.py
**用途**：计算综合 ASO 健康评分

**核心函数**：
- `calculate_overall_score()`：0-100 ASO 健康评分
- `score_metadata_quality()`：评估元数据优化
- `score_ratings_reviews()`：评估评分质量和数量
- `score_keyword_performance()`：分析排名位置
- `score_conversion_metrics()`：评估转化率
- `generate_recommendations()`：优先改进行动

### 5. ab_test_planner.py
**用途**：规划和追踪 ASO 元素的 A/B 测试

**核心函数**：
- `design_test()`：创建测试假设和结构
- `calculate_sample_size()`：确定所需访客量
- `calculate_significance()`：评估统计有效性
- `track_test_results()`：监控进行中的测试
- `generate_test_report()`：创建全面的测试报告

### 6. localization_helper.py
**用途**：管理多语言 ASO 优化

**核心函数**：
- `identify_target_markets()`：优先本地化市场
- `translate_metadata()`：适配各语言的元数据
- `adapt_keywords()`：文化关键词适配
- `validate_translations()`：字符限制验证
- `calculate_localization_roi()`：估算投资回报

### 7. review_analyzer.py
**用途**：分析用户评论以获取可执行洞察

**核心函数**：
- `analyze_sentiment()`：计算情感分布
- `extract_common_themes()`：识别高频话题
- `identify_issues()`：发现 Bug 和问题
- `find_feature_requests()`：提取用户期望的功能
- `track_sentiment_trends()`：监控随时间的变化
- `generate_response_templates()`：创建评论回复

### 8. launch_checklist.py
**用途**：生成全面的上线和更新检查清单

**核心函数**：
- `generate_prelaunch_checklist()`：完整的提交验证
- `validate_app_store_compliance()`：检查指南合规性
- `create_update_plan()`：规划更新频率
- `optimize_launch_timing()`：推荐上线日期
- `plan_seasonal_campaigns()`：识别季节性机会

## 安装

### 适用于 Claude Code（桌面版/CLI）

#### 项目级安装
```bash
# 复制技能文件夹到项目
cp -r app-store-optimization /path/to/your/project/.claude/skills/

# Claude 将在此项目中自动加载该技能
```

#### 用户级安装（在所有项目中可用）
```bash
# 复制技能文件夹到用户级技能目录
cp -r app-store-optimization ~/.claude/skills/

# Claude 将在所有项目中加载此技能
```

### 适用于 Claude Apps（浏览器版）

1. 使用 `skill-creator` 技能导入
2. 或通过 Claude Apps 界面手动导入

### 验证

验证安装：
```bash
# 检查技能文件夹是否存在
ls ~/.claude/skills/app-store-optimization/

# 你应该看到：
# SKILL.md
# keyword_analyzer.py
# metadata_optimizer.py
# competitor_analyzer.py
# aso_scorer.py
# ab_test_planner.py
# localization_helper.py
# review_analyzer.py
# launch_checklist.py
# sample_input.json
# expected_output.json
# HOW_TO_USE.md
# README.md
```

## 使用示例

### 示例 1：完整关键词研究

```
Hey Claude—I just added the "app-store-optimization" skill. Can you research keywords for my fitness app? I'm targeting people who want home workouts, yoga, and meal planning. Analyze top competitors like Nike Training Club and Peloton.
```

**Claude 将执行**：
- 使用 `keyword_analyzer.py` 研究关键词
- 使用 `competitor_analyzer.py` 分析 Nike Training Club 和 Peloton
- 提供带搜索量、竞争度的优先关键词列表
- 识别差距和长尾机会
- 推荐标题的主关键词和描述的次关键词

### 示例 2：优化 App Store 元数据

```
Hey Claude—I just added the "app-store-optimization" skill. Optimize my app's metadata for both Apple App Store and Google Play Store:
- App: FitFlow
- Category: Health & Fitness
- Features: AI workout plans, nutrition tracking, progress photos
- Keywords: fitness app, workout planner, home fitness
```

**Claude 将执行**：
- 使用 `metadata_optimizer.py` 创建优化标题（多个选项）
- 生成平台专属描述（简短和完整）
- 优化 Apple 的 100 字符关键词字段
- 验证所有字符限制
- 计算关键词密度
- 提供优化前后对比

### 示例 3：计算 ASO 健康评分

```
Hey Claude—I just added the "app-store-optimization" skill. Calculate my app's ASO score:
- Average rating: 4.3 stars (8,200 ratings)
- Keywords in top 10: 4
- Keywords in top 50: 15
- Conversion rate: 3.8%
- Title: "FitFlow - Home Workouts"
- Description: 1,500 characters with 3 keyword mentions
```

**Claude 将执行**：
- 使用 `aso_scorer.py` 计算总分（0-100）
- 按分类细分（元数据：X/25，评分：X/25，关键词：X/25，转化：X/25）
- 识别优势和劣势
- 生成优先建议
- 估算改进的影响

### 示例 4：A/B 测试规划

```
Hey Claude—I just added the "app-store-optimization" skill. I want to A/B test my app icon. My current conversion rate is 4.2%. How many visitors do I need and how long should I run the test?
```

**Claude 将执行**：
- 使用 `ab_test_planner.py` 设计测试
- 计算所需样本量（基于最小可检测效应）
- 估算低/中/高流量场景下的测试时长
- 提供测试结构和成功指标
- 说明如何分析结果

### 示例 5：评论情感分析

```
Hey Claude—I just added the "app-store-optimization" skill. Analyze my last 500 reviews and tell me:
- Overall sentiment
- Most common complaints
- Top feature requests
- Bugs needing immediate fixes
```

**Claude 将执行**：
- 使用 `review_analyzer.py` 处理评论
- 计算情感分布
- 提取常见主题
- 识别和优先排序问题
- 聚类功能需求
- 生成回复模板

### 示例 6：上线前检查清单

```
Hey Claude—I just added the "app-store-optimization" skill. Generate a complete pre-launch checklist for both app stores. My launch date is March 15, 2026.
```

**Claude 将执行**：
- 使用 `launch_checklist.py` 生成检查清单
- 创建 Apple App Store 检查清单（元数据、素材、技术、法律）
- 创建 Google Play Store 检查清单（元数据、素材、技术、法律）
- 添加通用检查清单（营销、QA、支持）
- 生成带里程碑的时间线
- 计算完成百分比

## 最佳实践

### 关键词研究
1. 从 20-30 个种子关键词开始
2. 分析你分类中的前 5 名竞品
3. 平衡高搜索量和长尾关键词
4. 优先考虑相关性而非搜索量
5. 每季度更新关键词研究

### 元数据优化
1. 在标题中前置关键词（前 15 个字符最重要）
2. 用满每个可用字符（不要浪费空间）
3. 先为人写，再为搜索引擎写
4. 在确认前先 A/B 测试重大变更
5. 每次重大发布时更新描述

### A/B 测试
1. 一次只测试一个元素（图标 vs 截图 vs 标题）
2. 运行测试直到统计显著（90%+ 置信度）
3. 先测试高影响元素（图标影响最大）
4. 留出足够时长（至少 1 周，最好 2-3 周）
5. 记录经验教训以供未来测试

### 本地化
1. 从前 5 大收入市场开始（美国、中国、日本、德国、英国）
2. 使用专业翻译人员，而非机器翻译
3. 让母语者测试翻译
4. 根据文化背景适配关键词
5. 按市场监控 ROI

### 评论管理
1. 在 24-48 小时内回复评论
2. 始终保持专业，即使面对负面评论
3. 解决提出的具体问题
4. 感谢用户的正面反馈
5. 利用洞察优先排序产品改进

## 技术要求

- **Python**：3.7+（用于 Python 模块）
- **平台支持**：Apple App Store、Google Play Store
- **数据格式**：JSON 输入/输出
- **依赖**：仅标准库（无需外部包）

## 限制

### 数据依赖
- 关键词搜索量为估算值（无 Apple/Google 官方数据）
- 竞品数据仅限于公开信息
- 评论分析需要访问公开评论
- 新应用可能没有历史数据

### 平台约束
- Apple：元数据变更需要提交应用（推广文本除外）
- Google：元数据变更需要 1-2 小时才能被索引
- A/B 测试需要大量流量才能达到统计显著性
- 商店算法为专有算法，可能随时变更

### 范围
- 不包含付费用户获取（Apple Search Ads、Google Ads）
- 不涵盖应用内分析实现
- 不处理技术性应用开发
- 专注于有机发现和转化优化

## 故障排除

### 问题：找不到 Python 模块
**解决方案**：确保所有 .py 文件与 SKILL.md 在同一目录下

### 问题：字符限制验证失败
**解决方案**：检查你是否使用了正确的平台（'apple' 或 'google'）

### 问题：关键词研究返回结果有限
**解决方案**：提供更多关于你的应用、功能和目标受众的上下文

### 问题：ASO 评分似乎不准确
**解决方案**：确保你提供了准确的指标（评分、关键词排名、转化率）

## 版本历史

### 版本 1.0.0（2025 年 11 月 7 日）
- 初始发布
- 8 个 Python 模块，提供全面的 ASO 能力
- 支持 Apple App Store 和 Google Play Store
- 关键词研究、元数据优化、竞品分析
- ASO 评分、A/B 测试、本地化、评论分析
- 上线规划和季节性活动工具

## 支持与反馈

本技能旨在帮助应用开发者和营销人员在竞争激烈的应用市场中取得成功。为获得最佳效果：

1. 提供关于你应用的详细上下文
2. 有具体指标时请包含
3. 有疑问时提出后续问题
4. 根据结果迭代

## 致谢

由 Claude Skills Factory 开发
基于行业标准 ASO 最佳实践
平台要求截至 2025 年 11 月

## 许可

本技能按原样提供，用于 Claude Code 和 Claude Apps。可根据你的具体用例自定义和扩展。

---

**准备好优化你的应用了吗？** 从关键词研究开始，然后进行元数据优化，最后实施 A/B 测试以持续改进。本技能涵盖从上线前规划到持续优化的一切。

详细使用示例请参阅 [HOW_TO_USE.md](HOW_TO_USE.md)。
