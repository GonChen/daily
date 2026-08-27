# 2026-08-28 深挖：SGLang #35634 与 #36541

## 发生了什么

2026-08-27 SGLang 合入两个独立 PR。#35634 新增 DeepEPv2 `ElasticBuffer` MoE A2A 后端（`deepep_v2`），以固定 capacity 通信 shape 使 decode CUDA-graph 可捕获，并对不支持的模型/量化/runner/deterministic/speculative 组合 fail-fast。#36541 修复 AITER `unified_attention` draft-extend 路径中 `seqused_k` 被截成 int32 的 bug：当某层 KV buffer ≥ 2 GiB 时偏移链静默 wrap，draft attention 输出 NaN，speculative acceptance 坍塌为纯自回归。两 PR 均为作者报告，未独立复现。

## 数字与对比

#35634（DeepSeek V4 Flash FP8, TP8/DP8/EP8, DP attention, DeepGEMM；作者报告）：

| 工作负载 | v2 direct | v2 hybrid | legacy DeepEP |
| --- | ---: | ---: | ---: |
| H20×8 decode tok/s | 4,339 | 4,379 | 4,379 |
| H20×8 prefill in_tok/s | 22,353 | 22,651 | 21,651 |
| B200×8 decode tok/s | 8,429 | 8,675 | 8,675 |
| B200×8 prefill in_tok/s | 32,447 | 31,533 | 31,533 |
| 2×H20×8 hybrid (RoCE) | 4,610 decode / 20,688 prefill | — | 无同 fabric 基线 |

decode -0.9%~-2.8%、prefill +2.9%~+3.2%；多节点 hybrid 无可对比的 legacy 基线（NVSHMEM 数据面在该拓扑未完成）。GSM8K/MMLU 与 legacy 差异在 ±0.02 内。

#36541（Qwen3.5-397B-A17B-MXFP4, MI355X×2 TP2, EAGLE steps=3/topk=1/draft=4, fp8 KV, page 16, ISL 4096/OSL 256, conc 4×16；作者报告）：

| 配置 | accept len | TPOT (ms) | E2E 中位 (ms) |
| --- | ---: | ---: | ---: |
| 8,380,416 tokens（buffer 2.000 GiB，未越界） | 3.59 | — | — |
| 8,404,992 tokens（buffer 2.004 GiB，int32，bug） | 1.03 | 12.99 | 3871 |
| 同上，修复后 int64 | 3.53 | 5.45 | 1593 |
| 同上，legacy FMHA（env=0） | 3.51 | 5.53 | 1605 |

临界点 = 2³¹ B / 256 B/token = 8,388,608 tokens；bisect 确认 8,380,416 通过、8,404,992 失败。修复后 TPOT 5.45 ms 略低于 legacy FMHA 5.53 ms。

## 对部署/成本/能力意味着什么

- #35634：`deepep_v2` 把 decode 纳入 CUDA-graph，代价是 decode 吞吐小幅回退、prefill 提升。运营上需新增容量治理：`SGLANG_DEEPEP_V2_NUM_MAX_DISPATCH_TOKENS_PER_RANK` 是内存预留而非语义 token 上限，启动检查覆盖 prefill budget、decode graph batch、per-DP-rank running-request、speculative width，但运行时行数才是权威 guard。升级到 #30105 后的 AITER+EAGLE 部署若同时上 #35634，须确认不在 #35634 明确 fail-fast 的组合内（Qwen3.8、BF16 experts、MXFP8、非 DeepGEMM、deterministic、`deepep_v2` 作 draft backend 均不支持，会启动期失败）。
- #36541：任何 AITER+EAGLE 部署在 #30105（2026-08-22 合入）之后、#36541（2026-08-27）之前都处于静默 NaN 风险窗口。症状不是报错而是 `accept len≈1.0`、TPOT 退化约 2.4×，日志不指向 attention。触发条件是单层 KV buffer ≥ 2 GiB，与 `--max-running-requests`、`--max-total-tokens`、`--mem-fraction-static`、GPU 显存、page size 共同决定；调大 `--max-running-requests` 反而可能掩盖问题（缩小 KV pool 到阈值下）。

## 可行动的运营检查

1. AITER+EAGLE 部署：升级到含 #36541 的版本；若不能升级，设 `SGLANG_AITER_UNIFIED_DRAFT_EXTEND=0` 回退 legacy FMHA（TPOT 5.53 vs 5.45，损失可忽略）。
2. 监控 `accept len` 与 `accept rate`：若稳定在 1.0/0.0 且 TPOT 较基线翻倍以上，立即检查 draft 模型 per-layer KV buffer 是否接近 2 GiB。
3. 估算阈值：`draft per-layer KV buffer = max_total_num_tokens × page_size × bytes_per_token / layers`（此处 head_dim 256、fp8 KV、256 B/token）；保持 < 2 GiB 留余量。
4. 上 #35634 前：核对模型/量化/runner/deterministic/speculative 组合是否在支持表；不在则预期启动失败而非运行时错误。`SGLANG_DEEPEP_V2_NUM_SMS=0` 让 sgl-deep-ep 0.1.2 自动选 SM/QP；`NCCL_CUMEM_ENABLE=1` 被默认 setenv，显式用户设置仍优先。
5. 多节点 hybrid：仅 RoCE 2×H20×8 一组数据，无 legacy 同 fabric 基线，不要把 4,610 tok/s 当作对 legacy 的提升结论。

## 什么证据会推翻它

- #35634：独立复现若在 H20/B200 之外的平台（如 MI300X）得到 decode 不回退或 prefill 不提升，则"decode -0.9%~-2.8%、prefill +2.9%~+3.2%"的范围结论被收窄。若 fail-fast 组合实际能跑通且产出正确，则不支持范围结论被推翻。
- #36541：若存在 int32 路径在 < 2 GiB 也出错的 case，或 int64 修复后在 > 2.87 GiB 仍 wrap，则"临界点 2 GiB、int64 充分"的结论被推翻。AITER 上游若改为内部强制 int64，则 SGLang 侧这一行不再 load-bearing。

## 可信级与来源

- #35634：中高。单一来源（PR 正文），作者报告；CPU 204 测试+15 子测试通过，功能门控与单/多节点 A/B 自洽，但无独立复现、无用户文档。CI Base 失败、Extra 运行中、AMD ROCm 失败（与本后端无关）。
- #36541：高。单一来源（PR 正文），作者报告；bug 链路（int32 截断→offset wrap→NaN→accept 坍塌）有 kernel 级 fp32 参考对照（2.0 GiB int32 NaN、int64 1.0e-4）和端到端 bisect（8,380,416/8,404,992）双重确认，逻辑闭环。CI Base 通过、Extra 与 AMD ROCm 失败（与本修复无关路径）。
- 来源：[#35634](https://github.com/sgl-project/sglang/pull/35634)、[#36541](https://github.com/sgl-project/sglang/pull/36541)、[#30105](https://github.com/sgl-project/sglang/pull/30105)（引入 bug）、[#35568](https://github.com/sgl-project/sglang/pull/35568)（revert 前身 #29525）。
- 与 dedup（2026-08-27 基线）对照：#35634 的 DeepEPv2 capacity/fail-fast 契约与上期 DeepSeek V4 shared-expert topology gate（#35505）不同事实主体；#36541 的 int32 KV wrap 与上期 TP batch-invariant deterministic fallback（#51292）无重叠。新事实成立。
