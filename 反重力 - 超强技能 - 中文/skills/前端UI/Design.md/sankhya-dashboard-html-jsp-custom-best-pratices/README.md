# Sankhya 仪表盘自定义最佳实践

本技能提供了一套全面的最佳实践、高级模式和结构指南，用于在Sankhya生态系统中开发自定义HTML/JSP仪表盘。

Sankhya ERP部署通常需要创建自定义可视化、操作仪表盘和动态报告。要有效开发这些组件，需要遵循特定的架构模式、安全的查询实践和一致的界面设计。本技能作为一个协作蓝图，将社区驱动的标准直接注入您的开发工作流。

## 功能特性

- **JSP/JSTL 代码质量**：强制使用 `core_rt`、安全参数、全局状态模式，并严格分离业务逻辑与表现层。
- **视觉标识标准**：注入基础CSS令牌，用于标准化生态系统内仪表盘的UI，确保视觉一致性和更好的用户体验。
- **SQL 最佳实践**：强调安全的查询参数、使用 `DBExplorer` 进行数据库探索技术，以及在Sankhya内正确的索引映射。
- **BI 组件流程**：概述构建交互式组件的方法，涵盖下钻、多层导航（`openLevel`）、模态框操作以及异步数据加载的弹性。
- **安全协议**：关于防止直接SQL注入、处理用户会话（`CODUSU_LOG`）以及按用户组权限限定行级安全的指南。

## 安装

本技能可以按仓库本地安装，也可以全局安装以供所有Sankhya开发项目使用。

### 全局安装（推荐）
此方法设置一个符号链接，使技能在您工作的任何仓库中都可用。从克隆的 `cli-ai-skills` 目录根目录运行以下命令：

#### 适用于 Claude Code
```bash
mkdir -p ~/.claude/skills
ln -sf $(pwd)/skills/sankhya-dashboard-html-jsp-custom-best-pratices ~/.claude/skills/sankhya-dashboard-html-jsp-custom-best-pratices
```

#### 适用于 GitHub Copilot CLI
```bash
mkdir -p ~/.copilot/skills
ln -sf $(pwd)/skills/sankhya-dashboard-html-jsp-custom-best-pratices ~/.copilot/skills/sankhya-dashboard-html-jsp-custom-best-pratices
```

### 本地仓库安装
如果您希望将技能限制在特定项目工作区，只需将该目录移动或复制到项目的本地AI注册文件夹中（例如 `.claude/skills/` 或 `.github/skills/`）。

## 使用示例

安装后，当讨论Sankhya仪表盘时，此技能会自动触发。尝试使用以下示例提示词与您的AI助手：

- *“创建一个Sankhya仪表盘的初始结构，包含一个基础表格和JSTL集成。”*
- *“Sankhya中在JSP里构建参数化SQL查询的最佳实践是什么？”*
- *“分析我这个Sankhya小部件的JSP，并基于sankhya-dashboard技能提出改进建议。”*
- *“如何在Sankhya的HTML5中使用openLevel函数创建多层下钻？”*
- *“生成Sankhya技能推荐的标准CSS（.card、颜色变量）。”*

通过参考此技能，AI将使用为Sankhya开发映射出的具体技术笔记来组织其响应。