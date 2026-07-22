# AI Studio Image — 完整安装指南

## 1. 获取 API Key

1. 访问 https://aistudio.google.com/apikey
2. 点击 "Create API Key"
3. 选择或创建一个 Google Cloud 项目
4. 复制生成的密钥

## 2. 配置 API Key

### 选项 A：.env 文件（推荐）

创建/编辑 `C:\Users\renat\skills\ai-studio-image\.env`：

```
GEMINI_API_KEY=您的主API密钥
GEMINI_API_KEY_BACKUP_1=备用密钥1
GEMINI_API_KEY_BACKUP_2=备用密钥2
```

### 选项 B：环境变量

```bash
# Windows CMD
set GEMINI_API_KEY=您的API密钥

# Windows PowerShell
$env:GEMINI_API_KEY="您的API密钥"

# Linux/Mac
export GEMINI_API_KEY=您的API密钥
```

## 3. 安装依赖

```bash
pip install -r C:\Users\renat\skills\ai-studio-image\scripts\requirements.txt
```

或手动安装：
```bash
pip install google-genai Pillow python-dotenv
```

## 4. 快速测试

```bash
# 测试是否一切正常
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py --list-models

# 生成第一张图像
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py \
  --prompt "年轻人在咖啡馆微笑" \
  --mode influencer \
  --format square
```

## 5. 可用模型

| 模型 | ID | 速度 | 质量 | 成本 | 最佳用途 |
|--------|-----|-----------|-----------|-------|-------------|
| imagen-4 | imagen-4.0-generate-001 | 中等 | 高 | $0.03 | **通用（推荐）** |
| imagen-4-ultra | imagen-4.0-ultra-generate-001 | 慢 | 最高 | $0.06 | 高质量、印刷 |
| imagen-4-fast | imagen-4.0-fast-generate-001 | 快 | 良好 | $0.02 | 大批量、快速迭代 |
| gemini-flash-image | gemini-2.5-flash-preview-image-generation | 快 | 高 | 变动 | 编辑、多轮对话 |
| gemini-pro-image | gemini-3-pro-image-preview | 中等 | 最高+4K | 变动 | 文字、参考图、4K |

## 6. 格式（宽高比）

| 名称 | 比例 | 用途 |
|------|-------|-----|
| square | 1:1 | Instagram/Facebook 动态 |
| portrait-45 | 4:5 | Instagram 竖版（最佳！） |
| portrait-34 | 3:4 | Pinterest、卡片 |
| portrait-23 | 2:3 | 海报、印刷品 |
| widescreen | 16:9 | YouTube、横幅 |
| ultrawide | 21:9 | 电影风格 |
| stories | 9:16 | Stories、Reels、TikTok |
| landscape-43 | 4:3 | 演示文稿 |
| landscape-32 | 3:2 | 35mm 摄影 |
| landscape-54 | 5:4 | 接近方形 |

## 7. 拟人化级别

| 级别 | 描述 | 使用场景 |
|-------|-----------|-------------|
| ultra | 看起来像业余手机拍摄 | 非常休闲的内容、幕后花絮 |
| natural | 现代手机、均衡 | **默认 — 大多数情况** |
| polished | 自然但精致 | 专业内容 |
| editorial | 杂志风格 | 品牌、编辑 |

## 8. 故障排除

| 错误 | 原因 | 解决方案 |
|------|-------|---------|
| API key not found | 未配置密钥 | 创建 .env 或设置变量 |
| 403 Forbidden | 密钥无权限 | 检查 Google Cloud 权限 |
| 429 Rate Limited | 请求过多 | 等待或使用备用密钥 |
| Image blocked | 内容受限 | 调整提示词，避免敏感内容 |
| Model not found | 模型不可用 | 尝试其他模型：imagen-4 |
| Empty response | 提示词太泛泛 | 给提示词添加更多细节 |
