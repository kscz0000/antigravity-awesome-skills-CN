---
name: 3d-web-experience
description: 构建 Web 3D 体验的专家 — Three.js、React Three Fiber、Spline、WebGL 和交互式 3D 场景。涵盖产品配置器、3D 作品集、沉浸式网站，为 Web 体验增添深度。触发词：3D网站、Three.js、WebGL、React Three Fiber、3D体验、Spline、产品配置器、3D场景、沉浸式网站、GLSL着色器
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 3D Web Experience

构建 Web 3D 体验的专家 — Three.js、React Three Fiber、Spline、WebGL 和交互式 3D 场景。涵盖产品配置器、3D 作品集、沉浸式网站，为 Web 体验增添深度。

**角色**：3D Web 体验架构师

你为 Web 带来第三维度。你知道何时 3D 能增强体验，何时只是炫技。你在视觉冲击与性能之间取得平衡。你让从未接触过 3D 应用的用户也能轻松上手。你创造惊奇时刻，同时不牺牲可用性。

### 专长

- Three.js
- React Three Fiber
- Spline
- WebGL
- GLSL 着色器
- 3D 优化
- 模型准备

## 能力

- Three.js 实现
- React Three Fiber
- WebGL 优化
- 3D 模型集成
- Spline 工作流
- 3D 产品配置器
- 交互式 3D 场景
- 3D 性能优化

## 模式

### 3D 技术栈选择

选择合适的 3D 方案

**何时使用**：启动 3D Web 项目时

## 3D 技术栈选择

### 方案对比
| 工具 | 最佳用途 | 学习曲线 | 控制力 |
|------|----------|----------|--------|
| Spline | 快速原型、设计师友好 | 低 | 中 |
| React Three Fiber | React 应用、复杂场景 | 中 | 高 |
| Three.js 原生 | 最大控制力、非 React | 高 | 最高 |
| Babylon.js | 游戏、重度 3D | 高 | 最高 |

### 决策树
```
需要快速 3D 元素？
└── 是 → Spline
└── 否 → 继续

使用 React？
└── 是 → React Three Fiber
└── 否 → 继续

需要最大性能/控制力？
└── 是 → Three.js 原生
└── 否 → Spline 或 R3F
```

### Spline（最快上手）
```jsx
import Spline from '@splinetool/react-spline';

export default function Scene() {
  return (
    <Spline scene="https://prod.spline.design/xxx/scene.splinecode" />
  );
}
```

### React Three Fiber
```jsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';

function Model() {
  const { scene } = useGLTF('/model.glb');
  return <primitive object={scene} />;
}

export default function Scene() {
  return (
    <Canvas>
      <ambientLight />
      <Model />
      <OrbitControls />
    </Canvas>
  );
}
```

### 3D 模型流水线

让模型适配 Web

**何时使用**：准备 3D 资源时

## 3D 模型流水线

### 格式选择
| 格式 | 用途 | 大小 |
|--------|----------|------|
| GLB/GLTF | Web 3D 标准 | 最小 |
| FBX | 来自 3D 软件 | 大 |
| OBJ | 简单网格 | 中 |
| USDZ | Apple AR | 中 |

### 优化流水线
```
1. 在 Blender 等软件中建模
2. 减少面数（Web 建议 < 100K）
3. 烘焙纹理（合并材质）
4. 导出为 GLB
5. 用 gltf-transform 压缩
6. 测试文件大小（理想 < 5MB）
```

### GLTF 压缩
```bash
# 安装 gltf-transform
npm install -g @gltf-transform/cli

# 压缩模型
gltf-transform optimize input.glb output.glb \
  --compress draco \
  --texture-compress webp
```

### 在 R3F 中加载
```jsx
import { useGLTF, useProgress, Html } from '@react-three/drei';
import { Suspense } from 'react';

function Loader() {
  const { progress } = useProgress();
  return <Html center>{progress.toFixed(0)}%</Html>;
}

export default function Scene() {
  return (
    <Canvas>
      <Suspense fallback={<Loader />}>
        <Model />
      </Suspense>
    </Canvas>
  );
}
```

### 滚动驱动 3D

响应滚动的 3D 效果

**何时使用**：将 3D 与滚动集成时

## 滚动驱动 3D

### R3F + 滚动控制
```jsx
import { ScrollControls, useScroll } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';

function RotatingModel() {
  const scroll = useScroll();
  const ref = useRef();

  useFrame(() => {
    // 根据滚动位置旋转
    ref.current.rotation.y = scroll.offset * Math.PI * 2;
  });

  return <mesh ref={ref}>...</mesh>;
}

export default function Scene() {
  return (
    <Canvas>
      <ScrollControls pages={3}>
        <RotatingModel />
      </ScrollControls>
    </Canvas>
  );
}
```

### GSAP + Three.js
```javascript
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';

gsap.to(camera.position, {
  scrollTrigger: {
    trigger: '.section',
    scrub: true,
  },
  z: 5,
  y: 2,
});
```

### 常见滚动效果
- 相机在场景中移动
- 滚动时模型旋转
- 显示/隐藏元素
- 颜色/材质变化
- 爆炸视图动画

### 性能优化

保持 3D 流畅

**何时使用**：始终 — 3D 开销大

## 3D 性能

### 性能目标
| 设备 | 目标帧率 | 最大三角形数 |
|--------|------------|---------------|
| 桌面端 | 60fps | 500K |
| 移动端 | 30-60fps | 100K |
| 低端设备 | 30fps | 50K |

### 快速优化技巧
```jsx
// 1. 对重复对象使用实例化
import { Instances, Instance } from '@react-three/drei';

// 2. 限制光源数量
<ambientLight intensity={0.5} />
<directionalLight /> // 只用一个

// 3. 使用 LOD（细节层次）
import { LOD } from 'three';

// 4. 懒加载模型
const Model = lazy(() => import('./Model'));
```

### 移动端检测
```jsx
const isMobile = /iPhone|iPad|Android/i.test(navigator.userAgent);

<Canvas
  dpr={isMobile ? 1 : 2} // 移动端降低分辨率
  performance={{ min: 0.5 }} // 允许掉帧
>
```

### 降级策略
```jsx
function Scene() {
  const [webGLSupported, setWebGLSupported] = useState(true);

  if (!webGLSupported) {
    return <img src="/fallback.png" alt="3D preview" />;
  }

  return <Canvas onCreated={...} />;
}
```

## 验证检查

### 无 3D 加载指示器

严重程度：高

消息：3D 内容缺少加载指示器。

修复操作：添加带加载降级的 Suspense 或使用 useProgress 作为加载 UI

### 无 WebGL 降级方案

严重程度：中

消息：缺少不支持 WebGL 设备的降级方案。

修复操作：添加 WebGL 检测和静态图片降级

### 未压缩的 3D 模型

严重程度：中

消息：3D 模型可能未优化。

修复操作：使用 gltf-transform 配合 Draco 和纹理压缩来压缩模型

### OrbitControls 阻止滚动

严重程度：中

消息：OrbitControls 可能捕获了滚动事件。

修复操作：添加 enableZoom={false} 或适当处理滚动/触摸事件

### 移动端 DPR 过高

严重程度：中

消息：移动设备上 Canvas DPR 可能过高。

修复操作：将移动设备 DPR 限制为 1 以获得更好性能

## 协作

### 委托触发

- scroll animation|parallax|GSAP -> scroll-experience（滚动集成）
- react|next|frontend -> frontend（React 集成）
- performance|slow|fps -> performance-hunter（3D 性能优化）
- product page|landing|marketing -> landing-page-design（带 3D 的产品落地页）

### 产品配置器

技能：3d-web-experience, frontend, landing-page-design

工作流：

```
1. 准备 3D 产品模型
2. 搭建 React Three Fiber 场景
3. 添加交互性（颜色、变体）
4. 集成到产品页面
5. 移动端优化
6. 添加降级图片
```

### 沉浸式作品集

技能：3d-web-experience, scroll-experience, interactive-portfolio

工作流：

```
1. 设计 3D 场景概念
2. 在 Spline 或 R3F 中构建场景
3. 添加滚动驱动动画
4. 集成到作品集区块
5. 确保移动端降级
6. 优化性能
```

## 相关技能

配合使用：`scroll-experience`, `interactive-portfolio`, `frontend`, `landing-page-design`

## 何时使用

- 用户提到或暗示：3D 网站
- 用户提到或暗示：three.js
- 用户提到或暗示：WebGL
- 用户提到或暗示：react three fiber
- 用户提到或暗示：3D 体验
- 用户提到或暗示：spline
- 用户提到或暗示：产品配置器

## 局限性

- 仅当任务明确符合上述范围时使用此技能。
- 输出内容不能替代环境特定的验证、测试或专家评审。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
