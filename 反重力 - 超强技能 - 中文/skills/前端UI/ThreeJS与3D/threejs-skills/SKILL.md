---
name: threejs-skills
description: "使用 Three.js 创建 3D 场景、交互体验和视觉效果。涉及 3D 图形、WebGL 体验、3D 可视化、动画或交互式 3D 元素时使用。"
risk: safe
source: "https://github.com/CloudAI-X/threejs-skills"
date_added: "2026-02-27"
---

# Three.js 技能

使用 Three.js 最佳实践，系统化地创建高质量 3D 场景和交互体验。

## 适用场景
- 需要 3D 可视化或图形（"创建一个 3D 模型"、"用 3D 展示"）
- 需要交互式 3D 体验（"旋转的立方体"、"可探索的场景"）
- 需要 WebGL 或基于 canvas 的渲染
- 需要动画、粒子或视觉效果
- 提及 Three.js、WebGL 或 3D 渲染
- 需要在 3D 空间中可视化数据

## 核心配置模式

### 1. Three.js 基础导入

现代 Three.js（r183+）使用 ES module import map：

```html
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.183.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.183.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
</script>
```

生产环境使用 npm/vite/webpack：

```javascript
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
```

### 2. 场景初始化

每个 Three.js 作品都需要这些核心组件：

```javascript
// Scene - 包含所有 3D 对象
const scene = new THREE.Scene();

// Camera - 定义观察视角
const camera = new THREE.PerspectiveCamera(
  75, // Field of view
  window.innerWidth / window.innerHeight, // Aspect ratio
  0.1, // Near clipping plane
  1000, // Far clipping plane
);
camera.position.z = 5;

// Renderer - 绘制场景
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
```

### 3. 动画循环

优先使用 `renderer.setAnimationLoop()`，或使用 `requestAnimationFrame`：

```javascript
// 推荐：setAnimationLoop（兼容 WebXR）
renderer.setAnimationLoop(() => {
  mesh.rotation.x += 0.01;
  mesh.rotation.y += 0.01;
  renderer.render(scene, camera);
});

// 备选：手动 requestAnimationFrame
function animate() {
  requestAnimationFrame(animate);
  mesh.rotation.x += 0.01;
  mesh.rotation.y += 0.01;
  renderer.render(scene, camera);
}
animate();
```

## 系统化开发流程

### 1. 定义场景

首先确定：

- **需要渲染哪些对象**
- **摄像机位置**和视场角
- **所需的光照配置**
- **交互模式**（静态、旋转、用户控制）

### 2. 构建几何体

选择合适的几何体类型：

**基础形状：**

- `BoxGeometry` — 立方体、长方体
- `SphereGeometry` — 球体、行星
- `CylinderGeometry` — 圆柱体、管道
- `PlaneGeometry` — 平面、地面
- `TorusGeometry` — 环形体、圆环

**CapsuleGeometry** 可用（自 r142 起稳定）：

```javascript
new THREE.CapsuleGeometry(0.5, 1, 4, 8); // radius, length, capSegments, radialSegments
```

### 3. 应用材质

根据视觉需求选择材质：

**常用材质：**

- `MeshBasicMaterial` — 无光照、纯色（不需要灯光）
- `MeshStandardMaterial` — 基于物理、逼真（需要灯光）
- `MeshPhongMaterial` — 光亮表面，带高光反射
- `MeshLambertMaterial` — 哑光表面，漫反射

```javascript
const material = new THREE.MeshStandardMaterial({
  color: 0x00ff00,
  metalness: 0.5,
  roughness: 0.5,
});
```

### 4. 添加光照

**使用受光材质**（Standard、Phong、Lambert）时需添加灯光：

```javascript
// 环境光 - 整体照明
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

// 平行光 - 类似阳光
const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
directionalLight.position.set(5, 5, 5);
scene.add(directionalLight);
```

**使用 `MeshBasicMaterial` 时无需光照** — 它本身就是无光的。

### 5. 处理响应式

始终添加窗口尺寸变化处理：

```javascript
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

## 常用模式

### 旋转物体

```javascript
function animate() {
  requestAnimationFrame(animate);
  mesh.rotation.x += 0.01;
  mesh.rotation.y += 0.01;
  renderer.render(scene, camera);
}
```

### OrbitControls

使用 import map 或构建工具时，OrbitControls 可直接使用：

```javascript
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// 在动画循环中更新
renderer.setAnimationLoop(() => {
  controls.update();
  renderer.render(scene, camera);
});
```

### 自定义摄像机控制（备选方案）

不导入 OrbitControls 时的轻量自定义控制：

```javascript
let isDragging = false;
let previousMousePosition = { x: 0, y: 0 };

renderer.domElement.addEventListener("mousedown", () => {
  isDragging = true;
});

renderer.domElement.addEventListener("mouseup", () => {
  isDragging = false;
});

renderer.domElement.addEventListener("mousemove", (event) => {
  if (isDragging) {
    const deltaX = event.clientX - previousMousePosition.x;
    const deltaY = event.clientY - previousMousePosition.y;

    // 围绕场景旋转摄像机
    const rotationSpeed = 0.005;
    camera.position.x += deltaX * rotationSpeed;
    camera.position.y -= deltaY * rotationSpeed;
    camera.lookAt(scene.position);
  }

  previousMousePosition = { x: event.clientX, y: event.clientY };
});

// 鼠标滚轮缩放
renderer.domElement.addEventListener("wheel", (event) => {
  event.preventDefault();
  camera.position.z += event.deltaY * 0.01;
  camera.position.z = Math.max(2, Math.min(20, camera.position.z)); // Clamp
});
```

### 射线拾取（对象选择）

检测鼠标点击和悬停在 3D 对象上的事件：

```javascript
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const clickableObjects = []; // Array of meshes that can be clicked

// 更新鼠标位置
window.addEventListener("mousemove", (event) => {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
});

// 检测点击
window.addEventListener("click", () => {
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(clickableObjects);

  if (intersects.length > 0) {
    const clickedObject = intersects[0].object;
    // 处理点击 - 改变颜色、缩放等
    clickedObject.material.color.set(0xff0000);
  }
});

// 动画循环中的悬停效果
function animate() {
  requestAnimationFrame(animate);

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(clickableObjects);

  // 重置所有对象
  clickableObjects.forEach((obj) => {
    obj.scale.set(1, 1, 1);
  });

  // 高亮悬停对象
  if (intersects.length > 0) {
    intersects[0].object.scale.set(1.2, 1.2, 1.2);
    document.body.style.cursor = "pointer";
  } else {
    document.body.style.cursor = "default";
  }

  renderer.render(scene, camera);
}
```

### 粒子系统

```javascript
const particlesGeometry = new THREE.BufferGeometry();
const particlesCount = 1000;
const posArray = new Float32Array(particlesCount * 3);

for (let i = 0; i < particlesCount * 3; i++) {
  posArray[i] = (Math.random() - 0.5) * 10;
}

particlesGeometry.setAttribute(
  "position",
  new THREE.BufferAttribute(posArray, 3),
);

const particlesMaterial = new THREE.PointsMaterial({
  size: 0.02,
  color: 0xffffff,
});

const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
scene.add(particlesMesh);
```

### 用户交互（鼠标移动）

```javascript
let mouseX = 0;
let mouseY = 0;

document.addEventListener("mousemove", (event) => {
  mouseX = (event.clientX / window.innerWidth) * 2 - 1;
  mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
});

function animate() {
  requestAnimationFrame(animate);
  camera.position.x = mouseX * 2;
  camera.position.y = mouseY * 2;
  camera.lookAt(scene.position);
  renderer.render(scene, camera);
}
```

### 加载纹理

```javascript
const textureLoader = new THREE.TextureLoader();
const texture = textureLoader.load("texture-url.jpg");

const material = new THREE.MeshStandardMaterial({
  map: texture,
});
```

## 最佳实践

### 性能优化

- **复用几何体和材质**，创建多个相似对象时
- **使用 `BufferGeometry`** 处理自定义形状（更高效）
- **限制粒子数量**以保持 60fps（从 1000-5000 开始）
- **释放资源**，移除对象时：
  ```javascript
  geometry.dispose();
  material.dispose();
  texture.dispose();
  ```

### 画面质量

- 渲染器始终设置 `antialias: true` 以获得平滑边缘
- 使用合适的摄像机 FOV（通常 45-75 度）
- 合理放置灯光 — 避免多个强光重叠
- 添加环境光 + 平行光以获得逼真场景

### 代码组织

- 在顶部初始化 scene、camera、renderer
- 将相关对象分组（如所有粒子放在一个组中）
- 动画逻辑放在 animate 函数中
- 复杂场景中将对象创建分离到独立函数

### 常见错误

- ❌ 使用 `outputEncoding` 而非 `outputColorSpace`（r152 中已重命名）
- ❌ 忘记用 `scene.add()` 将对象添加到场景
- ❌ 使用受光材质但未添加灯光
- ❌ 未处理窗口尺寸变化
- ❌ 动画循环中忘记调用 `renderer.render()`
- ❌ 使用 `THREE.Clock` 而未考虑 `THREE.Timer`（r183 推荐）

## 示例工作流

用户："创建一个响应鼠标移动的交互式 3D 球体"

1. **配置**：导入 Three.js，创建 scene/camera/renderer
2. **几何体**：创建 `SphereGeometry(1, 32, 32)` 获得平滑球体
3. **材质**：使用 `MeshStandardMaterial` 获得逼真外观
4. **光照**：添加环境光 + 平行光
5. **交互**：追踪鼠标位置，更新摄像机
6. **动画**：旋转球体，持续渲染
7. **响应式**：添加窗口尺寸变化处理
8. **结果**：流畅的交互式 3D 球体 ✓

## 故障排查

**黑屏 / 无渲染：**

- 检查对象是否已添加到场景
- 确认摄像机位置不在对象内部
- 确保已调用 renderer.render()
- 使用受光材质时添加灯光

**性能差：**

- 减少粒子数量
- 降低几何体细分度（segments）
- 复用材质/几何体
- 检查浏览器控制台错误

**对象不可见：**

- 检查对象位置与摄像机位置的关系
- 确认材质有可见的颜色/属性
- 确保摄像机远裁剪面包含对象
- 按需添加光照

## 高级技巧

### 作品集级渲染的视觉打磨

**阴影：**

```javascript
// 启用渲染器阴影
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap; // Soft shadows

// 投射阴影的灯光
const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 10, 5);
directionalLight.castShadow = true;

// 配置阴影质量
directionalLight.shadow.mapSize.width = 2048;
directionalLight.shadow.mapSize.height = 2048;
directionalLight.shadow.camera.near = 0.5;
directionalLight.shadow.camera.far = 50;

scene.add(directionalLight);

// 对象投射和接收阴影
mesh.castShadow = true;
mesh.receiveShadow = true;

// 地面接收阴影
const groundGeometry = new THREE.PlaneGeometry(20, 20);
const groundMaterial = new THREE.MeshStandardMaterial({ color: 0x808080 });
const ground = new THREE.Mesh(groundGeometry, groundMaterial);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);
```

**环境贴图与反射：**

```javascript
// 从立方体贴图创建环境贴图
const loader = new THREE.CubeTextureLoader();
const envMap = loader.load([
  "px.jpg",
  "nx.jpg", // positive x, negative x
  "py.jpg",
  "ny.jpg", // positive y, negative y
  "pz.jpg",
  "nz.jpg", // positive z, negative z
]);

scene.environment = envMap; // 影响所有 PBR 材质
scene.background = envMap; // 可选：用作天空盒

// 或应用于特定材质
const material = new THREE.MeshStandardMaterial({
  metalness: 1.0,
  roughness: 0.1,
  envMap: envMap,
});
```

**色调映射与输出编码：**

```javascript
// 提升色彩准确度和 HDR 渲染
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.outputColorSpace = THREE.SRGBColorSpace; // Was outputEncoding in older versions

// 使颜色更鲜艳逼真
```

**雾效增加深度感：**

```javascript
// 线性雾
scene.fog = new THREE.Fog(0xcccccc, 10, 50); // color, near, far

// 或指数雾（更逼真）
scene.fog = new THREE.FogExp2(0xcccccc, 0.02); // color, density
```

### 从顶点创建自定义几何体

```javascript
const geometry = new THREE.BufferGeometry();
const vertices = new Float32Array([-1, -1, 0, 1, -1, 0, 1, 1, 0]);
geometry.setAttribute("position", new THREE.BufferAttribute(vertices, 3));
```

### 后处理效果

后处理效果可通过 import map 或构建工具使用。详见 `threejs-postprocessing` 技能了解 EffectComposer、bloom、DOF 等。

### 对象分组

```javascript
const group = new THREE.Group();
group.add(mesh1);
group.add(mesh2);
group.rotation.y = Math.PI / 4;
scene.add(group);
```

## 总结

Three.js 作品需要系统化配置：

1. 通过 import map 或构建工具导入 Three.js
2. 初始化 scene、camera、renderer
3. 创建几何体 + 材质 = 网格
4. 使用受光材质时添加灯光
5. 实现动画循环（推荐 `setAnimationLoop`）
6. 处理窗口尺寸变化
7. 设置 `renderer.outputColorSpace = THREE.SRGBColorSpace`

遵循这些模式，即可获得可靠、高性能的 3D 体验。

## 现代 Three.js 实践（r183）

### 模块化导入

```javascript
// 使用 npm/vite/webpack：
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
```

### WebGPU 渲染器（备选方案）

Three.js r183 包含 WebGPU 渲染器作为 WebGL 的替代方案：

```javascript
import { WebGPURenderer } from "three/addons/renderers/webgpu/WebGPURenderer.js";

const renderer = new WebGPURenderer({ antialias: true });
await renderer.init();
renderer.setSize(window.innerWidth, window.innerHeight);
```

WebGPU 使用 TSL（Three.js Shading Language）替代 GLSL 编写自定义着色器。详见 `threejs-shaders`。

### Timer（r183 推荐）

r183 起推荐使用 `THREE.Timer` 替代 `THREE.Clock`：

```javascript
const timer = new THREE.Timer();

renderer.setAnimationLoop(() => {
  timer.update();
  const delta = timer.getDelta();
  const elapsed = timer.getElapsed();

  mesh.rotation.y += delta;
  renderer.render(scene, camera);
});
```

**相比 Clock 的优势：**

- 不受页面可见性影响（标签页隐藏时暂停）
- 更简洁的 API 设计
- 与 `setAnimationLoop` 集成更好

### 动画库（GSAP 集成）

```javascript
// 基于时间线的平滑动画
import gsap from "gsap";

// 替代手动动画循环：
gsap.to(mesh.position, {
  x: 5,
  duration: 2,
  ease: "power2.inOut",
});

// 复杂序列：
const timeline = gsap.timeline();
timeline
  .to(mesh.rotation, { y: Math.PI * 2, duration: 2 })
  .to(mesh.scale, { x: 2, y: 2, z: 2, duration: 1 }, "-=1");
```

**选择 GSAP 的理由：**

- 专业的缓动函数
- 时间线控制（暂停、倒放、拖拽）
- 复杂动画优于手动插值

### 滚动交互

```javascript
// 将 3D 动画与页面滚动同步
let scrollY = window.scrollY;

window.addEventListener("scroll", () => {
  scrollY = window.scrollY;
});

function animate() {
  requestAnimationFrame(animate);

  // 基于滚动位置旋转
  mesh.rotation.y = scrollY * 0.001;

  // 摄像机穿越场景
  camera.position.y = -(scrollY / window.innerHeight) * 10;

  renderer.render(scene, camera);
}
```

**高级滚动库：**

- ScrollTrigger（GSAP 插件）
- Locomotive Scroll
- Lenis 平滑滚动

### 生产环境性能优化

```javascript
// 细节层次（LOD）
const lod = new THREE.LOD();
lod.addLevel(highDetailMesh, 0); // 近景
lod.addLevel(mediumDetailMesh, 10); // 中距离
lod.addLevel(lowDetailMesh, 50); // 远景
scene.add(lod);

// 实例化网格，用于大量相同对象
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshStandardMaterial();
const instancedMesh = new THREE.InstancedMesh(geometry, material, 1000);

// 为每个实例设置变换
const matrix = new THREE.Matrix4();
for (let i = 0; i < 1000; i++) {
  matrix.setPosition(
    Math.random() * 100,
    Math.random() * 100,
    Math.random() * 100,
  );
  instancedMesh.setMatrixAt(i, matrix);
}
```

### 现代加载模式

```javascript
// 生产环境中加载 3D 模型：
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";

const loader = new GLTFLoader();
loader.load("model.gltf", (gltf) => {
  scene.add(gltf.scene);

  // 遍历并配置材质
  gltf.scene.traverse((child) => {
    if (child.isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;
    }
  });
});
```

### 如何选择

**Import Map 方式：**

- 快速原型和演示
- 教学内容
- 作品和嵌入式体验
- 无需构建步骤

**生产构建方式：**

- 客户项目和作品集
- 复杂应用
- 性能敏感型应用
- 团队协作配合版本控制

### 推荐的生产技术栈

```
Three.js r183 + Vite
├── GSAP (animations)
├── React Three Fiber (optional - React integration)
├── Drei (helper components)
├── Leva (debug GUI)
└── Post-processing effects
```

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 缺少所需输入、权限、安全边界或成功标准时，停下来请求澄清。
