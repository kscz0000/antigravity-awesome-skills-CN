---
name: threejs-lighting
description: Three.js 光照系统——灯光类型、阴影、环境光照。用于添加灯光、配置阴影、设置 IBL 或优化光照性能。
risk: unknown
source: community
---

# Three.js 光照系统

## 适用场景
- 需要在 Three.js 场景中添加或调整光照。
- 任务涉及灯光类型、阴影、环境光照或光照性能取舍。
- 希望通过 Three.js 光照设置提升场景的可读性、真实感或氛围。

## 快速上手

```javascript
import * as THREE from "three";

// Basic lighting setup
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 5, 5);
scene.add(directionalLight);
```

## 灯光类型总览

| 灯光             | 描述                   | 阴影支持 | 开销     |
| ---------------- | ---------------------- | -------- | -------- |
| AmbientLight     | 全局均匀照明           | 否       | 极低     |
| HemisphereLight  | 天地渐变               | 否       | 极低     |
| DirectionalLight | 平行光线（太阳）       | 是       | 低       |
| PointLight       | 全向发光（灯泡）       | 是       | 中       |
| SpotLight        | 锥形光                 | 是       | 中       |
| RectAreaLight    | 面光源（窗户）         | 否\*     | 高       |

\*RectAreaLight 阴影需要自定义方案

## AmbientLight

均匀照亮所有物体，无方向、无阴影。

```javascript
// AmbientLight(color, intensity)
const ambient = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambient);

// Modify at runtime
ambient.color.set(0xffffcc);
ambient.intensity = 0.3;
```

## HemisphereLight

从天空色到地面色的渐变，适合户外场景。

```javascript
// HemisphereLight(skyColor, groundColor, intensity)
const hemi = new THREE.HemisphereLight(0x87ceeb, 0x8b4513, 0.6);
hemi.position.set(0, 50, 0);
scene.add(hemi);

// Properties
hemi.color; // Sky color
hemi.groundColor; // Ground color
hemi.intensity;
```

## DirectionalLight

平行光线，模拟远距离光源（如太阳）。

```javascript
// DirectionalLight(color, intensity)
const dirLight = new THREE.DirectionalLight(0xffffff, 1);
dirLight.position.set(5, 10, 5);

// Light points at target (default: 0, 0, 0)
dirLight.target.position.set(0, 0, 0);
scene.add(dirLight.target);

scene.add(dirLight);
```

### DirectionalLight 阴影

```javascript
dirLight.castShadow = true;

// Shadow map size (higher = sharper, more expensive)
dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;

// Shadow camera (orthographic)
dirLight.shadow.camera.near = 0.5;
dirLight.shadow.camera.far = 50;
dirLight.shadow.camera.left = -10;
dirLight.shadow.camera.right = 10;
dirLight.shadow.camera.top = 10;
dirLight.shadow.camera.bottom = -10;

// Shadow softness
dirLight.shadow.radius = 4; // Blur radius (PCFSoftShadowMap only)

// Shadow bias (fixes shadow acne)
dirLight.shadow.bias = -0.0001;
dirLight.shadow.normalBias = 0.02;

// Helper to visualize shadow camera
const helper = new THREE.CameraHelper(dirLight.shadow.camera);
scene.add(helper);
```

## PointLight

从一个点向所有方向发射光线，类似灯泡。

```javascript
// PointLight(color, intensity, distance, decay)
const pointLight = new THREE.PointLight(0xffffff, 1, 100, 2);
pointLight.position.set(0, 5, 0);
scene.add(pointLight);

// Properties
pointLight.distance; // Maximum range (0 = infinite)
pointLight.decay; // Light falloff (physically correct = 2)
```

### PointLight 阴影

```javascript
pointLight.castShadow = true;
pointLight.shadow.mapSize.width = 1024;
pointLight.shadow.mapSize.height = 1024;

// Shadow camera (perspective - 6 directions for cube map)
pointLight.shadow.camera.near = 0.5;
pointLight.shadow.camera.far = 50;

pointLight.shadow.bias = -0.005;
```

## SpotLight

锥形光线，类似手电筒或舞台灯光。

```javascript
// SpotLight(color, intensity, distance, angle, penumbra, decay)
const spotLight = new THREE.SpotLight(0xffffff, 1, 100, Math.PI / 6, 0.5, 2);
spotLight.position.set(0, 10, 0);

// Target (light points at this)
spotLight.target.position.set(0, 0, 0);
scene.add(spotLight.target);

scene.add(spotLight);

// Properties
spotLight.angle; // Cone angle (radians, max Math.PI/2)
spotLight.penumbra; // Soft edge (0-1)
spotLight.distance; // Range
spotLight.decay; // Falloff
```

### SpotLight 阴影

```javascript
spotLight.castShadow = true;
spotLight.shadow.mapSize.width = 1024;
spotLight.shadow.mapSize.height = 1024;

// Shadow camera (perspective)
spotLight.shadow.camera.near = 0.5;
spotLight.shadow.camera.far = 50;
spotLight.shadow.camera.fov = 30;

spotLight.shadow.bias = -0.0001;

// Focus (affects shadow projection)
spotLight.shadow.focus = 1;
```

## RectAreaLight

矩形面光源，非常适合柔和、真实的光照效果。

```javascript
import { RectAreaLightHelper } from "three/examples/jsm/helpers/RectAreaLightHelper.js";
import { RectAreaLightUniformsLib } from "three/examples/jsm/lights/RectAreaLightUniformsLib.js";

// Must initialize uniforms first (WebGL renderer only)
RectAreaLightUniformsLib.init();

// RectAreaLight(color, intensity, width, height)
const rectLight = new THREE.RectAreaLight(0xffffff, 5, 4, 2);
rectLight.position.set(0, 5, 0);
rectLight.lookAt(0, 0, 0);
scene.add(rectLight);

// Helper
const helper = new RectAreaLightHelper(rectLight);
rectLight.add(helper);

// Works with MeshStandardMaterial, MeshPhysicalMaterial
// r183: Clearcoat on MeshPhysicalMaterial is now properly lit by RectAreaLight
// Does not cast shadows natively
```

## 阴影设置

### 启用阴影

```javascript
// 1. Enable on renderer
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// Shadow map types:
// THREE.BasicShadowMap - fastest, low quality
// THREE.PCFShadowMap - default, filtered
// THREE.PCFSoftShadowMap - softer edges
// THREE.VSMShadowMap - variance shadow map

// 2. Enable on light
light.castShadow = true;

// 3. Enable on objects
mesh.castShadow = true;
mesh.receiveShadow = true;

// Ground plane
floor.receiveShadow = true;
floor.castShadow = false; // Usually false for floors
```

### 阴影优化

```javascript
// Tight shadow camera frustum
const d = 10;
dirLight.shadow.camera.left = -d;
dirLight.shadow.camera.right = d;
dirLight.shadow.camera.top = d;
dirLight.shadow.camera.bottom = -d;
dirLight.shadow.camera.near = 0.5;
dirLight.shadow.camera.far = 30;

// Fix shadow acne
dirLight.shadow.bias = -0.0001; // Depth bias
dirLight.shadow.normalBias = 0.02; // Bias along normal

// Shadow map size (balance quality vs performance)
// 512 - low quality
// 1024 - medium quality
// 2048 - high quality
// 4096 - very high quality (expensive)
```

### 接触阴影（模拟方案，速度快）

```javascript
import { ContactShadows } from "three/examples/jsm/objects/ContactShadows.js";

const contactShadows = new ContactShadows({
  resolution: 512,
  blur: 2,
  opacity: 0.5,
  scale: 10,
  position: [0, 0, 0],
});
scene.add(contactShadows);
```

## 灯光辅助工具

```javascript
import { RectAreaLightHelper } from "three/examples/jsm/helpers/RectAreaLightHelper.js";

// DirectionalLight helper
const dirHelper = new THREE.DirectionalLightHelper(dirLight, 5);
scene.add(dirHelper);

// PointLight helper
const pointHelper = new THREE.PointLightHelper(pointLight, 1);
scene.add(pointHelper);

// SpotLight helper
const spotHelper = new THREE.SpotLightHelper(spotLight);
scene.add(spotHelper);

// Hemisphere helper
const hemiHelper = new THREE.HemisphereLightHelper(hemiLight, 5);
scene.add(hemiHelper);

// RectAreaLight helper
const rectHelper = new RectAreaLightHelper(rectLight);
rectLight.add(rectHelper);

// Update helpers when light changes
dirHelper.update();
spotHelper.update();
```

## 环境光照（IBL）

基于图像的光照，使用 HDR 环境贴图。

```javascript
import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader.js";

const rgbeLoader = new RGBELoader();
rgbeLoader.load("environment.hdr", (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;

  // Set as scene environment (affects all PBR materials)
  scene.environment = texture;

  // Optional: also use as background
  scene.background = texture;
  scene.backgroundBlurriness = 0; // 0-1, blur the background
  scene.backgroundIntensity = 1;
});

// PMREMGenerator for better reflections
const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();

rgbeLoader.load("environment.hdr", (texture) => {
  const envMap = pmremGenerator.fromEquirectangular(texture).texture;
  scene.environment = envMap;
  texture.dispose();
  pmremGenerator.dispose();
});
```

### 立方体贴图环境

```javascript
const cubeLoader = new THREE.CubeTextureLoader();
const envMap = cubeLoader.load([
  "px.jpg",
  "nx.jpg",
  "py.jpg",
  "ny.jpg",
  "pz.jpg",
  "nz.jpg",
]);

scene.environment = envMap;
scene.background = envMap;
```

## 光照探针（进阶）

从空间中某个点捕获光照信息，用于环境照明。

```javascript
import { LightProbeGenerator } from "three/examples/jsm/lights/LightProbeGenerator.js";

// Generate from cube texture
const lightProbe = new THREE.LightProbe();
scene.add(lightProbe);

lightProbe.copy(LightProbeGenerator.fromCubeTexture(cubeTexture));

// Or from render target
const cubeCamera = new THREE.CubeCamera(
  0.1,
  100,
  new THREE.WebGLCubeRenderTarget(256),
);
cubeCamera.update(renderer, scene);
lightProbe.copy(
  LightProbeGenerator.fromCubeRenderTarget(renderer, cubeCamera.renderTarget),
);
```

## 常见光照方案

### 三点布光

```javascript
// Key light (main light)
const keyLight = new THREE.DirectionalLight(0xffffff, 1);
keyLight.position.set(5, 5, 5);
scene.add(keyLight);

// Fill light (softer, opposite side)
const fillLight = new THREE.DirectionalLight(0xffffff, 0.5);
fillLight.position.set(-5, 3, 5);
scene.add(fillLight);

// Back light (rim lighting)
const backLight = new THREE.DirectionalLight(0xffffff, 0.3);
backLight.position.set(0, 5, -5);
scene.add(backLight);

// Ambient fill
const ambient = new THREE.AmbientLight(0x404040, 0.3);
scene.add(ambient);
```

### 户外日光

```javascript
// Sun
const sun = new THREE.DirectionalLight(0xffffcc, 1.5);
sun.position.set(50, 100, 50);
sun.castShadow = true;
scene.add(sun);

// Sky ambient
const hemi = new THREE.HemisphereLight(0x87ceeb, 0x8b4513, 0.6);
scene.add(hemi);
```

### 室内摄影棚

```javascript
// Multiple area lights
RectAreaLightUniformsLib.init();

const light1 = new THREE.RectAreaLight(0xffffff, 5, 2, 2);
light1.position.set(3, 3, 3);
light1.lookAt(0, 0, 0);
scene.add(light1);

const light2 = new THREE.RectAreaLight(0xffffff, 3, 2, 2);
light2.position.set(-3, 3, 3);
light2.lookAt(0, 0, 0);
scene.add(light2);

// Ambient fill
const ambient = new THREE.AmbientLight(0x404040, 0.2);
scene.add(ambient);
```

## 灯光动画

```javascript
const clock = new THREE.Clock();

function animate() {
  const time = clock.getElapsedTime();

  // Orbit light around scene
  light.position.x = Math.cos(time) * 5;
  light.position.z = Math.sin(time) * 5;

  // Pulsing intensity
  light.intensity = 1 + Math.sin(time * 2) * 0.5;

  // Color cycling
  light.color.setHSL((time * 0.1) % 1, 1, 0.5);

  // Update helpers if using
  lightHelper.update();
}
```

## 性能优化建议

1. **控制灯光数量**：每增加一个灯光都会增加着色器复杂度
2. **使用烘焙光照**：静态场景可将光照烘焙到贴图中
3. **缩小阴影贴图**：512-1024 通常足够
4. **收紧阴影视锥**：只覆盖需要的区域
5. **关闭不必要的阴影**：并非所有灯光都需要投射阴影
6. **使用灯光分层**：将特定物体排除在某些灯光的影响之外

```javascript
// Light layers
light.layers.set(1); // Light only affects layer 1
mesh.layers.enable(1); // Mesh is on layer 1
otherMesh.layers.disable(1); // Other mesh not affected

// Selective shadows
mesh.castShadow = true;
mesh.receiveShadow = true;
decorMesh.castShadow = false; // Small objects often don't need to cast
```

## 相关技能

- `threejs-materials` - 材质的光照响应
- `threejs-textures` - 光照贴图和环境贴图
- `threejs-postprocessing` - 泛光等光照特效

## 限制条件
- 仅在任务明确匹配上述范围时使用本技能。
- 不可将输出视为环境特定验证、测试或专家评审的替代品。
- 缺少必要输入、权限、安全边界或成功标准时，应停下来请求澄清。
