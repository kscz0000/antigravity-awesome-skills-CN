# 数据转换参考

清洗、规范化、去重与丰富提取网页数据的模式。
在阶段 5（转换）中应用这些转换，位于提取与验证之间。

---

## 自动转换

始终对每个提取结果应用以下转换。

### 空白字符清理

```python
# 去除首尾空白，合并内部空白
value = ' '.join(value.split())

# 移除零宽字符
import re
value = re.sub(r'[\u200b\u200c\u200d\ufeff\u00a0]', ' ', value).strip()
```

需要处理的模式：
- 单元格值内的 `\n`、`\r`、`\t` -> 单个空格
- 多个连续空格 -> 单个空格
- 不间断空格（`&nbsp;`、`\u00a0`）-> 普通空格
- 零宽字符 -> 移除

### HTML 实体解码

| 实体       | 字符   | 实体        | 字符          |
|:------------|:----------|:-----------|:--------------|
| `&amp;`    | `&`       | `&quot;`   | `"`           |
| `&lt;`     | `<`       | `&apos;`   | `'`           |
| `&gt;`     | `>`       | `&#39;`    | `'`           |
| `&nbsp;`   | ` `       | `&#8217;`  | （弯引号 '）  |
| `&mdash;`  | `--`      | `&#8212;`  | `--`          |

```python
import html
value = html.unescape(value)
```

### Unicode 规范化

```python
import unicodedata
value = unicodedata.normalize('NFKC', value)
```

这会处理：
- 花引号 -> 标准引号
- 连字 -> 拆分的字符（例如 `ﬁ` -> `fi`）
- 全角字符 -> 标准字符（例如 `Ａ` -> `A`）
- 上标/下标数字 -> 普通数字

### 空值标准化

| 输入                       | Markdown 输出 | JSON 输出 |
|:---------------------------|:----------------|:------------|
| `""`（空字符串）            | `N/A`           | `null`      |
| `"-"` 或 `"--"`            | `N/A`           | `null`      |
| `"N/A"`、`"n/a"`、`"NA"`   | `N/A`           | `null`      |
| `"None"`、`"null"`         | `N/A`           | `null`      |
| `"TBD"`、`"TBA"`           | `TBD`           | `"TBD"`     |

---

## 价格规范化

在提取产品、定价或金融数据时应用。

### 提取模式

```python
import re

def normalize_price(raw):
    if not raw:
        return None
    # 移除货币单词
    cleaned = re.sub(r'(?i)(USD|EUR|GBP|BRL|R\$|US\$)', '', raw)
    # 提取数值（同时处理 1,234.56 和 1.234,56 两种格式）
    match = re.search(r'[\d.,]+', cleaned)
    if not match:
        return None
    num_str = match.group()
    # 检测格式：若最后分隔符是逗号且后跟 2 位数字，则为小数
    if re.search(r',\d{2}$', num_str):
        num_str = num_str.replace('.', '').replace(',', '.')
    else:
        num_str = num_str.replace(',', '')
    return float(num_str)
```

### 货币检测

| 符号/代码              | 货币         | 符号/代码           | 货币         |
|:------------------------|:-------------|:---------------------|:-------------|
| `$`、`US$`、`USD`       | 美元         | `R$`、`BRL`         | 巴西雷亚尔   |
| `€`、`EUR`              | 欧元         | `£`、`GBP`          | 英镑         |
| `¥`、`JPY`              | 日元         | `₹`、`INR`          | 印度卢比     |
| `C$`、`CAD`             | 加拿大元     | `A$`、`AUD`         | 澳大利亚元   |

### 输出格式

```json
{
  "price": 29.99,
  "currency": "USD",
  "rawPrice": "$29.99"
}
```

对于 Markdown，按以下格式显示：`$29.99`（在表格中右对齐）。

---

## 日期规范化

将所有日期统一为 ISO-8601 格式。

### 常见待处理格式

| 输入格式              | 示例                  | 规范化结果         |
|:------------------------|:---------------------|:-------------------|
| 完整文本                | February 25, 2026    | 2026-02-25         |
| 简短文本                | Feb 25, 2026         | 2026-02-25         |
| 美式数字                | 02/25/2026           | 2026-02-25         |
| 欧式数字                | 25/02/2026           | 2026-02-25         |
| 已是 ISO                | 2026-02-25           | 2026-02-25         |
| 相对日期                | 3 days ago           | （从当前计算）     |
| 相对日期                | Yesterday            | （从当前计算）     |
| 时间戳                  | 1740441600           | 2025-02-25         |
| 含时间                  | 2026-02-25T14:30:00Z | 2026-02-25 14:30   |

### 模糊日期

当格式模糊时（例如 `03/04/2026`）：
- 默认采用美式格式（MM/DD/YYYY），除非站点明显为非美式
- 检查页面的 `lang` 属性或 URL TLD 以获取区域提示
- 在交付备注中注明模糊性

### 相对日期解析

```python
from datetime import datetime, timedelta
import re

def resolve_relative_date(text):
    text = text.lower().strip()
    today = datetime.now()

    if 'today' in text: return today.strftime('%Y-%m-%d')
    if 'yesterday' in text: return (today - timedelta(days=1)).strftime('%Y-%m-%d')

    match = re.search(r'(\d+)\s*(hour|day|week|month|year)s?\s*ago', text)
    if match:
        n, unit = int(match.group(1)), match.group(2)
        deltas = {'hour': 0, 'day': n, 'week': n*7, 'month': n*30, 'year': n*365}
        return (today - timedelta(days=deltas.get(unit, 0))).strftime('%Y-%m-%d')

    return text  # 无法解析则原样返回
```

---

## URL 解析

将相对 URL 转换为绝对 URL。

### 模式

| 输入                      | 基础 URL                     | 解析结果                                |
|:--------------------------|:------------------------------|:----------------------------------------|
| `/products/item-1`        | `https://example.com/shop`    | `https://example.com/products/item-1`   |
| `item-1`                  | `https://example.com/shop/`   | `https://example.com/shop/item-1`       |
| `//cdn.example.com/img`   | `https://example.com`         | `https://cdn.example.com/img`           |
| `https://other.com/page`  | （任意）                      | `https://other.com/page`（绝对）         |

### JavaScript 解析

```javascript
function resolveUrl(relative, base) {
  try { return new URL(relative, base || window.location.href).href; }
  catch { return relative; }
}
```

---

## 电话规范化

用于联系模式提取。

### 模式

```python
import re

def normalize_phone(raw):
    if not raw:
        return None
    # 移除所有非数字字符，但保留开头的 +
    digits = re.sub(r'[^\d+]', '', raw)
    if not digits or len(digits) < 7:
        return None
    # 若像是国际号码则补上前缀 +
    if len(digits) >= 11 and not digits.startswith('+'):
        digits = '+' + digits
    return digits
```

### 按场景格式化

| 场景         | 格式示例            |
|:-------------|:---------------------|
| JSON 输出    | `"+5511999998888"`   |
| Markdown 表格 | `+55 11 99999-8888`  |
| CSV 输出     | `"+5511999998888"`   |

---

## 去重

### 精确去重

```python
def deduplicate(records, key_fields=None):
    """移除完全重复的记录。
    若提供 key_fields，则仅按这些字段去重。
    """
    seen = set()
    unique = []
    for record in records:
        if key_fields:
            key = tuple(record.get(f) for f in key_fields)
        else:
            key = tuple(sorted(record.items()))
        if key not in seen:
            seen.add(key)
            unique.append(record)
    return unique, len(records) - len(unique)  # 返回 (去重后列表, 移除数量)
```

### 近似重复检测

当记录共享关键字段但细节不同时：
1. 按关键字段分组（例如 商品名 + 来源）
2. 对每组，保留 null 值最少的那条
3. 若仍平分，保留先出现的那条
4. 在备注中报告："已合并 N 条近似重复记录"

### 按模式选择去重键

| 模式     | 关键字段                              |
|:---------|:--------------------------------------|
| product  | name + source（或 name + brand）      |
| contact  | name + email（或 name + org）         |
| jobs     | title + company + location            |
| events   | title + date + location               |
| table    | 所有字段（完全匹配）                  |
| list     | 前 2-3 个识别字段                     |

---

## 文本清洗

### 移除噪声

从提取的文本中剥离常见的噪声模式：

| 模式                                | 操作                  |
|:------------------------------------|:----------------------|
| `\[edit\]`、`\[citation needed\]`    | 移除（维基百科）      |
| `Read more...`、`See more`          | 移除（截断标记）      |
| `Sponsored`、`Ad`、`Promoted`        | 移除或标记            |
| Cookie 同意文本                     | 移除                  |
| 导航面包屑                          | 移除                  |
| 页脚样板文字                        | 移除                  |

### 句首大写规范化

在提取全大写或大小写不一致的文本时：

```python
def normalize_case(text):
    if text.isupper() and len(text) > 3:
        return text.title()  # ALL CAPS -> Title Case
    return text
```

仅在以下情况应用：字段明显是全大写输入（老旧站点常见）、用户要求、或数据规范化后看起来更佳。

---

## 数据类型强制转换

### 自动类型检测

| 原始值           | 检测类型    | 转换值              |
|:----------------|:------------|:--------------------|
| `"123"`         | 整数        | `123`               |
| `"12.99"`       | 浮点数      | `12.99`             |
| `"true"`        | 布尔        | `true`              |
| `"false"`       | 布尔        | `false`             |
| `"2026-02-25"`  | 日期字符串  | `"2026-02-25"`      |
| `"$29.99"`      | 价格        | `29.99` + 货币      |
| `"4.5/5"`       | 评分        | `4.5`               |
| `"1,234"`       | 整数        | `1234`              |

### 评分规范化

```python
import re

def normalize_rating(raw):
    if not raw:
        return None
    match = re.search(r'([\d.]+)\s*(?:/\s*([\d.]+))?', str(raw))
    if match:
        score = float(match.group(1))
        max_score = float(match.group(2)) if match.group(2) else 5.0
        return round(score / max_score * 5, 1)  # 归一化到 /5 分制
    return None
```

---

## 丰富模式

### 域名提取

从完整 URL 中提取域名：
```python
from urllib.parse import urlparse

def extract_domain(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        return domain
    except:
        return None
```

### 字数统计

用于文章模式：
```python
def word_count(text):
    return len(text.split()) if text else 0
```

### 相对时间

添加自该日期以来人类可读的时间：
```python
def time_since(date_str):
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(date_str)
        delta = datetime.now() - dt
        if delta.days == 0: return "Today"
        if delta.days == 1: return "Yesterday"
        if delta.days < 7: return f"{delta.days} days ago"
        if delta.days < 30: return f"{delta.days // 7} weeks ago"
        if delta.days < 365: return f"{delta.days // 30} months ago"
        return f"{delta.days // 365} years ago"
    except:
        return None
```

---

## 转换流水线顺序

按以下顺序应用转换：

1. **HTML 实体解码** - 原始文本清洗
2. **Unicode 规范化** - 字符标准化
3. **空白字符清理** - 间距规范化
4. **空值标准化** - null/N/A 处理
5. **URL 解析** - 相对转绝对
6. **数据类型强制转换** - 字符串转数字/日期
7. **价格规范化** - 若适用
8. **日期规范化** - 若适用
9. **电话规范化** - 若适用
10. **文本清洗** - 噪声移除
11. **去重** - 移除重复
12. **排序** - 用户要求的顺序
13. **丰富** - 域名、字数统计等

并非所有步骤都适用于每次提取。只需应用与数据类型和提取模式相关的部分。
