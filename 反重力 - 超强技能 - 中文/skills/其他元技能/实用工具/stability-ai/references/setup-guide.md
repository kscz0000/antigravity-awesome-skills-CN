# 配置指南 — Stable Diffusion 技能

## 1. 注册 Stability AI 账号

1. 访问 **https://platform.stability.ai**
2. 点击 **Sign Up**（已有账号则点 Login）
3. 支持 Google、GitHub 或邮箱/密码注册
4. **Community License** 免费且自动生效，适用于个人或年营收低于 100 万美元的企业

## 2. 获取 API Key

1. 登录后进入 **Account** > **API Keys**（或直接访问：https://platform.stability.ai/account/keys）
2. 点击 **Create API Key**
3. 命名（如 "claude-skills"）
4. 复制生成的 Key（以 `sk-` 开头）

## 3. 配置 Key

编辑技能根目录下的 `.env` 文件（`stable-diffusion/.env`）：

```
STABILITY_API_KEY=sk-sua-chave-aqui
```

也可通过环境变量导出：

```bash
export STABILITY_API_KEY="sk-sua-chave-aqui"
```

## 4. 安装依赖

```bash
cd stable-diffusion
pip install -r scripts/requirements.txt
```

唯一外部依赖：**Pillow**（图像处理）。
HTTP 请求使用 `urllib`（Python 标准库）。

## 5. 测试连接

```bash
python scripts/generate.py --list-models
```

如果 Key 正确，会显示可用模型列表。

## 6. 首次生成

```bash
python scripts/generate.py --prompt "a beautiful sunset over mountains" --mode generate
```

图像将保存到 `data/outputs/`。

## 故障排查

### 401 错误（未授权）
- 检查 `.env` 中的 Key 是否正确
- 检查 Key 是否有多余空格
- 在控制面板重新生成 Key

### 402 错误（需要付款）
- 账号可能已超出额度限制
- Community License 额度充足，但高峰时段可能有限制
- 查看控制面板确认状态

### 429 错误（请求频率超限）
- 限制：每 10 秒 150 次请求
- 脚本已内置指数退避自动重试
- 持续出现则等待几分钟

### 400 错误（请求格式错误）
- 检查提示词是否为空
- 检查宽高比是否有效（用 `--list-models` 查看选项）
- 图生图/局部重绘时，检查图像文件是否存在

### 图像未保存
- 检查 `data/outputs/` 目录的写入权限
- 目录会自动创建，但在受限环境中可能失败

## 详细速率限制

| 计划 | 每 10 秒请求数 | 可用模型 |
|------|---------------|----------|
| Community | 150 | SD3.5、Ultra、Core 全部 |

## 安全说明

- Key 不会被记录或显示在输出中
- `.env` 已在 `.gitignore` 中（不要提交！）
- 每日限额可配置：`SAFETY_MAX_IMAGES_PER_DAY=100`（环境变量）
- 每日计数器保存在 `data/daily_counter.json`
