---
name: odoo-backup-strategy
description: "完整的 Odoo 备份与恢复策略：数据库转储、filestore 备份、自动化调度、云存储备份上传以及经过验证的恢复流程。当用户要求'Odoo 备份'、'Odoo 恢复'、'数据库备份'、'filestore 备份'、'自动备份脚本'、'Odoo 迁移'或'备份策略'时使用。"
risk: safe
source: "self"
---

# Odoo 备份策略

## 概述

一次完整的 Odoo 备份必须同时包含 **PostgreSQL 数据库**和 **filestore**（附件、图片）。本技能涵盖手动和自动备份流程、异地存储，以及在 Odoo 实例宕机后将其恢复上线的正确步骤。

## 使用场景

- 为生产环境 Odoo 实例搭建备份策略。
- 使用 shell 脚本和 cron 实现每日自动备份。
- 在服务器故障或数据损坏后恢复 Odoo。
- 诊断备份失败或恢复损坏的问题。

## 工作原理

1. **激活**：提及 `@odoo-backup-strategy` 并描述你的服务器环境。
2. **生成**：获得一份针对你的环境定制的完整备份脚本。
3. **恢复**：获取针对各种故障场景的分步恢复指南。

## 示例

### 示例 1：手动备份数据库 + Filestore

```bash
#!/bin/bash
# backup_odoo.sh

DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="odoo"
DB_USER="odoo"
FILESTORE_PATH="/var/lib/odoo/.local/share/Odoo/filestore/$DB_NAME"
BACKUP_DIR="/backups/odoo"

mkdir -p "$BACKUP_DIR"

# Step 1: Dump the database
pg_dump -U $DB_USER -Fc $DB_NAME > "$BACKUP_DIR/db_$DATE.dump"

# Step 2: Archive the filestore
tar -czf "$BACKUP_DIR/filestore_$DATE.tar.gz" -C "$FILESTORE_PATH" .

echo "✅ Backup complete: db_$DATE.dump + filestore_$DATE.tar.gz"
```

### 示例 2：使用 Cron 自动化（每日凌晨 2 点）

```bash
# Run: crontab -e
# Add this line:
0 2 * * * /opt/scripts/backup_odoo.sh >> /var/log/odoo_backup.log 2>&1
```

### 示例 3：上传到 S3（备份完成后）

```bash
# Add to backup script after tar command:
aws s3 cp "$BACKUP_DIR/db_$DATE.dump"        s3://my-odoo-backups/db/
aws s3 cp "$BACKUP_DIR/filestore_$DATE.tar.gz" s3://my-odoo-backups/filestore/

# Optional: Delete local backups older than 7 days
find "$BACKUP_DIR" -type f -mtime +7 -delete
```

### 示例 4：完整恢复流程

```bash
# Step 1: Stop Odoo
docker compose stop odoo  # or: systemctl stop odoo

# Step 2: Recreate and restore the database
# (--clean alone fails if the DB doesn't exist; drop and recreate first)
dropdb -U odoo odoo 2>/dev/null || true
createdb -U odoo odoo
pg_restore -U odoo -d odoo db_YYYYMMDD_HHMMSS.dump

# Step 3: Restore the filestore
FILESTORE=/var/lib/odoo/.local/share/Odoo/filestore/odoo
rm -rf "$FILESTORE"/*
tar -xzf filestore_YYYYMMDD_HHMMSS.tar.gz -C "$FILESTORE"/

# Step 4: Restart Odoo
docker compose start odoo

# Step 5: Verify — open Odoo in the browser and check:
#   - Can you log in?
#   - Are recent records visible?
#   - Are file attachments loading?
```

## 最佳实践

- ✅ **推荐做法**：每月在预发布环境中测试恢复——一个从未恢复过的备份不算真正的备份。
- ✅ **推荐做法**：遵循 **3-2-1 原则**：3 份副本、2 种不同存储介质、1 份异地副本（如 S3 或远程服务器）。
- ✅ **推荐做法**：在**每次 Odoo 升级前立即备份**——这是你的回滚点。
- ✅ **推荐做法**：验证备份完整性：`pg_restore --list backup.dump` 应无错误完成。
- ❌ **禁止做法**：只备份数据库而不备份 filestore——恢复后所有附件和图片都会丢失。
- ❌ **禁止做法**：将备份存储在与 Odoo 相同的磁盘或服务器上——磁盘或服务器故障会同时毁掉两者。
- ❌ **禁止做法**：对不存在的数据库运行 `pg_restore --clean`——必须先创建数据库。

## 局限性

- 不涵盖 **Odoo.sh 内置备份**——Odoo.sh 有自己的备份系统，可从控制面板访问。
- 本脚本假设为**单数据库** Odoo 部署。多数据库实例需要遍历所有数据库。
- 不同安装方式下 filestore 路径可能不同（Docker 卷 vs 裸机部署）。恢复前务必通过 `odoo-bin shell` 确认路径。
- 超大 filestore（100GB+）可能需要使用增量备份工具如 `rsync` 或 `restic`，而非完整的 `tar.gz` 归档。
