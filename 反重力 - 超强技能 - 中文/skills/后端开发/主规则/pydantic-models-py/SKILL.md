---
name: pydantic-models-py
description: "遵循多模型模式创建 Pydantic 模型，构建清晰的 API 契约。触发词：Pydantic模型、多模型模式、API契约、数据模型、Pydantic model、FastAPI模型、请求响应模型"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Pydantic 模型

遵循多模型模式创建 Pydantic 模型，构建清晰的 API 契约。

## 快速开始

复制 assets/template.py 中的模板并替换占位符：
- `{{ResourceName}}` → PascalCase 命名（如 `Project`）
- `{{resource_name}}` → snake_case 命名（如 `project`）

## 多模型模式

| 模型 | 用途 |
|------|------|
| `Base` | 各模型共享的公共字段 |
| `Create` | 创建请求体（必填字段） |
| `Update` | 更新请求体（全部可选） |
| `Response` | 包含所有字段的 API 响应 |
| `InDB` | 带 `doc_type` 的数据库文档 |

## camelCase 别名

```python
class MyModel(BaseModel):
    workspace_id: str = Field(..., alias="workspaceId")
    created_at: datetime = Field(..., alias="createdAt")
    
    class Config:
        populate_by_name = True  # Accept both snake_case and camelCase
```

## 可选更新字段

```python
class MyUpdate(BaseModel):
    """All fields optional for PATCH requests."""
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
```

## 数据库文档

```python
class MyInDB(MyResponse):
    """Adds doc_type for Cosmos DB queries."""
    doc_type: str = "my_resource"
```

## 集成步骤

1. 在 `src/backend/app/models/` 中创建模型
2. 从 `src/backend/app/models/__init__.py` 导出
3. 添加对应的 TypeScript 类型

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅当任务明确匹配上述范围时使用本技能
- 不要将输出视为环境特定验证、测试或专家审查的替代品
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清
