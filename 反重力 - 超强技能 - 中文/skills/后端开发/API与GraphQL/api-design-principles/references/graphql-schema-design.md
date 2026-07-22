# GraphQL Schema 设计模式

## Schema 组织

### 模块化 Schema 结构

```graphql
# user.graphql
type User {
  id: ID!
  email: String!
  name: String!
  posts: [Post!]!
}

extend type Query {
  user(id: ID!): User
  users(first: Int, after: String): UserConnection!
}

extend type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

# post.graphql
type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}

extend type Query {
  post(id: ID!): Post
}
```

## 类型设计模式

### 1. Non-Null 类型

```graphql
type User {
  id: ID! # 始终必需
  email: String! # 必需
  phone: String # 可选（nullable）
  posts: [Post!]! # 非空数组，元素非空
  tags: [String!] # 可空数组，元素非空
}
```

### 2. 接口实现多态

```graphql
interface Node {
  id: ID!
  createdAt: DateTime!
}

type User implements Node {
  id: ID!
  createdAt: DateTime!
  email: String!
}

type Post implements Node {
  id: ID!
  createdAt: DateTime!
  title: String!
}

type Query {
  node(id: ID!): Node
}
```

### 3. 联合类型处理异构结果

```graphql
union SearchResult = User | Post | Comment

type Query {
  search(query: String!): [SearchResult!]!
}

# 查询示例
{
  search(query: "graphql") {
    ... on User {
      name
      email
    }
    ... on Post {
      title
      content
    }
    ... on Comment {
      text
      author {
        name
      }
    }
  }
}
```

### 4. 输入类型

```graphql
input CreateUserInput {
  email: String!
  name: String!
  password: String!
  profileInput: ProfileInput
}

input ProfileInput {
  bio: String
  avatar: String
  website: String
}

input UpdateUserInput {
  id: ID!
  email: String
  name: String
  profileInput: ProfileInput
}
```

## 分页模式

### Relay 游标分页（推荐）

```graphql
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

type Query {
  users(first: Int, after: String, last: Int, before: String): UserConnection!
}

# 使用示例
{
  users(first: 10, after: "cursor123") {
    edges {
      cursor
      node {
        id
        name
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### 偏移分页（更简单）

```graphql
type UserList {
  items: [User!]!
  total: Int!
  page: Int!
  pageSize: Int!
}

type Query {
  users(page: Int = 1, pageSize: Int = 20): UserList!
}
```

## 变更设计模式

### 1. Input/Payload 模式

```graphql
input CreatePostInput {
  title: String!
  content: String!
  tags: [String!]
}

type CreatePostPayload {
  post: Post
  errors: [Error!]
  success: Boolean!
}

type Error {
  field: String
  message: String!
  code: String!
}

type Mutation {
  createPost(input: CreatePostInput!): CreatePostPayload!
}
```

### 2. 乐观响应支持

```graphql
type UpdateUserPayload {
  user: User
  clientMutationId: String
  errors: [Error!]
}

input UpdateUserInput {
  id: ID!
  name: String
  clientMutationId: String
}

type Mutation {
  updateUser(input: UpdateUserInput!): UpdateUserPayload!
}
```

### 3. 批量变更

```graphql
input BatchCreateUserInput {
  users: [CreateUserInput!]!
}

type BatchCreateUserPayload {
  results: [CreateUserResult!]!
  successCount: Int!
  errorCount: Int!
}

type CreateUserResult {
  user: User
  errors: [Error!]
  index: Int!
}

type Mutation {
  batchCreateUsers(input: BatchCreateUserInput!): BatchCreateUserPayload!
}
```

## 字段设计

### 参数与过滤

```graphql
type Query {
  posts(
    # 分页
    first: Int = 20
    after: String

    # 过滤
    status: PostStatus
    authorId: ID
    tag: String

    # 排序
    orderBy: PostOrderBy = CREATED_AT
    orderDirection: OrderDirection = DESC

    # 搜索
    search: String
  ): PostConnection!
}

enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

enum PostOrderBy {
  CREATED_AT
  UPDATED_AT
  TITLE
}

enum OrderDirection {
  ASC
  DESC
}
```

### 计算字段

```graphql
type User {
  firstName: String!
  lastName: String!
  fullName: String! # 在 resolver 中计算
  posts: [Post!]!
  postCount: Int! # 计算得出，不加载所有文章
}

type Post {
  likeCount: Int!
  commentCount: Int!
  isLikedByViewer: Boolean! # 依赖上下文
}
```

## 订阅

```graphql
type Subscription {
  postAdded: Post!

  postUpdated(postId: ID!): Post!

  userStatusChanged(userId: ID!): UserStatus!
}

type UserStatus {
  userId: ID!
  online: Boolean!
  lastSeen: DateTime!
}

# 客户端使用
subscription {
  postAdded {
    id
    title
    author {
      name
    }
  }
}
```

## 自定义标量

```graphql
scalar DateTime
scalar Email
scalar URL
scalar JSON
scalar Money

type User {
  email: Email!
  website: URL
  createdAt: DateTime!
  metadata: JSON
}

type Product {
  price: Money!
}
```

## 指令

### 内置指令

```graphql
type User {
  name: String!
  email: String! @deprecated(reason: "使用 emails 字段代替")
  emails: [String!]!

  # 条件包含
  privateData: PrivateData @include(if: $isOwner)
}

# 查询
query GetUser($isOwner: Boolean!) {
  user(id: "123") {
    name
    privateData @include(if: $isOwner) {
      ssn
    }
  }
}
```

### 自定义指令

```graphql
directive @auth(requires: Role = USER) on FIELD_DEFINITION

enum Role {
  USER
  ADMIN
  MODERATOR
}

type Mutation {
  deleteUser(id: ID!): Boolean! @auth(requires: ADMIN)
  updateProfile(input: ProfileInput!): User! @auth
}
```

## 错误处理

### 联合错误模式

```graphql
type User {
  id: ID!
  email: String!
}

type ValidationError {
  field: String!
  message: String!
}

type NotFoundError {
  message: String!
  resourceType: String!
  resourceId: ID!
}

type AuthorizationError {
  message: String!
}

union UserResult = User | ValidationError | NotFoundError | AuthorizationError

type Query {
  user(id: ID!): UserResult!
}

# 使用示例
{
  user(id: "123") {
    ... on User {
      id
      email
    }
    ... on NotFoundError {
      message
      resourceType
    }
    ... on AuthorizationError {
      message
    }
  }
}
```

### Payload 中的错误

```graphql
type CreateUserPayload {
  user: User
  errors: [Error!]
  success: Boolean!
}

type Error {
  field: String
  message: String!
  code: ErrorCode!
}

enum ErrorCode {
  VALIDATION_ERROR
  UNAUTHORIZED
  NOT_FOUND
  INTERNAL_ERROR
}
```

## N+1 查询问题解决方案

### DataLoader 模式

```python
from aiodataloader import DataLoader

class PostLoader(DataLoader):
    async def batch_load_fn(self, post_ids):
        posts = await db.posts.find({"id": {"$in": post_ids}})
        post_map = {post["id"]: post for post in posts}
        return [post_map.get(pid) for pid in post_ids]

# Resolver
@user_type.field("posts")
async def resolve_posts(user, info):
    loader = info.context["loaders"]["post"]
    return await loader.load_many(user["post_ids"])
```

### 查询深度限制

```python
from graphql import GraphQLError

def depth_limit_validator(max_depth: int):
    def validate(context, node, ancestors):
        depth = len(ancestors)
        if depth > max_depth:
            raise GraphQLError(
                f"查询深度 {depth} 超过最大值 {max_depth}"
            )
    return validate
```

### 查询复杂度分析

```python
def complexity_limit_validator(max_complexity: int):
    def calculate_complexity(node):
        # 每个字段 = 1，列表乘以倍数
        complexity = 1
        if is_list_field(node):
            complexity *= get_list_size_arg(node)
        return complexity

    return validate_complexity
```

## Schema 版本控制

### 字段弃用

```graphql
type User {
  name: String! @deprecated(reason: "使用 firstName 和 lastName")
  firstName: String!
  lastName: String!
}
```

### Schema 演进

```graphql
# v1 - 初始版本
type User {
  name: String!
}

# v2 - 添加可选字段（向后兼容）
type User {
  name: String!
  email: String
}

# v3 - 弃用并添加新字段
type User {
  name: String! @deprecated(reason: "使用 firstName/lastName")
  firstName: String!
  lastName: String!
  email: String
}
```

## 最佳实践总结

1. **Nullable 与 Non-Null**：初始设为 nullable，确定后再改为 non-null
2. **输入类型**：变更始终使用输入类型
3. **Payload 模式**：在变更 payload 中返回错误
4. **分页**：无限滚动用游标分页，简单场景用偏移分页
5. **命名**：字段用 camelCase，类型用 PascalCase
6. **弃用**：使用 `@deprecated` 而非删除字段
7. **DataLoader**：关系字段始终使用以防止 N+1
8. **复杂度限制**：防止昂贵查询
9. **自定义标量**：用于领域特定类型（Email、DateTime）
10. **文档**：为所有字段添加描述
