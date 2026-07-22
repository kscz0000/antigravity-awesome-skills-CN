---
name: awt-e2e-testing
description: "AI驱动的E2E Web测试——AI编码工具的眼睛和双手。声明式YAML场景、Playwright执行、视觉匹配（OpenCV + OCR）、平台自动检测（Flutter/React/Vue）、学习数据库。安装：npx skills add ksgisang/awt-skill --skill awt -g。触发词：E2E测试、端到端测试、Web测试、Playwright测试、视觉测试、OCR测试、YAML测试场景、AI测试、自动化测试"
risk: unknown
source: "https://github.com/ksgisang/awt-skill"
---

# AWT — AI驱动的E2E测试（Beta版）

> `npx skills add ksgisang/awt-skill --skill awt -g`

AWT赋予AI编码工具通过真实浏览器查看和交互Web应用的能力。你的AI设计YAML测试场景；AWT使用Playwright执行它们。

## 何时使用
- 你需要通过真实浏览器进行AI辅助的端到端测试，使用声明式YAML场景。
- 测试流程依赖于视觉匹配、OCR或平台自动检测，而非稳定的DOM选择器。
- 你想要一个既能执行测试又能为AI编码工作流解释失败的E2E工具链。

## 当前功能
- YAML场景 → Playwright，模拟人类交互
- 视觉匹配：OpenCV模板匹配 + OCR（无需CSS选择器）
- 平台自动检测：Flutter、React、Next.js、Vue、Angular、Svelte
- 结构化失败诊断，附带调查清单
- 学习数据库：SQLite中存储失败→修复模式
- 5个AI提供商：Claude、OpenAI、Gemini、DeepSeek、Ollama
- 技能模式：无需额外的AI API密钥

## 链接
- 主仓库：https://github.com/ksgisang/AI-Watch-Tester
- 技能仓库：https://github.com/ksgisang/awt-skill
- 云端演示：https://ai-watch-tester.vercel.app

在AI编码工具的帮助下构建——旨在帮助AI编码工具更好地测试。

由AILoopLab的独立开发者积极开发中。欢迎反馈！

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
