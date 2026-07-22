---
name: django-perf-review
description: Django 性能代码审查。当被要求"审查 Django 性能"、"查找 N+1 查询"、"优化 Django"、"检查 queryset 性能"、"数据库性能"、"Django ORM 问题"或审计 Django 代码的性能问题时使用。
allowed-tools: Read, Grep, Glob, Bash, Task
license: LICENSE
risk: unknown
source: community
---

# Django 性能审查

审查 Django 代码以发现**已验证的**性能问题。研究代码库以在报告前确认问题。只报告你能证明的内容。

## 何时使用
- 你需要专注于已验证的 ORM 和查询问题的 Django 性能审查。
- 代码可能存在 N+1 查询、无界 queryset、缺失索引或其他数据库驱动的瓶颈。
- 你只需要可证明的性能发现，而非推测性的优化建议。

## 审查方法

1. **先研究** - 追踪数据流，检查现有优化，验证数据量
2. **报告前验证** - 模式匹配不是验证
3. **零发现是可接受的** - 不要为了显得全面而编造问题
4. **严重程度必须匹配影响** - 如果你发现自己在 CRITICAL 发现中写"次要"，那它就不是关键。降级或跳过。

## 影响类别

问题按影响组织。重点关注 CRITICAL 和 HIGH - 这些在规模化时会导致实际问题。

| 优先级 | 类别 | 影响 |
|--------|------|------|
| 1 | N+1 查询 | **CRITICAL** - 随数据倍增，导致超时 |
| 2 | 无界 Queryset | **CRITICAL** - 内存耗尽，OOM 终止 |
| 3 | 缺失索引 | **HIGH** - 大表全表扫描 |
| 4 | 写入循环 | **HIGH** - 锁竞争，慢请求 |
| 5 | 低效模式 | **LOW** - 很少值得报告 |

---

## 优先级 1：N+1 查询 (CRITICAL)

**影响：** 每个 N+1 增加 `O(n)` 次数据库往返。100 行 = 100 次额外查询。10,000 行 = 超时。

### 规则：预取循环中访问的关联数据

通过追踪验证：View → Queryset → Template/Serializer → 循环访问

```python
# 问题：N+1 - 每次迭代查询 profile
def user_list(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})

# 模板：
# {% for user in users %}
#     {{ user.profile.bio }}  ← 每个用户触发一次查询
# {% endfor %}

# 解决方案：在视图中预取
def user_list(request):
    users = User.objects.select_related('profile')
    return render(request, 'users.html', {'users': users})
```

### 规则：在序列化器中预取，不只是视图

DRF 序列化器访问关联字段会在 queryset 未优化时导致 N+1。

```python
# 问题：SerializerMethodField 每个对象查询一次
class UserSerializer(serializers.ModelSerializer):
    order_count = serializers.SerializerMethodField()

    def get_order_count(self, obj):
        return obj.orders.count()  # ← 每个用户一次查询

# 解决方案：在 viewset 中注解，在序列化器中访问
class UserViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return User.objects.annotate(order_count=Count('orders'))

class UserSerializer(serializers.ModelSerializer):
    order_count = serializers.IntegerField(read_only=True)
```

### 规则：在循环中查询的模型属性是危险的

```python
# 问题：属性被访问时触发查询
class User(models.Model):
    @property
    def recent_orders(self):
        return self.orders.filter(created__gte=last_week)[:5]

# 在模板循环中使用 = N+1

# 解决方案：使用带自定义 queryset 的 Prefetch，或注解
```

### N+1 验证清单
- [ ] 从视图追踪数据流到模板/序列化器
- [ ] 确认关联字段在循环内被访问
- [ ] 搜索代码库中现有的 select_related/prefetch_related
- [ ] 验证表有显著的行数（1000+）
- [ ] 确认这是热路径（不是 admin，不是罕见操作）

---

## 优先级 2：无界 Queryset (CRITICAL)

**影响：** 加载整个表会耗尽内存。大表会导致 OOM 终止和 worker 重启。

### 规则：始终对列表端点分页

```python
# 问题：无分页 - 加载所有行
class UserListView(ListView):
    model = User
    template_name = 'users.html'

# 解决方案：添加分页
class UserListView(ListView):
    model = User
    template_name = 'users.html'
    paginate_by = 25
```

### 规则：对大批量处理使用 iterator()

```python
# 问题：一次性将所有对象加载到内存
for user in User.objects.all():
    process(user)

# 解决方案：用 iterator() 流式处理
for user in User.objects.iterator(chunk_size=1000):
    process(user)
```

### 规则：永远不要对无界 queryset 调用 list()

```python
# 问题：强制完全求值到内存
all_users = list(User.objects.all())

# 解决方案：保持为 queryset，需要时切片
users = User.objects.all()[:100]
```

### 无界 Queryset 验证清单
- [ ] 表很大（10k+ 行）或会无限增长
- [ ] 没有分页类、paginate_by 或切片
- [ ] 这在面向用户的请求上运行（不是有分块的后台任务）

---

## 优先级 3：缺失索引 (HIGH)

**影响：** 全表扫描。小表可忽略，大表灾难性。

### 规则：对大表 WHERE 子句中使用的字段建索引

```python
# 问题：在未索引字段上过滤
# User.objects.filter(email=email)  # 无索引则全表扫描

class User(models.Model):
    email = models.EmailField()  # ← 无 db_index

# 解决方案：添加索引
class User(models.Model):
    email = models.EmailField(db_index=True)
```

### 规则：对大表 ORDER BY 中使用的字段建索引

```python
# 问题：无索引排序需要全表扫描
Order.objects.order_by('-created')

# 解决方案：索引排序字段
class Order(models.Model):
    created = models.DateTimeField(db_index=True)
```

### 规则：对常见查询模式使用复合索引

```python
class Order(models.Model):
    user = models.ForeignKey(User)
    status = models.CharField(max_length=20)
    created = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['user', 'status']),  # 用于 filter(user=x, status=y)
            models.Index(fields=['status', '-created']),  # 用于 filter(status=x).order_by('-created')
        ]
```

### 缺失索引验证清单
- [ ] 表有 10k+ 行
- [ ] 字段在热路径的 filter() 或 order_by() 中使用
- [ ] 检查模型 - 无 db_index=True 或 Meta.indexes 条目
- [ ] 不是外键（已自动索引）

---

## 优先级 4：写入循环 (HIGH)

**影响：** N 次数据库写入而非 1 次。锁竞争。慢请求。

### 规则：在循环中使用 bulk_create 而非 create()

```python
# 问题：N 次插入，N 次往返
for item in items:
    Model.objects.create(name=item['name'])

# 解决方案：单次批量插入
Model.objects.bulk_create([
    Model(name=item['name']) for item in items
])
```

### 规则：在循环中使用 update() 或 bulk_update 而非 save()

```python
# 问题：N 次更新
for obj in queryset:
    obj.status = 'done'
    obj.save()

# 解决方案 A：单条 UPDATE 语句（所有值相同）
queryset.update(status='done')

# 解决方案 B：bulk_update（不同值）
for obj in objects:
    obj.status = compute_status(obj)
Model.objects.bulk_update(objects, ['status'], batch_size=500)
```

### 规则：对 queryset 使用 delete()，而非循环

```python
# 问题：N 次删除
for obj in queryset:
    obj.delete()

# 解决方案：单条 DELETE
queryset.delete()
```

### 写入循环验证清单
- [ ] 循环迭代 100+ 项（或无界）
- [ ] 每次迭代调用 create()、save() 或 delete()
- [ ] 这在面向用户的请求上运行（不是一次性迁移脚本）

---

## 优先级 5：低效模式 (LOW)

**很少值得报告。** 仅在你已报告实际问题时作为次要备注包含。

### 模式：count() vs exists()

```python
# 稍微次优
if queryset.count() > 0:
    do_thing()

# 略好
if queryset.exists():
    do_thing()
```

**通常跳过** - 大多数情况下差异 <1ms。

### 模式：len(queryset) vs count()

```python
# 获取所有行来计数
if len(queryset) > 0:  # 如果 queryset 尚未求值则不好

# 单条 COUNT 查询
if queryset.count() > 0:
```

**仅标记** queryset 很大且尚未求值的情况。

### 模式：小循环中的 get()

```python
# N 次查询，但如果 N 很小（< 20），通常可以
for id in ids:
    obj = Model.objects.get(id=id)
```

**仅标记** 循环很大或这在非常热的路径中。

---

## 验证要求

报告任何问题前：

1. **追踪数据流** - 从创建到消费跟踪 queryset
2. **搜索现有优化** - Grep 搜索 select_related、prefetch_related、分页
3. **验证数据量** - 检查表是否真的很大
4. **确认热路径** - 追踪调用点，验证这频繁运行
5. **排除缓解措施** - 检查缓存、速率限制

**如果无法验证所有步骤，不要报告。**

---

## 输出格式

```markdown
## Django 性能审查：[文件/组件名称]

### 摘要
已验证问题：X（Y 个 Critical，Z 个 High）

### 发现

#### [PERF-001] UserListView 中的 N+1 查询 (CRITICAL)
**位置：** `views.py:45`

**问题：** 关联字段 `profile` 在模板循环中访问，未预取。

**验证：**
- 追踪：UserListView → users queryset → user_list.html → 循环中的 `{{ user.profile.bio }}`
- 搜索代码库：未找到 select_related('profile')
- User 表：50k+ 行（在 admin 中验证）
- 热路径：从首页导航链接

**证据：**
```python
def get_queryset(self):
    return User.objects.filter(active=True)  # 无 select_related
```

**修复：**
```python
def get_queryset(self):
    return User.objects.filter(active=True).select_related('profile')
```
```

如果未发现问题："审查 [文件] 并验证 [检查内容] 后未发现性能问题。"

**提交前，对每个发现进行合理性检查：**
- 严重程度是否匹配实际影响？（"次要低效" ≠ CRITICAL）
- 这是真正的性能问题还是只是风格偏好？
- 修复这个会显著改善性能吗？

如果任何答案为"否" - 移除该发现。

---

## 不应报告的内容

- 测试文件
- 仅 admin 的视图
- 管理命令
- 迁移文件
- 一次性脚本
- 禁用功能标志后的代码
- <1000 行且不会增长的表
- 冷路径中的模式（很少执行的代码）
- 微优化（exists vs count，无证据的 only/defer）

### 应避免的误报

**Queryset 变量赋值不是问题：**
```python
# 这没问题 - 无性能差异
projects_qs = Project.objects.filter(org=org)
projects = list(projects_qs)

# vs 这个 - 性能相同
projects = list(Project.objects.filter(org=org))
```
Queryset 是惰性的。赋值给变量不会执行任何操作。

**单查询模式不是 N+1：**
```python
# 这是一次查询，不是 N+1
projects = list(Project.objects.filter(org=org))
```
N+1 需要触发额外查询的循环。单个 `list()` 调用没问题。

**单对象获取时缺失 select_related 不是 N+1：**
```python
# 这是 2 次查询，不是 N+1 - 最多报告为 LOW
state = AutofixState.objects.filter(pr_id=pr_id).first()
project_id = state.request.project_id  # 第二次查询
```
N+1 需要循环。单个对象做 2 次查询而非 1 次可以报告为 LOW（如果相关），但绝不能是 CRITICAL/HIGH。

**风格偏好不是性能问题：**
如果你唯一的建议是"合并这两行"或"重命名这个变量" - 那是风格，不是性能。不要报告。

## 局限性
- 仅当任务明确匹配上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停下来请求澄清。
