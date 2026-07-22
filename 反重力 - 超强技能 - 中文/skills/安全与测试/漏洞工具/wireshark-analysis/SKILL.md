---
name: wireshark-analysis
description: "使用 Wireshark 执行全面的网络流量分析,捕获、过滤并检查网络数据包,用于安全调查、性能优化与故障排查。触发词:Wireshark、网络抓包、流量分析、PCAP、协议分析、故障排查、安全调查。"
risk: unknown
source: community
author: zebbern
date_added: "2026-02-27"
---

# Wireshark 网络流量分析

## 目的

使用 Wireshark 执行全面的网络流量分析,捕获、过滤并检查网络数据包,用于安全调查、性能优化与故障排查。本技能支持对网络协议进行系统化分析、检测异常行为,并从 PCAP 文件中重建网络会话。

## 输入 / 前置条件

### 必需工具
- 已安装 Wireshark(Windows、macOS 或 Linux)
- 具有抓包权限的网络接口
- 用于离线分析的 PCAP/PCAPNG 文件
- 用于实时抓包的管理员/root 权限

### 技术要求
- 理解网络协议(TCP、UDP、HTTP、DNS)
- 熟悉 IP 地址和端口
- 掌握 OSI 模型各层
- 了解常见攻击模式

### 使用场景
- 网络故障排查与连接性问题
- 安全事件调查
- 恶意软件流量分析
- 性能监控与优化
- 协议学习与教育

## 输出 / 交付物

### 主要输出
- 针对特定流量的过滤后抓包
- 重建的通信流
- 流量统计与可视化
- 事件取证文档

## 核心工作流

### 阶段 1:捕获网络流量

#### 启动实时抓包
在网络接口上开始捕获数据包:

```
1. Launch Wireshark
2. Select network interface from main screen
3. Click shark fin icon or double-click interface
4. Capture begins immediately
```

#### 抓包控制
| 操作 | 快捷键 | 描述 |
|--------|----------|-------------|
| 开始/停止抓包 | Ctrl+E | 切换抓包开关 |
| 重新抓包 | Ctrl+R | 停止并启动新抓包 |
| 打开 PCAP 文件 | Ctrl+O | 加载已有抓包文件 |
| 保存抓包 | Ctrl+S | 保存当前抓包 |

#### 抓包过滤器
在抓包前应用过滤器以限制数据收集:

```
# Capture only specific host
host 192.168.1.100

# Capture specific port
port 80

# Capture specific network
net 192.168.1.0/24

# Exclude specific traffic
not arp

# Combine filters
host 192.168.1.100 and port 443
```

### 阶段 2:显示过滤器

#### 基础过滤语法
对已捕获的数据包进行过滤以进行分析:

```
# IP address filters
ip.addr == 192.168.1.1              # All traffic to/from IP
ip.src == 192.168.1.1               # Source IP only
ip.dst == 192.168.1.1               # Destination IP only

# Port filters
tcp.port == 80                       # TCP port 80
udp.port == 53                       # UDP port 53
tcp.dstport == 443                   # Destination port 443
tcp.srcport == 22                    # Source port 22
```

#### 协议过滤器
按特定协议过滤:

```
# Common protocols
http                                  # HTTP traffic
https or ssl or tls                   # Encrypted web traffic
dns                                   # DNS queries and responses
ftp                                   # FTP traffic
ssh                                   # SSH traffic
icmp                                  # Ping/ICMP traffic
arp                                   # ARP requests/responses
dhcp                                  # DHCP traffic
smb or smb2                          # SMB file sharing
```

#### TCP 标志位过滤器
识别特定的连接状态:

```
tcp.flags.syn == 1                   # SYN packets (connection attempts)
tcp.flags.ack == 1                   # ACK packets
tcp.flags.fin == 1                   # FIN packets (connection close)
tcp.flags.reset == 1                 # RST packets (connection reset)
tcp.flags.syn == 1 && tcp.flags.ack == 0  # SYN-only (initial connection)
```

#### 内容过滤器
搜索特定内容:

```
frame contains "password"            # Packets containing string
http.request.uri contains "login"    # HTTP URIs with string
tcp contains "GET"                   # TCP packets with string
```

#### 分析过滤器
识别潜在问题:

```
tcp.analysis.retransmission          # TCP retransmissions
tcp.analysis.duplicate_ack           # Duplicate ACKs
tcp.analysis.zero_window             # Zero window (flow control)
tcp.analysis.flags                   # Packets with issues
dns.flags.rcode != 0                 # DNS errors
```

#### 组合过滤器
使用逻辑运算符构建复杂查询:

```
# AND operator
ip.addr == 192.168.1.1 && tcp.port == 80

# OR operator
dns || http

# NOT operator
!(arp || icmp)

# Complex combinations
(ip.src == 192.168.1.1 || ip.src == 192.168.1.2) && tcp.port == 443
```

### 阶段 3:跟踪流

#### TCP 流重建
查看完整的 TCP 会话:

```
1. Right-click on any TCP packet
2. Select Follow > TCP Stream
3. View reconstructed conversation
4. Toggle between ASCII, Hex, Raw views
5. Filter to show only this stream
```

#### 流类型
| 流类型 | 访问方式 | 用途 |
|--------|--------|----------|
| TCP 流 | Follow > TCP Stream | Web、文件传输、任意 TCP |
| UDP 流 | Follow > UDP Stream | DNS、VoIP、流媒体 |
| HTTP 流 | Follow > HTTP Stream | Web 内容、请求头 |
| TLS 流 | Follow > TLS Stream | 加密流量(需具备密钥) |

#### 流分析技巧
- 审查请求/响应对
- 识别已传输的文件或数据
- 寻找明文中的凭据
- 注意异常模式或命令

### 阶段 4:统计分析

#### 协议层级
查看协议分布:

```
Statistics > Protocol Hierarchy

Shows:
- Percentage of each protocol
- Packet counts
- Bytes transferred
- Protocol breakdown tree
```

#### 会话
分析通信对:

```
Statistics > Conversations

Tabs:
- Ethernet: MAC address pairs
- IPv4/IPv6: IP address pairs
- TCP: Connection details (ports, bytes, packets)
- UDP: Datagram exchanges
```

#### 端点
查看活跃的网络参与者:

```
Statistics > Endpoints

Shows:
- All source/destination addresses
- Packet and byte counts
- Geographic information (if enabled)
```

#### 流向图
可视化数据包序列:

```
Statistics > Flow Graph

Options:
- All packets or displayed only
- Standard or TCP flow
- Shows packet timing and direction
```

#### I/O 图表
绘制随时间变化的流量:

```
Statistics > I/O Graph

Features:
- Packets per second
- Bytes per second
- Custom filter graphs
- Multiple graph overlays
```

### 阶段 5:安全分析

#### 检测端口扫描
识别侦察活动:

```
# SYN scan detection (many ports, same source)
ip.src == SUSPECT_IP && tcp.flags.syn == 1

# Review Statistics > Conversations for anomalies
# Look for single source hitting many destination ports
```

#### 识别可疑流量
过滤异常行为:

```
# Traffic to unusual ports
tcp.dstport > 1024 && tcp.dstport < 49152

# Traffic outside trusted network
!(ip.addr == 192.168.1.0/24)

# Unusual DNS queries
dns.qry.name contains "suspicious-domain"

# Large data transfers
frame.len > 1400
```

#### ARP 欺骗检测
识别 ARP 攻击:

```
# Duplicate ARP responses
arp.duplicate-address-frame

# ARP traffic analysis
arp

# Look for:
# - Multiple MACs for same IP
# - Gratuitous ARP floods
# - Unusual ARP patterns
```

#### 检查下载行为
分析文件传输:

```
# HTTP file downloads
http.request.method == "GET" && http contains "Content-Disposition"

# Follow HTTP Stream to view file content
# Use File > Export Objects > HTTP to extract files
```

#### DNS 分析
调查 DNS 活动:

```
# All DNS traffic
dns

# DNS queries only
dns.flags.response == 0

# DNS responses only
dns.flags.response == 1

# Failed DNS lookups
dns.flags.rcode != 0

# Specific domain queries
dns.qry.name contains "domain.com"
```

### 阶段 6:专家信息

#### 访问专家分析
查看 Wireshark 的自动分析结果:

```
Analyze > Expert Information

Categories:
- Errors: Critical issues
- Warnings: Potential problems
- Notes: Informational items
- Chats: Normal conversation events
```

#### 常见专家发现
| 发现 | 含义 | 处理建议 |
|---------|---------|--------|
| TCP 重传 | 数据包重发 | 检查是否有丢包 |
| 重复 ACK | 可能存在丢包 | 调查网络路径 |
| 零窗口 | 缓冲区已满 | 检查接收方性能 |
| RST | 连接重置 | 检查是否有阻塞或错误 |
| 乱序 | 数据包顺序错乱 | 通常正常,过多则视为问题 |

## 快速参考

### 键盘快捷键
| 操作 | 快捷键 |
|--------|----------|
| 打开文件 | Ctrl+O |
| 保存文件 | Ctrl+S |
| 开始/停止抓包 | Ctrl+E |
| 查找数据包 | Ctrl+F |
| 跳转到数据包 | Ctrl+G |
| 下一个数据包 | ↓ |
| 上一个数据包 | ↑ |
| 第一个数据包 | Ctrl+Home |
| 最后一个数据包 | Ctrl+End |
| 应用过滤器 | Enter |
| 清除过滤器 | Ctrl+Shift+X |

### 常用过滤器参考
```
# Web traffic
http || https

# Email
smtp || pop || imap

# File sharing  
smb || smb2 || ftp

# Authentication
ldap || kerberos

# Network management
snmp || icmp

# Encrypted
tls || ssl
```

### 导出选项
```
File > Export Specified Packets    # Save filtered subset
File > Export Objects > HTTP       # Extract HTTP files
File > Export Packet Dissections   # Export as text/CSV
```

## 约束与防护

### 操作边界
- 仅捕获经授权的网络流量
- 按照隐私政策处理已捕获数据
- 避免无必要地捕获敏感凭据
- 妥善保护包含敏感数据的 PCAP 文件

### 技术限制
- 大型抓包会消耗大量内存
- 无密钥时无法查看加密流量内容
- 高速网络可能发生丢包
- 部分协议需要插件才能完全解码

### 最佳实践
- 使用抓包过滤器限制数据收集
- 长时间会话中定期保存抓包
- 使用显示过滤器而非删除数据包
- 记录分析发现与方法

## 示例

### 示例 1:HTTP 凭据分析

**场景**:调查潜在的明文凭据传输

```
1. Filter: http.request.method == "POST"
2. Look for login forms
3. Follow HTTP Stream
4. Search for username/password parameters
```

**发现**:凭据以明文表单数据形式传输。

### 示例 2:恶意软件 C2 检测

**场景**:识别命令与控制流量

```
1. Filter: dns
2. Look for unusual query patterns
3. Check for high-frequency beaconing
4. Identify domains with random-looking names
5. Filter: ip.dst == SUSPICIOUS_IP
6. Analyze traffic patterns
```

**指标**:
- 规律的间隔时间
- 编码/加密的载荷
- 异常端口或协议

### 示例 3:网络故障排查

**场景**:诊断 Web 应用缓慢问题

```
1. Filter: ip.addr == WEB_SERVER
2. Check Statistics > Service Response Time
3. Filter: tcp.analysis.retransmission
4. Review I/O Graph for patterns
5. Check for high latency or packet loss
```

**发现**:TCP 重传表明网络存在拥塞。

## 故障排查

### 未捕获到数据包
- 确认选择了正确的接口
- 检查是否具有管理员/root 权限
- 确认网卡处于活动状态
- 若问题仍然存在,关闭混杂模式

### 过滤器不生效
- 验证过滤语法(红色 = 错误)
- 检查字段名是否有拼写错误
- 使用 Expression 按钮选择有效字段
- 清除过滤器并逐步重建

### 性能问题
- 使用抓包过滤器限制流量
- 将大型抓包拆分为较小的文件
- 在抓包期间禁用名称解析
- 关闭不必要的协议解析器

### 无法解密 TLS/SSL
- 获取服务器私钥
- 在 Edit > Preferences > Protocols > TLS 中配置
- 对于临时密钥,从浏览器捕获 pre-master secret
- 部分现代密码算法无法被动解密

## 何时使用
本技能适用于执行上述概述中的工作流或操作。
