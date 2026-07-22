# 发布指南 — 媒体规格和流程

## 媒体规格

### 照片（IMAGE）
| 属性 | 要求 |
|-------------|-----------|
| 格式 | JPEG（必需 — PNG/WebP 由 publish.py 通过 Pillow 自动转换） |
| 最小分辨率 | 320 x 320 px |
| 最大分辨率 | 1080 x 1350 px（推荐） |
| 宽高比 | 4:5（竖版）到 1.91:1（横版） |
| 最大大小 | 8 MB |
| 色彩空间 | sRGB |

### 视频（VIDEO）
| 属性 | 要求 |
|-------------|-----------|
| 格式 | MP4（H.264 编码） |
| 最小分辨率 | 640 x 640 px |
| 最大分辨率 | 1920 x 1080 px |
| 时长 | 3 秒到 60 分钟 |
| 最大大小 | 250 MB（推荐 < 100 MB） |
| 帧率 | 23-60 fps |
| 音频 | AAC，48kHz 采样率 |

### Reel（REELS）
| 属性 | 要求 |
|-------------|-----------|
| 格式 | MP4（H.264 编码） |
| 宽高比 | 9:16（竖版，必需） |
| 推荐分辨率 | 1080 x 1920 px |
| 时长 | 3 秒到 15 分钟 |
| 最大大小 | 250 MB |
| 音频 | 必需（可以是静音，但音轨必须存在） |

### Story（STORIES）
| 属性 | 要求 |
|-------------|-----------|
| 照片格式 | JPEG |
| 视频格式 | MP4 |
| 宽高比 | 9:16（推荐 1080 x 1920 px） |
| 视频时长 | 最长 60 秒 |
| 消失 | 24 小时后 |

### 轮播（CAROUSEL_ALBUM）
| 属性 | 要求 |
|-------------|-----------|
| 项目数 | 2 到 10 张图片/视频 |
| 允许类型 | 照片和视频混合 |
| 每项规格 | 遵循上述 IMAGE 或 VIDEO 规格 |
| 宽高比 | 所有项目必须具有相同宽高比 |

## 发布流程（两步法）

### 照片完整流程

```
1. 本地上传 → Imgur（如果是本地路径）
   POST https://api.imgur.com/3/image
   → 返回公开 URL

2. 创建容器
   POST /{user-id}/media
     image_url=<公开URL>
     caption=<文字>
   → 返回 container_id

3. 发布容器
   POST /{user-id}/media_publish
     creation_id=<container_id>
   → 返回 ig_media_id + permalink
```

### 视频/Reel 完整流程

```
1. 本地上传 → Imgur（如果是本地路径）

2. 创建容器
   POST /{user-id}/media
     video_url=<公开URL>
     caption=<文字>
     media_type=VIDEO（或 REELS）
   → 返回 container_id

3. 等待处理（轮询）
   GET /{container_id}?fields=status_code
   每 10s 重复直到 status = FINISHED
   （超时：5 分钟）

4. 发布容器
   POST /{user-id}/media_publish
     creation_id=<container_id>
   → 返回 ig_media_id
```

### 轮播完整流程

```
1. 对每个项目（2-10）：
   POST /{user-id}/media
     image_url=<URL>（或 video_url）
     is_carousel_item=true
   → 返回 item_container_id

2. 创建轮播容器
   POST /{user-id}/media
     media_type=CAROUSEL
     children=[item1_id, item2_id, ...]
     caption=<文字>
   → 返回 carousel_container_id

3. 发布
   POST /{user-id}/media_publish
     creation_id=<carousel_container_id>
   → 返回 ig_media_id
```

## 状态管道（publish.py）

```
draft → approved → scheduled → container_created → published
                                      ↓
                                    failed
```

| 状态 | 含义 | 下一步操作 |
|--------|-------------|--------------|
| `draft` | 草稿，不会自动发布 | `--approve --id X` |
| `approved` | 已批准发布 | `schedule.py --process` |
| `scheduled` | 已安排到未来日期 | 等待时间 |
| `container_created` | 容器已在 API 创建，等待发布 | 自动恢复 |
| `published` | 发布成功 | 完成 |
| `failed` | 发布错误 | 检查 error_msg，可能重试 |

## 崩溃恢复

如果进程在 `container_created` 和 `published` 之间崩溃：
1. `schedule.py --process` 检测状态为 `container_created` 的帖子
2. 通过 API 验证容器是否仍然有效
3. 如果有效 → 发布
4. 如果无效 → 重新创建容器并重新发布

## 通过 Imgur 上传本地文件

`publish.py` 检测路径是否为本地（不以 http 开头）：

1. 读取本地文件
2. 如需要转换为 JPEG（通过 Pillow）
3. 匿名上传到 Imgur（POST https://api.imgur.com/3/image）
4. 使用返回的 URL 作为 Graph API 的 `image_url`

**配置：** 在 config.py 或环境变量中设置 `IMGUR_CLIENT_ID`。

## 标题和话题标签

### 限制
- 标题：最多 2,200 个字符
- 话题标签：每帖最多 30 个
- 提及（@）：无官方限制

### 模板（通过 templates.py）
```python
caption_template = "新促销：{产品}！{折扣}% OFF"
# 使用变量：产品="运动鞋", 折扣=30
# 结果："新促销：运动鞋！30% OFF"
```

### 模板中的话题标签
话题标签存储为 JSON 数组，添加到标题末尾：
```
渲染后的标题 + "\n\n" + " ".join(hashtags)
```
