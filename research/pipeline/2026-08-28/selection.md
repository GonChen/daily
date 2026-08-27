# 2026-08-28 selection

## 入选 Top 5

1. **SGLang #35634**：ElasticBuffer 的固定 capacity shape 使 decode graph 可捕获，但以配置、模型、量化、runner 和 deterministic/speculative 组合 fail-fast；适合解释拓扑与容量契约。
2. **SGLang #36330**：MI355X 上 Qwen3.5 MTP kernel 从微基准落实到 70k 服务 A/B，同时保留 C16 TPOT +5.4% 的反例。
3. **SGLang #36541**：int32 KV 地址链在 2 GiB 后静默 NaN，导致 speculative acceptance 坍塌；其 2 GiB 临界点与修复后端到端恢复可直接行动。
4. **FlashInfer #4789**：按 module variant 过滤不可能 dispatch 的 cubin manifest；冷 JIT 成本从近 20 分钟降至不足 4 分钟，并披露 persisted tactic 不兼容。
5. **TensorRT-LLM #17985**：MiniMax-M3 混合 NVFP4/FP8 KV 将 pure decode selected pages staged 到 graph-stable FP8 scratch；GB300 AgentX 有 3,600 秒同配置 A/B，route 条件清楚。

## 编辑口径

- 一律标为“作者报告”；不将 PR 中的 accuracy、服务或微基准扩展成独立复现或通用结论。
- 把 performance 写成工作负载、硬件、拓扑和函数边界的条件结论。
- 把 #35634 与 #17985 的 fallback/fail-fast 视作事实主体，不只报性能；把 #36330 的 C16 TPOT 回归写入限制。
- 标准桶：分布式/控制面（#35634）、异构硬件 fast path（#36330/#36541）、构建与冷启动（#4789）、KV/graph 内存路径（#17985）。

## 打分与准入

| 候选 | 新颖度 | 物质性 | 可验证性 | 准入 | 标准桶 |
|---|---:|---:|---:|---|---|
| #35634 DeepEPv2 | 5.0 | 4.5 | 4.5 | 合格：H20/B200 A/B + fail-fast 契约 | 推理与系统 |
| #36330 gfx950 MTP | 4.5 | 4.5 | 4.5 | 合格：microbenchmark 与 70k serving A/B | 推理与系统 |
| #36541 int32 KV wrap | 5.0 | 5.0 | 4.5 | 合格：2 GiB bisect、kernel reference、E2E 恢复 | 推理与系统 |
| #4789 JIT manifest | 4.5 | 4.5 | 4.5 | 合格：B200 cold-build A/B + tactics tests | 论文与开源 |
| #17985 hybrid NVFP4 KV | 4.5 | 4.5 | 4.5 | 合格：GB300 3,600 秒 serving A/B | 推理与系统 |

## 落选与雷达

- [vLLM #53685](https://github.com/vllm-project/vllm/pull/53685)：DeepSeek V4 serving 的 +1.40% output tok/s 量化完整，但与 #35634 的 MoE 主线重叠，降为雷达。
- [vLLM #54088](https://github.com/vllm-project/vllm/pull/54088)：H200 CUDA Graph GEMM 仅有 M=1/2 微基准，没有服务 workload。
- [vLLM #54012](https://github.com/vllm-project/vllm/pull/54012)：native CP MLA 有 task-completion 数据，未给相同配置的服务 A/B。
- [FlashInfer #4442](https://github.com/flashinfer-ai/flashinfer/pull/4442)：性能细节外置 gist，且依赖未合入的 CCCL PR。
- [TensorRT-LLM #17862](https://github.com/NVIDIA/TensorRT-LLM/pull/17862)、[ #17887](https://github.com/NVIDIA/TensorRT-LLM/pull/17887)：前者仍是 GPU parity pending draft，后者没有服务量化。

## 深挖分配

- 控制面与静默失败：[SGLang #35634](https://github.com/sgl-project/sglang/pull/35634)、[SGLang #36541](https://github.com/sgl-project/sglang/pull/36541)，见 `deep-control.md`。
- 异构 fast path 准入：[SGLang #36330](https://github.com/sgl-project/sglang/pull/36330)、[FlashInfer #4789](https://github.com/flashinfer-ai/flashinfer/pull/4789)、[TensorRT-LLM #17985](https://github.com/NVIDIA/TensorRT-LLM/pull/17985)，见 `deep-fastpath.md`。

## Executive readout 与 30 秒结论

本期事实共同说明：fast path 的真实输入不只是模型和 GPU，而是 capacity、地址空间、consumer 与启动状态。#35634 以模型/精度/runner/topology gate 阻止不相容 MoE 执行；#36541 显示地址类型会随 KV allocation 跨过 2 GiB 临界点；#36330、#4789、#17985 分别将 shape、module variant、phase/consumer route 编码为准入条件。收益只能在这些条件和反例被完整发布时成立。

- 结果显示 #35634 的 decode −0.9% 至 −2.8%、prefill +2.9% 至 +3.2%，核心价值是 graph capture 与 fail-fast，不是 decode 加速。
- #36330 的 70k TP2 服务 C8 +9.6% tok/s，但 C16 TPOT +5.4%，不能外推为通用 AMD decode 提升。
- #36541 的 int32 地址 wrap 在 2 GiB 后让 accept length 1.03→3.53；这是静默性能退化而非 target 输出错误。
- #4789 把 B200 cold JIT 1,175.7→226.4 秒，但升级需要考虑 persisted tactic index。
- #17985 的 GB300 3,600 秒 A/B 为 P90 E2EL −17.82%，只属于 pure decode 的合格 staging route。

## KPI 与配额说明

- Top5 新颖度均值：4.70；动态发现：5/5。
- 标准桶覆盖：2（推理与系统、论文与开源），不足政策目标的 3；其余标准桶在本窗口无合格新增事实，不强行凑数。
- 开源一手 PR 作者报告：5；严格“非官方社区信号”口径：0。本期没有将 PR 作者报告伪装为独立从业者复现。
- 落选候选：6；degraded：是，`intel-scout` 两轮均无首个模型事件，认证与系统 proxy 已确认，主控一手发现及审校完成。
