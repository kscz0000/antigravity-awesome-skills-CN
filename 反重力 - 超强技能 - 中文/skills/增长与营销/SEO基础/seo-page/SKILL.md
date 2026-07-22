---
name: seo-page
description: >
  深度单页SEO分析，涵盖页面元素、内容质量、技术元标签、结构化数据、图片和性能。
  当用户说"分析这个页面"、"检查页面SEO"、"单页SEO审查"、"页面SEO诊断"、
  "SEO页面分析"、"检查SEO"、"页面优化检查"，或提供单个URL进行审查时使用。
risk: safe
source: "https://github.com/AgriciDaniel/claude-seo"
date_added: "2026-03-21"
user-invokable: true
argument-hint: "[url]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# 单页分析

## 何时使用
- 当用户提供单个URL需要进行详细页面SEO审查时使用。
- 当审查单个页面而非整站时使用。
- 当需要同时检查元数据、内容、结构化数据、图片和页面级技术信号时使用。

## 分析内容

### 页面SEO
- Title标签：50-60字符，包含主关键词，唯一
- Meta描述：150-160字符，有吸引力，包含关键词
- H1：仅一个，匹配页面意图，包含关键词
- H2-H6：逻辑层级（无跳级），描述性强
- URL：简短、描述性强、连字符分隔、无参数
- 内部链接：充足，相关锚文本，无孤立页面
- 外部链接：指向权威来源，数量合理

### 内容质量
- 字数与页面类型最低要求对比（见 quality-gates.md）
- 可读性：Flesch Reading Ease分数、年级水平
- 关键词密度：自然（1-3%），存在语义变体
- E-E-A-T信号：作者简介、资质、一手经验标记
- 内容新鲜度：发布日期、最后更新日期

### 技术元素
- Canonical标签：存在，自引用或正确指向
- Meta robots：index/follow，除非有意屏蔽
- Open Graph：og:title、og:description、og:image、og:url
- Twitter Card：twitter:card、twitter:title、twitter:description
- Hreflang：如为多语言，实现是否正确

### 结构化数据
- 检测所有类型（优先JSON-LD）
- 验证必需属性
- 识别缺失的机会
- 永远不要推荐HowTo（已弃用）或FAQ（仅限政府/健康类网站）

### 图片
- Alt文本：存在、描述性强、自然包含关键词
- 文件大小：>200KB标记警告，>500KB标记严重
- 格式：推荐WebP/AVIF而非JPEG/PNG
- 尺寸：设置width/height以防止CLS
- 懒加载：首屏以下图片使用loading="lazy"

### Core Web Vitals（仅供参考，无法仅从HTML测量）
- 标记潜在LCP问题（巨型首屏图片、渲染阻塞资源）
- 标记潜在INP问题（重型JS、缺少async/defer）
- 标记潜在CLS问题（缺少图片尺寸、注入的内容）

## 输出

### 页面评分卡
```
Overall Score: XX/100

On-Page SEO:     XX/100  ████████░░
Content Quality: XX/100  ██████████
Technical:       XX/100  ███████░░░
Schema:          XX/100  █████░░░░░
Images:          XX/100  ████████░░
```

### 发现的问题
按优先级排列：严重 → 高 → 中 → 低

### 建议
具体、可操作的改进措施及预期影响

### 结构化数据建议
针对检测到的机会提供可直接使用的JSON-LD代码

## DataForSEO集成（可选）

如果DataForSEO MCP工具可用，使用`serp_organic_live_advanced`获取真实SERP排名，使用`backlinks_summary`获取反向链接数据和垃圾评分。

## 错误处理

| 场景 | 操作 |
|------|------|
| URL不可达（DNS失败、连接被拒） | 清晰报告错误，不猜测页面内容。建议用户验证URL后重试。 |
| 页面需要认证（401/403） | 报告页面在认证之后。建议用户提供渲染后的HTML或公开可访问的URL。 |
| JavaScript渲染内容（HTML中body为空） | 注明关键内容可能在客户端渲染。分析可用HTML并标记结果可能不完整。建议使用浏览器渲染快照（如有）。 |

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，停止并请求澄清。
