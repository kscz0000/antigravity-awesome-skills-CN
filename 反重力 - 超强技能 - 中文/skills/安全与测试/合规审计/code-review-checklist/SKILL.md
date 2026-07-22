---
name: code-review-checklist
description: "全面的代码审查清单，涵盖功能、安全、性能和可维护性。当用户要求'代码审查'、'code review'、'审查PR'、'代码审核'或相关主题时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 代码审查清单

## 概述

提供系统化的代码审查清单。帮助审查者确保代码质量、发现 bug、识别安全问题，并保持代码库的一致性。

## 使用场景

- 审查 pull request 时使用
- 进行代码审计时使用
- 为团队建立代码审查标准时使用
- 培训新开发者代码审查实践时使用
- 确保审查不遗漏任何问题时使用
- 创建代码审查文档时使用

## 工作流程

### 步骤 1：理解上下文

审查代码前，我会帮你理解：
- 这段代码解决什么问题？
- 需求是什么？
- 哪些文件被修改了，为什么？
- 是否有相关的 issue 或工单？
- 测试策略是什么？

### 步骤 2：审查功能

检查代码是否正确工作：
- 是否解决了陈述的问题？
- 边界情况是否处理？
- 错误处理是否恰当？
- 是否存在逻辑错误？
- 是否符合需求？

### 步骤 3：审查代码质量

评估代码可维护性：
- 代码是否清晰易读？
- 命名是否有描述性？
- 结构是否合理？
- 函数/方法是否聚焦？
- 是否存在不必要的复杂性？

### 步骤 4：审查安全

检查安全问题：
- 输入是否验证？
- 敏感数据是否保护？
- 是否存在 SQL 注入风险？
- 认证/授权是否正确？
- 依赖是否安全？

### 步骤 5：审查性能

查找性能问题：
- 是否存在不必要的循环？
- 数据库访问是否优化？
- 是否存在内存泄漏？
- 缓存使用是否恰当？
- 是否存在 N+1 查询问题？

### 步骤 6：审查测试

验证测试覆盖：
- 新代码是否有测试？
- 测试是否覆盖边界情况？
- 测试是否有意义？
- 所有测试是否通过？
- 测试覆盖率是否足够？

## 示例

### 示例 1：功能审查清单

```markdown
## 功能审查

### 需求
- [ ] 代码解决了陈述的问题
- [ ] 所有验收标准已满足
- [ ] 边界情况已处理
- [ ] 错误情况已处理
- [ ] 用户输入已验证

### 逻辑
- [ ] 无逻辑错误或 bug
- [ ] 条件正确（无差一错误）
- [ ] 循环正确终止
- [ ] 递归有正确的基准情况
- [ ] 状态管理正确

### 错误处理
- [ ] 错误被恰当捕获
- [ ] 错误消息清晰有用
- [ ] 错误不暴露敏感信息
- [ ] 失败操作已回滚
- [ ] 日志记录恰当

### 需要发现的问题示例：

**❌ 错误 - 缺少验证：**
\`\`\`javascript
function createUser(email, password) {
  // 无验证！
  return db.users.create({ email, password });
}
\`\`\`

**✅ 正确 - 恰当验证：**
\`\`\`javascript
function createUser(email, password) {
  if (!email || !isValidEmail(email)) {
    throw new Error('Invalid email address');
  }
  if (!password || password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }
  return db.users.create({ email, password });
}
\`\`\`
```

### 示例 2：安全审查清单

```markdown
## 安全审查

### 输入验证
- [ ] 所有用户输入已验证
- [ ] SQL 注入已防护（使用参数化查询）
- [ ] XSS 已防护（转义输出）
- [ ] CSRF 保护已到位
- [ ] 文件上传已验证（类型、大小、内容）

### 认证与授权
- [ ] 需要认证的地方已要求认证
- [ ] 授权检查已存在
- [ ] 密码已哈希（绝不存储明文）
- [ ] 会话管理安全
- [ ] Token 过期设置恰当

### 数据保护
- [ ] 敏感数据已加密
- [ ] API 密钥未硬编码
- [ ] 密钥使用环境变量
- [ ] 个人数据符合隐私法规
- [ ] 数据库凭证安全

### 依赖
- [ ] 无已知漏洞依赖
- [ ] 依赖已更新
- [ ] 不必要依赖已移除
- [ ] 依赖版本已固定

### 需要发现的问题示例：

**❌ 错误 - SQL 注入风险：**
\`\`\`javascript
const query = \`SELECT * FROM users WHERE email = '\${email}'\`;
db.query(query);
\`\`\`

**✅ 正确 - 参数化查询：**
\`\`\`javascript
const query = 'SELECT * FROM users WHERE email = $1';
db.query(query, [email]);
\`\`\`

**❌ 错误 - 硬编码密钥：**
\`\`\`javascript
const API_KEY = 'sk_live_abc123xyz';
\`\`\`

**✅ 正确 - 环境变量：**
\`\`\`javascript
const API_KEY = process.env.API_KEY;
if (!API_KEY) {
  throw new Error('API_KEY environment variable is required');
}
\`\`\`
```

### 示例 3：代码质量审查清单

```markdown
## 代码质量审查

### 可读性
- [ ] 代码易于理解
- [ ] 变量名有描述性
- [ ] 函数名说明其功能
- [ ] 复杂逻辑有注释
- [ ] 魔法数字已替换为常量

### 结构
- [ ] 函数小而聚焦
- [ ] 代码遵循 DRY 原则（不要重复自己）
- [ ] 关注点分离恰当
- [ ] 代码风格一致
- [ ] 无死代码或注释掉的代码

### 可维护性
- [ ] 代码模块化可复用
- [ ] 依赖最小化
- [ ] 变更向后兼容
- [ ] 破坏性变更已记录
- [ ] 技术债务已标注

### 需要发现的问题示例：

**❌ 错误 - 命名不清：**
\`\`\`javascript
function calc(a, b, c) {
  return a * b + c;
}
\`\`\`

**✅ 正确 - 描述性命名：**
\`\`\`javascript
function calculateTotalPrice(quantity, unitPrice, tax) {
  return quantity * unitPrice + tax;
}
\`\`\`

**❌ 错误 - 函数职责过多：**
\`\`\`javascript
function processOrder(order) {
  // 验证订单
  if (!order.items) throw new Error('No items');
  
  // 计算总额
  let total = 0;
  for (let item of order.items) {
    total += item.price * item.quantity;
  }
  
  // 应用折扣
  if (order.coupon) {
    total *= 0.9;
  }
  
  // 处理支付
  const payment = stripe.charge(total);
  
  // 发送邮件
  sendEmail(order.email, 'Order confirmed');
  
  // 更新库存
  updateInventory(order.items);
  
  return { orderId: order.id, total };
}
\`\`\`

**✅ 正确 - 关注点分离：**
\`\`\`javascript
function processOrder(order) {
  validateOrder(order);
  const total = calculateOrderTotal(order);
  const payment = processPayment(total);
  sendOrderConfirmation(order.email);
  updateInventory(order.items);
  
  return { orderId: order.id, total };
}
\`\`\`
```

## 最佳实践

### ✅ 应该做

- **审查小变更** — 较小的 PR 更容易彻底审查
- **先检查测试** — 验证测试通过且覆盖新代码
- **运行代码** — 尽可能在本地测试
- **提出问题** — 不要假设，要求澄清
- **建设性反馈** — 提出改进建议，而非单纯批评
- **聚焦重要问题** — 不要纠结细枝末节的风格问题
- **使用自动化工具** — Linter、格式化工具、安全扫描器
- **审查文档** — 检查文档是否更新
- **考虑性能** — 思考规模和效率
- **检查回归** — 确保现有功能仍正常工作

### ❌ 不应该做

- **不读就批准** — 实际审查代码
- **反馈模糊** — 提供具体反馈和示例
- **忽视安全** — 安全问题至关重要
- **跳过测试** — 未测试的代码会出问题
- **态度粗鲁** — 保持尊重和专业
- **走过场** — 每次审查都应创造价值
- **疲劳时审查** — 会遗漏重要问题
- **忘记上下文** — 理解全局图景

## 完整审查清单

### 审查前
- [ ] 阅读 PR 描述和关联 issue
- [ ] 理解正在解决的问题
- [ ] 检查 CI/CD 测试是否通过
- [ ] 拉取分支并在本地运行

### 功能
- [ ] 代码解决了陈述的问题
- [ ] 边界情况已处理
- [ ] 错误处理恰当
- [ ] 用户输入已验证
- [ ] 无逻辑错误

### 安全
- [ ] 无 SQL 注入漏洞
- [ ] 无 XSS 漏洞
- [ ] 认证/授权正确
- [ ] 敏感数据已保护
- [ ] 无硬编码密钥

### 性能
- [ ] 无不必要的数据库查询
- [ ] 无 N+1 查询问题
- [ ] 使用高效算法
- [ ] 无内存泄漏
- [ ] 缓存使用恰当

### 代码质量
- [ ] 代码清晰易读
- [ ] 命名有描述性
- [ ] 函数聚焦且小
- [ ] 无代码重复
- [ ] 遵循项目规范

### 测试
- [ ] 新代码有测试
- [ ] 测试覆盖边界情况
- [ ] 测试有意义
- [ ] 所有测试通过
- [ ] 测试覆盖率足够

### 文档
- [ ] 代码注释解释原因，而非内容
- [ ] API 文档已更新
- [ ] README 已更新（如需要）
- [ ] 破坏性变更已记录
- [ ] 迁移指南已提供（如需要）

### Git
- [ ] 提交消息清晰
- [ ] 无合并冲突
- [ ] 分支与 main 同步
- [ ] 无不必要的文件提交
- [ ] .gitignore 配置正确

## 常见陷阱

### 问题：遗漏边界情况
**症状：** 代码在正常路径工作，但在边界情况失败
**解决方案：** 问"如果……会怎样？"问题
- 如果输入为 null？
- 如果数组为空？
- 如果用户未认证？
- 如果网络请求失败？

### 问题：安全漏洞
**症状：** 代码暴露安全风险
**解决方案：** 使用安全清单
- 运行安全扫描器（npm audit, Snyk）
- 检查 OWASP Top 10
- 验证所有输入
- 使用参数化查询
- 永不信任用户输入

### 问题：测试覆盖不足
**症状：** 新代码无测试或测试不足
**解决方案：** 要求所有新代码有测试
- 函数的单元测试
- 功能的集成测试
- 边界情况测试
- 错误情况测试

### 问题：代码不清晰
**症状：** 审查者无法理解代码功能
**解决方案：** 要求改进
- 更好的变量名
- 解释性注释
- 更小的函数
- 清晰的结构

## 审查评论模板

### 要求修改
```markdown
**问题：** [描述问题]

**当前代码：**
\`\`\`javascript
// 展示有问题的代码
\`\`\`

**建议修复：**
\`\`\`javascript
// 展示改进后的代码
\`\`\`

**原因：** [解释为什么这样更好]
```

### 提问
```markdown
**问题：** [你的问题]

**上下文：** [你提问的原因]

**建议：** [如果有]
```

### 赞扬好代码
```markdown
**很好！** [你喜欢的地方]

这很棒，因为 [解释原因]
```

## 相关技能

- `@requesting-code-review` — 准备代码接受审查
- `@receiving-code-review` — 处理审查反馈
- `@systematic-debugging` — 调试审查中发现的问题
- `@test-driven-development` — 确保代码有测试

## 更多资源

- [Google Code Review Guidelines](https://google.github.io/eng-practices/review/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Code Review Best Practices](https://github.com/thoughtbot/guides/tree/main/code-review)
- [How to Review Code](https://www.kevinlondon.com/2015/05/05/code-review-best-practices.html)

---

**专业提示：** 每次审查都使用清单模板，确保一致性和彻底性。根据团队具体需求定制！

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
