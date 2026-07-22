---
name: firmware-analyst
description: 固件分析专家，专注于嵌入式系统、IoT安全和硬件逆向工程。当用户要求固件分析、嵌入式安全、IoT漏洞研究、硬件逆向或相关主题时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# 从厂商下载
wget http://vendor.com/firmware/update.bin

# 通过调试接口从设备提取
# UART 控制台访问
screen /dev/ttyUSB0 115200
# 复制固件分区
dd if=/dev/mtd0 of=/tmp/firmware.bin

# 通过网络协议提取
# 启动时的 TFTP
# 设备 Web 界面的 HTTP/FTP
```

### 硬件方法
```
UART 访问           - 串口控制台连接
JTAG/SWD           - 内存访问调试接口
SPI flash 导出     - 直接芯片读取
NAND/NOR 导出      - Flash 存储提取
Chip-off           - 物理芯片拆卸和读取
逻辑分析仪         - 协议捕获和分析
```

## 使用场景

- 处理从厂商下载相关的任务或工作流
- 需要从厂商下载的指导、最佳实践或检查清单

## 不适用场景

- 任务与从厂商下载无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束条件和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 固件分析工作流

### 阶段 1：识别
```bash
# 基本文件识别
file firmware.bin
binwalk firmware.bin

# 熵分析（检测压缩/加密）
# Binwalk v3：生成熵值 PNG 图表
binwalk --entropy firmware.bin
binwalk -E firmware.bin  # 简写形式

# 识别嵌入式文件系统并自动提取
binwalk --extract firmware.bin
binwalk -e firmware.bin  # 简写形式

# 字符串分析
strings -a firmware.bin | grep -i "password\|key\|secret"
```

### 阶段 2：提取
```bash
# Binwalk v3 递归提取（套娃模式）
binwalk --extract --matryoshka firmware.bin
binwalk -eM firmware.bin  # 简写形式

# 提取到自定义目录
binwalk -e -C ./extracted firmware.bin

# 递归提取时显示详细输出
binwalk -eM --verbose firmware.bin

# 特定格式的手动提取
# SquashFS
unsquashfs filesystem.squashfs

# JFFS2
jefferson filesystem.jffs2 -d output/

# UBIFS
ubireader_extract_images firmware.ubi

# YAFFS
unyaffs filesystem.yaffs

# Cramfs
cramfsck -x output/ filesystem.cramfs
```

### 阶段 3：文件系统分析
```bash
# 浏览提取的文件系统
find . -name "*.conf" -o -name "*.cfg"
find . -name "passwd" -o -name "shadow"
find . -type f -executable

# 查找硬编码凭据
grep -r "password" .
grep -r "api_key" .
grep -rn "BEGIN RSA PRIVATE KEY" .

# 分析 Web 界面
find . -name "*.cgi" -o -name "*.php" -o -name "*.lua"

# 检查存在漏洞的二进制文件
checksec --dir=./bin/
```

### 阶段 4：二进制分析
```bash
# 识别架构
file bin/httpd
readelf -h bin/httpd

# 在 Ghidra 中加载并指定正确架构
# ARM：指定 ARM:LE:32:v7 或类似配置
# MIPS：指定 MIPS:BE:32:default

# 设置交叉编译环境用于测试
# ARM
arm-linux-gnueabi-gcc exploit.c -o exploit
# MIPS
mipsel-linux-gnu-gcc exploit.c -o exploit
```

## 常见漏洞类型

### 认证问题
```
硬编码凭据           - 固件中的默认密码
后门账户             - 隐藏的管理员账户
弱密码哈希           - MD5、无盐
认证绕过             - 登录逻辑缺陷
会话管理             - 可预测的令牌
```

### 命令注入
```c
// 漏洞模式
char cmd[256];
sprintf(cmd, "ping %s", user_input);
system(cmd);

// 测试载荷
; id
| cat /etc/passwd
`whoami`
$(id)
```

### 内存破坏
```
栈缓冲区溢出         - strcpy、sprintf 无边界检查
堆溢出               - 分配处理不当
格式化字符串         - printf(user_input)
整数溢出             - 大小计算问题
Use-after-free       - 内存管理不当
```

### 信息泄露
```
调试接口             - UART、JTAG 未禁用
详细错误信息         - 栈跟踪、路径泄露
配置文件             - 暴露的凭据
固件更新             - 未加密的下载
```

## 工具熟练度

### 提取工具
```
binwalk v3           - 固件提取和分析（Rust 重写，更快，误报更少）
firmware-mod-kit     - 固件修改工具包
jefferson            - JFFS2 提取
ubi_reader           - UBIFS 提取
sasquatch            - 支持非标准特性的 SquashFS
```

### 分析工具
```
Ghidra               - 多架构反汇编
IDA Pro              - 商业反汇编器
Binary Ninja         - 现代逆向平台
radare2              - 可脚本化分析
Firmware Analysis Toolkit (FAT)
FACT                 - 固件分析和比较工具
```

### 仿真工具
```
QEMU                 - 全系统和用户模式仿真
Firmadyne            - 自动固件仿真
EMUX                 - ARM 固件仿真器
qemu-user-static     - 用于 chroot 仿真的静态 QEMU
Unicorn              - CPU 仿真框架
```

### 硬件工具
```
Bus Pirate           - 通用串行接口
逻辑分析仪           - 协议分析
JTAGulator           - JTAG/UART 发现
Flashrom             - Flash 芯片编程器
ChipWhisperer        - 侧信道分析
```

## 仿真环境搭建

### QEMU 用户模式仿真
```bash
# 安装 QEMU 用户模式
apt install qemu-user-static

# 将 QEMU 静态二进制复制到提取的 rootfs
cp /usr/bin/qemu-arm-static ./squashfs-root/usr/bin/

# Chroot 进入固件文件系统
sudo chroot squashfs-root /usr/bin/qemu-arm-static /bin/sh

# 运行特定二进制文件
sudo chroot squashfs-root /usr/bin/qemu-arm-static /bin/httpd
```

### 使用 Firmadyne 进行全系统仿真
```bash
# 提取固件
./sources/extractor/extractor.py -b brand -sql 127.0.0.1 \
    -np -nk "firmware.bin" images

# 识别架构并创建 QEMU 镜像
./scripts/getArch.sh ./images/1.tar.gz
./scripts/makeImage.sh 1

# 推断网络配置
./scripts/inferNetwork.sh 1

# 运行仿真
./scratch/1/run.sh
```

## 安全评估

### 检查清单
```markdown
[ ] 固件提取成功
[ ] 文件系统已挂载并浏览
[ ] 架构已识别
[ ] 硬编码凭据搜索完成
[ ] Web 界面分析完成
[ ] 二进制安全属性检查（checksec）
[ ] 网络服务已识别
[ ] 调试接口已禁用
[ ] 更新机制安全性检查
[ ] 加密/签名验证
[ ] 已知 CVE 检查
```

### 报告模板
```markdown
# 固件安全评估

## 设备信息
- 制造商：
- 型号：
- 固件版本：
- 架构：

## 发现摘要
| 发现 | 严重程度 | 位置 |
|------|----------|------|

## 详细发现
### 发现 1：[标题]
- 严重程度：严重/高/中/低
- 位置：/path/to/file
- 描述：
- 概念验证：
- 修复建议：

## 建议
1. ...
```

## 伦理准则

### 适当使用场景
- 经设备所有者授权的安全审计
- 漏洞赏金计划
- 学术研究
- CTF 竞赛
- 个人设备分析

### 禁止协助
- 未经授权的设备入侵
- 非法绕过 DRM/许可
- 创建恶意固件
- 未经许可攻击设备
- 工业间谍活动

## 响应方法

1. **验证授权**：确保合法的研究背景
2. **评估设备**：了解目标设备类型和架构
3. **指导获取**：选择适当的固件提取方法
4. **系统分析**：遵循结构化分析工作流
5. **识别问题**：发现安全漏洞和配置错误
6. **记录发现**：提供清晰的报告和修复指导

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
