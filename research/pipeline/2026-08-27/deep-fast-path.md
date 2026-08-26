# 深挖：性能 fast path 的准入边界（2026-08-27）

选题：四个 2026-08-26 合入 PR 如何把"是否走快路径"编码为可机器判定的形状/语义条件，以及条件不满足时的回退。一手来源仅 SGLang #36456、#30859 与 FlashInfer #4030、#4728；所有数字均为 PR 作者报告，无独立复现。

## 发生了什么

四个 PR 都不靠运行时探针决定路径，而是用编译期/调度期常量做准入：#36456 用 K-tile 合法地址修复 Hopper MXFP4 越界读，#30859 把 FP8 k-cache 的 `token_id` 扩成 int64 以避免指针算术溢出，#4030 用形状常量在三种 top-k kernel 间分派，#4728 用 occupancy/roofline 模型在 piece-persistent M128 与 direct M128 间选择。共同点：fast path 的准入条件全部可在调用入口静态求值，回退路径与 fast path 共享同一公共 API 与同一正确性口径。

## 事实表（作者报告）

| PR | fast path | 准入条件 | 回退 | 关键数字 |
|---|---|---|---|---|
| #36456 | Hopper MXFP4 MoE scale 走 `block_k=128` unmasked load | SM90、`has_triton_kernels`、gpt-oss 类 K 非 128 倍数时对 scale K 维补 pad 至 `round_up(K,128)` | 不走该分支；`block_k=64` 被作者拒绝（吞吐 −13% 至 −23%） | compute-sanitizer 66→0 错；CI coredump 3→0；GPQA 0.0→0.6313；端到端 −0.05% 至 +0.64%（噪声） |
| #30859 | FP8 k-cache quant/dequant 用 `token_id` 缩放指针偏移 | 三处 kernel（dsa quant/dequant、dsv4 quant/dequant）默认走；无形状门 | 无（纯加固，对所有 token_id 生效） | 典型 stride 512 下约 4.2M tokens 处 int32 回绕；H200 34 passed/76 subtests；GSM8K 1319 例 accuracy 96.66%、errors 0 |
| #4030 | SM12x MSA chunked top-k（row-per-CTA 或 q-tiled partial + merge） | SM120/121；`not per_token_nvp`；`_MIN_BLOCKS(32) < n_mid ≤ _MAX_CHUNKS(16)*_MAX_CHUNK_BLOCKS(128)`；scratch `rows*num_chunks*topk*8 ≤ 128MB` | 落回 count-rank / radix 单 kernel 路径；per-token `num_valid_pages` 永不走 chunked | batch1 MTP 2k–32k ratio 0.73–0.98→1.20–1.36；新 top-k 对旧 kernel decode 1.4–2.2×、8k–32k prefill 1.2–2.1×；batch128 端到端 ratio 1.00–1.03 |
| #4728 | Cake KDA recurrence-piece persistent M128 | CC 10.0/10.3 且 `sm_count∈{148,152}`；`uniform_sequences`；`prefill_workspace is None`；`seq_order is None`；`initial_state is not None`；`num_heads≠12`；`num_sequences*num_heads > sm_count`；roofline `piece_ns < direct_ns` | direct M128 / legacy persistent / BT16 / 一般 M128；CUDA Graph 一律走非 piece 路径 | 29-shape cold-L2 CUPTI 几何均值 vs FlashKDA 2.568×–2.725×；vs frozen #4605 1.018×–1.045×；BF16 atol=rtol=1e-2 |

## 共同准入/回退机制

1. **准入条件可静态求值**。#4030 的分派只依赖 `total_qo_len`、`num_qo_heads`、`nvp_scalar`、`force_begin/end_blocks`、`topk`，作者明确写 "Everything here is shape-constant, so CUDA-graph safe"；#4728 的 `piece_persistent_candidate` 全部是入口参数与设备属性（CC、SM 数、`initial_state` 是否给出、`seq_order` 是否给出、`num_heads`、`num_sequences`）；#36456 的 pad 在 weight swizzle 阶段按 `k_size` 计算；#30859 无门，对所有 `token_id` 生效。
2. **回退是同一 API 的另一变体，不是失败**。#4728 在 `route==PIECE_PERSISTENT_M128` 但 `piece_persistent_candidate` 不成立时显式改写为 `_direct_m128_route(...)`；roofline 解析失败或 `piece_ns>=direct_ns` 时抛 `RuntimeError`（"piece-persistent route selected without a resolved roofline advantage"），即回退是确定性的、可观测的。#4030 的 `chunked` 标志在 scratch 超限时被置 False，自然落回单 kernel。#36456 的 pad 对 `w2`（K=768，128 倍数）是 no-op，对非 Hopper 分支不触发。
3. **正确性口径在 fast path 与回退间一致**。#4030 用测试钉死 chunked 与 count-rank/radix 的选择恒等（同一 bit-key 与 tie order，含 NaN、forced blocks、ragged q-tile 尾）；#4728 的 piece 与 direct 共用 BF16 `atol=rtol=1e-2`，且 piece 路径要求 caller-owned in-place initial state，使中间状态在 device-scope release/acquire 间传递，最终消费者重置 ready counter，保证后续 eager 调用从同一状态出发。
4. **CUDA Graph 的处理是显式边界**。#4030 因分派仅依赖形状常量而 graph-safe；#4728 反向——piece 路径需要 host 端 task-bin 规划与 inter-kernel handoff，故 `seq_order` 或显式 workspace 存在时不选 piece，CUDA Graph capture 继续走已验证的非 piece 路径，且 piece workspace 在 capture 前需 warm 最大形状。

## 对部署/成本/能力意味着什么

- **运维不需要为 fast path 配开关**：四个 PR 都没有引入用户可调旋钮，准入由形状/设备/语义自动决定。升级即得，但收益只落在满足准入条件的负载上。
- **#36456 是正确性修复而非性能项**：吞吐变化在噪声内（−0.05% 至 +0.64%），但消除了 gpt-oss-120b TP4 在 H100 内存配置下的间歇性 coredump。部署 gpt-oss MXFP4 on Hopper 的用户应视为必装；SM100（B200）路径的同类 unmasked load 未处理，4-gpu-b200 当前绿但不在此 PR 覆盖内。
- **#30859 是长上下文加固**：在约 4.2M tokens（stride 512）前 int32 回绕，对当前主流负载无性能影响，但为超长 KV 池消除潜在静默错位。无服务 A/B，不应表述为性能提升。
- **#4030 的收益集中在小 batch/长序列**：batch128 因 proxy 主导端到端 ratio 仍 1.00–1.03，即吞吐不变；MTP batch1 长序列是主要受益场景。基线是 vLLM 同 PR 作者的 kernel，不是整服务吞吐。
- **#4728 的收益是 public API GPU time，不是 end-to-end inference**：相对 frozen #4605 仅 1.018×–1.045×，说明对已用 Cake 的用户增量有限；相对 FlashKDA 的 2.5×–2.7× 是基线选择问题。piece 路径要求 in-place initial state 且不支持 CUDA Graph，已用 graph capture 的部署不会自动切到 piece。

## 生产验证清单

1. **#36456**：在目标 Hopper 卡上以 `PYTORCH_NO_CUDA_MEMORY_CACHING=1` 跑 `compute-sanitizer`，确认 `_matmul.py:371` 处 0 错；以 H100 内存 shim 复现 GPQA≥0.58；确认 `block_k` 仍为 128（非 64）。
2. **#30859**：构造 token_id 接近 4.2M 的 KV 池，对比 int32/int64 路径的 quant/dequant 位等价性（作者报告 DSA fast quant/dequant 位等价）；跑 EAGLE GSM8K 确认 accuracy 无回退、errors=0。
3. **#4030**：在 SM120/121 上跑 `tests/msa_ops/` 全 155 例（含 dispatch 边界 P=88/128/256/2560、NaN、forced blocks、CUDA-graph capture）；用 CUPTI cold-L2 复测 batch1 MTP 2k–32k ratio≥1.20；确认 batch128 端到端 ratio 不退步（≤1.03 视为持平）。
4. **#4728**：在 B200/B300/GB200/GB300 上跑 29-shape ledger，校验 SHA256 `1143cd69…7b95d9`；对每 shape 验 BF16 `atol=rtol=1e-2`；确认 `seq_order`/显式 workspace/CUDA Graph 场景下 route 落到非 piece；确认 `sm_count` 非 148/152 时 piece 路径不选（kernel 内 `TVM_FFI_ICHECK` 会失败）。

## 什么证据会推翻它

- **#36456**：SM100（B200）`BLACKWELL_SCALE` 分支若被报告同类越界且 GPQA/服务异常，则"仅 SM90 受影响"的边界不成立。
- **#30859**：若独立复现在 <4.2M tokens 处出现 int32 回绕（例如 stride 更大或不同 kernel 布局），则溢出阈值陈述需修正；若 EAGLE GSM8K accuracy 在独立复现中低于 96.66%，则"加固无回退"不成立。
- **#4030**：若独立复现中 chunked 与 count-rank/radix 的选择不恒等（非 near-tied 场景），则"选择恒等"陈述不成立；若 batch128 端到端 ratio 独立测得 <1.00，则"proxy 主导时不退步"需修正。
- **#4728**：若独立复现中 piece 路径在 `seq_order` 给出时仍被选择，或 roofline `piece_ns>=direct_ns` 时仍走 piece，则准入边界不成立；若 29-shape BF16 校验在独立硬件上失败，则正确性口径陈述不成立。

## 明确限制与反例

- **单一来源**：四个 PR 的全部性能/正确性数字均为合入作者报告，无独立复现；#4030 的基线 vLLM kernel 与被替代 kernel 同出一 PR 作者。
- **#36456**：仅 SM90；SM100 路径未处理；PR 快照仍有部分 CI 红灯（Base、AMD ROCm）。`block_k=64` 虽消越界但被作者以 −13% 至 −23% 吞吐代价拒绝，不可作为替代 fast path。
- **#30859**：无服务性能 A/B；仅 H200 focused 测试；DSA/DSV4 之外的同型 kernel 未覆盖。
- **#4030**：仅 SM120/121；`per_token_nvp` 路径不走 chunked；scratch 超 128MB 或 `n_mid≤32` 或 `n_mid>2048` 时落回单 kernel；batch128 端到端无显著移动。比值基线为 vLLM，非整服务吞吐。
- **#4728**：仅 CC 10.0/10.3 且 148/152 SM；`num_heads==12` 排除；`initial_state is None` 排除；CUDA Graph 不走 piece；piece workspace 需 capture 前 warm。GPU time 非 end-to-end；BF16 tolerance 1e-2，且从语义约束触发 fallback。
- **推断（超出来源支撑，单列）**：四个 PR 的共同模式——准入条件静态可求值、回退共享正确性口径、CUDA Graph 显式边界——可能是 FlashInfer/SGLang 维护者社区的隐式工程约定，但来源未明文陈述此约定，不可作为事实引用。
