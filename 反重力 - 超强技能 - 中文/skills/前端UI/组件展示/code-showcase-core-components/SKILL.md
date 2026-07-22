---
name: code-showcase-core-components
description: 核心组件库与设计系统模式。在构建 UI、使用设计令牌或操作组件库时使用。触发词：核心组件、设计令牌、组件库、设计系统、UI 构建、design tokens、core components、design system、组件模式、token props。
risk: unknown
source: https://github.com/ChrisWiles/claude-code-showcase/tree/main/.claude/skills/core-components
source_repo: ChrisWiles/claude-code-showcase
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/ChrisWiles/claude-code-showcase/blob/main/LICENSE
---

# 核心组件
## 使用时机

当你需要核心组件库和设计系统模式时使用本技能。在构建 UI、使用设计令牌或操作组件库时调用。


## 设计系统概览

应使用核心库中的组件，而不是直接使用底层平台组件。这能保证样式和行为的一致性。

## 设计令牌

**严禁硬编码数值。始终使用设计令牌。**

### 间距令牌

```tsx
// 正确 - 使用令牌
<Box padding="$4" marginBottom="$2" />

// 错误 - 硬编码数值
<Box padding={16} marginBottom={8} />
```

| 令牌 | 数值 |
|-------|-------|
| `$1` | 4px |
| `$2` | 8px |
| `$3` | 12px |
| `$4` | 16px |
| `$6` | 24px |
| `$8` | 32px |

### 颜色令牌

```tsx
// 正确 - 语义化令牌
<Text color="$textPrimary" />
<Box backgroundColor="$backgroundSecondary" />

// 错误 - 硬编码颜色
<Text color="#333333" />
<Box backgroundColor="rgb(245, 245, 245)" />
```

| 语义令牌 | 用途 |
|----------------|---------|
| `$textPrimary` | 主要文本 |
| `$textSecondary` | 次要文本 |
| `$textTertiary` | 禁用/提示文本 |
| `$primary500` | 品牌/强调色 |
| `$statusError` | 错误状态 |
| `$statusSuccess` | 成功状态 |

### 排版令牌

```tsx
<Text fontSize="$lg" fontWeight="$semibold" />
```

| 令牌 | 尺寸 |
|-------|------|
| `$xs` | 12px |
| `$sm` | 14px |
| `$md` | 16px |
| `$lg` | 18px |
| `$xl` | 20px |
| `$2xl` | 24px |

## 核心组件

### Box

带令牌支持的基础布局组件：

```tsx
<Box
  padding="$4"
  backgroundColor="$backgroundPrimary"
  borderRadius="$lg"
>
  {children}
</Box>
```

### HStack / VStack

水平和垂直方向的弹性布局：

```tsx
<HStack gap="$3" alignItems="center">
  <Icon name="user" />
  <Text>Username</Text>
</HStack>

<VStack gap="$4" padding="$4">
  <Heading>Title</Heading>
  <Text>Content</Text>
</VStack>
```

### Text

支持令牌的排版组件：

```tsx
<Text
  fontSize="$lg"
  fontWeight="$semibold"
  color="$textPrimary"
>
  Hello World
</Text>
```

### Button

支持多种变体的可交互按钮：

```tsx
<Button
  onPress={handlePress}
  variant="solid"
  size="md"
  isLoading={loading}
  isDisabled={disabled}
>
  Click Me
</Button>
```

| 变体 | 用途 |
|---------|---------|
| `solid` | 主要操作 |
| `outline` | 次要操作 |
| `ghost` | 第三级/弱化操作 |
| `link` | 行内操作 |

### Input

带校验功能的表单输入框：

```tsx
<Input
  value={value}
  onChangeText={setValue}
  placeholder="Enter text"
  error={touched ? errors.field : undefined}
  label="Field Name"
/>
```

### Card

内容容器组件：

```tsx
<Card padding="$4" gap="$3">
  <CardHeader>
    <Heading size="sm">Card Title</Heading>
  </CardHeader>
  <CardBody>
    <Text>Card content</Text>
  </CardBody>
</Card>
```

## 布局模式

### 页面布局

```tsx
const MyScreen = () => (
  <Screen>
    <ScreenHeader title="Page Title" />
    <ScreenContent padding="$4">
      {/* 内容 */}
    </ScreenContent>
  </Screen>
);
```

### 表单布局

```tsx
<VStack gap="$4" padding="$4">
  <Input label="Name" {...nameProps} />
  <Input label="Email" {...emailProps} />
  <Button isLoading={loading}>Submit</Button>
</VStack>
```

### 列表项布局

```tsx
<HStack
  padding="$4"
  gap="$3"
  alignItems="center"
  borderBottomWidth={1}
  borderColor="$borderLight"
>
  <Avatar source={{ uri: imageUrl }} size="md" />
  <VStack flex={1}>
    <Text fontWeight="$semibold">{title}</Text>
    <Text color="$textSecondary" fontSize="$sm">{subtitle}</Text>
  </VStack>
  <Icon name="chevron-right" color="$textTertiary" />
</HStack>
```

## 反模式

```tsx
// 错误 - 硬编码数值
<View style={{ padding: 16, backgroundColor: '#fff' }}>

// 正确 - 设计令牌
<Box padding="$4" backgroundColor="$backgroundPrimary">


// 错误 - 直接使用底层平台组件
import { View, Text } from 'react-native';

// 正确 - 核心组件
import { Box, Text } from 'components/core';


//// 错误 - 内联样式
<Text style={{ fontSize: 18, fontWeight: '600' }}>

// 正确 - 令牌属性
<Text fontSize="$lg" fontWeight="$semibold">
```

## 组件属性模式

创建组件时，应使用基于令牌的属性：

```tsx
interface CardProps {
  padding?: '$2' | '$4' | '$6';
  variant?: 'elevated' | 'outlined' | 'filled';
  children: React.ReactNode;
}

const Card = ({ padding = '$4', variant = 'elevated', children }: CardProps) => (
  <Box
    padding={padding}
    backgroundColor="$backgroundPrimary"
    borderRadius="$lg"
    {...variantStyles[variant]}
  >
    {children}
  </Box>
);
```

## 与其他技能的集成

- **react-ui-patterns**：使用核心组件处理 UI 状态
- **testing-patterns**：在测试中模拟核心组件
- **storybook**：记录组件变体

## 限制

- 仅当任务与上游来源及本地项目上下文明确匹配时使用本技能。
- 在应用更改前，请验证命令、生成的代码、依赖、凭据以及外部服务的行为。
- 不要将示例视为环境特定测试、安全审查或针对破坏性/高成本操作的用户授权的替代。