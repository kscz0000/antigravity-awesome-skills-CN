# GGUF 量化指南

GGUF 量化格式与模型转换的完整指南。

## 目录

- Hub 优先的量化选择
- 量化格式
- 模型转换
- K-Quantization 方法
- 质量测试
- 用途指南
- 模型规模缩放
- 查找预量化模型
- 重要性矩阵（`imatrix`）
- 故障排查

## Hub 优先的量化选择

在使用通用表格之前，先打开模型仓库：

```text
https://huggingface.co/<repo>?local-app=llama.cpp
```

优先采用抓取的 `?local-app=llama.cpp` 页面文本或 HTML 中 `Hardware compatibility` 段落展示的精确量化标签和大小。然后在以下位置确认匹配的文件名：

```text
https://huggingface.co/api/models/<repo>/tree/main?recursive=true
```

优先使用 Hub 页面；当仓库页面未给出明确推荐时，再回退到下面的通用启发式。

## 量化格式

**GGUF**（GPT-Generated Unified Format）—— llama.cpp 模型的标准格式。

### 格式对比

| Format | Perplexity | Size (7B) | Tokens/sec | Notes |
|--------|------------|-----------|------------|-------|
| FP16 | 5.9565 (baseline) | 13.0 GB | 15 tok/s | Original quality |
| Q8_0 | 5.9584 (+0.03%) | 7.0 GB | 25 tok/s | Nearly lossless |
| **Q6_K** | 5.9642 (+0.13%) | 5.5 GB | 30 tok/s | Best quality/size |
| **Q5_K_M** | 5.9796 (+0.39%) | 4.8 GB | 35 tok/s | Balanced |
| **Q4_K_M** | 6.0565 (+1.68%) | 4.1 GB | 40 tok/s | **Recommended** |
| Q4_K_S | 6.1125 (+2.62%) | 3.9 GB | 42 tok/s | Faster, lower quality |
| Q3_K_M | 6.3184 (+6.07%) | 3.3 GB | 45 tok/s | Small models only |
| Q2_K | 6.8673 (+15.3%) | 2.7 GB | 50 tok/s | Not recommended |

**推荐**：使用 **Q4_K_M** 以获得质量与速度的最佳平衡。

## 模型转换

### Hugging Face 转 GGUF

```bash
# 1. Download Hugging Face model
hf download meta-llama/Llama-2-7b-chat-hf \
    --local-dir models/llama-2-7b-chat/

# 2. Convert to FP16 GGUF
python convert_hf_to_gguf.py \
    models/llama-2-7b-chat/ \
    --outtype f16 \
    --outfile models/llama-2-7b-chat-f16.gguf

# 3. Quantize to Q4_K_M
./llama-quantize \
    models/llama-2-7b-chat-f16.gguf \
    models/llama-2-7b-chat-Q4_K_M.gguf \
    Q4_K_M
```

### 批量量化

```bash
# Quantize to multiple formats
for quant in Q4_K_M Q5_K_M Q6_K Q8_0; do
    ./llama-quantize \
        model-f16.gguf \
        model-${quant}.gguf \
        $quant
done
```

## K-Quantization 方法

**K-quants** 使用混合精度以获得更好的质量：
- Attention weights: Higher precision
- Feed-forward weights: Lower precision

**Variants**:
- `_S` (Small): Faster, lower quality
- `_M` (Medium): Balanced (recommended)
- `_L` (Large): Better quality, larger size

**Example**: `Q4_K_M`
- `Q4`: 4-bit quantization
- `K`: Mixed precision method
- `M`: Medium quality

## 质量测试

```bash
# Calculate perplexity (quality metric)
./llama-perplexity \
    -m model.gguf \
    -f wikitext-2-raw/wiki.test.raw \
    -c 512

# Lower perplexity = better quality
# Baseline (FP16): ~5.96
# Q4_K_M: ~6.06 (+1.7%)
# Q2_K: ~6.87 (+15.3% - too much degradation)
```

## 用途指南

### 通用目的（聊天机器人、助手）
```
Q4_K_M - Best balance
Q5_K_M - If you have extra RAM
```

### 代码生成
```
Q5_K_M or Q6_K - Higher precision helps with code
```

### 创意写作
```
Q4_K_M - Sufficient quality
Q3_K_M - Acceptable for draft generation
```

### 技术/医学
```
Q6_K or Q8_0 - Maximum accuracy
```

### 边缘设备（树莓派）
```
Q2_K or Q3_K_S - Fit in limited RAM
```

## 模型规模缩放

### 7B 参数模型

| Format | Size | RAM needed |
|--------|------|------------|
| Q2_K | 2.7 GB | 5 GB |
| Q3_K_M | 3.3 GB | 6 GB |
| Q4_K_M | 4.1 GB | 7 GB |
| Q5_K_M | 4.8 GB | 8 GB |
| Q6_K | 5.5 GB | 9 GB |
| Q8_0 | 7.0 GB | 11 GB |

### 13B 参数模型

| Format | Size | RAM needed |
|--------|------|------------|
| Q2_K | 5.1 GB | 8 GB |
| Q3_K_M | 6.2 GB | 10 GB |
| Q4_K_M | 7.9 GB | 12 GB |
| Q5_K_M | 9.2 GB | 14 GB |
| Q6_K | 10.7 GB | 16 GB |

### 70B 参数模型

| Format | Size | RAM needed |
|--------|------|------------|
| Q2_K | 26 GB | 32 GB |
| Q3_K_M | 32 GB | 40 GB |
| Q4_K_M | 41 GB | 48 GB |
| Q4_K_S | 39 GB | 46 GB |
| Q5_K_M | 48 GB | 56 GB |

**70B 模型推荐**：使用 Q3_K_M 或 Q4_K_S 以适配消费级硬件。

## 查找预量化模型

使用 llama.cpp app 过滤器在 Hub 上搜索：

```text
https://huggingface.co/models?apps=llama.cpp&sort=trending
https://huggingface.co/models?search=<term>&apps=llama.cpp&sort=trending
https://huggingface.co/models?search=<term>&apps=llama.cpp&num_parameters=min:0,max:24B&sort=trending
```

针对特定仓库，打开：

```text
https://huggingface.co/<repo>?local-app=llama.cpp
https://huggingface.co/api/models/<repo>/tree/main?recursive=true
```

然后无需额外 Hub 工具，直接从 Hub 启动：

```bash
llama-cli -hf <repo>:Q4_K_M
llama-server -hf <repo>:Q4_K_M
```

如果需要从 tree API 获取精确文件名：

```bash
llama-server --hf-repo <repo> --hf-file <filename.gguf>
```

## 重要性矩阵（imatrix）

**What**: Calibration data to improve quantization quality.

**Benefits**:
- 10-20% perplexity improvement with Q4
- Essential for Q3 and below

**Usage**:
```bash
# 1. Generate importance matrix
./llama-imatrix \
    -m model-f16.gguf \
    -f calibration-data.txt \
    -o model.imatrix

# 2. Quantize with imatrix
./llama-quantize \
    --imatrix model.imatrix \
    model-f16.gguf \
    model-Q4_K_M.gguf \
    Q4_K_M
```

**Calibration data**:
- Use domain-specific text (e.g., code for code models)
- ~100MB of representative text
- Higher quality data = better quantization

## 故障排查

**Model outputs gibberish**:
- Quantization too aggressive (Q2_K)
- Try Q4_K_M or Q5_K_M
- Verify model converted correctly

**Out of memory**:
- Use lower quantization (Q4_K_S instead of Q5_K_M)
- Offload fewer layers to GPU (`-ngl`)
- Use smaller context (`-c 2048`)

**Slow inference**:
- Higher quantization uses more compute
- Q8_0 much slower than Q4_K_M
- Consider speed vs quality trade-off