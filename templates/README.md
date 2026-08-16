# 日报模板约束

`daily-template.html` 是 2026-08-16 高质量增强版日报的冻结副本，也是后续日报的最低质量基线。

每日生成时必须：

- 保留 Executive readout、30 秒结论、分类详情、推理加速路线图、论文、宏观、深度解读和跟踪清单。
- 让 Executive readout、30 秒结论和深度解读提供可验证的内部跳转或可信外链。
- 重点检查 SGLang、vLLM、TensorRT-LLM、PyTorch，FlashAttention、FlashInfer、FlashMLA、cuDNN、cuBLAS，以及 DeepSeek、GLM、Kimi、Qwen。
- 每条明确区分事实、报道、传闻、论文主张和编辑推断。
- 优先一手来源，所有数字保留适用范围与口径，不把行情相关性写成因果。
- 验证桌面和手机视口，确保目录、锚点和外链可用。
- 更新 `docs/archive/index.html`：按日期倒序添加摘要、主题关键词和完整日报链接，并让当期页面能返回归档。

禁止使用通用 RSS 摘要或无编辑判断的自动卡片列表覆盖模板。
