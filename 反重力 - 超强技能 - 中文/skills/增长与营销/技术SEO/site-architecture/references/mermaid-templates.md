# Mermaid 图表模板

可直接复制粘贴的 Mermaid 图表，用于可视化站点地图。根据您的网站自定义节点标签和连接。

---

## 基础层级结构

简单的自上而下页面层级。

```mermaid
graph TD
    HOME["Homepage<br/>/"] --> FEAT["Features<br/>/features"]
    HOME --> PRICE["Pricing<br/>/pricing"]
    HOME --> BLOG["Blog<br/>/blog"]
    HOME --> ABOUT["About<br/>/about"]

    FEAT --> F1["Analytics<br/>/features/analytics"]
    FEAT --> F2["Automation<br/>/features/automation"]
    FEAT --> F3["Integrations<br/>/features/integrations"]

    BLOG --> B1["Post: SEO Guide<br/>/blog/seo-guide"]
    BLOG --> B2["Post: CRO Tips<br/>/blog/cro-tips"]
```

---

## 带导航区域的层级结构

使用子图显示哪些页面出现在哪个导航区域。

```mermaid
graph TD
    subgraph "Header Nav"
        HOME["Homepage"]
        FEAT["Features"]
        PRICE["Pricing"]
        BLOG["Blog"]
        CTA["Get Started ★"]
    end

    subgraph "Feature Pages"
        F1["Analytics"]
        F2["Automation"]
        F3["Integrations"]
    end

    subgraph "Footer Nav"
        ABOUT["About"]
        CAREERS["Careers"]
        CONTACT["Contact"]
        PRIVACY["Privacy"]
        TERMS["Terms"]
    end

    HOME --> FEAT
    HOME --> PRICE
    HOME --> BLOG
    FEAT --> F1
    FEAT --> F2
    FEAT --> F3
    HOME --> ABOUT
    ABOUT --> CAREERS
    HOME --> CONTACT
```

---

## 带 URL 标签的层级结构

每个节点显示页面名称和 URL 路径。

```mermaid
graph TD
    HOME["Homepage<br/><small>/</small>"] --> PROD["Product<br/><small>/product</small>"]
    HOME --> PRICE["Pricing<br/><small>/pricing</small>"]
    HOME --> BLOG["Blog<br/><small>/blog</small>"]
    HOME --> DOCS["Docs<br/><small>/docs</small>"]
    HOME --> ABOUT["About<br/><small>/about</small>"]

    PROD --> P1["Analytics<br/><small>/product/analytics</small>"]
    PROD --> P2["Reports<br/><small>/product/reports</small>"]

    DOCS --> D1["Getting Started<br/><small>/docs/getting-started</small>"]
    DOCS --> D2["API Reference<br/><small>/docs/api</small>"]
```

---

## 中心辐射内容模型

显示一个中心页面连接到辐射文章，辐射文章之间相互链接。

```mermaid
graph TD
    HUB["SEO Guide<br/>(Hub Page)"]

    HUB --> S1["Keyword Research"]
    HUB --> S2["On-Page SEO"]
    HUB --> S3["Technical SEO"]
    HUB --> S4["Link Building"]

    S1 -.-> S2
    S2 -.-> S3
    S3 -.-> S4

    style HUB fill:#f9f,stroke:#333,stroke-width:2px
```

图例：
- 实线 = 主要中心辐射链接
- 虚线 = 辐射之间的交叉链接

---

## 内部链接流

显示不同网站部分如何相互链接。

```mermaid
graph LR
    subgraph "Marketing"
        HOME["Homepage"]
        FEAT["Features"]
        PRICE["Pricing"]
    end

    subgraph "Content"
        BLOG["Blog"]
        GUIDE["Guides"]
        CASE["Case Studies"]
    end

    subgraph "Product"
        DOCS["Docs"]
        API["API Ref"]
        CHANGE["Changelog"]
    end

    BLOG --> FEAT
    BLOG --> CASE
    CASE --> FEAT
    CASE --> PRICE
    FEAT --> DOCS
    GUIDE --> BLOG
    GUIDE --> DOCS
    HOME --> FEAT
    HOME --> BLOG
    HOME --> CASE
```

---

## 重构前后对比

并排比较当前和提议的网站结构。

```mermaid
graph TD
    subgraph "Before"
        B_HOME["Homepage"] --> B_P1["Page 1"]
        B_HOME --> B_P2["Page 2"]
        B_HOME --> B_P3["Page 3"]
        B_HOME --> B_P4["Page 4"]
        B_HOME --> B_P5["Page 5"]
        B_HOME --> B_P6["Page 6"]
        B_HOME --> B_P7["Page 7"]
        B_HOME --> B_P8["Page 8"]
    end

    subgraph "After"
        A_HOME["Homepage"] --> A_S1["Features"]
        A_HOME --> A_S2["Resources"]
        A_HOME --> A_S3["Company"]
        A_S1 --> A_P1["Feature A"]
        A_S1 --> A_P2["Feature B"]
        A_S2 --> A_P3["Blog"]
        A_S2 --> A_P4["Guides"]
        A_S3 --> A_P5["About"]
        A_S3 --> A_P6["Contact"]
    end
```

---

## 颜色编码约定

使用样式突出显示页面状态、优先级或类型。

```mermaid
graph TD
    HOME["Homepage"] --> FEAT["Features"]
    HOME --> PRICE["Pricing"]
    HOME --> BLOG["Blog"]
    HOME --> NEW["New Section"]
    HOME --> REMOVE["Deprecated Page"]

    FEAT --> F1["Existing Feature"]
    FEAT --> F2["New Feature"]

    style HOME fill:#4CAF50,color:#fff
    style PRICE fill:#4CAF50,color:#fff
    style FEAT fill:#4CAF50,color:#fff
    style BLOG fill:#4CAF50,color:#fff
    style F1 fill:#4CAF50,color:#fff
    style NEW fill:#2196F3,color:#fff
    style F2 fill:#2196F3,color:#fff
    style REMOVE fill:#f44336,color:#fff
```

颜色说明：
- **绿色** (`#4CAF50`)：现有页面（无更改）
- **蓝色** (`#2196F3`)：需要创建的新页面
- **红色** (`#f44336`)：需要删除或重定向的页面
- **黄色** (`#FFC107`)：需要重构或移动的页面
- **紫色** (`#9C27B0`)：高优先级 / CTA 页面