# Stable Diffusion 提示词工程

## 目录

1. [提示词结构](#提示词结构)
2. [品质修饰词](#品质修饰词)
3. [光照](#光照)
4. [构图](#构图)
5. [艺术风格](#艺术风格)
6. [反向提示词](#反向提示词)
7. [进阶技巧](#进阶技巧)
8. [分类示例](#分类示例)

---

## 提示词结构

Stable Diffusion 对分层结构的提示词响应更好：

```
[主体], [视觉细节], [风格], [光照], [品质], [镜头/技法]
```

每增加一层就多一分精确度。从主体开始，逐步添加细节。

**好的写法：**
```
a warrior princess in golden armor, intricate filigree details,
fantasy art style, dramatic rim lighting, 8k uhd, highly detailed
```

**差的写法：**
```
princess
```

## 品质修饰词

添加到提示词末尾，提升整体品质：

### 高品质
- `masterpiece, best quality`
- `highly detailed, ultra detailed`
- `8k uhd, high resolution`
- `sharp focus, crisp details`
- `professional, award-winning`

### 渲染效果
- `ray tracing, global illumination`
- `physically based rendering`
- `subsurface scattering`
- `volumetric lighting`

### 摄影风格
- `shot on Canon EOS R5`
- `85mm f/1.4 lens`
- `DSLR quality`
- `film grain, Kodak Portra 400`

## 光照

光照决定了画面的情绪氛围：

| 类型 | 效果 | 用途 |
|------|------|------|
| `natural lighting` | 柔和、真实 | 户外场景 |
| `golden hour` | 温暖、金色 | 人像、风景 |
| `dramatic lighting` | 高对比度 | 动作、戏剧 |
| `rim lighting` | 轮廓发光 | 艺术人像 |
| `studio lighting` | 均匀、专业 | 产品、人像 |
| `neon lighting` | 彩色、都市 | 赛博朋克、夜景 |
| `candlelight` | 温暖、私密 | 私密场景 |
| `moonlight` | 冷调、神秘 | 夜景、奇幻 |
| `chiaroscuro` | 极端明暗对比 | 古典、戏剧 |
| `backlit` | 逆光、光晕 | 艺术风格 |
| `volumetric fog` | 大气感 | 奇幻、恐怖 |

## 构图

控制取景和视角：

| 术语 | 效果 |
|------|------|
| `close-up portrait` | 面部特写 |
| `full body shot` | 全身照 |
| `wide angle` | 广角、开阔 |
| `bird's eye view` | 俯瞰视角 |
| `low angle` | 仰拍（力量感） |
| `dutch angle` | 倾斜（紧张感） |
| `symmetrical` | 中心对称 |
| `rule of thirds` | 三分法构图 |
| `depth of field` | 背景虚化 |
| `macro` | 极限特写 |

## 艺术风格

### 按流派
- `art nouveau` — 有机曲线、装饰风格
- `art deco` — 几何、奢华
- `impressionism` — 可见笔触
- `surrealism` — 超现实、梦幻
- `baroque` — 戏剧性、华丽装饰
- `romanticism` — 情感化、自然

### 按媒介
- `oil painting` — 古典、有质感
- `watercolor` — 柔和、流动
- `pencil sketch` — 单色、线条
- `digital painting` — 干净、精细
- `vector art` — 简洁图形、扁平化
- `pixel art` — 复古、像素风
- `3d render` — 体积感、写实

### 按参考
- `trending on artstation` — 高品质数字艺术
- `unreal engine 5` — 写实 3D
- `octane render` — 高端渲染
- `studio ghibli` — 经典日式动漫

## 反向提示词

反向提示词用于排除不想要的元素。技能会按风格自动应用，
也可以通过 `--negative-prompt` 手动添加。

### 通用（适用大多数场景）
```
low quality, blurry, distorted, deformed, ugly,
bad anatomy, bad proportions, extra limbs,
watermark, text, signature, logo
```

### 写实风格
```
cartoon, anime, painting, illustration,
drawing, cgi, render, sketch, comic
```

### 艺术风格
```
photo, photograph, realistic, 3d render,
low quality, amateur
```

### 人像
```
deformed face, ugly face, bad eyes,
cross-eyed, asymmetric face, extra fingers
```

## 进阶技巧

### 词语权重
部分模型支持括号加权：
```
(masterpiece:1.4), (beautiful:1.2), landscape
```
权重越高 = 该元素越突出。

### 混合风格
组合不同风格获得独特效果：
```
cyberpunk city, art nouveau architecture, neon lights,
watercolor style with digital art details
```

### 渐进描述
从宏观到微观逐步细化：
```
epic landscape, mountain range at sunset,
snow-capped peaks reflecting golden light,
a lone traveler on a winding path below,
fantasy art, dramatic clouds, volumetric lighting
```

### 情绪词汇
定义画面情感基调的词语：
- `serene, peaceful, calm` — 宁静
- `epic, grand, majestic` — 史诗
- `dark, moody, ominous` — 暗黑
- `whimsical, playful, fun` — 趣味
- `ethereal, dreamy, mystical` — 梦幻
- `gritty, raw, intense` — 粗犷

## 分类示例

### 艺术人像
```
a young woman with flowing red hair, wind-blown,
freckles, green eyes, wearing a flower crown,
oil painting style, warm golden hour lighting,
masterpiece, highly detailed, soft focus background
```

### 奇幻风景
```
floating islands above clouds, waterfalls cascading into void,
ancient temple ruins with glowing runes, bioluminescent plants,
epic fantasy landscape, dramatic sunset, volumetric god rays,
concept art, matte painting, 8k uhd
```

### 赛博朋克场景
```
neon-lit cyberpunk alley in rain, holographic advertisements,
steam rising from grates, lone figure with umbrella,
blade runner aesthetic, moody atmosphere, reflections on wet ground,
cinematic composition, anamorphic lens flare
```

### 产品/物品
```
luxury wristwatch on marble surface,
crystal clear details, metal and glass textures,
professional product photography, studio lighting,
shallow depth of field, 4k, commercial quality
```

### 游戏素材
```
crystal sword with ice enchantment,
glowing blue runes along the blade, ornate silver handle,
game item concept art, clean background,
multiple angle views, pixel-perfect details
```

### 海报/封面
```
epic dragon perched on mountain peak, wings spread wide,
medieval castle in valley below, army approaching,
cinematic movie poster composition, dramatic sky,
bold contrast, fantasy art, highly detailed illustration
```
