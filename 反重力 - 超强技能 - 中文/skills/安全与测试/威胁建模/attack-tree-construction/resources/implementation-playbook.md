# 攻击树构建实现手册

本文件包含技能引用的详细模式、检查清单和代码示例。

## 核心概念

### 1. 攻击树结构

```
                    [根目标]
                         |
            ┌────────────┴────────────┐
            │                         │
       [子目标 1]                [子目标 2]
       (OR节点)                  (AND节点)
            │                         │
      ┌─────┴─────┐             ┌─────┴─────┐
      │           │             │           │
   [攻击]     [攻击]        [攻击]     [攻击]
    (叶子)     (叶子)        (叶子)     (叶子)
```

### 2. 节点类型

| 类型 | 符号 | 描述 |
|------|--------|-------------|
| **OR** | 椭圆 | 任一子节点达成目标 |
| **AND** | 矩形 | 所有子节点均需达成 |
| **叶子** | 方框 | 原子攻击步骤 |

### 3. 攻击属性

| 属性 | 描述 | 取值 |
|-----------|-------------|--------|
| **成本** | 所需资源 | $, $$, $$$ |
| **时间** | 执行时长 | 小时, 天, 周 |
| **技能** | 所需专业能力 | 低, 中, 高 |
| **检测风险** | 被检测的可能性 | 低, 中, 高 |

## 模板

### 模板 1：攻击树数据模型

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Union
import json

class NodeType(Enum):
    OR = "or"
    AND = "and"
    LEAF = "leaf"


class Difficulty(Enum):
    TRIVIAL = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    EXPERT = 5


class Cost(Enum):
    FREE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


class DetectionRisk(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CERTAIN = 4


@dataclass
class AttackAttributes:
    difficulty: Difficulty = Difficulty.MEDIUM
    cost: Cost = Cost.MEDIUM
    detection_risk: DetectionRisk = DetectionRisk.MEDIUM
    time_hours: float = 8.0
    requires_insider: bool = False
    requires_physical: bool = False


@dataclass
class AttackNode:
    id: str
    name: str
    description: str
    node_type: NodeType
    attributes: AttackAttributes = field(default_factory=AttackAttributes)
    children: List['AttackNode'] = field(default_factory=list)
    mitigations: List[str] = field(default_factory=list)
    cve_refs: List[str] = field(default_factory=list)

    def add_child(self, child: 'AttackNode') -> None:
        self.children.append(child)

    def calculate_path_difficulty(self) -> float:
        """计算此路径的综合难度。"""
        if self.node_type == NodeType.LEAF:
            return self.attributes.difficulty.value

        if not self.children:
            return 0

        child_difficulties = [c.calculate_path_difficulty() for c in self.children]

        if self.node_type == NodeType.OR:
            return min(child_difficulties)
        else:  # AND
            return max(child_difficulties)

    def calculate_path_cost(self) -> float:
        """计算此路径的综合成本。"""
        if self.node_type == NodeType.LEAF:
            return self.attributes.cost.value

        if not self.children:
            return 0

        child_costs = [c.calculate_path_cost() for c in self.children]

        if self.node_type == NodeType.OR:
            return min(child_costs)
        else:  # AND
            return sum(child_costs)

    def to_dict(self) -> Dict:
        """转换为字典以便序列化。"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.node_type.value,
            "attributes": {
                "difficulty": self.attributes.difficulty.name,
                "cost": self.attributes.cost.name,
                "detection_risk": self.attributes.detection_risk.name,
                "time_hours": self.attributes.time_hours,
            },
            "mitigations": self.mitigations,
            "children": [c.to_dict() for c in self.children]
        }


@dataclass
class AttackTree:
    name: str
    description: str
    root: AttackNode
    version: str = "1.0"

    def find_easiest_path(self) -> List[AttackNode]:
        """查找难度最低的路径。"""
        return self._find_path(self.root, minimize="difficulty")

    def find_cheapest_path(self) -> List[AttackNode]:
        """查找成本最低的路径。"""
        return self._find_path(self.root, minimize="cost")

    def find_stealthiest_path(self) -> List[AttackNode]:
        """查找检测风险最低的路径。"""
        return self._find_path(self.root, minimize="detection")

    def _find_path(
        self,
        node: AttackNode,
        minimize: str
    ) -> List[AttackNode]:
        """递归路径查找。"""
        if node.node_type == NodeType.LEAF:
            return [node]

        if not node.children:
            return [node]

        if node.node_type == NodeType.OR:
            # 选择最佳子路径
            best_path = None
            best_score = float('inf')

            for child in node.children:
                child_path = self._find_path(child, minimize)
                score = self._path_score(child_path, minimize)
                if score < best_score:
                    best_score = score
                    best_path = child_path

            return [node] + (best_path or [])
        else:  # AND
            # 必须遍历所有子节点
            path = [node]
            for child in node.children:
                path.extend(self._find_path(child, minimize))
            return path

    def _path_score(self, path: List[AttackNode], metric: str) -> float:
        """计算路径得分。"""
        if metric == "difficulty":
            return sum(n.attributes.difficulty.value for n in path if n.node_type == NodeType.LEAF)
        elif metric == "cost":
            return sum(n.attributes.cost.value for n in path if n.node_type == NodeType.LEAF)
        elif metric == "detection":
            return sum(n.attributes.detection_risk.value for n in path if n.node_type == NodeType.LEAF)
        return 0

    def get_all_leaf_attacks(self) -> List[AttackNode]:
        """获取所有叶子攻击节点。"""
        leaves = []
        self._collect_leaves(self.root, leaves)
        return leaves

    def _collect_leaves(self, node: AttackNode, leaves: List[AttackNode]) -> None:
        if node.node_type == NodeType.LEAF:
            leaves.append(node)
        for child in node.children:
            self._collect_leaves(child, leaves)

    def get_unmitigated_attacks(self) -> List[AttackNode]:
        """查找无缓解措施的攻击。"""
        return [n for n in self.get_all_leaf_attacks() if not n.mitigations]

    def export_json(self) -> str:
        """导出树为JSON。"""
        return json.dumps({
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "root": self.root.to_dict()
        }, indent=2)
```

### 模板 2：攻击树构建器

```python
class AttackTreeBuilder:
    """攻击树的流式构建器。"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._node_stack: List[AttackNode] = []
        self._root: Optional[AttackNode] = None

    def goal(self, id: str, name: str, description: str = "") -> 'AttackTreeBuilder':
        """设置根目标（默认为OR节点）。"""
        self._root = AttackNode(
            id=id,
            name=name,
            description=description,
            node_type=NodeType.OR
        )
        self._node_stack = [self._root]
        return self

    def or_node(self, id: str, name: str, description: str = "") -> 'AttackTreeBuilder':
        """添加OR子目标。"""
        node = AttackNode(
            id=id,
            name=name,
            description=description,
            node_type=NodeType.OR
        )
        self._current().add_child(node)
        self._node_stack.append(node)
        return self

    def and_node(self, id: str, name: str, description: str = "") -> 'AttackTreeBuilder':
        """添加AND子目标（所有子节点均需达成）。"""
        node = AttackNode(
            id=id,
            name=name,
            description=description,
            node_type=NodeType.AND
        )
        self._current().add_child(node)
        self._node_stack.append(node)
        return self

    def attack(
        self,
        id: str,
        name: str,
        description: str = "",
        difficulty: Difficulty = Difficulty.MEDIUM,
        cost: Cost = Cost.MEDIUM,
        detection: DetectionRisk = DetectionRisk.MEDIUM,
        time_hours: float = 8.0,
        mitigations: List[str] = None
    ) -> 'AttackTreeBuilder':
        """添加叶子攻击节点。"""
        node = AttackNode(
            id=id,
            name=name,
            description=description,
            node_type=NodeType.LEAF,
            attributes=AttackAttributes(
                difficulty=difficulty,
                cost=cost,
                detection_risk=detection,
                time_hours=time_hours
            ),
            mitigations=mitigations or []
        )
        self._current().add_child(node)
        return self

    def end(self) -> 'AttackTreeBuilder':
        """关闭当前节点，返回父节点。"""
        if len(self._node_stack) > 1:
            self._node_stack.pop()
        return self

    def build(self) -> AttackTree:
        """构建攻击树。"""
        if not self._root:
            raise ValueError("未定义根目标")
        return AttackTree(
            name=self.name,
            description=self.description,
            root=self._root
        )

    def _current(self) -> AttackNode:
        if not self._node_stack:
            raise ValueError("无当前节点")
        return self._node_stack[-1]


# 示例用法
def build_account_takeover_tree() -> AttackTree:
    """构建账户接管场景的攻击树。"""
    return (
        AttackTreeBuilder("账户接管", "获取用户账户的未授权访问")
        .goal("G1", "接管用户账户")

        .or_node("S1", "窃取凭证")
            .attack(
                "A1", "钓鱼攻击",
                difficulty=Difficulty.LOW,
                cost=Cost.LOW,
                detection=DetectionRisk.MEDIUM,
                mitigations=["安全意识培训", "邮件过滤"]
            )
            .attack(
                "A2", "凭证填充",
                difficulty=Difficulty.TRIVIAL,
                cost=Cost.LOW,
                detection=DetectionRisk.HIGH,
                mitigations=["速率限制", "MFA", "密码泄露监控"]
            )
            .attack(
                "A3", "键盘记录恶意软件",
                difficulty=Difficulty.MEDIUM,
                cost=Cost.MEDIUM,
                detection=DetectionRisk.MEDIUM,
                mitigations=["端点防护", "MFA"]
            )
        .end()

        .or_node("S2", "绕过认证")
            .attack(
                "A4", "会话劫持",
                difficulty=Difficulty.MEDIUM,
                cost=Cost.LOW,
                detection=DetectionRisk.LOW,
                mitigations=["安全会话管理", "仅HTTPS"]
            )
            .attack(
                "A5", "认证绕过漏洞",
                difficulty=Difficulty.HIGH,
                cost=Cost.LOW,
                detection=DetectionRisk.LOW,
                mitigations=["安全测试", "代码审查", "WAF"]
            )
        .end()

        .or_node("S3", "社会工程")
            .and_node("S3.1", "账户恢复攻击")
                .attack(
                    "A6", "收集个人信息",
                    difficulty=Difficulty.LOW,
                    cost=Cost.FREE,
                    detection=DetectionRisk.NONE
                )
                .attack(
                    "A7", "致电客服",
                    difficulty=Difficulty.MEDIUM,
                    cost=Cost.FREE,
                    detection=DetectionRisk.MEDIUM,
                    mitigations=["客服验证流程", "安全问题"]
                )
            .end()
        .end()

        .build()
    )
```

### 模板 3：Mermaid 图表生成器

```python
class MermaidExporter:
    """将攻击树导出为Mermaid图表格式。"""

    def __init__(self, tree: AttackTree):
        self.tree = tree
        self._lines: List[str] = []
        self._node_count = 0

    def export(self) -> str:
        """导出树为Mermaid流程图。"""
        self._lines = ["flowchart TD"]
        self._export_node(self.tree.root, None)
        return "\n".join(self._lines)

    def _export_node(self, node: AttackNode, parent_id: Optional[str]) -> str:
        """递归导出节点。"""
        node_id = f"N{self._node_count}"
        self._node_count += 1

        # 根据类型确定节点形状
        if node.node_type == NodeType.OR:
            shape = f"{node_id}(({node.name}))"
        elif node.node_type == NodeType.AND:
            shape = f"{node_id}[{node.name}]"
        else:  # LEAF
            # 根据难度着色
            style = self._get_leaf_style(node)
            shape = f"{node_id}[/{node.name}/]"
            self._lines.append(f"    style {node_id} {style}")

        self._lines.append(f"    {shape}")

        if parent_id:
            connector = "-->" if node.node_type != NodeType.AND else "==>"
            self._lines.append(f"    {parent_id} {connector} {node_id}")

        for child in node.children:
            self._export_node(child, node_id)

        return node_id

    def _get_leaf_style(self, node: AttackNode) -> str:
        """根据攻击属性获取样式。"""
        colors = {
            Difficulty.TRIVIAL: "fill:#ff6b6b",  # 红色 - 简单攻击
            Difficulty.LOW: "fill:#ffa06b",
            Difficulty.MEDIUM: "fill:#ffd93d",
            Difficulty.HIGH: "fill:#6bcb77",
            Difficulty.EXPERT: "fill:#4d96ff",  # 蓝色 - 困难攻击
        }
        color = colors.get(node.attributes.difficulty, "fill:#gray")
        return color


class PlantUMLExporter:
    """将攻击树导出为PlantUML格式。"""

    def __init__(self, tree: AttackTree):
        self.tree = tree

    def export(self) -> str:
        """导出树为PlantUML。"""
        lines = [
            "@startmindmap",
            f"* {self.tree.name}",
        ]
        self._export_node(self.tree.root, lines, 1)
        lines.append("@endmindmap")
        return "\n".join(lines)

    def _export_node(self, node: AttackNode, lines: List[str], depth: int) -> None:
        """递归导出节点。"""
        prefix = "*" * (depth + 1)

        if node.node_type == NodeType.OR:
            marker = "[OR]"
        elif node.node_type == NodeType.AND:
            marker = "[AND]"
        else:
            diff = node.attributes.difficulty.name
            marker = f"<<{diff}>>"

        lines.append(f"{prefix} {marker} {node.name}")

        for child in node.children:
            self._export_node(child, lines, depth + 1)
```

### 模板 4：攻击路径分析

```python
from typing import Set, Tuple

class AttackPathAnalyzer:
    """分析攻击路径和覆盖范围。"""

    def __init__(self, tree: AttackTree):
        self.tree = tree

    def get_all_paths(self) -> List[List[AttackNode]]:
        """获取所有可能的攻击路径。"""
        paths = []
        self._collect_paths(self.tree.root, [], paths)
        return paths

    def _collect_paths(
        self,
        node: AttackNode,
        current_path: List[AttackNode],
        all_paths: List[List[AttackNode]]
    ) -> None:
        """递归收集所有路径。"""
        current_path = current_path + [node]

        if node.node_type == NodeType.LEAF:
            all_paths.append(current_path)
            return

        if not node.children:
            all_paths.append(current_path)
            return

        if node.node_type == NodeType.OR:
            # 每个子节点是独立路径
            for child in node.children:
                self._collect_paths(child, current_path, all_paths)
        else:  # AND
            # 必须组合所有子节点
            child_paths = []
            for child in node.children:
                child_sub_paths = []
                self._collect_paths(child, [], child_sub_paths)
                child_paths.append(child_sub_paths)

            # 组合所有AND子节点的路径
            combined = self._combine_and_paths(child_paths)
            for combo in combined:
                all_paths.append(current_path + combo)

    def _combine_and_paths(
        self,
        child_paths: List[List[List[AttackNode]]]
    ) -> List[List[AttackNode]]:
        """组合AND节点子节点的路径。"""
        if not child_paths:
            return [[]]

        if len(child_paths) == 1:
            return [path for paths in child_paths for path in paths]

        # 所有子路径组合的笛卡尔积
        result = [[]]
        for paths in child_paths:
            new_result = []
            for existing in result:
                for path in paths:
                    new_result.append(existing + path)
            result = new_result
        return result

    def calculate_path_metrics(self, path: List[AttackNode]) -> Dict:
        """计算特定路径的指标。"""
        leaves = [n for n in path if n.node_type == NodeType.LEAF]

        total_difficulty = sum(n.attributes.difficulty.value for n in leaves)
        total_cost = sum(n.attributes.cost.value for n in leaves)
        total_time = sum(n.attributes.time_hours for n in leaves)
        max_detection = max((n.attributes.detection_risk.value for n in leaves), default=0)

        return {
            "steps": len(leaves),
            "total_difficulty": total_difficulty,
            "avg_difficulty": total_difficulty / len(leaves) if leaves else 0,
            "total_cost": total_cost,
            "total_time_hours": total_time,
            "max_detection_risk": max_detection,
            "requires_insider": any(n.attributes.requires_insider for n in leaves),
            "requires_physical": any(n.attributes.requires_physical for n in leaves),
        }

    def identify_critical_nodes(self) -> List[Tuple[AttackNode, int]]:
        """查找出现在最多路径中的节点。"""
        paths = self.get_all_paths()
        node_counts: Dict[str, Tuple[AttackNode, int]] = {}

        for path in paths:
            for node in path:
                if node.id not in node_counts:
                    node_counts[node.id] = (node, 0)
                node_counts[node.id] = (node, node_counts[node.id][1] + 1)

        return sorted(
            node_counts.values(),
            key=lambda x: x[1],
            reverse=True
        )

    def coverage_analysis(self, mitigated_attacks: Set[str]) -> Dict:
        """分析缓解措施如何影响攻击覆盖。"""
        all_paths = self.get_all_paths()
        blocked_paths = []
        open_paths = []

        for path in all_paths:
            path_attacks = {n.id for n in path if n.node_type == NodeType.LEAF}
            if path_attacks & mitigated_attacks:
                blocked_paths.append(path)
            else:
                open_paths.append(path)

        return {
            "total_paths": len(all_paths),
            "blocked_paths": len(blocked_paths),
            "open_paths": len(open_paths),
            "coverage_percentage": len(blocked_paths) / len(all_paths) * 100 if all_paths else 0,
            "open_path_details": [
                {"path": [n.name for n in p], "metrics": self.calculate_path_metrics(p)}
                for p in open_paths[:5]  # 前5条开放路径
            ]
        }

    def prioritize_mitigations(self) -> List[Dict]:
        """按影响优先排序缓解措施。"""
        critical_nodes = self.identify_critical_nodes()
        paths = self.get_all_paths()
        total_paths = len(paths)

        recommendations = []
        for node, count in critical_nodes:
            if node.node_type == NodeType.LEAF and node.mitigations:
                recommendations.append({
                    "attack": node.name,
                    "attack_id": node.id,
                    "paths_blocked": count,
                    "coverage_impact": count / total_paths * 100,
                    "difficulty": node.attributes.difficulty.name,
                    "mitigations": node.mitigations,
                })

        return sorted(recommendations, key=lambda x: x["coverage_impact"], reverse=True)
```

## 最佳实践

### 应该做的
- **从明确目标开始** - 定义攻击者想要什么
- **穷尽考虑** - 考虑所有攻击向量
- **标注攻击属性** - 成本、技能和检测风险
- **定期更新** - 新威胁不断出现
- **专家验证** - 红队评审

### 不应该做的
- **不要过度简化** - 真实攻击很复杂
- **不要忽略依赖关系** - AND节点很重要
- **不要忘记内部威胁** - 并非所有攻击者都是外部的
- **不要跳过缓解措施** - 攻击树用于防御规划
- **不要使其静态化** - 威胁形势在演变

## 资源

- [Bruce Schneier的攻击树](https://www.schneier.com/academic/archives/1999/12/attack_trees.html)
- [MITRE ATT&CK框架](https://attack.mitre.org/)
- [OWASP攻击面分析](https://owasp.org/www-community/controls/Attack_Surface_Analysis_Cheat_Sheet)
