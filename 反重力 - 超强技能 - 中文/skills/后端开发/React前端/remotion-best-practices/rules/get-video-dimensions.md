---
name: get-video-dimensions
description: "使用 Mediabunny 获取视频文件的宽度和高度。触发词：dimensions、width、height、resolution、size、video、remotion"
metadata:
  tags: dimensions, width, height, resolution, size, video
---

# 使用 Mediabunny 获取视频尺寸

Mediabunny 可以提取视频文件的宽度和高度。它适用于浏览器、Node.js 和 Bun 环境。

## 获取视频尺寸

```tsx
import { Input, ALL_FORMATS, UrlSource } from "mediabunny";

export const getVideoDimensions = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src, {
      getRetryDelay: () => null,
    }),
  });

  const videoTrack = await input.getPrimaryVideoTrack();
  if (!videoTrack) {
    throw new Error("No video track found");
  }

  return {
    width: videoTrack.displayWidth,
    height: videoTrack.displayHeight,
  };
};
```

## 使用方法

```tsx
const dimensions = await getVideoDimensions("https://remotion.media/video.mp4");
console.log(dimensions.width);  // 例如 1920
console.log(dimensions.height); // 例如 1080
```

## 与本地文件一起使用

对于本地文件，使用 `FileSource` 代替 `UrlSource`：

```tsx
import { Input, ALL_FORMATS, FileSource } from "mediabunny";

const input = new Input({
  formats: ALL_FORMATS,
  source: new FileSource(file), // 来自输入或拖放的 File 对象
});

const videoTrack = await input.getPrimaryVideoTrack();
const width = videoTrack.displayWidth;
const height = videoTrack.displayHeight;
```

## 在 Remotion 中与 staticFile 一起使用

```tsx
import { staticFile } from "remotion";

const dimensions = await getVideoDimensions(staticFile("video.mp4"));
```