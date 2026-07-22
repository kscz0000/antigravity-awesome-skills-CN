# last30days 实现任务

## 设置与配置
- [x] 创建目录结构
- [x] 编写 SPEC.md
- [x] 编写 TASKS.md
- [x] 编写带有正确前置元数据的 SKILL.md

## 核心库模块
- [x] scripts/lib/env.py - 环境和 API 密钥加载
- [x] scripts/lib/dates.py - 日期范围和置信度工具
- [x] scripts/lib/cache.py - 基于 TTL 的缓存
- [x] scripts/lib/http.py - 带重试的 HTTP 客户端
- [x] scripts/lib/models.py - 自动模型选择
- [x] scripts/lib/schema.py - 数据结构
- [x] scripts/lib/openai_reddit.py - OpenAI Responses API
- [x] scripts/lib/xai_x.py - xAI Responses API
- [x] scripts/lib/reddit_enrich.py - Reddit 帖子 JSON 获取器
- [x] scripts/lib/normalize.py - 模式标准化
- [x] scripts/lib/score.py - 流行度评分
- [x] scripts/lib/dedupe.py - 近重复检测
- [x] scripts/lib/render.py - 输出渲染

## 主脚本
- [x] scripts/last30days.py - CLI 编排器

## 固定数据
- [x] fixtures/openai_sample.json
- [x] fixtures/xai_sample.json
- [x] fixtures/reddit_thread_sample.json
- [x] fixtures/models_openai_sample.json
- [x] fixtures/models_xai_sample.json

## 测试
- [x] tests/test_dates.py
- [x] tests/test_cache.py
- [x] tests/test_models.py
- [x] tests/test_score.py
- [x] tests/test_dedupe.py
- [x] tests/test_normalize.py
- [x] tests/test_render.py

## 验证
- [x] 在模拟模式下运行测试
- [x] 演示 --emit=compact
- [x] 演示 --emit=context
- [x] 验证文件树
