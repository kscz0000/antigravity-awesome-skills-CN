---
name: app-store-optimization
description: "完整的 App Store 优化（ASO）工具包，用于研究、优化和追踪移动应用在 Apple App Store 和 Google Play Store 上的表现。当用户要求'ASO优化'、'应用商店优化'、'关键词研究'、'元数据优化'、'竞品分析'、'A/B测试'、'应用评分管理'、'上架优化'、'本地化策略'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# App Store 优化（ASO）技能

本综合技能提供完整的 ASO 能力，帮助你在 Apple App Store 和 Google Play Store 上成功上线和优化移动应用。

## 能力

### 研究与分析
- **关键词研究**：分析关键词的搜索量、竞争度和相关性，提升应用发现率
- **竞品分析**：深入分析你所在分类中表现最佳的应用
- **市场趋势分析**：识别应用分类中的新兴趋势和机会
- **评论情感分析**：从用户评论中提取洞察，发现优势和问题
- **分类分析**：评估最佳分类和子分类的投放策略

### 元数据优化
- **标题优化**：创建具有最佳关键词布局的吸引力标题（遵循各平台字符限制）
- **描述优化**：撰写既能转化又能排名的简短描述和完整描述
- **副标题/推广文本**：优化 Apple 专属副标题（30字符）和推广文本（170字符）
- **关键词字段**：通过策略性选择最大化 Apple 的 100 字符关键词字段
- **分类选择**：基于数据推荐主分类和次分类
- **图标最佳实践**：设计高转化应用图标的指南
- **截图优化**：创建驱动安装量的截图策略
- **预览视频**：应用预览视频的最佳实践
- **本地化**：面向全球市场的多语言优化策略

### 转化优化
- **A/B 测试框架**：规划和追踪元数据实验，实现持续改进
- **视觉素材测试**：测试图标、截图和视频以获得最大转化
- **商店列表优化**：全面的页面优化，提升从曝光到安装的转化率
- **行动号召**：优化描述和推广材料中的 CTA

### 评分与评论管理
- **评论监控**：追踪和分析用户评论，获取可执行的洞察
- **回复策略**：回复评论的模板和最佳实践
- **评分提升**：有机提升应用评分的策略方法
- **问题识别**：从评论中发现常见问题和功能需求

### 上线与更新策略
- **上线前检查清单**：提交到商店前的完整验证
- **上线时机**：优化发布时间以获得最大曝光和下载量
- **更新频率**：规划最佳更新频率和功能发布节奏
- **功能公告**：撰写能重新吸引用户的"新功能"内容
- **季节性优化**：利用季节性趋势和事件

### 分析与追踪
- **ASO 评分**：计算多维度综合 ASO 健康评分
- **关键词排名**：追踪关键词排名位置随时间的变化
- **转化指标**：监控从曝光到安装的转化率
- **下载速度**：追踪下载趋势和增长势头
- **绩效基准对比**：与分类平均值和竞品进行比较

### 平台专属要求
- **Apple App Store**：
  - 标题：30 字符
  - 副标题：30 字符
  - 推广文本：170 字符（无需应用更新即可编辑）
  - 描述：4,000 字符
  - 关键词：100 字符（逗号分隔，不加空格）
  - 新功能：4,000 字符
- **Google Play Store**：
  - 标题：50 字符（原 30 字符，2021 年增加）
  - 简短描述：80 字符
  - 完整描述：4,000 字符
  - 无独立关键词字段（关键词从标题和描述中提取）

## 输入要求

### 关键词研究
```json
{
  "app_name": "MyApp",
  "category": "Productivity",
  "target_keywords": ["task manager", "productivity", "todo list"],
  "competitors": ["Todoist", "Any.do", "Microsoft To Do"],
  "language": "en-US"
}
```

### 元数据优化
```json
{
  "platform": "apple" | "google",
  "app_info": {
    "name": "MyApp",
    "category": "Productivity",
    "target_audience": "Professionals aged 25-45",
    "key_features": ["Task management", "Team collaboration", "AI assistance"],
    "unique_value": "AI-powered task prioritization"
  },
  "current_metadata": {
    "title": "Current Title",
    "subtitle": "Current Subtitle",
    "description": "Current description..."
  },
  "target_keywords": ["productivity", "task manager", "todo"]
}
```

### 评论分析
```json
{
  "app_id": "com.myapp.app",
  "platform": "apple" | "google",
  "date_range": "last_30_days" | "last_90_days" | "all_time",
  "rating_filter": [1, 2, 3, 4, 5],
  "language": "en"
}
```

### ASO 评分计算
```json
{
  "metadata": {
    "title_quality": 0.8,
    "description_quality": 0.7,
    "keyword_density": 0.6
  },
  "ratings": {
    "average_rating": 4.5,
    "total_ratings": 15000
  },
  "conversion": {
    "impression_to_install": 0.05
  },
  "keyword_rankings": {
    "top_10": 5,
    "top_50": 12,
    "top_100": 18
  }
}
```

## 输出格式

### 关键词研究报告
- 推荐关键词列表及搜索量估算
- 竞争度分析（低/中/高）
- 每个关键词的相关性评分
- 主关键词与次关键词的策略建议
- 长尾关键词机会

### 优化元数据包
- 平台专属标题（含字符数验证）
- 副标题/推广文本（Apple）
- 简短描述（Google）
- 完整描述（双平台）
- 关键词字段（Apple - 100 字符）
- 所有字段的字符数验证
- 关键词密度分析
- 优化前后对比

### 竞品分析报告
- 分类中前 10 名竞品
- 竞品的元数据策略
- 关键词重叠分析
- 视觉素材评估
- 评分和评论量对比
- 已识别的差距和机会

### ASO 健康评分
- 总分（0-100）
- 分类细分：
  - 元数据质量（0-25）
  - 评分与评论（0-25）
  - 关键词表现（0-25）
  - 转化指标（0-25）
- 具体改进建议
- 优先行动项

### A/B 测试计划
- 假设和测试变量
- 测试时长建议
- 成功指标定义
- 样本量计算
- 统计显著性阈值

### 上线检查清单
- 提交前验证（所有必需素材、元数据）
- 商店合规性验证
- 测试检查清单（设备、操作系统版本）
- 营销准备事项
- 上线后监控计划

## 使用方法

### 关键词研究
```
Hey Claude—I just added the "app-store-optimization" skill. Can you research the best keywords for a productivity app targeting professionals? Focus on keywords with good search volume but lower competition.
```

### 优化 App Store 列表
```
Hey Claude—I just added the "app-store-optimization" skill. Can you optimize my app's metadata for the Apple App Store? Here's my current listing: [provide current metadata]. I want to rank for "task management" and "productivity tools".
```

### 分析竞品策略
```
Hey Claude—I just added the "app-store-optimization" skill. Can you analyze the ASO strategies of Todoist, Any.do, and Microsoft To Do? I want to understand what they're doing well and where there are opportunities.
```

### 评论情感分析
```
Hey Claude—I just added the "app-store-optimization" skill. Can you analyze recent reviews for my app (com.myapp.ios) and identify the most common user complaints and feature requests?
```

### 计算 ASO 评分
```
Hey Claude—I just added the "app-store-optimization" skill. Can you calculate my app's overall ASO health score and provide specific recommendations for improvement?
```

### 规划 A/B 测试
```
Hey Claude—I just added the "app-store-optimization" skill. I want to A/B test my app icon and first screenshot. Can you help me design the test and determine how long to run it?
```

### 上线前检查清单
```
Hey Claude—I just added the "app-store-optimization" skill. Can you generate a comprehensive pre-launch checklist for submitting my app to both Apple App Store and Google Play Store?
```

## 脚本

### keyword_analyzer.py
分析关键词的搜索量、竞争度和相关性。提供主关键词和次关键词的策略建议。

**核心函数：**
- `analyze_keyword()`：分析单个关键词指标
- `compare_keywords()`：比较多个关键词
- `find_long_tail()`：发现长尾关键词机会
- `calculate_keyword_difficulty()`：评估竞争程度

### metadata_optimizer.py
优化标题、描述和关键词字段，支持平台专属字符限制验证。

**核心函数：**
- `optimize_title()`：创建有吸引力且关键词丰富的标题
- `optimize_description()`：生成以转化为导向的描述
- `optimize_keyword_field()`：最大化 Apple 的 100 字符关键词字段
- `validate_character_limits()`：确保符合平台限制
- `calculate_keyword_density()`：分析元数据中的关键词使用情况

### competitor_analyzer.py
分析头部竞品的 ASO 策略并识别机会。

**核心函数：**
- `get_top_competitors()`：识别分类领导者
- `analyze_competitor_metadata()`：提取并分析竞品关键词
- `compare_visual_assets()`：评估图标和截图
- `identify_gaps()`：发现竞争机会

### aso_scorer.py
计算多维度综合 ASO 健康评分。

**核心函数：**
- `calculate_overall_score()`：计算 0-100 ASO 评分
- `score_metadata_quality()`：评估标题、描述、关键词
- `score_ratings_reviews()`：评估评分质量和数量
- `score_keyword_performance()`：分析排名位置
- `score_conversion_metrics()`：评估从曝光到安装的转化率
- `generate_recommendations()`：提供优先行动项

### ab_test_planner.py
规划和追踪元数据和视觉素材的 A/B 测试。

**核心函数：**
- `design_test()`：创建测试假设和变量
- `calculate_sample_size()`：确定所需测试时长
- `calculate_significance()`：评估统计显著性
- `track_results()`：监控测试表现
- `generate_report()`：总结测试结果

### localization_helper.py
管理多语言 ASO 优化策略。

**核心函数：**
- `identify_target_markets()`：推荐本地化优先级
- `translate_metadata()`：生成本地化元数据
- `adapt_keywords()`：研究特定地区的关键词
- `validate_translations()`：检查各语言的字符限制
- `calculate_localization_roi()`：估算本地化的影响

### review_analyzer.py
分析用户评论的情感、问题和功能需求。

**核心函数：**
- `analyze_sentiment()`：计算正面/负面/中性比例
- `extract_common_themes()`：识别高频话题
- `identify_issues()`：发现 Bug 和用户投诉
- `find_feature_requests()`：提取用户期望的功能
- `track_sentiment_trends()`：监控情感随时间的变化
- `generate_response_templates()`：创建评论回复草稿

### launch_checklist.py
生成全面的上线和更新检查清单。

**核心函数：**
- `generate_prelaunch_checklist()`：完整的提交验证
- `validate_app_store_compliance()`：检查 Apple 指南
- `validate_play_store_compliance()`：检查 Google 政策
- `create_update_plan()`：规划更新频率和功能
- `optimize_launch_timing()`：推荐发布日期
- `plan_seasonal_campaigns()`：识别季节性机会

## 最佳实践

### 关键词研究
1. **搜索量与竞争度**：平衡高搜索量关键词与可实现的排名
2. **相关性优先**：只定位与你应用真正相关的关键词
3. **长尾策略**：包含 3-4 个词的短语，竞争度更低
4. **持续研究**：关键词趋势会变化——每季度研究一次
5. **竞品关键词**：不要盲目复制；确保与你的功能相关

### 元数据优化
1. **关键词前置**：将最重要的关键词放在标题/描述的前面
2. **自然语言**：先为人写，再为搜索引擎写
3. **功能收益**：聚焦用户收益，而非仅列举功能
4. **A/B 测试一切**：系统性地测试标题、描述、截图
5. **定期更新**：每次重大更新时刷新元数据
6. **字符限制**：用满每个字符——不要浪费宝贵空间
7. **Apple 关键词字段**：不加复数、重复词或逗号间的空格

### 视觉素材
1. **图标**：必须在小尺寸（60x60px）下可识别
2. **截图**：前 2-3 张最关键——大多数用户不会滑动
3. **说明文字**：用截图说明文字讲述你的价值故事
4. **一致性**：视觉风格与应用设计匹配
5. **A/B 测试图标**：图标是最重要的视觉元素

### 评论与评分
1. **快速回复**：在 24-48 小时内回复评论
2. **专业语气**：即使面对负面评论也要礼貌
3. **解决问题**：展示你正在积极修复报告的问题
4. **感谢支持者**：认可正面评论
5. **策略性引导**：在正面体验后请求评分

### 上线策略
1. **软上线**：考虑先在较小市场上线
2. **PR 时机**：将媒体报道与上线协调
3. **频繁更新**：初期更新表明开发活跃
4. **密切监控**：前两周每天追踪指标
5. **快速迭代**：立即修复关键问题

### 本地化
1. **优先市场**：从英语、西班牙语、中文、法语、德语开始
2. **母语者**：使用专业翻译人员，而非机器翻译
3. **文化适配**：某些功能在不同文化中反响不同
4. **本地测试**：发布前让母语者审核
5. **衡量 ROI**：按地区追踪下载量以评估影响

## 限制

### 数据依赖
- 关键词搜索量估算为近似值（Apple/Google 无官方数据）
- 私有应用的竞品数据可能不完整
- 评论分析仅限于公开评论（无法访问私有反馈）
- 新应用可能没有历史数据

### 平台约束
- Apple App Store 关键词变更需要提交应用（推广文本除外）
- Google Play Store 元数据变更需要 1-2 小时才能被索引
- A/B 测试需要大量流量才能达到统计显著性
- 商店算法为专有算法，可能随时变更

### 行业差异
- ASO 基准因分类差异很大（游戏 vs 工具类）
- 季节性对不同分类的影响不同
- 不同地理市场有不同的竞争格局
- 文化偏好影响不同国家的效果

### 范围边界
- 不包含付费用户获取策略（Apple Search Ads、Google Ads）
- 不涵盖应用开发或 UI/UX 优化
- 不包含应用分析实现（使用 Firebase、Mixpanel 等）
- 不处理应用提交的技术问题（配置文件、证书）

### 何时不使用本技能
- 用于 Web 应用（适用不同的 SEO 策略）
- 用于不在公开商店的企业应用
- 用于仅处于 Beta/TestFlight 阶段的应用
- 如果你需要付费广告策略（改用营销技能）

## 与其他技能的集成

本技能与以下技能配合良好：
- **内容策略技能**：用于创建应用描述和营销文案
- **分析技能**：用于分析下载和参与数据
- **本地化技能**：用于管理多语言内容
- **设计技能**：用于创建优化的视觉素材
- **营销技能**：用于协调更广泛的上线活动

## 版本与更新

本技能基于截至 2025 年 11 月的 Apple App Store 和 Google Play Store 当前要求。商店政策和最佳实践会演变——在重大上线前请验证当前要求。

**需要关注的关键更新：**
- Apple App Store Connect 更新（apple.com/app-store/review/guidelines）
- Google Play Console 更新（play.google.com/console/about/guides/releasewithconfidence）
- iOS/Android 版本采用率（影响设备测试）
- 商店算法变更（关注 ASO 博客和社区）

## 何时使用
本技能适用于执行概述中描述的工作流或操作。
