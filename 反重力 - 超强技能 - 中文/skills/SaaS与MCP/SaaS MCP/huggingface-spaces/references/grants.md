# 社区 GPU 赠款

当非 PRO 用户对 ZeroGPU 有很好的用例（开放研究 demo、业余项目、教育工具、机构展示）并且不想订阅时，他们可以从 Hugging Face 请求免费的社区赠款。

## 流程

1. **构建 Space。** 创建为 `--flavor cpu-basic`（用户不是 PRO，因此使用 `--flavor zero-a10g` 创建会在 `create_repo` 处失败）。仍然针对 ZeroGPU 编写应用代码 — `import spaces`、`@spaces.GPU`、模块作用域的 `.to("cuda")`。Space 在技术上将在 CPU 上运行，直到赠款被批准，但它将准备好立即切换。

   在此模式下，**你不能在真实推理中迭代**之前 — CPU Space 实际上不会运行重计算。让应用干净 BUILD 并 `RUNNING`（即使运行时在实际输入上会 OOM），然后提交。

2. **在 Space 上提交 Community Tab 讨论**。标题：

   ```
   Apply for a GPU community grant: <Personal|Company|Academic> project
   ```

   选择最接近的匹配。主体：

   ```
   Description of the app: one paragraph on what it does + who it's for.
   Justification: one paragraph on why this should run on ZeroGPU
   (open-source, research, educational, etc.).
   ```

   如果用户没有给出理由，合理的默认值是"非 PRO 用户想要构建公共 ZeroGPU 应用 — 如有帮助很乐意提供更多上下文。"

3. **等待。** 研究人员、修补匠和机构的开放和面向公众的应用程序通常会被批准。批准可能需要几天时间。

4. **批准后**，Space 自动移动到 ZeroGPU — 无需代码更改。用户回来后，你可以使用真实 GPU 访问进行迭代/优化。

## 何时建议

- 用户不在 PRO 上，但他们的用例清楚地适合 ZeroGPU（公共 ML demo，而不是私人工具）。
- 模型适合 `large`（在所选精度下 ≤ 48 GB VRAM）。

## 何时不建议

- 私人/商业/闭源项目 — 推动用户改为 PRO。
- 模型确实需要专用付费硬件（巨大的 LLM、vLLM/JAX/ONNX 作为主模型且初始化很重）— `canPay=True` 用户可以直接使用付费 flavor。
- 用户已经是 PRO — 他们拥有 ZeroGPU 访问；无需赠款。

## 以编程方式发布请求

```python
from huggingface_hub import HfApi

api = HfApi(token="hf_...")
api.create_discussion(
    repo_id="<ns>/<space>",
    repo_type="space",
    title="Apply for a GPU community grant: Personal project",
    description="<description and justification>",
)
```

必须在 Space 上启用 Community Tab（默认 — 保持启用）。