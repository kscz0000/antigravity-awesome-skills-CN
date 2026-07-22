---
name: godot-4-migration
description: "Godot 3.x 项目迁移至 Godot 4（GDScript 2.0）的专业指南，涵盖语法变更、Tween 系统和 export 注解。当用户要求'迁移 Godot 3 到 4'、'Godot 4 升级'、'GDScript 2.0 语法'时使用。"
risk: safe
source: community
date_added: "2026-02-27"
---

# Godot 4 迁移指南

## 概述

面向从 Godot 3.x 迁移至 Godot 4 的开发者的关键指南。本技能聚焦于 GDScript 2.0 的重大语法变更、全新的 `Tween` 系统以及 `export` 注解更新。

## 何时使用本技能

- 将 Godot 3 项目移植到 Godot 4 时
- 升级后遇到语法错误时
- 替换已弃用节点（如 `Tween` 节点改用 `create_tween`）时
- 将 `export` 变量更新为 `@export` 注解时

## 关键变更

### 1. 注解（`@`）

Godot 4 使用 `@` 作为修饰行为的关键字前缀。
- `export var x` -> `@export var x`
- `onready var y` -> `@onready var y`
- `tool` -> `@tool`（置于文件顶部）

### 2. Setter 与 Getter

属性现在采用内联方式定义 setter/getter。

**Godot 3:**
```gdscript
var health setget set_health, get_health

func set_health(value):
    health = value
```

**Godot 4:**
```gdscript
var health: int:
    set(value):
        health = value
        emit_signal("health_changed", health)
    get:
        return health
```

### 3. Tween 系统

`Tween` 节点已弃用。请在代码中使用 `create_tween()`。

**Godot 3:**
```gdscript
$Tween.interpolate_property(...)
$Tween.start()
```

**Godot 4:**
```gdscript
var tween = create_tween()
tween.tween_property($Sprite, "position", Vector2(100, 100), 1.0)
tween.parallel().tween_property($Sprite, "modulate:a", 0.0, 1.0)
```

### 4. 信号连接

基于字符串的连接方式已不推荐使用。请使用 callable。

**Godot 3:**
```gdscript
connect("pressed", self, "_on_pressed")
```

**Godot 4:**
```gdscript
pressed.connect(_on_pressed)
```

## 示例

### 示例 1：类型化数组

GDScript 2.0 支持类型化数组，可提升性能并增强类型安全。

```gdscript
# Godot 3
var enemies = []

# Godot 4
var enemies: Array[Node] = []

func _ready():
    for child in get_children():
        if child is Enemy:
            enemies.append(child)
```

### 示例 2：等待信号（协程）

`yield` 已被 `await` 取代。

**Godot 3:**
```gdscript
yield(get_tree().create_timer(1.0), "timeout")
```

**Godot 4:**
```gdscript
await get_tree().create_timer(1.0).timeout
```

## 最佳实践

- ✅ **推荐：** 使用 `@export_range`、`@export_file` 等注解以优化检查器 UI。
- ✅ **推荐：** 为所有变量添加类型注解（`var x: int`）以获得 GDScript 2.0 的性能提升。
- ✅ **推荐：** 使用 `super()` 调用父类方法，而非 `.function_name()`。
- ❌ **避免：** 若可使用信号对象（`name.emit()`），则不要使用字符串形式的信号名（`emit_signal("name")`）。

## 故障排查

**问题：** "Identifier 'Tween' is not a valid type."
**解决方案：** `Tween` 现为 `SceneTreeTween` 或 `create_tween()` 返回的对象。通常无需显式声明类型，直接使用 `var tween = create_tween()` 即可。

## 限制
- 仅在任务明确符合上述范围时使用本技能。
- 输出内容不可替代环境特定的验证、测试或专家评审。
- 若缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
