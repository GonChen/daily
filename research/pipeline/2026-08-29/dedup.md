# 2026-08-29 去重基线

已核对 2026-08-27 与 2026-08-28 ledger、selection、深挖和 tracker。本期不得原样重复：

- 8/28：SGLang #35634 DeepEPv2 ElasticBuffer capacity/fail-fast；#36330 gfx950 Qwen3.5 MTP attention；#36541 AITER int32 KV 2 GiB wrap；FlashInfer #4789 MoE manifest cold JIT；TensorRT-LLM #17985 MiniMax-M3 hybrid NVFP4/FP8 KV staging。
- 8/27：SGLang #36456 Hopper MXFP4 OOB；vLLM #52914 DP pause idle；SGLang #35343 TP autotune consensus；FlashInfer #4030 MSA top-k；FlashInfer #4728 Cake KDA persistent。
- 仅在有新一手事实（新 benchmark、release、CI/事故、实质实现或配置边界）时，可跟进以上 tracker 条目；版本 bump、重命名、文档、普通 CI 改动不进 Top 5。

本期优先检查：异步 KV load/fence、DeepSeek V4 的 Hopper/AMD 路径、Blackwell MoE grid barrier、dynamic-tree/speculative 与 agent/API security/streaming 语义。
