---
name: c
description: "C 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# C：惯用效率参考

## 目录
1. [内存管理](#memory)
2. [指针与数组](#pointers)
3. [错误处理](#errors)
4. [字符串](#strings)
5. [结构体与枚举](#structs)
6. [预处理器与头文件](#preprocessor)
7. [C 特有反模式](#antipatterns)

---

## 1. 内存管理 {#memory}

```c
// ❌ malloc 不检查返回值
char *buf = malloc(size);
strcpy(buf, src);

// ✅
char *buf = malloc(size);
if (!buf) return -ENOMEM;
memcpy(buf, src, size);
```

```c
// ❌ 转换 malloc 返回值（C 中不必要，隐藏了缺失的 #include）
int *p = (int *)malloc(n * sizeof(int));

// ✅
int *p = malloc(n * sizeof *p);
```

```c
// ❌ free 后未置空（长生命周期作用域中的悬垂指针风险）
free(ptr);
// ... 后续代码可能使用 ptr

// ✅
free(ptr);
ptr = NULL;
```

```c
// ❌ 忘记在提前返回路径上释放
char *a = malloc(100);
char *b = malloc(200);
if (!b) return -1; // 泄漏 a

// ✅ — 单一清理标签
char *a = NULL, *b = NULL;
a = malloc(100);
if (!a) goto cleanup;
b = malloc(200);
if (!b) goto cleanup;
// ... 使用 a, b ...
cleanup:
    free(b);
    free(a);
```

**使用 `sizeof *ptr` 而非 `sizeof(Type)`——类型变更时仍然正确。**

---

## 2. 指针与数组 {#pointers}

```c
// ❌ 手动跟踪数组大小
void process(int *arr, int len) { ... }
process(data, 10);

// ✅ — 指针旁传递大小，或使用结构体
typedef struct { int *data; size_t len; } IntSlice;
```

```c
// ❌ 指针算术在数组索引更清晰时
*(arr + i) = value;

// ✅
arr[i] = value;
```

```c
// ❌ 生产代码中使用 VLA（栈溢出风险，C11+ 中可选）
int arr[n];

// ✅
int *arr = malloc(n * sizeof *arr);
if (!arr) return -ENOMEM;
// ... 使用 arr ...
free(arr);
```

---

## 3. 错误处理 {#errors}

```c
// ❌ 使用魔术数字做错误返回
if (do_thing() == -1) { ... }

// ✅ — 定义或使用命名错误码
#include <errno.h>
if (do_thing() < 0) {
    perror("do_thing");
    return errno;
}
```

```c
// ❌ 深层嵌套的错误检查
int r1 = step1();
if (r1 == 0) {
    int r2 = step2();
    if (r2 == 0) {
        int r3 = step3();
        // ...
    }
}

// ✅ — 提前返回 / goto cleanup
if (step1() < 0) goto fail;
if (step2() < 0) goto fail;
if (step3() < 0) goto fail;
return 0;
fail:
    cleanup();
    return -1;
```

**`goto cleanup` 是 C 中资源释放的惯用写法——不要出于教条而回避它。**

---

## 4. 字符串 {#strings}

```c
// ❌ strcpy 不做边界检查
strcpy(dest, src);

// ✅
strncpy(dest, src, sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';
// 或更好：snprintf(dest, sizeof(dest), "%s", src);
```

```c
// ❌ strcmp 误用
if (str == "hello") { ... } // 比较指针，非内容

// ✅
if (strcmp(str, "hello") == 0) { ... }
```

```c
// ❌ 用重复 strcat 构建字符串（O(n²)）
char result[1024] = "";
for (int i = 0; i < n; i++) {
    strcat(result, items[i]);
}

// ✅ — 跟踪写入位置
char result[1024];
int pos = 0;
for (int i = 0; i < n && pos < (int)sizeof(result); i++) {
    pos += snprintf(result + pos, sizeof(result) - pos, "%s", items[i]);
}
```

**始终优先用 `snprintf` 而非 `sprintf`。**

---

## 5. 结构体与枚举 {#structs}

```c
// ❌ 裸结构体到处需要 `struct` 关键字
struct point { int x, y; };
struct point p = {1, 2};

// ✅
typedef struct { int x, y; } Point;
Point p = {1, 2};
```

```c
// ❌ 未初始化的结构体
Point p;
use(p.x); // 未定义行为

// ✅
Point p = {0};
```

```c
// ❌ 魔术整数常量
if (state == 3) { ... }

// ✅
typedef enum { STATE_IDLE, STATE_RUNNING, STATE_DONE } State;
if (state == STATE_DONE) { ... }
```

---

## 6. 预处理器与头文件 {#preprocessor}

```c
// ❌ 宏在 inline 函数可用时使用（无类型安全，双重求值）
#define MAX(a, b) ((a) > (b) ? (a) : (b))
MAX(x++, y) // 若 x > y，x 被自增两次

// ✅
static inline int max_int(int a, int b) { return a > b ? a : b; }
```

```c
// ❌ 无包含守卫
// my_header.h
struct Foo { int x; };

// ✅
#ifndef MY_HEADER_H
#define MY_HEADER_H
struct Foo { int x; };
#endif
// 或：#pragma once（广泛支持，非标准）
```

**宏仅用于条件编译和常量。逻辑用 `static inline`。**

---

## 7. C 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| `sprintf` | `snprintf` 带缓冲区大小 |
| `gets` | `fgets`（gets 在 C11 中已移除） |
| 转换 `malloc` 返回值 | 让隐式 `void*` 转换生效 |
| malloc 中用 `sizeof(Type)` | `sizeof *ptr` |
| 大/运行时数组用 VLA | 堆分配 |
| `void*` 回调无上下文参数 | 传递 `void *ctx` 与函数指针一同 |
| 全局可变状态 | 通过结构体指针传递状态 |
| `assert` 用于运行时错误处理 | 正确的错误返回码 |
| 只读指针参数缺少 `const` | `const char *str` |
| 比较中混用有符号/无符号 | 使用一致类型，显式转换 |



## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。