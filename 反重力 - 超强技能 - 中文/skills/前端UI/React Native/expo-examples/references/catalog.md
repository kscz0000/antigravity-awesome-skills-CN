# 示例目录（快照）

[expo/examples](https://github.com/expo/examples) 的分类视图，便于快速分诊。每条记录都是 **单一关注点的集成演示**（一个库/服务、managed 工程、通常是单屏页面）— 而非完整应用。本快照会过时 — **以实时仓库为权威来源**。在推荐或脚手架之前，请通过 `gh api repos/expo/examples/contents` 确认准确名称，并检查 `meta.json` 以获取别名/废弃信息（见 SKILL.md 第 1 步）。

使用任意名称：`npx create-expo --example <名称>`（脚手架），或通过 `gh api repos/expo/examples/contents/<名称>/<文件>` 检查它。

大多数都是单屏集成；少数有所不同：

- **全栈**（包含 Expo Router `+api` 路由 — 还附带后端）：`with-stripe`、`with-clerk`、`with-better-auth`、`with-openai`、`with-router-ai`、`with-graphql`、`with-s3`、`with-satori`。
- **较大规模展示：** `with-shadcn`、`with-router-tv`、`with-router-menus`、`with-react-navigation`、`with-webgpu`。
- **入门模板（非集成）：** `blank`、`stickersmash`。

## 身份认证
- `with-clerk` — Clerk 身份认证
- `with-auth0` — Auth0 登录
- `with-better-auth` — Better Auth
- `with-magic` — Magic 无密码登录
- `with-facebook-auth` — Facebook 登录
- `with-firebase-saml-login` — Firebase SAML 单点登录

## 支付
- `with-stripe` — Stripe 支付（原生 + Web）

## 后端、数据与存储
- `with-convex` — Convex 实时后端
- `with-legend-state-supabase` — Supabase + Legend-State 同步
- `with-firebase-storage-upload` — Firebase Storage 上传
- `with-aws-storage-upload`、`with-s3` — AWS / S3 文件上传
- `with-apollo`、`with-graphql` — GraphQL 客户端
- `with-formdata-image-upload` — multipart 图片上传

## 本地数据库与状态
- `with-sqlite` — expo-sqlite
- `with-libsql` — libSQL / Turso
- `with-tinybase` — TinyBase 本地优先存储
- `with-zustand` — Zustand 状态管理

## 导航与路由
- `with-router` — Expo Router 基础
- `with-react-navigation` — React Navigation（栈 + 标签）
- `with-drawer-navigation` — 抽屉导航器
- `with-router-menus` — 基于 Router 的原生上下文菜单
- `with-router-uniwind` — Router + Uniwind 样式
- `with-router-ai` — Router + AI 聊天界面
- `with-router-tv` — 电视端 Router
- `with-react-router` — React Router（Web）

## 样式与 UI
- `with-tailwindcss` — Tailwind / NativeWind（另见 `expo-tailwind-setup` 技能）
- `with-styled-components` — styled-components
- `with-shadcn` — shadcn 风格组件
- `with-moti` — Moti 动画
- `with-custom-font` — 自定义字体
- `with-svg` — react-native-svg
- `with-icons` — 图标集
- `with-splash-screen` — 自定义启动屏
- `with-video-background` — 全屏视频背景

## 动画与图形
- `with-reanimated` — Reanimated
- `with-skia` — React Native Skia 2D 图形
- `with-three`、`with-react-three-fiber` — three.js / R3F 3D
- `with-webgpu` — WebGPU
- `with-processing` — Processing 风格草图
- `with-react-flow` — 节点/流程图
- `with-victory-native` — 图表

## AI 与机器学习
- `with-openai` — OpenAI API
- `with-router-ai` — 基于 Expo Router 的 AI 聊天应用
- `with-google-vision` — Google Cloud Vision
- `with-tfjs-camera` — 摄像头上的 TensorFlow.js

## 媒体与设备
- `with-camera` — expo-camera
- `with-maps` — react-native-maps
- `with-webrtc` — WebRTC
- `with-pdf` — 渲染 / 查看 PDF

## Web 与渲染
- `with-nextjs` — Next.js + Expo
- `with-rsc` — React Server Components
- `with-react-strict-dom` — React Strict DOM
- `with-react-compiler` — React Compiler
- `with-html` — 渲染原始 HTML
- `with-satori` — 使用 Satori 生成 OG 图片
- `with-workbox` — service worker / PWA
- `with-webbrowser-redirect` — expo-web-browser 认证重定向

## 平台：TV、桌面小组件
- `with-tv` — Apple TV / Android TV
- `with-widgets` — iOS / Android 主屏桌面小组件

## 工具链、测试与 monorepo
- `with-typescript` — TypeScript 基线
- `with-yarn-workspaces` — Yarn monorepo
- `with-storybook` — Storybook
- `with-maestro` — Maestro 端到端测试
- `with-sentry` — Sentry 错误监控
- `with-socket-io` — Socket.IO 实时通信
- `with-github-remote-build-cache-provider` — GitHub 远程构建缓存

## 入门模板
- `blank` — 最简应用
- `stickersmash` — 教程应用