---
name: plaid-fintech
description: Plaid API 集成专家模式，涵盖 Link token 流程、交易同步、身份验证、ACH Auth、余额查询、webhook 处理及金融科技合规最佳实践。当用户要求集成 Plaid、银行账户关联、ACH 转账、交易同步或金融科技开发时使用。
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Plaid 金融科技

Plaid API 集成专家模式，涵盖 Link token 流程、交易同步、身份验证、ACH Auth、余额查询、webhook 处理及金融科技合规最佳实践。

## 模式

### Link Token 创建与交换

为 Plaid Link 创建 link_token，将 public_token 交换为 access_token。
Link token 生命周期短且仅限一次使用。access_token 不会过期，
但用户修改密码时可能需要更新。

// server.ts - Link token creation endpoint
import { Configuration, PlaidApi, PlaidEnvironments, Products, CountryCode } from 'plaid';

const configuration = new Configuration({
  basePath: PlaidEnvironments[process.env.PLAID_ENV || 'sandbox'],
  baseOptions: {
    headers: {
      'PLAID-CLIENT-ID': process.env.PLAID_CLIENT_ID,
      'PLAID-SECRET': process.env.PLAID_SECRET,
    },
  },
});

const plaidClient = new PlaidApi(configuration);

// Create link token for new user
app.post('/api/plaid/create-link-token', async (req, res) => {
  const { userId } = req.body;

  try {
    const response = await plaidClient.linkTokenCreate({
      user: {
        client_user_id: userId,  // Your internal user ID
      },
      client_name: 'My Finance App',
      products: [Products.Transactions],
      country_codes: [CountryCode.Us],
      language: 'en',
      webhook: 'https://yourapp.com/api/plaid/webhooks',
      // Request 180 days for recurring transactions
      transactions: {
        days_requested: 180,
      },
    });

    res.json({ link_token: response.data.link_token });
  } catch (error) {
    console.error('Link token creation failed:', error);
    res.status(500).json({ error: 'Failed to create link token' });
  }
});

// Exchange public token for access token
app.post('/api/plaid/exchange-token', async (req, res) => {
  const { publicToken, userId } = req.body;

  try {
    // Exchange for permanent access token
    const exchangeResponse = await plaidClient.itemPublicTokenExchange({
      public_token: publicToken,
    });

    const { access_token, item_id } = exchangeResponse.data;

    // Store securely - access_token doesn't expire!
    await db.plaidItem.create({
      data: {
        userId,
        itemId: item_id,
        accessToken: await encrypt(access_token),  // Encrypt at rest
        status: 'ACTIVE',
        products: ['transactions'],
      },
    });

    // Trigger initial transaction sync
    await initiateTransactionSync(item_id, access_token);

    res.json({ success: true, itemId: item_id });
  } catch (error) {
    console.error('Token exchange failed:', error);
    res.status(500).json({ error: 'Failed to exchange token' });
  }
});

// Frontend - React component
import { usePlaidLink } from 'react-plaid-link';

function BankLinkButton({ userId }: { userId: string }) {
  const [linkToken, setLinkToken] = useState<string | null>(null);

  useEffect(() => {
    async function createLinkToken() {
      const response = await fetch('/api/plaid/create-link-token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId }),
      });
      const { link_token } = await response.json();
      setLinkToken(link_token);
    }
    createLinkToken();
  }, [userId]);

  const { open, ready } = usePlaidLink({
    token: linkToken,
    onSuccess: async (publicToken, metadata) => {
      // Exchange public token for access token
      await fetch('/api/plaid/exchange-token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ publicToken, userId }),
      });
    },
    onExit: (error, metadata) => {
      if (error) {
        console.error('Link exit error:', error);
      }
    },
  });

  return (
    <button onClick={() => open()} disabled={!ready}>
      Connect Bank Account
    </button>
  );
}

### 上下文

- 初始银行关联
- 用户引导
- 账户连接

### 交易同步

使用 /transactions/sync 进行增量交易更新，比 /transactions/get 更高效。
通过 webhook 获取实时更新，而非轮询。

// Transactions sync service
interface TransactionSyncState {
  cursor: string | null;
  hasMore: boolean;
}

async function syncTransactions(
  accessToken: string,
  itemId: string
): Promise<void> {
  // Get last cursor from database
  const item = await db.plaidItem.findUnique({
    where: { itemId },
  });

  let cursor = item?.transactionsCursor || null;
  let hasMore = true;
  let addedCount = 0;
  let modifiedCount = 0;
  let removedCount = 0;

  while (hasMore) {
    try {
      const response = await plaidClient.transactionsSync({
        access_token: accessToken,
        cursor: cursor || undefined,
        count: 500,  // Max per request
      });

      const { added, modified, removed, next_cursor, has_more } = response.data;

      // Process added transactions
      if (added.length > 0) {
        await db.transaction.createMany({
          data: added.map(txn => ({
            plaidTransactionId: txn.transaction_id,
            itemId,
            accountId: txn.account_id,
            amount: txn.amount,
            date: new Date(txn.date),
            name: txn.name,
            merchantName: txn.merchant_name,
            category: txn.personal_finance_category?.primary,
            subcategory: txn.personal_finance_category?.detailed,
            pending: txn.pending,
            paymentChannel: txn.payment_channel,
            location: txn.location ? JSON.stringify(txn.location) : null,
          })),
          skipDuplicates: true,
        });
        addedCount += added.length;
      }

      // Process modified transactions
      for (const txn of modified) {
        await db.transaction.updateMany({
          where: { plaidTransactionId: txn.transaction_id },
          data: {
            amount: txn.amount,
            name: txn.name,
            merchantName: txn.merchant_name,
            pending: txn.pending,
            updatedAt: new Date(),
          },
        });
        modifiedCount++;
      }

      // Process removed transactions
      if (removed.length > 0) {
        await db.transaction.deleteMany({
          where: {
            plaidTransactionId: {
              in: removed.map(r => r.transaction_id),
            },
          },
        });
        removedCount += removed.length;
      }

      cursor = next_cursor;
      hasMore = has_more;

    } catch (error: any) {
      if (error.response?.data?.error_code === 'TRANSACTIONS_SYNC_MUTATION_DURING_PAGINATION') {
        // Data changed during pagination, restart from null
        cursor = null;
        continue;
      }
      throw error;
    }
  }

  // Save cursor for next sync
  await db.plaidItem.update({
    where: { itemId },
    data: { transactionsCursor: cursor },
  });

  console.log(`Sync complete: +${addedCount} ~${modifiedCount} -${removedCount}`);
}

// Webhook handler for real-time updates
app.post('/api/plaid/webhooks', async (req, res) => {
  const { webhook_type, webhook_code, item_id } = req.body;

  // Verify webhook (see webhook verification pattern)
  if (!verifyPlaidWebhook(req)) {
    return res.status(401).send('Invalid webhook');
  }

  if (webhook_type === 'TRANSACTIONS') {
    switch (webhook_code) {
      case 'SYNC_UPDATES_AVAILABLE':
        // New transactions available, trigger sync
        await queueTransactionSync(item_id);
        break;
      case 'INITIAL_UPDATE':
        // Initial batch of transactions ready
        await queueTransactionSync(item_id);
        break;
      case 'HISTORICAL_UPDATE':
        // Historical transactions ready
        await queueTransactionSync(item_id);
        break;
    }
  }

  res.sendStatus(200);
});

### 上下文

- 获取交易记录
- 交易历史
- 账户活动

### Item 错误处理与更新模式

通过 Link 更新模式处理 ITEM_LOGIN_REQUIRED 错误。
监听 PENDING_DISCONNECT webhook 以主动提示用户。

// Create link token for update mode
app.post('/api/plaid/create-update-token', async (req, res) => {
  const { itemId } = req.body;

  const item = await db.plaidItem.findUnique({
    where: { itemId },
    include: { user: true },
  });

  if (!item) {
    return res.status(404).json({ error: 'Item not found' });
  }

  try {
    const response = await plaidClient.linkTokenCreate({
      user: {
        client_user_id: item.userId,
      },
      client_name: 'My Finance App',
      country_codes: [CountryCode.Us],
      language: 'en',
      webhook: 'https://yourapp.com/api/plaid/webhooks',
      // Update mode: provide access_token instead of products
      access_token: await decrypt(item.accessToken),
    });

    res.json({ link_token: response.data.link_token });
  } catch (error) {
    console.error('Update token creation failed:', error);
    res.status(500).json({ error: 'Failed to create update token' });
  }
});

// Handle item errors from webhooks
app.post('/api/plaid/webhooks', async (req, res) => {
  const { webhook_type, webhook_code, item_id, error } = req.body;

  if (webhook_type === 'ITEM') {
    switch (webhook_code) {
      case 'ERROR':
        // Item has entered an error state
        await db.plaidItem.update({
          where: { itemId: item_id },
          data: {
            status: 'ERROR',
            errorCode: error?.error_code,
            errorMessage: error?.error_message,
          },
        });

        // Notify user to reconnect
        if (error?.error_code === 'ITEM_LOGIN_REQUIRED') {
          await notifyUserReconnect(item_id, 'Please reconnect your bank account');
        }
        break;

      case 'PENDING_DISCONNECT':
        // User needs to reauthorize soon
        await db.plaidItem.update({
          where: { itemId: item_id },
          data: { status: 'PENDING_DISCONNECT' },
        });

        // Proactive notification
        await notifyUserReconnect(item_id, 'Your bank connection will expire soon');
        break;

      case 'USER_PERMISSION_REVOKED':
        // User revoked access at their bank
        await db.plaidItem.update({
          where: { itemId: item_id },
          data: { status: 'REVOKED' },
        });

        // Clean up stored data
        await db.transaction.deleteMany({
          where: { itemId: item_id },
        });
        break;
    }
  }

  res.sendStatus(200);
});

// Check item status before API calls
async function getItemWithValidation(itemId: string) {
  const item = await db.plaidItem.findUnique({
    where: { itemId },
  });

  if (!item) {
    throw new Error('Item not found');
  }

  if (item.status === 'ERROR') {
    throw new ItemNeedsUpdateError(item.errorCode, item.errorMessage);
  }

  return item;
}

### 上下文

- 错误恢复
- 重新授权
- 凭据更新

### ACH 转账 Auth

使用 Auth 产品获取 ACH 转账所需的账户号和路由号。
结合 Identity 在发起转账前验证账户所有权。

// Get account and routing numbers
async function getACHNumbers(accessToken: string): Promise<ACHInfo[]> {
  const response = await plaidClient.authGet({
    access_token: accessToken,
  });

  const { accounts, numbers } = response.data;

  // Map ACH numbers to accounts
  return accounts.map(account => {
    const achNumber = numbers.ach.find(
      n => n.account_id === account.account_id
    );

    return {
      accountId: account.account_id,
      name: account.name,
      mask: account.mask,
      type: account.type,
      subtype: account.subtype,
      routing: achNumber?.routing,
      account: achNumber?.account,
      wireRouting: achNumber?.wire_routing,
    };
  });
}

// Verify identity before ACH transfer
async function verifyAndInitiateTransfer(
  accessToken: string,
  userId: string,
  amount: number
): Promise<TransferResult> {
  // Get identity from linked account
  const identityResponse = await plaidClient.identityGet({
    access_token: accessToken,
  });

  const accountOwners = identityResponse.data.accounts[0]?.owners || [];

  // Get user's stored identity
  const user = await db.user.findUnique({
    where: { id: userId },
  });

  // Match identity
  const matchResponse = await plaidClient.identityMatch({
    access_token: accessToken,
    user: {
      legal_name: user.legalName,
      phone_number: user.phoneNumber,
      email_address: user.email,
      address: {
        street: user.street,
        city: user.city,
        region: user.state,
        postal_code: user.postalCode,
        country: 'US',
      },
    },
  });

  const matchScores = matchResponse.data.accounts[0]?.legal_name;

  // Require high confidence for transfers
  if ((matchScores?.score || 0) < 70) {
    throw new Error('Identity verification failed');
  }

  // Get real-time balance for the transfer
  const balanceResponse = await plaidClient.accountsBalanceGet({
    access_token: accessToken,
  });

  const account = balanceResponse.data.accounts[0];

  // Check sufficient funds (consider pending)
  const availableBalance = account.balances.available ?? account.balances.current;
  if (availableBalance < amount) {
    throw new Error('Insufficient funds');
  }

  // Get ACH numbers and initiate transfer
  const authResponse = await plaidClient.authGet({
    access_token: accessToken,
  });

  const achNumbers = authResponse.data.numbers.ach.find(
    n => n.account_id === account.account_id
  );

  // Initiate ACH transfer with your payment processor
  return await initiateACHTransfer({
    routingNumber: achNumbers.routing,
    accountNumber: achNumbers.account,
    amount,
    accountType: account.subtype,
  });
}

### 上下文

- ACH 转账
- 资金移动
- 账户注资

### 实时余额查询

使用 /accounts/balance/get 获取实时余额（付费端点）。
/accounts/get 返回缓存数据，适合展示但不适合实时决策。

interface BalanceInfo {
  accountId: string;
  available: number | null;
  current: number;
  limit: number | null;
  isoCurrencyCode: string;
  lastUpdated: Date;
  isRealtime: boolean;
}

// Get cached balance (free, suitable for display)
async function getCachedBalances(accessToken: string): Promise<BalanceInfo[]> {
  const response = await plaidClient.accountsGet({
    access_token: accessToken,
  });

  return response.data.accounts.map(account => ({
    accountId: account.account_id,
    available: account.balances.available,
    current: account.balances.current,
    limit: account.balances.limit,
    isoCurrencyCode: account.balances.iso_currency_code || 'USD',
    lastUpdated: new Date(account.balances.last_updated_datetime || Date.now()),
    isRealtime: false,
  }));
}

// Get real-time balance (paid, for payment validation)
async function getRealTimeBalance(
  accessToken: string,
  accountIds?: string[]
): Promise<BalanceInfo[]> {
  const response = await plaidClient.accountsBalanceGet({
    access_token: accessToken,
    options: accountIds ? { account_ids: accountIds } : undefined,
  });

  return response.data.accounts.map(account => ({
    accountId: account.account_id,
    available: account.balances.available,
    current: account.balances.current,
    limit: account.balances.limit,
    isoCurrencyCode: account.balances.iso_currency_code || 'USD',
    lastUpdated: new Date(),
    isRealtime: true,
  }));
}

// Payment validation with balance check
async function validatePayment(
  accessToken: string,
  accountId: string,
  amount: number
): Promise<PaymentValidation> {
  const balances = await getRealTimeBalance(accessToken, [accountId]);
  const account = balances.find(b => b.accountId === accountId);

  if (!account) {
    return { valid: false, reason: 'Account not found' };
  }

  const available = account.available ?? account.current;

  if (available < amount) {
    return {
      valid: false,
      reason: 'Insufficient funds',
      available,
      requested: amount,
    };
  }

  return {
    valid: true,
    available,
    requested: amount,
  };
}

### 上下文

- 余额查询
- 资金可用性
- 支付验证

### Webhook 验证

使用验证密钥端点验证 Plaid webhook。
以幂等方式处理重复 webhook，并设计为支持乱序送达。

import jwt from 'jsonwebtoken';
import jwksClient from 'jwks-rsa';

// Cache JWKS client
const client = jwksClient({
  jwksUri: 'https://production.plaid.com/.well-known/jwks.json',
  cache: true,
  cacheMaxAge: 86400000,  // 24 hours
});

async function getSigningKey(kid: string): Promise<string> {
  const key = await client.getSigningKey(kid);
  return key.getPublicKey();
}

async function verifyPlaidWebhook(req: Request): Promise<boolean> {
  const signedJwt = req.headers['plaid-verification'];

  if (!signedJwt) {
    return false;
  }

  try {
    // Decode to get kid
    const decoded = jwt.decode(signedJwt, { complete: true });
    if (!decoded?.header?.kid) {
      return false;
    }

    // Get signing key
    const key = await getSigningKey(decoded.header.kid);

    // Verify JWT
    const claims = jwt.verify(signedJwt, key, {
      algorithms: ['ES256'],
    }) as any;

    // Verify body hash
    const bodyHash = crypto
      .createHash('sha256')
      .update(JSON.stringify(req.body))
      .digest('hex');

    if (claims.request_body_sha256 !== bodyHash) {
      return false;
    }

    // Check timestamp (within 5 minutes)
    const issuedAt = new Date(claims.iat * 1000);
    const fiveMinutesAgo = new Date(Date.now() - 5 * 60 * 1000);
    if (issuedAt < fiveMinutesAgo) {
      return false;
    }

    return true;
  } catch (error) {
    console.error('Webhook verification failed:', error);
    return false;
  }
}

// Idempotent webhook handler
app.post('/api/plaid/webhooks', async (req, res) => {
  // Verify webhook signature
  if (!await verifyPlaidWebhook(req)) {
    return res.status(401).send('Invalid signature');
  }

  const { webhook_type, webhook_code, item_id } = req.body;

  // Create idempotency key
  const idempotencyKey = `${webhook_type}:${webhook_code}:${item_id}:${JSON.stringify(req.body)}`;
  const idempotencyHash = crypto.createHash('sha256').update(idempotencyKey).digest('hex');

  // Check if already processed
  const existing = await db.webhookLog.findUnique({
    where: { idempotencyHash },
  });

  if (existing) {
    console.log('Duplicate webhook, skipping:', idempotencyHash);
    return res.sendStatus(200);
  }

  // Record webhook before processing
  await db.webhookLog.create({
    data: {
      idempotencyHash,
      webhookType: webhook_type,
      webhookCode: webhook_code,
      itemId: item_id,
      payload: req.body,
      processedAt: new Date(),
    },
  });

  // Process webhook (async for quick response)
  processWebhookAsync(req.body).catch(console.error);

  res.sendStatus(200);
});

### 上下文

- webhook 安全
- 事件处理
- 生产部署

## 注意事项

### access_token 永不过期但极其敏感

严重级别：严重

### accounts/get 返回缓存余额，非实时数据

严重级别：高

### webhook 可能乱序到达或重复送达

严重级别：高

### Item 进入错误状态需要用户操作

严重级别：高

### Sandbox 无法反映生产环境复杂度

严重级别：中

### TRANSACTIONS_SYNC_MUTATION_DURING_PAGINATION 需要重启

严重级别：中

### Link Token 生命周期短且仅限一次使用

严重级别：中

### 周期性交易需要 180 天以上历史数据

严重级别：中

## 验证检查

### access_token 明文存储

严重级别：错误

Plaid access_token 必须加密存储

提示：Plaid access_token 似乎以明文存储，请加密存储。

### Plaid Secret 暴露在客户端代码中

严重级别：错误

Plaid secret 绝不能暴露给客户端

提示：Plaid secret 可能已暴露，请仅在服务端使用。

### Plaid 凭据硬编码

严重级别：错误

凭据必须使用环境变量

提示：Plaid 凭据被硬编码，请使用环境变量。

### 缺少 Webhook 签名验证

严重级别：错误

Plaid webhook 必须验证 JWT 签名

提示：webhook 处理程序缺少签名验证，请验证 Plaid-Verification header。

### 使用缓存余额进行支付决策

严重级别：错误

支付验证应使用实时余额

提示：使用 accountsGet（缓存）进行支付验证，请使用 accountsBalanceGet 获取实时余额。

### 缺少 Item 错误状态处理

严重级别：警告

API 调用应处理 ITEM_LOGIN_REQUIRED

提示：API 调用未处理 ITEM_LOGIN_REQUIRED，请处理 item 错误状态。

### 轮询交易而非使用 Webhook

严重级别：警告

应使用 webhook 获取交易更新

提示：正在轮询交易，请配置 webhook 监听 SYNC_UPDATES_AVAILABLE。

### Link Token 被缓存或复用

严重级别：警告

Link token 仅限一次使用，4 小时后过期

提示：Link token 不应被缓存，请为每次会话创建新的 token。

### 使用已废弃的 Public Key

严重级别：错误

Public Key 集成已于 2025 年 1 月终止

提示：Public Key 已废弃，请改用 Link token。

### 交易同步未存储 Cursor

严重级别：警告

存储 cursor 以支持增量同步

提示：交易同步未持久化 cursor，请存储 cursor 以支持增量同步。

## 协作

### 委派触发条件

- 用户需要支付处理 -> stripe-integration（Stripe 处理实际支付，Plaid 处理账户关联）
- 用户需要预算功能 -> analytics-specialist（交易分类与分析）
- 用户需要投资追踪 -> data-engineer（投资组合分析与报告）
- 用户需要合规/审计 -> security-specialist（SOC 2、PCI 合规）
- 用户需要移动应用 -> mobile-developer（React Native Plaid SDK）

## 使用场景
- 用户提及或暗示：plaid
- 用户提及或暗示：银行账户关联
- 用户提及或暗示：银行连接
- 用户提及或暗示：ach
- 用户提及或暗示：账户聚合
- 用户提及或暗示：银行交易
- 用户提及或暗示：开放银行
- 用户提及或暗示：金融科技
- 用户提及或暗示：银行身份验证

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。