# 深挖 1：silent dispatch/gating 失效

日期 2026-08-30。三条 SGLang 一手来源共享同一失效模式：平台、容量或输入模态的门控/分发决策在隔离测试中不可见，在真实 serving 的特定组合下静默禁用 fast path、复用陈旧 metadata 或造成跨组 collective desync。

## 发生了什么

- PR #36714（tianxiaojiang4，维护者 kpham-sgl 2026-08-29 合入，commit 24c9251）：`should_remap_pd_dsa_seed_to_local_slots()` 的门控由 `is_cuda()` 改为 `(is_cuda() or is_hip())`，NPU 仍拒绝。此前 #31477 的 GLM-5.2 MTP IndexShare PD decode-local fused-TopK seed remap 在 gfx942/gfx950 永远失效，`pd_index_share_seed` 留 True、`should_use_dsa_fused_topk()` 返回 False，PD decode 不融合且无任何报错。
- PR #36915（zijiecode，维护者 HaiShaw 2026-08-29 合入，commit 7f2ee22）：AITER non-MLA EAGLE draft-extend 的 eager fallback（CUDA Graph 关闭或 live batch 超出 captured max 时进入）丢弃当前 batch 的 `qo_indptr`，改传后端可复用 `self.qo_indptr` 缓冲，`cu_seqlens_q=[0,80]` 指向 80 行而 query 仅 4 行，越界写触发 HIP memory fault。回退复用由 #30105 引入。
- Issue #37059（yuweih205，2026-08-29 开，仍 open，无维护者回复）：`AudioEncoderAttention` 未设 `use_data_parallel`/`use_dp_attention_reduce`（`mimo_audio.py:503`），注意力权重按 attn-TP(4) 分片，但输出 `RowParallelLinear` 在 full-TP(8) 上 all-reduce；仅带 audio 的 DP group 进入编码器（`mm_utils.py:420`），另一组永不加入，造成跨组 collective desync，watchdog 600 s 超时后整服务挂死。

## 机制

三者均为门控条件在隔离单元测试中成立、在真实组合下静默失效：#36714 是平台谓词错把 ROCm 当 NPU 拒绝（正确但慢，无报错）；#36915 是 graph-容量外的 eager 路径复用陈旧 metadata（形状正常却越界）；#37059 是模态+DP 分组使集体通信一方缺席。#36714 作者补充：2.92× 主要非来自 kernel launch 消除，而是 `transform_index_*` 因上下文增长在运行时 JIT 重编译被融合消除。

## before/after 对比

| 事项 | 修复前 | 修复后 | 口径与边界 |
|---|---|---|---|
| #36714 PD decode TPOT (p50) | 23.16 ms | 7.94 ms（2.92×） | MI355X×8、GLM-5.2-MXFP4、TP2、1P1D、C4、300 s、accept sim off；作者报告 |
| #36714 TTFT / accept length | 2125.5 ms / 3.12 | 2112.3 ms / 3.12 | 持平，预期为 decode 侧改动；作者报告 |
| #36714 decode "Disabling fused DSA top-k" 告警 | w1=2 | w1=0 | 选定 worker 证据；跨三次独立 job 对复现；作者报告 |
| #36714 GSM8K 1319 / LBv2-short 180 | 0.9287 / 0.6000 | 0.9295 / 0.6111 | 配对 95% CI [−1.1,+1.3]pp / [−5.4,+7.6]pp，McNemar p=1.0/0.868，不证精度提升；作者报告 |
| #36915 graph off warmup ready / faults | No / 2 | Yes / 0 | TP2、Qwen3.5-397B-A17B-MXFP4、EAGLE 3步4draft、FP8 KV；作者报告 |
| #36915 graph on 512线程 GSM8K 1314 条 | — | score 0.9414、0 fault、0 exc、accept 3.5051，15 个 eager batch 被走到 | main @ 2a96ebf；作者报告 |
| #37059 audio 请求 | 全服务挂 600 s 后拒绝连接 | 无修复 | 8×H200、sglang 0.5.18、main @ 97781eb7f；社区报告，两次独立复现，未确认 |

## 对部署/成本/能力意味着什么

- #36714：在 gfx942/gfx950 上跑 GLM-5.2 MTP+PD 的部署者此前为 invisibly-slow path 付 2.92× decode 时延而无告警；合入后应直接受益，且须确认 `SGLANG_OPT_USE_TOPK_V2` 在 ROCm 仍 force-disabled，走的是 `fast_topk_transform_fused`。
- #36915：使用 AITER unified draft-extend 且 `--cuda-graph-max-bs` 可能被 live batch 超出的 MI355X 部署者，升级前应视为存在确定性 warmup 失败与运行期 HIP fault 风险；修复与 #36541 int64 `seqused_k` 共存。
- #37059：MiMo-V2.5 在 8 卡节点强制 `--enable-dp-attention`（因 fused qkv_proj 要求有效 attn-TP=4）的部署者，只要任一请求带 audio 即整服务挂死；当前唯一缓解是避免音频模态或退回非 DP-encoder 配置。即便两组都带 audio，数值仍错（跨 DP audio partial 求和）。

## 共同论点

门控/分发决策需在 fail-closed 契约下暴露：平台谓词、容量回退分支、模态分组进入条件均应在 warmup 期或单测中可观测。#37059 中被堵住的 `_ALLGATHER_BASE`（NumelIn=38144、NumelOut=152576=1×152576/4）实为 logits gather，提示 watchdog 诊断指向非首恶。对照 Codex v0.151.0 把 MCP/sandbox 改为 fail-closed 契约，推理侧尚缺等价机制。

## 什么证据会推翻它

- #36714 被推翻：在相同 MI355X×8/TP2/1P1D 配置上独立复现得 TPOT 降幅显著小于 2.92×，或 w1 decode 告警未从 2 降至 0；或 ROCm 上 fused 路径出现正确性偏差（accept length 偏离 3.12）。
- #36915 被推翻：修复后 graph-off warmup 仍 fault，或 graph-on 高并发 GSM8K 出现 fault/未完成/accept 显著偏离 3.5051；或 eager metadata 修正引入新的非本文覆盖路径越界。
- #37059 被推翻：维护者复现显示 audio 请求不挂（如特定 fa3/NCCL/CUDA 13 组合下集体通信意外对齐），或根因不在 audio `RowParallelLinear` reduce 域；反之，若修复后 audio + video + text 全模态在 TP8/DP2 并发稳定即确认根因。待验证项：#36714 在 RDMA 可用集群的 TTFT；#36915 无新增 unit test；#37059 无 main 复测与维护者诊断。

## 可信级与来源

- #36714：主线提交，作者报告。Base/Extra/AMD ROCm 7.2 CI 快照均 ❌；一条 wire 单测重跑 ✅；作者声明 NVIDIA-only 路径失败与 gate 改动字节一致。单一作者环境数字。来源：[PR #36714](https://github.com/sgl-project/sglang/pull/36714)、[#31477 评论](https://github.com/sgl-project/sglang/pull/31477#issuecomment-5399580921)。
- #36915：主线提交，作者报告。Base/Extra CI ❌、AMD ROCm 7.2 ⏳；checklist 未勾选（无新增 unit/doc）。单一作者环境数字。来源：[PR #36915](https://github.com/sgl-project/sglang/pull/36915)。
- #37059：社区一手报告，未确认。两次独立复现（FP8 与 BF16 export），含 launch command、stack、源码行定位；无维护者确认/修复。来源：[issue #37059](https://github.com/sgl-project/sglang/issues/37059)。推断（单一来源，跨 DP 数值错、watchdog 非首恶）已单列于机制段并标注。
