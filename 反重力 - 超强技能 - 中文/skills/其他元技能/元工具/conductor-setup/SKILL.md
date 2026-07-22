---
name: conductor-setup
description: 配置 Rails 项目以使用 Conductor（并行编码智能体）
allowed-tools: Bash(chmod *), Bash(bundle *), Bash(npm *), Bash(script/server)
context: fork
risk: unknown
source: community
metadata:
  author: Shpigford
  version: "1.0"
---

为 Conductor（Mac 平台的并行编码智能体应用）设置此 Rails 项目。

## 何时使用
- 你需要配置 Rails 项目，使其在 Conductor 工作区中正确运行。
- 项目需要支持并行编码智能体，包括隔离端口、Redis 设置和共享密钥。
- 你需要为 Rails 仓库创建标准的 `conductor.json`、`bin/conductor-setup` 和 `script/server` 脚手架。

# 需要创建的文件

## 1. conductor.json（项目根目录）

如果项目根目录下不存在 `conductor.json`，则创建：

```json
{
  "scripts": {
    "setup": "bin/conductor-setup",
    "run": "script/server"
  }
}
```

## 2. bin/conductor-setup（可执行文件）

如果不存在 `bin/conductor-setup`，则创建：

```bash
#!/bin/bash
set -e

# 从仓库根目录符号链接 .env（密钥存放位置，worktree 外部）
[ -f "$CONDUCTOR_ROOT_PATH/.env" ] && ln -sf "$CONDUCTOR_ROOT_PATH/.env" .env

# 符号链接 Rails master key
[ -f "$CONDUCTOR_ROOT_PATH/config/master.key" ] && ln -sf "$CONDUCTOR_ROOT_PATH/config/master.key" config/master.key

# 安装依赖
bundle install
npm install
```

使用 `chmod +x bin/conductor-setup` 使其可执行。

## 3. script/server（可执行文件）

如需要则创建 `script` 目录，然后创建 `script/server`（如果不存在）：

```bash
#!/bin/bash

# === 端口配置 ===
export PORT=${CONDUCTOR_PORT:-3000}
export VITE_RUBY_PORT=$((PORT + 1000))

# === Redis 隔离 ===
if [ -n "$CONDUCTOR_WORKSPACE_NAME" ]; then
  HASH=$(printf '%s' "$CONDUCTOR_WORKSPACE_NAME" | cksum | cut -d' ' -f1)
  REDIS_DB=$((HASH % 16))
  export REDIS_URL="redis://localhost:6379/${REDIS_DB}"
fi

exec bin/dev
```

使用 `chmod +x script/server` 使其可执行。

## 4. 更新 Rails 配置文件

对于以下文件，如果存在且包含 Redis 配置，更新为使用 `ENV.fetch('REDIS_URL', ...)` 或 `ENV['REDIS_URL']` 并提供回退值：

### config/initializers/sidekiq.rb
如果此文件存在并配置了 Redis，更新为使用：
```ruby
redis_url = ENV.fetch('REDIS_URL', 'redis://localhost:6379/0')
```

### config/cable.yml
如果此文件存在，更新 development 适配器为使用：
```yaml
development:
  adapter: redis
  url: <%= ENV.fetch('REDIS_URL', 'redis://localhost:6379/1') %>
```

### config/environments/development.rb
如果此文件配置了 Redis 缓存，更新为使用：
```ruby
config.cache_store = :redis_cache_store, { url: ENV.fetch('REDIS_URL', 'redis://localhost:6379/0') }
```

### config/initializers/rack_attack.rb
如果此文件存在并配置了 Redis 缓存存储，更新为使用：
```ruby
Rack::Attack.cache.store = ActiveSupport::Cache::RedisCacheStore.new(url: ENV.fetch('REDIS_URL', 'redis://localhost:6379/0'))
```

# 实现注意事项

- **不要覆盖现有文件**：创建 conductor.json、bin/conductor-setup 和 script/server 之前先检查是否存在。如果已存在，跳过创建并告知用户。
- **Rails 配置更新**：仅修改 Redis 相关配置。如果文件不存在或不使用 Redis，则优雅地跳过。
- **按需创建目录**：如果 `script/` 目录不存在则创建。

# 验证

创建文件后：
1. 确认所有 Conductor 文件存在且脚本可执行
2. 运行 `script/server` 验证其能正常启动
3. 检查 Rails 配置是否正确引用 `ENV['REDIS_URL']` 或 `ENV.fetch('REDIS_URL', ...)`

## 限制
- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
