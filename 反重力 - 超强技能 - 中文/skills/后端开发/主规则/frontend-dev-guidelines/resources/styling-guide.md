# 样式指南

使用 MUI v7 sx prop、内联样式和主题集成的现代样式模式。

---

## 内联样式 vs 独立样式

### 决策阈值

**<100 行：在组件顶部使用内联样式**

```typescript
import type { SxProps, Theme } from '@mui/material';

const componentStyles: Record<string, SxProps<Theme>> = {
    container: {
        p: 2,
        display: 'flex',
        flexDirection: 'column',
    },
    header: {
        mb: 2,
        borderBottom: '1px solid',
        borderColor: 'divider',
    },
    // ... more styles
};

export const MyComponent: React.FC = () => {
    return (
        <Box sx={componentStyles.container}>
            <Box sx={componentStyles.header}>
                <h2>Title</h2>
            </Box>
        </Box>
    );
};
```

**>100 行：使用独立的 `.styles.ts` 文件**

```typescript
// MyComponent.styles.ts
import type { SxProps, Theme } from '@mui/material';

export const componentStyles: Record<string, SxProps<Theme>> = {
    container: { ... },
    header: { ... },
    // ... 100+ lines of styles
};

// MyComponent.tsx
import { componentStyles } from './MyComponent.styles';

export const MyComponent: React.FC = () => {
    return <Box sx={componentStyles.container}>...</Box>;
};
```

### 实际示例：UnifiedForm.tsx

**第 48-126 行**：78 行内联样式（可接受）

```typescript
const formStyles: Record<string, SxProps<Theme>> = {
    gridContainer: {
        height: '100%',
        maxHeight: 'calc(100vh - 220px)',
    },
    section: {
        height: '100%',
        maxHeight: 'calc(100vh - 220px)',
        overflow: 'auto',
        p: 4,
    },
    // ... 15 more style objects
};
```

**指导原则**：约 80 行内联样式是可接受的。在接近 100 行时根据实际情况判断。

---

## sx Prop 模式

### 基本用法

```typescript
<Box sx={{ p: 2, mb: 3, display: 'flex' }}>
    Content
</Box>
```

### 使用主题访问

```typescript
<Box
    sx={{
        p: 2,
        backgroundColor: (theme) => theme.palette.primary.main,
        color: (theme) => theme.palette.primary.contrastText,
        borderRadius: (theme) => theme.shape.borderRadius,
    }}
>
    Themed Box
</Box>
```

### 响应式样式

```typescript
<Box
    sx={{
        p: { xs: 1, sm: 2, md: 3 },
        width: { xs: '100%', md: '50%' },
        flexDirection: { xs: 'column', md: 'row' },
    }}
>
    Responsive Layout
</Box>
```

### 伪选择器

```typescript
<Box
    sx={{
        p: 2,
        '&:hover': {
            backgroundColor: 'rgba(0,0,0,0.05)',
        },
        '&:active': {
            backgroundColor: 'rgba(0,0,0,0.1)',
        },
        '& .child-class': {
            color: 'primary.main',
        },
    }}
>
    Interactive Box
</Box>
```

---

## MUI v7 模式

### Grid 组件（v7 语法）

```typescript
import { Grid } from '@mui/material';

// ✅ CORRECT - v7 syntax with size prop
<Grid container spacing={2}>
    <Grid size={{ xs: 12, md: 6 }}>
        Left Column
    </Grid>
    <Grid size={{ xs: 12, md: 6 }}>
        Right Column
    </Grid>
</Grid>

// ❌ WRONG - Old v6 syntax
<Grid container spacing={2}>
    <Grid xs={12} md={6}>  {/* OLD - Don't use */}
        Content
    </Grid>
</Grid>
```

**关键变更**：使用 `size={{ xs: 12, md: 6 }}` 替代 `xs={12} md={6}`

### 响应式 Grid

```typescript
<Grid container spacing={3}>
    <Grid size={{ xs: 12, sm: 6, md: 4, lg: 3 }}>
        Responsive Column
    </Grid>
</Grid>
```

### 嵌套 Grid

```typescript
<Grid container spacing={2}>
    <Grid size={{ xs: 12, md: 8 }}>
        <Grid container spacing={1}>
            <Grid size={{ xs: 12, sm: 6 }}>
                Nested 1
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
                Nested 2
            </Grid>
        </Grid>
    </Grid>

    <Grid size={{ xs: 12, md: 4 }}>
        Sidebar
    </Grid>
</Grid>
```

---

## 类型安全的样式

### 样式对象类型

```typescript
import type { SxProps, Theme } from '@mui/material';

// Type-safe styles
const styles: Record<string, SxProps<Theme>> = {
    container: {
        p: 2,
        // Autocomplete and type checking work here
    },
};

// Or individual style
const containerStyle: SxProps<Theme> = {
    p: 2,
    display: 'flex',
};
```

### 主题感知样式

```typescript
const styles: Record<string, SxProps<Theme>> = {
    primary: {
        color: (theme) => theme.palette.primary.main,
        backgroundColor: (theme) => theme.palette.primary.light,
        '&:hover': {
            backgroundColor: (theme) => theme.palette.primary.dark,
        },
    },
    customSpacing: {
        padding: (theme) => theme.spacing(2),
        margin: (theme) => theme.spacing(1, 2), // top/bottom: 1, left/right: 2
    },
};
```

---

## 不应使用的模式

### ❌ makeStyles（MUI v4 模式）

```typescript
// ❌ AVOID - Old Material-UI v4 pattern
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles((theme) => ({
    root: {
        padding: theme.spacing(2),
    },
}));
```

**避免原因**：已弃用，v7 对其支持不佳

### ❌ styled() 组件

```typescript
// ❌ AVOID - styled-components pattern
import { styled } from '@mui/material/styles';

const StyledBox = styled(Box)(({ theme }) => ({
    padding: theme.spacing(2),
}));
```

**避免原因**：sx prop 更灵活，且不会创建新组件

### ✅ 改用 sx Prop

```typescript
// ✅ PREFERRED
<Box
    sx={{
        p: 2,
        backgroundColor: 'primary.main',
    }}
>
    Content
</Box>
```

---

## 代码风格规范

### 缩进

**4 个空格**（不是 2 个，不是制表符）

```typescript
const styles: Record<string, SxProps<Theme>> = {
    container: {
        p: 2,
        display: 'flex',
        flexDirection: 'column',
    },
};
```

### 引号

字符串使用**单引号**（项目标准）

```typescript
// ✅ CORRECT
const color = 'primary.main';
import { Box } from '@mui/material';

// ❌ WRONG
const color = "primary.main";
import { Box } from "@mui/material";
```

### 尾随逗号

在对象和数组中**始终使用尾随逗号**

```typescript
// ✅ CORRECT
const styles = {
    container: { p: 2 },
    header: { mb: 1 },  // Trailing comma
};

const items = [
    'item1',
    'item2',  // Trailing comma
];

// ❌ WRONG - No trailing comma
const styles = {
    container: { p: 2 },
    header: { mb: 1 }  // Missing comma
};
```

---

## 常见样式模式

### Flexbox 布局

```typescript
const styles = {
    flexRow: {
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        gap: 2,
    },
    flexColumn: {
        display: 'flex',
        flexDirection: 'column',
        gap: 1,
    },
    spaceBetween: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
};
```

### 间距

```typescript
// Padding
p: 2           // All sides
px: 2          // Horizontal (left + right)
py: 2          // Vertical (top + bottom)
pt: 2, pr: 1   // Specific sides

// Margin
m: 2, mx: 2, my: 2, mt: 2, mr: 1

// Units: 1 = 8px (theme.spacing(1))
p: 2  // = 16px
p: 0.5  // = 4px
```

### 定位

```typescript
const styles = {
    relative: {
        position: 'relative',
    },
    absolute: {
        position: 'absolute',
        top: 0,
        right: 0,
    },
    sticky: {
        position: 'sticky',
        top: 0,
        zIndex: 1000,
    },
};
```

---

## 总结

**样式清单：**
- ✅ 使用 `sx` prop 进行 MUI 样式设置
- ✅ 使用 `SxProps<Theme>` 实现类型安全
- ✅ <100 行使用内联样式；>100 行使用独立文件
- ✅ MUI v7 Grid：`size={{ xs: 12 }}`
- ✅ 4 空格缩进
- ✅ 单引号
- ✅ 尾随逗号
- ❌ 不使用 makeStyles 或 styled()

**另请参阅：**
- [component-patterns.md](component-patterns.md) - 组件结构
- [complete-examples.md](complete-examples.md) - 完整样式示例
