# 扩展参考

构建 UI 扩展和 Shopify Functions 的指南。

## 结账 UI 扩展

使用原生渲染组件自定义结账和感谢页面。

### 扩展点

**块级目标（商家可配置）：**

- `purchase.checkout.block.render` - 主结账页
- `purchase.thank-you.block.render` - 感谢页面

**静态目标（固定位置）：**

- `purchase.checkout.header.render-after`
- `purchase.checkout.contact.render-before`
- `purchase.checkout.shipping-option-list.render-after`
- `purchase.checkout.payment-method-list.render-after`
- `purchase.checkout.footer.render-before`

### 设置

```bash
shopify app generate extension --type checkout_ui_extension
```

配置（`shopify.extension.toml`）：

```toml
api_version = "2026-01"
name = "gift-message"
type = "ui_extension"

[[extensions.targeting]]
target = "purchase.checkout.block.render"

[capabilities]
network_access = true
api_access = true
```

### 基础示例

```javascript
import {
  reactExtension,
  BlockStack,
  TextField,
  Checkbox,
  useApi,
} from "@shopify/ui-extensions-react/checkout";

export default reactExtension("purchase.checkout.block.render", () => (
  <Extension />
));

function Extension() {
  const [message, setMessage] = useState("");
  const [isGift, setIsGift] = useState(false);
  const { applyAttributeChange } = useApi();

  useEffect(() => {
    if (isGift) {
      applyAttributeChange({
        type: "updateAttribute",
        key: "gift_message",
        value: message,
      });
    }
  }, [message, isGift]);

  return (
    <BlockStack spacing="loose">
      <Checkbox checked={isGift} onChange={setIsGift}>
        This is a gift
      </Checkbox>
      {isGift && (
        <TextField
          label="Gift Message"
          value={message}
          onChange={setMessage}
          multiline={3}
        />
      )}
    </BlockStack>
  );
}
```

### 常用 Hooks

**useApi：**

```javascript
const { extensionPoint, shop, storefront, i18n, sessionToken } = useApi();
```

**useCartLines：**

```javascript
const lines = useCartLines();
lines.forEach((line) => {
  console.log(line.merchandise.product.title, line.quantity);
});
```

**useShippingAddress：**

```javascript
const address = useShippingAddress();
console.log(address.city, address.countryCode);
```

**useApplyCartLinesChange：**

```javascript
const applyChange = useApplyCartLinesChange();

async function addItem() {
  await applyChange({
    type: "addCartLine",
    merchandiseId: "gid://shopify/ProductVariant/123",
    quantity: 1,
  });
}
```

### 核心组件

**布局：**

- `BlockStack` - 垂直堆叠
- `InlineStack` - 水平布局
- `Grid`, `GridItem` - 网格布局
- `View` - 容器
- `Divider` - 分隔线

**输入：**

- `TextField` - 文本输入
- `Checkbox` - 布尔值
- `Select` - 下拉选择
- `DatePicker` - 日期选择
- `Form` - 表单容器

**展示：**

- `Text`, `Heading` - 排版
- `Banner` - 消息横幅
- `Badge` - 状态标记
- `Image` - 图片
- `Link` - 超链接
- `List`, `ListItem` - 列表

**交互：**

- `Button` - 操作按钮
- `Modal` - 弹窗
- `Pressable` - 可点击区域

## 管理后台 UI 扩展

扩展 Shopify 管理后台界面。

### 管理后台操作

资源页面上的自定义操作。

```bash
shopify app generate extension --type admin_action
```

```javascript
import {
  reactExtension,
  AdminAction,
  Button,
} from "@shopify/ui-extensions-react/admin";

export default reactExtension("admin.product-details.action.render", () => (
  <Extension />
));

function Extension() {
  const { data } = useData();

  async function handleExport() {
    const response = await fetch("/api/export", {
      method: "POST",
      body: JSON.stringify({ productId: data.product.id }),
    });
    console.log("Exported:", await response.json());
  }

  return (
    <AdminAction
      title="Export Product"
      primaryAction={<Button onPress={handleExport}>Export</Button>}
    />
  );
}
```

**目标：**

- `admin.product-details.action.render`
- `admin.order-details.action.render`
- `admin.customer-details.action.render`

### 管理后台块

管理后台页面中的嵌入内容。

```javascript
import {
  reactExtension,
  BlockStack,
  Text,
  Badge,
} from "@shopify/ui-extensions-react/admin";

export default reactExtension("admin.product-details.block.render", () => (
  <Extension />
));

function Extension() {
  const { data } = useData();
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    fetchAnalytics(data.product.id).then(setAnalytics);
  }, []);

  return (
    <BlockStack>
      <Text variant="headingMd">Product Analytics</Text>
      <Text>Views: {analytics?.views || 0}</Text>
      <Text>Conversions: {analytics?.conversions || 0}</Text>
      <Badge tone={analytics?.trending ? "success" : "info"}>
        {analytics?.trending ? "Trending" : "Normal"}
      </Badge>
    </BlockStack>
  );
}
```

**目标：**

- `admin.product-details.block.render`
- `admin.order-details.block.render`
- `admin.customer-details.block.render`

## POS UI 扩展

自定义销售点（POS）体验。

### 智能网格磁贴

POS 主屏幕上的快捷操作。

```javascript
import {
  reactExtension,
  SmartGridTile,
} from "@shopify/ui-extensions-react/pos";

export default reactExtension("pos.home.tile.render", () => <Extension />);

function Extension() {
  function handlePress() {
    // 导航到自定义工作流
  }

  return (
    <SmartGridTile
      title="Gift Cards"
      subtitle="Manage gift cards"
      onPress={handlePress}
    />
  );
}
```

### POS 弹窗

全屏工作流。

```javascript
import {
  reactExtension,
  Screen,
  BlockStack,
  Button,
  TextField,
} from "@shopify/ui-extensions-react/pos";

export default reactExtension("pos.home.modal.render", () => <Extension />);

function Extension() {
  const { navigation } = useApi();
  const [amount, setAmount] = useState("");

  function handleIssue() {
    // 发行礼品卡
    navigation.pop();
  }

  return (
    <Screen name="Gift Card" title="Issue Gift Card">
      <BlockStack>
        <TextField label="Amount" value={amount} onChange={setAmount} />
        <TextField label="Recipient Email" />
        <Button onPress={handleIssue}>Issue</Button>
      </BlockStack>
    </Screen>
  );
}
```

## 客户账户扩展

自定义客户账户页面。

### 订单状态扩展

```javascript
import {
  reactExtension,
  BlockStack,
  Text,
  Button,
} from "@shopify/ui-extensions-react/customer-account";

export default reactExtension(
  "customer-account.order-status.block.render",
  () => <Extension />,
);

function Extension() {
  const { order } = useApi();

  function handleReturn() {
    // 发起退货
  }

  return (
    <BlockStack>
      <Text variant="headingMd">Need to return?</Text>
      <Text>Start return for order {order.name}</Text>
      <Button onPress={handleReturn}>Start Return</Button>
    </BlockStack>
  );
}
```

**目标：**

- `customer-account.order-status.block.render`
- `customer-account.order-index.block.render`
- `customer-account.profile.block.render`

## Shopify Functions

无服务器后端自定义。

### 函数类型

**折扣：**

- `order_discount` - 订单级折扣
- `product_discount` - 特定产品折扣
- `shipping_discount` - 运费折扣

**支付自定义：**

- 隐藏/重命名/重排支付方式

**配送自定义：**

- 自定义配送选项
- 配送规则

**验证：**

- 购物车验证规则
- 结账验证

### 创建函数

```bash
shopify app generate extension --type function
```

### 订单折扣函数

```javascript
// input.graphql
query Input {
  cart {
    lines {
      quantity
      merchandise {
        ... on ProductVariant {
          product {
            hasTag(tag: "bulk-discount")
          }
        }
      }
    }
  }
}

// function.js
export default function orderDiscount(input) {
  const targets = input.cart.lines
    .filter(line => line.merchandise.product.hasTag)
    .map(line => ({
      productVariant: { id: line.merchandise.id }
    }));

  if (targets.length === 0) {
    return { discounts: [] };
  }

  return {
    discounts: [{
      targets,
      value: {
        percentage: {
          value: 10  // 10% 折扣
        }
      }
    }]
  };
}
```

### 支付自定义函数

```javascript
export default function paymentCustomization(input) {
  const hidePaymentMethods = input.cart.lines.some(
    (line) => line.merchandise.product.hasTag,
  );

  if (!hidePaymentMethods) {
    return { operations: [] };
  }

  return {
    operations: [
      {
        hide: {
          paymentMethodId: "gid://shopify/PaymentMethod/123",
        },
      },
    ],
  };
}
```

### 验证函数

```javascript
export default function cartValidation(input) {
  const errors = [];

  // 每单最多 5 件商品
  if (input.cart.lines.length > 5) {
    errors.push({
      localizedMessage: "Maximum 5 items allowed per order",
      target: "cart",
    });
  }

  // 批发最低 $50
  const isWholesale = input.cart.lines.some(
    (line) => line.merchandise.product.hasTag,
  );

  if (isWholesale && input.cart.cost.totalAmount.amount < 50) {
    errors.push({
      localizedMessage: "Wholesale orders require $50 minimum",
      target: "cart",
    });
  }

  return { errors };
}
```

## 网络请求

扩展可以调用外部 API。

```javascript
import { useApi } from "@shopify/ui-extensions-react/checkout";

function Extension() {
  const { sessionToken } = useApi();

  async function fetchData() {
    const token = await sessionToken.get();

    const response = await fetch("https://your-app.com/api/data", {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    return await response.json();
  }
}
```

## 最佳实践

**性能：**

- 懒加载数据
- 缓存昂贵计算的结果
- 使用加载状态
- 最小化重新渲染

**用户体验：**

- 提供清晰的错误消息
- 显示加载指示器
- 验证输入
- 支持键盘导航

**安全：**

- 在后端验证会话令牌
- 清理用户输入
- 所有请求使用 HTTPS
- 不要暴露敏感数据

**测试：**

- 在开发商店上测试
- 验证移动端/桌面端
- 检查无障碍性
- 测试边界情况

## 资源

- 结账扩展：https://shopify.dev/docs/api/checkout-extensions
- 管理后台扩展：https://shopify.dev/docs/apps/admin/extensions
- Functions：https://shopify.dev/docs/apps/functions
- 组件：https://shopify.dev/docs/api/checkout-ui-extensions/components
