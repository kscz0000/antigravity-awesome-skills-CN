---
name: vibecode-production-qa-validator
description: "面向全栈 Next.js 应用的 13 阶段生产 QA：构建验证、SEO 标签、OG 图片、favicon、路由回归、API 鉴权、页面速度、懒加载、漏洞扫描、UI/UX 卡片、错误边界、数据库、安全渲染与清理。用于生产环境 QA、上线前检查、Next.js 全栈检查清单、13 阶段验证、构建验证、SEO 检查、OG 图片验证、favicon 检查、路由回归、API 鉴权、PageSpeed、懒加载、漏洞扫描、UI/UX 检查、错误边界、数据库检查、安全渲染、清理、部署清单。"
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-05-31"
author: Whoisabhishekadhikari
tags: [qa, nextjs, production, deployment, seo, authentication, api, performance, favicon, cleanup, lighthouse, database, security, ui-ux]
tools: [claude, cursor, gemini, claude-code, opencode]
version: 2.0.0
---

# 生产环境 QA 校验器

按顺序执行各阶段。修复失败项后再进入下一阶段。

## 适用场景

- 在全栈 Next.js 应用发布或晋升到生产环境之前使用。
- 在涉及 UI、SEO、鉴权、API、数据库或依赖的大改动之后，需要一次具体的上线就绪度检查时使用。
- 当你需要一份紧凑的、以命令驱动的检查清单，覆盖构建、路由、元数据、性能、安全与清理项时使用。

```bash
export PROD_URL="https://yourdomain.com"
export QA_AUTH_HEADER=""       # optional: "Bearer eyJ..."
export PAGESPEED_API_KEY=""    # optional: for auto PageSpeed API
```

---

## 合并运行器

```bash
qa:all() { qa:code && qa:build && qa:routes / /about /contact /privacy /terms /faq /sitemap.xml /robots.txt /api/health && qa:seo && qa:api /api/health /api/tools && qa:git && qa:smoke; }
qa:full() { qa:all && qa:auth && qa:auth:cookies && qa:lazyload && qa:heavyload && qa:vulns && qa:cleanup && qa:ux:cards && qa:ux:boundaries && qa:ux:animation && qa:database && qa:secure; }
```

---

### 阶段 1：代码完整性

- [ ] `npx tsc --noEmit`
- [ ] `npx eslint . --ext .js,.jsx,.ts,.tsx --max-warnings 0`
- [ ] `npm test -- --runInBand --passWithNoTests`

```bash
qa:code() { npx tsc --noEmit && npx eslint . --ext .js,.jsx,.ts,.tsx --max-warnings 0 && npm test -- --runInBand --passWithNoTests; }
```

---

### 阶段 2：构建验证

- [ ] `npm run build` 成功
- [ ] SEO 页面显示 `○`/`●` 而非 `λ`
- [ ] 构建日志无错误

```bash
qa:build() { local log; log="$(mktemp "${TMPDIR:-/tmp}/qa-build.XXXXXX.log")" || return 1; set -o pipefail; npm run build 2>&1 | tee "$log"; local rc=$?; set +o pipefail; [ "$rc" -eq 0 ] && ! grep -qi "error\|failed" "$log"; local ok=$?; rm -f "$log"; return "$ok"; }
```

| 符号 | 含义 |
|--------|---------|
| `○` | 静态 |
| `●` | SSG |
| `λ` | 动态/无服务器 |
| `⊕` | 部分预渲染 |

---

### 阶段 3：API 会话与鉴权

- [ ] 鉴权端点正常响应（登录、会话、登出）
- [ ] 受保护路由返回 401/403
- [ ] 会话 Cookie：HttpOnly + Secure + SameSite
- [ ] Cookie 未过期，Path/Domain 正确
- [ ] 无法绕过限流

```bash
qa:auth() {
  local F=0
  for ep in /api/auth/login /api/auth/session /api/auth/logout; do
    curl -so /dev/null -w "%{http_code}" "$PROD_URL$ep" | grep -q "200\|401" || { echo "  ✗ $ep unreachable"; ((F++)); }
  done
  curl -so /dev/null -w "%{http_code}" "$PROD_URL/api/protected" | grep -q "401\|403" || echo "  ⚠ Protected route not denying unauthenticated"
  return $F
}
qa:auth:cookies() {
  for ep in /api/auth/session /api/auth/login; do
    curl -sI "$PROD_URL$ep" | grep -i "^set-cookie:" | while IFS= read -r c; do
      echo "  $ep: $(echo "$c" | cut -d= -f1)"
      echo "$c" | grep -qi "HttpOnly" || echo "    ✗ Missing HttpOnly"
      echo "$c" | grep -qi "Secure" || echo "    ✗ Missing Secure"
      echo "$c" | grep -qi "SameSite" || echo "    ⚠ Missing SameSite"
    done
  done
}
```

---

### 阶段 4：路由回归

- [ ] 核心页面、sitemap、robots.txt 均返回 200
- [ ] URL 使用 kebab-case，无重复 slug
- [ ] robots.txt 允许收录
- [ ] sitemap XML 合法，所有 URL 解析为 200

```bash
qa:routes() { local F=0; for p; do local C=$(curl -so /dev/null -w "%{http_code}" "$PROD_URL$p"); echo "$C $p"; [ "$C" = "200" ] || ((F++)); done; return $F; }
qa:robots() { curl -s "$PROD_URL/robots.txt" | grep -qi "Disallow: /$" && echo "  ✗ Blocks all crawlers" || echo "  ✓ OK"; }
qa:sitemap() { curl -s "$PROD_URL/sitemap.xml" | python3 -c "import sys,xml.etree.ElementTree as ET; ET.parse(sys.stdin); print('✓ Valid XML')"; }
```

---

### 阶段 5：SEO — 标签、图片、Favicon、Slug

- [ ] `<title>` 30–60 字符，每页唯一
- [ ] 原始 HTML 中包含 `<meta name="description">`
- [ ] og:title 与 `<title>` 一致，og:url 与 canonical 一致
- [ ] og:image ≥ 1200×630px，绝对 URL，加载返回 200
- [ ] twitter:card = summary_large_image
- [ ] Canonical 自引用，无重复
- [ ] `/favicon.ico` 返回 200，存在 apple-touch-icon
- [ ] 多语言时使用 `hreflang` 标签
- [ ] 存在 JSON-LD 结构化数据
- [ ] Slug：kebab-case，< 80 字符，无停用词

```bash
qa:seo() {
  local H=$(curl -s "$PROD_URL"); local F=0
  for t in "og:title" "og:description" "og:image" "twitter:card" "canonical" "description"; do echo "$H" | grep -qi "$t" || { echo "  ✗ $t"; ((F++)); }; done
  echo "$H" | grep -qi "<title>" || { echo "  ✗ <title>"; ((F++)); }
  local T=$(echo "$H" | grep -oP '<title>\K[^<]+'); local L=${#T}; [ $L -ge 30 -a $L -le 60 ] || echo "  ⚠ Title ${L}chars (target 30-60)"
  curl -so /dev/null -w "%{http_code}" "$PROD_URL/favicon.ico" | grep -q 200 || echo "  ⚠ No favicon.ico"
  return $F
}
qa:seo:ogimage() {
  local I=$(curl -s "$PROD_URL" | grep -oP 'og:image" content="\K[^"]+'); [[ "$I" =~ ^http ]] || I="$PROD_URL$I"
  curl -so /dev/null -w "%{http_code}" "$I" | grep -q 200 || { echo "  ✗ og:image returns non-200"; return 1; }
  command -v identify &>/dev/null && curl -s "$I" | identify -format "%wx%h" - 2>/dev/null | grep -qP "12\d{2}x6\d{2}" && echo "  ✓ ≥ 1200x630" || echo "  ⚠ Install imagemagick to check dimensions"
}
```

---

### 阶段 6：API 路由行为

- [ ] 状态码与 Content-Type 正确
- [ ] 错误返回一致的 JSON `{ error, message }`
- [ ] 响应时间 < 200ms
- [ ] CORS 头正确（跨域时）

```bash
qa:api() {
  for p; do
    local R=$(curl -so /dev/null -w "%{http_code} %{content_type}" "$PROD_URL$p")
    echo "  $p → $R"
  done
  local E=$(curl -s "$PROD_URL/api/nonexistent")
  echo "$E" | python3 -c "import sys,json; d=json.load(sys.stdin); assert 'error' in d; print('✓ Consistent errors')" 2>/dev/null || echo "  ⚠ Inconsistent error shape"
}
```

---

### 阶段 7：Git 卫生

- [ ] diff 中无密钥/凭据
- [ ] 没有暂存 `.next`/`node_modules`
- [ ] 提交信息：`type(scope): message`

```bash
qa:git() {
  local S=$(git diff HEAD 2>/dev/null | grep -i "password\|secret\|api_key\|localhost:3000" | grep "^+")
  [ -n "$S" ] && { echo "  ✗ Secrets in diff!"; echo "$S"; return 1; } || echo "  ✓ No secrets"
  local A=$(git status --short 2>/dev/null | grep -E "\.next|node_modules" | head -3)
  [ -n "$A" ] && echo "  ⚠ Build artifacts:" && echo "$A" || echo "  ✓ No artifacts"
}
```

---

### 阶段 8：部署后冒烟测试

- [ ] 首页 200，关键页面 200
- [ ] OG 图片加载返回 200
- [ ] 无控制台错误（手动）
- [ ] 鉴权流程可用（手动）

```bash
qa:smoke() {
  curl -sI "$PROD_URL" | head -1 | grep -q "200" && echo "  ✓ Homepage" || echo "  ✗ Homepage"
  curl -sI "$PROD_URL/sitemap.xml" | head -1 | grep -q "200" && echo "  ✓ Sitemap" || echo "  ✗ Sitemap"
}
```

---

### 阶段 9：页面速度、懒加载与包体积

- [ ] Lighthouse ≥ 90（性能、可访问性、SEO）
- [ ] FCP < 2.5s，LCP < 4.0s，CLS < 0.1
- [ ] 图片懒加载（`loading="lazy"`），使用 WebP/AVIF
- [ ] 对重量级组件使用动态导入
- [ ] 最大 JS chunk < 200KB（gzip 后）
- [ ] `font-display: swap`，无 FOIT
- [ ] 页面总权重 < 1MB

```bash
qa:lazyload() {
  local N=$(grep -r "loading=" app/ --include="*.tsx" 2>/dev/null | grep -c "lazy" || true)
  echo "  Lazy images: $N"
  grep -rn "next/dynamic\|dynamic((" app/ --include="*.tsx" 2>/dev/null | head -5 | grep . || echo "  ⚠ No dynamic imports"
}
qa:heavyload() {
  ls -lhS .next/static/chunks/*.js 2>/dev/null | head -5
  local W=$(curl -so /dev/null -w "%{size_download}" "$PROD_URL" 2>/dev/null || echo 0)
  echo "  HTML weight: ~$((W/1024))KB"
  echo "  ⚠ Run 'npx lighthouse $PROD_URL --view' for full weight analysis"
}
# PageSpeed: open "https://pagespeed.web.dev/?url=$PROD_URL"
```

---

### 阶段 10：清理与漏洞扫描

- [ ] `npm prune`、`depcheck` — 无未使用的依赖
- [ ] 暂存代码中无 console.log/debugger
- [ ] `npm audit` — 无 critical/high 级别漏洞
- [ ] 无 eval/new Function/document.write
- [ ] 所有 TODO 已处理

```bash
qa:vulns() {
  npm audit 2>/dev/null | grep -E "critical|high" | grep . && echo "  ✗ Vulnerabilities!" || echo "  ✓ No critical/high vulns"
  npm outdated 2>/dev/null | head -5 | grep . || echo "  ✓ All up to date"
  local D=$(grep -rn "eval(\|new Function(\|document.write(" app/ src/ --include="*.ts" --include="*.tsx" 2>/dev/null | head -5)
  [ -n "$D" ] && echo "  ⚠ Dangerous patterns:" && echo "$D" || echo "  ✓ No dangerous patterns"
}
qa:cleanup() {
  local D=$(git diff --cached 2>/dev/null | grep "^+" | grep -i "console\.log\|debugger" | head -5)
  [ -n "$D" ] && echo "  ✗ Debug artifacts:" && echo "$D" || echo "  ✓ No debug artifacts"
  local T=$(git diff --cached 2>/dev/null | grep "^+" | grep -i "TODO\|FIXME\|HACK" | head -5)
  [ -n "$T" ] && echo "  ⚠ TODOs remain:" && echo "$T"
}
```

---

### 阶段 11：UI/UX — 卡片、动画、错误边界

- [ ] 卡片：等高网格，无重叠，文本省略，响应式（1→2→3 列）
- [ ] 在任意视口（320–1440px）下无横向滚动
- [ ] 图片：统一的 `aspect-ratio` + `object-fit: cover`
- [ ] 触控目标 ≥ 44×44px
- [ ] 动画仅使用 `transform`+`opacity`（不使用布局属性）
- [ ] 尊重 `prefers-reduced-motion`
- [ ] 根级与路由级均有错误边界（`app/error.tsx`、`app/global-error.tsx`）
- [ ] 存在 `app/not-found.tsx` 与 `app/loading.tsx`
- [ ] 所有客户端请求都展示 loading + error + empty 三种状态
- [ ] 按钮：hover、focus-visible、active、disabled、loading 状态齐全
- [ ] 表单点击后立即禁用提交（防止重复提交）

```bash
qa:ux:cards() {
  local E=$(grep -rn "text-overflow\|line-clamp\|truncate" app/ --include="*.css" --include="*.tsx" 2>/dev/null | head -3)
  [ -n "$E" ] && echo "  ✓ Text overflow handling" || echo "  ⚠ No text overflow handling"
  local A=$(grep -rn "aspect-\|object-fit" app/ --include="*.css" --include="*.tsx" 2>/dev/null | head -3)
  [ -n "$A" ] && echo "  ✓ aspect-ratio/object-fit used" || echo "  ⚠ No aspect-ratio set"
}
qa:ux:boundaries() {
  for f in app/error.tsx app/global-error.tsx app/not-found.tsx app/loading.tsx; do
    [ -f "$f" ] && echo "  ✓ $f" || echo "  ⚠ Missing $f"
  done
}
qa:ux:animation() {
  local A=$(grep -rn "animation.*width\|transition.*height\|@keyframes.*top\|@keyframes.*margin" app/ --include="*.css" --include="*.tsx" 2>/dev/null | head -5)
  [ -n "$A" ] && echo "  ⚠ Layout-triggering animations:" && echo "$A" || echo "  ✓ No layout-triggering animations"
  local P=$(grep -r "@media.*prefers-reduced-motion" app/ --include="*.css" --include="*.tsx" 2>/dev/null | head -3)
  [ -n "$P" ] && echo "  ✓ prefers-reduced-motion found in CSS" || echo "  ⚠ No prefers-reduced-motion in CSS"
}
```

---

### 阶段 12：数据库与数据层

- [ ] 已配置连接池（避免耗尽）
- [ ] Schema 与迁移保持一致
- [ ] 所有被查询字段都有索引，无 N+1
- [ ] 源码中无硬编码的数据库凭据
- [ ] 无原始 SQL 注入风险
- [ ] API 响应未泄露敏感数据
- [ ] 迁移具有幂等性

```bash
qa:database() {
  local H=$(grep -rn "postgres://\|mysql://\|mongodb://" app/ src/ --include="*.ts" --include="*.tsx" 2>/dev/null | grep -v ".env" | head -5)
  [ -n "$H" ] && { echo "  ✗ Hardcoded DB URL:"; echo "$H"; } || echo "  ✓ No hardcoded DB URLs"
  local R=$(grep -rn "\$queryRaw\|\.raw(" app/ src/ --include="*.ts" --include="*.tsx" 2>/dev/null | head -5)
  [ -n "$R" ] && echo "  ⚠ Raw SQL:" && echo "$R" || echo "  ✓ No raw SQL"
  local N=$(grep -rn "\.findMany\|\.findUnique" app/ src/ --include="*.ts" --include="*.tsx" 2>/dev/null | grep -v "include:" | head -5)
  [ -n "$N" ] && echo "  ⚠ Possible N+1:" && echo "$N" || echo "  ✓ No N+1 patterns"
}
qa:db:migrations() {
  [ -d "prisma/migrations" ] && echo "  ✓ Prisma: $(ls prisma/migrations 2>/dev/null | wc -l) migrations" || echo "  - No prisma migrations dir"
  local M=$(ls db/migrations/*.sql 2>/dev/null | head -5); [ -n "$M" ] && echo "  ✓ SQL migrations:" && echo "$M" || echo "  - No SQL migration files"
}
```

---

### 阶段 13：安全的数据渲染

- [ ] 客户端源码或 localStorage 中无密钥/token
- [ ] 未配合 DOMPurify 时不使用 `dangerouslySetInnerHTML`
- [ ] API 错误未泄露堆栈
- [ ] 内部 ID 使用 UUID 而非自增
- [ ] UI 中对用户邮箱脱敏
- [ ] NEXT_PUBLIC_ 变量中不包含密钥

```bash
qa:secure() {
  local S=$(git grep -n "api_key\|API_KEY\|secret_key\|PRIVATE_KEY" -- ':!*.env*' ':!*test*' 2>/dev/null | head -5)
  [ -n "$S" ] && echo "  ✗ Secrets in source:" && echo "$S" || echo "  ✓ No hardcoded secrets"
  local D=$(grep -rn "dangerouslySetInnerHTML" app/ src/ --include="*.tsx" 2>/dev/null | head -5)
  [ -n "$D" ] && echo "  ⚠ XSS risk — use DOMPurify:" && echo "$D" || echo "  ✓ No dangerouslySetInnerHTML"
  local T=$(grep -rn "localStorage\|sessionStorage" app/ src/ --include="*.ts" --include="*.tsx" 2>/dev/null | grep -i "token\|jwt\|secret" | head -5)
  [ -n "$T" ] && echo "  ⚠ Tokens in storage — use httpOnly cookies:" && echo "$T" || echo "  ✓ No tokens in storage"
  curl -s "$PROD_URL/api/nonexistent" 2>/dev/null | grep -qi "stack\|Error:" && echo "  ✗ Stack trace leak" || echo "  ✓ No stack leak"
}
```

---

## Pre-Commit Hook

```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
npx tsc --noEmit || exit 1
npx eslint . --ext .js,.jsx,.ts,.tsx --max-warnings 0 || exit 1
EOF
chmod +x .git/hooks/pre-commit
```

---

## CI/CD（GitHub Actions）

```yaml
name: QA
on: [push, pull_request]
jobs:
  qa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx tsc --noEmit
      - run: npx eslint . --ext .js,.jsx,.ts,.tsx --max-warnings 0
      - run: npm test -- --runInBand --passWithNoTests
      - run: npm run build
```

---

## 最佳实践

| ✅ 应该 | ❌ 不应该 |
|-------|----------|
| 部署前运行完整的 13 阶段流程 | 跳过类型检查或 lint |
| 在 profile/.envrc 中设置 `PROD_URL` | 在脚本中硬编码 URL |
| OG 图片 ≥ 1200×630 | 使用小尺寸 OG 图片 |
| 使用 `transform`+`opacity` 做动画 | 对 width/height/top 做动画 |
| 展示 loading/error/empty 三种状态 | 让用户停留在空白页面 |
| 动画使用 `prefers-reduced-motion` | 对所有用户强制开启动效 |
| token 使用 HttpOnly + Secure Cookie | 把鉴权 token 存入 localStorage |
| 在所有层级设置错误边界 | 崩溃时出现白屏 |
| 数据库加索引 + include/populate | 在循环中执行 N+1 查询 |
| 部署前执行 `npm audit` | 在存在已知漏洞时部署 |

---

## 常见陷阱

| 问题 | 解决方案 |
|---------|----------|
| 原始 HTML 中缺少 OG 标签 | 在 Next.js 中使用 `export const metadata` |
| `Disallow: /` 出现在 robots.txt | 会阻止所有爬虫 — 改为针对具体路径 |
| 网格中卡片高度不一致 | 使用 `display: grid` 并设置等高行，而非 flex |
| 文本溢出卡片 | 添加 `text-overflow: ellipsis` + `overflow: hidden` |
| 动画卡顿 | 动画作用于 `transform` 而非 `width`/`height` |
| 表单重复提交 | 首次点击后立即禁用按钮 |
| 生产环境出现控制台错误 | 添加 `no-console` ESLint 规则 |
| 数据库连接超时 | 增加连接池（PgBouncer/Prisma Accelerate） |
| API 泄露敏感数据 | 在响应转换层剥离 `passwordHash`/`secret` |
| 应用因错误而崩溃 | 添加 `app/error.tsx` 错误边界 |
| JS 包体积过大 | 对重量级组件使用动态导入，配合 `next/bundle-analyzer` 分析 |
| 图片加载缓慢 | 添加 `loading="lazy"`，使用 WebP/AVIF，调整到显示尺寸 |

---

## 安全注意事项

- 所有 `qa:*` 函数都是只读的（tsc、lint、test、build、curl、grep）
- `PROD_URL` 与 `QA_AUTH_HEADER` 仅用于你拥有的环境
- `git diff` 中只做了基础的密钥扫描 — 生产环境请使用 `trufflehog`/`git-secrets`
- 在生产环境上使用真实凭据进行鉴权测试具有破坏性 — 请改用预发布环境

---

## 局限性

- 通过全部阶段只能降低风险，无法消除生产 bug
- 部分检查依赖项目特定的工具（Prisma、NextAuth 等）
- 关键用户路径仍需手动进行 UX 测试
- SEO 检查仅验证原始 HTML，无法覆盖社交预览渲染
- 路由检查仅验证状态码，不验证内容正确性

---

## 主检查清单

### 阶段 1：代码
- [ ] `tsc --noEmit`、`eslint`、`npm test` 通过

### 阶段 2：构建
- [ ] `npm run build` 成功，无错误，页面为静态

### 阶段 3：鉴权
- [ ] 端点正常响应，受保护路由被拒绝，Cookie 安全

### 阶段 4：路由
- [ ] 所有核心页面 200，sitemap 合法，robots.txt 正确

### 阶段 5：SEO
- [ ] title、description、og:*、twitter:card、canonical、favicon、slug

### 阶段 6：API
- [ ] 状态码、Content-Type、一致的错误结构、响应时间

### 阶段 7：Git
- [ ] 无密钥、无构建产物、Conventional Commit

### 阶段 8：冒烟
- [ ] 首页与关键页面 200，og:image 可加载

### 阶段 9：速度
- [ ] Lighthouse ≥ 90，图片懒加载，动态导入，font-display: swap

### 阶段 10：清理
- [ ] 无漏洞、无调试残留、未使用的依赖已剪除

### 阶段 11：UI/UX
- [ ] 卡片响应式，错误边界，按钮状态完整，prefers-reduced-motion

### 阶段 12：数据库
- [ ] 索引齐全，无 N+1，无硬编码 URL，无敏感信息泄露

### 阶段 13：安全渲染
- [ ] 客户端无密钥，无 XSS，无堆栈泄露，使用 UUID