# D3.js 可视化模式

本参考提供常见 d3.js 可视化类型的详细代码模式。

## 层次可视化

### 树状图

```javascript
useEffect(() => {
  if (!data) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 600;
  
  const tree = d3.tree().size([height - 100, width - 200]);
  
  const root = d3.hierarchy(data);
  tree(root);
  
  const g = svg.append("g")
    .attr("transform", "translate(100,50)");
  
  // 连接线
  g.selectAll("path")
    .data(root.links())
    .join("path")
    .attr("d", d3.linkHorizontal()
      .x(d => d.y)
      .y(d => d.x))
    .attr("fill", "none")
    .attr("stroke", "#555")
    .attr("stroke-width", 2);
  
  // 节点
  const node = g.selectAll("g")
    .data(root.descendants())
    .join("g")
    .attr("transform", d => `translate(${d.y},${d.x})`);
  
  node.append("circle")
    .attr("r", 6)
    .attr("fill", d => d.children ? "#555" : "#999");
  
  node.append("text")
    .attr("dy", "0.31em")
    .attr("x", d => d.children ? -8 : 8)
    .attr("text-anchor", d => d.children ? "end" : "start")
    .text(d => d.data.name)
    .style("font-size", "12px");
    
}, [data]);
```

### 树图

```javascript
useEffect(() => {
  if (!data) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 600;
  
  const root = d3.hierarchy(data)
    .sum(d => d.value)
    .sort((a, b) => b.value - a.value);
  
  d3.treemap()
    .size([width, height])
    .padding(2)
    .round(true)(root);
  
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
  
  const cell = svg.selectAll("g")
    .data(root.leaves())
    .join("g")
    .attr("transform", d => `translate(${d.x0},${d.y0})`);
  
  cell.append("rect")
    .attr("width", d => d.x1 - d.x0)
    .attr("height", d => d.y1 - d.y0)
    .attr("fill", d => colourScale(d.parent.data.name))
    .attr("stroke", "white")
    .attr("stroke-width", 2);
  
  cell.append("text")
    .attr("x", 4)
    .attr("y", 16)
    .text(d => d.data.name)
    .style("font-size", "12px")
    .style("fill", "white");
    
}, [data]);
```

### 旭日图

```javascript
useEffect(() => {
  if (!data) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 600;
  const height = 600;
  const radius = Math.min(width, height) / 2;
  
  const root = d3.hierarchy(data)
    .sum(d => d.value)
    .sort((a, b) => b.value - a.value);
  
  const partition = d3.partition()
    .size([2 * Math.PI, radius]);
  
  partition(root);
  
  const arc = d3.arc()
    .startAngle(d => d.x0)
    .endAngle(d => d.x1)
    .innerRadius(d => d.y0)
    .outerRadius(d => d.y1);
  
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
  
  const g = svg.append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);
  
  g.selectAll("path")
    .data(root.descendants())
    .join("path")
    .attr("d", arc)
    .attr("fill", d => colourScale(d.depth))
    .attr("stroke", "white")
    .attr("stroke-width", 1);
    
}, [data]);
```

### 弦图

```javascript
function drawChordDiagram(data) {
  // 数据格式：包含 source、target 和 value 的对象数组
  // 示例: [{ source: 'A', target: 'B', value: 10 }, ...]

  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove();

  const width = 600;
  const height = 600;
  const innerRadius = Math.min(width, height) * 0.3;
  const outerRadius = innerRadius + 30;

  // 从数据创建矩阵
  const nodes = Array.from(new Set(data.flatMap(d => [d.source, d.target])));
  const matrix = Array.from({ length: nodes.length }, () => Array(nodes.length).fill(0));

  data.forEach(d => {
    const i = nodes.indexOf(d.source);
    const j = nodes.indexOf(d.target);
    matrix[i][j] += d.value;
    matrix[j][i] += d.value;
  });

  // 创建弦布局
  const chord = d3.chord()
    .padAngle(0.05)
    .sortSubgroups(d3.descending);

  const arc = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius);

  const ribbon = d3.ribbon()
    .source(d => d.source)
    .target(d => d.target);

  const colourScale = d3.scaleOrdinal(d3.schemeCategory10)
    .domain(nodes);

  const g = svg.append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);

  const chords = chord(matrix);

  // 绘制带状
  g.append("g")
    .attr("fill-opacity", 0.67)
    .selectAll("path")
    .data(chords)
    .join("path")
    .attr("d", ribbon)
    .attr("fill", d => colourScale(nodes[d.source.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.source.index])).darker());

  // 绘制组（弧）
  const group = g.append("g")
    .selectAll("g")
    .data(chords.groups)
    .join("g");

  group.append("path")
    .attr("d", arc)
    .attr("fill", d => colourScale(nodes[d.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.index])).darker());

  // 添加标签
  group.append("text")
    .each(d => { d.angle = (d.startAngle + d.endAngle) / 2; })
    .attr("dy", "0.31em")
    .attr("transform", d => `rotate(${(d.angle * 180 / Math.PI) - 90})translate(${outerRadius + 30})${d.angle > Math.PI ? "rotate(180)" : ""}`)
    .attr("text-anchor", d => d.angle > Math.PI ? "end" : null)
    .text((d, i) => nodes[i])
    .style("font-size", "12px");
}

// 数据格式示例:
// const data = [
//   { source: '类别 A', target: '类别 B', value: 100 },
//   { source: '类别 A', target: '类别 C', value: 50 },
//   { source: '类别 B', target: '类别 C', value: 75 }
// ];
// drawChordDiagram(data);
```

## 高级图表类型

### 热力图

```javascript
function drawHeatmap(data) {
  // 数据格式：包含 row、column 和 value 的对象数组
  // 示例: [{ row: 'A', column: 'X', value: 10 }, ...]

  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove();

  const width = 800;
  const height = 600;
  const margin = { top: 100, right: 30, bottom: 30, left: 100 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // 获取唯一的行和列
  const rows = Array.from(new Set(data.map(d => d.row)));
  const columns = Array.from(new Set(data.map(d => d.column)));

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // 创建比例尺
  const xScale = d3.scaleBand()
    .domain(columns)
    .range([0, innerWidth])
    .padding(0.01);

  const yScale = d3.scaleBand()
    .domain(rows)
    .range([0, innerHeight])
    .padding(0.01);

  // 值的颜色比例尺（从浅到深的红色序列）
  const colourScale = d3.scaleSequential(d3.interpolateYlOrRd)
    .domain([0, d3.max(data, d => d.value)]);

  // 绘制矩形
  g.selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", d => xScale(d.column))
    .attr("y", d => yScale(d.row))
    .attr("width", xScale.bandwidth())
    .attr("height", yScale.bandwidth())
    .attr("fill", d => colourScale(d.value));

  // 添加 x 轴标签
  svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)
    .selectAll("text")
    .data(columns)
    .join("text")
    .attr("x", d => xScale(d) + xScale.bandwidth() / 2)
    .attr("y", -10)
    .attr("text-anchor", "middle")
    .text(d => d)
    .style("font-size", "12px");

  // 添加 y 轴标签
  svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)
    .selectAll("text")
    .data(rows)
    .join("text")
    .attr("x", -10)
    .attr("y", d => yScale(d) + yScale.bandwidth() / 2)
    .attr("dy", "0.35em")
    .attr("text-anchor", "end")
    .text(d => d)
    .style("font-size", "12px");

  // 添加颜色图例
  const legendWidth = 20;
  const legendHeight = 200;
  const legend = svg.append("g")
    .attr("transform", `translate(${width - 60},${margin.top})`);

  const legendScale = d3.scaleLinear()
    .domain(colourScale.domain())
    .range([legendHeight, 0]);

  const legendAxis = d3.axisRight(legendScale).ticks(5);

  // 在图例中绘制颜色渐变
  for (let i = 0; i < legendHeight; i++) {
    legend.append("rect")
      .attr("y", i)
      .attr("width", legendWidth)
      .attr("height", 1)
      .attr("fill", colourScale(legendScale.invert(i)));
  }

  legend.append("g")
    .attr("transform", `translate(${legendWidth},0)`)
    .call(legendAxis);
}

// 数据格式示例:
// const data = [
//   { row: '周一', column: '上午', value: 42 },
//   { row: '周一', column: '下午', value: 78 },
//   { row: '周二', column: '上午', value: 65 },
//   { row: '周二', column: '下午', value: 55 }
// ];
// drawHeatmap(data);
```

### 带渐变的面积图

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  // 定义渐变
  const defs = svg.append("defs");
  const gradient = defs.append("linearGradient")
    .attr("id", "areaGradient")
    .attr("x1", "0%")
    .attr("x2", "0%")
    .attr("y1", "0%")
    .attr("y2", "100%");
  
  gradient.append("stop")
    .attr("offset", "0%")
    .attr("stop-color", "steelblue")
    .attr("stop-opacity", 0.8);
  
  gradient.append("stop")
    .attr("offset", "100%")
    .attr("stop-color", "steelblue")
    .attr("stop-opacity", 0.1);
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const xScale = d3.scaleTime()
    .domain(d3.extent(data, d => d.date))
    .range([0, innerWidth]);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([innerHeight, 0]);
  
  const area = d3.area()
    .x(d => xScale(d.date))
    .y0(innerHeight)
    .y1(d => yScale(d.value))
    .curve(d3.curveMonotoneX);
  
  g.append("path")
    .datum(data)
    .attr("fill", "url(#areaGradient)")
    .attr("d", area);
  
  const line = d3.line()
    .x(d => xScale(d.date))
    .y(d => yScale(d.value))
    .curve(d3.curveMonotoneX);
  
  g.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 2)
    .attr("d", line);
  
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));
  
  g.append("g")
    .call(d3.axisLeft(yScale));
    
}, [data]);
```

### 堆叠柱状图

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const categories = Object.keys(data[0]).filter(k => k !== 'group');
  const stackedData = d3.stack().keys(categories)(data);
  
  const xScale = d3.scaleBand()
    .domain(data.map(d => d.group))
    .range([0, innerWidth])
    .padding(0.1);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(stackedData[stackedData.length - 1], d => d[1])])
    .range([innerHeight, 0]);
  
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
  
  g.selectAll("g")
    .data(stackedData)
    .join("g")
    .attr("fill", (d, i) => colourScale(i))
    .selectAll("rect")
    .data(d => d)
    .join("rect")
    .attr("x", d => xScale(d.data.group))
    .attr("y", d => yScale(d[1]))
    .attr("height", d => yScale(d[0]) - yScale(d[1]))
    .attr("width", xScale.bandwidth());
  
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));
  
  g.append("g")
    .call(d3.axisLeft(yScale));
    
}, [data]);
```

### 分组柱状图

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const categories = Object.keys(data[0]).filter(k => k !== 'group');
  
  const x0Scale = d3.scaleBand()
    .domain(data.map(d => d.group))
    .range([0, innerWidth])
    .padding(0.1);
  
  const x1Scale = d3.scaleBand()
    .domain(categories)
    .range([0, x0Scale.bandwidth()])
    .padding(0.05);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => Math.max(...categories.map(c => d[c])))])
    .range([innerHeight, 0]);
  
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
  
  const group = g.selectAll("g")
    .data(data)
    .join("g")
    .attr("transform", d => `translate(${x0Scale(d.group)},0)`);
  
  group.selectAll("rect")
    .data(d => categories.map(key => ({ key, value: d[key] })))
    .join("rect")
    .attr("x", d => x1Scale(d.key))
    .attr("y", d => yScale(d.value))
    .attr("width", x1Scale.bandwidth())
    .attr("height", d => innerHeight - yScale(d.value))
    .attr("fill", d => colourScale(d.key));
  
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x0Scale));
  
  g.append("g")
    .call(d3.axisLeft(yScale));
    
}, [data]);
```

### 气泡图

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 600;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.x)])
    .range([0, innerWidth]);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.y)])
    .range([innerHeight, 0]);
  
  const sizeScale = d3.scaleSqrt()
    .domain([0, d3.max(data, d => d.size)])
    .range([0, 50]);
  
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
  
  g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", d => sizeScale(d.size))
    .attr("fill", d => colourScale(d.category))
    .attr("opacity", 0.6)
    .attr("stroke", "white")
    .attr("stroke-width", 2);
  
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));
  
  g.append("g")
    .call(d3.axisLeft(yScale));
    
}, [data]);
```

## 地理可视化

### 带点位的基础地图

```javascript
useEffect(() => {
  if (!geoData || !pointData) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 600;
  
  const projection = d3.geoMercator()
    .fitSize([width, height], geoData);
  
  const pathGenerator = d3.geoPath().projection(projection);
  
  // 绘制地图
  svg.selectAll("path")
    .data(geoData.features)
    .join("path")
    .attr("d", pathGenerator)
    .attr("fill", "#e0e0e0")
    .attr("stroke", "#999")
    .attr("stroke-width", 0.5);
  
  // 绘制点位
  svg.selectAll("circle")
    .data(pointData)
    .join("circle")
    .attr("cx", d => projection([d.longitude, d.latitude])[0])
    .attr("cy", d => projection([d.longitude, d.latitude])[1])
    .attr("r", 5)
    .attr("fill", "steelblue")
    .attr("opacity", 0.7);
    
}, [geoData, pointData]);
```

### 分级统计地图

```javascript
useEffect(() => {
  if (!geoData || !valueData) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 600;
  
  const projection = d3.geoMercator()
    .fitSize([width, height], geoData);
  
  const pathGenerator = d3.geoPath().projection(projection);
  
  // 创建值查找表
  const valueLookup = new Map(valueData.map(d => [d.id, d.value]));
  
  // 颜色比例尺
  const colourScale = d3.scaleSequential(d3.interpolateBlues)
    .domain([0, d3.max(valueData, d => d.value)]);
  
  svg.selectAll("path")
    .data(geoData.features)
    .join("path")
    .attr("d", pathGenerator)
    .attr("fill", d => {
      const value = valueLookup.get(d.id);
      return value ? colourScale(value) : "#e0e0e0";
    })
    .attr("stroke", "#999")
    .attr("stroke-width", 0.5);
    
}, [geoData, valueData]);
```

## 高级交互

### 框选和缩放

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.x)])
    .range([0, innerWidth]);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.y)])
    .range([innerHeight, 0]);
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const circles = g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 5)
    .attr("fill", "steelblue");
  
  // 添加框选
  const brush = d3.brush()
    .extent([[0, 0], [innerWidth, innerHeight]])
    .on("start brush", (event) => {
      if (!event.selection) return;
      
      const [[x0, y0], [x1, y1]] = event.selection;
      
      circles.attr("fill", d => {
        const cx = xScale(d.x);
        const cy = yScale(d.y);
        return (cx >= x0 && cx <= x1 && cy >= y0 && cy <= y1) 
          ? "orange" 
          : "steelblue";
      });
    });
  
  g.append("g")
    .attr("class", "brush")
    .call(brush);
    
}, [data]);
```

### 图表间联动框选

```javascript
function LinkedCharts({ data }) {
  const [selectedPoints, setSelectedPoints] = useState(new Set());
  const svg1Ref = useRef();
  const svg2Ref = useRef();
  
  useEffect(() => {
    // 图表 1: 散点图
    const svg1 = d3.select(svg1Ref.current);
    svg1.selectAll("*").remove();
    
    // ... 创建第一个图表 ...
    
    const circles1 = svg1.selectAll("circle")
      .data(data)
      .join("circle")
      .attr("fill", d => selectedPoints.has(d.id) ? "orange" : "steelblue");
    
    // 图表 2: 柱状图
    const svg2 = d3.select(svg2Ref.current);
    svg2.selectAll("*").remove();
    
    // ... 创建第二个图表 ...
    
    const bars = svg2.selectAll("rect")
      .data(data)
      .join("rect")
      .attr("fill", d => selectedPoints.has(d.id) ? "orange" : "steelblue");
    
    // 为第一个图表添加框选
    const brush = d3.brush()
      .on("start brush end", (event) => {
        if (!event.selection) {
          setSelectedPoints(new Set());
          return;
        }
        
        const [[x0, y0], [x1, y1]] = event.selection;
        const selected = new Set();
        
        data.forEach(d => {
          const x = xScale(d.x);
          const y = yScale(d.y);
          if (x >= x0 && x <= x1 && y >= y0 && y <= y1) {
            selected.add(d.id);
          }
        });
        
        setSelectedPoints(selected);
      });
    
    svg1.append("g").call(brush);
    
  }, [data, selectedPoints]);
  
  return (
    <div>
      <svg ref={svg1Ref} width="400" height="300" />
      <svg ref={svg2Ref} width="400" height="300" />
    </div>
  );
}
```

## 动画模式

### 带过渡的进入、更新、退出

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  
  const circles = svg.selectAll("circle")
    .data(data, d => d.id); // 键函数用于对象恒定性
  
  // 退出: 移除旧元素
  circles.exit()
    .transition()
    .duration(500)
    .attr("r", 0)
    .remove();
  
  // 更新: 修改现有元素
  circles
    .transition()
    .duration(500)
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("fill", "steelblue");
  
  // 进入: 添加新元素
  circles.enter()
    .append("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 0)
    .attr("fill", "steelblue")
    .transition()
    .duration(500)
    .attr("r", 5);
    
}, [data]);
```

### 路径变形

```javascript
useEffect(() => {
  if (!data1 || !data2) return;
  
  const svg = d3.select(svgRef.current);
  
  const line = d3.line()
    .x(d => xScale(d.x))
    .y(d => yScale(d.y))
    .curve(d3.curveMonotoneX);
  
  const path = svg.select("path");
  
  // 从 data1 变形到 data2
  path
    .datum(data1)
    .attr("d", line)
    .transition()
    .duration(1000)
    .attrTween("d", function() {
      const previous = d3.select(this).attr("d");
      const current = line(data2);
      return d3.interpolatePath(previous, current);
    });
    
}, [data1, data2]);
```
