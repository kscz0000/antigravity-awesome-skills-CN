# 基于 CLI 的 Actorization

对于没有 SDK 的语言（Go、Rust、Java 等），创建使用 Apify CLI 的包装脚本。

## 创建包装脚本

在项目根目录创建 `start.sh`：

```bash
#!/bin/bash
set -e

# 从 Apify 键值存储获取输入
INPUT=$(apify actor:get-input)

# 解析输入值（根据你的输入 schema 调整）
MY_PARAM=$(echo "$INPUT" | jq -r '.myParam // "default"')

# 使用输入运行你的应用程序
./your-application --param "$MY_PARAM"

# 如果你的应用写入文件，将其推送到键值存储
# apify actor:set-value OUTPUT --contentType application/json < output.json

# 或推送结构化数据到数据集
# apify actor:push-data '{"result": "value"}'
```

## 更新 Dockerfile

参考 [cli-start 模板 Dockerfile](https://github.com/apify/actor-templates/blob/master/templates/cli-start/Dockerfile)，其中包含用于从 GitHub releases 安装二进制文件的 `ubi` 工具。

```dockerfile
FROM apify/actor-node:20

# 从包源或已验证的发布产物安装 ubi
# 示例：使用基础镜像包管理器或在构建上下文中供应商固定二进制文件
# RUN apt-get update && apt-get install -y ubi

# 从 GitHub releases 安装你的 CLI 工具（示例）
# RUN install -m 0755 ./vendor/your-tool /usr/local/bin/your-tool

# 或手动安装 apify-cli 和 jq
RUN npm install -g apify-cli
RUN apt-get update && apt-get install -y jq

# 复制你的应用程序
COPY . .

# 如需要构建你的应用程序
# RUN ./build.sh

# 使启动脚本可执行
RUN chmod +x start.sh

# 运行包装脚本
CMD ["./start.sh"]
```

## 测试基于 CLI 的 Actor

对于基于 CLI 的 actor（shell 包装脚本），你可能需要直接使用模拟输入测试底层应用程序，因为 `apify run` 需要 Node.js 或 Python 入口点。

本地测试包装脚本：

```bash
# 设置模拟输入
export INPUT='{"myParam": "test-value"}'

# 运行包装脚本
./start.sh
```

## CLI 命令参考

| 命令 | 描述 |
|---------|-------------|
| `apify actor:get-input` | 从键值存储获取输入 JSON |
| `apify actor:set-value KEY` | 在键值存储中存储值 |
| `apify actor:push-data JSON` | 推送数据到数据集 |
| `apify actor:get-value KEY` | 从键值存储检索值 |
