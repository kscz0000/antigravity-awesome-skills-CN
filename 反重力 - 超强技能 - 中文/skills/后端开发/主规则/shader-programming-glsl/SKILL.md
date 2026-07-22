---
name: shader-programming-glsl
description: "编写高效 GLSL 着色器（顶点/片段）的专家指南，适用于 Web 和游戏引擎，涵盖语法、uniform 变量和常见特效。触发词：GLSL、着色器编程、WebGL、Three.js、顶点着色器、片段着色器、GPU编程、后处理效果、纹理生成、SDF、光线步进"
risk: safe
source: community
date_added: "2026-02-27"
---

# GLSL 着色器编程

## 概述

使用 GLSL（OpenGL 着色语言）编写 GPU 着色器的全面指南。学习语法、uniform 变量、varying 变量，以及 swizzle 操作和向量运算等用于视觉效果的关键数学概念。

## 适用场景

- 在 WebGL、Three.js 或游戏引擎中创建自定义视觉效果时
- 优化图形渲染性能时
- 实现后处理效果（模糊、泛光、色彩校正）时
- 在 GPU 上程序化生成纹理或几何体时

## 分步指南

### 1. 结构：顶点着色器 vs 片段着色器

理解渲染管线：
- **顶点着色器**：将 3D 坐标变换到 2D 屏幕空间（`gl_Position`）。
- **片段着色器**：为单个像素着色（`gl_FragColor`）。

```glsl
// 顶点着色器（基础）
attribute vec3 position;
uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;

void main() {
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
```

```glsl
// 片段着色器（基础）
uniform vec3 color;

void main() {
    gl_FragColor = vec4(color, 1.0);
}
```

### 2. Uniform 与 Varying

- `uniform`：对所有顶点/片段恒定的数据（从 CPU 传入）。
- `varying`：从顶点着色器插值传递到片段着色器的数据。

```glsl
// 传递 UV 坐标
varying vec2 vUv;

// 在顶点着色器中
void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}

// 在片段着色器中
void main() {
    // 基于 UV 的渐变
    gl_FragColor = vec4(vUv.x, vUv.y, 1.0, 1.0);
}
```

### 3. Swizzle 操作与向量运算

自由访问向量分量：`vec4 color = vec4(1.0, 0.5, 0.0, 1.0);`
- `color.rgb` -> `vec3(1.0, 0.5, 0.0)`
- `color.zyx` -> `vec3(0.0, 0.5, 1.0)`（重排序）

## 示例

### 示例 1：简单光线步进（SDF 球体）

```glsl
float sdSphere(vec3 p, float s) {
    return length(p) - s;
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = (fragCoord - 0.5 * iResolution.xy) / iResolution.y;
    vec3 ro = vec3(0.0, 0.0, -3.0); // 光线起点
    vec3 rd = normalize(vec3(uv, 1.0)); // 光线方向
    
    float t = 0.0;
    for(int i = 0; i < 64; i++) {
        vec3 p = ro + rd * t;
        float d = sdSphere(p, 1.0); // 球体半径 1.0
        if(d < 0.001) break;
        t += d;
    }
    
    vec3 col = vec3(0.0);
    if(t < 10.0) {
        vec3 p = ro + rd * t;
        vec3 normal = normalize(p);
        col = normal * 0.5 + 0.5; // 按法线着色
    }
    
    fragColor = vec4(col, 1.0);
}
```

## 最佳实践

- ✅ **推荐**：使用 `mix()` 进行线性插值，而非手动计算。
- ✅ **推荐**：使用 `step()` 和 `smoothstep()` 实现阈值判定和柔和边缘（避免 `if` 分支）。
- ✅ **推荐**：将数据打包进向量（`vec4`）以减少内存访问。
- ❌ **避免**：在循环中使用大量分支（`if-else`）；这会损害 GPU 并行性能。
- ❌ **避免**：在着色器内计算常量值；应在 CPU 端预计算（通过 uniform 传入）。

## 故障排查

**问题**：着色器编译通过但屏幕全黑。
**解决方案**：检查 `gl_Position.w` 是否正确（通常为 1.0）。检查 uniform 是否确实从宿主应用传入。验证 UV 坐标是否在 [0, 1] 范围内。

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不可将输出内容替代针对特定环境的验证、测试或专家评审。
- 当所需输入、权限、安全边界或成功标准缺失时，请停下来请求澄清。
