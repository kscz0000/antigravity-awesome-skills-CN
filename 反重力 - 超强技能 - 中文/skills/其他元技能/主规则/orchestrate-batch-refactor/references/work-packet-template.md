# 工作包模板

在生成 worker 之前，使用此模板定义每个工作包。

## 工作包

- `id`：
- `objective`：
- `mode`：`refactor` | `rewrite` | `hybrid`
- `owner_agent_type`：`worker`
- `owned_files`：
- `dependencies`：
- `invariants_to_preserve`：
- `out_of_scope`：
- `required_checks`：
- `integration_notes`：
- `done_criteria`：

## 示例

- `id`：`P3`
- `objective`："Extract duplicated parsing logic from thread reducers into shared helper"
- `mode`：`refactor`
- `owner_agent_type`：`worker`
- `owned_files`：`src/features/threads/hooks/threadReducer/*.ts`
- `dependencies`：`P1`
- `invariants_to_preserve`："Thread ordering and hidden-thread filtering behavior"
- `out_of_scope`："UI rendering components"
- `required_checks`：`npm run typecheck`、`npm run test -- src/features/threads/hooks`
- `integration_notes`："Main thread verifies no overlapping helper names with existing util package"
- `done_criteria`："No duplicated parsing block remains; all required checks pass"
