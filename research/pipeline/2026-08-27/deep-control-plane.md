# 深挖 02：控制面完成语义——barrier 还是状态位

## 发生了什么

2026-08-26，三个独立仓库各自合入一条控制面修复，均把"完成"从 CPU 侧谓词升级为跨 rank 的设备/集合屏障：vLLM #52914 给 DP `pause_generation()`/`wake_up()` 加 device barrier；SGLang #35343 把 FlashInfer tactic autotune 从 rank-local argmin 改为 TP 组 all-reduce 共识；TensorRT-LLM #18092 给 KV cache V2 host-tier 初始化加 world-rank `KEEP_HOST/USE_NO_HOST/ABORT` 共识。三者均为控制面改动，不触及模型输出。

## 数字与对比（均 PR 作者报告）

| 维度 | #52914 vLLM | #35343 SGLang | #18092 TRT-LLM |
|---|---|---|---|
| 修复前完成判据 | `has_work()` CPU 谓词 + gloo all-reduce | 每 rank 独立 argmin | rank-local 初始化结果 |
| 修复后判据 | `collective_rpc("synchronize_device")` 全 worker barrier | TP 组 per-tactic 时间 all-reduce | world comm 三态 MAX 共识 |
| 修复前事故 | idle 引擎 pause 返回时 device busy，wall 3.40s | 20/20 shape bucket tactic 分歧；worst rank +2.45%（m=1） | rank 间提交不同 cache-tier 配置，进入不同 manager/collective 路径 |
| 修复后 | pause/drain 返回均 idle，wall 仍 3.40s（burst 未缩） | 0/20 分歧；单流 509.56±0.72→510.68±0.13 tok/s，c32 22,956→23,130 | 两 rank 收敛到同一 hostless manager |
| 代价 | 不缩短 burst；#52957 才把 cadence 3.40s→0.17s | cold autotune 79→106s（一次性，缓存命中免重算） | 无 host-tier 配置走旧路径；无性能/事故数字 |
| 测试 | 3 unit + 2 对抗 DP + 14 回归 | digest 语义 + 2-rank gloo cache gate | 31 unit + 2-rank attention-DP/MPI |

## 统一机制

三者共享同一缺陷模式：完成信号由局部状态置位，而后续使用者假定该信号蕴含跨 rank 的设备/集合一致性。修复统一为"先做集合操作，再置完成位"：#52914 在 cache reset 前对**所有** worker 做 `synchronize_device`，并补 `wake_up` 尾部 `torch.accelerator.synchronize()`；#35343 在 `autotune()` 块外包 process group，all-reduce 每 tactic 时间后 argmin，且 `_drop_diverged_autotune_cache` 以 cache digest+env stamp all-gather 防止 cache hit 把 rank 踢出同步；#18092 先 all-gather 三态、任一 fallback 则全 rank 重建并同步重建完成再 commit。共同红线：局部 fast path（cache hit、`has_work()`、rank-local init）必须先证明自己与组内一致，否则降级到集合路径。

## 生产准入与可观测性

准入：#52914 要求所有 worker 经 `torch.accelerator` 注册；非 `torch.accelerator` 后端必须 override `synchronize_device`，CPU-only 保持 no-op。#35343 仅在 TP>1 且同 dummy forward 的 rank 间生效；loner rank 无组可对齐，照常 rank-local 调优。#18092 仅对配置了 host cache tier 的配置启用，无 host tier 走旧路径。可观测信号：#52914 应在 pause/wake 返回后探 `device_idle`（PR 提供 `device_idle()` probe RPC）；#35343 应监控 tactic cache digest 一致性与 cold autotune wall（106s）；#18092 应在 init 阶段记录三态分布与 fallback 重建事件。三者均无独立复现，#52914 的 3.40s 与 device busy 为作者 A/B（dummy batch 人为放大至 ~110ms），#35343 的吞吐 delta 作者自述为"no regression rather than speedup"。

## 什么证据会推翻它

- #52914：若存在非 `torch.accelerator` 后端未 override `synchronize_device`，则 barrier 退化为 no-op，pause 返回仍可能 busy；若 `collective_rpc` 未覆盖某 completion 路径（in-proc/fast/deferred 之外），则该路径仍 race。
- #35343：若 cache digest 漏掉影响 tactic 选择的 env 变量，all-reduce 仍可能在不同输入上 argmin，分歧复发；若 cold autotune 106s 在大 TP 下线性放大，可能抵消稳态收益。
- #18092：若 world comm 不等于实际 collective 路径的 rank 集（如 attention-DP 子组），world-rank 共识可能掩盖子组内分歧；PR 未给用户工作负载或性能数字，生产事故缓解未经量化。

## 可信级与来源

单一来源（各 PR 作者报告），无独立复现。控制面语义结论高可信（代码与测试可核验）；性能/事故数字中可信。来源：vLLM PR #52914、SGLang PR #35343、TensorRT-LLM PR #18092，均 2026-08-26 合入。
