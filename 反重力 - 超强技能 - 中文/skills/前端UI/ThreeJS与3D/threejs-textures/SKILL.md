---
name: threejs-textures
description: Three.js 纹理——纹理类型、UV 映射、环境贴图、纹理设置。用于处理图像、UV 坐标、立方体贴图、HDR 环境或纹理优化等场景。
risk: unknown
source: community
---

# Three.js 纹理

## 适用场景
- 需要在 Three.js 中加载、配置或优化纹理。
- 任务涉及 UV 映射、纹理设置、立方体贴图、环境贴图或 HDR 纹理工作流。
- 处理的是表面细节和材质输入，而非几何体或动画。

## 快速开始

```javascript
import * as THREE from "three";

// Load texture
const loader = new THREE.TextureLoader();
const texture = loader.load("texture.jpg");

// Apply to material
const material = new THREE.MeshStandardMaterial({
  map: texture,
});
```

## 纹理加载

### 基础加载

```javascript
const loader = new THREE.TextureLoader();

// Async with callbacks
loader.load(
  "texture.jpg",
  (texture) => console.log("Loaded"),
  (progress) => console.log("Progress"),
  (error) => console.error("Error"),
);

// Synchronous style (loads async internally)
const texture = loader.load("texture.jpg");
material.map = texture;
```

### Promise 封装

```javascript
function loadTexture(url) {
  return new Promise((resolve, reject) => {
    new THREE.TextureLoader().load(url, resolve, undefined, reject);
  });
}

// Usage
const [colorMap, normalMap, roughnessMap] = await Promise.all([
  loadTexture("color.jpg"),
  loadTexture("normal.jpg"),
  loadTexture("roughness.jpg"),
]);
```

## 纹理配置

### 色彩空间

对精确色彩还原至关重要。

```javascript
// Color/albedo textures - use sRGB
colorTexture.colorSpace = THREE.SRGBColorSpace;

// Data textures (normal, roughness, metalness, AO) - leave as default
// Do NOT set colorSpace for data textures (NoColorSpace is default)
```

### 环绕模式

```javascript
texture.wrapS = THREE.RepeatWrapping; // Horizontal
texture.wrapT = THREE.RepeatWrapping; // Vertical

// Options:
// THREE.ClampToEdgeWrapping - Stretches edge pixels (default)
// THREE.RepeatWrapping - Tiles the texture
// THREE.MirroredRepeatWrapping - Tiles with mirror flip
```

### 重复、偏移、旋转

```javascript
// Tile texture 4x4
texture.repeat.set(4, 4);
texture.wrapS = THREE.RepeatWrapping;
texture.wrapT = THREE.RepeatWrapping;

// Offset (0-1 range)
texture.offset.set(0.5, 0.5);

// Rotation (radians, around center)
texture.rotation = Math.PI / 4;
texture.center.set(0.5, 0.5); // Rotation pivot
```

### 过滤

```javascript
// Minification (texture larger than screen pixels)
texture.minFilter = THREE.LinearMipmapLinearFilter; // Default, smooth
texture.minFilter = THREE.NearestFilter; // Pixelated
texture.minFilter = THREE.LinearFilter; // Smooth, no mipmaps

// Magnification (texture smaller than screen pixels)
texture.magFilter = THREE.LinearFilter; // Smooth (default)
texture.magFilter = THREE.NearestFilter; // Pixelated (retro games)

// Anisotropic filtering (sharper at angles)
texture.anisotropy = renderer.capabilities.getMaxAnisotropy();
```

### 生成 Mipmap

```javascript
// Usually true by default
texture.generateMipmaps = true;

// Disable for non-power-of-2 textures or data textures
texture.generateMipmaps = false;
texture.minFilter = THREE.LinearFilter;
```

## 纹理类型

### 普通纹理

```javascript
const texture = new THREE.Texture(image);
texture.needsUpdate = true;
```

### 数据纹理

从原始数据创建纹理。

```javascript
// Create gradient texture
const size = 256;
const data = new Uint8Array(size * size * 4);

for (let i = 0; i < size; i++) {
  for (let j = 0; j < size; j++) {
    const index = (i * size + j) * 4;
    data[index] = i; // R
    data[index + 1] = j; // G
    data[index + 2] = 128; // B
    data[index + 3] = 255; // A
  }
}

const texture = new THREE.DataTexture(data, size, size);
texture.needsUpdate = true;
```

### Canvas 纹理

```javascript
const canvas = document.createElement("canvas");
canvas.width = 256;
canvas.height = 256;
const ctx = canvas.getContext("2d");

// Draw on canvas
ctx.fillStyle = "red";
ctx.fillRect(0, 0, 256, 256);
ctx.fillStyle = "white";
ctx.font = "48px Arial";
ctx.fillText("Hello", 50, 150);

const texture = new THREE.CanvasTexture(canvas);

// Update when canvas changes
texture.needsUpdate = true;
```

### 视频纹理

```javascript
const video = document.createElement("video");
video.src = "video.mp4";
video.loop = true;
video.muted = true;
video.play();

const texture = new THREE.VideoTexture(video);
texture.colorSpace = THREE.SRGBColorSpace;

// No need to set needsUpdate - auto-updates
```

### 压缩纹理

```javascript
import { KTX2Loader } from "three/examples/jsm/loaders/KTX2Loader.js";

const ktx2Loader = new KTX2Loader();
ktx2Loader.setTranscoderPath("path/to/basis/");
ktx2Loader.detectSupport(renderer);

ktx2Loader.load("texture.ktx2", (texture) => {
  material.map = texture;
});
```

## 立方体纹理

用于环境贴图和天空盒。

### CubeTextureLoader

```javascript
const loader = new THREE.CubeTextureLoader();
const cubeTexture = loader.load([
  "px.jpg",
  "nx.jpg", // +X, -X
  "py.jpg",
  "ny.jpg", // +Y, -Y
  "pz.jpg",
  "nz.jpg", // +Z, -Z
]);

// As background
scene.background = cubeTexture;

// As environment map
scene.environment = cubeTexture;
material.envMap = cubeTexture;
```

### 等距矩形转立方体贴图

```javascript
import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader.js";

const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();

new RGBELoader().load("environment.hdr", (texture) => {
  const envMap = pmremGenerator.fromEquirectangular(texture).texture;
  scene.environment = envMap;
  scene.background = envMap;

  texture.dispose();
  pmremGenerator.dispose();
});
```

## HDR 纹理

### RGBELoader

```javascript
import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader.js";

const loader = new RGBELoader();
loader.load("environment.hdr", (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = texture;
  scene.background = texture;
});
```

### EXRLoader

```javascript
import { EXRLoader } from "three/examples/jsm/loaders/EXRLoader.js";

const loader = new EXRLoader();
loader.load("environment.exr", (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = texture;
});
```

### 背景选项

```javascript
scene.background = texture;
scene.backgroundBlurriness = 0.5; // 0-1, blur background
scene.backgroundIntensity = 1.0; // Brightness
scene.backgroundRotation.y = Math.PI; // Rotate background
```

## 渲染目标

渲染到纹理以实现特效。

```javascript
// Create render target
const renderTarget = new THREE.WebGLRenderTarget(512, 512, {
  minFilter: THREE.LinearFilter,
  magFilter: THREE.LinearFilter,
  format: THREE.RGBAFormat,
});

// Render scene to target
renderer.setRenderTarget(renderTarget);
renderer.render(scene, camera);
renderer.setRenderTarget(null); // Back to screen

// Use as texture
material.map = renderTarget.texture;
```

### 深度纹理

```javascript
const renderTarget = new THREE.WebGLRenderTarget(512, 512);
renderTarget.depthTexture = new THREE.DepthTexture(
  512,
  512,
  THREE.UnsignedShortType,
);

// Access depth
const depthTexture = renderTarget.depthTexture;
```

### 多重采样渲染目标

```javascript
const renderTarget = new THREE.WebGLRenderTarget(512, 512, {
  samples: 4, // MSAA
});
```

## CubeCamera

用于反射的动态环境贴图。

```javascript
const cubeRenderTarget = new THREE.WebGLCubeRenderTarget(256, {
  generateMipmaps: true,
  minFilter: THREE.LinearMipmapLinearFilter,
});

const cubeCamera = new THREE.CubeCamera(0.1, 1000, cubeRenderTarget);
scene.add(cubeCamera);

// Apply to reflective material
reflectiveMaterial.envMap = cubeRenderTarget.texture;

// Update in animation loop (expensive!)
function animate() {
  // Hide reflective object, update env map, show again
  reflectiveObject.visible = false;
  cubeCamera.position.copy(reflectiveObject.position);
  cubeCamera.update(renderer, scene);
  reflectiveObject.visible = true;
}
```

## UV 映射

### 访问 UV

```javascript
const uvs = geometry.attributes.uv;

// Read UV
const u = uvs.getX(vertexIndex);
const v = uvs.getY(vertexIndex);

// Modify UV
uvs.setXY(vertexIndex, newU, newV);
uvs.needsUpdate = true;
```

### 第二 UV 通道（用于 AO 贴图）

```javascript
// Required for aoMap
geometry.setAttribute("uv2", geometry.attributes.uv);

// Or create custom second UV
const uv2 = new Float32Array(vertexCount * 2);
// ... fill uv2 data
geometry.setAttribute("uv2", new THREE.BufferAttribute(uv2, 2));
```

### Shader 中的 UV 变换

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: {
    map: { value: texture },
    uvOffset: { value: new THREE.Vector2(0, 0) },
    uvScale: { value: new THREE.Vector2(1, 1) },
  },
  vertexShader: `
    varying vec2 vUv;
    uniform vec2 uvOffset;
    uniform vec2 uvScale;

    void main() {
      vUv = uv * uvScale + uvOffset;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    varying vec2 vUv;
    uniform sampler2D map;

    void main() {
      gl_FragColor = texture2D(map, vUv);
    }
  `,
});
```

## 纹理图集

将多张图片合并在一个纹理中。

```javascript
// Atlas with 4 sprites (2x2 grid)
const atlas = loader.load("atlas.png");
atlas.wrapS = THREE.ClampToEdgeWrapping;
atlas.wrapT = THREE.ClampToEdgeWrapping;

// Select sprite by UV offset/scale
function selectSprite(row, col, gridSize = 2) {
  atlas.offset.set(col / gridSize, 1 - (row + 1) / gridSize);
  atlas.repeat.set(1 / gridSize, 1 / gridSize);
}

// Select top-left sprite
selectSprite(0, 0);
```

## 材质纹理贴图

### PBR 纹理集

```javascript
const material = new THREE.MeshStandardMaterial({
  // Base color (sRGB)
  map: colorTexture,

  // Surface detail (Linear)
  normalMap: normalTexture,
  normalScale: new THREE.Vector2(1, 1),

  // Roughness (Linear, grayscale)
  roughnessMap: roughnessTexture,
  roughness: 1, // Multiplier

  // Metalness (Linear, grayscale)
  metalnessMap: metalnessTexture,
  metalness: 1, // Multiplier

  // Ambient occlusion (Linear, uses uv2)
  aoMap: aoTexture,
  aoMapIntensity: 1,

  // Self-illumination (sRGB)
  emissiveMap: emissiveTexture,
  emissive: 0xffffff,
  emissiveIntensity: 1,

  // Vertex displacement (Linear)
  displacementMap: displacementTexture,
  displacementScale: 0.1,
  displacementBias: 0,

  // Alpha (Linear)
  alphaMap: alphaTexture,
  transparent: true,
});

// Don't forget UV2 for AO
geometry.setAttribute("uv2", geometry.attributes.uv);
```

### 法线贴图类型

```javascript
// OpenGL style normals (default)
material.normalMapType = THREE.TangentSpaceNormalMap;

// Object space normals
material.normalMapType = THREE.ObjectSpaceNormalMap;
```

## 程序化纹理

### 噪声纹理

```javascript
function generateNoiseTexture(size = 256) {
  const data = new Uint8Array(size * size * 4);

  for (let i = 0; i < size * size; i++) {
    const value = Math.random() * 255;
    data[i * 4] = value;
    data[i * 4 + 1] = value;
    data[i * 4 + 2] = value;
    data[i * 4 + 3] = 255;
  }

  const texture = new THREE.DataTexture(data, size, size);
  texture.needsUpdate = true;
  return texture;
}
```

### 渐变纹理

```javascript
function generateGradientTexture(color1, color2, size = 256) {
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = 1;
  const ctx = canvas.getContext("2d");

  const gradient = ctx.createLinearGradient(0, 0, size, 0);
  gradient.addColorStop(0, color1);
  gradient.addColorStop(1, color2);

  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, size, 1);

  return new THREE.CanvasTexture(canvas);
}
```

## 纹理内存管理

### 释放纹理

```javascript
// Single texture
texture.dispose();

// Material textures
function disposeMaterial(material) {
  const maps = [
    "map",
    "normalMap",
    "roughnessMap",
    "metalnessMap",
    "aoMap",
    "emissiveMap",
    "displacementMap",
    "alphaMap",
    "envMap",
    "lightMap",
    "bumpMap",
    "specularMap",
  ];

  maps.forEach((mapName) => {
    if (material[mapName]) {
      material[mapName].dispose();
    }
  });

  material.dispose();
}
```

### 纹理池化

```javascript
class TexturePool {
  constructor() {
    this.textures = new Map();
    this.loader = new THREE.TextureLoader();
  }

  async get(url) {
    if (this.textures.has(url)) {
      return this.textures.get(url);
    }

    const texture = await new Promise((resolve, reject) => {
      this.loader.load(url, resolve, undefined, reject);
    });

    this.textures.set(url, texture);
    return texture;
  }

  dispose(url) {
    const texture = this.textures.get(url);
    if (texture) {
      texture.dispose();
      this.textures.delete(url);
    }
  }

  disposeAll() {
    this.textures.forEach((t) => t.dispose());
    this.textures.clear();
  }
}
```

## 性能优化建议

1. **使用 2 的幂次尺寸**：256、512、1024、2048
2. **压缩纹理**：Web 端使用 KTX2/Basis 格式
3. **使用纹理图集**：减少纹理切换
4. **启用 Mipmap**：用于远处物体
5. **限制纹理尺寸**：Web 端通常 2048 足够
6. **复用纹理**：相同纹理 = 更好的批处理

```javascript
// Check texture memory
console.log(renderer.info.memory.textures);

// Optimize for mobile
const maxSize = renderer.capabilities.maxTextureSize;
const isMobile = /iPhone|iPad|Android/i.test(navigator.userAgent);
const textureSize = isMobile ? 1024 : 2048;
```

## KTX2Loader BC3 Alpha 修复 (r183)

从 r183 起，`KTX2Loader` 正确处理带 Alpha 通道的 BC3 压缩纹理，修复了之前 Alpha 渲染不正确的问题。

## ISO 21496-1 Gainmap 元数据 (r183)

Three.js r183 支持 HDR 纹理中的 ISO 21496-1 gainmap 元数据，可对基于 gainmap 的 HDR 图片（如近期智能手机拍摄的照片）进行正确的色调映射。

## 参考

- `threejs-materials` - 将纹理应用到材质
- `threejs-loaders` - 加载纹理文件
- `threejs-shaders` - 自定义纹理采样

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 输出不能替代针对特定环境的验证、测试或专家审查。
- 缺少必要输入、权限、安全边界或成功标准时，应停下来请求澄清。
