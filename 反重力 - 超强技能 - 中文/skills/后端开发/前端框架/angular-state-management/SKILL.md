---
name: angular-state-management
description: "掌握现代 Angular 状态管理，涵盖 Signals、NgRx 和 RxJS。适用于设置全局状态、管理组件存储、选择状态解决方案或从旧模式迁移。触发词：Angular状态管理、Signals、NgRx、组件存储、全局状态、Signal服务、状态迁移、RxJS状态"
risk: safe
source: self
date_added: "2026-02-27"
---

# Angular 状态管理

现代 Angular 状态管理模式的综合指南，从基于 Signal 的本地状态到全局存储和服务器状态同步。

## 何时使用此技能

- 在 Angular 中设置全局状态管理
- 在 Signals、NgRx 或 Akita 之间进行选择
- 管理组件级存储
- 实现乐观更新
- 调试状态相关问题
- 从旧版状态模式迁移

## 何时不使用此技能

- 任务与 Angular 状态管理无关
- 需要 React 状态管理 → 使用 `react-state-management`

---

## 核心概念

### 状态分类

| 类型 | 描述 | 解决方案 |
| ---------------- | ---------------------------- | --------------------- |
| **本地状态**  | 组件特定，UI 状态 | Signals, `signal()`   |
| **共享状态** | 相关组件之间 | Signal 服务   |
| **全局状态** | 应用范围，复杂 | NgRx, Akita, Elf      |
| **服务器状态** | 远程数据，缓存 | NgRx Query, RxAngular |
| **URL 状态** | 路由参数 | ActivatedRoute        |
| **表单状态** | 输入值，验证 | Reactive Forms        |

### 选择标准

```
小型应用，简单状态 → Signal 服务
中型应用，适度状态 → 组件存储
大型应用，复杂状态 → NgRx Store
大量服务器交互 → NgRx Query + Signal 服务
实时更新 → RxAngular + Signals
```

---

## 快速入门：基于 Signal 的状态

### 模式 1：简单 Signal 服务

```typescript
// services/counter.service.ts
import { Injectable, signal, computed } from "@angular/core";

@Injectable({ providedIn: "root" })
export class CounterService {
  // 私有可写信号
  private _count = signal(0);

  // 公开只读
  readonly count = this._count.asReadonly();
  readonly doubled = computed(() => this._count() * 2);
  readonly isPositive = computed(() => this._count() > 0);

  increment() {
    this._count.update((v) => v + 1);
  }

  decrement() {
    this._count.update((v) => v - 1);
  }

  reset() {
    this._count.set(0);
  }
}

// 组件中使用
@Component({
  template: `
    <p>Count: {{ counter.count() }}</p>
    <p>Doubled: {{ counter.doubled() }}</p>
    <button (click)="counter.increment()">+</button>
  `,
})
export class CounterComponent {
  counter = inject(CounterService);
}
```

### 模式 2：功能 Signal 存储

```typescript
// stores/user.store.ts
import { Injectable, signal, computed, inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { toSignal } from "@angular/core/rxjs-interop";

interface User {
  id: string;
  name: string;
  email: string;
}

interface UserState {
  user: User | null;
  loading: boolean;
  error: string | null;
}

@Injectable({ providedIn: "root" })
export class UserStore {
  private http = inject(HttpClient);

  // 状态信号
  private _user = signal<User | null>(null);
  private _loading = signal(false);
  private _error = signal<string | null>(null);

  // 选择器（只读计算属性）
  readonly user = computed(() => this._user());
  readonly loading = computed(() => this._loading());
  readonly error = computed(() => this._error());
  readonly isAuthenticated = computed(() => this._user() !== null);
  readonly displayName = computed(() => this._user()?.name ?? "Guest");

  // 操作
  async loadUser(id: string) {
    this._loading.set(true);
    this._error.set(null);

    try {
      const user = await fetch(`/api/users/${id}`).then((r) => r.json());
      this._user.set(user);
    } catch (e) {
      this._error.set("Failed to load user");
    } finally {
      this._loading.set(false);
    }
  }

  updateUser(updates: Partial<User>) {
    this._user.update((user) => (user ? { ...user, ...updates } : null));
  }

  logout() {
    this._user.set(null);
    this._error.set(null);
  }
}
```

### 模式 3：SignalStore（NgRx Signals）

```typescript
// stores/products.store.ts
import {
  signalStore,
  withState,
  withMethods,
  withComputed,
  patchState,
} from "@ngrx/signals";
import { inject } from "@angular/core";
import { ProductService } from "./product.service";

interface ProductState {
  products: Product[];
  loading: boolean;
  filter: string;
}

const initialState: ProductState = {
  products: [],
  loading: false,
  filter: "",
};

export const ProductStore = signalStore(
  { providedIn: "root" },

  withState(initialState),

  withComputed((store) => ({
    filteredProducts: computed(() => {
      const filter = store.filter().toLowerCase();
      return store
        .products()
        .filter((p) => p.name.toLowerCase().includes(filter));
    }),
    totalCount: computed(() => store.products().length),
  })),

  withMethods((store, productService = inject(ProductService)) => ({
    async loadProducts() {
      patchState(store, { loading: true });

      try {
        const products = await productService.getAll();
        patchState(store, { products, loading: false });
      } catch {
        patchState(store, { loading: false });
      }
    },

    setFilter(filter: string) {
      patchState(store, { filter });
    },

    addProduct(product: Product) {
      patchState(store, ({ products }) => ({
        products: [...products, product],
      }));
    },
  })),
);

// 使用
@Component({
  template: `
    <input (input)="store.setFilter($event.target.value)" />
    @if (store.loading()) {
      <app-spinner />
    } @else {
      @for (product of store.filteredProducts(); track product.id) {
        <app-product-card [product]="product" />
      }
    }
  `,
})
export class ProductListComponent {
  store = inject(ProductStore);

  ngOnInit() {
    this.store.loadProducts();
  }
}
```

---

## NgRx Store（全局状态）

### 设置

```typescript
// store/app.state.ts
import { ActionReducerMap } from "@ngrx/store";

export interface AppState {
  user: UserState;
  cart: CartState;
}

export const reducers: ActionReducerMap<AppState> = {
  user: userReducer,
  cart: cartReducer,
};

// main.ts
bootstrapApplication(AppComponent, {
  providers: [
    provideStore(reducers),
    provideEffects([UserEffects, CartEffects]),
    provideStoreDevtools({ maxAge: 25 }),
  ],
});
```

### 功能切片模式

```typescript
// store/user/user.actions.ts
import { createActionGroup, props, emptyProps } from "@ngrx/store";

export const UserActions = createActionGroup({
  source: "User",
  events: {
    "Load User": props<{ userId: string }>(),
    "Load User Success": props<{ user: User }>(),
    "Load User Failure": props<{ error: string }>(),
    "Update User": props<{ updates: Partial<User> }>(),
    Logout: emptyProps(),
  },
});
```

```typescript
// store/user/user.reducer.ts
import { createReducer, on } from "@ngrx/store";
import { UserActions } from "./user.actions";

export interface UserState {
  user: User | null;
  loading: boolean;
  error: string | null;
}

const initialState: UserState = {
  user: null,
  loading: false,
  error: null,
};

export const userReducer = createReducer(
  initialState,

  on(UserActions.loadUser, (state) => ({
    ...state,
    loading: true,
    error: null,
  })),

  on(UserActions.loadUserSuccess, (state, { user }) => ({
    ...state,
    user,
    loading: false,
  })),

  on(UserActions.loadUserFailure, (state, { error }) => ({
    ...state,
    loading: false,
    error,
  })),

  on(UserActions.logout, () => initialState),
);
```

```typescript
// store/user/user.selectors.ts
import { createFeatureSelector, createSelector } from "@ngrx/store";
import { UserState } from "./user.reducer";

export const selectUserState = createFeatureSelector<UserState>("user");

export const selectUser = createSelector(
  selectUserState,
  (state) => state.user,
);

export const selectUserLoading = createSelector(
  selectUserState,
  (state) => state.loading,
);

export const selectIsAuthenticated = createSelector(
  selectUser,
  (user) => user !== null,
);
```

```typescript
// store/user/user.effects.ts
import { Injectable, inject } from "@angular/core";
import { Actions, createEffect, ofType } from "@ngrx/effects";
import { switchMap, map, catchError, of } from "rxjs";

@Injectable()
export class UserEffects {
  private actions$ = inject(Actions);
  private userService = inject(UserService);

  loadUser$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UserActions.loadUser),
      switchMap(({ userId }) =>
        this.userService.getUser(userId).pipe(
          map((user) => UserActions.loadUserSuccess({ user })),
          catchError((error) =>
            of(UserActions.loadUserFailure({ error: error.message })),
          ),
        ),
      ),
    ),
  );
}
```

### 组件使用

```typescript
@Component({
  template: `
    @if (loading()) {
      <app-spinner />
    } @else if (user(); as user) {
      <h1>Welcome, {{ user.name }}</h1>
      <button (click)="logout()">Logout</button>
    }
  `,
})
export class HeaderComponent {
  private store = inject(Store);

  user = this.store.selectSignal(selectUser);
  loading = this.store.selectSignal(selectUserLoading);

  logout() {
    this.store.dispatch(UserActions.logout());
  }
}
```

---

## 基于 RxJS 的模式

### 组件存储（本地功能状态）

```typescript
// stores/todo.store.ts
import { Injectable } from "@angular/core";
import { ComponentStore } from "@ngrx/component-store";
import { switchMap, tap, catchError, EMPTY } from "rxjs";

interface TodoState {
  todos: Todo[];
  loading: boolean;
}

@Injectable()
export class TodoStore extends ComponentStore<TodoState> {
  constructor(private todoService: TodoService) {
    super({ todos: [], loading: false });
  }

  // 选择器
  readonly todos$ = this.select((state) => state.todos);
  readonly loading$ = this.select((state) => state.loading);
  readonly completedCount$ = this.select(
    this.todos$,
    (todos) => todos.filter((t) => t.completed).length,
  );

  // 更新器
  readonly addTodo = this.updater((state, todo: Todo) => ({
    ...state,
    todos: [...state.todos, todo],
  }));

  readonly toggleTodo = this.updater((state, id: string) => ({
    ...state,
    todos: state.todos.map((t) =>
      t.id === id ? { ...t, completed: !t.completed } : t,
    ),
  }));

  // 效果
  readonly loadTodos = this.effect<void>((trigger$) =>
    trigger$.pipe(
      tap(() => this.patchState({ loading: true })),
      switchMap(() =>
        this.todoService.getAll().pipe(
          tap({
            next: (todos) => this.patchState({ todos, loading: false }),
            error: () => this.patchState({ loading: false }),
          }),
          catchError(() => EMPTY),
        ),
      ),
    ),
  );
}
```

---

## 使用 Signals 的服务器状态

### HTTP + Signals 模式

```typescript
// services/api.service.ts
import { Injectable, signal, inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { toSignal } from "@angular/core/rxjs-interop";

interface ApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

@Injectable({ providedIn: "root" })
export class ProductApiService {
  private http = inject(HttpClient);

  private _state = signal<ApiState<Product[]>>({
    data: null,
    loading: false,
    error: null,
  });

  readonly products = computed(() => this._state().data ?? []);
  readonly loading = computed(() => this._state().loading);
  readonly error = computed(() => this._state().error);

  async fetchProducts(): Promise<void> {
    this._state.update((s) => ({ ...s, loading: true, error: null }));

    try {
      const data = await firstValueFrom(
        this.http.get<Product[]>("/api/products"),
      );
      this._state.update((s) => ({ ...s, data, loading: false }));
    } catch (e) {
      this._state.update((s) => ({
        ...s,
        loading: false,
        error: "Failed to fetch products",
      }));
    }
  }

  // 乐观更新
  async deleteProduct(id: string): Promise<void> {
    const previousData = this._state().data;

    // 乐观删除
    this._state.update((s) => ({
      ...s,
      data: s.data?.filter((p) => p.id !== id) ?? null,
    }));

    try {
      await firstValueFrom(this.http.delete(`/api/products/${id}`));
    } catch {
      // 错误时回滚
      this._state.update((s) => ({ ...s, data: previousData }));
    }
  }
}
```

---

## 最佳实践

### 推荐做法

| 实践                           | 原因                                |
| ---------------------------------- | ---------------------------------- |
| 使用 Signals 管理本地状态        | 简单、响应式、无需订阅 |
| 使用 `computed()` 处理派生数据  | 自动更新、记忆化             |
| 状态与功能模块放在一起                | 更易维护                 |
| 复杂流程使用 NgRx         | 操作、效果、开发工具         |
| 优先使用 `inject()` 而非构造函数 | 更简洁、适用于工厂        |

### 避免做法

| 反模式                      | 替代方案                                               |
| --------------------------------- | ----------------------------------------------------- |
| 存储派生数据                | 使用 `computed()`                                      |
| 直接修改信号           | 使用 `set()` 或 `update()`                             |
| 过度全局化状态              | 尽可能保持本地                              |
| 混乱地混合 RxJS 和 Signals  | 选择主要方式，用 `toSignal`/`toObservable` 桥接 |
| 在组件中订阅状态 | 在模板中使用 signals                             |

---

## 迁移路径

### 从 BehaviorSubject 迁移到 Signals

```typescript
// 之前：基于 RxJS
@Injectable({ providedIn: "root" })
export class OldUserService {
  private userSubject = new BehaviorSubject<User | null>(null);
  user$ = this.userSubject.asObservable();

  setUser(user: User) {
    this.userSubject.next(user);
  }
}

// 之后：基于 Signal
@Injectable({ providedIn: "root" })
export class UserService {
  private _user = signal<User | null>(null);
  readonly user = this._user.asReadonly();

  setUser(user: User) {
    this._user.set(user);
  }
}
```

### 桥接 Signals 和 RxJS

```typescript
import { toSignal, toObservable } from '@angular/core/rxjs-interop';

// Observable → Signal
@Component({...})
export class ExampleComponent {
  private route = inject(ActivatedRoute);

  // 将 Observable 转换为 Signal
  userId = toSignal(
    this.route.params.pipe(map(p => p['id'])),
    { initialValue: '' }
  );
}

// Signal → Observable
export class DataService {
  private filter = signal('');

  // 将 Signal 转换为 Observable
  filter$ = toObservable(this.filter);

  filteredData$ = this.filter$.pipe(
    debounceTime(300),
    switchMap(filter => this.http.get(`/api/data?q=${filter}`))
  );
}
```

---

## 资源

- [Angular Signals 指南](https://angular.dev/guide/signals)
- [NgRx 文档](https://ngrx.io/)
- [NgRx SignalStore](https://ngrx.io/guide/signals)
- [RxAngular](https://www.rx-angular.io/)

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
