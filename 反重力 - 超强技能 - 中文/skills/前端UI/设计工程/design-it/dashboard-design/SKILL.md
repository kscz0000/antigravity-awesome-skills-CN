---
name: dashboard-design
description: Dashboard Design 的 Web 与 App 实现指南。当用户需要分析导向布局、数据可视化和模块化概览界面时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Dashboard Design

> "数据一览。有序、易扫读、高度实用。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **模块化网格**：屏幕被拆解为功能性的"小部件"或卡片。通常左侧有侧边栏，顶部有导航栏。
2. **数据层级**：最重要的数字（KPI）大而显眼，通常位于顶部。图表占据中部，列表/表格在底部。
3. **柔和背景**：柔和的灰色或近白色背景，让白色数据卡片清晰地凸显出来。

## 视觉 DNA
- **颜色**：**Minimalist Slate** 或 **Earth-Grounded Elegance**。避免使用过多颜色。严格使用红/绿色表示正/负趋势。
- **排版**：干净、表格化的无衬线字体（`Inter`、`Roboto Mono` 用于数字）。
- **样式**：极细微的阴影或 1px 边框来分隔卡片。

## Web 实现
- 使用 CSS Grid 处理宏观布局（侧边栏、头部、主体）。
- **CSS 示例**：
```css
body {
  background-color: #F8F9FA;
  color: #212529;
  font-family: 'Inter', sans-serif;
  margin: 0;
}

.dashboard-layout {
  display: grid;
  grid-template-columns: 250px 1fr;
  grid-template-rows: 70px 1fr;
  height: 100vh;
}

.sidebar {
  grid-row: 1 / 3;
  background-color: #ffffff;
  border-right: 1px solid #e9ecef;
  padding: 20px;
}

.header {
  background-color: #ffffff;
  border-bottom: 1px solid #e9ecef;
  padding: 0 30px;
  display: flex;
  align-items: center;
}

.main-content {
  padding: 30px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  overflow-y: auto;
}

/* KPI 卡片 */
.kpi-card {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  border: 1px solid #e9ecef;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

.kpi-title { font-size: 0.9rem; color: #6c757d; }
.kpi-value { font-size: 2rem; font-weight: 700; margin-top: 8px; }
.kpi-trend.positive { color: #28a745; }
```

## App 实现

### SwiftUI
```swift
struct DashboardView: View {
    // iPad/Mac 适用 NavigationSplitView
    // iPhone 使用滚动 VGrid
    let columns = [
        GridItem(.adaptive(minimum: 150), spacing: 16)
    ]
    
    var body: some View {
        NavigationView {
            ScrollView {
                LazyVGrid(columns: columns, spacing: 16) {
                    KPICard(title: "Revenue", value: "$45,231", trend: "+12.5%", isPositive: true)
                    KPICard(title: "Active Users", value: "2,405", trend: "+4.1%", isPositive: true)
                    KPICard(title: "Churn Rate", value: "1.2%", trend: "-0.4%", isPositive: false)
                    KPICard(title: "Avg. Session", value: "4m 12s", trend: "+0.1%", isPositive: true)
                }
                .padding()
                
                // 图表占位
                RoundedRectangle(cornerRadius: 12)
                    .fill(Color.white)
                    .frame(height: 250)
                    .overlay(Text("Chart Area").foregroundColor(.gray))
                    .padding(.horizontal)
            }
            .background(Color(UIColor.systemGroupedBackground))
            .navigationTitle("Overview")
        }
    }
}

struct KPICard: View {
    let title: String
    let value: String
    let trend: String
    let isPositive: Bool
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title).font(.subheadline).foregroundColor(.secondary)
            Text(value).font(.title2).fontWeight(.bold)
            Text(trend)
                .font(.caption)
                .fontWeight(.semibold)
                .foregroundColor(isPositive ? .green : .red)
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color.white)
        .cornerRadius(12)
        .shadow(color: Color.black.opacity(0.02), radius: 4, y: 2)
    }
}
```
- 仪表板需要 `.adaptive` 网格。`LazyVGrid` 在 iPad 上自动排列 4 个一行的卡片，在 iPhone 上自动变为 2 个一行。
- 使用 `Color(UIColor.systemGroupedBackground)` 提供与纯白卡片相对的微妙近白色对比。

### Flutter
```dart
class DashboardScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8F9FA),
      appBar: AppBar(
        title: const Text('Overview', style: TextStyle(color: Colors.black)),
        backgroundColor: Colors.white,
        elevation: 1,
      ),
      // 平板用 Row + NavigationRail，移动端用 Drawer
      drawer: const Drawer(), 
      body: CustomScrollView(
        slivers: [
          SliverPadding(
            padding: const EdgeInsets.all(16),
            sliver: SliverGrid.extent(
              maxCrossAxisExtent: 200, // 根据宽度自适应布局
              mainAxisSpacing: 16,
              crossAxisSpacing: 16,
              childAspectRatio: 1.5,
              children: [
                _buildKPI('Revenue', '\$45,231', '+12.5%', true),
                _buildKPI('Active Users', '2,405', '+4.1%', true),
                _buildKPI('Churn Rate', '1.2%', '-0.4%', false),
                _buildKPI('Avg. Session', '4m 12s', '+0.1%', true),
              ],
            ),
          ),
          SliverPadding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            sliver: SliverToBoxAdapter(
              child: Container(
                height: 250,
                decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12)),
                child: const Center(child: Text('Chart Area', style: TextStyle(color: Colors.grey))),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildKPI(String title, String value, String trend, bool isPositive) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey[200]!),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(title, style: const TextStyle(color: Colors.grey, fontSize: 14)),
          const SizedBox(height: 8),
          Text(value, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
          Text(trend, style: TextStyle(color: isPositive ? Colors.green : Colors.red, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}
```
- `SliverGrid.extent` 配合 `maxCrossAxisExtent` 是 Flutter 仪表板的响应式杀手锏。无缝处理不同屏幕宽度。
- 对于图表，`fl_chart` 包是 Flutter 中的黄金标准。

### React Native
```jsx
const DashboardScreen = () => {
  return (
    <ScrollView style={{ flex: 1, backgroundColor: '#F8F9FA' }}>
      <View style={{ padding: 16, flexDirection: 'row', flexWrap: 'wrap', gap: 16 }}>
        <KPICard title="Revenue" value="$45,231" trend="+12.5%" isPositive={true} />
        <KPICard title="Users" value="2,405" trend="+4.1%" isPositive={true} />
        <KPICard title="Churn" value="1.2%" trend="-0.4%" isPositive={false} />
        <KPICard title="Session" value="4m 12s" trend="+0.1%" isPositive={true} />
      </View>
      
      <View style={{ paddingHorizontal: 16, paddingBottom: 32 }}>
        <View style={{ height: 250, backgroundColor: '#FFF', borderRadius: 12, justifyContent: 'center', alignItems: 'center' }}>
          <Text style={{ color: '#999' }}>Chart Area</Text>
        </View>
      </View>
    </ScrollView>
  );
};

const KPICard = ({ title, value, trend, isPositive }) => (
  <View style={{
    backgroundColor: '#FFF',
    padding: 16,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#E9ECEF',
    flexBasis: '47%', // 大约占一半宽度减去间隙
    minWidth: 150
  }}>
    <Text style={{ color: '#6C757D', fontSize: 14, marginBottom: 4 }}>{title}</Text>
    <Text style={{ fontSize: 22, fontWeight: '700', marginBottom: 4 }}>{value}</Text>
    <Text style={{ color: isPositive ? '#28A745' : '#DC3545', fontWeight: '600', fontSize: 12 }}>{trend}</Text>
  </View>
);
```
- 在 React Native 中创建响应式 flex 网格，使用 `flexDirection: 'row'`、`flexWrap: 'wrap'`，并将子元素设为 `flexBasis: '47%'`。
- 对于繁重的数据可视化，可参考 `victory-native` 或 `@shopify/react-native-skia`。

### Jetpack Compose
```kotlin
@Composable
fun DashboardScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF8F9FA))
            .verticalScroll(rememberScrollState())
    ) {
        // 顶部应用栏替代
        Text(
            text = "Overview",
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(16.dp)
        )

        // KPI 网格
        LazyVerticalGrid(
            columns = GridCells.Adaptive(minSize = 150.dp),
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
            modifier = Modifier.heightIn(max = 400.dp) // 在滚动视图中限定网格高度
        ) {
            item { KPICard("Revenue", "$45,231", "+12.5%", true) }
            item { KPICard("Active Users", "2,405", "+4.1%", true) }
            item { KPICard("Churn Rate", "1.2%", "-0.4%", false) }
            item { KPICard("Avg. Session", "4m 12s", "+0.1%", true) }
        }

        Spacer(Modifier.height(16.dp))

        // 图表区域
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp)
                .height(250.dp)
                .background(Color.White, RoundedCornerShape(12.dp))
                .border(1.dp, Color(0xFFE9ECEF), RoundedCornerShape(12.dp)),
            contentAlignment = Alignment.Center
        ) {
            Text("Chart Area", color = Color.Gray)
        }
        
        Spacer(Modifier.height(32.dp))
    }
}

@Composable
fun KPICard(title: String, value: String, trend: String, isPositive: Boolean) {
    Column(
        modifier = Modifier
            .background(Color.White, RoundedCornerShape(8.dp))
            .border(1.dp, Color(0xFFE9ECEF), RoundedCornerShape(8.dp))
            .padding(16.dp)
    ) {
        Text(title, color = Color.Gray, fontSize = 14.sp)
        Spacer(Modifier.height(4.dp))
        Text(value, fontSize = 22.sp, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(4.dp))
        Text(trend, color = if (isPositive) Color(0xFF28A745) else Color(0xFFDC3545), fontWeight = FontWeight.SemiBold, fontSize = 12.sp)
    }
}
```
- `GridCells.Adaptive(minSize = 150.dp)` 自动创建响应式卡片布局。
- 警告：在带有 `.verticalScroll` 的 `Column` 内嵌套 `LazyVerticalGrid` 可能会导致高度计算问题。必须使用 `.heightIn(max=...)` 限制网格高度，或将整个布局转换为单个 `LazyVerticalGrid`，其中图表只是 `GridItemSpan(maxLineSpan)` 元素。

## 推荐与避免
- **推荐**：表格中的数字右对齐，便于扫读和对比。
- **避免**：用不必要的装饰图片堆砌卡片。数据本身就是装饰。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。