# 任务简报模板

每次多智能体任务前复制此模板。填写后与协调器共享，等待确认。

```
MISSION BRIEF
─────────────────────────────────────────
Goal:
Total Agents:
Quota Strategy: [ FLASH-ONLY | MIXED | SONNET-LEAD ]
Expected Token Cost: [ LOW | MEDIUM | HIGH ]

AGENTS:
[1] ID: agent-001
    Role:
    Scope:
    Model: [ Gemini Flash | Claude Sonnet ]
    Input:
    Output:
    Depends on: [ none | agent-XXX ]

[2] ID: agent-002
    Role:
    Scope:
    Model:
    Input:
    Output:
    Depends on:

─────────────────────────────────────────
EXCLUSIONS（智能体不得触碰的文件）：
- node_modules/
- .next/
- dist/
- package-lock.json
- [添加项目特定的排除项]

API CONTRACT（如果智能体间共享数据）：
  Endpoint:
  Input shape:  { }
  Output shape: { }
─────────────────────────────────────────
```
