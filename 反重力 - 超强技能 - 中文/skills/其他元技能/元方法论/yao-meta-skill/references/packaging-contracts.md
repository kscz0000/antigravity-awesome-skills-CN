# 打包契约

`cross_packager.py` 不仅仅是一个导出辅助工具。它会校验平台契约，并嵌入来自 `compile_skill.py` 的目标编译器输出。

## 当前目标

- `openai`
- `claude`
- `generic`

## 契约结构

每个目标契约定义：

- 必需的输出字段
- 必需的输出文件
- 从中性源元数据进行的字段映射
- 来自 Skill IR 的已编译契约
- 目标转换元数据，包括生成的文件和不受支持的功能
- 可移植执行元数据
- 信任边界元数据
- 来自信任报告的权限契约元数据
- 目标特定的权限表示形式与评审者备注
- 针对原生表面、激活策略、资源策略、脚本策略、权限强制执行、安装范围、评审产物以及回退行为的目标原生行为契约
- 降级策略元数据

## 失败处理

当提供 `--expectations` 时：

- 缺少必需的文件会导致退出码 `2`
- 缺少必需的字段会导致退出码 `2`
- 校验失败会以 JSON 报告的形式输出

打包完成后，对生成的包目录运行 `scripts/probe_runtime_permissions.py`。打包过程会创建权限元数据；运行时权限探测用于验证每个目标适配器是否都对外暴露契约、目标特定的表示形式、原生强制执行标志、操作员备注以及残余的元数据回退风险。

## 真相来源

当存在 Skill IR 时，平台中性的语义源就是 Skill IR：

- `reports/skill-ir.json`
- `skill-ir/examples/<技能名称>.json`

结构校验源仍为：

- `SKILL.md`
- `agents/interface.yaml`

目标特定的元数据通过 `scripts/compile_skill.py` 生成，然后
在打包时嵌入。适配器必须携带 `compiler`、
`compiled_contract`、`permission_contract`、`target_permission_contract`、
`target_native_contract`、`target_transform`、`ir_source`、`ir_schema_version`、
`job_to_be_done`、`semantic_contract` 以及 `semantic_parity`，以便评审者能够
判断目标是保留了核心技能语义，还是已回退为
仅含 frontmatter 的元数据。

## 可移植性模型

打包层现在从中性源中保留四种可移植语义：

- 激活
- 执行
- 信任
- 权限
- 降级
- 来自 Skill IR 的平台中性技能含义
- 针对激活、资源、脚本、权限强制执行、安装范围、评审产物以及回退行为的目标特定原生行为备注
- 针对生成文件、适配器模式、已保留语义以及不受支持功能的目标特定编译备注

这意味着可移植性不仅仅是"它能否导出文件"，还包括"导出的目标是否保留了源包的激活与安全假设"。