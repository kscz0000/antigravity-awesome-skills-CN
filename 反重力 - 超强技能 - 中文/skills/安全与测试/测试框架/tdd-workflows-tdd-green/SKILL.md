---
name: tdd-workflows-tdd-green
description: "在 TDD 绿灯阶段，编写让失败测试通过所需的最简代码。触发词：TDD绿灯、绿灯阶段、最小实现、让测试通过、green phase"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 绿灯阶段：简单函数
def product_list(request):
    products = Product.objects.all()
    return JsonResponse({'products': list(products.values())})

# 重构：基于类的视图
class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return JsonResponse({'products': list(products.values())})

# 重构：通用视图
class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
```

### Express 模式

**内联 → 中间件 → 服务层：**
```javascript
// 绿灯阶段：内联逻辑
app.post('/api/users', (req, res) => {
  const user = { id: Date.now(), ...req.body };
  users.push(user);
  res.json(user);
});

// 重构：提取中间件
app.post('/api/users', validateUser, (req, res) => {
  const user = userService.create(req.body);
  res.json(user);
});

// 重构：完整分层
app.post('/api/users',
  validateUser,
  asyncHandler(userController.create)
);
```

## 适用场景

- TDD 循环中从红灯转到绿灯
- 编写最简行为以满足测试
- 刻意保持实现简单

## 不适用场景

- 因设计或性能原因进行重构
- 测试已通过，需要新增需求
- 需要完整的架构重设计

## 操作步骤

1. 审查失败测试，定位最小修复方案
2. 编写最简变更以通过下一个测试
3. 每次变更后运行测试确认进展
4. 记录捷径或技术债务，留待重构阶段处理

## 安全准则

- 不要绕过测试来使其通过
- 变更范围仅限于失败的行为

## 资源

- `resources/implementation-playbook.md` 包含详细模式和示例。

## 限制条件
- 仅在任务明确匹配上述范围时使用此技能
- 不要将输出视为环境特定验证、测试或专家审查的替代品
- 如缺少必需的输入、权限、安全边界或成功标准，请停下来要求澄清
