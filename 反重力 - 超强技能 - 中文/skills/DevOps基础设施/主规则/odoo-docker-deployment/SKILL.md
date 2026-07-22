---
name: odoo-docker-deployment
description: "生产就绪的 Odoo Docker 和 docker-compose 部署方案，包含 PostgreSQL、持久化卷、基于环境变量的配置以及 Nginx 反向代理。当用户要求'部署 Odoo Docker'、'配置 Odoo 容器'或'Odoo 生产环境搭建'时使用。"
risk: safe
source: "self"
---

# Odoo Docker 部署

## 概述

本技能提供一套完整的、生产就绪的 Odoo Docker 部署方案，包括 PostgreSQL、持久化文件存储、环境变量配置，以及可选的带 SSL 的 Nginx 反向代理。涵盖开发和生产两种配置场景。

## 使用场景

- 使用 Docker 快速搭建本地 Odoo 开发环境。
- 将 Odoo 部署到 VPS 或云服务器（AWS、DigitalOcean 等）。
- 排查 Odoo 容器启动失败或数据库连接错误。
- 为已有的 Odoo Docker 环境添加带 SSL 的反向代理。

## 工作方式

1. **激活**：提及 `@odoo-docker-deployment` 并描述你的部署场景。
2. **生成**：获得一份完整的、可直接运行的 `docker-compose.yml` 和 `odoo.conf`。
3. **调试**：描述容器错误信息，获取诊断结果和修复方案。

## 示例

### 示例 1：生产环境 docker-compose.yml

```yaml
# Note: The top-level 'version' key is deprecated in Docker Compose v2+
# and can be safely omitted. Remove it to avoid warnings.

services:
  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_DB: odoo
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - odoo-net

  odoo:
    image: odoo:17.0
    restart: always
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8069:8069"
      - "8072:8072"   # Longpolling for live chat / bus
    environment:
      HOST: db
      USER: odoo
      PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - odoo-web-data:/var/lib/odoo
      - ./addons:/mnt/extra-addons   # Custom modules
      - ./odoo.conf:/etc/odoo/odoo.conf
    networks:
      - odoo-net

volumes:
  postgres-data:
  odoo-web-data:

networks:
  odoo-net:
```

### 示例 2：odoo.conf

```ini
[options]
admin_passwd = ${ODOO_MASTER_PASSWORD}    ; set via env or .env file
db_host = db
db_port = 5432
db_user = odoo
db_password = ${POSTGRES_PASSWORD}        ; set via env or .env file

; addons_path inside the official Odoo Docker image (Debian-based)
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons

logfile = /var/log/odoo/odoo.log
log_level = warn

; Worker tuning for a 4-core / 8GB server:
workers = 9                ; (CPU cores × 2) + 1
max_cron_threads = 2
limit_memory_soft = 1610612736   ; 1.5 GB — soft kill threshold
limit_memory_hard = 2147483648   ; 2.0 GB — hard kill threshold
limit_time_cpu = 600
limit_time_real = 1200
limit_request = 8192
```

### 示例 3：常用命令

```bash
# Start all services in background
docker compose up -d

# Stream Odoo logs in real time
docker compose logs -f odoo

# Restart Odoo only (not DB — avoids data risk)
docker compose restart odoo

# Stop all services
docker compose down

# Backup the database to a local SQL dump
docker compose exec db pg_dump -U odoo odoo > backup_$(date +%Y%m%d).sql

# Update a custom module without restarting the server
docker compose exec odoo odoo -d odoo --update my_module --stop-after-init
```

## 最佳实践

- ✅ **推荐：** 将所有密钥存储在 `.env` 文件中，通过 `${VAR}` 引用——切勿在 `docker-compose.yml` 中硬编码密码。
- ✅ **推荐：** 使用 `depends_on: condition: service_healthy` 配合 PostgreSQL 健康检查，防止 Odoo 在数据库就绪前启动。
- ✅ **推荐：** 在 Odoo 前部署 Nginx 进行 SSL 终止（Let's Encrypt / Certbot）——切勿将 Odoo 直接暴露在 80/443 端口。
- ✅ **推荐：** 在 `odoo.conf` 中设置 `workers = (CPU 核心数 × 2) + 1`——`workers = 0` 会使用单线程模式，阻塞所有用户。
- ❌ **禁止：** 将 5432 端口（PostgreSQL）暴露到公网——仅保留在 Docker 内部网络中。
- ❌ **禁止：** 在生产环境使用 `latest` 或 `17` 等 Docker 镜像标签——始终锁定到具体的补丁版本标签（如 `odoo:17.0`）。
- ❌ **禁止：** 在 CI/CD 中挂载 `odoo.conf` 并依赖它存储密钥——应使用 Docker secrets 或环境变量。

## 限制

- 本技能涵盖**自托管 Docker 部署**——Odoo.sh（云托管）采用完全不同的部署模型。
- **水平扩展**（多个 Odoo 容器配合负载均衡器）需要共享文件存储（NFS 或 S3 兼容存储），此处不涉及。
- 不包含 Nginx 配置模板——完整的反向代理配置请参考 [Odoo 官方 Nginx 文档](https://www.odoo.com/documentation/17.0/administration/install/deploy.html)。
- Docker 镜像内的 `addons_path` 可能随基础镜像版本更新而变化——升级 Odoo 镜像后务必验证。
