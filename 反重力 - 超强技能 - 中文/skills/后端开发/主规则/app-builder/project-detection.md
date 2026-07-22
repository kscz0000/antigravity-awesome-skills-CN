# 项目类型检测

> 分析用户请求以确定项目类型和模板。

## 关键词矩阵

| 关键词 | 项目类型 | 模板 |
|----------|--------------|----------|
| blog, post, article | 博客 | astro-static |
| e-commerce, product, cart, payment | 电商 | nextjs-saas |
| dashboard, panel, management | 管理后台 | nextjs-fullstack |
| api, backend, service, rest | API 服务 | express-api |
| python, fastapi, django | Python API | python-fastapi |
| mobile, android, ios, react native | 移动应用 (RN) | react-native-app |
| flutter, dart | 移动应用 (Flutter) | flutter-app |
| portfolio, personal, cv | 个人作品集 | nextjs-static |
| crm, customer, sales | CRM | nextjs-fullstack |
| saas, subscription, stripe | SaaS | nextjs-saas |
| landing, promotional, marketing | 落地页 | nextjs-static |
| docs, documentation | 文档站 | astro-static |
| extension, plugin, chrome | 浏览器扩展 | chrome-extension |
| desktop, electron | 桌面应用 | electron-desktop |
| cli, command line, terminal | CLI 工具 | cli-tool |
| monorepo, workspace | Monorepo | monorepo-turborepo |

## 检测流程

```
1. 对用户请求进行分词
2. 提取关键词
3. 确定项目类型
4. 检测缺失信息 → 转发给 conversation-manager
5. 建议技术栈
```
