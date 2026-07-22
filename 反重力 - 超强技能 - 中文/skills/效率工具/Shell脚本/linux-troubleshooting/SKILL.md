---
name: linux-troubleshooting
description: "Linux 系统故障排查工作流，用于诊断和解决系统问题、性能故障及服务异常。当用户要求'Linux故障排查'、'系统诊断'、'服务故障'、'性能问题'、'Linux排障'时使用。"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# Linux 故障排查工作流

## 概述

专门用于诊断和解决 Linux 系统问题的工作流，涵盖性能故障、服务异常、网络问题和资源瓶颈。

## 适用场景

以下情况使用本工作流：
- 诊断系统性能问题
- 排查服务故障
- 调查网络问题
- 解决磁盘空间不足
- 调试应用错误

## 工作流阶段

### 阶段 1：初步评估

#### 调用技能
- `bash-linux` - Linux 命令
- `devops-troubleshooter` - 故障排查

#### 操作
1. 检查系统运行时间
2. 回顾近期变更
3. 识别症状
4. 收集错误信息
5. 记录发现

#### 命令
```bash
uptime
hostnamectl
cat /etc/os-release
dmesg | tail -50
```

#### 可复制提示词
```
Use @bash-linux to gather system information
```

### 阶段 2：资源分析

#### 调用技能
- `bash-linux` - 资源命令
- `performance-engineer` - 性能分析

#### 操作
1. 检查 CPU 使用率
2. 分析内存
3. 查看磁盘空间
4. 监控 I/O
5. 检查网络

#### 命令
```bash
top -bn1 | head -20
free -h
df -h
iostat -x 1 5
```

#### 可复制提示词
```
Use @performance-engineer to analyze system resources
```

### 阶段 3：进程调查

#### 调用技能
- `bash-linux` - 进程命令
- `server-management` - 进程管理

#### 操作
1. 列出运行中的进程
2. 找出资源占用大户
3. 检查进程状态
4. 查看进程树
5. 分析 strace 输出

#### 命令
```bash
ps aux --sort=-%cpu | head -10
pstree -p
lsof -p PID
strace -p PID
```

#### 可复制提示词
```
Use @server-management to investigate processes
```

### 阶段 4：日志分析

#### 调用技能
- `bash-linux` - 日志命令
- `error-detective` - 错误检测

#### 操作
1. 检查系统日志
2. 查看应用日志
3. 搜索错误
4. 分析日志模式
5. 关联事件

#### 命令
```bash
journalctl -xe
tail -f /var/log/syslog
grep -i error /var/log/*
```

#### 可复制提示词
```
Use @error-detective to analyze log files
```

### 阶段 5：网络诊断

#### 调用技能
- `bash-linux` - 网络命令
- `network-engineer` - 网络排障

#### 操作
1. 检查网络接口
2. 测试连通性
3. 分析连接
4. 查看防火墙规则
5. 检查 DNS 解析

#### 命令
```bash
ip addr show
ss -tulpn
curl -v http://target
dig domain
```

#### 可复制提示词
```
Use @network-engineer to diagnose network issues
```

### 阶段 6：服务排障

#### 调用技能
- `server-management` - 服务管理
- `systematic-debugging` - 调试

#### 操作
1. 检查服务状态
2. 查看服务日志
3. 测试重启服务
4. 验证依赖项
5. 检查配置

#### 命令
```bash
systemctl status service
journalctl -u service -f
systemctl restart service
```

#### 可复制提示词
```
Use @systematic-debugging to troubleshoot service issues
```

### 阶段 7：解决

#### 调用技能
- `incident-responder` - 事件响应
- `bash-pro` - 修复实施

#### 操作
1. 实施修复
2. 验证解决效果
3. 监控稳定性
4. 记录解决方案
5. 制定预防方案

#### 可复制提示词
```
Use @incident-responder to implement resolution
```

## 故障排查清单

- [ ] 已收集系统信息
- [ ] 已分析资源
- [ ] 已查看日志
- [ ] 已测试网络
- [ ] 已验证服务
- [ ] 已解决问题
- [ ] 已创建文档

## 质量门控

- [ ] 已定位根因
- [ ] 已验证修复
- [ ] 已部署监控
- [ ] 文档已完备

## 相关工作流包

- `os-scripting` - OS 脚本
- `bash-scripting` - Bash 脚本
- `cloud-devops` - DevOps

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 输出不能替代针对具体环境的验证、测试或专家评审。
- 若缺少必要的输入、权限、安全边界或成功标准，应停下来请求澄清。
