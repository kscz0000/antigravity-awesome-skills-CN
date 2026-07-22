---
name: angular-migration
description: "AngularJS 到 Angular 迁移专家，包括混合应用、组件转换、依赖注入变更和路由迁移。触发词：Angular迁移、AngularJS升级、ngUpgrade、混合应用、组件迁移、Angular现代化"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Angular 迁移

AngularJS 到 Angular 迁移专家，包括混合应用、组件转换、依赖注入变更和路由迁移。

## 使用此技能的场景

- 将 AngularJS (1.x) 应用迁移到 Angular (2+)
- 运行 AngularJS/Angular 混合应用
- 将指令转换为组件
- 现代化依赖注入
- 迁移路由系统
- 更新到最新 Angular 版本
- 实施 Angular 最佳实践

## 不使用此技能的场景

- 不是从 AngularJS 迁移到 Angular
- 应用已在使用现代 Angular 版本
- 只需要小型 UI 修复而不涉及框架变更

## 指导步骤

1. 评估 AngularJS 代码库、依赖项和迁移风险。
2. 选择迁移策略（混合 vs 重写）并定义里程碑。
3. 设置 ngUpgrade，迁移模块、组件和路由。
4. 通过测试验证并规划安全切换。

## 安全注意事项

- 避免没有回滚和预发布验证的一次性大规模切换。
- 在增量迁移期间保持混合兼容性测试。

## 迁移策略

### 1. 大爆炸式（完全重写）
- 用 Angular 重写整个应用
- 并行开发
- 一次性切换
- **最适合：** 小型应用、全新项目

### 2. 增量式（混合方法）
- AngularJS 和 Angular 并行运行
- 逐个功能迁移
- 使用 ngUpgrade 实现互操作
- **最适合：** 大型应用、持续交付

### 3. 垂直切片
- 完整迁移一个功能
- 新功能用 Angular，旧功能维护 AngularJS
- 逐步替换
- **最适合：** 中型应用、功能独立

## 混合应用设置

```typescript
// main.ts - 启动混合应用
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { UpgradeModule } from '@angular/upgrade/static';
import { AppModule } from './app/app.module';

platformBrowserDynamic()
  .bootstrapModule(AppModule)
  .then(platformRef => {
    const upgrade = platformRef.injector.get(UpgradeModule);
    // 启动 AngularJS
    upgrade.bootstrap(document.body, ['myAngularJSApp'], { strictDi: true });
  });
```

```typescript
// app.module.ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { UpgradeModule } from '@angular/upgrade/static';

@NgModule({
  imports: [
    BrowserModule,
    UpgradeModule
  ]
})
export class AppModule {
  constructor(private upgrade: UpgradeModule) {}

  ngDoBootstrap() {
    // 在 main.ts 中手动启动
  }
}
```

## 组件迁移

### AngularJS 控制器 → Angular 组件
```javascript
// 迁移前：AngularJS 控制器
angular.module('myApp').controller('UserController', function($scope, UserService) {
  $scope.user = {};

  $scope.loadUser = function(id) {
    UserService.getUser(id).then(function(user) {
      $scope.user = user;
    });
  };

  $scope.saveUser = function() {
    UserService.saveUser($scope.user);
  };
});
```

```typescript
// 迁移后：Angular 组件
import { Component, OnInit } from '@angular/core';
import { UserService } from './user.service';

@Component({
  selector: 'app-user',
  template: `
    <div>
      <h2>{{ user.name }}</h2>
      <button (click)="saveUser()">Save</button>
    </div>
  `
})
export class UserComponent implements OnInit {
  user: any = {};

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.loadUser(1);
  }

  loadUser(id: number) {
    this.userService.getUser(id).subscribe(user => {
      this.user = user;
    });
  }

  saveUser() {
    this.userService.saveUser(this.user);
  }
}
```

### AngularJS 指令 → Angular 组件
```javascript
// 迁移前：AngularJS 指令
angular.module('myApp').directive('userCard', function() {
  return {
    restrict: 'E',
    scope: {
      user: '=',
      onDelete: '&'
    },
    template: `
      <div class="card">
        <h3>{{ user.name }}</h3>
        <button ng-click="onDelete()">Delete</button>
      </div>
    `
  };
});
```

```typescript
// 迁移后：Angular 组件
import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-user-card',
  template: `
    <div class="card">
      <h3>{{ user.name }}</h3>
      <button (click)="delete.emit()">Delete</button>
    </div>
  `
})
export class UserCardComponent {
  @Input() user: any;
  @Output() delete = new EventEmitter<void>();
}

// 用法：<app-user-card [user]="user" (delete)="handleDelete()"></app-user-card>
```

## 服务迁移

```javascript
// 迁移前：AngularJS 服务
angular.module('myApp').factory('UserService', function($http) {
  return {
    getUser: function(id) {
      return $http.get('/api/users/' + id);
    },
    saveUser: function(user) {
      return $http.post('/api/users', user);
    }
  };
});
```

```typescript
// 迁移后：Angular 服务
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) {}

  getUser(id: number): Observable<any> {
    return this.http.get(`/api/users/${id}`);
  }

  saveUser(user: any): Observable<any> {
    return this.http.post('/api/users', user);
  }
}
```

## 依赖注入变更

### 降级 Angular → AngularJS
```typescript
// Angular 服务
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class NewService {
  getData() {
    return 'data from Angular';
  }
}

// 使其对 AngularJS 可用
import { downgradeInjectable } from '@angular/upgrade/static';

angular.module('myApp')
  .factory('newService', downgradeInjectable(NewService));

// 在 AngularJS 中使用
angular.module('myApp').controller('OldController', function(newService) {
  console.log(newService.getData());
});
```

### 升级 AngularJS → Angular
```typescript
// AngularJS 服务
angular.module('myApp').factory('oldService', function() {
  return {
    getData: function() {
      return 'data from AngularJS';
    }
  };
});

// 使其对 Angular 可用
import { InjectionToken } from '@angular/core';

export const OLD_SERVICE = new InjectionToken<any>('oldService');

@NgModule({
  providers: [
    {
      provide: OLD_SERVICE,
      useFactory: (i: any) => i.get('oldService'),
      deps: ['$injector']
    }
  ]
})

// 在 Angular 中使用
@Component({...})
export class NewComponent {
  constructor(@Inject(OLD_SERVICE) private oldService: any) {
    console.log(this.oldService.getData());
  }
}
```

## 路由迁移

```javascript
// 迁移前：AngularJS 路由
angular.module('myApp').config(function($routeProvider) {
  $routeProvider
    .when('/users', {
      template: '<user-list></user-list>'
    })
    .when('/users/:id', {
      template: '<user-detail></user-detail>'
    });
});
```

```typescript
// 迁移后：Angular 路由
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: 'users', component: UserListComponent },
  { path: 'users/:id', component: UserDetailComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
```

## 表单迁移

```html
<!-- 迁移前：AngularJS -->
<form name="userForm" ng-submit="saveUser()">
  <input type="text" ng-model="user.name" required>
  <input type="email" ng-model="user.email" required>
  <button ng-disabled="userForm.$invalid">Save</button>
</form>
```

```typescript
// 迁移后：Angular（模板驱动表单）
@Component({
  template: `
    <form #userForm="ngForm" (ngSubmit)="saveUser()">
      <input type="text" [(ngModel)]="user.name" name="name" required>
      <input type="email" [(ngModel)]="user.email" name="email" required>
      <button [disabled]="userForm.invalid">Save</button>
    </form>
  `
})

// 或响应式表单（推荐）
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  template: `
    <form [formGroup]="userForm" (ngSubmit)="saveUser()">
      <input formControlName="name">
      <input formControlName="email">
      <button [disabled]="userForm.invalid">Save</button>
    </form>
  `
})
export class UserFormComponent {
  userForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.userForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]]
    });
  }

  saveUser() {
    console.log(this.userForm.value);
  }
}
```

## 迁移时间线

```
阶段 1：设置（1-2 周）
- 安装 Angular CLI
- 设置混合应用
- 配置构建工具
- 设置测试

阶段 2：基础设施（2-4 周）
- 迁移服务
- 迁移工具函数
- 设置路由
- 迁移共享组件

阶段 3：功能迁移（时间不定）
- 逐个功能迁移
- 充分测试
- 增量部署

阶段 4：清理（1-2 周）
- 移除 AngularJS 代码
- 移除 ngUpgrade
- 优化打包
- 最终测试
```

## 资源

- **references/hybrid-mode.md**: 混合应用模式
- **references/component-migration.md**: 组件转换指南
- **references/dependency-injection.md**: DI 迁移策略
- **references/routing.md**: 路由迁移
- **assets/hybrid-bootstrap.ts**: 混合应用模板
- **assets/migration-timeline.md**: 项目规划
- **scripts/analyze-angular-app.sh**: 应用分析脚本

## 最佳实践

1. **从服务开始**：优先迁移服务（更容易）
2. **增量方法**：逐个功能迁移
3. **持续测试**：每一步都要测试
4. **使用 TypeScript**：尽早迁移到 TypeScript
5. **遵循风格指南**：从第一天起遵循 Angular 风格指南
6. **后期优化**：先让它工作，再优化
7. **文档记录**：保留迁移笔记

## 常见陷阱

- 混合应用设置不正确
- 先迁移 UI 后迁移逻辑
- 忽略变更检测差异
- 未正确处理作用域
- 混用模式（AngularJS + Angular）
- 测试不充分

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 输出内容不能替代环境特定的验证、测试或专家评审。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
