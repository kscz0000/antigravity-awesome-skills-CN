---
name: use-dom
description: 使用 Expo DOM 组件，让 Web 代码在原生平台的 webview 中运行，在 Web 平台按原样渲染，可将 Web 代码渐进式迁移到原生。涉及DOM组件、WebView、原生迁移、Expo、web代码复用、桥接原生时使用。
risk: unknown
source: https://github.com/expo/skills/tree/main/plugins/expo/skills/use-dom
source_repo: expo/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/expo/skills/blob/main/LICENSE
---

## 什么是 DOM 组件？

DOM 组件允许 Web 代码在原生平台的 webview 中按原文逐字运行，同时在 Web 平台按原样渲染。这使得你能在 Expo 应用中直接使用 `recharts`、`react-syntax-highlighter` 等仅限 Web 的库，或任何 React Web 库，无需修改。

## 适用场景

以下情况适合使用 DOM 组件：

- **仅限 Web 的库** —— 图表（recharts、chart.js）、代码高亮、富文本编辑器，或任何依赖 DOM API 的库
- **迁移 Web 代码** —— 无需重写，直接把现有的 React Web 组件带到原生
- **复杂的 HTML/CSS 布局** —— React Native 没有的 CSS 特性
- **iframe 或嵌入内容** —— 嵌入需要浏览器上下文才能运行的外部内容
- **Canvas 或 WebGL** —— 原生不支持的 Web 图形 API

## 不适用场景

以下情况应避免使用 DOM 组件：

- **对原生性能要求较高** —— Webview 会带来额外开销
- **简单的 UI** —— React Native 组件处理基础布局更高效
- **深度原生集成** —— 调用原生 API 请改用 local modules
- **布局路由** —— `_layout` 文件不能作为 DOM 组件

## 基础 DOM 组件

在文件顶部添加 `'use dom';` 指令来创建新文件：

```tsx
// components/WebChart.tsx
"use dom";

export default function WebChart({
  data,
}: {
  data: number[];
  dom: import("expo/dom").DOMProps;
}) {
  return (
    <div style={{ padding: 20 }}>
      <h2>Chart Data</h2>
      <ul>
        {data.map((value, i) => (
          <li key={i}>{value}</li>
        ))}
      </ul>
    </div>
  );
}
```

## DOM 组件的规则

1. **必须包含 `'use dom';` 指令**，写在文件顶部
2. **单一默认导出** —— 每个文件只导出一个 React 组件
3. **独立文件** —— 不能内联定义，也不能与原生组件写在同一文件
4. **只接收可序列化的 props** —— 字符串、数字、布尔值、数组、普通对象
5. **CSS 写在组件文件内** —— DOM 组件运行在隔离上下文中

## `dom` 属性

每个 DOM 组件都会接收一个特殊的 `dom` 属性，用来配置 webview。在 props 中务必声明其类型：

```tsx
"use dom";

interface Props {
  content: string;
  dom: import("expo/dom").DOMProps;
}

export default function MyComponent({ content }: Props) {
  return <div>{content}</div>;
}
```

### `dom` 属性的常用配置

```tsx
// Disable body scrolling
<DOMComponent dom={{ scrollEnabled: false }} />

// Flow under the notch (disable safe area insets)
<DOMComponent dom={{ contentInsetAdjustmentBehavior: "never" }} />

// Control size manually
<DOMComponent dom={{ style: { width: 300, height: 400 } }} />

// Combine options
<DOMComponent
  dom={{
    scrollEnabled: false,
    contentInsetAdjustmentBehavior: "never",
    style: { width: '100%', height: 500 }
  }}
/>
```

## 向 Webview 暴露原生方法

把异步函数作为 props 传入，即可将原生能力暴露给 DOM 组件：

```tsx
// app/index.tsx (native)
import { Alert } from "react-native";
import DOMComponent from "@/components/dom-component";

export default function Screen() {
  return (
    <DOMComponent
      showAlert={async (message: string) => {
        Alert.alert("From Web", message);
      }}
      saveData={async (data: { name: string; value: number }) => {
        // Save to native storage, database, etc.
        console.log("Saving:", data);
        return { success: true };
      }}
    />
  );
}
```

```tsx
// components/dom-component.tsx
"use dom";

interface Props {
  showAlert: (message: string) => Promise<void>;
  saveData: (data: {
    name: string;
    value: number;
  }) => Promise<{ success: boolean }>;
  dom?: import("expo/dom").DOMProps;
}

export default function DOMComponent({ showAlert, saveData }: Props) {
  const handleClick = async () => {
    await showAlert("Hello from the webview!");
    const result = await saveData({ name: "test", value: 42 });
    console.log("Save result:", result);
  };

  return <button onClick={handleClick}>Trigger Native Action</button>;
}
```

## 使用 Web 库

DOM 组件可以使用任意 Web 库：

```tsx
// components/syntax-highlight.tsx
"use dom";

import SyntaxHighlighter from "react-syntax-highlighter";
import { docco } from "react-syntax-highlighter/dist/esm/styles/hljs";

interface Props {
  code: string;
  language: string;
  dom?: import("expo/dom").DOMProps;
}

export default function SyntaxHighlight({ code, language }: Props) {
  return (
    <SyntaxHighlighter language={language} style={docco}>
      {code}
    </SyntaxHighlighter>
  );
}
```

```tsx
// components/chart.tsx
"use dom";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

interface Props {
  data: Array<{ name: string; value: number }>;
  dom: import("expo/dom").DOMProps;
}

export default function Chart({ data }: Props) {
  return (
    <LineChart width={400} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="value" stroke="#8884d8" />
    </LineChart>
  );
}
```

## DOM 组件中的 CSS

由于运行在隔离上下文中，CSS 导入必须放在 DOM 组件文件内：

```tsx
// components/styled-component.tsx
"use dom";

import "@/styles.css"; // CSS file in same directory

export default function StyledComponent({
  dom,
}: {
  dom: import("expo/dom").DOMProps;
}) {
  return (
    <div className="container">
      <h1 className="title">Styled Content</h1>
    </div>
  );
}
```

或者使用内联样式 / CSS-in-JS：

```tsx
"use dom";

const styles = {
  container: {
    padding: 20,
    backgroundColor: "#f0f0f0",
  },
  title: {
    fontSize: 24,
    color: "#333",
  },
};

export default function StyledComponent({
  dom,
}: {
  dom: import("expo/dom").DOMProps;
}) {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Styled Content</h1>
    </div>
  );
}
```

## DOM 组件中的 Expo Router

expo-router 的 `<Link />` 组件和路由 API 都可以在 DOM 组件中使用：

```tsx
"use dom";

import { Link, useRouter } from "expo-router";

export default function Navigation({
  dom,
}: {
  dom: import("expo/dom").DOMProps;
}) {
  const router = useRouter();

  return (
    <nav>
      <Link href="/about">About</Link>
      <button onClick={() => router.push("/settings")}>Settings</button>
    </nav>
  );
}
```

### 需要 props 配合的路由 API

下列 hooks 在 DOM 组件中无法直接使用，因为它们需要同步访问原生路由状态：

- `useLocalSearchParams()`
- `useGlobalSearchParams()`
- `usePathname()`
- `useSegments()`
- `useRootNavigation()`
- `useRootNavigationState()`

**解决办法：** 在原生父组件中读取这些值，再以 props 形式传入：

```tsx
// app/[id].tsx (native)
import { useLocalSearchParams, usePathname } from "expo-router";
import DOMComponent from "@/components/dom-component";

export default function Screen() {
  const { id } = useLocalSearchParams();
  const pathname = usePathname();

  return <DOMComponent id={id as string} pathname={pathname} />;
}
```

```tsx
// components/dom-component.tsx
"use dom";

interface Props {
  id: string;
  pathname: string;
  dom?: import("expo/dom").DOMProps;
}

export default function DOMComponent({ id, pathname }: Props) {
  return (
    <div>
      <p>Current ID: {id}</p>
      <p>Current Path: {pathname}</p>
    </div>
  );
}
```

## 检测 DOM 环境

检查代码是否运行在 DOM 组件中：

```tsx
"use dom";

import { IS_DOM } from "expo/dom";

export default function Component({
  dom,
}: {
  dom?: import("expo/dom").DOMProps;
}) {
  return <div>{IS_DOM ? "Running in DOM component" : "Running natively"}</div>;
}
```

## 资源

推荐使用 `require` 加载资源，而不是放到 public 目录：

```tsx
"use dom";

// Good - bundled with the component
const logo = require("../assets/logo.png");

export default function Component({
  dom,
}: {
  dom: import("expo/dom").DOMProps;
}) {
  return <img src={logo} alt="Logo" />;
}
```

## 在原生组件中使用

像普通组件一样导入并使用 DOM 组件：

```tsx
// app/index.tsx
import { View, Text } from "react-native";
import WebChart from "@/components/web-chart";
import CodeBlock from "@/components/code-block";

export default function HomeScreen() {
  return (
    <View style={{ flex: 1 }}>
      <Text>Native content above</Text>

      <WebChart data={[10, 20, 30, 40, 50]} dom={{ style: { height: 300 } }} />

      <CodeBlock
        code="const x = 1;"
        language="javascript"
        dom={{ scrollEnabled: true }}
      />

      <Text>Native content below</Text>
    </View>
  );
}
```

## 平台行为

| 平台   | 渲染方式                            |
| ------ | ----------------------------------- |
| iOS    | 在 WKWebView 中渲染                 |
| Android | 在 WebView 中渲染                   |
| Web    | 按原样渲染（无 webview 包装）       |

在 Web 平台上，`dom` 属性会被忽略，因为不需要 webview。

## 实用建议

- 开发期间 DOM 组件支持热更新
- 保持 DOM 组件职责单一 —— 不要把整个页面塞进 webview
- 导航栏用原生组件，特化的内容用 DOM 组件
- 在所有平台上测试 —— Web 渲染与原生 webview 之间可能存在细微差异
- 较大的 DOM 组件可能影响性能 —— 如有需要请进行性能分析
- webview 拥有独立的 JavaScript 上下文 —— 无法直接与原生共享状态

## 限制

- 仅在任务范围与上游产品或 API 范围明确匹配时使用本技能。
- 在做任何变更前，请对照当前官方文档核对命令、API 行为、定价、配额、凭据及部署影响。
- 不要把生成的示例当作针对特定环境的测试、安全审查或破坏性/高成本操作的审批替代品。
