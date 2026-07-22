---
name: display-captions
description: "在 Remotion 中显示字幕，支持 TikTok 风格页面和单词高亮。触发词：captions、subtitles、display、tiktok、highlight、remotion"
metadata:
  tags: captions, subtitles, display, tiktok, highlight
---

# 在 Remotion 中显示字幕

本指南介绍如何在 Remotion 中显示字幕，假设你已经有了 `Caption` 格式的字幕。

## 前提条件

首先，需要安装 @remotion/captions 包。
如果尚未安装，请使用以下命令：

```bash
npx remotion add @remotion/captions # If project uses npm
bunx remotion add @remotion/captions # If project uses bun
yarn remotion add @remotion/captions # If project uses yarn
pnpm exec remotion add @remotion/captions # If project uses pnpm
```

## 创建页面

使用 `createTikTokStyleCaptions()` 将字幕分组到页面中。`combineTokensWithinMilliseconds` 选项控制一次显示多少个单词：

```tsx
import {useMemo} from 'react';
import {createTikTokStyleCaptions} from '@remotion/captions';
import type {Caption} from '@remotion/captions';

// 字幕切换频率（毫秒）
// 值越大 = 每页单词越多
// 值越小 = 单词越少（更逐词显示）
const SWITCH_CAPTIONS_EVERY_MS = 1200;

const {pages} = useMemo(() => {
  return createTikTokStyleCaptions({
    captions,
    combineTokensWithinMilliseconds: SWITCH_CAPTIONS_EVERY_MS,
  });
}, [captions]);
```

## 使用 Sequence 渲染

遍历页面并在 `<Sequence>` 中渲染每个页面。从页面时间计算起始帧和时长：

```tsx
import {Sequence, useVideoConfig, AbsoluteFill} from 'remotion';
import type {TikTokPage} from '@remotion/captions';

const CaptionedContent: React.FC = () => {
  const {fps} = useVideoConfig();

  return (
    <AbsoluteFill>
      {pages.map((page, index) => {
        const nextPage = pages[index + 1] ?? null;
        const startFrame = (page.startMs / 1000) * fps;
        const endFrame = Math.min(
          nextPage ? (nextPage.startMs / 1000) * fps : Infinity,
          startFrame + (SWITCH_CAPTIONS_EVERY_MS / 1000) * fps,
        );
        const durationInFrames = endFrame - startFrame;

        if (durationInFrames <= 0) {
          return null;
        }

        return (
          <Sequence
            key={index}
            from={startFrame}
            durationInFrames={durationInFrames}
          >
            <CaptionPage page={page} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
```

## 单词高亮

字幕页面包含 `tokens`，你可以用它来高亮当前正在说的单词：

```tsx
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import type {TikTokPage} from '@remotion/captions';

const HIGHLIGHT_COLOR = '#39E508';

const CaptionPage: React.FC<{page: TikTokPage}> = ({page}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // 当前时间相对于序列开始
  const currentTimeMs = (frame / fps) * 1000;
  // 通过添加页面开始时间转换为绝对时间
  const absoluteTimeMs = page.startMs + currentTimeMs;

  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div style={{fontSize: 80, fontWeight: 'bold', whiteSpace: 'pre'}}>
        {page.tokens.map((token) => {
          const isActive =
            token.fromMs <= absoluteTimeMs && token.toMs > absoluteTimeMs;

          return (
            <span
              key={token.fromMs}
              style={{color: isActive ? HIGHLIGHT_COLOR : 'white'}}
            >
              {token.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```