---
name: django-access-review
description: Django 访问控制与 IDOR 安全审查。审查 Django 视图、DRF viewsets、ORM 查询或任何处理用户授权的 Python/Django 代码时使用。触发词："IDOR"、"access control"、"authorization"、"Django permissions"、"object permissions"、"tenant"...
risk: unknown
source: community
---

---
name: django-access-review
description: Django 访问控制与 IDOR 安全审查。审查 Django 视图、DRF viewsets、ORM 查询或任何处理用户授权的 Python/Django 代码时使用。触发词："IDOR"、"access control"、"authorization"、"Django permissions"、"object permissions"、"tenant"...
--- LICENSE
---

<!--
参考资料基于 OWASP Cheat Sheet Series (CC BY-SA 4.0)
https://cheatsheetseries.owasp.org/
-->

# Django 访问控制与 IDOR 审查

通过调查代码库如何回答一个问题来发现访问控制漏洞：

**用户 A 能否访问、修改或删除用户 B 的数据？**

## 何时使用
- 你需要审查 Django 或 DRF 代码的访问控制缺陷、IDOR 风险或对象级授权失败。
- 任务涉及确认一个用户是否能访问、修改或删除另一个用户的数据。
- 你想要调查驱动的授权审查，而非通用的模式匹配。

## 理念：调查优于模式匹配

不要扫描预定义的漏洞模式。相反：

1. **理解** 这个代码库如何实现授权
2. **提问** 关于具体数据流的问题
3. **追踪代码** 找到访问检查发生的位置（或是否发生）
4. **报告** 仅报告你通过调查确认的内容

每个代码库实现授权的方式不同。你的工作是理解这个特定实现，然后找出缺陷。

---

## 阶段 1：理解授权模型

在寻找 bug 之前，回答关于代码库的这些问题：

### 授权如何执行？

研究代码库以找到：

```
□ 权限检查在哪里实现？
  - 装饰器？(@login_required, @permission_required, 自定义？)
  - 中间件？(TenantMiddleware, AuthorizationMiddleware?)
  - 基类？(BaseAPIView, TenantScopedViewSet?)
  - 权限类？(DRF permission_classes?)
  - 自定义 mixin？(OwnershipMixin, TenantMixin?)

□ 查询如何限定范围？
  - 自定义管理器？(TenantManager, UserScopedManager?)
  - get_queryset() 重写？
  - 设置查询上下文的中间件？

□ 所有权模型是什么？
  - 单用户所有权？(document.owner_id)
  - 组织/租户所有权？(document.organization_id)
  - 层级结构？(org -> team -> user -> resource)
  - 上下文内的角色基础？(org admin vs member)
```

### 调查命令

```bash
# 查找授权通常如何实现
grep -rn "permission_classes\|@login_required\|@permission_required" --include="*.py" | head -20

# 查找视图继承的基类
grep -rn "class Base.*View\|class.*Mixin.*:" --include="*.py" | head -20

# 查找自定义管理器
grep -rn "class.*Manager\|def get_queryset" --include="*.py" | head -20

# 查找模型上的所有权字段
grep -rn "owner\|user_id\|organization\|tenant" --include="models.py" | head -30
```

**在理解授权模型之前不要继续。**

---

## 阶段 2：映射攻击面

识别处理用户特定数据的端点：

### 存在哪些资源？

```
□ 哪些模型包含用户数据？
□ 哪些有所有权字段 (owner_id, user_id, organization_id)？
□ 哪些通过 URL 或请求体中的 ID 访问？
```

### 暴露了哪些操作？

对每个资源，映射：
- 列表端点 - 返回什么数据？
- 详情/检索端点 - 对象如何获取？
- 创建端点 - 谁设置所有者？
- 更新端点 - 用户能否修改他人的数据？
- 删除端点 - 用户能否删除他人的数据？
- 自定义操作 - 它们访问什么？

---

## 阶段 3：提问并调查

对每个处理用户数据的端点，问：

### 核心问题

**"如果我是用户 A，我知道用户 B 资源的 ID，我能访问它吗？"**

追踪代码来回答：

```
1. 资源 ID 从哪里进入系统？
   - URL 路径: /api/documents/{id}/
   - 查询参数: ?document_id=123
   - 请求体: {"document_id": 123}

2. 该 ID 在哪里用于获取数据？
   - 找到 ORM 查询或数据库调用

3. 在 (1) 和 (2) 之间，存在什么检查？
   - 查询是否限定到当前用户？
   - 是否有显式的所有权检查？
   - 是否有对象上的权限检查？
   - 基类或 mixin 是否执行访问控制？

4. 如果找不到检查，是否有你遗漏的？
   - 检查父类
   - 检查中间件
   - 检查管理器
   - 检查 URL 级别的装饰器
```

### 后续问题

```
□ 对于列表端点：查询是否过滤到用户数据，还是返回所有内容？

□ 对于创建端点：谁设置所有者 - 服务器还是请求？

□ 对于批量操作：是否限定到用户数据？

□ 对于关联资源：如果我能访问一个文档，我能访问它的评论吗？
  如果文档属于其他人呢？

□ 对于租户/组织资源：组织 A 的用户能否通过更改 URL 中的 org_id
  访问组织 B 的数据？
```

---

## 阶段 4：追踪具体流程

选择一个具体端点并完整追踪。

### 示例调查

```
端点: GET /api/documents/{pk}/

1. 找到处理此 URL 的视图
   → DocumentViewSet.retrieve() 在 api/views.py

2. 检查 DocumentViewSet 继承自什么
   → class DocumentViewSet(viewsets.ModelViewSet)
   → 没有带授权的自定义基类

3. 检查 permission_classes
   → permission_classes = [IsAuthenticated]
   → 只检查登录，不检查所有权

4. 检查 get_queryset()
   → def get_queryset(self):
   →     return Document.objects.all()
   → 返回所有文档！

5. 检查 has_object_permission()
   → 未实现

6. 检查 retrieve() 方法
   → 使用默认实现，调用 get_object()
   → get_object() 使用 get_queryset()，返回所有文档

7. 结论: IDOR - 任何已认证用户可以访问任何文档
```

### 追踪时要寻找什么

```
潜在缺陷指标（需进一步调查，不要自动标记）：
- get_queryset() 返回 .all() 或过滤时未包含用户
- 直接 Model.objects.get(pk=pk) 查询中未包含所有权
- ID 来自敏感操作的请求体
- 权限类检查认证但不检查所有权
- 没有 has_object_permission() 且 queryset 未限定范围

可能安全的模式（但仍需验证实现）：
- get_queryset() 按 request.user 或用户组织过滤
- 自定义权限类带 has_object_permission()
- 强制限定范围的基类
- 自动过滤的管理器
```

---

## 阶段 5：报告发现

仅报告你通过调查确认的问题。

### 置信度级别

| 级别 | 含义 | 行动 |
|------|------|------|
| **高** | 追踪了流程，确认不存在检查 | 带证据报告 |
| **中** | 检查可能存在但无法确认 | 标记为需人工验证 |
| **低** | 理论上的，可能已被缓解 | 不报告 |

### 建议修复必须强制执行，而非文档化

**错误的修复**：添加注释说"调用者必须验证权限"
**正确的修复**：添加实际验证权限的代码

注释或文档字符串不执行授权。你建议的修复必须包含实际代码，该代码：
- 在继续之前验证用户有权限
- 如果未授权则抛出异常或返回错误
- 使未授权访问成为不可能，而非仅仅不鼓励

错误修复建议示例：
```python
def get_resource(resource_id):
    # 重要：调用者必须确保用户有权访问此资源
    return Resource.objects.get(pk=resource_id)
```

正确修复建议示例：
```python
def get_resource(resource_id, user):
    resource = Resource.objects.get(pk=resource_id)
    if resource.owner_id != user.id:
        raise PermissionDenied("访问被拒绝")
    return resource
```

如果你无法确定正确的强制执行机制，请说明 - 但永远不要建议文档作为修复。

### 报告格式

```markdown
## 访问控制审查：[组件]

### 授权模型
[简要描述此代码库如何处理授权]

### 发现

#### [IDOR-001] [标题] (严重程度：高/中)
- **位置**: `path/to/file.py:123`
- **置信度**: 高 - 通过代码追踪确认
- **问题**: 用户 A 能否访问用户 B 的文档？
- **调查**:
  1. 追踪 GET /api/documents/{pk}/ 到 DocumentViewSet
  2. 检查 get_queryset() - 返回 Document.objects.all()
  3. 检查 permission_classes - 只有 IsAuthenticated
  4. 检查 has_object_permission() - 未实现
  5. 验证没有相关的中间件或基类检查
- **证据**: [显示缺陷的代码片段]
- **影响**: 任何已认证用户可以通过 ID 读取任何文档
- **建议修复**: [强制执行授权的代码 - 不是注释]

### 需人工验证
[授权存在但无法确认有效性的问题]

### 未审查区域
[本次审查未覆盖的端点或流程]
```

---

## 常见 Django 授权模式

这些是你可能发现的模式 - 不是用来匹配的检查清单。

### 查询范围限定
```python
# 限定到用户
Document.objects.filter(owner=request.user)

# 限定到组织
Document.objects.filter(organization=request.user.organization)

# 使用自定义管理器
Document.objects.for_user(request.user)  # 调查它做了什么
```

### 权限执行
```python
# DRF 权限类
permission_classes = [IsAuthenticated, IsOwner]

# 自定义 has_object_permission
def has_object_permission(self, request, view, obj):
    return obj.owner == request.user

# Django 装饰器
@permission_required('app.view_document')

# 手动检查
if document.owner != request.user:
    raise PermissionDenied()
```

### 所有权分配
```python
# 服务端（安全）
def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

# 来自请求（需调查）
serializer.save(**request.data)  # request.data 是否包含 owner？
```

---

## 调查检查清单

用此指导你的审查，而非作为通过/失败检查清单：

```
□ 我理解此代码库通常如何实现授权
□ 我已识别所有权模型（用户、组织、租户等）
□ 我已映射处理用户数据的关键端点
□ 对每个敏感端点，我已追踪流程并询问：
  - ID 从哪里来？
  - 数据在哪里获取？
  - 输入和数据访问之间存在什么检查？
□ 我已通过检查父类和中间件验证我的发现
□ 我只报告了通过调查确认的问题
```

## 局限性
- 仅当任务明确匹配上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
