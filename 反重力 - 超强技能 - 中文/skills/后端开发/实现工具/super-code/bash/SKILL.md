---
name: bash
description: "Bash 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# Bash / Shell：惯用效率参考

## 目录
1. [引号与分词](#quoting)
2. [条件判断与测试](#conditionals)
3. [循环与迭代](#loops)
4. [管道与进程替换](#pipes)
5. [函数与返回值](#functions)
6. [错误处理](#errors)
7. [Bash 特有反模式](#antipatterns)

---

## 1. 引号与分词 {#quoting}

```bash
# ❌ 未加引号的变量（分词 + 通配符展开）
for f in $files; do rm $f; done

# ✅
for f in "${files[@]}"; do rm -- "$f"; done
```

```bash
# ❌ 未加引号的命令替换
path=$(find . -name config)
cat $path  # 含空格时出错

# ✅
path="$(find . -name config)"
cat "$path"
```

```bash
# ❌ 使用反引号做命令替换
result=`echo hello`

# ✅ — $() 可干净地嵌套
result=$(echo hello)
```

```bash
# ❌ 字符串比较不加引号
if [ $var = "hello" ]; then  # var 为空或含空格时出错

# ✅
if [[ "$var" = "hello" ]]; then
```

**规则：给每个 `$variable` 和 `$(command)` 加双引号，除非你明确需要分词。**

---

## 2. 条件判断与测试 {#conditionals}

```bash
# ❌ 单方括号测试（兼容 POSIX 但脆弱）
if [ -f "$file" -a -r "$file" ]; then

# ✅ — [[ 更安全，支持 &&/||，内部不进行分词
if [[ -f "$file" && -r "$file" ]]; then
```

```bash
# ❌ 用 if [ $? -eq 0 ] 测试命令退出状态
grep -q pattern file
if [ $? -eq 0 ]; then echo "found"; fi

# ✅ — 直接测试命令
if grep -q pattern file; then echo "found"; fi
```

```bash
# ❌ 在 [[ 外用 == 做字符串相等
if [ "$a" == "$b" ]; then  # == 在 [ ] 中非 POSIX

# ✅
if [[ "$a" == "$b" ]]; then  # Bash
# 或 POSIX：
if [ "$a" = "$b" ]; then
```

```bash
# ❌ 用 [ ] 和字符串比较做算术
if [ "$count" -gt 10 ]; then

# ✅ — (( )) 用于算术
if (( count > 10 )); then
```

---

## 3. 循环与迭代 {#loops}

```bash
# ❌ 解析 ls 输出
for f in $(ls *.txt); do process "$f"; done

# ✅ — 直接用通配符
for f in *.txt; do
    [[ -e "$f" ]] || continue  # 处理无匹配
    process "$f"
done
```

```bash
# ❌ 用 for 逐行读取文件
for line in $(cat file.txt); do  # 按词分割，非按行

# ✅
while IFS= read -r line; do
    process "$line"
done < file.txt
```

```bash
# ❌ 用 seq 计数
for i in $(seq 1 10); do

# ✅ — 花括号展开（Bash）
for i in {1..10}; do
# 或 C 风格：
for (( i = 1; i <= 10; i++ )); do
```

```bash
# ❌ 通过管道逐行处理命令输出（子 shell 陷阱）
count=0
cat file.txt | while read -r line; do
    (( count++ ))  # 循环后 count 重置——子 shell
done
echo "$count"  # 始终为 0

# ✅ — 重定向，而非管道
count=0
while IFS= read -r line; do
    (( count++ ))
done < file.txt
echo "$count"
```

---

## 4. 管道与进程替换 {#pipes}

```bash
# ❌ 链式 grep | grep 做 AND
grep "error" log.txt | grep "timeout"

# ✅ — 单次 grep 搭配模式
grep -E "error.*timeout|timeout.*error" log.txt
# 或 awk 处理复杂逻辑：
awk '/error/ && /timeout/' log.txt
```

```bash
# ❌ cat + 管道（UUOC — 无用使用 cat）
cat file.txt | grep pattern

# ✅
grep pattern file.txt
```

```bash
# ❌ 用临时文件比较两个命令的输出
cmd1 > /tmp/a.txt
cmd2 > /tmp/b.txt
diff /tmp/a.txt /tmp/b.txt
rm /tmp/a.txt /tmp/b.txt

# ✅ — 进程替换
diff <(cmd1) <(cmd2)
```

```bash
# ❌ 忽略管道失败（只取最后一个命令的退出码）
false | true
echo $?  # 0 — false 的失败被隐藏

# ✅
set -o pipefail
false | true
echo $?  # 1
```

---

## 5. 函数与返回值 {#functions}

```bash
# ❌ 用 return 返回字符串
get_name() {
    return "Alice"  # return 用于退出码 (0-255)
}

# ✅ — echo + 捕获
get_name() {
    echo "Alice"
}
name=$(get_name)
```

```bash
# ❌ 在函数内修改全局变量
result=""
compute() { result="done"; }

# ✅ — 使用 local，通过 stdout 返回
compute() {
    local tmp
    tmp=$(do_work)
    echo "$tmp"
}
result=$(compute)
```

```bash
# ❌ function 关键字（非 POSIX）
function my_func {

# ✅
my_func() {
```

---

## 6. 错误处理 {#errors}

```bash
# ❌ 无错误处理——失败后脚本继续执行
cd /some/dir
rm -rf *  # 如果 cd 失败，从错误目录删除

# ✅
set -euo pipefail

cd /some/dir || { echo "cd failed" >&2; exit 1; }
rm -rf ./*
```

```bash
# ❌ 退出时无清理
tmpfile=$(mktemp)
# ... 脚本可能提前退出，留下 tmpfile

# ✅ — 用 trap 清理
tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"' EXIT
```

```bash
# ❌ 盲目静默错误
command 2>/dev/null

# ✅ — 只在明确知道要抑制什么时才重定向
command 2>/dev/null || true  # 显式：我们预期并接受失败
```

**每个脚本以 `set -euo pipefail` 开头。按需选择性地移除。**

---

## 7. Bash 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| 解析 `ls` 输出 | 通配符：`for f in *.txt` |
| `cat file \| grep` | `grep pattern file` |
| 未加引号的 `$var` | 始终 `"$var"` |
| `[ ]` 做复杂测试 | `[[ ]]` |
| 反引号替换 | `$(command)` |
| 命令后用 `$?` 检查 | `if command; then` |
| `echo` 做调试输出 | `printf '%s\n'`（可移植） |
| 无 `set -euo pipefail` | 始终在脚本顶部设置 |
| 临时文件无清理 | `trap 'rm -f "$tmp"' EXIT` |
| 对用户输入用 `eval` | 避免；用数组构建动态命令 |
| `#!/bin/sh` 却用 Bash 特性 | `#!/usr/bin/env bash` |
| 字符串数学 `expr 1 + 1` | `$(( 1 + 1 ))` |
| `test -z` 做数字比较 | `(( ))` 用于算术 |



## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。