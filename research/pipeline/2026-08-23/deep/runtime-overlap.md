# 深挖 A：SGLang v0.5.18 启动/TP 通信重叠已发布，DeepGEMM MoE 输入流式交接仍为 RFC

## 发生了什么

2026-08-23 前后，SGLang 发布 v0.5.18（tag `v0.5.18`，710 PR / 212 contributors），其中两项通信/启动重叠优化以**已合并、已发布**形态落地：启动期 checkpoint 分级与 CUDA graph 捕获重叠（#32017）、TP LMHead 的 allgather+scatter 合并为单 all-to-all（#32313）。同期 DeepGEMM issue #410 以 **open RFC** 形式提出 MegaMoE 输入的 chunk-ready 流式交接协议，明确声明无任何性能结果、待维护者就接口与正确性模型达成共识后再实现。

## 数字与对比

| 项 | 状态 | 口径 | 作者报告数字 | 来源 |
|---|---|---|---|---|
| 启动 checkpoint 重叠 #32017 | 已发布（opt-in `--startup-weight-load-mode overlap`） | Qwen3-32B / H100，端到端启动时延 | 比串行+prefetch 快 8.6–11.7%；比 plain default 2.38×（35.6s vs 84.8s） | v0.5.18 release notes（作者报告） |
| TP LMHead all-to-all #32313 | 已发布 | DeepSeek-V4-Pro / B200 / decode，pure-DP dp-attention | LMHead 320µs→169µs；TPOT 36.97ms→35.67ms | v0.5.18 release notes（作者报告） |
| FlashInfer MNNVL pure allreduce #30700 | 已发布（DSV3/V3.2/V4 自动启用） | DeepSeek-V4-Flash / TP4 / Blackwell decode，小批 | 至多 +6.9% | v0.5.18 release notes（作者报告） |
| MegaMoE 输入流式交接 #410 | **open RFC，无实现** | 提议 B200/NVSwitch，未测量 | **无性能结果**（issue 正文明确声明） | DeepGEMM #410 |

启动重叠与 TP LMHead 数字均为 release notes 中作者报告，未见独立复现；MNNVL 数字同。RFC 项不得引用任何吞吐/时延数字。

## 对部署/成本/能力意味着什么

- 启动重叠对**频繁重启/弹性扩缩容**场景直接缩短冷启动：H100 单机 Qwen3-32B 从 84.8s 降到 35.6s（作者报告），可降低滚动升级与故障恢复的不可用窗口。需显式 opt-in，默认路径不变。
- TP LMHead all-to-all 仅在 **pure-DP dp-attention** 配置下生效，收益集中在 B200 + DeepSeek-V4-Pro decode；对非 DP-attention 或非 B200 部署无承诺。TPOT 降幅约 3.5%（36.97→35.67ms），属边际但免费。
- MNNVL pure allreduce 仅 Blackwell + DSV3/V3.2/V4 自动启用，小批 decode 受益；非 Blackwell 或 NCCL 路径不受影响。
- DeepGEMM #410 **不改变任何当前部署决策**：它是接口/正确性讨论，未合入、无实现、无测量。任何"流式 MoE 已提速"的表述均不成立。

## 什么证据会推翻它

- 启动重叠：独立方在 H100 + Qwen3-32B 复现得不到 2.38× 或 8.6–11.7% 区间；或在大模型/多机场景出现显存峰值越界、CUDA graph 捕获失败。证伪标准：同硬件同权重下 `--startup-weight-load-mode overlap` 启动时延未优于 plain default。
- TP LMHead：非 B200 或非 pure-DP 场景测不到 320→169µs；或 all-to-all 在非 NVSwitch 拓扑下退化。
- RFC #410：若维护者拒绝该协议、或合入后端到端 MoE 时延未改善（issue 自定成功标准为"端到端 MoE 时延下降，kernel-only 计时不算"），则其价值主张不成立。**不得声称 RFC 已有性能结果**——issue 正文已声明无 B200/NVSwitch 结果。

## 可信级与来源列表

- 已发布三项：可信级 **B**（作者报告，单一官方来源，无独立复现）。
- RFC #410：可信级 **D**（设计讨论，无实现无测量）。
- 来源：
  1. https://github.com/sgl-project/sglang/releases/tag/v0.5.18 （v0.5.18 release notes，PR #32017 / #32313 / #30700）
  2. https://github.com/deepseek-ai/DeepGEMM/issues/410 （open RFC，MegaMoE 流式输入协议）
- 与 dedup 对照：dedup 仅记录 SGLang #35554（SM107 packed-MXFP4，待验证）与 DeepSeek 雷达；本期 v0.5.18 启动/TP 重叠与 #410 RFC 为新事实，未与去重条目重复。
