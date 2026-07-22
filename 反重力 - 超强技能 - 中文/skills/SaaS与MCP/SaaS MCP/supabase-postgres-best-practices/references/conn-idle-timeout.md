---
title: 配置空闲连接超时
impact: HIGH
impactDescription: 从空闲客户端回收 30-50% 的连接槽
tags: connections, timeout, idle, resource-management
---

## 配置空闲连接超时

空闲连接浪费资源。配置超时以自动回收它们。

**错误做法（连接无限期保持）：**

```sql
-- 未配置超时
show idle_in_transaction_session_timeout;  -- 0（已禁用）

-- 连接一直保持打开，即使空闲
select pid, state, state_change, query
from pg_stat_activity
where state = 'idle in transaction';
-- 显示空闲数小时的事务，持有锁
```

**正确做法（自动清理空闲连接）：**

```sql
-- 30 秒后终止事务中空闲的连接
alter system set idle_in_transaction_session_timeout = '30s';

-- 10 分钟后终止完全空闲的连接
alter system set idle_session_timeout = '10min';

-- 重新加载配置
select pg_reload_conf();
```

对于连接池，在池化器层面配置：

```ini
# pgbouncer.ini
server_idle_timeout = 60
client_idle_timeout = 300
```

参考：[连接超时](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT)
