# CONTEXT.md 格式

## 结构

```md
# {上下文名称}

{一两句话描述这个上下文是什么以及为什么存在。}

## 语言

**Order**：
{术语的一两句话描述}
_避免_：Purchase、transaction

**Invoice**：
交付后发送给客户的付款请求。
_避免_：Bill、payment request

**Customer**：
下单的个人或组织。
_避免_：Client、buyer、account
```

## 规则

- **保持明确的立场。** 当同一个概念存在多个词语时，选择最合适的一个，并把其他列在 `_避免_` 下。
- **定义要简练。** 最多一两句话。定义它*是*什么，而不是它*做什么*。
- **仅纳入本项目上下文特有的术语。** 即使项目大量使用一般的编程概念（超时、错误类型、工具模式）也不应纳入。在添加术语之前问自己：这是该上下文独有的概念，还是一般的编程概念？只有前者才应纳入。
- **在自然成簇时用子标题对术语分组。** 如果所有术语都属于同一个内聚领域，则使用扁平列表即可。

## 单上下文与多上下文仓库

**单上下文（大多数仓库）：** 仓库根目录有一个 `CONTEXT.md`。

**多上下文：** 仓库根目录的 `CONTEXT-MAP.md` 列出所有上下文、它们所在位置以及它们之间的关系：

```md
# Context Map

## 上下文

- [Ordering](./src/ordering/CONTEXT.md) —— 接收并跟踪客户订单
- [Billing](./src/billing/CONTEXT.md) —— 生成发票并处理付款
- [Fulfillment](./src/fulfillment/CONTEXT.md) —— 管理仓库拣货与发货

## 关系

- **Ordering → Fulfillment**：Ordering 发出 `OrderPlaced` 事件；Fulfillment 消费这些事件以开始拣货
- **Fulfillment → Billing**：Fulfillment 发出 `ShipmentDispatched` 事件；Billing 消费这些事件以生成发票
- **Ordering ↔ Billing**：共享 `CustomerId` 和 `Money` 类型
```

技能会自动推断适用哪种结构：

- 如果存在 `CONTEXT-MAP.md`，读取它以查找上下文
- 如果仅存在根目录的 `CONTEXT.md`，则为单上下文
- 如果两者都不存在，则在第一个术语得到澄清时懒加载地创建根目录的 `CONTEXT.md`

当存在多个上下文时，自动推断当前主题与哪个上下文相关。如果不明确，请询问。