---
name: makepad-reference
description: "提供调试、代码质量和高级布局模式的参考材料。当用户要求'Makepad调试'、'Makepad参考'、'Makepad错误排查'或'Makepad布局'时使用。"
risk: unknown
source: community
---

# Makepad 参考

本类别提供调试、代码质量和高级布局模式的参考材料。

## 适用场景
- 需要快速查阅 Makepad 常见错误、调试方法或 API 用法
- 任务偏向诊断或查阅参考，而非在某个子系统中编写特定功能
- 在深入更专业的 Makepad 技能之前，需要一个统一的入口

## 快速导航

| 主题 | 内容 | 适用场景 |
|------|------|----------|
| API 文档 | 官方文档索引、快速 API 参考 | 查找详细 API 信息 |
| 故障排查 | 常见错误及修复方法 | 构建失败、运行时错误 |
| 代码质量 | 符合 Makepad 规范的重构 | 安全地简化代码 |
| 自适应布局 | 桌面端/移动端响应式 | 跨平台布局 |

## 常见问题速查

| 错误 | 快速修复 |
|------|----------|
| `no matching field: font` | 改用 `text_style: <THEME_FONT_*>{}` |
| 颜色解析错误（以 `e` 结尾） | 修改末位数字（如 `#14141e` → `#14141f`） |
| `set_text` 缺少参数 | 添加 `cx` 作为第一个参数 |
| UI 未更新 | 修改后调用 `redraw(cx)` |
| 找不到 Widget | 检查 ID 拼写，使用 `ids!()` 生成路径 |

## 调试技巧

```bash
# Run with line info for better error messages
MAKEPAD=lines cargo +nightly run
```

```rust
// Add logging
log!("Value: {:?}", my_value);
log!("State: {} / {}", self.counter, self.is_loading);
```

## 资源

- [Makepad 官方文档](https://publish.obsidian.md/makepad-docs/) - 基于 Obsidian 的文档
- [Makepad 仓库](https://github.com/makepad/makepad)
- [Robrix](https://github.com/project-robius/robrix) - 生产级参考项目
- [Moly](https://github.com/moxin-org/moly) - 生产级参考项目

## 限制
- 仅在任务明确符合上述范围时使用本技能
- 输出内容不能替代环境验证、测试或专家审查
- 若缺少必要的输入、权限、安全边界或成功标准，应停下来请求澄清
