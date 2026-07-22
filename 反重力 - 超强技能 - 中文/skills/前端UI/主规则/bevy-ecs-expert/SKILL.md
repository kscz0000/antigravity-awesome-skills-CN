---
name: bevy-ecs-expert
description: "精通 Bevy 的实体组件系统（ECS），涵盖 System、Query、Resource 和并行调度。当用户要求'Bevy ECS开发'、'Bevy实体组件系统'、'Rust游戏ECS'、'Bevy系统调度'或'ECS架构设计'时使用。"
risk: safe
source: community
date_added: "2026-02-27"
---

# Bevy ECS Expert

## 概述

使用 Bevy 面向数据的 ECS 架构构建高性能游戏逻辑的指南。学习如何组织系统、优化查询、管理资源，以及利用并行执行。

## 何时使用此技能

- 使用 Rust 和 Bevy 引擎开发游戏时
- 设计需要并行运行的游戏系统时
- 通过减少缓存未命中来优化游戏性能时
- 将面向对象逻辑重构为面向数据的 ECS 模式时

## 分步指南

### 1. 定义组件

用简单的结构体表示数据，派生 `Component` 和 `Reflect`。

```rust
#[derive(Component, Reflect, Default)]
#[reflect(Component)]
struct Velocity {
    x: f32,
    y: f32,
}

#[derive(Component)]
struct Player;
```

### 2. 编写系统

系统就是查询组件的普通 Rust 函数。

```rust
fn movement_system(
    time: Res<Time>,
    mut query: Query<(&mut Transform, &Velocity), With<Player>>,
) {
    for (mut transform, velocity) in &mut query {
        transform.translation.x += velocity.x * time.delta_seconds();
        transform.translation.y += velocity.y * time.delta_seconds();
    }
}
```

### 3. 管理资源

用 `Resource` 存储全局数据（分数、游戏状态等）。

```rust
#[derive(Resource)]
struct GameState {
    score: u32,
}

fn score_system(mut game_state: ResMut<GameState>) {
    game_state.score += 10;
}
```

### 4. 调度系统

将系统添加到 `App` 构建器中，按需定义执行顺序。

```rust
fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .init_resource::<GameState>()
        .add_systems(Update, (movement_system, score_system).chain())
        .run();
}
```

## 示例

### 示例 1：使用 Require 生成实体

```rust
use bevy::prelude::*;

#[derive(Component, Reflect, Default)]
#[require(Velocity, Sprite)]
struct Player;

#[derive(Component, Default)]
struct Velocity {
    x: f32,
    y: f32,
}

fn setup(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn((
        Player,
        Velocity { x: 10.0, y: 0.0 },
        Sprite::from_image(asset_server.load("player.png")), 
    ));
}
```

### 示例 2：查询过滤器

用 `With` 和 `Without` 高效过滤实体。

```rust
fn enemy_behavior(
    query: Query<&Transform, (With<Enemy>, Without<Dead>)>,
) {
    for transform in &query {
        // Only active enemies processed here
    }
}
```

## 最佳实践

- ✅ **推荐：** 使用 `Query` 过滤器（`With`、`Without`、`Changed`）减少迭代数量。
- ✅ **推荐：** 只读访问时优先用 `Res` 而非 `ResMut`，以允许并行执行。
- ✅ **推荐：** 使用 `Bundle` 原子化生成复杂实体。
- ❌ **避免：** 在组件中存放重逻辑；组件应保持为纯数据。
- ❌ **避免：** 在组件中使用 `RefCell` 或内部可变性；让 ECS 处理借用。

## 故障排除

**问题：** 系统因 "Conflict" 错误而 panic。
**解决：** 你可能在两个并行运行的系统中尝试可变访问同一组件。使用 `.chain()` 为它们排序，或拆分逻辑。

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出内容不能替代针对具体环境的验证、测试或专家评审。
- 若缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
