---
name: get-video-duration
description: "使用 Mediabunny 获取视频文件的时长（秒）。触发词：duration、video、length、time、seconds、remotion"
metadata:
  tags: duration, video, length, time, seconds
---

# 使用 Mediabunny 获取视频时长

Mediabunny 可以提取视频文件的时长。它适用于浏览器、Node.js 和 Bun 环境。

## 获取视频时长

```tsx
import { Input, ALL_FORMATS, UrlSource } from "mediabunny";

export const getVideoDuration = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src, {
      getRetryDelay: () => null,
    }),
  });

  const durationInSeconds = await input.computeDuration();
  return durationInSeconds;
};
```

## 使用方法

```tsx
const duration = await getVideoDuration("https://remotion.media/video.mp4");
console.log(duration); // 例如 10.5（秒）
```

## 与本地文件一起使用

对于本地文件，使用 `FileSource` 代替 `UrlSource`：

```tsx
import { Input, ALL_FORMATS, FileSource } from "mediabunny";

const input = new Input({
  formats: ALL_FORMATS,
  source: new FileSource(file), // 来自输入或拖放的 File 对象
});

const durationInSeconds = await input.computeDuration();
```

## 在 Remotion 中与 staticFile 一起使用

```tsx
import { staticFile } from "remotion";

const duration = await getVideoDuration(staticFile("video.mp4"));
```