---
name: graphql
description: GraphQL 让客户端精确获取所需数据——不多不少。单一端点、类型化 Schema、内省机制。但这种灵活性也带来风险。若无适当控制，客户端可构造查询拖垮服务器。触发词：GraphQL、GraphQL Schema、GraphQL Resolver、Apollo Server、Apollo Client、GraphQL Federation、DataLoader、GraphQL Codegen、GraphQL Query、GraphQL Mutation、graphql
risk: safe
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# GraphQL

GraphQL 让客户端精确获取所需数据——不多不少。单一端点、类型化 Schema、内省机制。但这种灵活性也带来风险。若无适当控制，客户端可构造查询拖垮服务器。

本技能涵盖 Schema 设计、Resolver、用于防止 N+1 的 DataLoader、微服务 Federation，以及 Apollo/urql 客户端集成。核心洞见：GraphQL 是契约。Schema 就是 API 文档。请谨慎设计。

2025 年的经验：GraphQL 并非万能解。简单 CRUD 场景，REST 更简洁。高性能公开 API，REST 配合缓存更优。当存在复杂数据关系和多样化客户端需求时，才使用 GraphQL。

## 原则

- Schema 优先设计——Schema 即契约
- 用 DataLoader 防止 N+1 查询
- 限制查询深度和复杂度
- 使用 Fragment 实现可复用选择集
- Mutation 应具体，而非通用更新操作
- 错误即数据——使用联合类型处理预期失败
- 可空性有意义——有意设计

## 能力

- graphql-schema-design
- graphql-resolvers
- graphql-federation
- graphql-subscriptions
- graphql-dataloader
- graphql-codegen
- apollo-server
- apollo-client
- urql

## 边界

- database-queries -> postgres-wizard
- authentication -> authentication-oauth
- rest-api-design -> backend
- websocket-infrastructure -> backend

## 工具

### 服务端

- @apollo/server - 适用场景：Apollo Server v4 备注：最流行的 GraphQL 服务器
- graphql-yoga - 适用场景：轻量替代方案 备注：适合 Serverless
- mercurius - 适用场景：Fastify 集成 备注：快速，使用 JIT

### 客户端

- @apollo/client - 适用场景：全功能客户端 备注：缓存、状态管理
- urql - 适用场景：轻量替代方案 备注：更小、更简洁
- graphql-request - 适用场景：简单请求 备注：极简，无缓存

### 工具

- graphql-codegen - 适用场景：类型生成 备注：TypeScript 必备
- dataloader - 适用场景：N+1 防护 备注：批处理与缓存

## 模式

### Schema 设计

类型安全的 Schema，合理的可空性设计

**适用场景**：设计任何 GraphQL API

# SCHEMA DESIGN:

"""
Schema 是你的 API 契约。有意设计可空性——非空字段必须始终能解析。
"""

type Query {
  # 非空——始终返回用户或抛出异常
  user(id: ID!): User!

  # 可空——未找到时返回 null
  userByEmail(email: String!): User

  # 非空列表，非空元素
  users(limit: Int = 10, offset: Int = 0): [User!]!

  # 搜索与分页
  searchUsers(
    query: String!
    first: Int
    after: String
  ): UserConnection!
}

type Mutation {
  # 复杂 Mutation 使用输入类型
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeleteUserPayload!
}

type Subscription {
  userCreated: User!
  messageReceived(roomId: ID!): Message!
}

# 输入类型
input CreateUserInput {
  email: String!
  name: String!
  role: Role = USER
}

input UpdateUserInput {
  email: String
  name: String
  role: Role
}

# Payload 类型（用于错误即数据模式）
type CreateUserPayload {
  user: User
  errors: [Error!]!
}

union UpdateUserPayload = UpdateUserSuccess | NotFoundError | ValidationError

type UpdateUserSuccess {
  user: User!
}

# 枚举
enum Role {
  USER
  ADMIN
  MODERATOR
}

# 带关系的类型
type User {
  id: ID!
  email: String!
  name: String!
  role: Role!
  posts(limit: Int = 10): [Post!]!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments: [Comment!]!
  published: Boolean!
}

# 分页（Relay 风格）
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

### DataLoader 防止 N+1

批处理和缓存数据库查询

**适用场景**：解析关系

# DATALOADER:

"""
没有 DataLoader，获取 10 篇文章及其作者需要 11 次查询（1 次查文章 + 10 次查作者）。
DataLoader 可批处理为 2 次查询。
"""

import DataLoader from 'dataloader';

// 每个请求创建 loader
function createLoaders(db) {
  return {
    userLoader: new DataLoader(async (ids) => {
      // 单次查询所有用户
      const users = await db.user.findMany({
        where: { id: { in: ids } }
      });

      // 按 ids 顺序返回
      const userMap = new Map(users.map(u => [u.id, u]));
      return ids.map(id => userMap.get(id) || null);
    }),

    postsByAuthorLoader: new DataLoader(async (authorIds) => {
      const posts = await db.post.findMany({
        where: { authorId: { in: authorIds } }
      });

      // 按作者分组
      const postsByAuthor = new Map();
      posts.forEach(post => {
        const existing = postsByAuthor.get(post.authorId) || [];
        postsByAuthor.set(post.authorId, [...existing, post]);
      });

      return authorIds.map(id => postsByAuthor.get(id) || []);
    })
  };
}

// 挂载到 context
const server = new ApolloServer({
  typeDefs,
  resolvers,
});

app.use('/graphql', expressMiddleware(server, {
  context: async ({ req }) => ({
    db,
    loaders: createLoaders(db),
    user: req.user
  })
}));

// 在 resolver 中使用
const resolvers = {
  Post: {
    author: (post, _, { loaders }) => {
      return loaders.userLoader.load(post.authorId);
    }
  },
  User: {
    posts: (user, _, { loaders }) => {
      return loaders.postsByAuthorLoader.load(user.id);
    }
  }
};

### Apollo Client 缓存

带类型策略的规范化缓存

**适用场景**：客户端数据管理

# APOLLO CLIENT CACHING:

"""
Apollo Client 将响应规范化为扁平缓存。
配置类型策略以自定义缓存行为。
"""

import { ApolloClient, InMemoryCache } from '@apollo/client';

const cache = new InMemoryCache({
  typePolicies: {
    Query: {
      fields: {
        // 分页字段
        users: {
          keyArgs: ['query'],  // 按查询分别缓存
          merge(existing = { edges: [] }, incoming, { args }) {
            // 无限滚动追加
            if (args?.after) {
              return {
                ...incoming,
                edges: [...existing.edges, ...incoming.edges]
              };
            }
            return incoming;
          }
        }
      }
    },
    User: {
      keyFields: ['id'],  // 用户标识方式
      fields: {
        fullName: {
          read(_, { readField }) {
            // 计算字段
            return `${readField('firstName')} ${readField('lastName')}`;
          }
        }
      }
    }
  }
});

const client = new ApolloClient({
  uri: '/graphql',
  cache,
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'cache-and-network'
    }
  }
});

// 使用 hooks 查询
import { useQuery, useMutation } from '@apollo/client';

const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
    }
  }
`;

function UserProfile({ userId }) {
  const { data, loading, error } = useQuery(GET_USER, {
    variables: { id: userId }
  });

  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} />;

  return <div>{data.user.name}</div>;
}

// Mutation 与缓存更新
const CREATE_USER = gql`
  mutation CreateUser($input: CreateUserInput!) {
    createUser(input: $input) {
      user {
        id
        name
        email
      }
      errors {
        field
        message
      }
    }
  }
`;

function CreateUserForm() {
  const [createUser, { loading }] = useMutation(CREATE_USER, {
    update(cache, { data: { createUser } }) {
      // Mutation 后更新缓存
      if (createUser.user) {
        cache.modify({
          fields: {
            users(existing = []) {
              const newRef = cache.writeFragment({
                data: createUser.user,
                fragment: gql`
                  fragment NewUser on User {
                    id
                    name
                    email
                  }
                `
              });
              return [...existing, newRef];
            }
          }
        });
      }
    }
  });
}

### 代码生成

从 Schema 生成类型安全的操作

**适用场景**：TypeScript 项目

# GRAPHQL CODEGEN:

"""
从 Schema 和操作生成 TypeScript 类型。
无需手动编写查询响应类型。
"""

# 安装
npm install -D @graphql-codegen/cli
npm install -D @graphql-codegen/typescript
npm install -D @graphql-codegen/typescript-operations
npm install -D @graphql-codegen/typescript-react-apollo

# codegen.ts
import type { CodegenConfig } from '@graphql-codegen/cli';

const config: CodegenConfig = {
  schema: 'http://localhost:4000/graphql',
  documents: ['src/**/*.graphql', 'src/**/*.tsx'],
  generates: {
    './src/generated/graphql.ts': {
      plugins: [
        'typescript',
        'typescript-operations',
        'typescript-react-apollo'
      ],
      config: {
        withHooks: true,
        withComponent: false
      }
    }
  }
};

export default config;

# 运行生成
npx graphql-codegen

# 使用——完全类型化！
import { useGetUserQuery, useCreateUserMutation } from './generated/graphql';

function UserProfile({ userId }: { userId: string }) {
  const { data, loading } = useGetUserQuery({
    variables: { id: userId }  // 类型检查！
  });

  // data.user 完全类型化
  return <div>{data?.user?.name}</div>;
}

### 使用联合类型处理错误

预期错误作为数据，而非异常

**适用场景**：可能以预期方式失败的操作

# ERRORS AS DATA:

"""
使用联合类型处理预期失败场景。
GraphQL 错误用于意外失败。
"""

# Schema
type Mutation {
  login(email: String!, password: String!): LoginResult!
}

union LoginResult = LoginSuccess | InvalidCredentials | AccountLocked

type LoginSuccess {
  user: User!
  token: String!
}

type InvalidCredentials {
  message: String!
}

type AccountLocked {
  message: String!
  unlockAt: DateTime
}

# Resolver
const resolvers = {
  Mutation: {
    login: async (_, { email, password }, { db }) => {
      const user = await db.user.findByEmail(email);

      if (!user || !await verifyPassword(password, user.hash)) {
        return {
          __typename: 'InvalidCredentials',
          message: 'Invalid email or password'
        };
      }

      if (user.lockedUntil && user.lockedUntil > new Date()) {
        return {
          __typename: 'AccountLocked',
          message: 'Account temporarily locked',
          unlockAt: user.lockedUntil
        };
      }

      return {
        __typename: 'LoginSuccess',
        user,
        token: generateToken(user)
      };
    }
  },

  LoginResult: {
    __resolveType(obj) {
      return obj.__typename;
    }
  }
};

# 客户端查询
const LOGIN = gql`
  mutation Login($email: String!, $password: String!) {
    login(email: $email, password: $password) {
      ... on LoginSuccess {
        user { id name }
        token
      }
      ... on InvalidCredentials {
        message
      }
      ... on AccountLocked {
        message
        unlockAt
      }
    }
  }
`;

// 处理所有情况
const result = data.login;
switch (result.__typename) {
  case 'LoginSuccess':
    setToken(result.token);
    redirect('/dashboard');
    break;
  case 'InvalidCredentials':
    setError(result.message);
    break;
  case 'AccountLocked':
    setError(`${result.message}. Try again at ${result.unlockAt}`);
    break;
}

## 陷阱

### 每个 Resolver 单独查询数据库

严重程度：严重

场景：你编写的 Resolver 各自独立获取数据。查询 10 篇带作者的文章会产生 11 次数据库查询。100 篇文章就是 101 次查询。响应时间变成数秒。

症状：
- API 响应缓慢
- 日志中出现大量相似数据库查询
- 性能随列表大小下降

原因：
GraphQL Resolver 独立运行。没有批处理，每篇文章的作者 Resolver 都会单独执行。数据库被重复的相似查询轰炸。

推荐修复：

# USE DATALOADER

import DataLoader from 'dataloader';

// 每个请求创建 loader
const userLoader = new DataLoader(async (ids) => {
  const users = await db.user.findMany({
    where: { id: { in: ids } }
  });
  // 重要：按输入 ids 顺序返回
  const userMap = new Map(users.map(u => [u.id, u]));
  return ids.map(id => userMap.get(id));
});

// 在 resolver 中使用
const resolvers = {
  Post: {
    author: (post, _, { loaders }) =>
      loaders.userLoader.load(post.authorId)
  }
};

# 要点：
# 1. 每个请求创建新 loader（限定缓存作用域）
# 2. 按输入 ID 顺序返回结果
# 3. 处理缺失项（返回 null，而非跳过）

### 深度嵌套查询可导致服务器 DoS

严重程度：严重

场景：你的 Schema 存在循环关系（user.posts.author.posts...）。客户端发送 20 层深的查询。服务器尝试解析，超时或崩溃。

症状：
- 特定查询导致服务器超时
- 内存耗尽
- 嵌套查询响应缓慢

原因：
GraphQL 允许客户端请求任何有效的查询形状。没有限制，恶意或有 bug 的客户端可构造需要指数级工作量的查询。即使是合法查询也可能意外过深。

推荐修复：

# LIMIT QUERY DEPTH AND COMPLEXITY

import depthLimit from 'graphql-depth-limit';
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    // 限制嵌套深度
    depthLimit(10),

    // 限制查询复杂度
    createComplexityLimitRule(1000, {
      scalarCost: 1,
      objectCost: 2,
      listFactor: 10
    })
  ]
});

# 还应考虑：
# - 查询超时限制
# - 按客户端限流
# - 持久化查询（仅允许预注册查询）

### 生产环境启用内省暴露 Schema

严重程度：高

场景：你部署到生产环境时启用了内省。任何人都可以查询你的 Schema，发现所有类型、Mutation 和字段名。攻击者清楚知道该攻击什么。

症状：
- 通过内省查询可见 Schema
- 生产环境可访问 GraphQL Playground
- 暴露完整类型信息

原因：
内省对开发和工具至关重要，但在生产环境中它是攻击者的路线图。他们可发现管理 Mutation、内部字段和已弃用但仍可用的 API。

推荐修复：

# DISABLE INTROSPECTION IN PRODUCTION

const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production',
  plugins: [
    process.env.NODE_ENV === 'production'
      ? ApolloServerPluginLandingPageDisabled()
      : ApolloServerPluginLandingPageLocalDefault()
  ]
});

# 更好：使用持久化查询
# 生产环境仅允许预注册查询
const server = new ApolloServer({
  typeDefs,
  resolvers,
  persistedQueries: {
    cache: new InMemoryLRUCache()
  }
});

### 仅在 Schema 指令中做授权，而非 Resolver

严重程度：高

场景：你完全依赖 @auth 指令进行授权。有人绕过了指令，或复杂业务规则不适合简单指令。授权失效。

症状：
- 未授权访问数据
- 业务规则未执行
- 仅依赖指令的安全被绕过

原因：
指令适合简单检查，但无法处理复杂业务逻辑。"用户可编辑自己的文章，或其管理的群组中的任何文章"不适合放入指令。

推荐修复：

# AUTHORIZE IN RESOLVERS

// 在 resolver 中简单检查
Mutation: {
  deletePost: async (_, { id }, { user, db }) => {
    if (!user) {
      throw new AuthenticationError('Must be logged in');
    }

    const post = await db.post.findUnique({ where: { id } });

    if (!post) {
      throw new NotFoundError('Post not found');
    }

    // 业务逻辑授权
    const canDelete =
      post.authorId === user.id ||
      user.role === 'ADMIN' ||
      await userModeratesGroup(user.id, post.groupId);

    if (!canDelete) {
      throw new ForbiddenError('Cannot delete this post');
    }

    return db.post.delete({ where: { id } });
  }
}

// 字段级授权辅助
User: {
  email: (user, _, { currentUser }) => {
    // 仅对自己或管理员显示邮箱
    if (currentUser?.id === user.id || currentUser?.role === 'ADMIN') {
      return user.email;
    }
    return null;
  }
}

### 仅在查询上做授权，而非字段

严重程度：高

场景：你检查用户是否可访问资源，但未检查各个字段。用户 A 可查看用户 B 的公开资料，却意外看到了私密邮箱和电话号码。

症状：
- 敏感数据暴露
- 隐私泄露
- 字段数据对错误用户可见

原因：
字段 Resolver 在父对象返回后运行。如果父查询返回了用户，所有字段都会被解析——包括敏感字段。每个敏感字段都需要自己的授权检查。

推荐修复：

# FIELD-LEVEL AUTHORIZATION

const resolvers = {
  User: {
    // 公开字段——无需检查
    id: (user) => user.id,
    name: (user) => user.name,

    // 私密字段——检查访问权限
    email: (user, _, { currentUser }) => {
      if (!currentUser) return null;
      if (currentUser.id === user.id) return user.email;
      if (currentUser.role === 'ADMIN') return user.email;
      return null;
    },

    phoneNumber: (user, _, { currentUser }) => {
      if (currentUser?.id !== user.id) return null;
      return user.phoneNumber;
    },

    // 或抛出异常而非返回 null
    privateData: (user, _, { currentUser }) => {
      if (currentUser?.id !== user.id) {
        throw new ForbiddenError('Not authorized');
      }
      return user.privateData;
    }
  }
};

### 非空字段失败导致整个父对象为 null

严重程度：中等

场景：你为方便将字段设为非空。某个 Resolver 抛出异常或返回 null。错误向上传播，使父对象变为 null，直到整个查询响应为 null 或报错。

症状：
- 查询意外返回 null
- 一个错误影响不相关字段
- 无法返回部分数据

原因：
GraphQL 的 null 传播意味着如果非空字段无法解析，其父对象变为 null。如果父对象也是非空的，会继续传播。一个失败的字段可能破坏整个响应。

推荐修复：

# DESIGN NULLABILITY INTENTIONALLY

# 错误：所有字段都非空
type User {
  id: ID!
  name: String!
  email: String!
  avatar: String!      # 没有头像怎么办？
  lastLogin: DateTime! # 从未登录怎么办？
}

# 正确：适当位置可空
type User {
  id: ID!              # 始终存在
  name: String!        # 必填字段
  email: String!       # 必填字段
  avatar: String       # 可选——可能不存在
  lastLogin: DateTime  # 可空——可能为 null
}

# 列表：
# [User!]! - 非空列表，非空元素（推荐）
# [User!]  - 可空列表，非空元素
# [User]!  - 非空列表，可空元素（很少有用）
# [User]   - 可空列表，可空元素（避免）

# 经验法则：
# - 始终存在且失败应导致查询失败时使用非空
# - 可选或失败不应破坏响应时使用可空

### 昂贵查询与廉价查询同等对待

严重程度：中等

场景：每个查询都被同等处理。简单的 user(id) 查询与 users(first: 1000) { posts { comments } } 使用相同资源。昂贵查询挤占廉价查询。

症状：
- 昂贵查询拖慢一切
- 无法优先处理查询
- 限流无效

原因：
并非所有 GraphQL 操作都相等。获取 1000 个用户及其嵌套数据比获取一个用户昂贵数个数量级。没有成本分析，无法正确限流。

推荐修复：

# QUERY COST ANALYSIS

import { createComplexityLimitRule } from 'graphql-validation-complexity';

// 定义每个字段的复杂度
const complexityRules = createComplexityLimitRule(1000, {
  scalarCost: 1,
  objectCost: 10,
  listFactor: 10,
  // 自定义字段成本
  fieldCost: {
    'Query.searchUsers': 100,
    'Query.analytics': 500,
    'User.posts': ({ args }) => args.limit || 10
  }
});

// 按成本限流
const costPlugin = {
  requestDidStart() {
    return {
      didResolveOperation({ request, document }) {
        const cost = calculateQueryCost(document);
        if (cost > 1000) {
          throw new Error(`Query too expensive: ${cost}`);
        }
        // 追踪成本用于限流
        rateLimiter.consume(request.userId, cost);
      }
    };
  }
};

### Subscription 未正确清理

严重程度：中等

场景：客户端订阅但未干净地取消订阅。网络问题留下孤立订阅。服务器内存随着死订阅累积而增长。

症状：
- 内存使用随时间增长
- 死连接累积
- 服务器变慢

原因：
每个订阅都占用服务器资源。断开连接时没有正确清理，资源会累积。长期运行的服务器最终会耗尽内存。

推荐修复：

# PROPER SUBSCRIPTION CLEANUP

import { PubSub, withFilter } from 'graphql-subscriptions';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';

const pubsub = new PubSub();

// 追踪活跃订阅
const activeSubscriptions = new Map();

const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql'
});

useServer({
  schema,
  context: (ctx) => ({
    pubsub,
    userId: ctx.connectionParams?.userId
  }),
  onConnect: (ctx) => {
    console.log('Client connected');
  },
  onDisconnect: (ctx) => {
    // 清理此连接的资源
    const userId = ctx.connectionParams?.userId;
    activeSubscriptions.delete(userId);
  }
}, wsServer);

// 带清理的订阅 Resolver
Subscription: {
  messageReceived: {
    subscribe: withFilter(
      (_, { roomId }, { pubsub, userId }) => {
        // 追踪订阅
        activeSubscriptions.set(userId, roomId);
        return pubsub.asyncIterator(`ROOM_${roomId}`);
      },
      (payload, { roomId }) => {
        return payload.roomId === roomId;
      }
    )
  }
}

## 验证检查

### 生产环境启用内省

严重程度：警告

信息：生产环境应禁用内省

修复操作：设置 introspection: process.env.NODE_ENV !== 'production'

### Resolver 中直接查询数据库

严重程度：警告

信息：考虑使用 DataLoader 批处理和缓存查询

修复操作：创建 DataLoader 并使用 .load() 替代直接查询

### 未限制查询深度

严重程度：警告

信息：考虑添加深度限制以防止 DoS

修复操作：添加 validationRules: [depthLimit(10)]

### Resolver 无 try-catch

严重程度：信息

信息：考虑用 try-catch 包装 Resolver 逻辑

修复操作：添加错误处理以提供更好的错误消息

### Schema 中使用 JSON 或 Any 类型

严重程度：信息

信息：避免 JSON/Any 类型——它们绕过 GraphQL 的类型安全

修复操作：定义正确的输入/输出类型

### Mutation 返回裸类型而非 Payload

严重程度：信息

信息：考虑为 Mutation 使用 Payload 类型（包含错误）

修复操作：创建 CreateUserPayload 类型，包含 user 和 errors 字段

### 列表字段无分页参数

严重程度：信息

信息：列表字段应有分页（limit、first、after）

修复操作：添加参数：field(limit: Int, offset: Int): [Type!]!

### Query hook 无错误处理

严重程度：信息

信息：在 UI 中处理查询错误

修复操作：解构并处理错误：const { error } = useQuery(...)

### 使用 refetch 而非缓存更新

严重程度：信息

信息：考虑使用缓存更新替代 refetch 以获得更好的用户体验

修复操作：使用 update 函数直接修改缓存

## 协作

### 委派触发

- 用户需要数据库优化 -> postgres-wizard（为 GraphQL Resolver 优化查询）
- 用户需要认证系统 -> authentication-oauth（GraphQL context 认证）
- 用户需要缓存层 -> caching-strategies（响应缓存、DataLoader 缓存）
- 用户需要实时基础设施 -> backend（Subscription 的 WebSocket 设置）

## 相关技能

与以下技能配合良好：`backend`、`postgres-wizard`、`nextjs-app-router`、`react-patterns`

## 使用时机

- 用户提及或暗示：graphql
- 用户提及或暗示：graphql schema
- 用户提及或暗示：graphql resolver
- 用户提及或暗示：apollo server
- 用户提及或暗示：apollo client
- 用户提及或暗示：graphql federation
- 用户提及或暗示：dataloader
- 用户提及或暗示：graphql codegen
- 用户提及或暗示：graphql query
- 用户提及或暗示：graphql mutation

## 限制

- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代为环境特定的验证、测试或专家审查。
- 若缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
