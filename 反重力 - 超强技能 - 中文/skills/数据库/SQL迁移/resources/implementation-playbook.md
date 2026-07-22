# SQL 数据库迁移策略与实施 实施手册

本文件包含技能所引用的详细模式、检查清单和代码示例。

# SQL 数据库迁移策略与实施

你是 SQL 数据库迁移专家，专精于 PostgreSQL、MySQL 和 SQL Server 的零停机部署、数据完整性和生产级迁移策略。需创建包含回滚程序、验证检查和性能优化的综合迁移脚本。

## 适用场景

- 处理 SQL 数据库迁移策略与实施相关的任务或工作流
- 需要 SQL 数据库迁移策略与实施的指导、最佳实践或检查清单

## 不适用场景

- 任务与 SQL 数据库迁移策略与实施无关
- 需要本范围之外的其他领域或工具

## 背景
用户需要能够保证数据完整性、最小化停机时间并提供安全回滚选项的 SQL 数据库迁移方案。需重点关注处理边缘情况、大数据集和并发操作的生产级策略。

## 需求
$ARGUMENTS

## 说明

### 1. 零停机迁移策略

**扩展-收缩模式（Expand-Contract Pattern）**

```sql
-- Phase 1: EXPAND (backward compatible)
ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;
CREATE INDEX CONCURRENTLY idx_users_email_verified ON users(email_verified);

-- Phase 2: MIGRATE DATA (in batches)
DO $$
DECLARE
    batch_size INT := 10000;
    rows_updated INT;
BEGIN
    LOOP
        UPDATE users
        SET email_verified = (email_confirmation_token IS NOT NULL)
        WHERE id IN (
            SELECT id FROM users
            WHERE email_verified IS NULL
            LIMIT batch_size
        );

        GET DIAGNOSTICS rows_updated = ROW_COUNT;
        EXIT WHEN rows_updated = 0;
        COMMIT;
        PERFORM pg_sleep(0.1);
    END LOOP;
END $$;

-- Phase 3: CONTRACT (after code deployment)
ALTER TABLE users DROP COLUMN email_confirmation_token;
```

**蓝绿 Schema 迁移（Blue-Green Schema Migration）**

```sql
-- Step 1: Create new schema version
CREATE TABLE v2_orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_v2_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT chk_v2_orders_amount
        CHECK (total_amount >= 0)
);

CREATE INDEX idx_v2_orders_customer ON v2_orders(customer_id);
CREATE INDEX idx_v2_orders_status ON v2_orders(status);

-- Step 2: Dual-write synchronization
CREATE OR REPLACE FUNCTION sync_orders_to_v2()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO v2_orders (id, customer_id, total_amount, status)
    VALUES (NEW.id, NEW.customer_id, NEW.amount, NEW.state)
    ON CONFLICT (id) DO UPDATE SET
        total_amount = EXCLUDED.total_amount,
        status = EXCLUDED.status;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER sync_orders_trigger
AFTER INSERT OR UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION sync_orders_to_v2();

-- Step 3: Backfill historical data
DO $$
DECLARE
    batch_size INT := 10000;
    last_id UUID := NULL;
BEGIN
    LOOP
        INSERT INTO v2_orders (id, customer_id, total_amount, status)
        SELECT id, customer_id, amount, state
        FROM orders
        WHERE (last_id IS NULL OR id > last_id)
        ORDER BY id
        LIMIT batch_size
        ON CONFLICT (id) DO NOTHING;

        SELECT id INTO last_id FROM orders
        WHERE (last_id IS NULL OR id > last_id)
        ORDER BY id LIMIT 1 OFFSET (batch_size - 1);

        EXIT WHEN last_id IS NULL;
        COMMIT;
    END LOOP;
END $$;
```

**在线 Schema 变更（Online Schema Change）**

```sql
-- PostgreSQL: Add NOT NULL safely
-- Step 1: Add column as nullable
ALTER TABLE large_table ADD COLUMN new_field VARCHAR(100);

-- Step 2: Backfill data
UPDATE large_table
SET new_field = 'default_value'
WHERE new_field IS NULL;

-- Step 3: Add constraint (PostgreSQL 12+)
ALTER TABLE large_table
    ADD CONSTRAINT chk_new_field_not_null
    CHECK (new_field IS NOT NULL) NOT VALID;

ALTER TABLE large_table
    VALIDATE CONSTRAINT chk_new_field_not_null;
```

### 2. 迁移脚本

**Flyway 迁移**

```sql
-- V001__add_user_preferences.sql
BEGIN;

CREATE TABLE IF NOT EXISTS user_preferences (
    user_id UUID PRIMARY KEY,
    theme VARCHAR(20) DEFAULT 'light' NOT NULL,
    language VARCHAR(10) DEFAULT 'en' NOT NULL,
    timezone VARCHAR(50) DEFAULT 'UTC' NOT NULL,
    notifications JSONB DEFAULT '{}' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user_preferences_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_user_preferences_language ON user_preferences(language);

-- Seed defaults for existing users
INSERT INTO user_preferences (user_id)
SELECT id FROM users
ON CONFLICT (user_id) DO NOTHING;

COMMIT;
```

**Alembic 迁移（Python）**

```python
"""add_user_preferences

Revision ID: 001_user_prefs
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table(
        'user_preferences',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('theme', sa.VARCHAR(20), nullable=False, server_default='light'),
        sa.Column('language', sa.VARCHAR(10), nullable=False, server_default='en'),
        sa.Column('timezone', sa.VARCHAR(50), nullable=False, server_default='UTC'),
        sa.Column('notifications', postgresql.JSONB, nullable=False,
                  server_default=sa.text("'{}'::jsonb")),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )

    op.create_index('idx_user_preferences_language', 'user_preferences', ['language'])

    op.execute("""
        INSERT INTO user_preferences (user_id)
        SELECT id FROM users
        ON CONFLICT (user_id) DO NOTHING
    """)

def downgrade():
    op.drop_table('user_preferences')
```

### 3. 数据完整性验证

```python
def validate_pre_migration(db_connection):
    checks = []

    # Check 1: NULL values in critical columns
    null_check = db_connection.execute("""
        SELECT table_name, COUNT(*) as null_count
        FROM users WHERE email IS NULL
    """).fetchall()

    if null_check[0]['null_count'] > 0:
        checks.append({
            'check': 'null_values',
            'status': 'FAILED',
            'severity': 'CRITICAL',
            'message': 'NULL values found in required columns'
        })

    # Check 2: Duplicate values
    duplicate_check = db_connection.execute("""
        SELECT email, COUNT(*) as count
        FROM users
        GROUP BY email
        HAVING COUNT(*) > 1
    """).fetchall()

    if duplicate_check:
        checks.append({
            'check': 'duplicates',
            'status': 'FAILED',
            'severity': 'CRITICAL',
            'message': f'{len(duplicate_check)} duplicate emails'
        })

    return checks

def validate_post_migration(db_connection, migration_spec):
    validations = []

    # Row count verification
    for table in migration_spec['affected_tables']:
        actual_count = db_connection.execute(
            f"SELECT COUNT(*) FROM {table['name']}"
        ).fetchone()[0]

        validations.append({
            'check': 'row_count',
            'table': table['name'],
            'expected': table['expected_count'],
            'actual': actual_count,
            'status': 'PASS' if actual_count == table['expected_count'] else 'FAIL'
        })

    return validations
```

### 4. 回滚程序

```python
import psycopg2
from contextlib import contextmanager

class MigrationRunner:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None

    @contextmanager
    def migration_transaction(self):
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.conn.autocommit = False

            cursor = self.conn.cursor()
            cursor.execute("SAVEPOINT migration_start")

            yield cursor

            self.conn.commit()

        except Exception as e:
            if self.conn:
                self.conn.rollback()
            raise
        finally:
            if self.conn:
                self.conn.close()

    def run_with_validation(self, migration):
        try:
            # Pre-migration validation
            pre_checks = self.validate_pre_migration(migration)
            if any(c['status'] == 'FAILED' for c in pre_checks):
                raise MigrationError("Pre-migration validation failed")

            # Create backup
            self.create_snapshot()

            # Execute migration
            with self.migration_transaction() as cursor:
                for statement in migration.forward_sql:
                    cursor.execute(statement)

                post_checks = self.validate_post_migration(migration, cursor)
                if any(c['status'] == 'FAIL' for c in post_checks):
                    raise MigrationError("Post-migration validation failed")

            self.cleanup_snapshot()

        except Exception as e:
            self.rollback_from_snapshot()
            raise
```

**回滚脚本**

```bash
#!/bin/bash
# rollback_migration.sh

set -e

MIGRATION_VERSION=$1
DATABASE=$2

# Verify current version
CURRENT_VERSION=$(psql -d $DATABASE -t -c \
    "SELECT version FROM schema_migrations ORDER BY applied_at DESC LIMIT 1" | xargs)

if [ "$CURRENT_VERSION" != "$MIGRATION_VERSION" ]; then
    echo "❌ Version mismatch"
    exit 1
fi

# Create backup
BACKUP_FILE="pre_rollback_${MIGRATION_VERSION}_$(date +%Y%m%d_%H%M%S).sql"
pg_dump -d $DATABASE -f "$BACKUP_FILE"

# Execute rollback
if [ -f "migrations/${MIGRATION_VERSION}.down.sql" ]; then
    psql -d $DATABASE -f "migrations/${MIGRATION_VERSION}.down.sql"
    psql -d $DATABASE -c "DELETE FROM schema_migrations WHERE version = '$MIGRATION_VERSION';"
    echo "✅ Rollback complete"
else
    echo "❌ Rollback file not found"
    exit 1
fi
```

### 5. 性能优化

**批处理**

```python
class BatchMigrator:
    def __init__(self, db_connection, batch_size=10000):
        self.db = db_connection
        self.batch_size = batch_size

    def migrate_large_table(self, source_query, target_query, cursor_column='id'):
        last_cursor = None
        batch_number = 0

        while True:
            batch_number += 1

            if last_cursor is None:
                batch_query = f"{source_query} ORDER BY {cursor_column} LIMIT {self.batch_size}"
                params = []
            else:
                batch_query = f"{source_query} AND {cursor_column} > %s ORDER BY {cursor_column} LIMIT {self.batch_size}"
                params = [last_cursor]

            rows = self.db.execute(batch_query, params).fetchall()
            if not rows:
                break

            for row in rows:
                self.db.execute(target_query, row)

            last_cursor = rows[-1][cursor_column]
            self.db.commit()

            print(f"Batch {batch_number}: {len(rows)} rows")
            time.sleep(0.1)
```

**并行迁移**

```python
from concurrent.futures import ThreadPoolExecutor

class ParallelMigrator:
    def __init__(self, db_config, num_workers=4):
        self.db_config = db_config
        self.num_workers = num_workers

    def migrate_partition(self, partition_spec):
        table_name, start_id, end_id = partition_spec

        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()

        cursor.execute(f"""
            INSERT INTO v2_{table_name} (columns...)
            SELECT columns...
            FROM {table_name}
            WHERE id >= %s AND id < %s
        """, [start_id, end_id])

        conn.commit()
        cursor.close()
        conn.close()

    def migrate_table_parallel(self, table_name, partition_size=100000):
        # Get table bounds
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()

        cursor.execute(f"SELECT MIN(id), MAX(id) FROM {table_name}")
        min_id, max_id = cursor.fetchone()

        # Create partitions
        partitions = []
        current_id = min_id
        while current_id <= max_id:
            partitions.append((table_name, current_id, current_id + partition_size))
            current_id += partition_size

        # Execute in parallel
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            results = list(executor.map(self.migrate_partition, partitions))

        conn.close()
```

### 6. 索引管理

```sql
-- Drop indexes before bulk insert, recreate after
CREATE TEMP TABLE migration_indexes AS
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'large_table'
  AND indexname NOT LIKE '%pkey%';

-- Drop indexes
DO $$
DECLARE idx_record RECORD;
BEGIN
    FOR idx_record IN SELECT indexname FROM migration_indexes
    LOOP
        EXECUTE format('DROP INDEX IF EXISTS %I', idx_record.indexname);
    END LOOP;
END $$;

-- Perform bulk operation
INSERT INTO large_table SELECT * FROM source_table;

-- Recreate indexes CONCURRENTLY
DO $$
DECLARE idx_record RECORD;
BEGIN
    FOR idx_record IN SELECT indexdef FROM migration_indexes
    LOOP
        EXECUTE regexp_replace(idx_record.indexdef, 'CREATE INDEX', 'CREATE INDEX CONCURRENTLY');
    END LOOP;
END $$;
```

## 输出格式

1. **迁移分析报告**：变更的详细分解
2. **零停机实施计划**：扩展-收缩或蓝绿策略
3. **迁移脚本**：版本控制的 SQL，集成框架
4. **验证套件**：迁移前后的检查
5. **回滚程序**：自动和手动回滚脚本
6. **性能优化**：批处理、并行执行
7. **监控集成**：进度跟踪和告警

专注于具有零停机部署策略、全面验证和企业级安全机制的生产级 SQL 迁移。

## 相关插件

- **nosql-migrations**：MongoDB、DynamoDB、Cassandra 的迁移策略
- **migration-observability**：实时监控和告警
- **migration-integration**：CI/CD 集成和自动化测试
