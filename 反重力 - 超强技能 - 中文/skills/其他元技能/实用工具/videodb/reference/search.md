# 搜索指南

VideoDB 提供强大的搜索能力，可在视频内或跨集合搜索内容。

## 搜索类型

### 语义搜索

语义搜索使用自然语言理解来查找概念上相关的内容，即使没有精确的关键词匹配：

```python
from videodb import SearchType

results = video.search(
    query="product announcement",
    search_type=SearchType.semantic,
)
```

### 关键词搜索

精确关键词匹配：

```python
results = video.search(
    query="artificial intelligence",
    search_type=SearchType.keyword,
)
```

### 场景搜索

视觉场景搜索（可能需要付费计划）：

```python
from videodb import SearchType, IndexType

results = video.search(
    query="people in a meeting room",
    search_type=SearchType.semantic,
    index_type=IndexType.scene,
    scene_index_id="scene-idx-123",  # 可选，目标特定场景索引
)
```

## 索引类型

| 索引类型 | 描述 |
|----------|------|
| `IndexType.spoken_word` | 搜索语音内容（转录文本） |
| `IndexType.scene` | 搜索视觉场景 |

## 前提条件

### 语音搜索

视频必须先索引语音：

```python
video.index_spoken_words(force=True)  # force=True 跳过已索引的情况
```

### 场景搜索

视频必须先索引场景：

```python
from videodb import SceneExtractionType

scene_index_id = video.index_scenes(
    extraction_type=SceneExtractionType.shot_based,
    prompt="Describe what's happening in each scene",
)
```

或使用 `index_visuals`：

```python
scene_index_id = video.index_visuals(
    prompt="Describe the visual content",
    batch_config={"batch_size": 10, "batch_duration": 30},
)
```

## 搜索参数

```python
results = video.search(
    query="your query",
    search_type=SearchType.semantic,
    index_type=IndexType.spoken_word,
    result_threshold=10,        # 最大结果数
    score_threshold=0.5,        # 最小相关性分数
    scene_index_id=None,        # 目标特定场景索引（通过 **kwargs 传递）
    filter=[],                  # 元数据过滤器（场景搜索）
)
```

### 参数说明

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `query` | `str` | 必需 | 搜索查询 |
| `search_type` | `SearchType` | `SearchType.semantic` | 搜索类型 |
| `index_type` | `IndexType` | `IndexType.spoken_word` | 索引类型 |
| `result_threshold` | `int` | `None` | 最大结果数 |
| `score_threshold` | `float` | `None` | 最小相关性分数 |
| `scene_index_id` | `str` | `None` | 目标场景索引 ID（通过 `**kwargs` 传递） |
| `filter` | `list` | `[]` | 元数据过滤器 |

> **注意：** `filter` 是 `video.search()` 的显式命名参数。`scene_index_id` 通过 `**kwargs` 传递给 API。

> **重要：** 当没有匹配结果时，`video.search()` 会抛出 `InvalidRequestError`，消息为 `"No results found"`。始终用 try/except 包装搜索调用。对于场景搜索，使用 `score_threshold=0.3` 或更高来过滤低相关性噪音。

## SearchResult 对象

搜索返回 `SearchResult` 对象：

```python
results = video.search("query", search_type=SearchType.semantic)

# 获取匹配片段
shots = results.get_shots()

# 编译所有片段为流 URL
stream_url = results.compile()

# 在浏览器中打开
player_url = results.play()
```

### SearchResult 方法

| 方法 | 返回值 | 描述 |
|------|--------|------|
| `results.get_shots()` | `list[Shot]` | 获取匹配片段列表 |
| `results.compile()` | `str` | 将所有片段编译为流 URL |
| `results.play()` | `str` | 在浏览器中打开编译后的流 |

## Shot 对象

每个匹配片段是一个 `Shot`：

```python
for shot in shots:
    print(f"Video: {shot.video_title}")
    print(f"Time: {shot.start}s - {shot.end}s")
    print(f"Text: {shot.text}")
    print(f"Score: {shot.search_score}")
    
    # 流传输此片段
    stream_url = shot.generate_stream()
    
    # 在浏览器中打开
    player_url = shot.play()
```

### Shot 属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `shot.video_id` | `str` | 源视频 ID |
| `shot.video_length` | `float` | 源视频时长 |
| `shot.video_title` | `str` | 源视频标题 |
| `shot.start` | `float` | 开始时间（秒） |
| `shot.end` | `float` | 结束时间（秒） |
| `shot.text` | `str` | 匹配的文本内容 |
| `shot.search_score` | `float` | 搜索相关性分数 |

### Shot 方法

| 方法 | 返回值 | 描述 |
|------|--------|------|
| `shot.generate_stream()` | `str` | 流式传输此特定片段 |
| `shot.play()` | `str` | 在浏览器中打开片段流 |

## 集合搜索

跨集合中的所有视频搜索：

```python
results = coll.search(
    query="product demo",
    search_type=SearchType.semantic,
    index_type=IndexType.spoken_word,
)
```

> **注意：** 集合搜索仅支持语义搜索。关键词和场景搜索会抛出 `NotImplementedError`。

## 完整示例

### 搜索并编译高光

```python
import videodb
from videodb import SearchType

conn = videodb.connect()
coll = conn.get_collection()
video = coll.get_video("your-video-id")

# 索引语音
video.index_spoken_words(force=True)

# 搜索
try:
    results = video.search(
        query="key features",
        search_type=SearchType.semantic,
        score_threshold=0.5,
    )
    
    # 获取片段
    shots = results.get_shots()
    print(f"Found {len(shots)} matches")
    
    # 编译高光集锦
    stream_url = results.compile()
    print(f"Highlight reel: {stream_url}")
    
except Exception as e:
    print(f"No results found: {e}")
```

### 场景搜索

```python
from videodb import SearchType, IndexType, SceneExtractionType

# 索引场景
scene_index_id = video.index_scenes(
    extraction_type=SceneExtractionType.shot_based,
    prompt="Describe each scene",
)

# 搜索场景
try:
    results = video.search(
        query="people working together",
        search_type=SearchType.semantic,
        index_type=IndexType.scene,
        scene_index_id=scene_index_id,
        score_threshold=0.3,
    )
    
    shots = results.get_shots()
    for shot in shots:
        print(f"Scene at {shot.start}s: {shot.text}")
        
except Exception as e:
    print(f"No results found: {e}")
```

## 提示

- **先索引**：搜索前确保视频已索引（语音或场景）。
- **使用 try/except**：`search()` 在无结果时抛出异常。
- **调整阈值**：使用 `score_threshold` 过滤低相关性结果。
- **场景搜索阈值**：场景搜索建议使用 `score_threshold=0.3` 或更高。
- **编译结果**：使用 `results.compile()` 快速创建高光集锦。
