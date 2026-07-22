---
name: burpsuite-project-parser
description: 从命令行搜索和浏览 Burp Suite 项目文件（.burp）。当用户要求使用正则模式搜索响应头或响应体、提取安全审计发现、导出代理历史或站点地图数据、或分析 Burp 项目中捕获的 HTTP 流量时使用。
allowed-tools:
  - Bash
  - Read
risk: unknown
source: community
---

# Burp Project Parser

使用 burpsuite-project-file-parser 扩展从 Burp Suite 项目文件中搜索和提取数据。

## 何时使用
- 使用正则模式搜索响应头或响应体
- 从 Burp 项目中提取安全审计发现
- 导出代理历史或站点地图数据
- 分析 Burp 项目文件中捕获的 HTTP 流量

## 前置条件

本技能**将解析工作委托给 Burp Suite Professional** — 不直接解析 .burp 文件。

**必需：**
1. **Burp Suite Professional** — 必须已安装 ([portswigger.net](https://portswigger.net/burp/pro))
2. **burpsuite-project-file-parser 扩展** — 提供 CLI 功能

**安装扩展：**
1. 从 [github.com/BuffaloWill/burpsuite-project-file-parser](https://github.com/BuffaloWill/burpsuite-project-file-parser) 下载
2. 在 Burp Suite 中：Extender → Extensions → Add
3. 选择下载的 JAR 文件

## 快速参考

使用包装脚本：
```bash
{baseDir}/scripts/burp-search.sh /path/to/project.burp [FLAGS]
```

该脚本使用环境变量实现平台兼容性：
- `BURP_JAVA`：Java 可执行文件路径
- `BURP_JAR`：burpsuite_pro.jar 路径

设置说明请参阅[平台配置](#platform-configuration)。

## 子组件过滤器（务必使用）

**务必使用子组件过滤器，而非完整导出。** 完整的 `proxyHistory` 或 `siteMap` 可能返回数 GB 数据。子组件过滤器仅返回所需内容。

### 可用过滤器

| 过滤器 | 返回内容 | 典型大小 |
|--------|---------|---------|
| `proxyHistory.request.headers` | 仅请求行 + 请求头 | 小（< 1KB/条） |
| `proxyHistory.request.body` | 仅请求体 | 可变 |
| `proxyHistory.response.headers` | 仅状态行 + 响应头 | 小（< 1KB/条） |
| `proxyHistory.response.body` | 仅响应体 | **大 — 避免使用** |
| `siteMap.request.headers` | 与上方站点地图相同 | 小 |
| `siteMap.request.body` | | 可变 |
| `siteMap.response.headers` | | 小 |
| `siteMap.response.body` | | **大 — 避免使用** |

### 默认方法

**从请求头开始，而非请求体：**

```bash
# GOOD - headers only, safe to retrieve
{baseDir}/scripts/burp-search.sh project.burp proxyHistory.request.headers | head -c 50000
{baseDir}/scripts/burp-search.sh project.burp proxyHistory.response.headers | head -c 50000

# BAD - full records include bodies, can be gigabytes
{baseDir}/scripts/burp-search.sh project.burp proxyHistory  # NEVER DO THIS
```

**仅在查看请求头后获取特定 URL 的请求体，且务必截断：**

```bash
# 1. First, find interesting URLs from headers
{baseDir}/scripts/burp-search.sh project.burp proxyHistory.response.headers | \
  jq -r 'select(.headers | test("text/html")) | .url' | head -n 20

# 2. Then search bodies with targeted regex - MUST truncate body to 1000 chars
{baseDir}/scripts/burp-search.sh project.burp "responseBody='.*specific-pattern.*'" | \
  head -n 10 | jq -c '.body = (.body[:1000] + "...[TRUNCATED]")'
```

**硬性规则：超过 1000 字符的请求体内容绝不能进入上下文。** 如果用户需要完整的请求体内容，必须在 Burp Suite 的 UI 中查看。

## 正则搜索操作

### 搜索响应头
```bash
responseHeader='.*regex.*'
```
搜索所有响应头。输出：`{"url":"...", "header":"..."}`

示例 — 查找服务器签名：
```bash
responseHeader='.*(nginx|Apache|Servlet).*' | head -c 50000
```

### 搜索响应体
```bash
responseBody='.*regex.*'
```
**强制要求：始终将请求体内容截断至最多 1000 字符。** 每个响应体可能达到数 MB。

```bash
# REQUIRED format - always truncate .body field
{baseDir}/scripts/burp-search.sh project.burp "responseBody='.*<form.*action.*'" | \
  head -n 10 | jq -c '.body = (.body[:1000] + "...[TRUNCATED]")'
```

**绝不要获取完整的请求体内容。** 如果需要查看某个响应的更多内容，请让用户在 Burp Suite 的 UI 中打开。

## 其他操作

### 提取审计项
```bash
auditItems
```
返回所有安全发现。输出包含：name、severity、confidence、host、port、protocol、url。

**注意：** 审计项很小（不含请求体）— 可安全使用 `head -n 100` 获取。

### 导出代理历史（避免使用）
```bash
proxyHistory
```
**绝不要直接使用此命令。** 请改用子组件过滤器：
- `proxyHistory.request.headers`
- `proxyHistory.response.headers`

### 导出站点地图（避免使用）
```bash
siteMap
```
**绝不要直接使用此命令。** 请改用子组件过滤器。

## 输出限制（必须遵守）

**关键：获取数据前务必先检查结果大小。** 宽泛的搜索可能返回数千条记录，每条可能达数 MB。这会导致上下文窗口溢出。

### 步骤 1：始终先检查大小

任何搜索之前，同时检查记录数和字节数：

```bash
# Check record count AND total bytes - never skip this step
{baseDir}/scripts/burp-search.sh project.burp proxyHistory | wc -cl
{baseDir}/scripts/burp-search.sh project.burp "responseHeader='.*Server.*'" | wc -cl
{baseDir}/scripts/burp-search.sh project.burp auditItems | wc -cl
```

`wc -cl` 输出格式：`<字节数> <行数>`（例如 `524288 42` 表示 512KB 共 42 条记录）。

**解读结果 — 两项都必须通过：**

| 指标 | 安全 | 需缩小搜索 | 过于宽泛 | 停止 |
|------|------|-----------|---------|------|
| **行数** | < 50 | 50-200 | 200+ | 1000+ |
| **字节数** | < 50KB | 50-200KB | 200KB+ | 1MB+ |

**一条 10MB 的响应只占 1 行但字节数很高 — 字节检查能捕获这种情况。**

### 步骤 2：缩小宽泛搜索

如果计数/大小过高：

1. **使用子组件过滤器**（见上方表格）：
   ```bash
   # Instead of: proxyHistory (gigabytes)
   # Use: proxyHistory.request.headers (kilobytes)
   ```

2. **缩小正则模式：**
   ```bash
   # Too broad (matches everything):
   responseHeader='.*'

   # Better - target specific headers:
   responseHeader='.*X-Frame-Options.*'
   responseHeader='.*Content-Security-Policy.*'
   ```

3. **获取前用 jq 过滤：**
   ```bash
   # Get only specific content types
   {baseDir}/scripts/burp-search.sh project.burp proxyHistory.response.headers | \
     jq -c 'select(.url | test("/api/"))' | head -n 50
   ```

### 步骤 3：始终截断输出

即使缩小了范围，也务必通过截断管道输出：

```bash
# ALWAYS use head -c to limit total bytes (max 50KB)
{baseDir}/scripts/burp-search.sh project.burp proxyHistory.request.headers | head -c 50000

# For body searches, truncate each JSON object's body field:
{baseDir}/scripts/burp-search.sh project.burp "responseBody='pattern'" | \
  head -n 20 | jq -c '.body = (.body | if length > 1000 then .[:1000] + "...[TRUNCATED]" else . end)'

# Limit both record count AND byte size:
{baseDir}/scripts/burp-search.sh project.burp auditItems | head -n 50 | head -c 50000
```

**必须执行的硬性限制：**
- 所有输出使用 `head -c 50000`（最大 50KB）
- **将 `.body` 字段截断至 1000 字符 — 强制要求，无例外**
  ```bash
  jq -c '.body = (.body[:1000] + "...[TRUNCATED]")'
  ```

**以下操作必须先计数再截断：**
- `proxyHistory` / `siteMap`（完整导出 — 始终使用子组件过滤器）
- `responseBody='...'` 搜索（每条响应体可能达数 MB）
- 任何宽泛的正则如 `.*` 或 `.+`

## 调查工作流

1. **确定范围** — 你在寻找什么？（特定漏洞类型、端点、请求头模式）

2. **先搜索审计项** — 从 Burp 的发现开始：
   ```bash
   {baseDir}/scripts/burp-search.sh project.burp auditItems | jq 'select(.severity == "High")'
   ```

3. **检查置信度评分** — 过滤出可操作的发现：
   ```bash
   ... | jq 'select(.confidence == "Certain" or .confidence == "Firm")'
   ```

4. **提取受影响的 URL** — 获取攻击面：
   ```bash
   ... | jq -r '.url' | sort -u
   ```

5. **搜索原始流量获取上下文** — 检查实际的请求/响应：
   ```bash
   {baseDir}/scripts/burp-search.sh project.burp "responseBody='pattern'"
   ```

6. **手动验证** — Burp 的发现是指标，不是证据。逐一验证每项发现。

## 理解结果

### 严重程度 vs 置信度

Burp 同时报告**严重程度**（High/Medium/Low）和**置信度**（Certain/Firm/Tentative）。分诊时两者都要参考：

| 组合 | 含义 |
|------|------|
| High + Certain | 可能是真实漏洞，优先调查 |
| High + Tentative | 常为误报，报告前需验证 |
| Medium + Firm | 值得调查，可能需要手动验证 |

"High 严重程度、Tentative 置信度"的发现通常是误报。不要仅凭严重程度报告发现。

### 代理历史不完整的情况

代理历史仅包含 Burp 捕获的内容。可能因以下原因缺少流量：
- **范围过滤器**排除了某些域名
- **拦截设置**丢弃了请求
- **浏览器流量**未经过 Burp 代理

如果未找到预期的流量，请在原始项目中检查 Burp 的范围和代理设置。

### HTTP 请求体编码

响应体可能经过 gzip 压缩、分块传输或使用非 UTF-8 编码。在纯文本上有效的正则模式可能在编码后的响应上静默失败。如果搜索返回的结果少于预期：
- 检查响应是否被压缩
- 尝试更宽泛的模式或先搜索请求头
- 使用 Burp 的 UI 检查原始响应与渲染响应

## 应拒绝的错误推理

导致遗漏漏洞或误报的常见捷径：

| 捷径 | 为何错误 |
|------|---------|
| "这个正则看起来没问题" | 先在样本数据上验证 — 编码和转义会导致静默失败 |
| "High 严重程度 = 必须修复" | 还要检查置信度评分；Burp 存在误报 |
| "所有审计项都相关" | 按实际威胁模型过滤；并非每个发现对每个应用都有意义 |
| "代理历史是完整的" | 可能被 Burp 范围/拦截设置过滤；你看到的只是 Burp 捕获的内容 |
| "Burp 发现了，所以是漏洞" | Burp 的发现需要手动验证 — 它们指示潜在问题，而非证据 |

## 输出格式

所有输出为 JSON，每行一个对象。通过管道传给 `jq` 进行格式化：
```bash
{baseDir}/scripts/burp-search.sh project.burp auditItems | jq .
```

使用 grep 过滤：
```bash
{baseDir}/scripts/burp-search.sh project.burp auditItems | grep -i "sql injection"
```

## 示例

搜索 CORS 请求头（带字节限制）：
```bash
{baseDir}/scripts/burp-search.sh project.burp "responseHeader='.*Access-Control.*'" | head -c 50000
```

获取所有高严重程度发现（审计项较小，但仍需限制）：
```bash
{baseDir}/scripts/burp-search.sh project.burp auditItems | jq -c 'select(.severity == "High")' | head -n 100
```

从代理历史中仅提取请求 URL：
```bash
{baseDir}/scripts/burp-search.sh project.burp proxyHistory.request.headers | jq -r '.request.url' | head -n 200
```

搜索响应体（必须将请求体截断至 1000 字符）：
```bash
{baseDir}/scripts/burp-search.sh project.burp "responseBody='.*password.*'" | \
  head -n 10 | jq -c '.body = (.body[:1000] + "...[TRUNCATED]")'
```

## 平台配置

包装脚本需要两个环境变量来定位 Burp Suite 自带的 Java 和 JAR 文件。

### macOS

```bash
export BURP_JAVA="/Applications/Burp Suite Professional.app/Contents/Resources/jre.bundle/Contents/Home/bin/java"
export BURP_JAR="/Applications/Burp Suite Professional.app/Contents/Resources/app/burpsuite_pro.jar"
```

### Windows

```powershell
$env:BURP_JAVA = "C:\Program Files\BurpSuiteProfessional\jre\bin\java.exe"
$env:BURP_JAR = "C:\Program Files\BurpSuiteProfessional\burpsuite_pro.jar"
```

### Linux

```bash
export BURP_JAVA="/opt/BurpSuiteProfessional/jre/bin/java"
export BURP_JAR="/opt/BurpSuiteProfessional/burpsuite_pro.jar"
```

将这些 export 语句添加到 shell 配置文件（`.bashrc`、`.zshrc` 等）中以持久化。

### 手动调用

如果不使用包装脚本，可直接调用：
```bash
"$BURP_JAVA" -jar -Djava.awt.headless=true "$BURP_JAR" \
  --project-file=/path/to/project.burp [FLAGS]
```

## 局限性
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
