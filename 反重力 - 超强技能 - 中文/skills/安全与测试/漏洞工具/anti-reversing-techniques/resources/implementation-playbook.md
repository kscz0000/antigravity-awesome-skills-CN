# 反逆向技术实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

# 反逆向技术

理解在授权软件分析、安全研究和恶意软件分析过程中遇到的保护机制。这些知识帮助分析师绕过保护以完成合法分析任务。

## 反调试技术

### Windows 反调试

#### 基于API的检测

```c
// IsDebuggerPresent
if (IsDebuggerPresent()) {
    exit(1);
}

// CheckRemoteDebuggerPresent
BOOL debugged = FALSE;
CheckRemoteDebuggerPresent(GetCurrentProcess(), &debugged);
if (debugged) exit(1);

// NtQueryInformationProcess
typedef NTSTATUS (NTAPI *pNtQueryInformationProcess)(
    HANDLE, PROCESSINFOCLASS, PVOID, ULONG, PULONG);

DWORD debugPort = 0;
NtQueryInformationProcess(
    GetCurrentProcess(),
    ProcessDebugPort,        // 7
    &debugPort,
    sizeof(debugPort),
    NULL
);
if (debugPort != 0) exit(1);

// Debug flags
DWORD debugFlags = 0;
NtQueryInformationProcess(
    GetCurrentProcess(),
    ProcessDebugFlags,       // 0x1F
    &debugFlags,
    sizeof(debugFlags),
    NULL
);
if (debugFlags == 0) exit(1);  // 0 表示正在被调试
```

**绕过方法：**
```python
# x64dbg: ScyllaHide 插件
# 修补常见的反调试检查

# 在调试器中手动修补：
# - 将 IsDebuggerPresent 返回值设为 0
# - 将 PEB.BeingDebugged 修补为 0
# - Hook NtQueryInformationProcess

# IDAPython: 修补检查
ida_bytes.patch_byte(check_addr, 0x90)  # NOP
```

#### 基于PEB的检测

```c
// 直接 PEB 访问
#ifdef _WIN64
    PPEB peb = (PPEB)__readgsqword(0x60);
#else
    PPEB peb = (PPEB)__readfsdword(0x30);
#endif

// BeingDebugged 标志
if (peb->BeingDebugged) exit(1);

// NtGlobalFlag
// 被调试时: 0x70 (FLG_HEAP_ENABLE_TAIL_CHECK |
//                 FLG_HEAP_ENABLE_FREE_CHECK |
//                 FLG_HEAP_VALIDATE_PARAMETERS)
if (peb->NtGlobalFlag & 0x70) exit(1);

// 堆标志
PDWORD heapFlags = (PDWORD)((PBYTE)peb->ProcessHeap + 0x70);
if (*heapFlags & 0x50000062) exit(1);
```

**绕过方法：**
```assembly
; 在调试器中直接修改 PEB
; x64dbg: dump at gs:[60] (x64) 或 fs:[30] (x86)
; 将 BeingDebugged (偏移 2) 设为 0
; 清除 NtGlobalFlag (x64 偏移 0xBC)
```

#### 基于时间的检测

```c
// RDTSC 计时
uint64_t start = __rdtsc();
// ... 一些代码 ...
uint64_t end = __rdtsc();
if ((end - start) > THRESHOLD) exit(1);

// QueryPerformanceCounter
LARGE_INTEGER start, end, freq;
QueryPerformanceFrequency(&freq);
QueryPerformanceCounter(&start);
// ... 代码 ...
QueryPerformanceCounter(&end);
double elapsed = (double)(end.QuadPart - start.QuadPart) / freq.QuadPart;
if (elapsed > 0.1) exit(1);  // 太慢 = 有调试器

// GetTickCount
DWORD start = GetTickCount();
// ... 代码 ...
if (GetTickCount() - start > 1000) exit(1);
```

**绕过方法：**
```
- 使用硬件断点而非软件断点
- 修补时间检查
- 使用时间受控的虚拟机
- Hook 时间 API 返回一致的值
```

#### 基于异常的检测

```c
// 基于 SEH 的检测
__try {
    __asm { int 3 }  // 软件断点
}
__except(EXCEPTION_EXECUTE_HANDLER) {
    // 正常执行: 异常被捕获
    return;
}
// 调试器吞掉了异常
exit(1);

// 基于 VEH 的检测
LONG CALLBACK VectoredHandler(PEXCEPTION_POINTERS ep) {
    if (ep->ExceptionRecord->ExceptionCode == EXCEPTION_BREAKPOINT) {
        ep->ContextRecord->Rip++;  // 跳过 INT3
        return EXCEPTION_CONTINUE_EXECUTION;
    }
    return EXCEPTION_CONTINUE_SEARCH;
}
```

### Linux 反调试

```c
// ptrace 自跟踪
if (ptrace(PTRACE_TRACEME, 0, NULL, NULL) == -1) {
    // 已被跟踪
    exit(1);
}

// /proc/self/status
FILE *f = fopen("/proc/self/status", "r");
char line[256];
while (fgets(line, sizeof(line), f)) {
    if (strncmp(line, "TracerPid:", 10) == 0) {
        int tracer_pid = atoi(line + 10);
        if (tracer_pid != 0) exit(1);
    }
}

// 父进程检查
if (getppid() != 1 && strcmp(get_process_name(getppid()), "bash") != 0) {
    // 异常父进程（可能是调试器）
}
```

**绕过方法：**
```bash
# LD_PRELOAD 来 hook ptrace
# 编译: gcc -shared -fPIC -o hook.so hook.c
long ptrace(int request, ...) {
    return 0;  // 总是成功
}

# 使用方法
LD_PRELOAD=./hook.so ./target
```

## 反虚拟机检测

### 硬件指纹识别

```c
// 基于 CPUID 的检测
int cpuid_info[4];
__cpuid(cpuid_info, 1);
// 检查虚拟机位 (ECX 的第 31 位)
if (cpuid_info[2] & (1 << 31)) {
    // 在虚拟机中运行
}

// CPUID 品牌字符串
__cpuid(cpuid_info, 0x40000000);
char vendor[13] = {0};
memcpy(vendor, &cpuid_info[1], 12);
// "VMwareVMware", "Microsoft Hv", "KVMKVMKVM", "VBoxVBoxVBox"

// MAC 地址前缀
// VMware: 00:0C:29, 00:50:56
// VirtualBox: 08:00:27
// Hyper-V: 00:15:5D
```

### 注册表/文件检测

```c
// Windows 注册表键
// HKLM\SOFTWARE\VMware, Inc.\VMware Tools
// HKLM\SOFTWARE\Oracle\VirtualBox Guest Additions
// HKLM\HARDWARE\ACPI\DSDT\VBOX__

// 文件
// C:\Windows\System32\drivers\vmmouse.sys
// C:\Windows\System32\drivers\vmhgfs.sys
// C:\Windows\System32\drivers\VBoxMouse.sys

// 进程
// vmtoolsd.exe, vmwaretray.exe
// VBoxService.exe, VBoxTray.exe
```

### 基于时间的虚拟机检测

```c
// VM 退出导致时间异常
uint64_t start = __rdtsc();
__cpuid(cpuid_info, 0);  // 导致 VM 退出
uint64_t end = __rdtsc();
if ((end - start) > 500) {
    // 可能在虚拟机中 (CPUID 耗时更长)
}
```

**绕过方法：**
```
- 使用物理机分析环境
- 加固虚拟机（移除客户机工具、更改 MAC）
- 修补检测代码
- 使用专用分析虚拟机 (FLARE-VM)
```

## 代码混淆

### 控制流混淆

#### 控制流平坦化

```c
// 原始代码
if (cond) {
    func_a();
} else {
    func_b();
}
func_c();

// 平坦化后
int state = 0;
while (1) {
    switch (state) {
        case 0:
            state = cond ? 1 : 2;
            break;
        case 1:
            func_a();
            state = 3;
            break;
        case 2:
            func_b();
            state = 3;
            break;
        case 3:
            func_c();
            return;
    }
}
```

**分析方法：**
- 识别状态变量
- 映射状态转换
- 重建原始流程
- 工具：D-810 (IDA)、SATURN

#### 不透明谓词

```c
// 总是为真，但分析复杂
int x = rand();
if ((x * x) >= 0) {  // 总是为真
    real_code();
} else {
    junk_code();  // 死代码
}

// 总是为假
if ((x * (x + 1)) % 2 == 1) {  // 连续数乘积 = 偶数
    junk_code();
}
```

**分析方法：**
- 识别常量表达式
- 使用符号执行证明谓词
- 模式匹配已知的不透明谓词

### 数据混淆

#### 字符串加密

```c
// XOR 加密
char decrypt_string(char *enc, int len, char key) {
    char *dec = malloc(len + 1);
    for (int i = 0; i < len; i++) {
        dec[i] = enc[i] ^ key;
    }
    dec[len] = 0;
    return dec;
}

// 栈字符串
char url[20];
url[0] = 'h'; url[1] = 't'; url[2] = 't'; url[3] = 'p';
url[4] = ':'; url[5] = '/'; url[6] = '/';
// ...
```

**分析方法：**
```python
# FLOSS 自动字符串解混淆
floss malware.exe

# IDAPython 字符串解密
def decrypt_xor(ea, length, key):
    result = ""
    for i in range(length):
        byte = ida_bytes.get_byte(ea + i)
        result += chr(byte ^ key)
    return result
```

#### API 混淆

```c
// 动态 API 解析
typedef HANDLE (WINAPI *pCreateFileW)(LPCWSTR, DWORD, DWORD,
    LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE);

HMODULE kernel32 = LoadLibraryA("kernel32.dll");
pCreateFileW myCreateFile = (pCreateFileW)GetProcAddress(
    kernel32, "CreateFileW");

// API 哈希
DWORD hash_api(char *name) {
    DWORD hash = 0;
    while (*name) {
        hash = ((hash >> 13) | (hash << 19)) + *name++;
    }
    return hash;
}
// 通过哈希比较而非字符串来解析
```

**分析方法：**
- 识别哈希算法
- 构建已知 API 的哈希数据库
- 使用 IDA 的 HashDB 插件
- 动态分析在运行时解析

### 指令级混淆

#### 死代码插入

```asm
; 原始代码
mov eax, 1

; 插入死代码后
push ebx           ; 死代码
mov eax, 1
pop ebx            ; 死代码
xor ecx, ecx       ; 死代码
add ecx, ecx       ; 死代码
```

#### 指令替换

```asm
; 原始: xor eax, eax (设为 0)
; 替换形式:
sub eax, eax
mov eax, 0
and eax, 0
lea eax, [0]

; 原始: mov eax, 1
; 替换形式:
xor eax, eax
inc eax

push 1
pop eax
```

## 加壳和加密

### 常见加壳工具

```
UPX          - 开源，易于脱壳
Themida      - 商业，基于虚拟机的保护
VMProtect    - 商业，代码虚拟化
ASPack       - 压缩壳
PECompact    - 压缩壳
Enigma       - 商业保护器
```

### 脱壳方法论

```
1. 识别加壳工具 (DIE, Exeinfo PE, PEiD)

2. 静态脱壳（如果是已知壳）：
   - UPX: upx -d packed.exe
   - 使用现有脱壳工具

3. 动态脱壳：
   a. 找到原始入口点 (OEP)
   b. 在 OEP 设置断点
   c. 到达 OEP 时转储内存
   d. 修复导入表 (Scylla, ImpREC)

4. OEP 查找技术：
   - 在栈上设置硬件断点 (ESP 技巧)
   - 在常见 API 调用上断点 (GetCommandLineA)
   - 跟踪并寻找典型入口模式
```

### 手动脱壳示例

```
1. 在 x64dbg 中加载加壳二进制文件
2. 记录入口点（壳桩）
3. 使用 ESP 技巧：
   - 运行到入口
   - 在 [ESP] 设置硬件断点
   - 运行直到断点命中（PUSHAD/POPAD 之后）
4. 寻找跳转到 OEP 的 JMP 指令
5. 在 OEP 处，使用 Scylla：
   - 转储进程
   - 查找导入 (IAT 自动搜索)
   - 修复转储
```

## 基于虚拟化的保护

### 代码虚拟化

```
原始 x86 代码被转换为自定义字节码，
在运行时由嵌入式虚拟机解释执行。

原始代码:     虚拟机保护后:
mov eax, 1    push vm_context
add eax, 2    call vm_entry
              ; 虚拟机解释字节码
              ; 等效于原始代码
```

### 分析方法

```
1. 识别虚拟机组件：
   - 虚拟机入口（调度器）
   - 处理程序表
   - 字节码位置
   - 虚拟寄存器/栈

2. 跟踪执行：
   - 记录处理程序调用
   - 映射字节码到操作
   - 理解指令集

3. 提升和去虚拟化：
   - 将虚拟机指令映射回原生指令
   - 工具：VMAttack、SATURN、NoVmp

4. 符号执行：
   - 语义分析虚拟机
   - angr、Triton
```

## 绕过策略总结

### 通用原则

1. **理解保护机制**：识别使用了什么技术
2. **定位检查点**：在二进制文件中找到保护代码
3. **修补或 Hook**：修改检查使其总是通过
4. **使用合适的工具**：ScyllaHide、x64dbg 插件
5. **记录发现**：保留绕过保护的笔记

### 工具推荐

```
反调试绕过:    ScyllaHide, TitanHide
脱壳:         x64dbg + Scylla, OllyDumpEx
去混淆:       D-810, SATURN, miasm
虚拟机分析:    VMAttack, NoVmp, 手动跟踪
字符串解密:    FLOSS, 自定义脚本
符号执行:     angr, Triton
```

### 伦理考量

这些知识仅应用于：
- 授权的安全研究
- 恶意软件分析（防御性）
- CTF 竞赛
- 为合法目的理解保护机制
- 教育目的

绝不应用于：
- 软件盗版
- 未授权访问
- 恶意目的
