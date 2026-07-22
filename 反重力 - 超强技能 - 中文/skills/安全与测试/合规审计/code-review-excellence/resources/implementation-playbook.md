# 代码审查卓越实践实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

## 使用时机

- 审查 pull request 和代码变更
- 为团队建立代码审查标准
- 通过审查指导初级开发者
- 进行架构审查
- 创建审查检查清单和指南
- 改善团队协作
- 缩短代码审查周期
- 维护代码质量标准

## 核心原则

### 1. 审查心态

**代码审查的目标：**
- 发现 bug 和边界情况
- 确保代码可维护性
- 在团队内分享知识
- 执行编码规范
- 改进设计和架构
- 建设团队文化

**不是目标：**
- 炫耀知识
- 纠结格式（用 linter）
- 不必要地阻塞进度
- 按自己的偏好重写

### 2. 有效反馈

**好的反馈：**
- 具体且可操作
- 教育性而非评判性
- 针对代码而非个人
- 平衡（也表扬好的工作）
- 有优先级（关键 vs 可选）

```markdown
❌ 差："这是错的。"
✅ 好："多用户同时访问时可能导致竞态条件。考虑在这里使用互斥锁。"

❌ 差："为什么不用 X 模式？"
✅ 好："考虑过 Repository 模式吗？会让测试更容易。示例：[链接]"

❌ 差："重命名这个变量。"
✅ 好："[nit] 建议用 `userCount` 替代 `uc` 更清晰。如果你想保留也没问题，不阻塞。"
```

### 3. 审查范围

**应审查：**
- 逻辑正确性和边界情况
- 安全漏洞
- 性能影响
- 测试覆盖和质量
- 错误处理
- 文档和注释
- API 设计和命名
- 架构契合度

**不应手动审查：**
- 代码格式（用 Prettier、Black 等）
- import 组织
- lint 违规
- 简单的拼写错误

## 审查流程

### 阶段 1：收集上下文（2-3 分钟）

```markdown
深入代码前，先理解：

1. 阅读 PR 描述和关联的 issue
2. 检查 PR 大小（>400 行？要求拆分）
3. 检查 CI/CD 状态（测试通过？）
4. 理解业务需求
5. 记录相关的架构决策
```

### 阶段 2：高层审查（5-10 分钟）

```markdown
1. **架构与设计**
   - 方案是否匹配问题？
   - 有更简单的方案吗？
   - 是否与现有模式一致？
   - 能否扩展？

2. **文件组织**
   - 新文件位置是否正确？
   - 代码分组是否合理？
   - 是否有重复文件？

3. **测试策略**
   - 有测试吗？
   - 测试覆盖边界情况吗？
   - 测试可读吗？
```

### 阶段 3：逐行审查（10-20 分钟）

```markdown
对每个文件：

1. **逻辑与正确性**
   - 边界情况处理了吗？
   - 差一错误？
   - Null/undefined 检查？
   - 竞态条件？

2. **安全性**
   - 输入验证？
   - SQL 注入风险？
   - XSS 漏洞？
   - 敏感数据暴露？

3. **性能**
   - N+1 查询？
   - 不必要的循环？
   - 内存泄漏？
   - 阻塞操作？

4. **可维护性**
   - 变量名清晰？
   - 函数职责单一？
   - 复杂代码有注释？
   - 魔法数字提取了？
```

### 阶段 4：总结与决策（2-3 分钟）

```markdown
1. 总结关键问题
2. 强调做得好的地方
3. 做出明确决定：
   - ✅ 批准
   - 💬 评论（次要建议）
   - 🔄 要求修改（必须处理）
4. 如果复杂，提议结对
```

## 审查技巧

### 技巧 1：检查清单法

```markdown
## 安全检查清单
- [ ] 用户输入已验证和清理
- [ ] SQL 查询使用参数化
- [ ] 认证/授权已检查
- [ ] 密钥未硬编码
- [ ] 错误消息不泄露信息

## 性能检查清单
- [ ] 无 N+1 查询
- [ ] 数据库查询有索引
- [ ] 大列表已分页
- [ ] 昂贵操作已缓存
- [ ] 热路径无阻塞 I/O

## 测试检查清单
- [ ] 正常路径已测试
- [ ] 边界情况已覆盖
- [ ] 错误情况已测试
- [ ] 测试名称描述清晰
- [ ] 测试确定性
```

### 技巧 2：提问法

不要直接指出问题，而是提问引导思考：

```markdown
❌ "列表为空时会失败。"
✅ "如果 `items` 是空数组会怎样？"

❌ "这里需要错误处理。"
✅ "如果 API 调用失败应该怎么处理？"

❌ "这效率低。"
✅ "我看到这里遍历了所有用户。考虑过 10 万用户时的性能影响吗？"
```

### 技巧 3：建议而非命令

```markdown
## 使用协作性语言

❌ "必须改成 async/await"
✅ "建议：async/await 可能更易读：
    ```typescript
    async function fetchUser(id: string) {
        const user = await db.query('SELECT * FROM users WHERE id = ?', id);
        return user;
    }
    ```
    你觉得呢？"

❌ "提取成函数"
✅ "这段逻辑在 3 处出现。是否值得提取成共享工具函数？"
```

### 技巧 4：区分严重程度

```markdown
用标签表示优先级：

🔴 [blocking] - 合并前必须修复
🟡 [important] - 应该修复，有异议可讨论
🟢 [nit] - 建议改进，不阻塞
💡 [suggestion] - 可考虑的替代方案
📚 [learning] - 教育性评论，无需操作
🎉 [praise] - 做得好，继续保持！

示例：
"🔴 [blocking] 这个 SQL 查询有注入风险。请使用参数化查询。"

"🟢 [nit] 建议将 `data` 重命名为 `userData` 更清晰。"

"🎉 [praise] 测试覆盖很棒！能捕获边界情况。"
```

## 语言特定模式

### Python 代码审查

```python
# 检查 Python 特有问题

# ❌ 可变默认参数
def add_item(item, items=[]):  # Bug! 调用间共享
    items.append(item)
    return items

# ✅ 用 None 作为默认值
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# ❌ 捕获范围太广
try:
    result = risky_operation()
except:  # 捕获一切，包括 KeyboardInterrupt！
    pass

# ✅ 捕获特定异常
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise

# ❌ 使用可变类属性
class User:
    permissions = []  # 所有实例共享！

# ✅ 在 __init__ 中初始化
class User:
    def __init__(self):
        self.permissions = []
```

### TypeScript/JavaScript 代码审查

```typescript
// 检查 TypeScript 特有问题

// ❌ 使用 any 破坏类型安全
function processData(data: any) {  // 避免 any
    return data.value;
}

// ✅ 使用正确类型
interface DataPayload {
    value: string;
}
function processData(data: DataPayload) {
    return data.value;
}

// ❌ 未处理异步错误
async function fetchUser(id: string) {
    const response = await fetch(`/api/users/${id}`);
    return response.json();  // 网络失败怎么办？
}

// ✅ 正确处理错误
async function fetchUser(id: string): Promise<User> {
    try {
        const response = await fetch(`/api/users/${id}`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch user:', error);
        throw error;
    }
}

// ❌ 变更 props
function UserProfile({ user }: Props) {
    user.lastViewed = new Date();  // 变更 prop！
    return <div>{user.name}</div>;
}

// ✅ 不变更 props
function UserProfile({ user, onView }: Props) {
    useEffect(() => {
        onView(user.id);  // 通知父组件更新
    }, [user.id]);
    return <div>{user.name}</div>;
}
```

## 高级审查模式

### 模式 1：架构审查

```markdown
审查重大变更时：

1. **先看设计文档**
   - 大功能先要求设计文档再写代码
   - 实现前与团队审查设计
   - 达成一致避免返工

2. **分阶段审查**
   - 第一个 PR：核心抽象和接口
   - 第二个 PR：实现
   - 第三个 PR：集成和测试
   - 更易审查，迭代更快

3. **考虑替代方案**
   - "考虑过使用 [模式/库] 吗？"
   - "与更简单方案的权衡是什么？"
   - "需求变化时如何演进？"
```

### 模式 2：测试质量审查

```typescript
// ❌ 差测试：测试实现细节
test('increments counter variable', () => {
    const component = render(<Counter />);
    const button = component.getByRole('button');
    fireEvent.click(button);
    expect(component.state.counter).toBe(1);  // 测试内部状态
});

// ✅ 好测试：测试行为
test('displays incremented count when clicked', () => {
    render(<Counter />);
    const button = screen.getByRole('button', { name: /increment/i });
    fireEvent.click(button);
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
});

// 测试审查问题：
// - 测试描述行为而非实现？
// - 测试名称清晰描述？
// - 覆盖边界情况？
// - 测试独立（无共享状态）？
// - 测试可任意顺序运行？
```

### 模式 3：安全审查

```markdown
## 安全审查检查清单

### 认证与授权
- [ ] 需要认证的地方有认证？
- [ ] 每个操作前有授权检查？
- [ ] JWT 验证正确（签名、过期）？
- [ ] API 密钥/密钥安全存储？

### 输入验证
- [ ] 所有用户输入已验证？
- [ ] 文件上传有限制（大小、类型）？
- [ ] SQL 查询参数化？
- [ ] XSS 防护（转义输出）？

### 数据保护
- [ ] 密码已哈希（bcrypt/argon2）？
- [ ] 敏感数据静态加密？
- [ ] 敏感数据强制 HTTPS？
- [ ] PII 按法规处理？

### 常见漏洞
- [ ] 无 eval() 或类似动态执行？
- [ ] 无硬编码密钥？
- [ ] 状态变更操作有 CSRF 防护？
- [ ] 公开端点有速率限制？
```

## 给出困难反馈

### 模式：三明治法（改进版）

```markdown
传统：表扬 + 批评 + 表扬（感觉假）

更好：上下文 + 具体问题 + 有用方案

示例：
"我注意到支付处理逻辑内联在控制器中。这让测试和复用变难。

[具体问题]
calculateTotal() 函数混合了税费计算、折扣逻辑和数据库查询，
难以单元测试和推理。

[有用方案]
能否提取成 PaymentService 类？这样可测试且可复用。
需要的话我可以和你结对完成。"
```

### 处理分歧

```markdown
当作者不同意你的反馈时：

1. **寻求理解**
   "帮我理解你的思路。是什么让你选择这个模式？"

2. **承认合理观点**
   "关于 X 这点你说得对。我之前没考虑到。"

3. **提供数据**
   "我担心性能。能加个基准测试验证方案吗？"

4. **必要时升级**
   "让 [架构师/资深开发者] 来看看这个。"

5. **知道何时放手**
   如果能工作且不是关键问题，就批准。
   完美是进步的敌人。
```

## 最佳实践

1. **及时审查**：24 小时内，最好当天
2. **限制 PR 大小**：有效审查最多 200-400 行
3. **分时段审查**：最多 60 分钟，注意休息
4. **使用审查工具**：GitHub、GitLab 或专用工具
5. **自动化能自动化的**：linter、格式化器、安全扫描
6. **建立关系**：表情符号、表扬、同理心很重要
7. **保持响应**：复杂问题提议结对
8. **向他人学习**：看别人的审查评论

## 常见陷阱

- **完美主义**：因次要风格偏好阻塞 PR
- **范围蔓延**："顺便也把那个改了..."
- **不一致**：对不同人用不同标准
- **延迟审查**：让 PR 放好几天
- **消失**：要求修改后消失
- **橡皮图章**：不实际审查就批准
- **自行车棚效应**：在琐事上争论不休

## 模板

### PR 审查评论模板

```markdown
## 概要
[审查内容简述]

## 亮点
- [做得好的地方]
- [好的模式或方案]

## 必须修改
🔴 [阻塞问题 1]
🔴 [阻塞问题 2]

## 建议
💡 [改进 1]
💡 [改进 2]

## 问题
❓ [需要澄清的 X]
❓ [考虑的替代方案]

## 结论
✅ 处理必须修改后批准
```

## 资源

- **references/code-review-best-practices.md**：全面审查指南
- **references/common-bugs-checklist.md**：语言特定的常见 bug
- **references/security-review-guide.md**：安全审查检查清单
- **assets/pr-review-template.md**：标准审查评论模板
- **assets/review-checklist.md**：快速参考检查清单
- **scripts/pr-analyzer.py**：分析 PR 复杂度并建议审查者
