---
name: angular-best-practices
description: "Angular 性能优化与最佳实践指南。用于编写、审查或重构 Angular 代码以获得最佳性能、包体积和渲染效率。触发词：Angular性能、Angular最佳实践、Angular优化、OnPush、Signals、Zoneless、懒加载、变更检测、SSR、水合、包优化"
risk: safe
source: self
date_added: "2026-02-27"
---

# Angular 最佳实践

Angular 应用的全面性能优化指南。包含消除性能瓶颈、优化包体积和提升渲染效率的优先级规则。

## 使用时机

在以下情况下参考这些指南：

- 编写新的 Angular 组件或页面
- 实现数据获取模式
- 审查代码性能问题
- 重构现有 Angular 代码
- 优化包体积或加载时间
- 配置 SSR/水合

---

## 按优先级分类的规则

| 优先级 | 类别 | 影响 | 重点 |
| -------- | --------------------- | ---------- | ------------------------------- |
| 1 | 变更检测 | 关键 | Signals、OnPush、Zoneless |
| 2 | 异步瀑布流 | 关键 | RxJS 模式、SSR 预加载 |
| 3 | 包优化 | 关键 | 懒加载、摇树优化 |
| 4 | 渲染性能 | 高 | @defer、trackBy、虚拟化 |
| 5 | 服务端渲染 | 高 | 水合、预渲染 |
| 6 | 模板优化 | 中 | 控制流、管道 |
| 7 | 状态管理 | 中 | Signal 模式、选择器 |
| 8 | 内存管理 | 中低 | 清理、订阅 |

---

## 1. 变更检测（关键）

### 使用 OnPush 变更检测策略

```typescript
// 正确 - OnPush 配合 Signals
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `<div>{{ count() }}</div>`,
})
export class CounterComponent {
  count = signal(0);
}

// 错误 - 默认变更检测
@Component({
  template: `<div>{{ count }}</div>`, // 每个周期都会检查
})
export class CounterComponent {
  count = 0;
}
```

### 优先使用 Signals 而非可变属性

```typescript
// 正确 - Signals 触发精确更新
@Component({
  template: `
    <h1>{{ title() }}</h1>
    <p>Count: {{ count() }}</p>
  `,
})
export class DashboardComponent {
  title = signal("Dashboard");
  count = signal(0);
}

// 错误 - 可变属性需要 zone.js 检查
@Component({
  template: `
    <h1>{{ title }}</h1>
    <p>Count: {{ count }}</p>
  `,
})
export class DashboardComponent {
  title = "Dashboard";
  count = 0;
}
```

### 为新项目启用 Zoneless

```typescript
// main.ts - Zoneless Angular (v20+)
bootstrapApplication(AppComponent, {
  providers: [provideZonelessChangeDetection()],
});
```

**优势：**

- 异步 API 上无 zone.js 补丁
- 更小的包体积（节省约 15KB）
- 干净的调试堆栈跟踪
- 更好的微前端兼容性

---

## 2. 异步操作与瀑布流（关键）

### 消除顺序数据获取

```typescript
// 错误 - 嵌套订阅创建瀑布流
this.route.params.subscribe((params) => {
  // 1. 等待参数
  this.userService.getUser(params.id).subscribe((user) => {
    // 2. 等待用户
    this.postsService.getPosts(user.id).subscribe((posts) => {
      // 3. 等待帖子
    });
  });
});

// 正确 - 使用 forkJoin 并行执行
forkJoin({
  user: this.userService.getUser(id),
  posts: this.postsService.getPosts(id),
}).subscribe((data) => {
  // 并行获取
});

// 正确 - 使用 switchMap 扁平化依赖调用
this.route.params
  .pipe(
    map((p) => p.id),
    switchMap((id) => this.userService.getUser(id)),
  )
  .subscribe();
```

### 避免 SSR 中的客户端瀑布流

```typescript
// 正确 - 对关键数据使用解析器或阻塞水合
export const route: Route = {
  path: "profile/:id",
  resolve: { data: profileResolver }, // 在服务端导航前获取
  component: ProfileComponent,
};

// 错误 - 组件在初始化时获取数据
class ProfileComponent implements OnInit {
  ngOnInit() {
    // 仅在 JS 加载和组件渲染后才开始
    this.http.get("/api/profile").subscribe();
  }
}
```

---

## 3. 包优化（关键）

### 懒加载路由

```typescript
// 正确 - 懒加载功能路由
export const routes: Routes = [
  {
    path: "admin",
    loadChildren: () =>
      import("./admin/admin.routes").then((m) => m.ADMIN_ROUTES),
  },
  {
    path: "dashboard",
    loadComponent: () =>
      import("./dashboard/dashboard.component").then(
        (m) => m.DashboardComponent,
      ),
  },
];

// 错误 - 急切加载所有内容
import { AdminModule } from "./admin/admin.module";
export const routes: Routes = [
  { path: "admin", component: AdminComponent }, // 在主包中
];
```

### 使用 @defer 延迟加载重型组件

```html
<!-- 正确 - 重型组件按需加载 -->
@defer (on viewport) {
<app-analytics-chart [data]="data()" />
} @placeholder {
<div class="chart-skeleton"></div>
}

<!-- 错误 - 重型组件在初始包中 -->
<app-analytics-chart [data]="data()" />
```

### 避免桶文件重导出

```typescript
// 错误 - 导入整个桶文件，破坏摇树优化
import { Button, Modal, Table } from "@shared/components";

// 正确 - 直接导入
import { Button } from "@shared/components/button/button.component";
import { Modal } from "@shared/components/modal/modal.component";
```

### 动态导入第三方库

```typescript
// 正确 - 按需加载重型库
async loadChart() {
  const { Chart } = await import('chart.js');
  this.chart = new Chart(this.canvas, config);
}

// 错误 - 将 Chart.js 打包到主块中
import { Chart } from 'chart.js';
```

---

## 4. 渲染性能（高）

### 始终在 @for 中使用 trackBy

```html
<!-- 正确 - 高效的 DOM 更新 -->
@for (item of items(); track item.id) {
<app-item-card [item]="item" />
}

<!-- 错误 - 任何更改都会重新渲染整个列表 -->
@for (item of items(); track $index) {
<app-item-card [item]="item" />
}
```

### 对大型列表使用虚拟滚动

```typescript
import { CdkVirtualScrollViewport, CdkFixedSizeVirtualScroll } from '@angular/cdk/scrolling';

@Component({
  imports: [CdkVirtualScrollViewport, CdkFixedSizeVirtualScroll],
  template: `
    <cdk-virtual-scroll-viewport itemSize="50" class="viewport">
      <div *cdkVirtualFor="let item of items" class="item">
        {{ item.name }}
      </div>
    </cdk-virtual-scroll-viewport>
  `
})
```

### 优先使用纯管道而非方法

```typescript
// 正确 - 纯管道，有记忆化
@Pipe({ name: 'filterActive', standalone: true, pure: true })
export class FilterActivePipe implements PipeTransform {
  transform(items: Item[]): Item[] {
    return items.filter(i => i.active);
  }
}

// 模板
@for (item of items() | filterActive; track item.id) { ... }

// 错误 - 方法在每次变更检测时都会调用
@for (item of getActiveItems(); track item.id) { ... }
```

### 使用 computed() 处理派生数据

```typescript
// 正确 - 计算属性，缓存直到依赖变化
export class ProductStore {
  products = signal<Product[]>([]);
  filter = signal('');

  filteredProducts = computed(() => {
    const f = this.filter().toLowerCase();
    return this.products().filter(p =>
      p.name.toLowerCase().includes(f)
    );
  });
}

// 错误 - 每次访问都重新计算
get filteredProducts() {
  return this.products.filter(p =>
    p.name.toLowerCase().includes(this.filter)
  );
}
```

---

## 5. 服务端渲染（高）

### 配置增量水合

```typescript
// app.config.ts
import {
  provideClientHydration,
  withIncrementalHydration,
} from "@angular/platform-browser";

export const appConfig: ApplicationConfig = {
  providers: [
    provideClientHydration(withIncrementalHydration(), withEventReplay()),
  ],
};
```

### 延迟非关键内容

```html
<!-- 关键的首屏内容 -->
<app-header />
<app-hero />

<!-- 使用水合触发器延迟首屏以下内容 -->
@defer (hydrate on viewport) {
<app-product-grid />
} @defer (hydrate on interaction) {
<app-chat-widget />
}
```

### 使用 TransferState 处理 SSR 数据

```typescript
@Injectable({ providedIn: "root" })
export class DataService {
  private http = inject(HttpClient);
  private transferState = inject(TransferState);
  private platformId = inject(PLATFORM_ID);

  getData(key: string): Observable<Data> {
    const stateKey = makeStateKey<Data>(key);

    if (isPlatformBrowser(this.platformId)) {
      const cached = this.transferState.get(stateKey, null);
      if (cached) {
        this.transferState.remove(stateKey);
        return of(cached);
      }
    }

    return this.http.get<Data>(`/api/${key}`).pipe(
      tap((data) => {
        if (isPlatformServer(this.platformId)) {
          this.transferState.set(stateKey, data);
        }
      }),
    );
  }
}
```

---

## 6. 模板优化（中）

### 使用新的控制流语法

```html
<!-- 正确 - 新控制流（更快、包更小） -->
@if (user()) {
<span>{{ user()!.name }}</span>
} @else {
<span>Guest</span>
} @for (item of items(); track item.id) {
<app-item [item]="item" />
} @empty {
<p>No items</p>
}

<!-- 错误 - 旧版结构指令 -->
<span *ngIf="user; else guest">{{ user.name }}</span>
<ng-template #guest><span>Guest</span></ng-template>
```

### 避免复杂的模板表达式

```typescript
// 正确 - 在组件中预计算
class Component {
  items = signal<Item[]>([]);
  sortedItems = computed(() =>
    [...this.items()].sort((a, b) => a.name.localeCompare(b.name))
  );
}

// 模板
@for (item of sortedItems(); track item.id) { ... }

// 错误 - 每次渲染都在模板中排序
@for (item of items() | sort:'name'; track item.id) { ... }
```

---

## 7. 状态管理（中）

### 使用选择器防止不必要的重渲染

```typescript
// 正确 - 选择性订阅
@Component({
  template: `<span>{{ userName() }}</span>`,
})
class HeaderComponent {
  private store = inject(Store);
  // 仅在 userName 变化时重渲染
  userName = this.store.selectSignal(selectUserName);
}

// 错误 - 订阅整个状态
@Component({
  template: `<span>{{ state().user.name }}</span>`,
})
class HeaderComponent {
  private store = inject(Store);
  // 任何状态变化都会重渲染
  state = toSignal(this.store);
}
```

### 将状态与功能模块放在一起

```typescript
// 正确 - 功能范围的状态存储
@Injectable() // 非 providedIn: 'root'
export class ProductStore { ... }

@Component({
  providers: [ProductStore], // 作用域限定在组件树
})
export class ProductPageComponent {
  store = inject(ProductStore);
}

// 错误 - 所有内容都在全局存储中
@Injectable({ providedIn: 'root' })
export class GlobalStore {
  // 包含所有应用状态 - 难以摇树优化
}
```

---

## 8. 内存管理（中低）

### 使用 takeUntilDestroyed 管理订阅

```typescript
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

@Component({...})
export class DataComponent {
  private destroyRef = inject(DestroyRef);

  constructor() {
    this.data$.pipe(
      takeUntilDestroyed(this.destroyRef)
    ).subscribe(data => this.process(data));
  }
}

// 错误 - 手动订阅管理
export class DataComponent implements OnDestroy {
  private subscription!: Subscription;

  ngOnInit() {
    this.subscription = this.data$.subscribe(...);
  }

  ngOnDestroy() {
    this.subscription.unsubscribe(); // 容易忘记
  }
}
```

### 优先使用 Signals 而非订阅

```typescript
// 正确 - 无需订阅
@Component({
  template: `<div>{{ data().name }}</div>`,
})
export class Component {
  data = toSignal(this.service.data$, { initialValue: null });
}

// 错误 - 手动订阅
@Component({
  template: `<div>{{ data?.name }}</div>`,
})
export class Component implements OnInit, OnDestroy {
  data: Data | null = null;
  private sub!: Subscription;

  ngOnInit() {
    this.sub = this.service.data$.subscribe((d) => (this.data = d));
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }
}
```

---

## 快速参考清单

### 新组件

- [ ] `changeDetection: ChangeDetectionStrategy.OnPush`
- [ ] `standalone: true`
- [ ] 使用 Signals 管理状态（`signal()`、`input()`、`output()`）
- [ ] 使用 `inject()` 注入依赖
- [ ] `@for` 使用 `track` 表达式

### 性能审查

- [ ] 模板中没有方法调用（使用管道或 computed）
- [ ] 大型列表已虚拟化
- [ ] 重型组件已延迟加载
- [ ] 路由已懒加载
- [ ] 第三方库已动态导入

### SSR 检查

- [ ] 已配置水合
- [ ] 关键内容优先渲染
- [ ] 非关键内容使用 `@defer (hydrate on ...)`
- [ ] 服务端获取的数据使用 TransferState

---

## 资源

- [Angular Performance Guide](https://angular.dev/best-practices/performance)
- [Zoneless Angular](https://angular.dev/guide/experimental/zoneless)
- [Angular SSR Guide](https://angular.dev/guide/ssr)
- [Change Detection Deep Dive](https://angular.dev/guide/change-detection)

## 使用时机
此技能适用于执行概述中描述的工作流程或操作。

## 局限性
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
