# 函数参考

## 全局函数

| 函数 | 签名 | 描述 |
|----------|-----------|-------------|
| `date()` | `date(string): date` | 将字符串解析为日期。格式：`YYYY-MM-DD HH:mm:ss` |
| `duration()` | `duration(string): duration` | 解析时长字符串 |
| `now()` | `now(): date` | 当前日期和时间 |
| `today()` | `today(): date` | 当前日期（时间 = 00:00:00） |
| `if()` | `if(condition, trueResult, falseResult?)` | 条件判断 |
| `min()` | `min(n1, n2, ...): number` | 最小值 |
| `max()` | `max(n1, n2, ...): number` | 最大值 |
| `number()` | `number(any): number` | 转换为数字 |
| `link()` | `link(path, display?): Link` | 创建链接 |
| `list()` | `list(element): List` | 若不是列表则包装为列表 |
| `file()` | `file(path): file` | 获取文件对象 |
| `image()` | `image(path): image` | 创建用于渲染的图像 |
| `icon()` | `icon(name): icon` | 按名称获取 Lucide 图标 |
| `html()` | `html(string): html` | 渲染为 HTML |
| `escapeHTML()` | `escapeHTML(string): string` | 转义 HTML 字符 |

## Any 类型函数

| 函数 | 签名 | 描述 |
|----------|-----------|-------------|
| `isTruthy()` | `any.isTruthy(): boolean` | 强制转换为布尔值 |
| `isType()` | `any.isType(type): boolean` | 检查类型 |
| `toString()` | `any.toString(): string` | 转换为字符串 |

## 日期函数与字段

**字段：** `date.year`、`date.month`、`date.day`、`date.hour`、`date.minute`、`date.second`、`date.millisecond`

| 函数 | 签名 | 描述 |
|----------|-----------|-------------|
| `date()` | `date.date(): date` | 移除时间部分 |
| `format()` | `date.format(string): string` | 使用 Moment.js 模式格式化 |
| `time()` | `date.time(): string` | 以字符串形式获取时间 |
| `relative()` | `date.relative(): string` | 人类可读的相对时间 |
| `isEmpty()` | `date.isEmpty(): boolean` | 对日期而言始终为 false |

## Duration 类型

两个日期相减的结果是 **Duration** 类型（不是数字）。Duration 有自己的属性和方法。

**Duration 字段：**
| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `duration.days` | Number | 时长中的总天数 |
| `duration.hours` | Number | 时长中的总小时数 |
| `duration.minutes` | Number | 时长中的总分钟数 |
| `duration.seconds` | Number | 时长中的总秒数 |
| `duration.milliseconds` | Number | 时长中的总毫秒数 |

**重要提示：** Duration 不直接支持 `.round()`、`.floor()`、`.ceil()`。必须先访问数值字段（如 `.days`），然后应用数字函数。

```yaml
# 正确：计算两个日期之间的天数
"(date(due_date) - today()).days"                    # 返回天数
"(now() - file.ctime).days"                          # 自创建以来的天数

# 正确：如需对数值结果四舍五入
"(date(due_date) - today()).days.round(0)"           # 四舍五入后的天数
"(now() - file.ctime).hours.round(0)"                # 四舍五入后的小时数

# 错误 - 将导致错误：
# "((date(due) - today()) / 86400000).round(0)"      # Duration 不支持先除后四舍五入
```

## 日期算术

```yaml
# Duration 单位：y/year/years、M/month/months、d/day/days、
#                w/week/weeks、h/hour/hours、m/minute/minutes、s/second/seconds

# 加/减 Duration
"date + \"1M\""           # 加 1 个月
"date - \"2h\""           # 减 2 小时
"now() + \"1 day\""       # 明天
"today() + \"7d\""        # 距离今天一周

# 日期相减返回 Duration 类型
"now() - file.ctime"                    # 返回 Duration
"(now() - file.ctime).days"             # 以数字形式获取天数
"(now() - file.ctime).hours"            # 以数字形式获取小时数

# 复杂的 Duration 算术
"now() + (duration('1d') * 2)"
```

## 字符串函数

**字段：** `string.length`

| 函数 | 签名 | 描述 |
|----------|-----------|-------------|
| `contains()` | `string.contains(value): boolean` | 检查子字符串 |
| `containsAll()` | `string.containsAll(...values): boolean` | 包含所有子字符串 |
| `containsAny()` | `string.containsAny(...values): boolean` | 包含任一子字符串 |
| `startsWith()` | `string.startsWith(query): boolean` | 以指定字符串开头 |
| `endsWith()` | `string.endsWith(query): boolean` | 以指定字符串结尾 |
| `isEmpty()` | `string.isEmpty(): boolean` | 为空或不存在 |
| `lower()` | `string.lower(): string` | 转为小写 |
| `title()` | `string.title(): string` | 转为标题大小写 |
| `trim()` | `string.trim(): string` | 去除空白字符 |
| `replace()` | `string.replace(pattern, replacement): string` | 替换模式 |
| `repeat()` | `string.repeat(count): string` | 重复字符串 |
| `reverse()` | `string.reverse(): string` | 反转字符串 |
| `slice()` | `string.slice(start, end?): string` | 子字符串 |
| `split()` | `string.split(separator, n?): list` | 拆分为列表 |

## 数字函数

| 函数 | 签名 | 描述 |
|----------|-----------|-------------|
| `abs()` | `number.abs(): number` | 绝对值 |
| `ceil()` | `number.ceil(): number` | 向上取整 |
| `floor()` | `number.floor(): number` | 向下取整 |
| `round()` | `number.round(digits?): number` | 四舍五入到指定位数 |
| `toFixed()` | `number.toFixed(precision): string` | 定点表示法 |
| `isEmpty()` | `number.isEmpty(): boolean` | 不存在 |

## 列表函数

**字段：** `list.length`

| 函数 | 签名 | 描述 |
|----------|-----------|-------------|
| `contains()` | `list.contains(value): boolean` | 元素是否存在 |
| `containsAll()` | `list.containsAll(...values): boolean` | 所有元素都存在 |
| `containsAny()` | `list.containsAny(...values): boolean` | 任一元素存在 |
| `filter()` | `list.filter(expression): list` | 按条件过滤（使用 `value`、`index`） |
| `map()` | `list.map(expression): list` | 转换元素（使用 `value`、`index`） |
| `reduce()` | `list.reduce(expression, initial): any` | 归约为单个值（使用 `value`、`index`、`acc`） |
| `flat()` | `list.flat(): list` | 扁平化嵌套列表 |
| `join()` | `list.join(separator): string` | 连接为字符串 |
| `reverse()` | `list.reverse(): list` | 反转顺序 |
| `slice()` | `list.slice(start, end?): list` | 子列表 |
| `sort()` | `list.sort(): list` | 升序排序 |
| `unique()` | `list.unique(): list` | 去除重复项 |
| `isEmpty()` | `list.isEmpty(): boolean` | 无元素 |

## 文件函数

| 函数 | 签名 | 描述 |
|----------|-----------|-------------|
| `asLink()` | `file.asLink(display?): Link` | 转换为链接 |
| `hasLink()` | `file.hasLink(otherFile): boolean` | 是否链接到指定文件 |
| `hasTag()` | `file.hasTag(...tags): boolean` | 是否拥有任一标签 |
| `hasProperty()` | `file.hasProperty(name): boolean` | 是否拥有指定属性 |
| `inFolder()` | `file.inFolder(folder): boolean` | 位于指定文件夹或其子文件夹 |

## 链接函数

| 函数 | 签名 | 描述 |
|----------|-----------|-------------|
| `asFile()` | `link.asFile(): file` | 获取文件对象 |
| `linksTo()` | `link.linksTo(file): boolean` | 是否链接到指定文件 |

## 对象函数

| 函数 | 签名 | 描述 |
|----------|-----------|-------------|
| `isEmpty()` | `object.isEmpty(): boolean` | 无属性 |
| `keys()` | `object.keys(): list` | 键的列表 |
| `values()` | `object.values(): list` | 值的列表 |

## 正则表达式函数

| 函数 | 签名 | 描述 |
|----------|-----------|-------------|
| `matches()` | `regexp.matches(string): boolean` | 测试是否匹配 |
