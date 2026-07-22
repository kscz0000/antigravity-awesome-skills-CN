# 服务与仓库 - 业务逻辑层

使用服务组织业务逻辑、使用仓库进行数据访问的完整指南。

## 目录

- [服务层概览](#service-layer-overview)
- [依赖注入模式](#dependency-injection-pattern)
- [单例模式](#singleton-pattern)
- [仓库模式](#repository-pattern)
- [服务设计原则](#service-design-principles)
- [缓存策略](#caching-strategies)
- [服务测试](#testing-services)

---

## 服务层概览

### 服务的用途

**服务包含业务逻辑** - 即应用的"做什么"和"为什么做"：

```
Controller 问："我应该执行这个操作吗？"
Service 回答："是/否，原因如下，以及会发生什么"
Repository 执行："这是你要的数据"
```

**服务负责：**
- ✅ 执行业务规则
- ✅ 编排多个仓库
- ✅ 事务管理
- ✅ 复杂计算
- ✅ 外部服务集成
- ✅ 业务验证

**服务不应该：**
- ❌ 了解 HTTP（Request/Response）
- ❌ 直接访问 Prisma（使用仓库）
- ❌ 处理路由相关逻辑
- ❌ 格式化 HTTP 响应

---

## 依赖注入模式

### 为什么使用依赖注入？

**优势：**
- 易于测试（注入 mock）
- 依赖关系清晰
- 配置灵活
- 促进松耦合

### 优秀示例：NotificationService

**文件：** `/blog-api/src/services/NotificationService.ts`

```typescript
// 定义依赖接口以保持清晰
export interface NotificationServiceDependencies {
    prisma: PrismaClient;
    batchingService: BatchingService;
    emailComposer: EmailComposer;
}

// 使用依赖注入的服务
export class NotificationService {
    private prisma: PrismaClient;
    private batchingService: BatchingService;
    private emailComposer: EmailComposer;
    private preferencesCache: Map<string, { preferences: UserPreference; timestamp: number }> = new Map();
    private CACHE_TTL = (notificationConfig.preferenceCacheTTLMinutes || 5) * 60 * 1000;

    // 通过构造函数注入依赖
    constructor(dependencies: NotificationServiceDependencies) {
        this.prisma = dependencies.prisma;
        this.batchingService = dependencies.batchingService;
        this.emailComposer = dependencies.emailComposer;
    }

    /**
     * 创建通知并进行路由
     */
    async createNotification(params: CreateNotificationParams) {
        const { recipientID, type, title, message, link, context = {}, channel = 'both', priority = NotificationPriority.NORMAL } = params;

        try {
            // 获取模板并渲染内容
            const template = getNotificationTemplate(type);
            const rendered = renderNotificationContent(template, context);

            // 创建应用内通知记录
            const notificationId = await createNotificationRecord({
                instanceId: parseInt(context.instanceId || '0', 10),
                template: type,
                recipientUserId: recipientID,
                channel: channel === 'email' ? 'email' : 'inApp',
                contextData: context,
                title: finalTitle,
                message: finalMessage,
                link: finalLink,
            });

            // 根据渠道路由通知
            if (channel === 'email' || channel === 'both') {
                await this.routeNotification({
                    notificationId,
                    userId: recipientID,
                    type,
                    priority,
                    title: finalTitle,
                    message: finalMessage,
                    link: finalLink,
                    context,
                });
            }

            return notification;
        } catch (error) {
            ErrorLogger.log(error, {
                context: {
                    '[NotificationService] createNotification': {
                        type: params.type,
                        recipientID: params.recipientID,
                    },
                },
            });
            throw error;
        }
    }

    /**
     * 根据用户偏好路由通知
     */
    private async routeNotification(params: { notificationId: number; userId: string; type: string; priority: NotificationPriority; title: string; message: string; link?: string; context?: Record<string, any> }) {
        // 获取用户偏好（带缓存）
        const preferences = await this.getUserPreferences(params.userId);

        // 判断是批量发送还是立即发送
        if (this.shouldBatchEmail(preferences, params.type, params.priority)) {
            await this.batchingService.queueNotificationForBatch({
                notificationId: params.notificationId,
                userId: params.userId,
                userPreference: preferences,
                priority: params.priority,
            });
        } else {
            // 通过 EmailComposer 立即发送
            await this.sendImmediateEmail({
                userId: params.userId,
                title: params.title,
                message: params.message,
                link: params.link,
                context: params.context,
                type: params.type,
            });
        }
    }

    /**
     * 判断邮件是否应该批量发送
     */
    shouldBatchEmail(preferences: UserPreference, notificationType: string, priority: NotificationPriority): boolean {
        // 高优先级始终立即发送
        if (priority === NotificationPriority.HIGH) {
            return false;
        }

        // 检查批量模式
        const batchMode = preferences.emailBatchMode || BatchMode.IMMEDIATE;
        return batchMode !== BatchMode.IMMEDIATE;
    }

    /**
     * 获取用户偏好（带缓存）
     */
    async getUserPreferences(userId: string): Promise<UserPreference> {
        // 先检查缓存
        const cached = this.preferencesCache.get(userId);
        if (cached && Date.now() - cached.timestamp < this.CACHE_TTL) {
            return cached.preferences;
        }

        const preference = await this.prisma.userPreference.findUnique({
            where: { userID: userId },
        });

        const finalPreferences = preference || DEFAULT_PREFERENCES;

        // 更新缓存
        this.preferencesCache.set(userId, {
            preferences: finalPreferences,
            timestamp: Date.now(),
        });

        return finalPreferences;
    }
}
```

**在 Controller 中使用：**

```typescript
// 使用依赖实例化
const notificationService = new NotificationService({
    prisma: PrismaService.main,
    batchingService: new BatchingService(PrismaService.main),
    emailComposer: new EmailComposer(),
});

// 在 controller 中使用
const notification = await notificationService.createNotification({
    recipientID: 'user-123',
    type: 'AFRLWorkflowNotification',
    context: { workflowName: 'AFRL Monthly Report' },
});
```

**关键要点：**
- 依赖通过构造函数传入
- 清晰的接口定义所需依赖
- 易于测试（注入 mock）
- 缓存逻辑封装
- 业务规则与 HTTP 隔离

---

## 单例模式

### 何时使用单例

**适用于：**
- 初始化成本高的服务
- 有共享状态的服务（缓存）
- 被多处访问的服务
- 权限服务
- 配置服务

### 示例：PermissionService（单例）

**文件：** `/blog-api/src/services/permissionService.ts`

```typescript
import { PrismaClient } from '@prisma/client';

class PermissionService {
    private static instance: PermissionService;
    private prisma: PrismaClient;
    private permissionCache: Map<string, { canAccess: boolean; timestamp: number }> = new Map();
    private CACHE_TTL = 5 * 60 * 1000; // 5 分钟

    // 私有构造函数防止直接实例化
    private constructor() {
        this.prisma = PrismaService.main;
    }

    // 获取单例实例
    public static getInstance(): PermissionService {
        if (!PermissionService.instance) {
            PermissionService.instance = new PermissionService();
        }
        return PermissionService.instance;
    }

    /**
     * 检查用户是否可以完成工作流步骤
     */
    async canCompleteStep(userId: string, stepInstanceId: number): Promise<boolean> {
        const cacheKey = `${userId}:${stepInstanceId}`;

        // 检查缓存
        const cached = this.permissionCache.get(cacheKey);
        if (cached && Date.now() - cached.timestamp < this.CACHE_TTL) {
            return cached.canAccess;
        }

        try {
            const post = await this.prisma.post.findUnique({
                where: { id: postId },
                include: {
                    author: true,
                    comments: {
                        include: {
                            user: true,
                        },
                    },
                },
            });

            if (!post) {
                return false;
            }

            // 检查用户是否有权限
            const canEdit = post.authorId === userId ||
                await this.isUserAdmin(userId);

            // 缓存结果
            this.permissionCache.set(cacheKey, {
                canAccess: isAssigned,
                timestamp: Date.now(),
            });

            return isAssigned;
        } catch (error) {
            console.error('[PermissionService] Error checking step permission:', error);
            return false;
        }
    }

    /**
     * 清除指定用户的缓存
     */
    clearUserCache(userId: string): void {
        for (const [key] of this.permissionCache) {
            if (key.startsWith(`${userId}:`)) {
                this.permissionCache.delete(key);
            }
        }
    }

    /**
     * 清除所有缓存
     */
    clearCache(): void {
        this.permissionCache.clear();
    }
}

// 导出单例实例
export const permissionService = PermissionService.getInstance();
```

**使用方式：**

```typescript
import { permissionService } from '../services/permissionService';

// 在代码库任意位置使用
const canComplete = await permissionService.canCompleteStep(userId, stepId);

if (!canComplete) {
    throw new ForbiddenError('You do not have permission to complete this step');
}
```

---

## 仓库模式

### 仓库的用途

**仓库抽象数据访问** - 即数据操作的"怎么做"：

```
Service 说："给我所有按名称排序的活跃用户"
Repository 说："这是执行该操作的 Prisma 查询"
```

**仓库负责：**
- ✅ 所有 Prisma 操作
- ✅ 查询构建
- ✅ 查询优化（select, include）
- ✅ 数据库错误处理
- ✅ 缓存数据库结果

**仓库不应该：**
- ❌ 包含业务逻辑
- ❌ 了解 HTTP
- ❌ 做决策（那是服务层的事）

### 仓库模板

```typescript
// repositories/UserRepository.ts
import { PrismaService } from '@project-lifecycle-portal/database';
import type { User, Prisma } from '@project-lifecycle-portal/database';

export class UserRepository {
    /**
     * 通过 ID 查找用户（优化查询）
     */
    async findById(userId: string): Promise<User | null> {
        try {
            return await PrismaService.main.user.findUnique({
                where: { userID: userId },
                select: {
                    userID: true,
                    email: true,
                    name: true,
                    isActive: true,
                    roles: true,
                    createdAt: true,
                    updatedAt: true,
                },
            });
        } catch (error) {
            console.error('[UserRepository] Error finding user by ID:', error);
            throw new Error(`Failed to find user: ${userId}`);
        }
    }

    /**
     * 查找所有活跃用户
     */
    async findActive(options?: { orderBy?: Prisma.UserOrderByWithRelationInput }): Promise<User[]> {
        try {
            return await PrismaService.main.user.findMany({
                where: { isActive: true },
                orderBy: options?.orderBy || { name: 'asc' },
                select: {
                    userID: true,
                    email: true,
                    name: true,
                    roles: true,
                },
            });
        } catch (error) {
            console.error('[UserRepository] Error finding active users:', error);
            throw new Error('Failed to find active users');
        }
    }

    /**
     * 通过邮箱查找用户
     */
    async findByEmail(email: string): Promise<User | null> {
        try {
            return await PrismaService.main.user.findUnique({
                where: { email },
            });
        } catch (error) {
            console.error('[UserRepository] Error finding user by email:', error);
            throw new Error(`Failed to find user with email: ${email}`);
        }
    }

    /**
     * 创建新用户
     */
    async create(data: Prisma.UserCreateInput): Promise<User> {
        try {
            return await PrismaService.main.user.create({ data });
        } catch (error) {
            console.error('[UserRepository] Error creating user:', error);
            throw new Error('Failed to create user');
        }
    }

    /**
     * 更新用户
     */
    async update(userId: string, data: Prisma.UserUpdateInput): Promise<User> {
        try {
            return await PrismaService.main.user.update({
                where: { userID: userId },
                data,
            });
        } catch (error) {
            console.error('[UserRepository] Error updating user:', error);
            throw new Error(`Failed to update user: ${userId}`);
        }
    }

    /**
     * 删除用户（通过设置 isActive = false 实现软删除）
     */
    async delete(userId: string): Promise<User> {
        try {
            return await PrismaService.main.user.update({
                where: { userID: userId },
                data: { isActive: false },
            });
        } catch (error) {
            console.error('[UserRepository] Error deleting user:', error);
            throw new Error(`Failed to delete user: ${userId}`);
        }
    }

    /**
     * 检查邮箱是否已存在
     */
    async emailExists(email: string): Promise<boolean> {
        try {
            const count = await PrismaService.main.user.count({
                where: { email },
            });
            return count > 0;
        } catch (error) {
            console.error('[UserRepository] Error checking email exists:', error);
            throw new Error('Failed to check if email exists');
        }
    }
}

// 导出单例实例
export const userRepository = new UserRepository();
```

**在服务中使用仓库：**

```typescript
// services/userService.ts
import { userRepository } from '../repositories/UserRepository';
import { ConflictError, NotFoundError } from '../utils/errors';

export class UserService {
    /**
     * 创建新用户（含业务规则）
     */
    async createUser(data: { email: string; name: string; roles: string[] }): Promise<User> {
        // 业务规则：检查邮箱是否已存在
        const emailExists = await userRepository.emailExists(data.email);
        if (emailExists) {
            throw new ConflictError('Email already exists');
        }

        // 业务规则：验证角色
        const validRoles = ['admin', 'operations', 'user'];
        const invalidRoles = data.roles.filter((role) => !validRoles.includes(role));
        if (invalidRoles.length > 0) {
            throw new ValidationError(`Invalid roles: ${invalidRoles.join(', ')}`);
        }

        // 通过仓库创建用户
        return await userRepository.create({
            email: data.email,
            name: data.name,
            roles: data.roles,
            isActive: true,
        });
    }

    /**
     * 通过 ID 获取用户
     */
    async getUser(userId: string): Promise<User> {
        const user = await userRepository.findById(userId);

        if (!user) {
            throw new NotFoundError(`User not found: ${userId}`);
        }

        return user;
    }
}
```

---

## 服务设计原则

### 1. 单一职责

每个服务应该只有一个明确的用途：

```typescript
// ✅ 正确 - 单一职责
class UserService {
    async createUser() {}
    async updateUser() {}
    async deleteUser() {}
}

class EmailService {
    async sendEmail() {}
    async sendBulkEmails() {}
}

// ❌ 错误 - 职责过多
class UserService {
    async createUser() {}
    async sendWelcomeEmail() {}  // 应该是 EmailService
    async logUserActivity() {}   // 应该是 AuditService
    async processPayment() {}    // 应该是 PaymentService
}
```

### 2. 清晰的方法命名

方法名应该描述它们做什么：

```typescript
// ✅ 正确 - 意图明确
async createNotification()
async getUserPreferences()
async shouldBatchEmail()
async routeNotification()

// ❌ 错误 - 模糊或误导
async process()
async handle()
async doIt()
async execute()
```

### 3. 返回类型

始终使用显式返回类型：

```typescript
// ✅ 正确 - 显式类型
async createUser(data: CreateUserDTO): Promise<User> {}
async findUsers(): Promise<User[]> {}
async deleteUser(id: string): Promise<void> {}

// ❌ 错误 - 隐式 any
async createUser(data) {}  // 没有类型！
```

### 4. 错误处理

服务应该抛出有意义的错误：

```typescript
// ✅ 正确 - 有意义的错误
if (!user) {
    throw new NotFoundError(`User not found: ${userId}`);
}

if (emailExists) {
    throw new ConflictError('Email already exists');
}

// ❌ 错误 - 通用错误
if (!user) {
    throw new Error('Error');  // 什么错误？
}
```

### 5. 避免上帝服务

不要创建包揽一切的服务：

```typescript
// ❌ 错误 - 上帝服务
class WorkflowService {
    async startWorkflow() {}
    async completeStep() {}
    async assignRoles() {}
    async sendNotifications() {}  // 应该是 NotificationService
    async validatePermissions() {}  // 应该是 PermissionService
    async logAuditTrail() {}  // 应该是 AuditService
    // ... 还有 50 个方法
}

// ✅ 正确 - 职责聚焦的服务
class WorkflowService {
    constructor(
        private notificationService: NotificationService,
        private permissionService: PermissionService,
        private auditService: AuditService
    ) {}

    async startWorkflow() {
        // 编排其他服务
        await this.permissionService.checkPermission();
        await this.workflowRepository.create();
        await this.notificationService.notify();
        await this.auditService.log();
    }
}
```

---

## 缓存策略

### 1. 内存缓存

```typescript
class UserService {
    private cache: Map<string, { user: User; timestamp: number }> = new Map();
    private CACHE_TTL = 5 * 60 * 1000; // 5 分钟

    async getUser(userId: string): Promise<User> {
        // 检查缓存
        const cached = this.cache.get(userId);
        if (cached && Date.now() - cached.timestamp < this.CACHE_TTL) {
            return cached.user;
        }

        // 从数据库获取
        const user = await userRepository.findById(userId);

        // 更新缓存
        if (user) {
            this.cache.set(userId, { user, timestamp: Date.now() });
        }

        return user;
    }

    clearUserCache(userId: string): void {
        this.cache.delete(userId);
    }
}
```

### 2. 缓存失效

```typescript
class UserService {
    async updateUser(userId: string, data: UpdateUserDTO): Promise<User> {
        // 在数据库中更新
        const user = await userRepository.update(userId, data);

        // 使缓存失效
        this.clearUserCache(userId);

        return user;
    }
}
```

---

## 服务测试

### 单元测试

```typescript
// tests/userService.test.ts
import { UserService } from '../services/userService';
import { userRepository } from '../repositories/UserRepository';
import { ConflictError } from '../utils/errors';

// Mock 仓库
jest.mock('../repositories/UserRepository');

describe('UserService', () => {
    let userService: UserService;

    beforeEach(() => {
        userService = new UserService();
        jest.clearAllMocks();
    });

    describe('createUser', () => {
        it('当邮箱不存在时应该创建用户', async () => {
            // 准备
            const userData = {
                email: 'test@example.com',
                name: 'Test User',
                roles: ['user'],
            };

            (userRepository.emailExists as jest.Mock).mockResolvedValue(false);
            (userRepository.create as jest.Mock).mockResolvedValue({
                userID: '123',
                ...userData,
            });

            // 执行
            const user = await userService.createUser(userData);

            // 断言
            expect(user).toBeDefined();
            expect(user.email).toBe(userData.email);
            expect(userRepository.emailExists).toHaveBeenCalledWith(userData.email);
            expect(userRepository.create).toHaveBeenCalled();
        });

        it('当邮箱已存在时应该抛出 ConflictError', async () => {
            // 准备
            const userData = {
                email: 'existing@example.com',
                name: 'Test User',
                roles: ['user'],
            };

            (userRepository.emailExists as jest.Mock).mockResolvedValue(true);

            // 执行 & 断言
            await expect(userService.createUser(userData)).rejects.toThrow(ConflictError);
            expect(userRepository.create).not.toHaveBeenCalled();
        });
    });
});
```

---

**相关文件：**
- SKILL.md - 主指南
- [routing-and-controllers.md](routing-and-controllers.md) - 使用服务的控制器
- [database-patterns.md](database-patterns.md) - Prisma 和仓库模式
- [complete-examples.md](complete-examples.md) - 完整的服务/仓库示例
