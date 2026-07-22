# NotebookLM 技能故障排除指南

## 快速修复表

| 错误 | 解决方案 |
|------|----------|
| ModuleNotFoundError | 使用 `python scripts/run.py [script].py` |
| 认证失败 | 浏览器必须在设置时可见 |
| 浏览器崩溃 | `python scripts/run.py cleanup_manager.py --preserve-library` |
| 速率限制触发 | 等待 1 小时或切换账号 |
| 找不到笔记本 | `python scripts/run.py notebook_manager.py list` |
| 脚本不工作 | 始终使用 run.py 包装器 |

## 关键：始终使用 run.py

大多数问题通过使用 run.py 包装器解决：

```bash
# ✅ 正确 - 始终：
python scripts/run.py auth_manager.py status
python scripts/run.py ask_question.py --question "..."

# ❌ 错误 - 绝不要：
python scripts/auth_manager.py status  # ModuleNotFoundError!
```

## 常见问题和解决方案

### 认证问题

#### 未认证错误
```
Error: Not authenticated. Please run auth setup first.
```

**解决方案：**
```bash
# 检查状态
python scripts/run.py auth_manager.py status

# 设置认证（浏览器必须可见！）
python scripts/run.py auth_manager.py setup
# 用户必须手动登录 Google

# 如果设置失败，尝试重新认证
python scripts/run.py auth_manager.py reauth
```

#### 认证频繁过期
**解决方案：**
```bash
# 清除旧认证
python scripts/run.py cleanup_manager.py --preserve-library

# 全新认证设置
python scripts/run.py auth_manager.py setup --timeout 15

# 使用持久浏览器配置文件
export PERSIST_AUTH=true
```

#### Google 阻止自动登录
**解决方案：**
1. 使用专用 Google 账号进行自动化
2. 如果可用，启用「不够安全的应用访问」
3. 始终使用可见浏览器：
```bash
python scripts/run.py auth_manager.py setup
# 浏览器必须可见 - 用户手动登录
# 不存在 headless 参数 - 使用 --show-browser 进行调试
```

### 浏览器问题

#### 浏览器崩溃或挂起
```
TimeoutError: Waiting for selector failed
```

**解决方案：**
```bash
# 终止挂起进程
pkill -f chromium
pkill -f chrome

# 清理浏览器状态
python scripts/run.py cleanup_manager.py --confirm --preserve-library

# 重新认证
python scripts/run.py auth_manager.py reauth
```

#### 找不到浏览器错误
**解决方案：**
```bash
# 通过 run.py 安装 Chromium（自动）
python scripts/run.py auth_manager.py status
# run.py 会自动安装 Chromium

# 或手动安装（如需要）
cd ~/.claude/skills/notebooklm
source .venv/bin/activate
python -m patchright install chromium
```

### 速率限制

#### 速率限制超出（50次查询/天）
**解决方案：**

**选项 1：等待**
```bash
# 检查限制何时重置（通常是午夜 PST）
date -d "tomorrow 00:00 PST"
```

**选项 2：切换账号**
```bash
# 清除当前认证
python scripts/run.py auth_manager.py clear

# 使用不同账号登录
python scripts/run.py auth_manager.py setup
```

**选项 3：轮换账号**
```python
# 使用多个账号
accounts = ["account1", "account2"]
for account in accounts:
    # 速率限制时切换账号
    subprocess.run(["python", "scripts/run.py", "auth_manager.py", "reauth"])
```

### 笔记本访问问题

#### 找不到笔记本
**解决方案：**
```bash
# 列出所有笔记本
python scripts/run.py notebook_manager.py list

# 搜索笔记本
python scripts/run.py notebook_manager.py search --query "关键词"

# 如果缺失则添加笔记本
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/..." \
  --name "名称" \
  --topics "主题"
```

#### 笔记本访问被拒绝
**解决方案：**
1. 检查笔记本是否仍公开共享
2. 使用更新的 URL 重新添加笔记本
3. 验证使用了正确的 Google 账号

#### 使用了错误的笔记本
**解决方案：**
```bash
# 检查活动笔记本
python scripts/run.py notebook_manager.py list | grep "active"

# 激活正确的笔记本
python scripts/run.py notebook_manager.py activate --id correct-id
```

### 虚拟环境问题

#### ModuleNotFoundError
```
ModuleNotFoundError: No module named 'patchright'
```

**解决方案：**
```bash
# 始终使用 run.py - 它自动处理 venv！
python scripts/run.py [any_script].py

# run.py 会：
# 1. 如缺失则创建 .venv
# 2. 安装依赖
# 3. 运行脚本
```

#### Python 版本错误
**解决方案：**
```bash
# 检查 Python 版本（需要 3.8+）
python --version

# 如果版本错误，指定正确的 Python
python3.8 scripts/run.py auth_manager.py status
```

### 网络问题

#### 连接超时
**解决方案：**
```bash
# 增加超时
export TIMEOUT_SECONDS=60

# 检查连接
ping notebooklm.google.com

# 如需要使用代理
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

### 数据问题

#### 笔记本库损坏
```
JSON decode error when listing notebooks
```

**解决方案：**
```bash
# 备份当前库
cp ~/.claude/skills/notebooklm/data/library.json library.backup.json

# 重置库
rm ~/.claude/skills/notebooklm/data/library.json

# 重新添加笔记本
python scripts/run.py notebook_manager.py add --url ... --name ...
```

#### 磁盘空间满
**解决方案：**
```bash
# 检查磁盘使用
df -h ~/.claude/skills/notebooklm/data/

# 清理
python scripts/run.py cleanup_manager.py --confirm --preserve-library
```

## 调试技术

### 启用详细日志
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
python scripts/run.py ask_question.py --question "测试" --show-browser
```

### 测试单个组件
```bash
# 测试认证
python scripts/run.py auth_manager.py status

# 测试笔记本访问
python scripts/run.py notebook_manager.py list

# 测试浏览器启动
python scripts/run.py ask_question.py --question "test" --show-browser
```

### 错误时保存截图
添加到脚本用于调试：
```python
try:
    # 您的代码
except Exception as e:
    page.screenshot(path=f"error_{timestamp}.png")
    raise e
```

## 恢复程序

### 完全重置
```bash
#!/bin/bash
# 终止进程
pkill -f chromium

# 备份库（如存在）
if [ -f ~/.claude/skills/notebooklm/data/library.json ]; then
    cp ~/.claude/skills/notebooklm/data/library.json ~/library.backup.json
fi

# 清理所有内容
cd ~/.claude/skills/notebooklm
python scripts/run.py cleanup_manager.py --confirm --force

# 移除 venv
rm -rf .venv

# 重新安装（run.py 会处理）
python scripts/run.py auth_manager.py setup

# 恢复库（如备份存在）
if [ -f ~/library.backup.json ]; then
    mkdir -p ~/.claude/skills/notebooklm/data/
    cp ~/library.backup.json ~/.claude/skills/notebooklm/data/library.json
fi
```

### 部分恢复（保留数据）
```bash
# 保留认证和库，修复执行
cd ~/.claude/skills/notebooklm
rm -rf .venv

# run.py 会自动重建 venv
python scripts/run.py auth_manager.py status
```

## 错误消息参考

### 认证错误
| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 未认证 | 无有效认证 | `run.py auth_manager.py setup` |
| 认证过期 | 会话过旧 | `run.py auth_manager.py reauth` |
| 凭据无效 | 错误账号 | 检查 Google 账号 |
| 需要 2FA | 安全挑战 | 在可见浏览器中完成 |

### 浏览器错误
| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 找不到浏览器 | Chromium 缺失 | 使用 run.py（自动安装） |
| 连接被拒绝 | 浏览器崩溃 | 终止进程，重启 |
| 等待超时 | 页面慢 | 增加超时 |
| 上下文关闭 | 浏览器终止 | 检查日志查找崩溃原因 |

### 笔记本错误
| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 找不到笔记本 | ID 无效 | `run.py notebook_manager.py list` |
| 访问被拒绝 | 未共享 | 在 NotebookLM 中重新共享 |
| URL 无效 | 格式错误 | 使用完整 NotebookLM URL |
| 无活动笔记本 | 未选择 | `run.py notebook_manager.py activate` |

## 预防提示

1. **始终使用 run.py** - 防止 90% 的问题
2. **定期维护** - 每周清理浏览器状态
3. **监控查询** - 跟踪每日计数以避免限制
4. **备份库** - 定期导出笔记本列表
5. **使用专用账号** - 为自动化使用单独的 Google 账号

## 获取帮助

### 收集诊断信息
```bash
# 系统信息
python --version
cd ~/.claude/skills/notebooklm
ls -la

# 技能状态
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list | head -5

# 检查数据目录
ls -la ~/.claude/skills/notebooklm/data/
```

### 常见问题

**问：为什么这在 Claude 网页 UI 中不起作用？**
答：网页 UI 没有网络访问权限。使用本地 Claude Code。

**问：我可以使用多个 Google 账号吗？**
答：可以，使用 `run.py auth_manager.py reauth` 切换。

**问：如何增加速率限制？**
答：使用多个账号或升级到 Google Workspace。

**问：这对我的 Google 账号安全吗？**
答：为自动化使用专用账号。仅访问 NotebookLM。
