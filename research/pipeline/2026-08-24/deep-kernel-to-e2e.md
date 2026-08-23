# 深挖一：kernel 加速必须同时通过端到端和首次使用成本两道门

## 事实对比

| 项目 | 已合入变化 | 最接近的性能口径 | 关键数字 | 不能据此推出什么 |
|---|---|---|---|---|
| FlashInfer #4593 | SM100/SM103 block-sparse VSA attention | synchronized kernel/API 与 FastWan 全生成 | canonical 16 行 1.902192×几何均速；FastWan E2E 1.015714× | 不代表所有视频模型或服务吞吐提高 90% |
| FlashInfer #4686 | B300/SM103 W4A16 dense GEMM O3 + 30 tactics | 单 GPU CUPTI kernel time | 16 形状 1.029759×几何均速；15/16 改善 | 不代表端到端模型吞吐或所有形状改善 |

## 解释

#4593 把局部 block-sparse attention 的 1.90×几何均速，与 FastWan 61 帧生成的 1.016×端到端几何均速并列公开。这不是互相矛盾：完整生成仍包含非该 attention path 的计算、调度、内存、编码/解码和 materialization。正确的决策单位是受优化阶段在整条请求中的时间占比，而不是最快 kernel 的倍数。

#4686 说明第二个门槛：更大的 autotune 搜索能在已持久化 cache 的形状上换取约 2.98% 几何均速，但在这组 16 个形状中将 profile time 从 196.68 秒增至 417.83 秒。对于大量重复形状、cache 命中充分的长寿命服务，这可摊销；对于短任务、形状高度离散、弹性扩缩频繁或 cache 常被清空的部署，首次使用的 2.12×调优成本可能盖过 kernel 收益。

## 部署检查表

1. 分开记录 kernel、模型 forward、TTFT、TPOT、完整工作流和冷启动/预热时间。
2. 以真实形状分布计算 cache 命中率；不要只在单一 best shape 选择策略。
3. 在升级前保存旧 tactic cache 并设定 cache miss 的超时/回退路径。
4. 以完整工作流的 p50/p99、成本和正确性作发布门槛；kernel 微基准只用于定位。

## 证伪条件

- 若相同 FastWan/SM100/103 环境下独立 E2E 测试未高于 1.0×，或存在输出/稳定性回归，则 #4593 的端到端价值应降级为单核信号。
- 若 #4686 在真实线上形状中 cache miss 频繁，以 p95 首次请求计算的节省低于预热/调优成本，则不应扩大 30 tactic 的生产搜索空间。
- 两项均没有 B200/SM100 最终全模型复现；异构 GPU 上出现相反排序时，不可从 B300/SM103 结果外推。

来源：[FlashInfer #4593](https://github.com/flashinfer-ai/flashinfer/pull/4593)；[FlashInfer #4686](https://github.com/flashinfer-ai/flashinfer/pull/4686)。性能均为 PR 作者报告。
