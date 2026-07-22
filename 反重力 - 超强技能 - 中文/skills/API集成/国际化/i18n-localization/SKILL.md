---
name: i18n-localization
description: "国际化与本地化模式。检测硬编码字符串、管理翻译、语言环境文件、RTL支持。触发词：i18n、国际化、本地化、多语言、翻译、locale、RTL、语言切换、多语言支持"
risk: safe
source: community
date_added: "2026-02-27"
---

# i18n & 本地化

> 国际化 (i18n) 和本地化 (L10n) 最佳实践。

---

## 1. 核心概念

| 术语 | 含义 |
|------|------|
| **i18n** | 国际化 - 使应用可翻译 |
| **L10n** | 本地化 - 实际翻译工作 |
| **Locale** | 语言 + 地区 (en-US, tr-TR) |
| **RTL** | 从右到左的语言 (阿拉伯语、希伯来语) |

---

## 2. 何时使用 i18n

| 项目类型 | 是否需要 i18n |
|----------|---------------|
| 公共 Web 应用 | ✅ 需要 |
| SaaS 产品 | ✅ 需要 |
| 内部工具 | ⚠️ 视情况 |
| 单一地区应用 | ⚠️ 考虑未来需求 |
| 个人项目 | ❌ 可选 |

---

## 3. 实现模式

### React (react-i18next)

```tsx
import { useTranslation } from 'react-i18next';

function Welcome() {
  const { t } = useTranslation();
  return <h1>{t('welcome.title')}</h1>;
}
```

### Next.js (next-intl)

```tsx
import { useTranslations } from 'next-intl';

export default function Page() {
  const t = useTranslations('Home');
  return <h1>{t('title')}</h1>;
}
```

### Python (gettext)

```python
from gettext import gettext as _

print(_("Welcome to our app"))
```

---

## 4. 文件结构

```
locales/
├── en/
│   ├── common.json
│   ├── auth.json
│   └── errors.json
├── tr/
│   ├── common.json
│   ├── auth.json
│   └── errors.json
└── ar/          # RTL
    └── ...
```

---

## 5. 最佳实践

### 推荐 ✅

- 使用翻译键，而非原始文本
- 按功能模块命名空间划分翻译
- 支持复数形式
- 按语言环境处理日期/数字格式
- 从一开始就规划 RTL 支持
- 对复杂字符串使用 ICU 消息格式

### 避免 ❌

- 在组件中硬编码字符串
- 拼接翻译后的字符串
- 假设文本长度（德语通常长 30%）
- 忘记 RTL 布局
- 在同一文件中混合语言

---

## 6. 常见问题

| 问题 | 解决方案 |
|------|----------|
| 翻译缺失 | 回退到默认语言 |
| 硬编码字符串 | 使用 linter/检查脚本 |
| 日期格式 | 使用 Intl.DateTimeFormat |
| 数字格式 | 使用 Intl.NumberFormat |
| 复数形式 | 使用 ICU 消息格式 |

---

## 7. RTL 支持

```css
/* CSS 逻辑属性 */
.container {
  margin-inline-start: 1rem;  /* 而非 margin-left */
  padding-inline-end: 1rem;   /* 而非 padding-right */
}

[dir="rtl"] .icon {
  transform: scaleX(-1);
}
```

---

## 8. 检查清单

发布前检查：

- [ ] 所有面向用户的字符串使用翻译键
- [ ] 所有支持语言的翻译文件已存在
- [ ] 日期/数字格式使用 Intl API
- [ ] RTL 布局已测试（如适用）
- [ ] 已配置回退语言
- [ ] 组件中无硬编码字符串

---

## 脚本

| 脚本 | 用途 | 命令 |
|------|------|------|
| `scripts/i18n_checker.py` | 检测硬编码字符串和缺失翻译 | `python scripts/i18n_checker.py <project_path>` |

## 使用时机
本技能适用于执行概述中描述的工作流程或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出不能替代特定环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
