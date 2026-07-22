# 验证模式 - 使用 Zod 进行输入验证

使用 Zod schema 实现类型安全输入验证的完整指南。

## 目录

- [为什么选择 Zod？](#why-zod)
- [Zod 基础模式](#basic-zod-patterns)
- [代码库中的 Schema 示例](#schema-examples-from-codebase)
- [路由级验证](#route-level-validation)
- [控制器验证](#controller-validation)
- [DTO 模式](#dto-pattern)
- [错误处理](#error-handling)
- [高级模式](#advanced-patterns)

---

## Why Zod?

### 相比 Joi/其他库的优势

**类型安全：**
- ✅ 完整的 TypeScript 类型推断
- ✅ 运行时 + 编译时双重验证
- ✅ 自动生成类型定义

**开发体验：**
- ✅ 直观的 API
- ✅ 可组合的 schema
- ✅ 友好的错误提示

**性能：**
- ✅ 快速验证
- ✅ 包体积小
- ✅ 支持 Tree-shaking

### 从 Joi 迁移

现代验证应使用 Zod 替代 Joi：

```typescript
// ❌ 旧版 - Joi（逐步淘汰）
const schema = Joi.object({
    email: Joi.string().email().required(),
    name: Joi.string().min(3).required(),
});

// ✅ 新版 - Zod（推荐）
const schema = z.object({
    email: z.string().email(),
    name: z.string().min(3),
});
```

---

## Basic Zod Patterns

### 基本类型

```typescript
import { z } from 'zod';

// Strings
const nameSchema = z.string();
const emailSchema = z.string().email();
const urlSchema = z.string().url();
const uuidSchema = z.string().uuid();
const minLengthSchema = z.string().min(3);
const maxLengthSchema = z.string().max(100);

// Numbers
const ageSchema = z.number().int().positive();
const priceSchema = z.number().positive();
const rangeSchema = z.number().min(0).max(100);

// Booleans
const activeSchema = z.boolean();

// Dates
const dateSchema = z.string().datetime(); // ISO 8601 string
const nativeDateSchema = z.date(); // Native Date object

// Enums
const roleSchema = z.enum(['admin', 'operations', 'user']);
const statusSchema = z.enum(['PENDING', 'APPROVED', 'REJECTED']);
```

### 对象

```typescript
// 简单对象
const userSchema = z.object({
    email: z.string().email(),
    name: z.string(),
    age: z.number().int().positive(),
});

// 嵌套对象
const addressSchema = z.object({
    street: z.string(),
    city: z.string(),
    zipCode: z.string().regex(/^\d{5}$/),
});

const userWithAddressSchema = z.object({
    name: z.string(),
    address: addressSchema,
});

// 可选字段
const userSchema = z.object({
    name: z.string(),
    email: z.string().email().optional(),
    phone: z.string().optional(),
});

// 可空字段
const userSchema = z.object({
    name: z.string(),
    middleName: z.string().nullable(),
});
```

### 数组

```typescript
// 基本类型数组
const rolesSchema = z.array(z.string());
const numbersSchema = z.array(z.number());

// 对象数组
const usersSchema = z.array(
    z.object({
        id: z.string(),
        name: z.string(),
    })
);

// 带约束的数组
const tagsSchema = z.array(z.string()).min(1).max(10);
const nonEmptyArray = z.array(z.string()).nonempty();
```

---

## Schema Examples from Codebase

### 表单验证 Schema

**文件：** `/form/src/helpers/zodSchemas.ts`

```typescript
import { z } from 'zod';

// Question types enum
export const questionTypeSchema = z.enum([
    'input',
    'textbox',
    'editor',
    'dropdown',
    'autocomplete',
    'checkbox',
    'radio',
    'upload',
]);

// Upload types
export const uploadTypeSchema = z.array(
    z.enum(['pdf', 'image', 'excel', 'video', 'powerpoint', 'word']).nullable()
);

// Input types
export const inputTypeSchema = z
    .enum(['date', 'number', 'input', 'currency'])
    .nullable();

// Question option
export const questionOptionSchema = z.object({
    id: z.number().int().positive().optional(),
    controlTag: z.string().max(150).nullable().optional(),
    label: z.string().max(100).nullable().optional(),
    order: z.number().int().min(0).default(0),
});

// Question schema
export const questionSchema = z.object({
    id: z.number().int().positive().optional(),
    formID: z.number().int().positive(),
    sectionID: z.number().int().positive().optional(),
    options: z.array(questionOptionSchema).optional(),
    label: z.string().max(500),
    description: z.string().max(5000).optional(),
    type: questionTypeSchema,
    uploadTypes: uploadTypeSchema.optional(),
    inputType: inputTypeSchema.optional(),
    tags: z.array(z.string().max(150)).optional(),
    required: z.boolean(),
    isStandard: z.boolean().optional(),
    deprecatedKey: z.string().nullable().optional(),
    maxLength: z.number().int().positive().nullable().optional(),
    isOptionsSorted: z.boolean().optional(),
});

// Form section schema
export const formSectionSchema = z.object({
    id: z.number().int().positive(),
    formID: z.number().int().positive(),
    questions: z.array(questionSchema).optional(),
    label: z.string().max(500),
    description: z.string().max(5000).optional(),
    isStandard: z.boolean(),
});

// Create form schema
export const createFormSchema = z.object({
    id: z.number().int().positive(),
    label: z.string().max(150),
    description: z.string().max(6000).nullable().optional(),
    isPhase: z.boolean().optional(),
    username: z.string(),
});

// Update order schema
export const updateOrderSchema = z.object({
    source: z.object({
        index: z.number().int().min(0),
        sectionID: z.number().int().min(0),
    }),
    destination: z.object({
        index: z.number().int().min(0),
        sectionID: z.number().int().min(0),
    }),
});

// Controller-specific validation schemas
export const createQuestionValidationSchema = z.object({
    formID: z.number().int().positive(),
    sectionID: z.number().int().positive(),
    question: questionSchema,
    index: z.number().int().min(0).nullable().optional(),
    username: z.string(),
});

export const updateQuestionValidationSchema = z.object({
    questionID: z.number().int().positive(),
    username: z.string(),
    question: questionSchema,
});
```

### 代理关系 Schema

```typescript
// Proxy relationship validation
const createProxySchema = z.object({
    originalUserID: z.string().min(1),
    proxyUserID: z.string().min(1),
    startsAt: z.string().datetime(),
    expiresAt: z.string().datetime(),
});

// With custom validation
const createProxySchemaWithValidation = createProxySchema.refine(
    (data) => new Date(data.expiresAt) > new Date(data.startsAt),
    {
        message: 'expiresAt must be after startsAt',
        path: ['expiresAt'],
    }
);
```

### 工作流验证

```typescript
// Workflow start schema
const startWorkflowSchema = z.object({
    workflowCode: z.string().min(1),
    entityType: z.enum(['Post', 'User', 'Comment']),
    entityID: z.number().int().positive(),
    dryRun: z.boolean().optional().default(false),
});

// Workflow step completion schema
const completeStepSchema = z.object({
    stepInstanceID: z.number().int().positive(),
    answers: z.record(z.string(), z.any()),
    dryRun: z.boolean().optional().default(false),
});
```

---

## Route-Level Validation

### 模式 1：内联验证

```typescript
// routes/proxyRoutes.ts
import { z } from 'zod';

const createProxySchema = z.object({
    originalUserID: z.string().min(1),
    proxyUserID: z.string().min(1),
    startsAt: z.string().datetime(),
    expiresAt: z.string().datetime(),
});

router.post(
    '/',
    SSOMiddlewareClient.verifyLoginStatus,
    async (req, res) => {
        try {
            // Validate at route level
            const validated = createProxySchema.parse(req.body);

            // Delegate to service
            const proxy = await proxyService.createProxyRelationship(validated);

            res.status(201).json({ success: true, data: proxy });
        } catch (error) {
            if (error instanceof z.ZodError) {
                return res.status(400).json({
                    success: false,
                    error: {
                        message: 'Validation failed',
                        details: error.errors,
                    },
                });
            }
            handler.handleException(res, error);
        }
    }
);
```

**优点：**
- 快速简洁
- 适合简单路由

**缺点：**
- 验证逻辑写在路由里
- 难以测试
- 不可复用

---

## Controller Validation

### 模式 2：控制器验证（推荐）

```typescript
// validators/userSchemas.ts
import { z } from 'zod';

export const createUserSchema = z.object({
    email: z.string().email(),
    name: z.string().min(2).max(100),
    roles: z.array(z.enum(['admin', 'operations', 'user'])),
    isActive: z.boolean().default(true),
});

export const updateUserSchema = z.object({
    email: z.string().email().optional(),
    name: z.string().min(2).max(100).optional(),
    roles: z.array(z.enum(['admin', 'operations', 'user'])).optional(),
    isActive: z.boolean().optional(),
});

export type CreateUserDTO = z.infer<typeof createUserSchema>;
export type UpdateUserDTO = z.infer<typeof updateUserSchema>;
```

```typescript
// controllers/UserController.ts
import { Request, Response } from 'express';
import { BaseController } from './BaseController';
import { UserService } from '../services/userService';
import { createUserSchema, updateUserSchema } from '../validators/userSchemas';
import { z } from 'zod';

export class UserController extends BaseController {
    private userService: UserService;

    constructor() {
        super();
        this.userService = new UserService();
    }

    async createUser(req: Request, res: Response): Promise<void> {
        try {
            // Validate input
            const validated = createUserSchema.parse(req.body);

            // Call service
            const user = await this.userService.createUser(validated);

            this.handleSuccess(res, user, 'User created successfully', 201);
        } catch (error) {
            if (error instanceof z.ZodError) {
                // Handle validation errors with 400 status
                return this.handleError(error, res, 'createUser', 400);
            }
            this.handleError(error, res, 'createUser');
        }
    }

    async updateUser(req: Request, res: Response): Promise<void> {
        try {
            // Validate params and body
            const userId = req.params.id;
            const validated = updateUserSchema.parse(req.body);

            const user = await this.userService.updateUser(userId, validated);

            this.handleSuccess(res, user, 'User updated successfully');
        } catch (error) {
            if (error instanceof z.ZodError) {
                return this.handleError(error, res, 'updateUser', 400);
            }
            this.handleError(error, res, 'updateUser');
        }
    }
}
```

**优点：**
- 职责分离清晰
- Schema 可复用
- 易于测试
- 类型安全的 DTO

**缺点：**
- 需要管理更多文件

---

## DTO Pattern

### 从 Schema 推导类型

```typescript
import { z } from 'zod';

// Define schema
const createUserSchema = z.object({
    email: z.string().email(),
    name: z.string(),
    age: z.number().int().positive(),
});

// Infer TypeScript type from schema
type CreateUserDTO = z.infer<typeof createUserSchema>;

// Equivalent to:
// type CreateUserDTO = {
//     email: string;
//     name: string;
//     age: number;
// }

// Use in service
class UserService {
    async createUser(data: CreateUserDTO): Promise<User> {
        // data is fully typed!
        console.log(data.email); // ✅ TypeScript knows this exists
        console.log(data.invalid); // ❌ TypeScript error!
    }
}
```

### 输入类型与输出类型

```typescript
// Input schema (what API receives)
const createUserInputSchema = z.object({
    email: z.string().email(),
    name: z.string(),
    password: z.string().min(8),
});

// Output schema (what API returns)
const userOutputSchema = z.object({
    id: z.string().uuid(),
    email: z.string().email(),
    name: z.string(),
    createdAt: z.string().datetime(),
    // password excluded!
});

type CreateUserInput = z.infer<typeof createUserInputSchema>;
type UserOutput = z.infer<typeof userOutputSchema>;
```

---

## Error Handling

### Zod 错误格式

```typescript
try {
    const validated = schema.parse(data);
} catch (error) {
    if (error instanceof z.ZodError) {
        console.log(error.errors);
        // [
        //   {
        //     code: 'invalid_type',
        //     expected: 'string',
        //     received: 'number',
        //     path: ['email'],
        //     message: 'Expected string, received number'
        //   }
        // ]
    }
}
```

### 自定义错误信息

```typescript
const userSchema = z.object({
    email: z.string().email({ message: 'Please provide a valid email address' }),
    name: z.string().min(2, { message: 'Name must be at least 2 characters' }),
    age: z.number().int().positive({ message: 'Age must be a positive number' }),
});
```

### 格式化错误响应

```typescript
// Helper function to format Zod errors
function formatZodError(error: z.ZodError) {
    return {
        message: 'Validation failed',
        errors: error.errors.map((err) => ({
            field: err.path.join('.'),
            message: err.message,
            code: err.code,
        })),
    };
}

// In controller
catch (error) {
    if (error instanceof z.ZodError) {
        return res.status(400).json({
            success: false,
            error: formatZodError(error),
        });
    }
}

// Response example:
// {
//   "success": false,
//   "error": {
//     "message": "Validation failed",
//     "errors": [
//       {
//         "field": "email",
//         "message": "Invalid email",
//         "code": "invalid_string"
//       }
//     ]
//   }
// }
```

---

## Advanced Patterns

### 条件验证

```typescript
// Validate based on other field values
const submissionSchema = z.object({
    type: z.enum(['NEW', 'UPDATE']),
    postId: z.number().optional(),
}).refine(
    (data) => {
        // If type is UPDATE, postId is required
        if (data.type === 'UPDATE') {
            return data.postId !== undefined;
        }
        return true;
    },
    {
        message: 'postId is required when type is UPDATE',
        path: ['postId'],
    }
);
```

### 数据转换

```typescript
// Transform strings to numbers
const userSchema = z.object({
    name: z.string(),
    age: z.string().transform((val) => parseInt(val, 10)),
});

// Transform dates
const eventSchema = z.object({
    name: z.string(),
    date: z.string().transform((str) => new Date(str)),
});
```

### 数据预处理

```typescript
// Trim strings before validation
const userSchema = z.object({
    email: z.preprocess(
        (val) => typeof val === 'string' ? val.trim().toLowerCase() : val,
        z.string().email()
    ),
    name: z.preprocess(
        (val) => typeof val === 'string' ? val.trim() : val,
        z.string().min(2)
    ),
});
```

### 联合类型

```typescript
// Multiple possible types
const idSchema = z.union([z.string(), z.number()]);

// Discriminated unions
const notificationSchema = z.discriminatedUnion('type', [
    z.object({
        type: z.literal('email'),
        recipient: z.string().email(),
        subject: z.string(),
    }),
    z.object({
        type: z.literal('sms'),
        phoneNumber: z.string(),
        message: z.string(),
    }),
]);
```

### 递归 Schema

```typescript
// For nested structures like trees
type Category = {
    id: number;
    name: string;
    children?: Category[];
};

const categorySchema: z.ZodType<Category> = z.lazy(() =>
    z.object({
        id: z.number(),
        name: z.string(),
        children: z.array(categorySchema).optional(),
    })
);
```

### Schema 组合

```typescript
// Base schemas
const timestampsSchema = z.object({
    createdAt: z.string().datetime(),
    updatedAt: z.string().datetime(),
});

const auditSchema = z.object({
    createdBy: z.string(),
    updatedBy: z.string(),
});

// Compose schemas
const userSchema = z.object({
    id: z.string(),
    email: z.string().email(),
    name: z.string(),
}).merge(timestampsSchema).merge(auditSchema);

// Extend schemas
const adminUserSchema = userSchema.extend({
    adminLevel: z.number().int().min(1).max(5),
    permissions: z.array(z.string()),
});

// Pick specific fields
const publicUserSchema = userSchema.pick({
    id: true,
    name: true,
    // email excluded
});

// Omit fields
const userWithoutTimestamps = userSchema.omit({
    createdAt: true,
    updatedAt: true,
});
```

### 验证中间件

```typescript
// Create reusable validation middleware
import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';

export function validateBody<T extends z.ZodType>(schema: T) {
    return (req: Request, res: Response, next: NextFunction) => {
        try {
            req.body = schema.parse(req.body);
            next();
        } catch (error) {
            if (error instanceof z.ZodError) {
                return res.status(400).json({
                    success: false,
                    error: {
                        message: 'Validation failed',
                        details: error.errors,
                    },
                });
            }
            next(error);
        }
    };
}

// Usage
router.post('/users',
    validateBody(createUserSchema),
    async (req, res) => {
        // req.body is validated and typed!
        const user = await userService.createUser(req.body);
        res.json({ success: true, data: user });
    }
);
```

---

**相关文件：**
- SKILL.md - 主指南
- [routing-and-controllers.md](routing-and-controllers.md) - 在控制器中使用验证
- [services-and-repositories.md](services-and-repositories.md) - 在服务中使用 DTO
- [async-and-errors.md](async-and-errors.md) - 错误处理模式
