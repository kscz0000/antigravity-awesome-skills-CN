# 上下文映射模式

## 常见关系模式

- Partnership（合作）
- Shared Kernel（共享内核）
- Customer-Supplier（客户-供应商）
- Conformist（跟随者）
- Anti-Corruption Layer（防腐层）
- Open Host Service（开放主机服务）
- Published Language（发布语言）

## 映射模板

| 上游上下文 | 下游上下文 | 模式 | 契约所有者 | 是否需要转换 |
| --- | --- | --- | --- | --- |
| Billing | Checkout | Customer-Supplier | Billing | 是 |
| Identity | Checkout | Conformist | Identity | 否 |

## ACL 检查清单

- 为接收方上下文定义规范化领域模型。
- 将外部术语翻译为本地通用语言。
- ACL 代码应位于边界层，而非领域核心内部。
- 为映射行为添加契约测试。
