---
name: architecture-decision-records
description: "创建、维护和管理架构决策记录（ADR）的综合模式，用于捕获重大技术决策的上下文和理由。触发词：ADR、架构决策、记录这个决策、架构决策记录、我们为什么选、技术选型记录、架构选型、设计决策。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 架构决策记录

创建、维护和管理架构决策记录（ADR）的综合模式，用于捕获重大技术决策的上下文和理由。

## 使用此技能的时机

- 做出重大架构决策时
- 记录技术选型时
- 记录设计权衡时
- 新团队成员入职时
- 审查历史决策时
- 建立决策流程时

## 不使用此技能的时机

- 只需记录小型实现细节
- 变更是小型补丁或日常维护
- 没有架构决策需要记录

## 指导步骤

1. 捕获决策上下文、约束和驱动因素。
2. 记录考虑过的选项及其权衡。
3. 记录决策、理由和后果。
4. 链接相关ADR并随时间更新状态。

## 核心概念

### 1. 什么是ADR？

架构决策记录捕获：
- **上下文**：为什么需要做出决策
- **决策**：我们决定了什么
- **后果**：结果会发生什么

### 2. 何时编写ADR

| 编写ADR | 跳过ADR |
|-----------|----------|
| 新框架采用 | 小版本升级 |
| 数据库技术选型 | Bug修复 |
| API设计模式 | 实现细节 |
| 安全架构 | 日常维护 |
| 集成模式 | 配置变更 |

### 3. ADR生命周期

```
Proposed → Accepted → Deprecated → Superseded
              ↓
           Rejected
```

## 模板

### 模板1：标准ADR（MADR格式）

```markdown
# ADR-0001: 使用PostgreSQL作为主数据库

## 状态

已接受

## 上下文

我们需要为新的电商平台选择主数据库。系统将处理：
- 约10,000并发用户
- 带有层级分类的复杂产品目录
- 订单和支付的交易处理
- 产品全文搜索
- 门店定位的地理空间查询

团队有MySQL、PostgreSQL和MongoDB经验。我们需要金融交易的ACID合规性。

## 决策驱动因素

* **必须具备ACID合规性** 用于支付处理
* **必须支持复杂查询** 用于报表
* **应该支持全文搜索** 以减少基础设施复杂性
* **应该有良好的JSON支持** 用于灵活的产品属性
* **团队熟悉度** 减少上手时间

## 考虑的选项

### 选项1：PostgreSQL
- **优点**：ACID合规，优秀的JSON支持（JSONB），内置全文搜索，PostGIS支持地理空间，团队有经验
- **缺点**：复制设置比MySQL稍复杂

### 选项2：MySQL
- **优点**：团队非常熟悉，复制简单，社区大
- **缺点**：JSON支持较弱，无内置全文搜索（需要Elasticsearch），无地理空间支持需扩展

### 选项3：MongoDB
- **优点**：灵活模式，原生JSON，水平扩展
- **缺点**：多文档事务无ACID（决策时），团队经验有限，需要模式设计纪律

## 决策

我们将使用 **PostgreSQL 15** 作为主数据库。

## 理由

PostgreSQL提供了最佳平衡：
1. **ACID合规性** 对电商交易至关重要
2. **内置能力**（全文搜索、JSONB、PostGIS）减少基础设施复杂性
3. **团队熟悉度** SQL数据库减少学习曲线
4. **成熟生态** 优秀的工具和社区支持

复制稍复杂的问题被减少额外服务（无需单独Elasticsearch）的好处所抵消。

## 后果

### 正面
- 单一数据库处理事务、搜索和地理空间查询
- 减少运维复杂性（更少服务需要管理）
- 金融数据的强一致性保证
- 团队可利用现有SQL专业知识

### 负面
- 需要学习PostgreSQL特定功能（JSONB、全文搜索语法）
- 垂直扩展限制可能更早需要读副本
- 部分团队成员需要PostgreSQL特定培训

### 风险
- 全文搜索可能不如专用搜索引擎扩展性好
- 缓解措施：设计时考虑如需要可添加Elasticsearch

## 实现备注

- 使用JSONB存储灵活的产品属性
- 使用PgBouncer实现连接池
- 设置流复制用于读副本
- 使用pg_trgm扩展支持模糊搜索

## 相关决策

- ADR-0002: 缓存策略（Redis）- 补充数据库选择
- ADR-0005: 搜索架构 - 如需Elasticsearch可能取代

## 参考资料

- [PostgreSQL JSON Documentation](https://www.postgresql.org/docs/current/datatype-json.html)
- [PostgreSQL Full Text Search](https://www.postgresql.org/docs/current/textsearch.html)
- 内部：性能基准测试在 `/docs/benchmarks/database-comparison.md`
```

### 模板2：轻量级ADR

```markdown
# ADR-0012: 采用TypeScript进行前端开发

**状态**：已接受
**日期**：2024-01-15
**决策者**：@alice, @bob, @charlie

## 上下文

我们的React代码库已增长到50+组件，与prop类型不匹配和undefined错误相关的bug报告增加。PropTypes仅提供运行时检查。

## 决策

所有新前端代码采用TypeScript。渐进式迁移现有代码。

## 后果

**好处**：编译时捕获类型错误，更好的IDE支持，自文档化代码。

**坏处**：团队学习曲线，初期减速，构建复杂性增加。

**缓解措施**：TypeScript培训会，允许通过 `allowJs: true` 渐进采用。
```

### 模板3：Y语句格式

```markdown
# ADR-0015: API网关选择

在 **构建微服务架构** 的背景下，
面临 **需要集中式API管理、认证和限流** 的问题，
我们决定选择 **Kong Gateway**，
而非 **AWS API Gateway和自定义Nginx方案**，
以实现 **供应商独立、插件可扩展性和团队对Lua的熟悉度**，
接受 **我们需要自己管理Kong基础设施** 的代价。
```

### 模板4：废弃ADR

```markdown
# ADR-0020: 废弃MongoDB改用PostgreSQL

## 状态

已接受（取代ADR-0003）

## 上下文

ADR-0003（2021）因模式灵活性需求选择MongoDB存储用户配置文件。此后：
- MongoDB的多文档事务对我们的用例仍有问题
- 我们的模式已稳定，很少变更
- 我们从其他服务获得了PostgreSQL专业知识
- 维护两个数据库增加运维负担

## 决策

废弃MongoDB，将用户配置文件迁移到PostgreSQL。

## 迁移计划

1. **阶段1**（第1-2周）：创建PostgreSQL模式，启用双写
2. **阶段2**（第3-4周）：回填历史数据，验证一致性
3. **阶段3**（第5周）：切换读取到PostgreSQL，监控
4. **阶段4**（第6周）：移除MongoDB写入，下线

## 后果

### 正面
- 单一数据库技术减少运维复杂性
- 用户数据的ACID事务
- 团队可专注PostgreSQL专业知识

### 负面
- 迁移工作量（约4周）
- 迁移期间数据问题风险
- 失去部分模式灵活性

## 经验教训

从ADR-0003经验中记录：
- 模式灵活性的好处被高估了
- 多数据库的运维成本被低估了
- 技术决策中应考虑长期维护
```

### 模板5：征求意见（RFC）风格

```markdown
# RFC-0025: 订单管理采用事件溯源

## 摘要

建议订单管理领域采用事件溯源模式，以改善可审计性、支持时态查询并支持业务分析。

## 动机

当前挑战：
1. 审计需求需要完整订单历史
2. "订单在时间X的状态是什么？"查询无法实现
3. 分析团队需要事件流用于实时仪表盘
4. 客服的订单状态重建是手动的

## 详细设计

### 事件存储

```
OrderCreated { orderId, customerId, items[], timestamp }
OrderItemAdded { orderId, item, timestamp }
OrderItemRemoved { orderId, itemId, timestamp }
PaymentReceived { orderId, amount, paymentId, timestamp }
OrderShipped { orderId, trackingNumber, timestamp }
```

### 投影

- **CurrentOrderState**：用于查询的物化视图
- **OrderHistory**：用于审计的完整时间线
- **DailyOrderMetrics**：分析聚合

### 技术

- 事件存储：EventStoreDB（专用构建，处理投影）
- 考虑的替代方案：Kafka + 自定义投影服务

## 缺点

- 团队学习曲线
- 相比CRUD增加复杂性
- 需要仔细设计事件（存储后不可变）
- 存储增长（事件永不删除）

## 替代方案

1. **审计表**：更简单但不支持时态查询
2. **现有数据库CDC**：复杂，不改变数据模型
3. **混合**：仅对订单状态变更进行事件溯源

## 未解决问题

- [ ] 事件模式版本控制策略
- [ ] 事件保留策略
- [ ] 性能快照频率

## 实现计划

1. 单一订单类型原型（2周）
2. 团队事件溯源培训（1周）
3. 完整实现和迁移（4周）
4. 监控和优化（持续）

## 参考资料

- [Event Sourcing by Martin Fowler](https://martinfowler.com/eaaDev/EventSourcing.html)
- [EventStoreDB Documentation](https://www.eventstore.com/docs)
```

## ADR管理

### 目录结构

```
docs/
├── adr/
│   ├── README.md           # 索引和指南
│   ├── template.md         # 团队ADR模板
│   ├── 0001-use-postgresql.md
│   ├── 0002-caching-strategy.md
│   ├── 0003-mongodb-user-profiles.md  # [已废弃]
│   └── 0020-deprecate-mongodb.md      # 取代0003
```

### ADR索引（README.md）

```markdown
# 架构决策记录

此目录包含[项目名称]的架构决策记录（ADR）。

## 索引

| ADR | 标题 | 状态 | 日期 |
|-----|-------|--------|------|
| 0001 | 使用PostgreSQL作为主数据库 | 已接受 | 2024-01-10 |
| 0002 | Redis缓存策略 | 已接受 | 2024-01-12 |
| 0003 | MongoDB存储用户配置文件 | 已废弃 | 2023-06-15 |
| 0020 | 废弃MongoDB | 已接受 | 2024-01-15 |

## 创建新ADR

1. 复制 `template.md` 到 `NNNN-title-with-dashes.md`
2. 填写模板
3. 提交PR审查
4. 批准后更新此索引

## ADR状态

- **Proposed**：讨论中
- **Accepted**：已决策，实施中
- **Deprecated**：不再相关
- **Superseded**：被其他ADR取代
- **Rejected**：考虑过但未采用
```

### 自动化（adr-tools）

```bash
# 安装adr-tools
brew install adr-tools

# 初始化ADR目录
adr init docs/adr

# 创建新ADR
adr new "Use PostgreSQL as Primary Database"

# 取代ADR
adr new -s 3 "Deprecate MongoDB in Favor of PostgreSQL"

# 生成目录
adr generate toc > docs/adr/README.md

# 链接相关ADR
adr link 2 "Complements" 1 "Is complemented by"
```

## 审查流程

```markdown
## ADR审查清单

### 提交前
- [ ] 上下文清楚解释问题
- [ ] 考虑了所有可行选项
- [ ] 优缺点平衡且诚实
- [ ] 后果（正面和负面）已记录
- [ ] 相关ADR已链接

### 审查中
- [ ] 至少2名高级工程师审查
- [ ] 咨询受影响团队
- [ ] 考虑安全影响
- [ ] 记录成本影响
- [ ] 评估可逆性

### 接受后
- [ ] 更新ADR索引
- [ ] 通知团队
- [ ] 创建实现工单
- [ ] 更新相关文档
```

## 最佳实践

### 应该做的
- **尽早编写ADR** - 在实现开始之前
- **保持简短** - 最多1-2页
- **诚实面对权衡** - 包含真实的缺点
- **链接相关决策** - 构建决策图
- **更新状态** - 被取代时标记废弃

### 不应该做的
- **不要修改已接受的ADR** - 编写新的来取代
- **不要跳过上下文** - 未来读者需要背景
- **不要隐藏失败** - 被拒绝的决策也有价值
- **不要模糊** - 具体的决策，具体的后果
- **不要忘记实现** - 没有行动的ADR是浪费

## 资源

- [Documenting Architecture Decisions (Michael Nygard)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [MADR Template](https://adr.github.io/madr/)
- [ADR GitHub Organization](https://adr.github.io/)
- [adr-tools](https://github.com/npryce/adr-tools)

## 局限性
- 仅当任务明显符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
