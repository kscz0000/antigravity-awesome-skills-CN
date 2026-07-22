---
name: fastapi-router-py
description: "按照既定模式创建 FastAPI 路由，包含正确的认证、响应模型和 HTTP 状态码。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# FastAPI 路由

按照既定模式创建 FastAPI 路由，包含正确的认证、响应模型和 HTTP 状态码。

## 快速开始

从 assets/template.py 复制模板并替换占位符：
- `{{ResourceName}}` → 帕斯卡命名法名称（如 `Project`）
- `{{resource_name}}` → 蛇形命名法名称（如 `project`）
- `{{resource_plural}}` → 复数形式（如 `projects`）

## 认证模式

```python
# 可选认证 - 未认证时返回 None
current_user: Optional[User] = Depends(get_current_user)

# 必需认证 - 未认证时抛出 401
current_user: User = Depends(get_current_user_required)
```

## 响应模型

```python
@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str) -> Item:
    ...

@router.get("/items", response_model=list[Item])
async def list_items() -> list[Item]:
    ...
```

## HTTP 状态码

```python
@router.post("/items", status_code=status.HTTP_201_CREATED)
@router.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
```

## 集成步骤

1. 在 `src/backend/app/routers/` 中创建路由
2. 在 `src/backend/app/main.py` 中挂载
3. 创建对应的 Pydantic 模型
4. 如需要，创建服务层
5. 添加前端 API 函数

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
