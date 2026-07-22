# 分发注册表方法

注册表元数据把本地技能目录转变为可安装、可审查的包记录。

## 适用场景

针对库类、受治理、团队分发或升级敏感型技能执行注册表审计。脚手架类技能在复用尚未真实发生前可跳过。

## 必备证据

- 包名、版本、负责人、成熟度、审查节奏、许可证
- Skill IR 源与 schema 版本
- 信任等级与包 SHA256
- 包验证状态；构建 zip 分发时还需归档 SHA256
- 安装模拟状态；归档用于本地或团队安装时必须提供
- 采用度/漂移聚合状态；存在本地遥测时必须提供
- 目标兼容性矩阵
- 升级差异、推荐版本号递增、破坏性变更说明；存在先前包基线时必须提供
- 链接到概览、Review Studio、信任报告、符合性矩阵、包验证、安装模拟、采用度漂移证据、审查豁免

## 发布规则

当注册表审计报告缺失版本、哈希、负责人、审查节奏、许可证、合法 Skill IR，或对声明目标的兼容性未通过时，禁止发布团队包。

针对可安装归档，先构建分发并执行包验证：

```bash
python3 scripts/yao.py package . --platform openai --platform claude --platform generic --platform vscode --output-dir dist --zip
python3 scripts/yao.py package-verify . --package-dir dist --require-zip
python3 scripts/yao.py install-simulate . --package-dir dist
python3 scripts/yao.py registry-audit .
python3 scripts/yao.py upgrade-check . --previous-package-json registry/examples/yao-meta-skill-1.0.0.json
```

当包验证报告不安全 zip 路径、缺失目标适配器、缺失包清单、注册表元数据不匹配，或归档内容不可读时，禁止声称归档就绪。

当安装模拟无法将归档解包到临时技能根目录、无法加载 `SKILL.md` frontmatter、无法读取 `manifest.json`、无法读取 `agents/interface.yaml`、无法定位概览与 Review Studio 报告，或无法加载每个生成的适配器时，禁止声称安装就绪。

在同一个包通过安装预检之前，禁止从源同步本地或活动安装。`scripts/sync_local_install.py` 必须针对配置的包目录执行安装模拟，并在任何目标/能力对缺少活动权限批准或目标特定的执行证据时，于复制文件前失败。`--skip-install-preflight` 仅用于隔离诊断，不得用于发布或活动安装。

禁止将原始 `reports/telemetry_events.jsonl` 纳入分发包。仅纳入聚合后的采用度漂移报告；当遥测包含原始提示、输出、转录、笔记或消息时，阻止发布审查。

审查豁免证据可以以 `reports/review_waivers.md/json` 形式分发，因为它只含元数据级别的审查者问责信息。不得在豁免原因中存储原始提示、输出、转录、凭证或私有客户细节。

当升级检查报告版本号递增不足、删除目标却未做主版本递增、兼容性回退却未做主版本递增、包名变更，或 semver 非法时，禁止声称升级就绪。将 `reports/upgrade_check.md` 纳入审查者证据包，使发布说明与迁移指南与精确的注册表差异绑定。

## 审查者关卡

审查者应能回答：

1. 正在安装哪个包版本？
2. 该包由谁负责？
3. 哪些目标兼容？
4. 哪个校验和标识被审查的包内容？
5. 哪些报告证明信任与运行时就绪？
6. 可安装归档是否经过验证，由哪个校验和标识？
7. 该归档是否在临时本地技能根目录中完成安装模拟？
8. 本地或活动安装同步是否保留了上述预检与安装器权限关卡？
9. 相对先前包做了哪些变更，声明的版本号递增是否与推荐递增匹配？
10. 采用度与漂移信号是否以聚合形式呈现，未将原始本地遥测打包？
