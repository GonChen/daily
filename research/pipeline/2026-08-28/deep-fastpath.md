# 深挖：异构硬件 fast path 的三条新路径（2026-08-28）

选题：SGLang #36330（gfx950 Qwen3.5 MTP attention）、FlashInfer #4789（按 module variant 过滤 MoE cubin manifest）、TensorRT-LLM #17985（MiniMax-M3 混合 NVFP4/FP8 KV）。三 PR 均于 2026-08-27 合入。一手来源仅各 PR 正文，所有数字为作者报告，无独立复现。

## 发生了什么

#36330 为 MI355X 上 Qwen3.5 MTP 验证加 SGLang 自有 Triton 3D unified-attention kernel，每 workgroup 处理 2 个 speculative query token、复用同一 KV tile，仅对 gfx950 + 16 query head / 1 KV head / head_dim 256 / page 16 / BF16 query / FP8 KV / 非 sliding / 无 softcap/sink 的形状 dispatch。#4789 把 trtllm-gen MoE 的 `flashinferMetaInfo.h` 按 module variant（`enable_rubin`）过滤，使 B200 CUDA 13 冷 JIT 不再编译跨 arch 家族的死 cubin。#17985 给 MiniMax-M3 的 57 个 sparse target 层加 NVFP4/P128 KV，dense 层与 Eagle draft 层保留 FP8，并为 pure decode 提供"selected NVFP4 pages → FP8 scratch → 预规划 MSA FP8"的 staged 路径。

## 数字与对比（作者报告）

| PR | 维度 | before | after |
|---|---|---|---|
| #36330 | 微基准 KV=8192/40960/89088，batch20 q=4 | 117.5/367.5/684.1 us | 51.3/186.4/347.6 us（1.97–2.29×） |
| #36330 | IL70000 decode attention/层，C4/C64 | 137.4/140.3 us | 85.9/86.5 us（−37.5%/−38.3%） |
| #36330 | 服务 TP2 IL70k OL300，C4/C8/C16 tok/s/gpu | 9954/9942/10586 | 10245/10892/10900（+2.9%/+9.6%/+3.0%） |
| #36330 | 同上 TPOT | 27.49/65.68/129.76 ms | 23.80/64.50/136.77 ms（C16 +5.4% 回归） |
| #4789 | manifest 条目 / `trtllm_batched_gemm_runner.cu` 编译 / 整模块冷 JIT | 6862 / 1175.2 s / 1175.7 s | 3476 / 205.1 s / 226.4 s（5.7×/5.2×） |
| #17985 | GB300 AgentX 3600s A/B，1×CTX TP4 + 2×GEN TP4，conc60 | direct NVFP4：P90 TPOT 8.713ms，31.5k tok/s/GPU | staged：P90 TPOT 7.379ms（−15.31%），33.8k tok/s/GPU（+7.09%），P90 E2EL −17.82% |

## 对部署/成本/能力意味着什么

- **#36330**：MI355X 上跑 Qwen3.5-MTP 验证的部署，升级即得 decode attention −37% 与服务 TPOT 改善；但 C16 TPOT +5.4% 回归未定位，高并发 TPOT 敏感场景应先压测 C16。准入形状严格，非 Qwen3.5 MTP 形状仍走 AITER 旧路径，无收益。
- **#4789**：B200/sm100 上冷启动 fused-MoE JIT 的部署，冷启动从 ~20 分钟降到 ~4 分钟，直接缩短首请求就绪时间与弹性扩容窗口。仅影响 trtllm-gen MoE 编译路径，FMHA/GEMM manifest 不受影响。**persisted tactic 风险**：旧的 `FLASHINFER_TACTICS_BLOCKLIST` JSON 或保存的 autotune 结果会因 configIndex 重编号而失效，升级前需清空或重跑 autotune。
- **#17985**：GB300 AgentX 上跑 MiniMax-M3 的部署，GEN worker 设 `TRTLLM_M3_NVFP4_STANDARD_STAGE=1` 即得 P90 TPOT −15%、吞吐 +7%。CTX prefill 不受该变量影响（staging 仅 pure decode）。需同时启用 `use_kv_cache_manager_v2`、`dtype: nvfp4`、`tokens_per_block: 128`、MSA backend。不支持 dynamic-tree speculation（显式拒绝）。

## 什么证据会推翻它

- **#36330**：若独立复现中 C16 TPOT 回归 >5.4% 或在 C16+ 持续放大，则"端到端改善"需限定为 C≤8；若非准入形状被错误 dispatch 到新 kernel，则准入门不成立。
- **#4789**：若独立复现中过滤后 manifest 与运行时 dispatch 不一致（某 arch 的合法 cubin 被误删），则"无 cubin 丢失"不成立；若 persisted tactic 在升级后仍被加载且数值错误，则"仅 in-process 一致"的边界需收紧。
- **#17985**：若独立复现中 staged 路径在 mixed batch 或 decode q>8 时被错误选中，则准入门不成立；若 3600s A/B 外更长运行出现 scratch 越界或 graph replay 失败，则"graph-stable"陈述需修正。

## 可信级与来源

- 可信级：中。三 PR 均单一来源（合入作者报告），无独立复现；#36330 的 C16 回归、#4789 的 persisted tactic 失效、#17985 的 dynamic-tree 拒绝均为作者自报的限制。
- 来源：
  - SGLang #36330 https://github.com/sgl-project/sglang/pull/36330
  - FlashInfer #4789 https://github.com/flashinfer-ai/flashinfer/pull/4789
  - TensorRT-LLM #17985 https://github.com/NVIDIA/TensorRT-LLM/pull/17985
  - 去重基线：research/pipeline/2026-08-27/dedup.md（本期无独立 dedup.md，fallback-discovery.md 声明按 8/26、8/27 ledger 与 tracker 去重）

## 推断（超出来源支撑，单列）

- #36330 的 C16 TPOT 回归与 decode attention −38% 同时出现，推断回归源在 attention 之外的瓶颈（如 scheduler/proxy），但来源未定位，不可作为事实。
- #4789 的 5.2× 编译加速推断可线性外推到 sm107/sm103 AOT 双 variant 构建，但来源仅在 B200/sm100 测量，其他 arch 未验证。
- #17985 的 staged 路径 scratch 按 requests×max_decode_length 分配，推断其容量与并发解耦，但来源未给出 scratch 占用绝对值，不可量化。
