# 仪表板截图

本目录包含 Loki Mode README 的截图。

---

## 所需截图

### 1. `dashboard-agents.png`

**捕获内容：** Loki Mode 仪表板的智能体监控部分，显示活跃智能体。

**创建方法：**
1. 用测试项目运行 Loki Mode：
   ```bash
   cd /path/to/test/project
   ../../autonomy/run.sh examples/simple-todo-app.md
   ```

2. 打开仪表板：
   ```bash
   open .loki/dashboard/index.html
   ```

3. 等待智能体生成（应在 30-60 秒内发生）

4. 截取**"活跃智能体"部分**，显示：
   - 多个智能体卡片（理想情况 5-8 个可见）
   - 智能体 ID 和类型（如 "eng-frontend"、"qa-001-testing"）
   - 模型徽章（Sonnet、Haiku、Opus）带颜色编码
   - 当前正在执行的工作
   - 运行时间和已完成任务统计
   - 状态指示器（活跃/已完成）

**推荐尺寸：** 1200px 宽（使用浏览器缩放以适应多个智能体）

**保存为：** `dashboard-agents.png`

---

### 2. `dashboard-tasks.png`

**捕获内容：** 任务队列看板部分。

**创建方法：**
1. 使用上面运行的同一个 Loki Mode 实例

2. 向下滚动到**"任务队列"部分**

3. 截取显示所有四列的截图：
   - **待处理**（左列，理想情况 3-5 个任务）
   - **进行中**（应至少有 1 个任务）
   - **已完成**（应显示多个已完成任务）
   - **失败**（可以为空，这没问题）

4. 确保截图显示：
   - 带计数徽章的列标题
   - 带 ID、类型和描述的任务卡片
   - 列之间的清晰分隔

**推荐尺寸：** 1200px 宽

**保存为：** `dashboard-tasks.png`

---

## 截图规格

- **格式：** PNG（用于质量和透明度支持）
- **分辨率：** 至少 1200px 宽，尽可能 retina/2x
- **浏览器：** 使用 Chrome 或 Firefox 以获得一致的渲染
- **缩放：** 调整浏览器缩放以很好地适应内容（90-100%）
- **干净状态：** 确保没有可见的浏览器扩展，干净的 URL 栏

---

## 测试截图

添加截图后，验证它们在 README 中正确显示：

```bash
# 查看带截图的 README
open README.md
# 或使用 Markdown 查看器
```

检查：
- [ ] 图像无错误加载
- [ ] 分辨率清晰可读
- [ ] 颜色匹配 Loki Mode 设计（奶油色背景、珊瑚色强调）
- [ ] 截图中的文字清晰可辨

---

## 占位图像

如果您还没有实时智能体数据，可以使用本仓库提供的测试数据：

```bash
# 创建测试智能体数据
cd /Users/lokesh/git/jobman  # 或任何测试项目
mkdir -p .agent/sub-agents .loki/state .loki/queue

# 从 Loki Mode 仓库复制测试数据
cp ~/git/loki-mode/tests/fixtures/agents/*.json .agent/sub-agents/
cp ~/git/loki-mode/tests/fixtures/queue/*.json .loki/queue/

# 生成仪表板
~/git/loki-mode/autonomy/run.sh --generate-dashboard-only

# 打开仪表板
open .loki/dashboard/index.html
```

---

## 当前状态

- [ ] `dashboard-agents.png` - 尚未创建
- [ ] `dashboard-tasks.png` - 尚未创建

添加截图后，更新此检查清单并提交：

```bash
git add docs/screenshots/*.png
git commit -m "为 README 添加仪表板截图"
```

---

## 替代方案：创建模拟截图

如果您想快速创建模拟/占位截图：

1. 使用测试夹具数据（见上文）
2. 编辑 `.loki/state/agents.json` 添加更多智能体
3. 编辑 `.loki/queue/*.json` 填充任务列
4. 刷新仪表板并截取屏幕

这可以让您获得精美的截图，而无需等待完整的 Loki Mode 运行。

---

**注意：** 截图应展示 Loki Mode 的能力，同时保持整洁和专业。避免显示：
- 个人信息或 API 密钥
- 错误状态（除非专门演示错误处理）
- 杂乱或令人困惑的数据

目标是向潜在用户展示仪表板在正常运行时的样子。
