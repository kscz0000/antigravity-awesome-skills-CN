---
name: developer-sandbox
description: '设计与构建交互式 Playground，让开发者在无需承诺的前提下体验你的产品。本技能涵盖 Playground 架构、预置示例、嵌入策略、门控决策，以及将 Playground 用户转化为注册用户。触发词："开发者 Playground"、"开发者沙盒"、"交互式试用"、"开发者演示"、"API 试用"、"Playground 转化"、"开发者体验"'
risk: unknown
source: https://github.com/jonathimer/devmarketing-skills/tree/main/skills/developer-sandbox
source_repo: jonathimer/devmarketing-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/jonathimer/devmarketing-skills/blob/main/LICENSE
---

# 交互式 Playground 与演示环境
## 何时使用

当你需要设计与构建交互式 Playground，让开发者在无需承诺的前提下体验你的产品时，请使用本技能。本技能涵盖 Playground 架构、预置示例、嵌入策略、门控决策，以及将 Playground 用户转化为注册用户。触发词："开发者 Playground"、"开发者沙盒"、"交互式试用"、"开发者演示"、"API 试用"、"Playground 转化"、"开发者体验"


让开发者在做出承诺之前先体验你的产品。一个出色的 Playground 能消除采用过程中的最大障碍：开发者不确定你的产品是否能解决他们的问题。

## 概述

开发者 Playground 承担多重用途：
- **评估**：让开发者在投入搭建时间之前先行测试
- **学习**：用于理解概念的交互式环境
- **营销**：无需销售电话即可展示能力
- **支持**：用于调试问题的可复现环境

本技能介绍如何设计能将好奇访客转化为活跃用户的 Playground。

## 开始之前

请先阅读 **developer-audience-context** 技能，了解以下问题：
- 开发者在注册前希望验证什么？
- 你的领域中典型的评估流程是怎样的？
- 竞品提供了哪些 Playground？
- 展示产品价值的最小可行体验是什么？

你的 Playground 应当回答开发者在评估时产生的疑问。

## Playground 设计原则

### 原则 1：即时满足

开发者落地后，应在 10 秒内看到有意义的内容。

**好的做法**：页面加载时已经运行着一个可用的示例
**不好的做法**：空白的编辑器只显示"在此输入代码"占位符

```html
<!-- 好：预加载的运行中示例 -->
<div class="playground">
  <div class="editor">
    <pre><code>// 分析这段文本的情感
const result = await api.analyze("I love this product!");
console.log(result.sentiment); // "positive"</code></pre>
  </div>
  <div class="output">
    <pre>{ "sentiment": "positive", "confidence": 0.94 }</pre>
  </div>
  <button class="run-btn">Run ▶️</button>
</div>
```

### 原则 2：渐进式复杂度

从简单入手，让开发者随着好奇心加深逐步深入。

**Level 1：一键演示**
```
[分析文本] → 立即看到结果
```

**Level 2：可编辑输入**
```
[编辑文本] → [运行] → 查看结果
```

**Level 3：完整 API 访问**
```
编辑代码 → 修改参数 → 查看原始请求/响应
```

**Level 4：完整 Playground**
```
多文件处理 → 导入 SDK → 构建迷你应用
```

### 原则 3：真实 API，真实结果

永远不要伪造结果。使用真实 API 配合沙盒凭证。

**为什么真实很重要：**
- 建立信任（不是 demo，而是真正的产品）
- 展示真实的性能特征
- 演示真实的错误处理
- 注册后不会有意外

### 原则 4：零摩擦

基础 Playground 无需注册、无需安装、无需配置。

```
❌ 不好的做法："注册后才能试用 Playground"
❌ 不好的做法："先安装我们的 CLI 才能继续"
❌ 不好的做法："请配置你的环境……"

✅ 好的做法：在浏览器中立即可用
```

## 预置示例

### 示例选择策略

所选示例应满足：
1. **30 秒内展示核心价值**
2. **解决开发者的真实问题**
3. **展示与竞品的差异点**
4. **复杂度由浅入深逐步展开**

### 示例分类

**"Hello World" 示例**
- API 最简单的使用方式
- 应当零修改即可运行
- 证明系统是正常工作的

```javascript
// 示例：文本分析 API
const result = await api.analyze("Hello, world!");
// 输出：{ words: 2, characters: 13 }
```

**"顿悟时刻" 示例**
- 展示产品的独特能力
- 引发"哇，原来这么简单"的反应
- 这是最重要的示例

```javascript
// 示例：展示 AI 做出令人惊艳的事情
const result = await api.summarize(longArticle);
// 输出：一段完美的 3 句话摘要
```

**"真实用例" 示例**
- 开发者实际遇到的场景
- 展示如何解决具体问题
- 针对不同用例提供多个示例

```javascript
// 示例 1：电商 - 分析商品评论
// 示例 2：客服 - 对工单进行分类
// 示例 3：社交 - 检测垃圾评论
```

**"集成" 示例**
- 展示产品与流行工具的协作
- 回应"它能和我的技术栈配合吗？"的疑虑

```javascript
// 示例：与 Express.js 集成
app.post('/analyze', async (req, res) => {
  const result = await api.analyze(req.body.text);
  res.json(result);
});
```

### 示例质量清单

- [ ] 示例无需修改即可运行
- [ ] 输出有趣或令人印象深刻
- [ ] 代码遵循语言最佳实践
- [ ] 注释解释清楚发生了什么
- [ ] 真实场景一目了然
- [ ] 自然引发"它还能做什么？"的好奇心

## 分享与嵌入

### 可分享的 Playground URL

让开发者可以分享他们的 Playground 状态：

```
https://playground.example.com/?code=BASE64_ENCODED_CODE
https://playground.example.com/share/abc123 (stored state)
```

**使用场景：**
- 与团队成员共享代码
- 在 Stack Overflow 回答中链接
- 附上可复现的 Bug 报告
- 博客文章中的代码片段

### 可嵌入的 Playground

让开发者能在自己的内容中嵌入 Playground：

```html
<!-- 嵌入到文档中 -->
<iframe
  src="https://playground.example.com/embed/quickstart"
  width="100%"
  height="400px"
></iframe>

<!-- 或者通过 script 标签 -->
<div class="example-playground" data-example="quickstart"></div>
<script src="https://playground.example.com/embed.js"></script>
```

### 嵌入考虑事项

**体积与性能：**
- 轻量级的嵌入脚本（< 50KB）
- 延迟加载 Playground，直到可见时才加载
- 自适应宽度，高度可配置

**定制化：**
- 主题选项（浅色/深色，匹配宿主站点）
- 显示/隐藏特定的 UI 元素
- 只读与可编辑模式

**归属：**
- 含蓄的品牌展示，带有回链
- "由 [产品] 提供支持"页脚
- "在完整 Playground 中编辑"链接

## 门控与非门控

### 保持非门控的场景

**非门控**（无需注册）的场景：
- 开发者正在评估是否采用
- 示例能展示产品的核心价值
- 可以用速率限制防止滥用
- 目标是漏斗顶端的曝光

### 应当门控的场景

**门控**（要求注册）的场景：
- 使用生产环境的 API 资源
- 访问个人/已保存的 Playground
- 需要账户的高级功能
- 为外部使用生成 API 密钥

### 渐进式门控策略

```
┌─────────────────────────────────────────────────────────┐
│ 非门控                                                  │
│ • 运行预置示例                                          │
│ • 编辑并重新运行示例                                    │
│ • 分享 Playground URL                                   │
├─────────────────────────────────────────────────────────┤
│ 免费注册                                                │
│ • 保存 Playground                                       │
│ • 获取外部使用的 API 密钥                              │
│ • 访问更多示例                                          │
│ • 更高的速率限制                                        │
├─────────────────────────────────────────────────────────┤
│ 付费                                                    │
│ • 生产环境 API 访问                                     │
│ • 团队功能                                              │
│ • 高级模型/功能                                         │
└─────────────────────────────────────────────────────────┘
```

### 门控体验设计

当你确实需要门控时，请尽量减少摩擦：

```html
<!-- 好：非阻塞式门控 -->
<div class="save-prompt">
  <p>想保存这个 Playground 吗？</p>
  <button onclick="signup()">创建免费账户</button>
  <button onclick="dismiss()">继续但不保存</button>
</div>

<!-- 不好：阻塞式门控 -->
<div class="modal">
  <p>注册后才能继续使用 Playground</p>
  <form><!-- required fields --></form>
</div>
```

## 从 Playground 到注册转化

### 转化漏斗

```
Playground 访问
      ↓
运行第一个示例（首次交互时间）
      ↓
修改示例（参与度）
      ↓
探索更多示例（兴趣）
      ↓
遇到限制（触发点）
      ↓
注册（转化）
```

### 设计转化触发器

能促进注册的**自然限制**：

```javascript
// 速率限制提示
"今天的免费 Playground 请求已用完 10/10。
 注册即可获得每月 1,000 次免费请求。"

// 功能引导
"本示例使用我们的 Pro 模型。
 注册后可免费试用。"

// 保存提示
"你的 Playground 会话将在 30 分钟后过期。
 创建账户以保存你的工作。"
```

**避免人为制造的摩擦：**
```javascript
// 不好：武断的拦截
"注册后才能运行超过 3 个示例"

// 不好：本应免费的功能
"注册后才能查看请求/响应详情"
```

### 转化最佳实践

**清晰的价值主张：**
```
┌─────────────────────────────────────────┐
│ 创建免费账户                            │
│                                         │
│ ✓ 获得你自己的 API 密钥                │
│ ✓ 保存与分享 Playground                │
│ ✓ 每月 1,000 次免费 API 调用          │
│                                         │
│ [使用 GitHub 注册]                     │
│ [使用 Google 注册]                     │
│ [使用邮箱注册]                          │
└─────────────────────────────────────────┘
```

**保留上下文：**
- 注册完成后，回到相同的 Playground 状态
- 在其代码中预填 API 密钥
- 展示与刚才操作相关的"下一步"

**度量漏斗：**
```javascript
analytics.track('playground_visit');
analytics.track('playground_first_run');
analytics.track('playground_code_edit');
analytics.track('playground_signup_prompt_shown');
analytics.track('playground_signup_started');
analytics.track('playground_signup_completed');
```

## Playground 架构

### 客户端 Playground

**适用场景：**
- JavaScript/TypeScript SDK
- 基于浏览器的 API
- 对延迟敏感的场景

**架构：**
```
┌──────────────────────────────────────────┐
│ 浏览器                                    │
│  ┌─────────────┐    ┌────────────────┐  │
│  │ Monaco      │    │ Preview/Output │  │
│  │ Editor      │ →  │ Iframe         │  │
│  └─────────────┘    └────────────────┘  │
│         ↓                    ↓           │
│  打包器 (esbuild-wasm) → 执行            │
│                              ↓           │
│                        你的 API          │
└──────────────────────────────────────────┘
```

### 服务端 Playground

**适用场景：**
- Python、Go、Ruby 等
- 隔离要求严格的场景
- 复杂依赖场景

**架构：**
```
┌────────────────────────────────────────────────┐
│ 浏览器                                         │
│  ┌─────────────┐    ┌────────────────────┐   │
│  │ Editor      │    │ Output             │   │
│  └─────────────┘    └────────────────────┘   │
│         ↓                    ↑                 │
└─────────│────────────────────│─────────────────┘
          │                    │
          ↓                    │
   ┌──────────────────────────────────────┐
   │ Backend                              │
   │  ┌────────────┐    ┌─────────────┐  │
   │  │ Code       │ →  │ Sandbox     │  │
   │  │ Receiver   │    │ Container   │  │
   │  └────────────┘    └─────────────┘  │
   └──────────────────────────────────────┘
```

### 安全考虑

**沙盒隔离：**
- 在容器中执行用户代码
- 限制 CPU、内存、网络
- 不能访问宿主文件系统
- 终止失控的进程

**API 保护：**
- 按 IP/会话进行速率限制
- 仅限沙盒使用的 API 凭证
- 监控滥用模式

**内容安全：**
- 扫描生成的内容
- 拦截恶意输出
- 记录审计日志

## Playground UX 组件

### 必备的 UI 元素

```
┌─────────────────────────────────────────────────────────────┐
│ [Examples ▼] [Docs] [Share] [Sign Up]                       │
├───────────────────────────────┬─────────────────────────────┤
│                               │                             │
│  // 在此编写你的代码          │  Output                     │
│  const result = await         │  {                         │
│    api.analyze("Hello");      │    "sentiment": "neutral"  │
│                               │  }                         │
│                               │                             │
│                               │                             │
├───────────────────────────────┴─────────────────────────────┤
│ [▶ Run]  [Reset]  [Copy Code]  [Copy as cURL]              │
└─────────────────────────────────────────────────────────────┘
```

### 编辑器功能

- 语法高亮
- SDK 方法的自动补全
- 错误高亮
- 行号
- 多文件支持（高级）

### 输出功能

- 格式化 JSON
- 可折叠的嵌套对象
- 复制输出按钮
- 请求/响应切换
- 时延信息

## 工具

### 代码编辑器
- **Monaco Editor**：VS Code 的编辑器（功能丰富）
- **CodeMirror**：轻量、可扩展
- **Ace Editor**：老牌稳定、久经考验

### 沙盒方案
- **Firecracker**：轻量级虚拟机
- **gVisor**：容器沙盒
- **WebContainers**：浏览器中的 Node.js

### Playground 平台
- **CodeSandbox**：完整的开发环境
- **StackBlitz**：基于 WebContainer
- **Replit**：多语言支持
- **Custom**：自建以获得完全控制权

### 嵌入方式
- **iframes**：简单但受限
- **Web Components**：隔离性更好
- **Script embeds**：最灵活

## 相关技能

- **api-onboarding**：将 Playground 作为入职工具
- **docs-as-marketing**：文档中的交互式示例
- **sdk-dx**：可在 Playground 上下文中使用的 SDK 设计
- **developer-metrics**：度量 Playground 效果
- **developer-audience-context**：理解应当演示什么

## 使用限制

- 仅在任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用变更前，请验证命令、生成的代码、依赖、凭证以及外部服务行为。
- 不要将示例视为环境特定测试、安全审查或用户对破坏性/高成本操作的批准的替代。