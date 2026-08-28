# 2026-08-29 深挖：liveness contract——SM 驻留与 forward/transfer 顺序

## 发生了什么

2026-08-28，SGLang 合并 #36657（commit `87c78ce`，作者 weireweire，审阅 BBuf），为 Blackwell（SM100+）DeepGEMM MegaMoE 默认预留 2 个 SM，修复 #30399 报告的 GB200 DeepSeek-V4-Pro P/D `DeepGEMM grid sync timeout`。同日 vLLM 合并 #53333（commit `308e4cc`，作者 GirasoleY，审阅 njhill），将无同步 KV load 步骤的 `start_load_kv()` 从 `pre_forward` 后移到 forward launch 之后。两者都把"主机/旁路工作不能抢占 fast path 必需的资源"显式化为契约。

## 机制

#36657：Blackwell MegaMoE 用 even clustered grid + whole-grid software barrier，cluster size=2，每 active SM 一个 CTA。若 launch 占满全部 SM 而另一 CUDA stream 暂占一个 SM，部分 cluster 无法 resident，resident cluster 在 barrier 永久等待，0.1.4 起报 `grid sync timeout`。修复：`_mega_moe_max_num_sms()` 取物理 `multi_processor_count` 减 `SGLANG_OPT_DEEPGEMM_MEGA_MOE_RESERVED_SMS`（默认 2），向下取偶；`_configure_mega_moe_deep_gemm_num_sms` 仅包住 `deep_gemm.fp8_fp4_mega_moe` 调用，finally 恢复进程级 `set_num_sms`；symm-buffer cache key 不含 launch SM 数。SM90 路径返回 None 不变。#30592 的同向修复被本 PR 取代。

#53333：scheduler 聚合 `has_sync_kv_loads`（仅当 `num_external_computed_tokens>0` 即 `load_async=False` 时置真）。worker 端：sync 步骤 `pre_forward` 立即 `start_load_kv`；async-only 步骤置 `_pending_load_start`，`post_forward` 在 forward launch 后执行。mixed 步骤保守走 pre-forward。Mooncake/Simple-CPU/LMCache connector 把 load/store 从 `get_finished()` 移到真正的 `start_load_kv`/`wait_for_save`；LMCache layerwise reset 移到新 `bind_connector_metadata()` hook。

## 数字与对比（作者报告）

| 项 | before | after | 变化 |
|---|---|---|---|
| #36657 side-stream repro | reserve=0 阻塞至 timeout | reserve=2 side stream 仍活时完成 | 定性 |
| #36657 kernel 100 iter | 0.059546 ms（reserve=0） | 0.059393 ms（reserve=2） | −0.26% |
| #36657 overlap-scheduler E2E | 重现 timeout | 12,748 warmup + 11,052 profiled 请求，0 error，~126.7K tok/s/GPU | — |
| #36657 CUDA Graph/SBO E2E | 重现 liveness 失败 | 12,345 请求，0 error，~69.5K tok/s/GPU | — |
| #53333 TPOT | 4.940 ms/tok（A2） | 4.697 ms/tok（B） | −4.92% |
| #53333 TTFT | 14,471.9 ms | 14,481.5 ms | +0.07% |
| #53333 ITL | 4.939 | 4.701 | −4.83% |
| #53333 E2E | 15,077.9 ms | 15,053.3 ms | −0.16% |

#53333 workload：两节点 P/D，Qwen3-0.6B，TP1 producer + TP1 decoder，1,319 GSM8K prompts，concurrency 64。NIXL 提交开销作者报告 ~5 ms（9 remote KV × TP8 = 72 handles），峰值 ~48 ms。#36657 硬件：GB300（148 SM，reserve 后 146）。#30399 原始重现：GB200，nightly `cu13-20260707`，`sgl-deep-gemm==0.1.4`，DeepSeek-V4-Pro，disagg 1p1d dep8/dep16 c512。

## 对部署/成本/能力意味着什么

- Blackwell MegaMoE 用户：升级到含 #36657 的 main 后，overlap scheduler / CUDA Graph / SBO 下不再随机 grid-sync 崩溃；默认 reserve=2 几乎无 kernel 性能损失（作者报告 −0.26%）。reserve 可经 env 调高（更多旁路 stream 时）或置 0（纯独占验证）。Hopper/SM90 不受影响。
- vLLM P/D 用户：async-only decode 步骤的 NIXL 提交与 GPU forward 重叠，TPOT 直接下降 ~4.9%；TTFT 几乎不变（+9.6 ms）。无 config opt-in，自动生效；sync/mixed 步骤保持旧序，无回归。Mooncake/CPU-offload connector 的 `get_finished()` workaround 被清理，后续 connector 实现须遵守"start_load_kv 在 forward 后"契约。
- 推断：两类修复共同说明，在 Blackwell 大规模 P/D 上，"fast path 必需的 SM 驻留余量"和"主机提交与 GPU forward 的顺序"已成为可观测的部署约束，不再可由单 kernel 最优性隐含保证。

## 什么证据会推翻它

- #36657：在非 GB300 的 SM100+（如 B200 单卡、B300 非 MegaMoE 路径）上 reserve=2 仍出现 grid-sync timeout；或 reserve=2 在长跑下出现非 timeout 的吞吐退化 >2%。当前 E2E 仅作者报告，无独立复现。
- #53333：在 TP>1 或更大模型（作者仅 Qwen3-0.6B TP1）下 TPOT 改善消失或转负；或 mixed 步骤保守路径在真实负载下被频繁命中使收益归零。NIXL 提交 ~5 ms/48 ms 仅为作者报告，无 trace 公开。
- 两者均无第三方独立复现；#36657 的 #30399 复现脚本（SemiAnalysisAI/InferenceX yaml）与 #53333 的两节点配置未公开可重跑产物。

## 可信级与来源

B-（机制清晰、diff 与测试一致、作者报告数字内部自洽；缺独立复现与公开 trace）。单一来源：两 PR 的所有 benchmark 数字均为作者报告，#36657 的 B300 E2E 与 #53333 的两节点 A/B 均无第三方复现。

来源：
- SGLang PR #36657 https://github.com/sgl-project/sglang/pull/36657
- SGLang issue #30399 https://github.com/sgl-project/sglang/issues/30399
- SGLang PR #30592（被取代）https://github.com/sgl-project/sglang/pull/30592
- vLLM PR #53333 https://github.com/vllm-project/vllm/pull/53333
