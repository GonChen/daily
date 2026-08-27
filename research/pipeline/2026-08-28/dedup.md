# 2026-08-28 去重基线

已逐条核对 2026-08-26、2026-08-27 的 ledger、selection、deep files 与 tracker。#35634、#36330、#36541、#4789、#17985 均为 8/27 新合入、此前未覆盖的事实主体。

- #35634 DeepEPv2 ElasticBuffer 不重复 8/26 的 vLLM DeepSeek V4 FlashInfer MoE-EP 或 SGLang shared-expert fusion；前者是 SGLang 的 capacity/fail-fast backend 契约。
- #36330 gfx950 MTP attention 不重复 8/25 的 gfx950 SWA attention 下界；模型、算子与服务 workload 不同。
- #36541 int32 KV wrap 不重复 8/26 的 TP batch invariance fallback；一个是地址溢出导致 draft NaN，另一个是 reduction order determinism。
- #4789 JIT manifest 不重复上期 FlashInfer MSA/KDA；衡量对象是宿主编译冷启动。
- #17985 MiniMax-M3 hybrid KV 不重复 8/27 的 TensorRT-LLM MSA reuse rollback；前者有 mixed NVFP4/FP8 cache route 与 3,600 秒 A/B。
