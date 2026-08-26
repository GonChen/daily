# 2026-08-27 去重基线

基线为 2026-08-25、2026-08-26 两期产品事实和 `research/tracker.md`。以下主题不得以相同事实再次入选：SGLang DP rank-local FlashInfer EXTEND warmup（#36219）、DeepSeek V4 FlashInfer MoE-EP（vLLM #49636）、TP batch-invariant deterministic fallback（#51292）、SM120 NVFP4 attention/LSE API（FlashInfer #4502）、DeepSeek V4 shared-expert topology gate（SGLang #35505）、NVIDIA AgentX 机架级声明、MI350X SWA lower-bound、persistent matmul 调优表、SM120 SVDQuant LoRA、DeepSeek V4 live-adapter LoRA，以及 TensorRT-LLM speculative sampling admission。

本轮候选均为 2026-08-26 合入的不同 PR。#30859 的长序列 FP8 KV 指针扩展留作雷达，不与上期的 `return_lse` 或共享专家事实混同。
