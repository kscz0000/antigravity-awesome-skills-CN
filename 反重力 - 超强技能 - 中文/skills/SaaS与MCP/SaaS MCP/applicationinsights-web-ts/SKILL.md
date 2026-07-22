---
name: applicationinsights-web-ts
description: 使用 Application Insights JavaScript SDK（@microsoft/applicationinsights-web）为浏览器/Web 应用进行埋点。适用于真实用户监控（RUM）——页面访问、点击、AJAX/fetch 依赖、异常、自定义事件，以及与后端关联的浏览器端 GenAI 代理追踪。触发词：applicationinsights、Application Insights、App Insights、RUM、真实用户监控、浏览器埋点、网页监控、JavaScript SDK、GenAI 追踪、OpenTelemetry、Web SDK、客户端遥测
risk: unknown
source: https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts
source_repo: microsoft/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/microsoft/skills/blob/main/LICENSE
---

# TypeScript 版 Application Insights JavaScript SDK（Web）
## 适用场景

当你需要使用 Application Insights JavaScript SDK（@microsoft/applicationinsights-web）为浏览器/Web 应用进行埋点时，请使用本技能。适用于真实用户监控（RUM）——页面访问、点击、AJAX/fetch 依赖、异常、自定义事件，以及与后端关联的浏览器端 GenAI 代理追踪。


通过 `@microsoft/applicationinsights-web` 为浏览器应用提供真实用户监控（RUM）。自动采集页面访问、AJAX/fetch 依赖、未处理异常，以及（搭配点击分析插件时）点击事件。支持自定义事件、指标，以及遵循 OpenTelemetry GenAI 语义约定并通过 W3C Trace Context 与后端追踪关联的 **GenAI 代理追踪**。

> **与 `azure-monitor-opentelemetry-ts` 不同**，后者用于 Node.js 服务端应用。本技能用于 **浏览器/Web** 代码（以及 React Native）。

## 实施前准备

通过 `microsoft-docs` MCP 搜索最新的 API 模式：

- 查询："Application Insights JavaScript SDK setup"
- 查询："Application Insights JavaScript SDK configuration"
- 查询："Application Insights JavaScript framework extensions React Angular"
- 校验包版本：`npm view @microsoft/applicationinsights-web version`

## 软件包

| 包名 | 用途 |
| --- | --- |
| `@microsoft/applicationinsights-web` | 核心 RUM SDK（页面访问、AJAX、异常）。 |
| `@microsoft/applicationinsights-clickanalytics-js` | 自动采集点击遥测。 |
| `@microsoft/applicationinsights-react-js` | React 插件（路由埋点、Hooks、HOC、ErrorBoundary）。 |
| `@microsoft/applicationinsights-react-native` | React Native 插件（原生崩溃、会话）。 |
| `@microsoft/applicationinsights-angularplugin-js` | Angular 插件（路由事件、ErrorHandler）。 |
| `@microsoft/applicationinsights-debugplugin-js` | 仅限开发环境的遥测检查器。 |
| `@microsoft/applicationinsights-perfmarkmeasure-js` | 与 User Timing（`performance.mark/measure`）集成。 |

## 安装

```bash
npm i --save @microsoft/applicationinsights-web
# 可选插件（仅安装你需要的）：
npm i --save @microsoft/applicationinsights-clickanalytics-js
npm i --save @microsoft/applicationinsights-react-js @microsoft/applicationinsights-react-native @microsoft/applicationinsights-angularplugin-js
```

类型定义随包一起发布——无需单独安装 `@types/...`。

## 连接字符串

浏览器 SDK 在初始化时需要连接字符串。**它会以明文形式下发到客户端** —— 浏览器遥测不支持 Microsoft Entra ID 身份验证。如果你需要将浏览器 RUM 与后端遥测隔离，请使用单独的、启用了本地身份验证的 App Insights 资源。

```bash
# Vite / CRA / Next.js —— 通过 public 环境变量前缀暴露给客户端
VITE_APPINSIGHTS_CONNECTION_STRING="InstrumentationKey=...;IngestionEndpoint=https://...;LiveEndpoint=https://..."
NEXT_PUBLIC_APPINSIGHTS_CONNECTION_STRING="InstrumentationKey=..."
```

## 快速上手（npm）

```typescript
import { ApplicationInsights } from "@microsoft/applicationinsights-web";

export const appInsights = new ApplicationInsights({
  config: {
    connectionString: import.meta.env.VITE_APPINSIGHTS_CONNECTION_STRING,
    enableAutoRouteTracking: true,        // SPA 路由变化 -> 页面访问
    enableCorsCorrelation: true,          // 将 Request-Id / traceparent 传递到跨域 AJAX
    enableRequestHeaderTracking: true,
    enableResponseHeaderTracking: true,
    distributedTracingMode: 2,            // DistributedTracingModes.AI_AND_W3C —— 输出 traceparent 以关联后端
    autoTrackPageVisitTime: true,
    disableFetchTracking: false,          // fetch() 默认会被自动埋点
    excludeRequestFromAutoTrackingPatterns: [/livemetrics\.azure\.com/i]
  }
});

appInsights.loadAppInsights();
appInsights.trackPageView();
```

应尽早调用 `loadAppInsights()`，且整个生命周期内仅调用一次（在需要被追踪的用户交互发生之前）。然后调用 `trackPageView()` 记录首次加载 —— 当 `enableAutoRouteTracking` 启用时，后续的路由变化会自动追踪。

## 快速上手（SDK 加载脚本）

当你希望 SDK 自动更新且无需构建流水线时推荐此方式。请将以下代码作为 `<head>` 中的 **第一个** `<script>` 粘贴：

```html
<script type="text/javascript" src="https://js.monitor.azure.com/scripts/b/ai.3.gbl.min.js" crossorigin="anonymous"></script>
<script type="text/javascript">
  var appInsights = window.appInsights || function (cfg) {
    /* 参考：https://learn.microsoft.com/azure/azure-monitor/app/javascript-sdk
       请使用上述 Microsoft Learn 页面中的最新代码片段 —— 它包含
       备用 CDN 故障转移（cr）、SDK 加载失败上报以及队列垫片，
       从而避免 SDK 就绪前的调用丢失。 */
  }({ src: "https://js.monitor.azure.com/scripts/b/ai.3.gbl.min.js",
      crossOrigin: "anonymous",
      cfg: { connectionString: "YOUR_CONNECTION_STRING" } });
</script>
```

仅加载器可用的 API（调用将排队，直到 SDK 加载完成）：`trackEvent`、`trackPageView`、`trackException`、`trackTrace`、`trackDependencyData`、`trackMetric`、`trackPageViewPerformance`、`startTrackPage`、`stopTrackPage`、`startTrackEvent`、`stopTrackEvent`、`addTelemetryInitializer`、`setAuthenticatedUserContext`、`clearAuthenticatedUserContext`、`flush`。

## 核心追踪 API

```typescript
// 页面访问（针对禁用了 enableAutoRouteTracking 的 SPA）
appInsights.trackPageView({ name: "Checkout", uri: "/checkout", properties: { cartSize: 3 } });

// 自定义事件（用户行为、业务事件）
appInsights.trackEvent({ name: "PurchaseCompleted" }, { orderId: "ord_123", amountUsd: 49.95 });

// 异常（已捕获的错误）
try {
  await pay(order);
} catch (err) {
  appInsights.trackException({ exception: err as Error, severityLevel: 3, properties: { orderId: order.id } });
}

// 跟踪（logs，severity 0=Verbose，1=Info，2=Warning，3=Error，4=Critical）
appInsights.trackTrace({ message: "Cart hydrated from local storage", severityLevel: 1 });

// 自定义指标（数值型）
appInsights.trackMetric({ name: "checkout.duration_ms", average: 1234 });

// 依赖项（手动追踪的外部调用 —— fetch/XHR 会被自动追踪）
appInsights.trackDependencyData({
  id: crypto.randomUUID(),
  name: "GET /api/orders",
  duration: 87, success: true, responseCode: 200,
  data: "https://api.example.com/api/orders", target: "api.example.com", type: "Fetch"
});

// 用户身份（每个已认证会话仅设置一次 —— 值为 PII，请勿传入邮箱）
appInsights.setAuthenticatedUserContext("user-id-123", "tenant-456", /*storeInCookie*/ true);
appInsights.clearAuthenticatedUserContext(); // 登出时调用

// 页面卸载前强制发送
appInsights.flush();
```

## 遥测初始化器（数据增强与过滤）

每个遥测包在发送前都会执行。返回 `false` 可丢弃该条数据。

```typescript
import type { ITelemetryItem } from "@microsoft/applicationinsights-web";

appInsights.addTelemetryInitializer((item: ITelemetryItem) => {
  item.tags ??= {};
  item.tags["ai.cloud.role"] = "web-shop";
  item.tags["ai.cloud.roleInstance"] = window.location.hostname;
  item.data ??= {};
  item.data["app.version"] = import.meta.env.VITE_APP_VERSION;
  item.data["app.build"] = import.meta.env.VITE_BUILD_SHA;

  // 丢弃嘈杂的健康检查页面访问
  if (item.baseType === "PageviewData" && item.baseData?.uri?.endsWith("/healthz")) return false;

  // 清理查询字符串中的敏感信息
  if (item.baseData?.uri) {
    item.baseData.uri = item.baseData.uri.replace(/([?&](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts/token|sig|key)=)[^&]+/gi, "$1REDACTED");
  }
});
```

## 点击分析

```typescript
import { ClickAnalyticsPlugin } from "@microsoft/applicationinsights-clickanalytics-js";

const clickPlugin = new ClickAnalyticsPlugin();
const appInsights = new ApplicationInsights({
  config: {
    connectionString: import.meta.env.VITE_APPINSIGHTS_CONNECTION_STRING,
    extensions: [clickPlugin],
    extensionConfig: {
      [clickPlugin.identifier]: {
        autoCapture: true,
        dataTags: { useDefaultContentNameOrId: true, customDataPrefix: "data-ai-" },
        urlCollectHash: false,
        behaviorValidator: (b: string) => /^[a-z0-9_]+$/.test(b) ? b : ""
      }
    }
  }
});
appInsights.loadAppInsights();
```

使用 `data-ai-*` 属性标记元素；点击事件会以 Custom Event 形式上报，并附带父级内容的元数据。

## SPA 路由追踪

- **内置方式：** 设置 `enableAutoRouteTracking: true`。会钩入 `history.pushState/replaceState` 与 `popstate`。
- **React Router：** 使用 `@microsoft/applicationinsights-react-js` 的 `withAITracking` 高阶组件（参见 [references/framework-extensions.md](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts/references/framework-extensions.md)）。
- **手动方式：** 在路由的 `useEffect` 中于路由变化时调用 `appInsights.trackPageView({ name, uri })`。请禁用 `enableAutoRouteTracking` 以避免重复计数。

## 分布式追踪（与后端关联）

设置 `distributedTracingMode: 2`（`DistributedTracingModes.AI_AND_W3C`）。SDK 会为对外的 `fetch`/`XHR` 请求注入 `traceparent`（以及旧版的 `Request-Id`）。使用 **OpenTelemetry** 埋点的后端（例如 `@azure/monitor-opentelemetry`）会自动关联到浏览器的 operation_Id。

对于跨域调用，还需设置 `enableCorsCorrelation: true`，并在 API 端的 **CORS 暴露响应头** 中加入调用来源。

## GenAI 代理追踪（OTel 语义约定）

当浏览器调用 AI 代理（函数调用、工具使用、直接来自客户端的模型调用）时，应上报属性遵循 OpenTelemetry **GenAI 语义约定** 的 App Insights **Dependency** 遥测，以便在 App Insights / Log Analytics 中可与后端代理追踪一起查询。

**首先设置 opt-in 环境变量**，使前后端埋点使用同一套 schema 版本：

```bash
OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental
```

### 必需的属性键（请原样使用 OTel 名称）

| Span / 操作 | 必需属性 |
| --- | --- |
| `invoke_agent {agent.name}` | `gen_ai.operation.name=invoke_agent`、`gen_ai.provider.name`、`gen_ai.agent.name`、`gen_ai.agent.id`（已知时） |
| `create_agent {agent.name}` | `gen_ai.operation.name=create_agent`、`gen_ai.provider.name`、`gen_ai.agent.name`、`gen_ai.request.model` |
| `chat {model}` | `gen_ai.operation.name=chat`、`gen_ai.provider.name`、`gen_ai.request.model`、`gen_ai.response.model`、`gen_ai.usage.input_tokens`、`gen_ai.usage.output_tokens` |
| `execute_tool {tool.name}` | `gen_ai.operation.name=execute_tool`、`gen_ai.tool.name`、`gen_ai.tool.type`（`function` \| `extension` \| `datastore`）、`gen_ai.tool.call.id` |

`gen_ai.provider.name` 的常见取值：`openai`、`azure.ai.openai`、`azure.ai.inference`、`anthropic`、`aws.bedrock`、`gcp.gemini`、`gcp.vertex_ai`、`cohere`、`mistral_ai`、`groq`、`deepseek`、`perplexity`、`x_ai`、`ibm.watsonx.ai`。

> **敏感内容 opt-in。** `gen_ai.system_instructions`、`gen_ai.input.messages`、`gen_ai.output.messages`、`gen_ai.tool.call.arguments`、`gen_ai.tool.call.result` 默认均为 **Opt-In**。请通过运行时开关控制，未通过审批的数据处理流程不应在生产环境中启用。

### 模式：invoke_agent 与嵌套的工具/模型追踪

```typescript
import { ApplicationInsights, SeverityLevel } from "@microsoft/applicationinsights-web";

type GenAiAttrs = Record<string, string | number | boolean | undefined>;

function startGenAiSpan(name: string, attrs: GenAiAttrs) {
  const id = crypto.randomUUID();
  const start = performance.now();
  const baseProps: GenAiAttrs = { "gen_ai.span.id": id, ...attrs };
  return {
    end(success: boolean, extra: GenAiAttrs = {}, error?: Error) {
      const duration = Math.round(performance.now() - start);
      const properties = { ...baseProps, ...extra };
      appInsights.trackDependencyData({
        id, name, duration, success,
        responseCode: error ? 500 : 200,
        type: "GenAI",
        target: String(attrs["gen_ai.provider.name"] ?? "genai"),
        properties: properties as Record<string, string>
      });
      if (error) {
        appInsights.trackException({
          exception: error,
          severityLevel: SeverityLevel.Error,
          properties: { ...properties, "error.type": error.name } as Record<string, string>
        });
      }
    }
  };
}

// 代理调用
const agentSpan = startGenAiSpan("invoke_agent ResearchAssistant", {
  "gen_ai.operation.name": "invoke_agent",
  "gen_ai.provider.name": "azure.ai.openai",
  "gen_ai.agent.name": "ResearchAssistant",
  "gen_ai.agent.id": "asst_5j66UpCpwteGg4YSxUnt7lPY",
  "gen_ai.request.model": "gpt-4o-mini",
  "server.address": "myresource.openai.azure.com"
});

try {
  // 嵌套的聊天补全追踪
  const chat = startGenAiSpan("chat gpt-4o-mini", {
    "gen_ai.operation.name": "chat",
    "gen_ai.provider.name": "azure.ai.openai",
    "gen_ai.request.model": "gpt-4o-mini"
  });
  const res = await callAzureOpenAi(/* ... */);
  chat.end(true, {
    "gen_ai.response.model": res.model,
    "gen_ai.response.id": res.id,
    "gen_ai.response.finish_reasons": JSON.stringify(res.choices.map(c => c.finish_reason)),
    "gen_ai.usage.input_tokens": res.usage.prompt_tokens,
    "gen_ai.usage.output_tokens": res.usage.completion_tokens,
    "gen_ai.output.type": "text"
  });

  // 嵌套的工具执行追踪
  const tool = startGenAiSpan("execute_tool getWeather", {
    "gen_ai.operation.name": "execute_tool",
    "gen_ai.tool.name": "getWeather",
    "gen_ai.tool.type": "function",
    "gen_ai.tool.call.id": "call_abc123"
  });
  const toolResult = await runGetWeather({ location: "SF" });
  tool.end(true);

  agentSpan.end(true, {
    "gen_ai.usage.input_tokens": res.usage.prompt_tokens,
    "gen_ai.usage.output_tokens": res.usage.completion_tokens
  });
} catch (err) {
  agentSpan.end(false, { "error.type": (err as Error).name }, err as Error);
}
```

当 `distributedTracingMode: 2` 时，浏览器的 `traceparent` 会自动附加到对外的 `fetch` 请求上，因此下游的 Azure OpenAI / 代理后端追踪都会挂载到 App Insights 中的同一个 operation_Id 下。

关于完整的属性参考、常见取值以及内容采集指引，请参阅 [references/agent-traces.md](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts/references/agent-traces.md)。

### KQL：在 App Insights 中查询 GenAI 追踪

```kusto
dependencies
| where type == "GenAI"
| extend op   = tostring(customDimensions["gen_ai.operation.name"]),
         agent = tostring(customDimensions["gen_ai.agent.name"]),
         model = tostring(customDimensions["gen_ai.request.model"]),
         tin   = toint(customDimensions["gen_ai.usage.input_tokens"]),
         tout  = toint(customDimensions["gen_ai.usage.output_tokens"])
| summarize calls=count(), p95_ms=percentile(duration, 95),
            avg_in=avg(tin), avg_out=avg(tout) by op, agent, model, bin(timestamp, 5m)
```

## React（TypeScript）

完整的 React、React Native、Angular、Next.js 与 Vite 示例请参阅 [references/framework-extensions.md](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts/references/framework-extensions.md)。

```typescript
import { ApplicationInsights } from "@microsoft/applicationinsights-web";
import { ReactPlugin, withAITracking } from "@microsoft/applicationinsights-react-js";
import { createBrowserHistory } from "history";

const reactPlugin = new ReactPlugin();
const browserHistory = createBrowserHistory();

export const appInsights = new ApplicationInsights({
  config: {
    connectionString: import.meta.env.VITE_APPINSIGHTS_CONNECTION_STRING,
    extensions: [reactPlugin],
    extensionConfig: { [reactPlugin.identifier]: { history: browserHistory } }
  }
});
appInsights.loadAppInsights();

export const TrackedCheckout = withAITracking(reactPlugin, Checkout, "Checkout");
```

## React Native

```typescript
import { ApplicationInsights } from "@microsoft/applicationinsights-web";
import { ReactNativePlugin } from "@microsoft/applicationinsights-react-native";

const rnPlugin = new ReactNativePlugin();
const appInsights = new ApplicationInsights({
  config: {
    connectionString: process.env.EXPO_PUBLIC_APPINSIGHTS_CONNECTION_STRING,
    extensions: [rnPlugin],
    disableFetchTracking: false
  }
});
appInsights.loadAppInsights();
```

## 性能 —— Web Vitals

自动采集：通过 `PerformanceTiming` / `PerformanceNavigationTiming` 获取页面加载时序。若需添加 Core Web Vitals：

```typescript
import { onCLS, onLCP, onINP, type Metric } from "web-vitals";

function send(m: Metric) {
  appInsights.trackMetric(
    { name: `web_vitals.${m.name.toLowerCase()}`, average: m.value },
    { rating: m.rating, navigationType: m.navigationType, id: m.id }
  );
}
onCLS(send); onLCP(send); onINP(send);
```

## Cookie 与隐私

```typescript
new ApplicationInsights({ config: {
  connectionString,
  isCookieUseDisabled: true,         // 彻底禁用所有 Cookie
  cookieCfg: { enabled: true, domain: ".example.com", path: "/", expiry: 365 }
}});
```

如需动态响应用户授权：

```typescript
appInsights.getCookieMgr().setEnabled(userGaveConsent);
appInsights.config.disableTelemetry = !userGaveConsent;
```

## 采样

服务端接入采样（推荐）在 App Insights 资源上配置。SDK 端采样可以减少网络流量：

```typescript
new ApplicationInsights({ config: { connectionString, samplingPercentage: 50 } });
```

按类型采样可通过遥测初始化器实现：根据 `item.baseType` 返回 `false` 来丢弃相应遥测。

## 离线 / 卸载时发送

SDK 使用 `sendBeacon`（默认 `onunloadDisableBeacon: false`）在 `pagehide` / `unload` 时刷新缓冲。对于 SPA，在销毁式跳转（登出、强制刷新）之前也应调用 `appInsights.flush()`。

## 常见陷阱

1. **不要重复初始化。** 同一模块在不同打包产物中被再次引入会导致页面访问重复上报。请使用单个共享模块导出。
2. **在首次用户输入之前完成初始化**，以免丢失早期的点击/异常事件。
3. **连接字符串是公开的** —— 切勿将同一 App Insights 资源复用于后端敏感数据。
4. **`enableAutoRouteTracking` 与手动 `trackPageView` 同时使用** 会产生重复。请二选一。
5. **CORS 分布式追踪** 要求 API 端允许 `Request-Id`、`Request-Context`、`traceparent`、`tracestate` 等请求头，并暴露 `Request-Context` 响应头。
6. **GenAI 敏感内容**（如 `gen_ai.input.messages` 等）属于 Opt-In —— 未经明确的运行时开关和审批的数据处理流程，请勿记录。
7. **代理的 token 用量记录在 `chat` 追踪上，而非 `invoke_agent`** —— 仅在确认数据时，才将汇总后的用量复制到父级 agent 追踪。
8. **React StrictMode** 在开发模式下会双重调用 effect —— 请用模块级单例来保护 `loadAppInsights()`。

## 包体积

完整的 Web SDK 压缩后约 110 KB（gzip 后约 36 KB）。若对体积要求严苛，可使用 **Loader Script** 方式使 SDK 异步加载以脱离关键路径，或对未使用的插件进行 tree-shaking。

## 关键类型

```typescript
import {
  ApplicationInsights,
  SeverityLevel,
  DistributedTracingModes,
  type IConfiguration,
  type IConfig,
  type ITelemetryItem,
  type ITelemetryPlugin,
  type ICustomProperties,
  type IPageViewTelemetry,
  type IEventTelemetry,
  type IExceptionTelemetry,
  type ITraceTelemetry,
  type IMetricTelemetry,
  type IDependencyTelemetry
} from "@microsoft/applicationinsights-web";
```

## 最佳实践

1. **单一单例实例** 从单一模块导出。
2. **尽早初始化**，在应用入口处、路由配置之前完成。
3. **使用遥测初始化器** 附加 `app.version`、`tenantId`，并清理 PII / 查询字符串中的敏感信息。
4. **设置 `distributedTracingMode: 2`**，并确保你的 API 接受/暴露 W3C trace context 头。
5. **针对 GenAI**，请原样使用 OTel `gen_ai.*` 属性名 —— 这样无论浏览器还是后端遥测都可以一致地查询。
6. **将敏感内容采集**（`gen_ai.input.messages` / `gen_ai.output.messages`）置于构建期或运行时的 opt-in 开关之后。
7. **在登出 / 敏感导航时调用 flush**，避免在途遥测丢失。

## 参考

- [references/agent-traces.md](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts/references/agent-traces.md) —— 完整的 OTel GenAI 语义约定精要（agent / model / tool 追踪、属性、内容采集）。
- [references/framework-extensions.md](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts/references/framework-extensions.md) —— React、React Native、Angular、Next.js、Vite 示例。
- [references/configuration.md](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts/references/configuration.md) —— 完整的 `IConfiguration` 参考与调优指南。
- Microsoft Learn：<https://learn.microsoft.com/azure/azure-monitor/app/javascript-sdk>
- ApplicationInsights-JS 源码：<https://github.com/microsoft/ApplicationInsights-JS>
- OTel GenAI 语义约定：<https://opentelemetry.io/docs/specs/semconv/gen-ai/>

## 使用限制

- 仅在任务明确匹配其上游来源与本地项目上下文时使用本技能。
- 在应用任何变更之前，请校验命令、生成的代码、依赖、凭据以及外部服务的行为。
- 请勿将示例视为环境特定测试、安全审查或针对破坏性/高成本操作的批准流程的替代。
