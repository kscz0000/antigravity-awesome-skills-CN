---
name: jq
description: "jq 专家级使用，用于 JSON 查询、过滤、转换和管道集成。实战 shell 工作流模式。触发词：jq、JSON查询、JSON过滤、JSON转换、shell管道、JSON处理、jq命令、数据转换"
category: development
risk: safe
source: community
date_added: "2026-03-28"
author: kostakost2
tags: [jq, json, shell, cli, data-transformation, bash]
tools: [claude, cursor, gemini]
---

# jq — JSON 查询与转换

## 概述

``jq` 是用于查询和重塑 JSON 的标准 CLI 工具。本技能涵盖实战专家级用法：过滤深层嵌套数据、转换结构、聚合值，以及将 ``jq`` 组合到 shell 管道中。每个示例都可直接复制用于真实工作流。

## 何时使用本技能

- 解析来自 API、CLI 工具（AWS、GitHub、kubectl、docker）或日志文件的 JSON 输出时使用
- 转换 JSON 结构（重命名键、扁平化数组、分组记录）时使用
- 用户需要在 bash 脚本或单行命令中使用 ``jq`` 时使用
- 解释复杂 ``jq`` 表达式的作用时使用

## 工作原理

``jq`` 接收一个过滤表达式并将其应用于 JSON 输入。过滤器通过管道（``|``）组合，``jq`` 原生处理数组、对象、字符串、数字、布尔值和 ``null``。

### 基础选择

```bash
# 提取字段
echo '{"name":"alice","age":30}' | jq '.name'
# "alice"

# 嵌套访问
echo '{"user":{"email":"a@b.com"}}' | jq '.user.email'

# 数组索引
echo '[10, 20, 30]' | jq '.[1]'
# 20

# 数组切片
echo '[1,2,3,4,5]' | jq '.[2:4]'
# [3, 4]

# 所有数组元素
echo '[{"id":1},{"id":2}]' | jq '.[]'
```

### 使用 ``select`` 过滤

```bash
# 只保留匹配元素
echo '[{"role":"admin"},{"role":"user"},{"role":"admin"}]' \
  | jq '[.[] | select(.role == "admin")]'

# 数值比较
curl -s https://api.github.com/repos/owner/repo/issues \
  | jq '[.[] | select(.comments > 5)]'

# 测试字段存在且非 null
jq '[.[] | select(.email != null)]'

# 组合条件
jq '[.[] | select(.active == true and .score >= 80)]'
```

### 映射与转换

```bash
# 从每个数组元素提取字段
echo '[{"name":"alice","age":30},{"name":"bob","age":25}]' \
  | jq '[.[] | .name]'
# ["alice", "bob"]

# 简写：map()
jq 'map(.name)'

# 为每个元素构建新对象
jq '[.[] | {user: .name, years: .age}]'

# 添加计算字段
jq '[.[] | . + {senior: (.age > 28)}]'

# 重命名键
jq '[.[] | {username: .name, email_address: .email}]'
```

### 聚合与归约

```bash
# 求和所有值
echo '[1, 2, 3, 4, 5]' | jq 'add'
# 15

# 对对象中的字段求和
jq '[.[].price] | add'

# 统计元素数量
jq 'length'

# 最大值 / 最小值
jq 'max_by(.score)'
jq 'min_by(.created_at)'

# reduce：自定义累加器
echo '[1,2,3,4,5]' | jq 'reduce .[] as $x (0; . + $x)'
# 15

# 按字段分组
jq 'group_by(.department)'

# 每组计数
jq 'group_by(.status) | map({status: .[0].status, count: length})'
```

### 字符串插值与格式化

```bash
# 字符串插值
jq -r '.[] | "\(.name) is \(.age) years old"'

# 格式化为 CSV（无表头）
jq -r '.[] | [.name, .age, .email] | @csv'

# 格式化为 TSV
jq -r '.[] | [.name, .score] | @tsv'

# URL 编码
jq -r '.query | @uri'

# Base64 编码
jq -r '.data | @base64'
```

### 操作键与路径

```bash
# 列出所有顶层键
jq 'keys'

# 检查键是否存在
jq 'has("email")'

# 删除键
jq 'del(.password)'

# 从每个元素删除嵌套键
jq '[.[] | del(.internal_id, .raw_payload)]'

# 递归下降：查找树中任意位置的键的所有值
jq '.. | .id? // empty'

# 获取所有叶子路径
jq '[paths(scalars)]'
```

### 条件与错误处理

```bash
# if-then-else
jq 'if .score >= 90 then "A" elif .score >= 80 then "B" else "C" end'

# 替代操作符：当 null 或 false 时使用后备值
jq '.nickname // .name'

# try-catch：跳过错误而非中止
jq '[.[] | try .nested.value catch null]'

# 用 // empty 抑制 null 输出
jq '.[] | .optional_field // empty'
```

### 实战 Shell 集成

```bash
# 从文件读取
jq '.users' data.json

# 紧凑输出（无空白）用于后续管道
jq -c '.[]' records.json | while IFS= read -r record; do
  echo "Processing: $ecord"
done

# 将 shell 变量传入 jq
STATUS="active"
jq --arg s "$STATUS" '[.[] | select(.status == $s)]'

# 传入数字
jq --argjson threshold 42 '[.[] | select(.value > $	hreshold)]'

# 将多行 JSON 摄入为数组
jq -s '.' records.ndjson

# 多个文件：将所有摄入为一个数组
jq -s 'add' file1.json file2.json

# 从命令进行空值安全管道
kubectl get pods -o json | jq '.items[] | {name: .metadata.name, status: .status.phase}'

# GitHub CLI：提取 PR 编号
gh pr list --json number,title | jq -r '.[] | "\(.number)\t\(.title)"'

# AWS CLI：列出运行中的实例 ID
aws ec2 describe-instances \
  | jq -r '.Reservations[].Instances[] | select(.State.Name=="running") | .InstanceId'

# Docker：显示容器名称和镜像
docker inspect $(docker ps -q) | jq -r '.[] | "\(.Name)\t\(.Config.Image)"'
```

### 高级模式

```bash
# 将对象数组转置为对象数组
# 输入：{"names":["a","b"],"scores":[10,20]}
jq '[.names, .scores] | transpose | map({name: .[0], score: .[1]})'

# 扁平化一层
jq 'flatten(1)'

# 按字段去重
jq 'unique_by(.email)'

# 排序、去重并重新索引
jq '[.[] | .name] | unique | sort'

# walk：递归地对每个节点应用转换
jq 'walk(if type == "string" then ascii_downcase else . end)'

# env：在 jq 内读取环境变量
export API_KEY=secret
jq -n 'env.API_KEY'
```

## 最佳实践

- 将 ``jq`` 结果传递给 shell 变量或其他命令时，始终使用 ``-r``（原始输出）以去除 JSON 字符串引号
- 使用 ``--arg`` / ``--argjson`` 安全地注入 shell 变量——切勿将 shell 变量直接插值到过滤字符串中
- 为可读性优先使用 ``map(f)`` 而非 ``[.[] | f]``
- 对换行分隔的 JSON 管道使用 ``-c``（紧凑）；人工调试时省略
- 在嵌入脚本前，使用 ``jq -n`` 和字面输入交互式测试过滤器
- 使用 ``empty`` 丢弃不需要的元素，而非过滤为 ``null``

## 安全与注意事项

- ``jq`` 设计为只读——它无法写入文件或执行命令
- 避免将不可信的 JSON 字段值直接嵌入 shell 命令；始终使用引号或 ``--arg``

## 常见陷阱

- **问题：** ``jq`` 输出 ``null`` 而非预期值
  **解决方案：** 检查键名拼写错误；使用 ``keys`` 检查实际字段名。记住 JSON 区分大小写。

- **问题：** 数字在输出中被引号包裹为字符串
  **解决方案：** 注入数值时使用 ``--argjson`` 而非 ``--arg``。

- **问题：** 过滤器在终端有效但在脚本中失败
  **解决方案：** 确保过滤字符串在 shell 中使用单引号以防止变量展开。示例：``jq '.field'`` 而非 ``jq ".field"``。

- **问题：** ``add`` 对空数组返回 ``null``
  **解决方案：** 使用 ``add // 0`` 或 ``add // ""`` 提供后备默认值。

- **问题：** 流式处理大文件很慢
  **解决方案：** 对非常大的文件使用 ``jq --stream`` 或切换到 ``jstream``/``gron``。

## 相关技能

- ``@bash-pro`` — 在健壮的 shell 脚本中包装 jq 调用
- ``@bash-linux`` — 通用 shell 管道模式
- ``@github-automation`` — 将 jq 与 GitHub CLI JSON 输出配合使用

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
