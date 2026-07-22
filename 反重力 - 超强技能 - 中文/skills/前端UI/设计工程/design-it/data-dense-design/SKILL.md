---
name: data-dense-design
description: Data-Dense Design 的 Web 与 App 实现指南。当用户需要专业工具、最大化信息密度和专家级界面（如彭博终端或 IDE）时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Data-Dense Design

> "密度本身就是特性。对专家用户而言，减少点击比留白更重要。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **紧凑布局**：极小的边距和内边距（通常为 2px 到 4px）。
2. **等宽与表格数据**：数字必须完美垂直对齐。
3. **高实用性**：每个像素都为功能服务。极少纯装饰性元素。

## 视觉 DNA
- **颜色**：**Industrial Chic**（高对比度）或 **Minimalist Slate**。避免亮色背景。强烈倾向暗色主题，以减轻 8 小时连续使用带来的眼疲劳。
- **排版**：小号基础字号（`11px` - `13px`）。严格使用等宽字体（`Fira Code`、`JetBrains Mono`）处理数据。
- **边框**：使用细 `1px` 边框（`#333` 或 `#e0e0e0`）广泛分隔细小数据单元。

## Web 实现
- 表格、CSS Grid 和无间隙 Flexbox。
- **CSS 示例**：
```css
body {
  background-color: #1e1e1e; /* IDE 暗色 */
  color: #cccccc;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 12px; /* 非常小 */
  margin: 0;
}

.dense-toolbar {
  display: flex;
  background-color: #2d2d2d;
  border-bottom: 1px solid #3c3c3c;
  padding: 2px 4px;
}

.dense-btn {
  background: transparent;
  color: #ccc;
  border: 1px solid transparent;
  padding: 2px 8px;
  border-radius: 2px;
  cursor: pointer;
}
.dense-btn:hover {
  background-color: #3c3c3c;
  border-color: #555;
}

/* 密集数据表 */
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'JetBrains Mono', monospace;
}

.data-table th, .data-table td {
  padding: 4px 8px;
  border: 1px solid #3c3c3c;
  text-align: right; /* 数字右对齐 */
}

.data-table tr:nth-child(even) { background-color: #252526; }
.data-table tr:hover { background-color: #094771; color: #fff; } /* 选中高亮 */
```

## App 实现

### SwiftUI
```swift
struct DataDenseView: View {
    var body: some View {
        ScrollView([.horizontal, .vertical]) {
            Grid(horizontalSpacing: 0, verticalSpacing: 0) {
                // 标题行
                GridRow {
                    HeaderCell("SYM")
                    HeaderCell("BID")
                    HeaderCell("ASK")
                    HeaderCell("CHG")
                }
                
                // 数据行
                DataRow(sym: "AAPL", bid: "173.40", ask: "173.45", chg: "+0.12", isPos: true)
                DataRow(sym: "MSFT", bid: "320.10", ask: "320.15", chg: "-0.45", isPos: false)
                DataRow(sym: "GOOG", bid: "135.20", ask: "135.30", chg: "+0.02", isPos: true)
            }
            .border(Color.gray.opacity(0.3), width: 1)
        }
        .background(Color(white: 0.12)) // 深色 IDE 背景
    }
}

struct HeaderCell: View {
    let text: String
    init(_ text: String) { self.text = text }
    var body: some View {
        Text(text)
            .font(.system(size: 11, weight: .bold, design: .monospaced))
            .foregroundColor(.gray)
            .padding(4)
            .frame(minWidth: 60, alignment: .leading)
            .border(Color.gray.opacity(0.3), width: 0.5)
            .background(Color(white: 0.18))
    }
}

struct DataRow: View {
    let sym, bid, ask, chg: String
    let isPos: Bool
    var body: some View {
        GridRow {
            Cell(sym, color: .white)
            Cell(bid, color: .white, align: .trailing)
            Cell(ask, color: .white, align: .trailing)
            Cell(chg, color: isPos ? .green : .red, align: .trailing)
        }
    }
}

struct Cell: View {
    let text: String
    let color: Color
    let align: Alignment
    init(_ text: String, color: Color, align: Alignment = .leading) {
        self.text = text; self.color = color; self.align = align
    }
    var body: some View {
        Text(text)
            .font(.system(size: 12, design: .monospaced))
            .foregroundColor(color)
            .padding(4)
            .frame(minWidth: 60, alignment: align)
            .border(Color.gray.opacity(0.3), width: 0.5)
    }
}
```
- 使用 `Grid` 配合 `0` 间距。
- 字体必须是 `.system(..., design: .monospaced)`。
- 在每个单元格上使用 `0.5` 宽度的 `.border()` 还原密集电子表格外观。

### Flutter
```dart
class DataDenseScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF1E1E1E),
      body: SingleChildScrollView(
        scrollDirection: Axis.vertical,
        child: SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: Theme(
            // 局部覆盖主题使表格高度密集
            data: Theme.of(context).copyWith(
              dividerColor: Colors.grey[800],
            ),
            child: DataTable(
              headingRowHeight: 28, // 极度密集
              dataRowMinHeight: 24,
              dataRowMaxHeight: 24, // 极度密集
              columnSpacing: 16,
              border: TableBorder.all(color: Colors.grey[800]!, width: 1),
              columns: const [
                DataColumn(label: Text('SYM', style: TextStyle(color: Colors.grey, fontSize: 11, fontFamily: 'RobotoMono'))),
                DataColumn(label: Text('BID', style: TextStyle(color: Colors.grey, fontSize: 11, fontFamily: 'RobotoMono')), numeric: true),
                DataColumn(label: Text('ASK', style: TextStyle(color: Colors.grey, fontSize: 11, fontFamily: 'RobotoMono')), numeric: true),
              ],
              rows: [
                _buildRow('AAPL', '173.40', '173.45'),
                _buildRow('MSFT', '320.10', '320.15'),
                _buildRow('GOOG', '135.20', '135.30'),
              ],
            ),
          ),
        ),
      ),
    );
  }

  DataRow _buildRow(String sym, String bid, String ask) {
    const style = TextStyle(color: Colors.white, fontSize: 12, fontFamily: 'RobotoMono');
    return DataRow(
      cells: [
        DataCell(Text(sym, style: style)),
        DataCell(Text(bid, style: style)),
        DataCell(Text(ask, style: style)),
      ],
    );
  }
}
```
- Flutter 的 `DataTable` 是完美的，但你必须手动将 `headingRowHeight` 和 `dataRowHeight` 从 Material 默认值（很大）压扁。
- 用双层 `SingleChildScrollView` 包裹以允许在大数据集上平移浏览。

### React Native
```jsx
const DataDenseScreen = () => {
  return (
    <ScrollView style={{ backgroundColor: '#1E1E1E', flex: 1 }}>
      <ScrollView horizontal>
        <View style={{ borderWidth: 1, borderColor: '#333' }}>
          {/* 标题 */}
          <View style={{ flexDirection: 'row', backgroundColor: '#2D2D2D' }}>
            <HeaderCell text="SYM" width={60} />
            <HeaderCell text="BID" width={80} align="right" />
            <HeaderCell text="ASK" width={80} align="right" />
            <HeaderCell text="CHG" width={60} align="right" />
          </View>
          
          {/* 行 */}
          <DataRow sym="AAPL" bid="173.40" ask="173.45" chg="+0.12" isPos={true} />
          <DataRow sym="MSFT" bid="320.10" ask="320.15" chg="-0.45" isPos={false} />
        </View>
      </ScrollView>
    </ScrollView>
  );
};

const HeaderCell = ({ text, width, align = 'left' }) => (
  <View style={{ width, padding: 4, borderWidth: 0.5, borderColor: '#333' }}>
    <Text style={{ color: '#999', fontSize: 11, fontFamily: 'monospace', textAlign: align, fontWeight: 'bold' }}>
      {text}
    </Text>
  </View>
);

const DataRow = ({ sym, bid, ask, chg, isPos }) => (
  <View style={{ flexDirection: 'row' }}>
    <Cell text={sym} width={60} />
    <Cell text={bid} width={80} align="right" />
    <Cell text={ask} width={80} align="right" />
    <Cell text={chg} width={60} align="right" color={isPos ? '#4CAF50' : '#F44336'} />
  </View>
);

const Cell = ({ text, width, align = 'left', color = '#CCC' }) => (
  <View style={{ width, padding: 4, borderWidth: 0.5, borderColor: '#333' }}>
    <Text style={{ color, fontSize: 12, fontFamily: 'monospace', textAlign: align }}>
      {text}
    </Text>
  </View>
);
```
- React Native 没有原生 Table 组件，所以必须使用 `flexDirection: 'row'` 和严格的单元格 `width` 属性来构建网格。
- 双层 ScrollView（垂直一个、水平一个）是移动数据表的标准做法。

### Jetpack Compose
```kotlin
@Composable
fun DataDenseScreen() {
    val scrollStateHorizontal = rememberScrollState()
    val scrollStateVertical = rememberScrollState()

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF1E1E1E))
            .verticalScroll(scrollStateVertical)
            .horizontalScroll(scrollStateHorizontal)
            .padding(8.dp)
    ) {
        Column(modifier = Modifier.border(1.dp, Color(0xFF333333))) {
            // 标题
            Row(modifier = Modifier.background(Color(0xFF2D2D2D))) {
                Cell("SYM", 60.dp, Color.Gray, true)
                Cell("BID", 80.dp, Color.Gray, true, TextAlign.End)
                Cell("ASK", 80.dp, Color.Gray, true, TextAlign.End)
            }
            
            // 行
            DataRow("AAPL", "173.40", "173.45")
            DataRow("MSFT", "320.10", "320.15")
        }
    }
}

@Composable
fun DataRow(sym: String, bid: String, ask: String) {
    Row {
        Cell(sym, 60.dp, Color.White, false)
        Cell(bid, 80.dp, Color.White, false, TextAlign.End)
        Cell(ask, 80.dp, Color.White, false, TextAlign.End)
    }
}

@Composable
fun Cell(text: String, width: Dp, color: Color, isHeader: Boolean, align: TextAlign = TextAlign.Start) {
    Text(
        text = text,
        color = color,
        fontSize = if (isHeader) 11.sp else 12.sp,
        fontWeight = if (isHeader) FontWeight.Bold else FontWeight.Normal,
        fontFamily = FontFamily.Monospace,
        textAlign = align,
        modifier = Modifier
            .width(width)
            .border(0.5.dp, Color(0xFF333333))
            .padding(4.dp)
    )
}
```
- 在根 `Box` 上链式调用 `.verticalScroll()` 和 `.horizontalScroll()`。
- Compose 允许 `.border()` 直接作用于 `Text` modifier，无需将所有内容包裹在 `Box` 中，使电子表格网格的实现非常简洁。

## 推荐与避免
- **推荐**：对数据变化使用颜色编码（红/绿），但保持饱和度柔和以防止眼疲劳。
- **避免**：使用大内边距或巨大的 H1 标题。专家用户已经知道自己在哪个屏幕上。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。