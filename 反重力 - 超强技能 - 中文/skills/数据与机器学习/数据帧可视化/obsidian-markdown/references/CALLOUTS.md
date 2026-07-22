# 标注参考

## 基本标注

```markdown
> [!note]
> This is a note callout.

> [!info] Custom Title
> This callout has a custom title.

> [!tip] Title Only
```

## 可折叠标注

```markdown
> [!faq]- Collapsed by default
> This content is hidden until expanded.

> [!faq]+ Expanded by default
> This content is visible but can be collapsed.
```

## 嵌套标注

```markdown
> [!question] Outer callout
> > [!note] Inner callout
> > Nested content
```

## 支持的标注类型

| 类型 | 别名 | 颜色 / 图标 |
|------|------|-------------|
| `note` | - | 蓝色，铅笔 |
| `abstract` | `summary`, `tldr` | 青色，剪贴板 |
| `info` | - | 蓝色，信息 |
| `todo` | - | 蓝色，复选框 |
| `tip` | `hint`, `important` | 青色，火焰 |
| `success` | `check`, `done` | 绿色，对勾 |
| `question` | `help`, `faq` | 黄色，问号 |
| `warning` | `caution`, `attention` | 橙色，警告 |
| `failure` | `fail`, `missing` | 红色，X |
| `danger` | `error` | 红色，闪电 |
| `bug` | - | 红色，虫子 |
| `example` | - | 紫色，列表 |
| `quote` | `cite` | 灰色，引用 |

## 自定义标注（CSS）

```css
.callout[data-callout="custom-type"] {
  --callout-color: 255, 0, 0;
  --callout-icon: lucide-alert-circle;
}
```
