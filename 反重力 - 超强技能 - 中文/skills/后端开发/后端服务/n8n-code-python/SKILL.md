---
name: n8n-code-python
description: 在 n8n Code 节点中编写 Python 代码。当需要在 n8n 中编写 Python、使用 _input/_json/_node 语法、使用标准库或需要了解 n8n Code 节点中 Python 的限制时使用。
risk: unknown
source: community
---

# Python Code 节点（Beta）

在 n8n Code 节点中编写 Python 代码的专家指导。

---

## ⚠️ 重要提示：优先使用 JavaScript

**建议**：**95% 的用例使用 JavaScript**。仅在以下情况下使用 Python：
- 你需要特定的 Python 标准库函数
- 你对 Python 语法更加熟悉
- 你正在做更适合 Python 的数据转换

**为什么优先选择 JavaScript：**
- 完整的 n8n 辅助函数（$helpers.httpRequest 等）
- Luxon DateTime 库用于高级日期/时间操作
- 无外部库限制
- 更好的 n8n 文档和社区支持

---

## 快速开始

```python
# Basic template for Python Code nodes
items = _input.all()

# Process data
processed = []
for item in items:
    processed.append({
        "json": {
            **item["json"],
            "processed": True,
            "timestamp": datetime.now().isoformat()
        }
    })

return processed
```

### 基本规则

1. **优先考虑 JavaScript** - 仅在必要时使用 Python
2. **访问数据**：`_input.all()`、`_input.first()` 或 `_input.item`
3. **关键**：必须返回 `[{"json": {...}}]` 格式
4. **关键**：Webhook 数据在 `_json["body"]` 下（不是直接使用 `_json`）
5. **关键限制**：**无外部库**（没有 requests、pandas、numpy）
6. **仅标准库**：json、datetime、re、base64、hashlib、urllib.parse、math、random、statistics

---

## 模式选择指南

与 JavaScript 相同 - 根据你的用例选择：

### 对所有项运行一次（推荐 - 默认）

**适用场景：** 95% 的用例

- **工作原理**：无论输入数量多少，代码**只执行一次**
- **数据访问**：`_input.all()` 或 `_items` 数组（Native 模式）
- **最适合**：聚合、过滤、批处理、转换
- **性能**：多项时更快（单次执行）

```python
# Example: Calculate total from all items
all_items = _input.all()
total = sum(item["json"].get("amount", 0) for item in all_items)

return [{
    "json": {
        "total": total,
        "count": len(all_items),
        "average": total / len(all_items) if all_items else 0
    }
}]
```

### 对每个项运行一次

**适用场景：** 仅用于特殊情况

- **工作原理**：代码对每个输入项**分别执行**
- **数据访问**：`_input.item` 或 `_item`（Native 模式）
- **最适合**：项特定逻辑、独立操作、逐项验证
- **性能**：大数据集时较慢（多次执行）

```python
# Example: Add processing timestamp to each item
item = _input.item

return [{
    "json": {
        **item["json"],
        "processed": True,
        "processed_at": datetime.now().isoformat()
    }
}]
```

---

## Python 模式：Beta vs Native

n8n 提供两种 Python 执行模式：

### Python (Beta) - 推荐
- **使用**：`_input`、`_json`、`_node` 辅助语法
- **最适合**：大多数 Python 用例
- **可用辅助函数**：`_now`、`_today`、`_jmespath()`
- **导入**：`from datetime import datetime`

```python
# Python (Beta) example
items = _input.all()
now = _now  # Built-in datetime object

return [{
    "json": {
        "count": len(items),
        "timestamp": now.isoformat()
    }
}]
```

### Python (Native) (Beta)
- **使用**：仅 `_items`、`_item` 变量
- **无辅助函数**：没有 `_input`、`_now` 等
- **更受限**：仅标准 Python
- **适用场景**：需要不含 n8n 辅助函数的纯 Python

```python
# Python (Native) example
processed = []

for item in _items:
    processed.append({
        "json": {
            "id": item["json"].get("id"),
            "processed": True
        }
    })

return processed
```

**建议**：使用 **Python (Beta)** 以获得更好的 n8n 集成。

---

## 数据访问模式

### 模式 1：_input.all() - 最常用

**适用场景**：处理数组、批操作、聚合

```python
# Get all items from previous node
all_items = _input.all()

# Filter, transform as needed
valid = [item for item in all_items if item["json"].get("status") == "active"]

processed = []
for item in valid:
    processed.append({
        "json": {
            "id": item["json"]["id"],
            "name": item["json"]["name"]
        }
    })

return processed
```

### 模式 2：_input.first() - 非常常用

**适用场景**：处理单个对象、API 响应

```python
# Get first item only
first_item = _input.first()
data = first_item["json"]

return [{
    "json": {
        "result": process_data(data),
        "processed_at": datetime.now().isoformat()
    }
}]
```

### 模式 3：_input.item - 仅限每项模式

**适用场景**：在"对每个项运行一次"模式下

```python
# Current item in loop (Each Item mode only)
current_item = _input.item

return [{
    "json": {
        **current_item["json"],
        "item_processed": True
    }
}]
```

### 模式 4：_node - 引用其他节点

**适用场景**：需要工作流中特定节点的数据

```python
# Get output from specific node
webhook_data = _node["Webhook"]["json"]
http_data = _node["HTTP Request"]["json"]

return [{
    "json": {
        "combined": {
            "webhook": webhook_data,
            "api": http_data
        }
    }
}]
```

**参见**：DATA_ACCESS.md 获取完整指南

---

## 关键：Webhook 数据结构

**最常见的错误**：Webhook 数据嵌套在 `["body"]` 下

```python
# ❌ WRONG - Will raise KeyError
name = _json["name"]
email = _json["email"]

# ✅ CORRECT - Webhook data is under ["body"]
name = _json["body"]["name"]
email = _json["body"]["email"]

# ✅ SAFER - Use .get() for safe access
webhook_data = _json.get("body", {})
name = webhook_data.get("name")
```

**原因**：Webhook 节点将所有请求数据包装在 `body` 属性下。这包括 POST 数据、查询参数和 JSON 负载。

**参见**：DATA_ACCESS.md 获取完整的 Webhook 结构详情

---

## 返回格式要求

**关键规则**：始终返回包含 `"json"` 键的字典列表

### 正确的返回格式

```python
# ✅ Single result
return [{
    "json": {
        "field1": value1,
        "field2": value2
    }
}]

# ✅ Multiple results
return [
    {"json": {"id": 1, "data": "first"}},
    {"json": {"id": 2, "data": "second"}}
]

# ✅ List comprehension
transformed = [
    {"json": {"id": item["json"]["id"], "processed": True}}
    for item in _input.all()
    if item["json"].get("valid")
]
return transformed

# ✅ Empty result (when no data to return)
return []

# ✅ Conditional return
if should_process:
    return [{"json": processed_data}]
else:
    return []
```

### 错误的返回格式

```python
# ❌ WRONG: Dictionary without list wrapper
return {
    "json": {"field": value}
}

# ❌ WRONG: List without json wrapper
return [{"field": value}]

# ❌ WRONG: Plain string
return "processed"

# ❌ WRONG: Incomplete structure
return [{"data": value}]  # Should be {"json": value}
```

**为什么重要**：下一个节点期望列表格式。格式不正确会导致工作流执行失败。

**参见**：ERROR_PATTERNS.md #2 获取详细错误解决方案

---

## 关键限制：无外部库

**最重要的 Python 限制**：无法导入外部包

### 不可用的内容

```python
# ❌ NOT AVAILABLE - Will raise ModuleNotFoundError
import requests  # ❌ No
import pandas  # ❌ No
import numpy  # ❌ No
import scipy  # ❌ No
from bs4 import BeautifulSoup  # ❌ No
import lxml  # ❌ No
```

### 可用的内容（标准库）

```python
# ✅ AVAILABLE - Standard library only
import json  # ✅ JSON parsing
import datetime  # ✅ Date/time operations
import re  # ✅ Regular expressions
import base64  # ✅ Base64 encoding/decoding
import hashlib  # ✅ Hashing functions
import urllib.parse  # ✅ URL parsing
import math  # ✅ Math functions
import random  # ✅ Random numbers
import statistics  # ✅ Statistical functions
```

### 替代方案

**需要 HTTP 请求？**
- ✅ 在 Code 节点之前使用 **HTTP Request 节点**
- ✅ 或切换到 **JavaScript** 并使用 `$helpers.httpRequest()`

**需要数据分析（pandas/numpy）？**
- ✅ 使用 Python **statistics** 模块进行基本统计
- ✅ 或切换到 **JavaScript** 处理大多数操作
- ✅ 使用列表和字典进行手动计算

**需要网页抓取（BeautifulSoup）？**
- ✅ 使用 **HTTP Request 节点** + **HTML Extract 节点**
- ✅ 或切换到 **JavaScript** 使用正则表达式/字符串方法

**参见**：STANDARD_LIBRARY.md 获取完整参考

---

## 常用模式概述

基于生产工作流，以下是最有用的 Python 模式：

### 1. 数据转换
使用列表推导式转换所有项

```python
items = _input.all()

return [
    {
        "json": {
            "id": item["json"].get("id"),
            "name": item["json"].get("name", "Unknown").upper(),
            "processed": True
        }
    }
    for item in items
]
```

### 2. 过滤与聚合
使用内置函数求和、过滤、计数

```python
items = _input.all()
total = sum(item["json"].get("amount", 0) for item in items)
valid_items = [item for item in items if item["json"].get("amount", 0) > 0]

return [{
    "json": {
        "total": total,
        "count": len(valid_items)
    }
}]
```

### 3. 使用正则表达式处理字符串
从文本中提取模式

```python
import re

items = _input.all()
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

all_emails = []
for item in items:
    text = item["json"].get("text", "")
    emails = re.findall(email_pattern, text)
    all_emails.extend(emails)

# Remove duplicates
unique_emails = list(set(all_emails))

return [{
    "json": {
        "emails": unique_emails,
        "count": len(unique_emails)
    }
}]
```

### 4. 数据验证
验证和清理数据

```python
items = _input.all()
validated = []

for item in items:
    data = item["json"]
    errors = []

    # Validate fields
    if not data.get("email"):
        errors.append("Email required")
    if not data.get("name"):
        errors.append("Name required")

    validated.append({
        "json": {
            **data,
            "valid": len(errors) == 0,
            "errors": errors if errors else None
        }
    })

return validated
```

### 5. 统计分析
使用 statistics 模块计算统计数据

```python
from statistics import mean, median, stdev

items = _input.all()
values = [item["json"].get("value", 0) for item in items if "value" in item["json"]]

if values:
    return [{
        "json": {
            "mean": mean(values),
            "median": median(values),
            "stdev": stdev(values) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values),
            "count": len(values)
        }
    }]
else:
    return [{"json": {"error": "No values found"}}]
```

**参见**：COMMON_PATTERNS.md 获取 10 个详细 Python 模式

---

## 错误预防 - 前 5 个错误

### #1：导入外部库（Python 特有！）

```python
# ❌ WRONG: Trying to import external library
import requests  # ModuleNotFoundError!

# ✅ CORRECT: Use HTTP Request node or JavaScript
# Add HTTP Request node before Code node
# OR switch to JavaScript and use $helpers.httpRequest()
```

### #2：空代码或缺少返回

```python
# ❌ WRONG: No return statement
items = _input.all()
# Processing...
# Forgot to return!

# ✅ CORRECT: Always return data
items = _input.all()
# Processing...
return [{"json": item["json"]} for item in items]
```

### #3：返回格式不正确

```python
# ❌ WRONG: Returning dict instead of list
return {"json": {"result": "success"}}

# ✅ CORRECT: List wrapper required
return [{"json": {"result": "success"}}]
```

### #4：字典访问时 KeyError

```python
# ❌ WRONG: Direct access crashes if missing
name = _json["user"]["name"]  # KeyError!

# ✅ CORRECT: Use .get() for safe access
name = _json.get("user", {}).get("name", "Unknown")
```

### #5：Webhook Body 嵌套

```python
# ❌ WRONG: Direct access to webhook data
email = _json["email"]  # KeyError!

# ✅ CORRECT: Webhook data under ["body"]
email = _json["body"]["email"]

# ✅ BETTER: Safe access with .get()
email = _json.get("body", {}).get("email", "no-email")
```

**参见**：ERROR_PATTERNS.md 获取完整错误指南

---

## 标准库参考

### 最有用的模块

```python
# JSON operations
import json
data = json.loads(json_string)
json_output = json.dumps({"key": "value"})

# Date/time
from datetime import datetime, timedelta
now = datetime.now()
tomorrow = now + timedelta(days=1)
formatted = now.strftime("%Y-%m-%d")

# Regular expressions
import re
matches = re.findall(r'\d+', text)
cleaned = re.sub(r'[^\w\s]', '', text)

# Base64 encoding
import base64
encoded = base64.b64encode(data).decode()
decoded = base64.b64decode(encoded)

# Hashing
import hashlib
hash_value = hashlib.sha256(text.encode()).hexdigest()

# URL parsing
import urllib.parse
params = urllib.parse.urlencode({"key": "value"})
parsed = urllib.parse.urlparse(url)

# Statistics
from statistics import mean, median, stdev
average = mean([1, 2, 3, 4, 5])
```

**参见**：STANDARD_LIBRARY.md 获取完整参考

---

## 最佳实践

### 1. 始终使用 .get() 访问字典

```python
# ✅ SAFE: Won't crash if field missing
value = item["json"].get("field", "default")

# ❌ RISKY: Crashes if field doesn't exist
value = item["json"]["field"]
```

### 2. 显式处理 None/Null 值

```python
# ✅ GOOD: Default to 0 if None
amount = item["json"].get("amount") or 0

# ✅ GOOD: Check for None explicitly
text = item["json"].get("text")
if text is None:
    text = ""
```

### 3. 使用列表推导式进行过滤

```python
# ✅ PYTHONIC: List comprehension
valid = [item for item in items if item["json"].get("active")]

# ❌ VERBOSE: Manual loop
valid = []
for item in items:
    if item["json"].get("active"):
        valid.append(item)
```

### 4. 返回一致的结构

```python
# ✅ CONSISTENT: Always list with "json" key
return [{"json": result}]  # Single result
return results  # Multiple results (already formatted)
return []  # No results
```

### 5. 使用 print() 语句调试

```python
# Debug statements appear in browser console (F12)
items = _input.all()
print(f"Processing {len(items)} items")
print(f"First item: {items[0] if items else 'None'}")
```

---

## 何时使用 Python vs JavaScript

### 使用 Python 当：
- ✅ 你需要 `statistics` 模块进行统计操作
- ✅ 你对 Python 语法更加熟悉
- ✅ 你的逻辑适合使用列表推导式
- ✅ 你需要特定的标准库函数

### 使用 JavaScript 当：
- ✅ 你需要 HTTP 请求（$helpers.httpRequest()）
- ✅ 你需要高级日期/时间（DateTime/Luxon）
- ✅ 你想要更好的 n8n 集成
- ✅ **95% 的用例**（推荐）

### 考虑使用其他节点当：
- ❌ 简单字段映射 → 使用 **Set** 节点
- ❌ 基本过滤 → 使用 **Filter** 节点
- ❌ 简单条件 → 使用 **IF** 或 **Switch** 节点
- ❌ 仅 HTTP 请求 → 使用 **HTTP Request** 节点

---

## 与其他技能的集成

### 配合使用：

**n8n 表达式语法**：
- 表达式在其他节点中使用 `{{ }}` 语法
- Code 节点直接使用 Python（无 `{{ }}`）
- 何时使用表达式 vs 代码

**n8n MCP 工具专家**：
- 如何找到 Code 节点：`search_nodes({query: "code"})`
- 获取配置帮助：`get_node_essentials("nodes-base.code")`
- 验证代码：`validate_node_operation()`

**n8n 节点配置**：
- 模式选择（所有项 vs 每项）
- 语言选择（Python vs JavaScript）
- 理解属性依赖

**n8n 工作流模式**：
- 转换步骤中的 Code 节点
- 模式中何时使用 Python vs JavaScript

**n8n 验证专家**：
- 验证 Code 节点配置
- 处理验证错误
- 自动修复常见问题

**n8n Code JavaScript**：
- 何时改用 JavaScript
- JavaScript vs Python 功能对比
- 从 Python 迁移到 JavaScript

---

## 快速参考清单

部署 Python Code 节点前，请验证：

- [ ] **已优先考虑 JavaScript** - 仅在必要时使用 Python
- [ ] **代码不为空** - 必须包含有意义的逻辑
- [ ] **存在返回语句** - 必须返回字典列表
- [ ] **正确的返回格式** - 每项：`{"json": {...}}`
- [ ] **数据访问正确** - 使用 `_input.all()`、`_input.first()` 或 `_input.item`
- [ ] **无外部导入** - 仅标准库（json、datetime、re 等）
- [ ] **安全的字典访问** - 使用 `.get()` 避免 KeyError
- [ ] **Webhook 数据** - 如果来自 Webhook，通过 `["body"]` 访问
- [ ] **模式选择** - 大多数情况下使用"所有项"
- [ ] **输出一致** - 所有代码路径返回相同结构

---

## 附加资源

### 相关文件
- DATA_ACCESS.md - 全面的 Python 数据访问模式
- COMMON_PATTERNS.md - 10 个 n8n Python 模式
- ERROR_PATTERNS.md - 前 5 个错误及解决方案
- STANDARD_LIBRARY.md - 完整的标准库参考

### n8n 文档
- Code Node Guide: https://docs.n8n.io/code/code-node/
- Python in n8n: https://docs.n8n.io/code/builtin/python-modules/

---

**准备在 n8n Code 节点中编写 Python - 但请优先考虑 JavaScript！** 使用 Python 满足特定需求，参考错误模式指南以避免常见错误，并有效利用标准库。

## 限制
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。