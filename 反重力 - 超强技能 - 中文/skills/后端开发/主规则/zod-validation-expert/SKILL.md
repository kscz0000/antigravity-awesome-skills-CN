---
name: zod-validation-expert
description: "Zod 专家——TypeScript 优先的 schema 验证。涵盖解析、自定义错误、refinements、类型推断，以及与 React Hook Form、Next.js、tRPC 的集成。触发词：Zod、schema 验证、TypeScript 验证、zodResolver、tRPC、Next.js 表单验证、环境变量校验。"
risk: safe
source: community
date_added: "2026-03-05"
---

# Zod 验证专家

你是一名生产级 Zod 专家。你帮助开发者构建类型安全的 schema 定义和验证逻辑。你精通 Zod 基础（primitives、objects、arrays、records）、类型推断（`z.infer`）、复杂验证（`.refine`、`.superRefine`）、转换（`.transform`），以及与现代 TypeScript 生态的集成（React Hook Form、Next.js API Routes / App Router Actions、tRPC 以及环境变量）。

## 何时使用此技能

- 用于为 API 输入或表单定义 TypeScript 验证 schema 时
- 用于设置环境变量验证时（`process.env`）
- 用于将 Zod 与 React Hook Form 集成时（`@hookform/resolvers/zod`）
- 用于从运行时验证 schema 中提取或推断 TypeScript 类型时
- 用于编写复杂验证规则时（例如跨字段验证、异步验证）
- 用于转换输入数据时（例如 string 转 Date、string 转 number 强制类型转换）
- 用于标准化错误消息格式时

## 核心概念

### 为什么选择 Zod？

Zod 消除了既编写 TypeScript 接口*又*编写运行时验证 schema 的重复劳动。你只需定义一次 schema，Zod 便会推断出静态的 TypeScript 类型。请注意，Zod 用于**解析，而不仅仅是验证**。`safeParse` 和 `parse` 返回干净的、带类型的数据，默认会剥离未知键。

## Schema 定义与推断

### Primitives 与 Coercion

```typescript
import { z } from "zod";

// 基础 primitives
const stringSchema = z.string().min(3).max(255);
const numberSchema = z.number().int().positive();
const dateSchema = z.date();

// Coercion（在验证前自动转换输入）
// 在 Next.js Server Actions 的 FormData 或 URL 查询参数中非常有用
const ageSchema = z.coerce.number().min(18); // "18" -> 18
const activeSchema = z.coerce.boolean(); // "true" -> true
const dobSchema = z.coerce.date(); // "2020-01-01" -> Date 对象
```

### Objects 与类型推断

```typescript
const UserSchema = z.object({
  id: z.string().uuid(),
  username: z.string().min(3).max(20),
  email: z.string().email(),
  role: z.enum(["ADMIN", "USER", "GUEST"]).default("USER"),
  age: z.number().min(18).optional(), // 可以省略
  website: z.string().url().nullable(), // 可以为 null
  tags: z.array(z.string()).min(1), // 至少包含 1 个元素的数组
});

// 直接从 schema 推断 TypeScript 类型
// 无需单独编写 `interface User { ... }`
export type User = z.infer<typeof UserSchema>;
```

### 高级类型

```typescript
// Records（具有动态 key 但具有特定 value 类型的对象）
const envSchema = z.record(z.string(), z.string()); // Record<string, string>

// Unions（或）
const idSchema = z.union([z.string(), z.number()]); // string | number
// 或更简洁的写法：
const idSchema2 = z.string().or(z.number());

// Discriminated Unions（类型安全的 switch 分支）
const ActionSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("create"), id: z.string() }),
  z.object({ type: z.literal("update"), id: z.string(), data: z.any() }),
  z.object({ type: z.literal("delete"), id: z.string() }),
]);
```

## 解析与验证

### parse vs safeParse

```typescript
const schema = z.string().email();

// ❌ parse：验证失败时抛出 ZodError
try {
  const email = schema.parse("invalid-email");
} catch (err) {
  if (err instanceof z.ZodError) {
    console.error(err.issues);
  }
}

// ✅ safeParse：返回结果对象（无需 try/catch）
const result = schema.safeParse("user@example.com");

if (!result.success) {
  // TypeScript 将 result 收窄为 SafeParseError
  console.log(result.error.format()); 
  // 提前返回或抛出领域错误
} else {
  // TypeScript 将 result 收窄为 SafeParseSuccess
  const validEmail = result.data; // 类型为 `string`
}
```

## 自定义验证

### 自定义错误消息

```typescript
const passwordSchema = z.string()
  .min(8, { message: "密码长度至少为 8 个字符" })
  .max(100, { message: "密码过长" })
  .regex(/[A-Z]/, { message: "密码必须至少包含一个大写字母" })
  .regex(/[0-9]/, { message: "密码必须至少包含一个数字" });

// 全局自定义错误映射（可用于国际化）
z.setErrorMap((issue, ctx) => {
  if (issue.code === z.ZodIssueCode.invalid_type) {
    if (issue.expected === "string") return { message: "该字段必须为文本" };
  }
  return { message: ctx.defaultError };
});
```

### Refinements（自定义逻辑）

```typescript
// 基础 refinement
const passwordCheck = z.string().refine((val) => val !== "password123", {
  message: "密码强度不足",
});

// 跨字段验证（例如密码匹配）
const formSchema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "两次输入的密码不一致",
  path: ["confirmPassword"], // 将错误挂载到具体字段
});
```

### Transformations

```typescript
// 在解析过程中转换数据
const stringToNumber = z.string()
  .transform((val) => parseInt(val, 10))
  .refine((val) => !isNaN(val), { message: "不是有效的整数" });

// 现在推断出的类型是 `number`，而不是 `string`！
type TransformedResult = z.infer<typeof stringToNumber>; // number
```

## 集成模式

### React Hook Form

```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const loginSchema = z.object({
  email: z.string().email("邮箱地址无效"),
  password: z.string().min(6, "密码长度至少 6 个字符"),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema)
  });

  const onSubmit = (data: LoginFormValues) => {
    // data 已完成类型校验与验证
    console.log(data.email, data.password);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("email")} />
      {errors.email && <span>{errors.email.message}</span>}
      {/* ... */}
    </form>
  );
}
```

### Next.js Server Actions

```typescript
"use server";
import { z } from "zod";

// 这里的 Coercion 至关重要，因为 FormData 的值始终是字符串
const createPostSchema = z.object({
  title: z.string().min(3),
  content: z.string().optional(),
  published: z.coerce.boolean().default(false), // checkbox -> "on" -> true
});

export async function createPost(prevState: any, formData: FormData) {
  // 使用 Object.fromEntries 将 FormData 转换为普通对象
  const rawData = Object.fromEntries(formData.entries());
  
  const validatedFields = createPostSchema.safeParse(rawData);
  
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }
  
  // 使用校验通过的数据继续执行数据库操作
  const { title, content, published } = validatedFields.data;
  // ...
  return { success: true };
}
```

### 环境变量

```typescript
// 让环境变量严格类型化并在启动时快速失败
import { z } from "zod";

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
  PORT: z.coerce.number().default(3000),
  API_KEY: z.string().min(10),
});

// 当环境变量缺失或无效时，构建立即失败
const env = envSchema.parse(process.env);

export default env;
```

## 最佳实践

- ✅ **应当：** 将 schema 与使用它们的组件或 API 路由放在一起维护，以保持关注点分离。
- ✅ **应当：** 在所有地方使用 `z.infer<typeof Schema>`，而不是手动维护重复的 TypeScript 接口。
- ✅ **应当：** 优先使用 `safeParse` 而非 `parse`，以避免分散的 `try/catch` 块，并借助 TypeScript 的控制流收窄实现健壮的错误处理。
- ✅ **应当：** 在接受来自 `URLSearchParams` 或 `FormData` 的数据时使用 `z.coerce`，并注意 `z.coerce.boolean()` 会在不做自定义预处理的情况下，将标准的 `"false"`/`"off"` 字符串意外地转换。
- ✅ **应当：** 对 `ZodError` 对象使用 `.flatten()` 或 `.format()`，以方便地提取可序列化、人类可读的错误信息供前端使用。
- ❌ **不要：** 当创建和更新操作的字段类型或约束不同时，仅依赖 `.partial()` 来生成更新 schema；应当定义不同的 schema。
- ❌ **不要：** 在执行对象级跨字段验证时忘记在 `.refine()` 或 `.superRefine()` 中传递 `path` 选项，否则错误将不会附加到正确的输入字段上。

## 故障排查

**问题：** `Type instantiation is excessively deep and possibly infinite.`
**解决方案：** 这种情况出现在极端的 schema 递归中（例如深度嵌套的自引用 schema）。对递归结构使用 `z.lazy(() => NodeSchema)`，并显式定义基础 TypeScript 类型，而不是仅依靠推断。

**问题：** 使用 `.optional()` 时空字符串能通过验证。
**解决方案：** `.optional()` 允许 `undefined`，并不允许空字符串。如果空字符串表示"无值"，请使用 `.or(z.literal(""))` 或进行预处理：`z.string().transform(v => v === "" ? undefined : v).optional()`。

## 局限性
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来询问澄清。
