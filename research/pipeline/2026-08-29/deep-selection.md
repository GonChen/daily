# 2026-08-29 深挖：capture-time / low-M / radix 选择在未知运行时状态下的失效

## 发生了什么

三条独立变更，同属"在 CUDAGraph 捕获时或低 M 形状下用一个静态近似代替运行时未知量"的失败/调优家族。SGLang #36094 于 8/28 把 MI355X 上 DeepSeek-V4-Pro decode attention 的 split-K 启发式从 `(target_wg_per_cu=2.0, max_kv_splits=64)` 收紧到 `(1.5, 16)`，并在评审后用 `is_hip()` 门控，CUDA 路径保持 `(2.0, 64)` 不变。vLLM #54168 于 8/28 合并，针对 B300 TP8 Kimi-K3 latent-MoE 的 `M<=16` 尾部做低 M 专用化（静态 SIMT up-projection 限 `M<=5`）。SGLang issue #36807（8/28，open）报告 `sgl_kernel.fast_topk_v2` 在 k=2048、长行下因 4096-entry 固定 candidate buffer 溢出而**静默返回错误 top-k**，无报错、形状正常。

## 数字与对比

| 条目 | 指标 | before | after | 来源 |
|---|---|---:|---:|---|
| #36094 kernel（MI355X, T=32, top-k 1024, H=128） | decode attn 时延 | 55.7 us | 44.1 us（-20.8%） | 作者报告 |
| #36094 启发式 geomean regret | 最坏 119% | 33.5% | 3.7% / 最坏 36% | 作者报告 |
| #36094 服务 A/B（DSV4-Pro, TP8+DP8+EP8/MoRI+EAGLE, 8192/1024） | conc 64 tput / TPOT | 5539.24 / 96.41 | 5776.29 / 92.41（+4.3% / -4.2%） | 作者报告 |
| #36094 plain TP8 同 build | 全部 delta | — | <1%，符号交替 | 作者报告 |
| #36094 GSM8K 1319 | acc | — | 0.958 / 0.946，invalid 0.000 | 作者报告 |
| #54168 M=1 exposed chain（Nsight） | 三内核关键链 | 12.096 us | 9.056 us（-25.1%） | 作者报告 |
| #54168 Lamport copy/reset 独立 / packed overlap | — | ~4.77 us | ~1.25 / ~1.95 us（-73.8% / -59.1%） | 作者报告 |
| #54168 whole-tail CUDA-event M=1 | 含跨 rank 调度 | 16.384 us | 16.352 us（基本持平） | 作者报告 |
| #54168 GSM8K 1319 5-shot | strict / flexible | — | 0.9606 / 0.9651 | 作者报告 |
| #36807 B200, 64×256K, k=2048 | 错行 / 每行错选 | — | 64/64 行错，每行 6–42 | 社区报告 |
| #36807 64×1M / 64×64K | 错行 | — | 64/64（98–157）/ 0/64 | 社区报告 |
| #36807 `topk_transform_512_v2` 对照 | 标准正态 256K/1M | 64/64 错 | 0/64 正确 | 社区报告 |
| #36807 同上 | 集中分布 256K | — | 64/64 错，2022–2041/2048 | 社区报告 |

## 对部署/成本/能力意味着什么

- MI355X + DSV4-Pro + DP attention 部署：升级到含 #36094 的镜像后，decode-bound 高并发（≥32）吞吐可直接升 +1.8%–4.3%、TPOT 降 1.6%–4.2%，且数值与准确率（GSM8K 0.946+）稳定；plain TP8（非 DP attention）用户无收益，不必为它升级。常数门控到 `is_hip()`，CUDA 用户零行为变化。
- B300 + Kimi-K3 低并发（M≤5，如单请求或小 batch spec decode）部署：尾链关键路径 -25.1%，但这是 **Nsight exposed chain**，不是整服务指标；whole-tail CUDA-event 基本持平，不要写成端到端服务收益。静态 SIMT 仅在 `M<=5` 启用，`M>=6` 自动回 WGMMA，边界由测量交叉点固定。
- 任何用 `fast_topk_v2` 作 DSA top-k（`SGLANG_DSA_FUSE_TOPK=0` 或 unfused legacy AOT 路径）且 k=2048、行长 ≥~256K 的 DSV3.2 工作负载：当前会静默出错，**不可用于生产**。缓解：切到 `topk_transform_512_v2`（标准正态分布已修，但集中分布仍溢出，不构成完整修复）或 `flashinfer.top_k`；CI 仅测到 65536，不会报警。

## 什么证据会推翻它

- #36094：独立 MI355X 复现若 plain TP8 也出现 >1% 变化，或 DP attention 在 `kv_len∉{128,512,1024}`/H≠128 上 regret 反升，则"全 decode 范围收紧"结论不成立。当前仅作者单 run/cell。
- #54168：若整服务 GSM8K 或端到端 TPOT 出现回归，或 `M=6` 交点在别的 B300 驱动/batch 下移到 `M<=4`，则低 M 专用化边界需重设。eval 依赖了一个**未提交的 `super().__init__()` startup workaround**（已声明与尾路径无关、push 前移除），若该前提被推翻则 0.9606 不可复现。
- #36807：待维护者确认 `topk.cu` L173 静默 drop 为根因，或独立方在**非标准正态、非集中**的真实 DSA 路由分数上复现 ≥256K 行的错行；若仅在合成分布触发、真实 DSA 分数桶人口始终 <4096，则生产暴露面被高估。维护者已表态 AOT kernel 将弃用，但**尚无修复 PR 或独立核验**。

## 可信级与来源

- #36094：**作者报告，单一来源**（PR 无独立 reviewer benchmark）。CI AMD ROCm 7.2 在合并时仍在跑；unit 38 例在 `is_hip=True/False` 双路径通过。来源：https://github.com/sgl-project/sglang/pull/36094 及评审串（gating commit `cbfa616`）。
- #54168：**作者报告，单一来源**，已 merged 2026-08-28。TP16 分布式 pytest 未跑（仅 8 GPU）。来源：https://github.com/vllm-project/vllm/pull/54168。
- #36807：**社区报告，单一来源**，issue open，无维护者修复或独立复现。报告者自做 `topk_transform_512_v2`/`flashinfer.top_k` 对照；维护者 DarkSharpness 给出弃用方向但未确认根因 PR。来源：https://github.com/sgl-project/sglang/issues/36807 及 4 条评论。

与 dedup 基线对照：本期 #36094（MI355X split-K capture-time）、#54168（B300 low-M tail）、#36807（fast_topk_v2 固定缓冲溢出）均为 8/27–8/28 ledger 未覆盖的新事实，不构成重复。
