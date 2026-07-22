---
name: claude-in-chrome-troubleshooting
description: 诊断并修复 Claude in Chrome MCP 扩展连接问题。当 mcp__claude-in-chrome__* 工具失败、返回"Browser extension is not connected"或行为异常时使用。
risk: critical
source: community
---

# Claude in Chrome MCP 故障排查

当 Claude in Chrome MCP 工具无法连接或工作不稳定时使用此技能。

## 何时使用
- `mcp__claude-in-chrome__*` 工具失败并显示 "Browser extension is not connected"
- 浏览器自动化工作不稳定或超时
- 更新 Claude Code 或 Claude.app 之后
- 在 Claude Code CLI 和 Claude.app (Cowork) 之间切换时
- 原生主机进程正在运行但 MCP 工具仍然失败

## 何时不使用

- **Linux 或 Windows 用户** - 本技能涵盖 macOS 特定路径和工具（`~/Library/Application Support/`、`osascript`）
- 与 Claude 扩展无关的通用 Chrome 自动化问题
- Claude.app 桌面应用问题（非浏览器相关）
- 网络连接问题
- Chrome 扩展安装问题（请使用 Chrome Web Store 支持）

## Claude.app 与 Claude Code 冲突（主要问题）

**背景：** 当 Claude.app 添加 Cowork 支持（从桌面应用进行浏览器自动化）时，它引入了一个与 Claude Code CLI 冲突的竞争性原生消息主机。

### 两个原生主机，两种 Socket 格式

| 组件 | 原生主机二进制文件 | Socket 位置 |
|-----------|-------------------|-----------------|
| **Claude.app (Cowork)** | `/Applications/Claude.app/Contents/Helpers/chrome-native-host` | `/tmp/claude-mcp-browser-bridge-$USER/<PID>.sock` |
| **Claude Code CLI** | `~/.local/share/claude/versions/<version> --chrome-native-host` | `$TMPDIR/claude-mcp-browser-bridge-$USER`（单个文件） |

### 为什么会冲突

1. 两者都在 Chrome 中注册原生消息配置：
   - `com.anthropic.claude_browser_extension.json` → Claude.app helper
   - `com.anthropic.claude_code_browser_extension.json` → Claude Code wrapper

2. Chrome 扩展按名称请求原生主机
3. 如果激活了错误的配置，就会运行错误的二进制文件
4. 错误的二进制文件以 MCP 客户端不期望的格式/位置创建 socket
5. 结果：即使一切看起来都在运行，也会显示 "Browser extension is not connected"

### 解决方案：禁用 Claude.app 的原生主机

**如果你使用 Claude Code CLI 进行浏览器自动化（而非 Cowork）：**

```bash
# 禁用 Claude.app 原生消息配置
mv ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_browser_extension.json \
   ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_browser_extension.json.disabled

# 确保 Claude Code 配置存在并指向 wrapper
cat ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json
```

**如果你使用 Cowork (Claude.app) 进行浏览器自动化：**

```bash
# 禁用 Claude Code 原生消息配置
mv ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json \
   ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json.disabled
```

**两者无法同时使用。** 选择一个并禁用另一个。

### 切换脚本

将此添加到 `~/.zshrc` 或直接运行：

```bash
chrome-mcp-toggle() {
    local CONFIG_DIR=~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts
    local CLAUDE_APP="$CONFIG_DIR/com.anthropic.claude_browser_extension.json"
    local CLAUDE_CODE="$CONFIG_DIR/com.anthropic.claude_code_browser_extension.json"

    if [[ -f "$CLAUDE_APP" && ! -f "$CLAUDE_APP.disabled" ]]; then
        # 当前使用 Claude.app，切换到 Claude Code
        mv "$CLAUDE_APP" "$CLAUDE_APP.disabled"
        [[ -f "$CLAUDE_CODE.disabled" ]] && mv "$CLAUDE_CODE.disabled" "$CLAUDE_CODE"
        echo "已切换到 Claude Code CLI"
        echo "重启 Chrome 和 Claude Code 以应用更改"
    elif [[ -f "$CLAUDE_CODE" && ! -f "$CLAUDE_CODE.disabled" ]]; then
        # 当前使用 Claude Code，切换到 Claude.app
        mv "$CLAUDE_CODE" "$CLAUDE_CODE.disabled"
        [[ -f "$CLAUDE_APP.disabled" ]] && mv "$CLAUDE_APP.disabled" "$CLAUDE_APP"
        echo "已切换到 Claude.app (Cowork)"
        echo "重启 Chrome 以应用更改"
    else
        echo "当前状态不明确。请检查配置："
        ls -la "$CONFIG_DIR"/com.anthropic*.json* 2>/dev/null
    fi
}
```

用法：运行 `chrome-mcp-toggle`，然后重启 Chrome（如果切换到 CLI，还需重启 Claude Code）。

## 快速诊断

```bash
# 1. 哪个原生主机二进制文件正在运行？
ps aux | grep chrome-native-host | grep -v grep
# Claude.app: /Applications/Claude.app/Contents/Helpers/chrome-native-host
# Claude Code: ~/.local/share/claude/versions/X.X.X --chrome-native-host

# 2. socket 在哪里？
# 对于 Claude Code（TMPDIR 中的单个文件）：
ls -la "$(getconf DARWIN_USER_TEMP_DIR)/claude-mcp-browser-bridge-$USER" 2>&1

# 对于 Claude.app（包含 PID 文件的目录）：
ls -la /tmp/claude-mcp-browser-bridge-$USER/ 2>&1

# 3. 原生主机连接到了什么？
lsof -U 2>&1 | grep claude-mcp-browser-bridge

# 4. 哪些配置处于激活状态？
ls ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.anthropic*.json
```

## 关键洞察

**MCP 在启动时连接。** 如果浏览器桥接在 Claude Code 启动时未就绪，整个会话的连接都会失败。修复方法通常是：确保 Chrome + 扩展使用正确配置运行，然后重启 Claude Code。

## 完整重置流程（Claude Code CLI）

```bash
# 1. 确保正确的配置处于激活状态
mv ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_browser_extension.json \
   ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_browser_extension.json.disabled 2>/dev/null

# 2. 更新 wrapper 以使用最新 Claude Code 版本
cat > ~/.claude/chrome/chrome-native-host << 'EOF'
#!/bin/bash
LATEST=$(ls -t ~/.local/share/claude/versions/ 2>/dev/null | head -1)
exec "$HOME/.local/share/claude/versions/$LATEST" --chrome-native-host
EOF
chmod +x ~/.claude/chrome/chrome-native-host

# 3. 终止现有原生主机并清理 socket
pkill -f chrome-native-host
rm -rf /tmp/claude-mcp-browser-bridge-$USER/
rm -f "$(getconf DARWIN_USER_TEMP_DIR)/claude-mcp-browser-bridge-$USER"

# 4. 重启 Chrome
osascript -e 'quit app "Google Chrome"' && sleep 2 && open -a "Google Chrome"

# 5. 等待 Chrome，点击 Claude 扩展图标

# 6. 验证正确的原生主机正在运行
ps aux | grep chrome-native-host | grep -v grep
# 应显示：~/.local/share/claude/versions/X.X.X --chrome-native-host

# 7. 验证 socket 存在
ls -la "$(getconf DARWIN_USER_TEMP_DIR)/claude-mcp-browser-bridge-$USER"

# 8. 重启 Claude Code
```

## 其他常见原因

### 多个 Chrome 配置文件

如果你在多个 Chrome 配置文件中安装了 Claude 扩展，每个都会生成自己的原生主机和 socket。这可能导致混乱。

**解决方法：** 仅在一个 Chrome 配置文件中启用 Claude 扩展。

### 多个 Claude Code 会话

运行多个 Claude Code 实例可能导致 socket 冲突。

**解决方法：** 一次只运行一个 Claude Code 会话，或在关闭其他会话后使用 `/mcp` 重新连接。

### Wrapper 中硬编码版本

`~/.claude/chrome/chrome-native-host` 中的 wrapper 可能有硬编码版本，更新后会过时。

**诊断：**
```bash
cat ~/.claude/chrome/chrome-native-host
# 错误：exec "/Users/.../.local/share/claude/versions/2.0.76" --chrome-native-host
# 正确：使用 $(ls -t ...) 查找最新版本
```

**解决方法：** 使用完整重置流程中显示的动态版本 wrapper。

### TMPDIR 未设置

Claude Code 期望 `TMPDIR` 已设置以找到 socket。

```bash
# 检查
echo $TMPDIR
# 应显示：/var/folders/XX/.../T/

# 修复：添加到 ~/.zshrc
export TMPDIR="${TMPDIR:-$(getconf DARWIN_USER_TEMP_DIR)}"
```

## 深度诊断

```bash
echo "=== 原生主机二进制文件 ==="
ps aux | grep chrome-native-host | grep -v grep

echo -e "\n=== Socket（Claude Code 位置）==="
ls -la "$(getconf DARWIN_USER_TEMP_DIR)/claude-mcp-browser-bridge-$USER" 2>&1

echo -e "\n=== Socket（Claude.app 位置）==="
ls -la /tmp/claude-mcp-browser-bridge-$USER/ 2>&1

echo -e "\n=== 原生主机打开的文件 ==="
pgrep -f chrome-native-host | xargs -I {} lsof -p {} 2>/dev/null | grep -E "(sock|claude-mcp)"

echo -e "\n=== 激活的原生消息配置 ==="
ls ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.anthropic*.json 2>/dev/null

echo -e "\n=== 自定义 Wrapper 内容 ==="
cat ~/.claude/chrome/chrome-native-host 2>/dev/null || echo "无自定义 wrapper"

echo -e "\n=== TMPDIR ==="
echo "TMPDIR=$TMPDIR"
echo "期望值：$(getconf DARWIN_USER_TEMP_DIR)"
```

## 文件参考

| 文件 | 用途 |
|------|---------|
| `~/.claude/chrome/chrome-native-host` | Claude Code 自定义 wrapper 脚本 |
| `/Applications/Claude.app/Contents/Helpers/chrome-native-host` | Claude.app (Cowork) 原生主机 |
| `~/.local/share/claude/versions/<version>` | Claude Code 二进制文件（使用 `--chrome-native-host` 运行） |
| `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_browser_extension.json` | Claude.app 原生主机配置 |
| `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json` | Claude Code 原生主机配置 |
| `$TMPDIR/claude-mcp-browser-bridge-$USER` | Socket 文件（Claude Code） |
| `/tmp/claude-mcp-browser-bridge-$USER/<PID>.sock` | Socket 文件（Claude.app） |

## 总结

1. **主要问题：** Claude.app (Cowork) 和 Claude Code 使用不同的原生主机，socket 格式不兼容
2. **解决方案：** 禁用你未使用的那个的原生消息配置
3. **任何修复后：** 必须重启 Chrome 和 Claude Code（MCP 在启动时连接）
4. **一个配置文件：** 只在一个 Chrome 配置文件中安装 Claude 扩展
5. **一个会话：** 只运行一个 Claude Code 实例

---

*原始技能由 [@jeffzwang](https://github.com/jeffzwang) 来自 [@ExaAILabs](https://github.com/ExaAILabs) 创作。为当前版本的 Claude Desktop 和 Claude Code 进行了增强和更新。*

## 局限性
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
