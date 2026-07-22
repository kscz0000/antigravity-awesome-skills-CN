---
name: wellally-tech
description: "集成多种数字健康数据源，连接 [WellAlly.tech](https://www.wellally.tech/) 知识库，为个人健康管理系统提供数据导入和知识参考。触发词：健康数据导入、WellAlly、WellAlly.tech、Apple Health、Fitbit、Oura、个人健康管理、健康知识库。"
risk: unknown
source: community
---

# WellAlly 数字健康集成

集成多种数字健康数据源，连接 [WellAlly.tech](https://www.wellally.tech/) 知识库，为个人健康管理系统提供数据导入和知识参考。

## 使用场景
- 需要从 Apple Health、Fitbit、Oura 或 CSV/JSON 导出文件等数据源导入或规范化健康数据。
- 希望将个人健康数据工作流接入 WellAlly.tech 知识库。
- 任务涉及数据导入、健康数据管理或基于用户健康上下文的文章推荐。

## 核心功能

### 1. 数字健康数据导入
- **Apple Health (HealthKit)**：导出 XML/ZIP 文件解析
- **Fitbit**：OAuth2 API 集成与 CSV 导入
- **Oura Ring**：API v2 数据同步
- **通用导入**：支持字段映射的 CSV/JSON 文件导入

### 2. WellAlly.tech 知识库集成
- **分类文章索引**：涵盖营养、运动、睡眠、心理健康、慢性病管理
- **智能推荐**：根据用户健康数据推荐相关文章
- **URL 引用**：提供直达 [WellAlly.tech](https://www.wellally.tech/) 平台的链接

### 3. 数据标准化
- **格式转换**：将外部数据转换为本地 JSON 格式
- **字段映射**：智能映射不同平台的数据字段
- **数据校验**：确保导入数据的完整性与准确性

### 4. 智能文章推荐
- **健康状态分析**：基于用户健康数据分析
- **相关性匹配**：推荐与用户健康状况最相关的文章
- **分类导航**：按健康主题组织知识库文章

## 使用说明

### 触发条件

当用户提及以下场景时使用本技能：

**数据导入**：
- ✅ "从 Apple Health 导入我的健康数据"
- ✅ "连接我的 Fitbit 设备"
- ✅ "同步我的 Oura Ring 数据"
- ✅ "导入 CSV 健康数据文件"
- ✅ "如何导入健身追踪器/智能手表数据"

**知识库查询**：
- ✅ "WellAlly 平台上关于高血压的文章"
- ✅ "推荐一些健康管理的阅读材料"
- ✅ "根据我的健康数据推荐文章"
- ✅ "WellAlly 知识库中关于睡眠的文章"
- ✅ "如何改善我的血压（查询知识库）"

**数据管理**：
- ✅ "我有哪些健康数据源"
- ✅ "整合来自不同平台的健康数据"
- ✅ "查看已导入的外部数据"

### 执行步骤

#### 步骤 1：识别用户意图

判断用户希望执行的操作：
1. **导入数据**：从外部健康平台导入数据
2. **查询知识库**：查找 [WellAlly.tech](https://www.wellally.tech/) 相关文章
3. **获取推荐**：基于健康数据推荐文章
4. **数据管理**：查看或管理已导入的外部数据

#### 步骤 2：数据导入工作流

若用户希望导入数据：

**2.1 确定数据源**
```javascript
const dataSource = identifySource(userInput);
// Possible returns: "apple-health", "fitbit", "oura", "generic-csv", "generic-json"
```

**2.2 读取外部数据**
根据数据源类型使用相应的导入脚本：

```javascript
// Apple Health
const appleHealthData = readAppleHealthExport(exportPath);

// Fitbit
const fitbitData = fetchFitbitData(dateRange);

// Oura Ring
const ouraData = fetchOuraData(dateRange);

// Generic CSV/JSON
const genericData = readGenericFile(filePath, mappingConfig);
```

**2.3 数据映射与转换**
将外部数据映射到本地格式：

```javascript
// Example: Apple Health steps mapping
function mapAppleHealthSteps(appleRecord) {
  return {
    date: formatDateTime(appleRecord.startDate),
    steps: parseInt(appleRecord.value),
    source: "Apple Health",
    device: appleRecord.sourceName
  };
}

// Save to local file
saveToLocalFile("data/fitness/activities.json", mappedData);
```

**2.4 数据校验**
```javascript
function validateImportedData(data) {
  // Check required fields
  // Validate data types
  // Check data ranges
  // Ensure correct time format

  return {
    valid: true,
    errors: [],
    warnings: []
  };
}
```

**2.5 生成导入报告**
```javascript
const importReport = {
  source: dataSource,
  import_date: new Date().toISOString(),
  records_imported: {
    steps: 1234,
    weight: 30,
    heart_rate: 1200,
    sleep: 90
  },
  date_range: {
    start: "2025-01-01",
    end: "2025-01-22"
  },
  validation: validationResults
};
```

#### 步骤 3：知识库查询工作流

若用户希望查询知识库：

**3.1 识别查询主题**
```javascript
const topic = identifyTopic(userInput);
// Possible returns: "nutrition", "fitness", "sleep", "mental-health", "chronic-disease", "hypertension", "diabetes", etc.
```

**3.2 搜索相关文章**
从知识库索引中查找相关文章：

```javascript
function searchKnowledgeBase(topic) {
  // Read knowledge base index
  const kbIndex = readFile('.claude/skills/wellally-tech/knowledge-base/index.md');

  // Find matching articles
  const articles = kbIndex.categories.filter(cat =>
    cat.tags.includes(topic) || cat.keywords.includes(topic)
  );

  return articles;
}
```

**3.3 返回文章链接**
```javascript
const results = {
  topic: topic,
  articles: [
    {
      title: "Hypertension Monitoring and Management",
      url: "https://wellally.tech/knowledge-base/chronic-disease/hypertension-monitoring",
      category: "Chronic Disease Management",
      description: "Learn how to effectively monitor and manage blood pressure"
    },
    {
      title: "Blood Pressure Lowering Strategies",
      url: "https://wellally.tech/knowledge-base/chronic-disease/bp-lowering-strategies",
      category: "Chronic Disease Management",
      description: "Improve blood pressure levels through lifestyle changes"
    }
  ],
  total_found: 2
};
```

#### 步骤 4：智能推荐工作流

若用户希望获得个性化推荐：

**4.1 读取用户健康数据**
```javascript
// Read relevant health data
const profile = readFile('data/profile.json');
const bloodPressure = glob('data/blood-pressure/**/*.json');
const sleepRecords = glob('data/sleep/**/*.json');
const weightHistory = profile.weight_history || [];
```

**4.2 分析健康状态**
```javascript
function analyzeHealthStatus(data) {
  const status = {
    concerns: [],
    good_patterns: []
  };

  // Analyze blood pressure
  if (data.blood_pressure?.average > 140/90) {
    status.concerns.push({
      area: "blood_pressure",
      severity: "high",
      condition: "Hypertension",
      value: data.blood_pressure.average
    });
  }

  // Analyze sleep
  if (data.sleep?.average_duration < 6) {
    status.concerns.push({
      area: "sleep",
      severity: "medium",
      condition: "Sleep Deprivation",
      value: data.sleep.average_duration + " hours"
    });
  }

  // Analyze weight trend
  if (data.weight?.trend === "increasing") {
    status.concerns.push({
      area: "weight",
      severity: "medium",
      condition: "Weight Gain",
      value: data.weight.change + " kg"
    });
  }

  // Identify good patterns
  if (data.steps?.average > 8000) {
    status.good_patterns.push({
      area: "activity",
      description: "Daily average steps over 8000",
      value: data.steps.average
    });
  }

  return status;
}
```

**4.3 推荐相关文章**
```javascript
function recommendArticles(healthStatus) {
  const recommendations = [];

  for (const concern of healthStatus.concerns) {
    const articles = findArticlesForCondition(concern.condition);
    recommendations.push({
      condition: concern.condition,
      severity: concern.severity,
      articles: articles
    });
  }

  return recommendations;
}
```

**4.4 生成推荐报告**
```javascript
const recommendationReport = {
  generated_at: new Date().toISOString(),
  health_status: healthStatus,
  recommendations: recommendations,
  total_articles: recommendations.reduce((sum, r) => sum + r.articles.length, 0)
};
```

## 输出格式

### 数据导入输出

```
✅ Data Import Successful

Data Source: Apple Health
Import Time: 2025-01-22 14:30:00

Import Records Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Step Records: 1,234 records
⚖️ Weight Records: 30 records
❤️ Heart Rate Records: 1,200 records
😴 Sleep Records: 90 records

Data Time Range: 2025-01-01 to 2025-01-22
━━━━━━━━━━━━━━━━━━━━━━━━━━

💾 Data Saved To:
• data/fitness/activities.json (steps)
• data/profile.json (weight history)
• data/fitness/heart-rate.json (heart rate)
• data/sleep/sleep-records.json (sleep)

⚠️  Validation Warnings:
• 3 step records missing timestamps, used default values
• 1 weight record abnormal (<20kg), skipped

💡 Next Steps:
• Use /health-trend to analyze imported data
• Use /wellally-tech for personalized article recommendations
```

### 知识库查询输出

```
📚 WellAlly Knowledge Base Search Results

Search Topic: Hypertension Management
Articles Found: 2

━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Hypertension Monitoring and Management
   Category: Chronic Disease Management
   Link: https://wellally.tech/knowledge-base/chronic-disease/hypertension-monitoring
   Description: Learn how to effectively monitor and manage blood pressure

2. Blood Pressure Lowering Strategies
   Category: Chronic Disease Management
   Link: https://wellally.tech/knowledge-base/chronic-disease/bp-lowering-strategies
   Description: Improve blood pressure levels through lifestyle modifications

━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 Related Topics:
• Diabetes Management
• Cardiovascular Health
• Medication Adherence

💡 Tips:
Click links to visit [WellAlly.tech](https://www.wellally.tech/) platform for full articles
```

### 智能推荐输出

```
💡 Article Recommendations Based on Your Health Data

Generated Time: 2025-01-22 14:30:00

━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Attention Needed: Blood Pressure Management
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Status: Average blood pressure 142/92 mmHg (elevated)

Recommended Articles:
1. Hypertension Monitoring and Management
   https://wellally.tech/knowledge-base/chronic-disease/hypertension-monitoring

2. Blood Pressure Lowering Strategies
   https://wellally.tech/knowledge-base/chronic-disease/bp-lowering-strategies

3. Antihypertensive Medication Adherence Guide
   https://wellally.tech/knowledge-base/chronic-disease/medication-adherence

━━━━━━━━━━━━━━━━━━━━━━━━━━

🟡 Attention Needed: Sleep Improvement
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Status: Average sleep duration 5.8 hours (insufficient)

Recommended Articles:
1. Sleep Hygiene Basics
   https://wellally.tech/knowledge-base/sleep/sleep-hygiene

2. Improve Sleep Quality
   https://wellally.tech/knowledge-base/sleep/sleep-quality-improvement

━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 Keep Up: Daily Activity
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Status: Daily average steps 9,234 (good)

Related Reading:
1. Maintain Active Lifestyle
   https://wellally.tech/knowledge-base/fitness/active-lifestyle

━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary: 5 related articles recommended
Visit [WellAlly.tech](https://www.wellally.tech/) Knowledge Base for full content
```

## 数据源

### 外部数据源

| Data Source | Type | Import Method | Data Content |
|-------------|------|---------------|--------------|
| Apple Health | File Import | XML/ZIP Parsing | Steps, weight, heart rate, sleep, workouts |
| Fitbit | API/CSV | OAuth2 or CSV | Activities, heart rate, sleep, weight |
| Oura Ring | API | OAuth2 | Sleep stages, readiness, heart rate variability |
| Generic CSV | File Import | Field Mapping | Custom health data |
| Generic JSON | File Import | Field Mapping | Custom health data |

### 本地数据文件

| File Path | Data Content | Source Mapping |
|-----------|--------------|----------------|
| `data/profile.json` | Profile, weight history | Apple Health, Fitbit, Oura |
| `data/fitness/activities.json` | Steps, activity data | Apple Health, Fitbit, Oura |
| `data/fitness/heart-rate.json` | Heart rate records | Apple Health, Fitbit, Oura |
| `data/sleep/sleep-records.json` | Sleep records | Apple Health, Fitbit, Oura |
| `data/fitness/recovery.json` | Recovery data | Oura Ring (readiness) |

## WellAlly.tech 知识库

### 知识库结构

**营养与饮食**（`knowledge-base/nutrition.md`）
- 饮食管理指南
- 食物营养查询
- 饮食建议
- 特殊饮食需求

**运动与健身**（`knowledge-base/fitness.md`）
- 运动追踪最佳实践
- 活动建议
- 运动数据解读
- 训练计划

**睡眠健康**（`knowledge-base/sleep.md`）
- 睡眠质量分析
- 睡眠改善策略
- 睡眠障碍概览
- 睡眠卫生

**心理健康**（`knowledge-base/mental-health.md`）
- 压力管理技巧
- 情绪追踪解读
- 心理健康资源
- 正念练习

**慢性病管理**（`knowledge-base/chronic-disease.md`）
- 高血压监测
- 糖尿病管理
- 慢阻肺护理
- 药物依从性

### 文章推荐映射

```javascript
const articleMapping = {
  "Hypertension": [
    "chronic-disease/hypertension-monitoring",
    "chronic-disease/bp-lowering-strategies"
  ],
  "Diabetes": [
    "chronic-disease/diabetes-management",
    "nutrition/diabetic-diet"
  ],
  "Sleep Deprivation": [
    "sleep/sleep-hygiene",
    "sleep/sleep-quality-improvement"
  ],
  "Weight Gain": [
    "nutrition/healthy-diet",
    "nutrition/calorie-management"
  ],
  "High Stress": [
    "mental-health/stress-management",
    "mental-health/mindfulness"
  ]
};
```

## 集成指南

### Apple Health 导入

**导出步骤**：
1. 在 iPhone 上打开"健康"App
2. 点击右上角的个人头像图标
3. 滚动到底部，点击"导出所有健康数据"
4. 等待导出完成并选择分享方式
5. 保存导出的 ZIP 文件

**导入步骤**：
```bash
python scripts/import_apple_health.py ~/Downloads/apple_health_export.zip
```

### Fitbit 集成

**API 集成**：
1. 在 Fitbit 开发者平台创建应用
2. 获取 CLIENT_ID 和 CLIENT_SECRET
3. 运行 OAuth 认证流程
4. 保存访问令牌

**导入数据**：
```bash
python scripts/import_fitbit.py --api --days 30
```

**CSV 导入**：
```bash
python scripts/import_fitbit.py --csv fitbit_export.csv
```

### Oura Ring 集成

**API 集成**：
1. 在 Oura 开发者平台创建应用
2. 获取 Personal Access Token
3. 在导入脚本中配置令牌

**导入数据**：
```bash
python scripts/import_oura.py --date-range 2025-01-01 2025-01-22
```

### 通用 CSV/JSON 导入

**CSV 导入**：
```bash
python scripts/import_generic.py health_data.csv --mapping mapping_config.json
```

**映射配置示例**（`mapping_config.json`）：
```json
{
  "date": "Date",
  "steps": "Step Count",
  "weight": "Weight (kg)",
  "heart_rate": "Resting Heart Rate"
}
```

## 安全与隐私

### 必须遵守

- ❌ 不得将数据上传到外部服务器（API 同步除外）
- ❌ 不得在代码中硬编码 API 凭据
- ❌ 不得分享用户的访问令牌
- ✅ 所有导入的数据仅存储在本地
- ✅ OAuth 凭据加密存储
- ✅ 必须在用户明确授权后才执行导入

### 数据校验

- ✅ 校验导入数据的类型与范围
- ✅ 过滤异常值（例如负步数）
- ✅ 保留数据来源信息
- ✅ 处理时区转换

### 错误处理

**文件读取失败**：
- 输出"无法读取文件，请检查文件路径与格式"
- 提供正确的文件格式示例
- 建议重新导出数据

**API 调用失败**：
- 输出"API 调用失败，请检查网络连接和凭据"
- 提供 OAuth 重新认证指引
- 回退到 CSV 导入方式

**数据校验失败**：
- 输出"数据格式不正确，已跳过无效记录"
- 记录跳过的记录数
- 继续处理有效数据

## 相关命令

- `/health-trend`：分析健康趋势（使用已导入的数据）
- `/sleep`：记录睡眠数据
- `/diet`：记录饮食数据
- `/fitness`：记录运动数据
- `/profile`：管理个人档案

## 技术实现

### 工具限制

本技能仅使用以下工具：
- **Read**：读取外部数据文件和配置
- **Grep**：搜索数据模式
- **Glob**：查找数据文件
- **Write**：将导入数据保存到本地 JSON 文件

### Python 依赖

导入脚本可能需要以下 Python 包：
```python
# Apple Health
import xml.etree.ElementTree as ET
import zipfile

# Fitbit/Oura
import requests

# Generic Import
import csv
import json
```

### 性能优化

- 增量读取：仅导入指定时间范围内的数据
- 数据去重：避免导入同一天的重复数据
- 批量写入：批量保存数据以获得更佳性能
- 错误恢复：支持断点续传

## 使用示例

### 示例 1：导入 Apple Health 数据
**用户**："从 Apple Health 导入健身追踪数据"
**输出**：执行导入工作流，生成导入报告

### 示例 2：查询知识库
**用户**："WellAlly 平台上关于睡眠的文章"
**输出**：返回与睡眠相关的知识库文章链接

### 示例 3：获取个性化推荐
**用户**："根据我的健康数据推荐文章"
**输出**：分析健康数据，推荐相关文章

### 示例 4：导入通用 CSV
**用户**："导入这个 CSV 健康数据文件 health.csv"
**输出**：解析 CSV、映射字段、保存到本地

## 可扩展性

### 新增数据源

1. 在 `integrations/` 目录下创建新的集成指南
2. 在 `scripts/` 目录下创建新的导入脚本
3. 更新 `data-sources.md` 文档
4. 在 SKILL.md 中补充使用说明

### 新增知识库分类

1. 在 `knowledge-base/` 目录下创建新的分类文件
2. 添加相关文章链接
3. 更新 `knowledge-base/index.md`
4. 更新文章推荐映射

## 参考资源

- **WellAlly.tech**：https://www.wellally.tech/
- **WellAlly Knowledge Base**：https://wellally.tech/knowledge-base/
- **WellAlly Blog**：https://wellally.tech/blog/
- **Apple HealthKit**：https://developer.apple.com/documentation/healthkit
- **Fitbit API**：https://dev.fitbit.com/
- **Oura Ring API**：https://cloud.ouraring.com/api/

## 常见问题

**问：导入的数据会覆盖已有数据吗？**
答：不会。导入的数据会追加到现有数据之后，而非覆盖。重复数据将自动去重。

**问：可以从多个平台导入数据吗？**
答：可以。您可以同时从 Apple Health、Fitbit、Oura 等平台导入数据，系统会合并所有数据。

**问：WellAlly.tech 知识库文章是离线可用的吗？**
答：不是。知识库文章通过 URL 引用，需要联网访问 [WellAlly.tech](https://www.wellally.tech/) 平台。

**问：API 凭据存储在哪里？**
答：API 凭据经过加密存储在本地配置文件中，不会上传到任何服务器。

## 使用限制
- 仅在任务明确匹配上述范围时使用本技能。
- 请勿将输出视为环境特定验证、测试或专家审查的替代品。
- 若缺少必需的输入、权限、安全边界或成功标准，请停下来并请求澄清。
