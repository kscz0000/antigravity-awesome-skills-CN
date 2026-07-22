# 项目设置约定（适用于所有 Cookbook）

在生成任何 cookbook 应用前，请先阅读本指引。

## 目标

建立一套安全的默认项目结构，避免密钥意外泄露，并使各 cookbook 之间的配置步骤保持一致。

## 必须遵循的顺序

1. 创建项目目录。
2. 立即初始化 git。
3. 在任何本地 `.env` 文件之前先创建 `.gitignore`。
4. 基于 [environment_requirements.md](environment_requirements.md) 创建 `.env`。
5. 提示用户填写必需值（`WEAVIATE_URL`、`WEAVIATE_API_KEY`）以及其实际需要使用的可选键。

## 必需文件

### `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/

# Node
node_modules/
.next/
out/
dist/

# Local env files (never commit secrets)
.env
.env.*
secrets/

# Common local artifacts
.DS_Store
```

### `.env`

- 使用 [environment_requirements.md](environment_requirements.md) 中提供的官方模板。
- 真实的 `.env` 值仅保留在本地。

## Git 基线

在每个新 cookbook 应用中都执行以下命令：

```bash
git init
git add .gitignore
git commit -m "initialize project baseline"
```

## Claude 安全基线（推荐）

对于通过 Claude Code 开发的项目，建议针对本地密钥文件添加拒绝规则：

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./**/.env)",
      "Read(./**/.env.*)",
      "Read(./secrets/**)"
    ]
  }
}
```

将该配置保存到项目根目录的 `.claude/settings.json`。