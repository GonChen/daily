# 2026-08-29 selection

## Top 5 与打分

| 候选 | 新颖度 | 物质性 | 可验证性 | 准入 | 桶 |
|---|---:|---:|---:|---|---|
| SGLang #36094 | 4.5 | 4.5 | 4.5 | MI355X 5-cell serving A/B、GSM8K、38 unit cases | 推理与系统 |
| SGLang #36657 | 5.0 | 5.0 | 4.5 | GB300 liveness repro、>23k requests 0 error、kernel perf | 推理与系统 |
| vLLM #53333 | 4.5 | 4.5 | 4.5 | 两节点 P/D 1,319 GSM8K C64 A/B | 推理与系统 |
| vLLM #54168 | 4.5 | 4.5 | 4.0 | B300 TP8 kernel trace + 1,319 GSM8K 正确性评测；非服务 A/B | 推理与系统 |
| SGLang #36807 | 5.0 | 5.0 | 4.0 | 社区最小复现，B200 64/64 错行和低/高长度对照 | 论文与开源 / 社区 |

## Executive readout 论点草稿

本期主线是：异步与稀疏 fast path 的失败不是单纯的“变慢”，而是**缺少可保留的资源余量、顺序或候选集**。#36657 为 Blackwell grid barrier 留出 SM residency；#53333 将 KV 传输提交排到 forward 后但只对 async-only step；#36094 让 capture-time split-K 保持安全近似；#54168 只在 low-M 安全切换 SIMT；#36807 显示 fixed candidate buffer 的 bounds guard 可避免 OOB 却产生静默错误。每条性能值仅在报告的硬件/shape/拓扑下成立。

## 深挖分配

- `deep-liveness.md`：[#36657](https://github.com/sgl-project/sglang/pull/36657) + [#53333](https://github.com/vllm-project/vllm/pull/53333)，资源可驻留与 forward/transfer order 的 liveness contract。
- `deep-selection.md`：[#36094](https://github.com/sgl-project/sglang/pull/36094) + [#54168](https://github.com/vllm-project/vllm/pull/54168) + [#36807](https://github.com/sgl-project/sglang/issues/36807)，capture-time/low-M/radix selection 如何在未知运行时状态下失效或降级。

## 30 秒结论

- GB300 MegaMoE reserve 2 SM 后，side stream 仍活跃时 kernel 完成；reserve=0 可重现 grid-sync timeout。
- MI355X DSV4 split-K service A/B 在 C4–64 吞吐 +0.8% 至 +4.3%、TPOT −0.8% 至 −4.2%，但 plain TP8 全部 <1%。
- vLLM P/D async KV 让 TPOT −4.92%，TTFT +0.07%；sync 或 mixed step 保持旧排序。
- B300 Kimi low-M trace 的 exposed chain −25.1%，而 whole-tail CUDA event 近乎不变，不能将前者写成全服务收益。
- 社区报告发现 B200 fast_topk_v2 在 64×256K、k=2048 下 64/64 rows 出错；尚待维护者核验/修复。

## 配额与 KPI

- Top5 新颖度均值：4.70；动态发现 5/5；标准桶 2（推理与系统、论文与开源）。本窗口芯片/资本、模型/Agent、中文产业未出现满足准入线的一手事实，未为凑桶引入弱候选。
- 社区/非官方来源：1（#36807，具名公开最小复现）；落选候选：6 个分组（7 条事项，#53409/#53141 与 #4494/#17870 各按一组）；degraded：是，scout 两轮无首事件，主控一手核验与审校继续。

## 落选者与理由

- #36738：HiCache forward-stream fence 机制合理，但没有稳定竞态复现或服务影响数据。
- #36583：H200 KV pool 数字强，但与 8/28 容量主题重叠，保留雷达而不占 Top5。
- #53409 / #53141：分别只有 focused regression 或单一栈收益，缺少服务 workload 与完整边界。
- #4494 / #17870：功能或兼容性变更，没有量化部署影响。
- #17434：无足够一手性能、正确性或部署证据。
- #36764：镜像膨胀为社区线索，尚未证明对应 main/latest 的确切构建。
