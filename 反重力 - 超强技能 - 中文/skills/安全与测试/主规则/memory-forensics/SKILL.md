---
name: memory-forensics
description: "内存取证综合技术——获取、分析和提取内存转储中的痕迹，用于应急响应和恶意软件分析。当用户要求'内存取证'、'内存分析'、'memory forensics'、'Volatility'、'内存转储分析'、'进程注入检测'、'rootkit检测'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Memory Forensics

内存取证综合技术——获取、分析和提取内存转储中的痕迹，用于应急响应和恶意软件分析。

## 何时使用此技能

- 执行内存取证任务或工作流
- 需要内存取证的指导、最佳实践或检查清单

## 何时不使用此技能

- 任务与内存取证无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入
- 应用相关最佳实践并验证结果
- 提供可操作的步骤和验证方法
- 如需详细示例，打开 `resources/implementation-playbook.md`

## 内存获取

### 在线获取工具

#### Windows
```powershell
# WinPmem (Recommended)
winpmem_mini_x64.exe memory.raw

# DumpIt
DumpIt.exe

# Belkasoft RAM Capturer
# GUI-based, outputs raw format

# Magnet RAM Capture
# GUI-based, outputs raw format
```

#### Linux
```bash
# LiME (Linux Memory Extractor)
sudo insmod lime.ko "path=/tmp/memory.lime format=lime"

# /dev/mem (limited, requires permissions)
sudo dd if=/dev/mem of=memory.raw bs=1M

# /proc/kcore (ELF format)
sudo cp /proc/kcore memory.elf
```

#### macOS
```bash
# osxpmem
sudo ./osxpmem -o memory.raw

# MacQuisition (commercial)
```

### 虚拟机内存

```bash
# VMware: .vmem file is raw memory
cp vm.vmem memory.raw

# VirtualBox: Use debug console
vboxmanage debugvm "VMName" dumpvmcore --filename memory.elf

# QEMU
virsh dump <domain> memory.raw --memory-only

# Hyper-V
# Checkpoint contains memory state
```

## Volatility 3 框架

### 安装与配置

```bash
# Install Volatility 3
pip install volatility3

# Install symbol tables (Windows)
# Download from https://downloads.volatilityfoundation.org/volatility3/symbols/

# Basic usage
vol -f memory.raw <plugin>

# With symbol path
vol -f memory.raw -s /path/to/symbols windows.pslist
```

### 核心插件

#### 进程分析
```bash
# List processes
vol -f memory.raw windows.pslist

# Process tree (parent-child relationships)
vol -f memory.raw windows.pstree

# Hidden process detection
vol -f memory.raw windows.psscan

# Process memory dumps
vol -f memory.raw windows.memmap --pid <PID> --dump

# Process environment variables
vol -f memory.raw windows.envars --pid <PID>

# Command line arguments
vol -f memory.raw windows.cmdline
```

#### 网络分析
```bash
# Network connections
vol -f memory.raw windows.netscan

# Network connection state
vol -f memory.raw windows.netstat
```

#### DLL 与模块分析
```bash
# Loaded DLLs per process
vol -f memory.raw windows.dlllist --pid <PID>

# Find hidden/injected DLLs
vol -f memory.raw windows.ldrmodules

# Kernel modules
vol -f memory.raw windows.modules

# Module dumps
vol -f memory.raw windows.moddump --pid <PID>
```

#### 内存注入检测
```bash
# Detect code injection
vol -f memory.raw windows.malfind

# VAD (Virtual Address Descriptor) analysis
vol -f memory.raw windows.vadinfo --pid <PID>

# Dump suspicious memory regions
vol -f memory.raw windows.vadyarascan --yara-rules rules.yar
```

#### 注册表分析
```bash
# List registry hives
vol -f memory.raw windows.registry.hivelist

# Print registry key
vol -f memory.raw windows.registry.printkey --key "Software\Microsoft\Windows\CurrentVersion\Run"

# Dump registry hive
vol -f memory.raw windows.registry.hivescan --dump
```

#### 文件系统痕迹
```bash
# Scan for file objects
vol -f memory.raw windows.filescan

# Dump files from memory
vol -f memory.raw windows.dumpfiles --pid <PID>

# MFT analysis
vol -f memory.raw windows.mftscan
```

### Linux 分析

```bash
# Process listing
vol -f memory.raw linux.pslist

# Process tree
vol -f memory.raw linux.pstree

# Bash history
vol -f memory.raw linux.bash

# Network connections
vol -f memory.raw linux.sockstat

# Loaded kernel modules
vol -f memory.raw linux.lsmod

# Mount points
vol -f memory.raw linux.mount

# Environment variables
vol -f memory.raw linux.envars
```

### macOS 分析

```bash
# Process listing
vol -f memory.raw mac.pslist

# Process tree
vol -f memory.raw mac.pstree

# Network connections
vol -f memory.raw mac.netstat

# Kernel extensions
vol -f memory.raw mac.lsmod
```

## 分析工作流

### 恶意软件分析工作流

```bash
# 1. Initial process survey
vol -f memory.raw windows.pstree > processes.txt
vol -f memory.raw windows.pslist > pslist.txt

# 2. Network connections
vol -f memory.raw windows.netscan > network.txt

# 3. Detect injection
vol -f memory.raw windows.malfind > malfind.txt

# 4. Analyze suspicious processes
vol -f memory.raw windows.dlllist --pid <PID>
vol -f memory.raw windows.handles --pid <PID>

# 5. Dump suspicious executables
vol -f memory.raw windows.pslist --pid <PID> --dump

# 6. Extract strings from dumps
strings -a pid.<PID>.exe > strings.txt

# 7. YARA scanning
vol -f memory.raw windows.yarascan --yara-rules malware.yar
```

### 应急响应工作流

```bash
# 1. Timeline of events
vol -f memory.raw windows.timeliner > timeline.csv

# 2. User activity
vol -f memory.raw windows.cmdline
vol -f memory.raw windows.consoles

# 3. Persistence mechanisms
vol -f memory.raw windows.registry.printkey \
    --key "Software\Microsoft\Windows\CurrentVersion\Run"

# 4. Services
vol -f memory.raw windows.svcscan

# 5. Scheduled tasks
vol -f memory.raw windows.scheduled_tasks

# 6. Recent files
vol -f memory.raw windows.filescan | grep -i "recent"
```

## 数据结构

### Windows 进程结构

```c
// EPROCESS (Executive Process)
typedef struct _EPROCESS {
    KPROCESS Pcb;                    // Kernel process block
    EX_PUSH_LOCK ProcessLock;
    LARGE_INTEGER CreateTime;
    LARGE_INTEGER ExitTime;
    // ...
    LIST_ENTRY ActiveProcessLinks;   // Doubly-linked list
    ULONG_PTR UniqueProcessId;       // PID
    // ...
    PEB* Peb;                        // Process Environment Block
    // ...
} EPROCESS;

// PEB (Process Environment Block)
typedef struct _PEB {
    BOOLEAN InheritedAddressSpace;
    BOOLEAN ReadImageFileExecOptions;
    BOOLEAN BeingDebugged;           // Anti-debug check
    // ...
    PVOID ImageBaseAddress;          // Base address of executable
    PPEB_LDR_DATA Ldr;              // Loader data (DLL list)
    PRTL_USER_PROCESS_PARAMETERS ProcessParameters;
    // ...
} PEB;
```

### VAD（虚拟地址描述符）

```c
typedef struct _MMVAD {
    MMVAD_SHORT Core;
    union {
        ULONG LongFlags;
        MMVAD_FLAGS VadFlags;
    } u;
    // ...
    PVOID FirstPrototypePte;
    PVOID LastContiguousPte;
    // ...
    PFILE_OBJECT FileObject;
} MMVAD;

// Memory protection flags
#define PAGE_EXECUTE           0x10
#define PAGE_EXECUTE_READ      0x20
#define PAGE_EXECUTE_READWRITE 0x40
#define PAGE_EXECUTE_WRITECOPY 0x80
```

## 检测模式

### 进程注入指标

```python
# Malfind indicators
# - PAGE_EXECUTE_READWRITE protection (suspicious)
# - MZ header in non-image VAD region
# - Shellcode patterns at allocation start

# Common injection techniques
# 1. Classic DLL Injection
#    - VirtualAllocEx + WriteProcessMemory + CreateRemoteThread

# 2. Process Hollowing
#    - CreateProcess (SUSPENDED) + NtUnmapViewOfSection + WriteProcessMemory

# 3. APC Injection
#    - QueueUserAPC targeting alertable threads

# 4. Thread Execution Hijacking
#    - SuspendThread + SetThreadContext + ResumeThread
```

### Rootkit 检测

```bash
# Compare process lists
vol -f memory.raw windows.pslist > pslist.txt
vol -f memory.raw windows.psscan > psscan.txt
diff pslist.txt psscan.txt  # Hidden processes

# Check for DKOM (Direct Kernel Object Manipulation)
vol -f memory.raw windows.callbacks

# Detect hooked functions
vol -f memory.raw windows.ssdt  # System Service Descriptor Table

# Driver analysis
vol -f memory.raw windows.driverscan
vol -f memory.raw windows.driverirp
```

### 凭据提取

```bash
# Dump hashes (requires hivelist first)
vol -f memory.raw windows.hashdump

# LSA secrets
vol -f memory.raw windows.lsadump

# Cached domain credentials
vol -f memory.raw windows.cachedump

# Mimikatz-style extraction
# Requires specific plugins/tools
```

## YARA 集成

### 编写内存 YARA 规则

```yara
rule Suspicious_Injection
{
    meta:
        description = "Detects common injection shellcode"

    strings:
        // Common shellcode patterns
        $mz = { 4D 5A }
        $shellcode1 = { 55 8B EC 83 EC }  // Function prologue
        $api_hash = { 68 ?? ?? ?? ?? 68 ?? ?? ?? ?? E8 }  // Push hash, call

    condition:
        $mz at 0 or any of ($shellcode*)
}

rule Cobalt_Strike_Beacon
{
    meta:
        description = "Detects Cobalt Strike beacon in memory"

    strings:
        $config = { 00 01 00 01 00 02 }
        $sleep = "sleeptime"
        $beacon = "%s (admin)" wide

    condition:
        2 of them
}
```

### 扫描内存

```bash
# Scan all process memory
vol -f memory.raw windows.yarascan --yara-rules rules.yar

# Scan specific process
vol -f memory.raw windows.yarascan --yara-rules rules.yar --pid 1234

# Scan kernel memory
vol -f memory.raw windows.yarascan --yara-rules rules.yar --kernel
```

## 字符串分析

### 提取字符串

```bash
# Basic string extraction
strings -a memory.raw > all_strings.txt

# Unicode strings
strings -el memory.raw >> all_strings.txt

# Targeted extraction from process dump
vol -f memory.raw windows.memmap --pid 1234 --dump
strings -a pid.1234.dmp > process_strings.txt

# Pattern matching
grep -E "(https?://|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})" all_strings.txt
```

### FLOSS 混淆字符串提取

```bash
# FLOSS extracts obfuscated strings
floss malware.exe > floss_output.txt

# From memory dump
floss pid.1234.dmp
```

## 最佳实践

### 获取最佳实践

1. **最小化足迹**：使用轻量级获取工具
2. **全程记录**：记录时间、工具和转储哈希值
3. **验证完整性**：获取后立即对内存转储计算哈希
4. **证据链**：保持规范的取证处理流程

### 分析最佳实践

1. **先广后深**：先获取全貌，再深入分析
2. **交叉验证**：用多个插件验证同一数据
3. **时间线关联**：将内存发现与磁盘/网络证据关联
4. **记录发现**：保留详细笔记和截图
5. **验证结果**：通过多种方法验证发现

### 常见陷阱

- **数据过期**：内存易失，应尽快分析
- **转储不完整**：验证转储大小是否匹配预期 RAM
- **符号问题**：确保符号文件与操作系统版本匹配
- **数据涂抹**：获取过程中内存可能发生变化
- **加密**：部分数据在内存中可能已加密

## 局限性
- 仅在任务明确匹配上述范围时使用此技能
- 输出不能替代环境特定的验证、测试或专家审查
- 若缺少必要输入、权限、安全边界或成功标准，应停止并请求澄清
