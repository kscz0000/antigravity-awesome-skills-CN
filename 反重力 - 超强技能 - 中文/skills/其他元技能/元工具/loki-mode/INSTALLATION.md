# Loki Mode 安装指南

所有平台和使用场景的完整安装说明。

---

## 目录

- [快速安装（推荐）](#快速安装推荐)
- [Claude Code (CLI)](#claude-code-cli)
- [Claude.ai (Web)](#claudeai-web)
- [Anthropic API 控制台](#anthropic-api-console)
- [验证安装](#验证安装)
- [故障排除](#故障排除)

---

## 快速安装（推荐）

**Claude Code 用户：**

```bash
# 克隆到您的技能目录
git clone https://github.com/asklokesh/loki-mode.git ~/.claude/skills/loki-mode
```

**完成！** 跳转到 [验证安装](#验证安装)。

---

## Claude Code (CLI)

Loki Mode 可以通过三种方式为 Claude Code 安装：

### 选项 A：Git 克隆（推荐）

**个人安装（在所有项目中可用）：**
```bash
git clone https://github.com/asklokesh/loki-mode.git ~/.claude/skills/loki-mode
```

**项目特定安装：**
```bash
# 首先导航到您的项目目录
cd /path/to/your/project

# 克隆到本地技能目录
git clone https://github.com/asklokesh/loki-mode.git .claude/skills/loki-mode
```

### 选项 B：从 Releases 下载

```bash
# 导航到技能目录
cd ~/.claude/skills

# 获取最新版本号
VERSION=$(curl -s https://api.github.com/repos/asklokesh/loki-mode/releases/latest | grep tag_name | cut -d'"' -f4 | tr -d 'v')

# 下载并解压
curl -L -o loki-mode.zip "https://github.com/asklokesh/loki-mode/releases/download/v${VERSION}/loki-mode-claude-code-${VERSION}.zip"
unzip loki-mode.zip && rm loki-mode.zip
```

**结果：** 创建 `~/.claude/skills/loki-mode/SKILL.md`

### 选项 C：最小安装（curl）

如果您只需要核心文件而不需要完整仓库：

```bash
# 创建目录结构
mkdir -p ~/.claude/skills/loki-mode/references

# 下载核心技能文件
curl -o ~/.claude/skills/loki-mode/SKILL.md \
  https://raw.githubusercontent.com/asklokesh/loki-mode/main/SKILL.md

# 下载智能体定义
curl -o ~/.claude/skills/loki-mode/references/agents.md \
  https://raw.githubusercontent.com/asklokesh/loki-mode/main/references/agents.md

# 下载部署指南
curl -o ~/.claude/skills/loki-mode/references/deployment.md \
  https://raw.githubusercontent.com/asklokesh/loki-mode/main/references/deployment.md

# 下载业务运营参考
curl -o ~/.claude/skills/loki-mode/references/business-ops.md \
  https://raw.githubusercontent.com/asklokesh/loki-mode/main/references/business-ops.md
```

**注意：** 此最小安装不包括示例、测试或自主运行器。使用选项 A 或 B 获取完整功能。

---

## Claude.ai (Web)

在 Claude.ai 网页界面使用 Loki Mode：

### 步骤 1：下载技能包

1. 访问 [Releases](https://github.com/asklokesh/loki-mode/releases)
2. 下载**任一**：
   - `loki-mode-X.X.X.zip`（标准格式）
   - `loki-mode-X.X.X.skill`（技能格式）

   两者包含相同的技能，都可以使用。

### 步骤 2：上传到 Claude.ai

1. 打开 [Claude.ai](https://claude.ai)
2. 进入**设置**（齿轮图标）
3. 导航到**功能 → 技能**
4. 点击**上传技能**
5. 选择下载的 `.zip` 或 `.skill` 文件

**文件结构：** Claude.ai 包在根级别有 `SKILL.md`，符合网页界面要求。

---

## Anthropic API 控制台

通过 Anthropic API 控制台 (console.anthropic.com) 使用 Loki Mode：

### 步骤 1：下载 API 包

1. 访问 [Releases](https://github.com/asklokesh/loki-mode/releases)
2. 下载 **`loki-mode-api-X.X.X.zip`**（注意 `-api-` 版本）

   **重要：** API 版本与网页版本的文件结构不同。

### 步骤 2：上传到 API 控制台

1. 访问 [console.anthropic.com](https://console.anthropic.com)
2. 导航到**技能**部分
3. 点击**上传技能**
4. 选择下载的 `loki-mode-api-X.X.X.zip` 文件

**文件结构：** API 包在 `loki-mode/` 文件夹内有 `SKILL.md`，符合 API 要求。

---

## 验证安装

### Claude Code (CLI)

检查技能文件是否就位：

```bash
cat ~/.claude/skills/loki-mode/SKILL.md | head -10
```

**预期输出：** 应显示以以下内容开头的 YAML 前置元数据：
```yaml
---
name: loki-mode
description: Multi-Agent Autonomous Startup System
...
---
```

### Claude.ai (Web)

1. 开始新对话
2. 输入：`Loki Mode`
3. Claude 应识别技能并请求 PRD

### API 控制台

1. 创建启用技能的新 API 调用
2. 在请求中包含该技能
3. 技能应可使用

---

## 文件结构

安装后，您应该有以下结构：

```
loki-mode/
├── SKILL.md              # 主技能文件（必需）
├── README.md             # 文档
├── INSTALLATION.md       # 本文件
├── CHANGELOG.md          # 版本历史
├── VERSION               # 当前版本号
├── LICENSE               # MIT 许可证
├── references/           # 智能体和部署参考
│   ├── agents.md
│   ├── deployment.md
│   └── business-ops.md
├── autonomy/             # 自主运行器（仅 CLI）
│   ├── run.sh
│   └── README.md
├── examples/             # 测试用示例 PRD
│   ├── simple-todo-app.md
│   ├── api-only.md
│   ├── static-landing-page.md
│   └── full-stack-demo.md
├── tests/                # 测试套件（仅 CLI）
│   ├── run-all-tests.sh
│   ├── test-bootstrap.sh
│   └── ...
└── integrations/         # 第三方集成
    └── vibe-kanban.md
```

**注意：** 某些文件/目录（autonomy、tests、examples）仅在完整安装（选项 A 或 B）中可用。

---

## 故障排除

### 技能未找到

**问题：** Claude 不识别 "Loki Mode" 命令。

**解决方案：**
1. **检查安装路径：**
   ```bash
   ls -la ~/.claude/skills/loki-mode/SKILL.md
   ```

2. **验证 YAML 前置元数据：**
   ```bash
   cat ~/.claude/skills/loki-mode/SKILL.md | head -5
   ```
   应显示 `name: loki-mode`

3. **重启 Claude Code：**
   ```bash
   # 退出并重启 claude 命令
   ```

### 权限被拒绝

**问题：** 无法创建目录或下载文件。

**解决方案：**
```bash
# 确保技能目录存在
mkdir -p ~/.claude/skills

# 检查权限
ls -la ~/.claude/
```

### 下载失败

**问题：** curl 或 wget 命令失败。

**解决方案：**
1. **检查网络连接**

2. **尝试替代下载方法：**
   ```bash
   # 使用 wget 代替 curl
   wget -O ~/.claude/skills/loki-mode/SKILL.md \
     https://raw.githubusercontent.com/asklokesh/loki-mode/main/SKILL.md
   ```

3. **手动下载：**
   - 在浏览器中访问 URL
   - 手动保存文件到 `~/.claude/skills/loki-mode/`

### 自主运行器无法启动

**问题：** `./autonomy/run.sh` 出现 "command not found" 或权限错误。

**解决方案：**
1. **添加执行权限：**
   ```bash
   chmod +x autonomy/run.sh
   ```

2. **从仓库根目录运行：**
   ```bash
   # 确保您在 loki-mode 目录中
   cd ~/.claude/skills/loki-mode
   ./autonomy/run.sh
   ```

3. **检查前置条件：**
   ```bash
   # 确保 Claude Code 已安装
   claude --version

   # 确保 Python 3 可用
   python3 --version
   ```

### 参考文件未加载

**问题：** 技能加载但智能体定义或部署指南缺失。

**解决方案：**
```bash
# 确保所有参考文件存在
ls -la ~/.claude/skills/loki-mode/references/

# 应显示：
# agents.md
# deployment.md
# business-ops.md

# 如果缺失，下载它们：
curl -o ~/.claude/skills/loki-mode/references/agents.md \
  https://raw.githubusercontent.com/asklokesh/loki-mode/main/references/agents.md
```

---

## 更新 Loki Mode

### Git 安装

```bash
cd ~/.claude/skills/loki-mode
git pull origin main
```

### 手动安装

1. 下载最新版本
2. 解压到同一目录（覆盖现有文件）
3. 或删除旧安装并重新安装

### 检查当前版本

```bash
cat ~/.claude/skills/loki-mode/VERSION
```

---

## 卸载

### Claude Code (CLI)

```bash
# 删除技能目录
rm -rf ~/.claude/skills/loki-mode
```

### Claude.ai (Web)

1. 进入**设置 → 功能 → 技能**
2. 在列表中找到 "loki-mode"
3. 点击**移除**

### API 控制台

1. 进入**技能**部分
2. 找到 "loki-mode"
3. 点击**删除**

---

## 下一步

安装后：

1. **快速测试：** 运行一个简单示例
   ```bash
   ./autonomy/run.sh examples/simple-todo-app.md
   ```

2. **阅读文档：** 查看 [README.md](README.md) 获取使用指南

3. **创建您的第一个 PRD：** 参见 README 中的快速开始部分

4. **加入社区：** 在 [GitHub](https://github.com/asklokesh/loki-mode) 报告问题或贡献

---

## 需要帮助？

- **问题/Bug：** [GitHub Issues](https://github.com/asklokesh/loki-mode/issues)
- **讨论：** [GitHub Discussions](https://github.com/asklokesh/loki-mode/discussions)
- **文档：** [README.md](README.md)

---

**祝您构建愉快！**
