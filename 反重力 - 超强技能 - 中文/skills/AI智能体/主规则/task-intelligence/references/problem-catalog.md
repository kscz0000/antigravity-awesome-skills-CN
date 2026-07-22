# 按领域分类的问题目录

## 技能与编排器

| 问题 | 频率 | 预防措施 |
|------|------|----------|
| SKILL.md 中 YAML 无效 | 高 | `python -c "import yaml; yaml.safe_load(open('SKILL.md').read())"` |
| YAML 中 `name` 或 `description` 重复 | 中 | 用 `^name:` 在文件中搜索——应只有1处匹配 |
| skill-installer 静默失败 | 中 | 使用 `--force` 并阅读完整输出 |
| scan_registry.py 的 sets/dicts bug | 低 | 手动通过 JSON 更新 registry |
| 技能在 .claude 中但不在 skills/ 中 | 中 | 始终通过 skill-installer 安装，不要手动复制 |

## API 与集成

| 问题 | 频率 | 预防措施 |
|------|------|----------|
| Token/API 密钥过期 | 高 | 执行前验证有效性 |
| 触发频率限制 | 中 | 实现带指数退避的重试 |
| 端点变更（破坏性更新） | 低 | 锁定 API 版本，更新前查看 changelog |
| Webhook 中 HMAC-SHA256 无效 | 中 | 上线前用示例 payload 测试 |
| 硬编码凭据被提交 | 低但关键 | 强制使用 `.env` + 配置 `.gitignore` |

## 文件与路径

| 问题 | 频率 | 预防措施 |
|------|------|----------|
| 路径不存在 | 高 | 操作前用 `os.path.exists()` 检查 |
| 权限拒绝 | 中 | 用 `os.access(path, os.W_OK)` 验证 |
| 编码错误（含重音的 pt-BR） | 高 | 始终显式使用 `open(f, encoding='utf-8')` |
| ZIP 损坏 | 低 | 生成后用 `zipfile.is_zipfile()` 验证 |
| 文件被其他进程占用 | 低 | 用 `with` 显式关闭句柄 |

## ZIP 与生态系统构建

| 问题 | 频率 | 预防措施 |
|------|------|----------|
| ecosystem-completo.zip 过期 | 高 | 每次新技能后执行 build_ecosystem.py |
| 技能编号顺序错乱 | 中 | 分配编号前检查总数 |
| ZIP 过大（>50MB） | 低 | 排除 __pycache__、.pyc、node_modules |

## Git

| 问题 | 频率 | 预防措施 |
|------|------|----------|
| 在错误分支上提交 | 高 | 提交前执行 `git branch --show-current` |
| 未提交的更改丢失 | 中 | 破坏性操作前执行 `git status` |
| 合并冲突 | 中 | 推送前执行 `git pull --rebase` |
| 推送了密钥 | 低但关键 | 提交前执行 `git diff --staged` |

## Python / 脚本

| 问题 | 频率 | 预防措施 |
|------|------|----------|
| ModuleNotFoundError | 高 | 先执行 `pip install -r requirements.txt` |
| Python 2 vs 3 | 低 | 显式使用 `python3` |
| 子进程无超时 | 中 | 始终使用 `subprocess.run(..., timeout=30)` |
| JSON 解码错误 | 中 | 显式处理 `json.JSONDecodeError` |
| UnicodeDecodeError | 高 | 文件操作使用 `encoding='utf-8', errors='replace'` |