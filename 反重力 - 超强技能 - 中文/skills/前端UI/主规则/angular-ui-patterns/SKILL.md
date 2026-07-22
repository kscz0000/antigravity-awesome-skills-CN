---
name: angular-ui-patterns
description: "现代 Angular UI 模式，涵盖加载状态、错误处理和数据展示。在构建 UI 组件、处理异步数据或管理组件状态时使用。触发词：Angular UI模式、加载状态、错误处理、空状态、骨架屏、延迟加载、@defer、信号、Signal、表单验证、对话框、模态框、按钮状态、乐观更新"
risk: safe
source: self
date_added: "2026-02-27"
---

# Angular UI 模式

## 核心原则

1. **永不显示过期 UI** - 仅在实际加载时显示加载状态
2. **始终暴露错误** - 用户必须知道何时出现问题
3. **乐观更新** - 让 UI 感觉即时响应
4. **渐进式披露** - 使用 `@defer` 在内容可用时显示
5. **优雅降级** - 部分数据优于无数据

---

## 加载状态模式

### 黄金法则

**仅当没有数据可显示时才显示加载指示器。**

```typescript
@Component({
  template: `
    @if (error()) {
      <app-error-state [error]="error()" (retry)="load()" />
    } @else if (loading() && !items().length) {
      <app-skeleton-list />
    } @else if (!items().length) {
      <app-empty-state message="No items found" />
    } @else {
      <app-item-list [items]="items()" />
    }
  `,
})
export class ItemListComponent {
  private store = inject(ItemStore);

  items = this.store.items;
  loading = this.store.loading;
  error = this.store.error;
}
```

### 加载状态决策树

```
是否存在错误？
  → 是：显示错误状态并提供重试选项
  → 否：继续

是否正在加载且没有数据？
  → 是：显示加载指示器（旋转器/骨架屏）
  → 否：继续

是否有数据？
  → 是，有数据项：显示数据
  → 是，但为空：显示空状态
  → 否：显示加载（兜底）
```

### 骨架屏 vs 旋转器

| 使用骨架屏的场景       | 使用旋转器的场景       |
| ---------------------- | ---------------------- |
| 已知内容形状           | 未知内容形状           |
| 列表/卡片布局          | 模态操作               |
| 初始页面加载           | 按钮提交               |
| 内容占位符             | 内联操作               |

---

## 控制流模式

### @if/@else 条件渲染

```html
@if (user(); as user) {
<span>Welcome, {{ user.name }}</span>
} @else if (loading()) {
<app-spinner size="small" />
} @else {
<a routerLink="/login">Sign In</a>
}
```

### @for 与 track

```html
@for (item of items(); track item.id) {
<app-item-card [item]="item" (delete)="remove(item.id)" />
} @empty {
<app-empty-state
  icon="inbox"
  message="No items yet"
  actionLabel="Create Item"
  (action)="create()"
/>
}
```

### @defer 渐进式加载

```html
<!-- 关键内容立即加载 -->
<app-header />
<app-hero-section />

<!-- 非关键内容延迟加载 -->
@defer (on viewport) {
<app-comments [postId]="postId()" />
} @placeholder {
<div class="h-32 bg-gray-100 animate-pulse"></div>
} @loading (minimum 200ms) {
<app-spinner />
} @error {
<app-error-state message="Failed to load comments" />
}
```

---

## 错误处理模式

### 错误处理层级

```
1. 内联错误（字段级）→ 表单验证错误
2. Toast 通知 → 可恢复错误，用户可重试
3. 错误横幅 → 页面级错误，数据仍部分可用
4. 全屏错误 → 不可恢复，需要用户操作
```

### 始终显示错误

**关键：绝不要静默吞掉错误。**

```typescript
// 正确 - 错误始终暴露给用户
@Component({...})
export class CreateItemComponent {
  private store = inject(ItemStore);
  private toast = inject(ToastService);

  async create(data: CreateItemDto) {
    try {
      await this.store.create(data);
      this.toast.success('Item created successfully');
      this.router.navigate(['/items']);
    } catch (error) {
      console.error('createItem failed:', error);
      this.toast.error('Failed to create item. Please try again.');
    }
  }
}

// 错误 - 错误被静默捕获
async create(data: CreateItemDto) {
  try {
    await this.store.create(data);
  } catch (error) {
    console.error(error); // 用户什么都看不到！
  }
}
```

### 错误状态组件模式

```typescript
@Component({
  selector: "app-error-state",
  standalone: true,
  imports: [NgOptimizedImage],
  template: `
    <div class="error-state">
      <img ngSrc="/assets/error-icon.svg" width="64" height="64" alt="" />
      <h3>{{ title() }}</h3>
      <p>{{ message() }}</p>
      @if (retry.observed) {
        <button (click)="retry.emit()" class="btn-primary">Try Again</button>
      }
    </div>
  `,
})
export class ErrorStateComponent {
  title = input("Something went wrong");
  message = input("An unexpected error occurred");
  retry = output<void>();
}
```

---

## 按钮状态模式

### 按钮加载状态

```html
<button
  (click)="handleSubmit()"
  [disabled]="isSubmitting() || !form.valid"
  class="btn-primary"
>
  @if (isSubmitting()) {
  <app-spinner size="small" class="mr-2" />
  Saving... } @else { Save Changes }
</button>
```

### 操作期间禁用

**关键：异步操作期间始终禁用触发器。**

```typescript
// 正确 - 加载时禁用按钮
@Component({
  template: `
    <button
      [disabled]="saving()"
      (click)="save()"
    >
      @if (saving()) {
        <app-spinner size="sm" /> Saving...
      } @else {
        Save
      }
    </button>
  `
})
export class SaveButtonComponent {
  saving = signal(false);

  async save() {
    this.saving.set(true);
    try {
      await this.service.save();
    } finally {
      this.saving.set(false);
    }
  }
}

// 错误 - 用户可以多次点击
<button (click)="save()">
  {{ saving() ? 'Saving...' : 'Save' }}
</button>
```

---

## 空状态

### 空状态要求

每个列表/集合必须有空状态：

```html
@for (item of items(); track item.id) {
<app-item-card [item]="item" />
} @empty {
<app-empty-state
  icon="folder-open"
  title="No items yet"
  description="Create your first item to get started"
  actionLabel="Create Item"
  (action)="openCreateDialog()"
/>
}
```

### 上下文空状态

```typescript
@Component({
  selector: "app-empty-state",
  template: `
    <div class="empty-state">
      <span class="icon" [class]="icon()"></span>
      <h3>{{ title() }}</h3>
      <p>{{ description() }}</p>
      @if (actionLabel()) {
        <button (click)="action.emit()" class="btn-primary">
          {{ actionLabel() }}
        </button>
      }
    </div>
  `,
})
export class EmptyStateComponent {
  icon = input("inbox");
  title = input.required<string>();
  description = input("");
  actionLabel = input<string | null>(null);
  action = output<void>();
}
```

---

## 表单模式

### 带加载和验证的表单

```typescript
@Component({
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <div class="form-field">
        <label for="name">Name</label>
        <input
          id="name"
          formControlName="name"
          [class.error]="isFieldInvalid('name')"
        />
        @if (isFieldInvalid("name")) {
          <span class="error-text">
            {{ getFieldError("name") }}
          </span>
        }
      </div>

      <div class="form-field">
        <label for="email">Email</label>
        <input id="email" type="email" formControlName="email" />
        @if (isFieldInvalid("email")) {
          <span class="error-text">
            {{ getFieldError("email") }}
          </span>
        }
      </div>

      <button type="submit" [disabled]="form.invalid || submitting()">
        @if (submitting()) {
          <app-spinner size="sm" /> Submitting...
        } @else {
          Submit
        }
      </button>
    </form>
  `,
})
export class UserFormComponent {
  private fb = inject(FormBuilder);

  submitting = signal(false);

  form = this.fb.group({
    name: ["", [Validators.required, Validators.minLength(2)]],
    email: ["", [Validators.required, Validators.email]],
  });

  isFieldInvalid(field: string): boolean {
    const control = this.form.get(field);
    return control ? control.invalid && control.touched : false;
  }

  getFieldError(field: string): string {
    const control = this.form.get(field);
    if (control?.hasError("required")) return "This field is required";
    if (control?.hasError("email")) return "Invalid email format";
    if (control?.hasError("minlength")) return "Too short";
    return "";
  }

  async onSubmit() {
    if (this.form.invalid) return;

    this.submitting.set(true);
    try {
      await this.service.submit(this.form.value);
      this.toast.success("Submitted successfully");
    } catch {
      this.toast.error("Submission failed");
    } finally {
      this.submitting.set(false);
    }
  }
}
```

---

## 对话框/模态框模式

### 确认对话框

```typescript
// dialog.service.ts
@Injectable({ providedIn: 'root' })
export class DialogService {
  private dialog = inject(Dialog); // CDK Dialog or custom

  async confirm(options: {
    title: string;
    message: string;
    confirmText?: string;
    cancelText?: string;
  }): Promise<boolean> {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: options,
    });

    return await firstValueFrom(dialogRef.closed) ?? false;
  }
}

// 使用方式
async deleteItem(item: Item) {
  const confirmed = await this.dialog.confirm({
    title: 'Delete Item',
    message: `Are you sure you want to delete "${item.name}"?`,
    confirmText: 'Delete',
  });

  if (confirmed) {
    await this.store.delete(item.id);
  }
}
```

---

## 反模式

### 加载状态

```typescript
// 错误 - 数据存在时显示旋转器（重新获取时会导致闪烁）
@if (loading()) {
  <app-spinner />
}

// 正确 - 仅在没有数据时显示加载
@if (loading() && !items().length) {
  <app-spinner />
}
```

### 错误处理

```typescript
// 错误 - 错误被吞掉
try {
  await this.service.save();
} catch (e) {
  console.log(e); // 用户毫无察觉！
}

// 正确 - 错误被暴露
try {
  await this.service.save();
} catch (e) {
  console.error("Save failed:", e);
  this.toast.error("Failed to save. Please try again.");
}
```

### 按钮状态

```html
<!-- 错误 - 提交期间按钮未禁用 -->
<button (click)="submit()">Submit</button>

<!-- 正确 - 禁用并显示加载状态 -->
<button (click)="submit()" [disabled]="loading()">
  @if (loading()) {
  <app-spinner size="sm" />
  } Submit
</button>
```

---

## UI 状态检查清单

完成任何 UI 组件前：

### UI 状态

- [ ] 错误状态已处理并显示给用户
- [ ] 仅在无数据时显示加载状态
- [ ] 为集合提供空状态（`@empty` 块）
- [ ] 异步操作期间禁用按钮
- [ ] 适当时在按钮上显示加载指示器

### 数据与变更

- [ ] 所有异步操作都有错误处理
- [ ] 所有用户操作都有反馈（toast/视觉）
- [ ] 乐观更新在失败时回滚

### 无障碍

- [ ] 加载状态已向屏幕阅读器播报
- [ ] 错误消息已关联到表单字段
- [ ] 状态变更后的焦点管理

---

## 与其他技能的集成

- **angular-state-management**：使用 Signal 存储管理状态
- **angular**：应用现代模式（Signals、@defer）
- **testing-patterns**：测试所有 UI 状态

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅当任务明确符合上述描述的范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
