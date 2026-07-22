---
name: angular
description: 现代 Angular（v20+）专家，精通 Signals、Standalone Components、Zoneless 应用、SSR/Hydration 和响应式模式。触发词：Angular、angular、angular-cli、创建项目、组件、服务、指令、管道、signals、linkedSignal、resource、表单、依赖注入、路由、SSR、ARIA、动画、组件样式、Tailwind CSS、测试、单元测试、E2E 测试、guard、resolver、reactive forms、template-driven forms、signal forms。
risk: safe
source: self
date_added: '2026-02-27'
---

# Angular 专家

掌握现代 Angular 开发，包括 Signals、Standalone Components、Zoneless 应用、SSR/Hydration 以及最新的响应式模式。

## 何时使用此技能

- 构建新的 Angular 应用（v20+）
- 实现基于 Signals 的响应式模式
- 创建 Standalone Components 并从 NgModules 迁移
- 配置 Zoneless Angular 应用
- 实现 SSR、预渲染和水合
- 优化 Angular 性能
- 采用现代 Angular 模式和最佳实践

## 何时不使用此技能

- 从 AngularJS（1.x）迁移 → 使用 `angular-migration` 技能
- 处理无法升级的旧版 Angular 应用
- 通用 TypeScript 问题 → 使用 `typescript-expert` 技能

## 指导原则

1. 评估 Angular 版本和项目结构
2. 应用现代模式（Signals、Standalone、Zoneless）
3. 使用正确的类型和响应式实现
4. 通过构建和测试验证

## 安全提示

- 始终在开发环境中测试后再部署到生产环境
- 现有应用采用渐进式迁移（避免大规模重构）
- 过渡期间保持向后兼容性

---

## Angular 版本时间线

| 版本            | 发布时间  | 关键特性                                                 |
| --------------- | --------- | -------------------------------------------------------- |
| **Angular 20**  | 2025 Q2   | Signals 稳定版、Zoneless 稳定版、增量水合                |
| **Angular 21**  | 2025 Q4   | Signals 优先默认、增强 SSR                               |
| **Angular 22**  | 2026 Q2   | Signal Forms、无选择器组件                               |

---

## 1. Signals：新的响应式原语

Signals 是 Angular 的细粒度响应式系统，用于替代基于 zone.js 的变更检测。

### 核心概念

```typescript
import { signal, computed, effect } from "@angular/core";

// 可写 signal
const count = signal(0);

// 读取值
console.log(count()); // 0

// 更新值
count.set(5); // 直接设置
count.update((v) => v + 1); // 函数式更新

// 计算派生 signal
const doubled = computed(() => count() * 2);

// 副作用
effect(() => {
  console.log(`Count changed to: ${count()}`);
});
```

### 基于 Signal 的输入和输出

```typescript
import { Component, input, output, model } from "@angular/core";

@Component({
  selector: "app-user-card",
  standalone: true,
  template: `
    <div class="card">
      <h3>{{ name() }}</h3>
      <span>{{ role() }}</span>
      <button (click)="select.emit(id())">Select</button>
    </div>
  `,
})
export class UserCardComponent {
  // Signal 输入（只读）
  id = input.required<string>();
  name = input.required<string>();
  role = input<string>("User"); // 带默认值

  // 输出
  select = output<string>();

  // 双向绑定（model）
  isSelected = model(false);
}

// 用法：
// <app-user-card [id]="'123'" [name]="'John'" [(isSelected)]="selected" />
```

### Signal 查询（ViewChild/ContentChild）

```typescript
import {
  Component,
  viewChild,
  viewChildren,
  contentChild,
} from "@angular/core";

@Component({
  selector: "app-container",
  standalone: true,
  template: `
    <input #searchInput />
    <app-item *ngFor="let item of items()" />
  `,
})
export class ContainerComponent {
  // 基于 Signal 的查询
  searchInput = viewChild<ElementRef>("searchInput");
  items = viewChildren(ItemComponent);
  projectedContent = contentChild(HeaderDirective);

  focusSearch() {
    this.searchInput()?.nativeElement.focus();
  }
}
```

### 何时使用 Signals vs RxJS

| 使用场景              | Signals         | RxJS                              |
| --------------------- | --------------- | --------------------------------- |
| 本地组件状态          | ✅ 推荐         | 过于复杂                          |
| 派生/计算值           | ✅ `computed()` | `combineLatest` 可用              |
| 副作用                | ✅ `effect()`   | `tap` 操作符                      |
| HTTP 请求             | ❌              | ✅ HttpClient 返回 Observable     |
| 事件流                | ❌              | ✅ `fromEvent`、操作符            |
| 复杂异步流程          | ❌              | ✅ `switchMap`、`mergeMap`        |

---

## 2. Standalone Components

Standalone components 是自包含的，不需要 NgModule 声明。

### 创建 Standalone Components

```typescript
import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import { RouterLink } from "@angular/router";

@Component({
  selector: "app-header",
  standalone: true,
  imports: [CommonModule, RouterLink], // 直接导入
  template: `
    <header>
      <a routerLink="/">Home</a>
      <a routerLink="/about">About</a>
    </header>
  `,
})
export class HeaderComponent {}
```

### 无 NgModule 启动

```typescript
// main.ts
import { bootstrapApplication } from "@angular/platform-browser";
import { provideRouter } from "@angular/router";
import { provideHttpClient } from "@angular/common/http";
import { AppComponent } from "./app/app.component";
import { routes } from "./app/app.routes";

bootstrapApplication(AppComponent, {
  providers: [provideRouter(routes), provideHttpClient()],
});
```

### 懒加载 Standalone Components

```typescript
// app.routes.ts
import { Routes } from "@angular/router";

export const routes: Routes = [
  {
    path: "dashboard",
    loadComponent: () =>
      import("./dashboard/dashboard.component").then(
        (m) => m.DashboardComponent,
      ),
  },
  {
    path: "admin",
    loadChildren: () =>
      import("./admin/admin.routes").then((m) => m.ADMIN_ROUTES),
  },
];
```

---

## 3. Zoneless Angular

Zoneless 应用不使用 zone.js，可提升性能和调试体验。

### 启用 Zoneless 模式

```typescript
// main.ts
import { bootstrapApplication } from "@angular/platform-browser";
import { provideZonelessChangeDetection } from "@angular/core";
import { AppComponent } from "./app/app.component";

bootstrapApplication(AppComponent, {
  providers: [provideZonelessChangeDetection()],
});
```

### Zoneless 组件模式

```typescript
import { Component, signal, ChangeDetectionStrategy } from "@angular/core";

@Component({
  selector: "app-counter",
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div>Count: {{ count() }}</div>
    <button (click)="increment()">+</button>
  `,
})
export class CounterComponent {
  count = signal(0);

  increment() {
    this.count.update((v) => v + 1);
    // 无需 zone.js - Signal 触发变更检测
  }
}
```

### Zoneless 核心优势

- **性能**：无需对异步 API 进行 zone.js 补丁
- **调试**：清晰的堆栈跟踪，无 zone 包装器
- **包体积**：不含 zone.js 更小（节省约 15KB）
- **互操作性**：与 Web Components 和微前端更兼容

---

## 4. 服务端渲染与水合

### 使用 Angular CLI 配置 SSR

```bash
ng add @angular/ssr
```

### 水合配置

```typescript
// app.config.ts
import { ApplicationConfig } from "@angular/core";
import {
  provideClientHydration,
  withEventReplay,
} from "@angular/platform-browser";

export const appConfig: ApplicationConfig = {
  providers: [provideClientHydration(withEventReplay())],
};
```

### 增量水合（v20+）

```typescript
import { Component } from "@angular/core";

@Component({
  selector: "app-page",
  standalone: true,
  template: `
    <app-hero />

    @defer (hydrate on viewport) {
      <app-comments />
    }

    @defer (hydrate on interaction) {
      <app-chat-widget />
    }
  `,
})
export class PageComponent {}
```

### 水合触发器

| 触发器            | 使用场景                             |
| ----------------- | ------------------------------------ |
| `on idle`         | 低优先级，浏览器空闲时水合           |
| `on viewport`     | 元素进入视口时水合                   |
| `on interaction`  | 首次用户交互时水合                   |
| `on hover`        | 用户悬停时水合                       |
| `on timer(ms)`    | 指定延迟后水合                       |

---

## 5. 现代路由模式

### 函数式路由守卫

```typescript
// auth.guard.ts
import { inject } from "@angular/core";
import { Router, CanActivateFn } from "@angular/router";
import { AuthService } from "./auth.service";

export const authGuard: CanActivateFn = (route, state) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  if (auth.isAuthenticated()) {
    return true;
  }

  return router.createUrlTree(["/login"], {
    queryParams: { returnUrl: state.url },
  });
};

// 在路由中使用
export const routes: Routes = [
  {
    path: "dashboard",
    loadComponent: () => import("./dashboard.component"),
    canActivate: [authGuard],
  },
];
```

### 路由级数据解析器

```typescript
import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { UserService } from './user.service';
import { User } from './user.model';

export const userResolver: ResolveFn<User> = (route) => {
  const userService = inject(UserService);
  return userService.getUser(route.paramMap.get('id')!);
};

// 在路由中
{
  path: 'user/:id',
  loadComponent: () => import('./user.component'),
  resolve: { user: userResolver }
}

// 在组件中
export class UserComponent {
  private route = inject(ActivatedRoute);
  user = toSignal(this.route.data.pipe(map(d => d['user'])));
}
```

---

## 6. 依赖注入模式

### 现代 inject() 函数

```typescript
import { Component, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UserService } from './user.service';

@Component({...})
export class UserComponent {
  // 现代 inject() - 无需构造函数
  private http = inject(HttpClient);
  private userService = inject(UserService);

  // 适用于任何注入上下文
  users = toSignal(this.userService.getUsers());
}
```

### 用于配置的注入令牌

```typescript
import { InjectionToken, inject } from "@angular/core";

// 定义令牌
export const API_BASE_URL = new InjectionToken<string>("API_BASE_URL");

// 在配置中提供
bootstrapApplication(AppComponent, {
  providers: [{ provide: API_BASE_URL, useValue: "https://api.example.com" }],
});

// 在服务中注入
@Injectable({ providedIn: "root" })
export class ApiService {
  private baseUrl = inject(API_BASE_URL);

  get(endpoint: string) {
    return this.http.get(`${this.baseUrl}/${endpoint}`);
  }
}
```

---

## 7. 组件组合与复用

### 内容投影（插槽）

```typescript
@Component({
  selector: 'app-card',
  template: `
    <div class="card">
      <div class="header">
        <!-- 按属性选择 -->
        <ng-content select="[card-header]"></ng-content>
      </div>
      <div class="body">
        <!-- 默认插槽 -->
        <ng-content></ng-content>
      </div>
    </div>
  `
})
export class CardComponent {}

// 用法
<app-card>
  <h3 card-header>Title</h3>
  <p>Body content</p>
</app-card>
```

### Host Directives（组合）

```typescript
// 无需继承的可复用行为
@Directive({
  standalone: true,
  selector: '[appTooltip]',
  inputs: ['tooltip'] // Signal 输入别名
})
export class TooltipDirective { ... }

@Component({
  selector: 'app-button',
  standalone: true,
  hostDirectives: [
    {
      directive: TooltipDirective,
      inputs: ['tooltip: title'] // 映射输入
    }
  ],
  template: `<ng-content />`
})
export class ButtonComponent {}
```

---

## 8. 状态管理模式

### 基于 Signal 的状态服务

```typescript
import { Injectable, signal, computed } from "@angular/core";

interface AppState {
  user: User | null;
  theme: "light" | "dark";
  notifications: Notification[];
}

@Injectable({ providedIn: "root" })
export class StateService {
  // 私有可写 signals
  private _user = signal<User | null>(null);
  private _theme = signal<"light" | "dark">("light");
  private _notifications = signal<Notification[]>([]);

  // 公开只读计算属性
  readonly user = computed(() => this._user());
  readonly theme = computed(() => this._theme());
  readonly notifications = computed(() => this._notifications());
  readonly unreadCount = computed(
    () => this._notifications().filter((n) => !n.read).length,
  );

  // 操作方法
  setUser(user: User | null) {
    this._user.set(user);
  }

  toggleTheme() {
    this._theme.update((t) => (t === "light" ? "dark" : "light"));
  }

  addNotification(notification: Notification) {
    this._notifications.update((n) => [...n, notification]);
  }
}
```

### 使用 Signals 的组件存储模式

```typescript
import { Injectable, signal, computed, inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { toSignal } from "@angular/core/rxjs-interop";

@Injectable()
export class ProductStore {
  private http = inject(HttpClient);

  // 状态
  private _products = signal<Product[]>([]);
  private _loading = signal(false);
  private _filter = signal("");

  // 选择器
  readonly products = computed(() => this._products());
  readonly loading = computed(() => this._loading());
  readonly filteredProducts = computed(() => {
    const filter = this._filter().toLowerCase();
    return this._products().filter((p) =>
      p.name.toLowerCase().includes(filter),
    );
  });

  // 操作方法
  loadProducts() {
    this._loading.set(true);
    this.http.get<Product[]>("/api/products").subscribe({
      next: (products) => {
        this._products.set(products);
        this._loading.set(false);
      },
      error: () => this._loading.set(false),
    });
  }

  setFilter(filter: string) {
    this._filter.set(filter);
  }
}
```

---

## 9. 使用 Signals 的表单（v22+ 即将推出）

### 当前响应式表单

```typescript
import { Component, inject } from "@angular/core";
import { FormBuilder, Validators, ReactiveFormsModule } from "@angular/forms";

@Component({
  selector: "app-user-form",
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <input formControlName="name" placeholder="Name" />
      <input formControlName="email" type="email" placeholder="Email" />
      <button [disabled]="form.invalid">Submit</button>
    </form>
  `,
})
export class UserFormComponent {
  private fb = inject(FormBuilder);

  form = this.fb.group({
    name: ["", Validators.required],
    email: ["", [Validators.required, Validators.email]],
  });

  onSubmit() {
    if (this.form.valid) {
      console.log(this.form.value);
    }
  }
}
```

### Signal 感知表单模式（预览）

```typescript
// 未来 Signal Forms API（实验性）
import { Component, signal } from '@angular/core';

@Component({...})
export class SignalFormComponent {
  name = signal('');
  email = signal('');

  // 计算验证
  isValid = computed(() =>
    this.name().length > 0 &&
    this.email().includes('@')
  );

  submit() {
    if (this.isValid()) {
      console.log({ name: this.name(), email: this.email() });
    }
  }
}
```

---

## 10. 性能优化

### 变更检测策略

```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  // 仅在以下情况检查：
  // 1. 输入 signal/引用变化
  // 2. 事件处理器执行
  // 3. Async pipe 发射
  // 4. Signal 值变化
})
```

### 用于懒加载的 Defer 块

```typescript
@Component({
  template: `
    <!-- 立即加载 -->
    <app-header />

    <!-- 可见时懒加载 -->
    @defer (on viewport) {
      <app-heavy-chart />
    } @placeholder {
      <div class="skeleton" />
    } @loading (minimum 200ms) {
      <app-spinner />
    } @error {
      <p>Failed to load chart</p>
    }
  `
})
```

### NgOptimizedImage

```typescript
import { NgOptimizedImage } from '@angular/common';

@Component({
  imports: [NgOptimizedImage],
  template: `
    <img
      ngSrc="hero.jpg"
      width="800"
      height="600"
      priority
    />

    <img
      ngSrc="thumbnail.jpg"
      width="200"
      height="150"
      loading="lazy"
      placeholder="blur"
    />
  `
})
```

---

## 11. 测试现代 Angular

### 测试 Signal 组件

```typescript
import { ComponentFixture, TestBed } from "@angular/core/testing";
import { CounterComponent } from "./counter.component";

describe("CounterComponent", () => {
  let component: CounterComponent;
  let fixture: ComponentFixture<CounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CounterComponent], // Standalone 导入
    }).compileComponents();

    fixture = TestBed.createComponent(CounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should increment count", () => {
    expect(component.count()).toBe(0);

    component.increment();

    expect(component.count()).toBe(1);
  });

  it("should update DOM on signal change", () => {
    component.count.set(5);
    fixture.detectChanges();

    const el = fixture.nativeElement.querySelector(".count");
    expect(el.textContent).toContain("5");
  });
});
```

### 使用 Signal Inputs 测试

```typescript
import { ComponentFixture, TestBed } from "@angular/core/testing";
import { ComponentRef } from "@angular/core";
import { UserCardComponent } from "./user-card.component";

describe("UserCardComponent", () => {
  let fixture: ComponentFixture<UserCardComponent>;
  let componentRef: ComponentRef<UserCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserCardComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(UserCardComponent);
    componentRef = fixture.componentRef;

    // 通过 setInput 设置 signal 输入
    componentRef.setInput("id", "123");
    componentRef.setInput("name", "John Doe");

    fixture.detectChanges();
  });

  it("should display user name", () => {
    const el = fixture.nativeElement.querySelector("h3");
    expect(el.textContent).toContain("John Doe");
  });
});
```

---

## 最佳实践总结

| 模式                 | ✅ 推荐                        | ❌ 避免                         |
| -------------------- | ------------------------------ | ------------------------------- |
| **状态**             | 使用 Signals 管理本地状态      | 对简单状态过度使用 RxJS         |
| **组件**             | Standalone 配合直接导入        | 臃肿的 SharedModules            |
| **变更检测**         | OnPush + Signals               | 到处使用默认 CD                 |
| **懒加载**           | `@defer` 和 `loadComponent`    | 急切加载所有内容                |
| **DI**               | `inject()` 函数                | 构造函数注入（冗长）            |
| **输入**             | `input()` signal 函数          | `@Input()` 装饰器（旧版）       |
| **Zoneless**         | 新项目启用                     | 未经测试强制用于旧项目          |

---

## 资源

- [Angular.dev 文档](https://angular.dev)
- [Angular Signals 指南](https://angular.dev/guide/signals)
- [Angular SSR 指南](https://angular.dev/guide/ssr)
- [Angular 更新指南](https://angular.dev/update-guide)
- [Angular 博客](https://blog.angular.dev)

---

## 常见问题排查

| 问题                          | 解决方案                                            |
| ----------------------------- | --------------------------------------------------- |
| Signal 未更新 UI              | 确保使用 `OnPush` + 将 signal 作为函数调用 `count()` |
| 水合不匹配                    | 检查服务端/客户端内容一致性                         |
| 循环依赖                      | 使用带 `forwardRef` 的 `inject()`                   |
| Zoneless 未检测到变更         | 通过 signal 更新触发，而非直接修改                  |
| SSR fetch 失败                | 使用 `TransferState` 或 `withFetch()`               |

## 限制

- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
