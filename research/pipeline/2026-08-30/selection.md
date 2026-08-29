# 2026-08-30 selection

## 打分表

| 候选 | 新颖度 | 物质性 | 可验证性 | 准入判定 | 主题桶 |
|---|---:|---:|---:|---|---|
| SGLang #36714 | 4.5 | 4.5 | 3.5 | 量化性能：TPOT 23.16→7.94 ms（2.92×），ROCm fast path 从静默禁用到启用 | 推理与系统 |
| SGLang #36915 | 4.0 | 4.0 | 3.5 | 量化正确性/liveness：HIP memory fault→0 fault，1314/1314 GSM8K score 0.9414 | 推理与系统 |
| FlashInfer #4722 | 4.5 | 3.5 | 4.0 | 量化性能：TP2 geomean 1.083×、TP4 1.053×，14 组 CUPTI 对照 + 逐 rank correctness | 论文与开源 |
| OpenAI Codex rust-v0.151.0 | 4.0 | 4.0 | 4.5 | 产品/可用性：正式 GA release，MCP 治理、sandbox 强化、permission profile 恢复 | 模型与 Agent |
| SGLang issue #37059 | 5.0 | 5.0 | 3.5 | 社区一手信号：具名部署者两次独立复现，含 launch command/stack/源码定位 | 模型与 Agent / 社区 |

打分修改理由：#36714 物质性维持 4.5——2.92× 不是渐进优化，而是 fast path 此前在 ROCm 上完全失效，修复等于启用一条新路径；可验证性降至 3.5，因为 Base/Extra/AMD CI 快照均失败，全部数字为作者报告。#36915 新颖度 4.0——与 8/28 的 int32 KV 地址回绕不同路径（graph 容量外的 eager metadata），但同属 AITER EAGLE 容量边界，不重复。#4722 物质性 3.5——单一 C1 workload 不能外推，但 prepared API fail-closed 与 correctness 设计强。#37059 可验证性 3.5——两次独立复现且定位到源码行，但无维护者确认/修复。

## Top 5 定稿

1. **SGLang #36714｜推理与系统｜动态发现。** ROCm 此前被 `is_cuda()` 排除，令 GLM-5.2 MTP IndexShare 的 PD decode-local DSA fused top-k seed remap 在 gfx942/gfx950 永远失效；改为 CUDA 或 HIP，NPU 仍拒绝。MI355X×8、GLM-5.2-MXFP4、TP2、1P1D、PD+EAGLE/MTP、C4 的 300 s 作者 A/B：TPOT 23.16→7.94 ms（2.92×），TTFT 基本持平，accept length 3.12 不变、0 request error。LongBench-v2 short 与 GSM8K 的 CI 不能证明稀疏精度提升。MI 硬件验证和 CPU tests 通过，但 PR Base/Extra/AMD CI 快照均失败，数字均为作者报告。准入依据：量化性能变化（准入线 1），口径与边界清楚。来源：[PR #36714](https://github.com/sgl-project/sglang/pull/36714)。
2. **SGLang #36915｜推理与系统｜动态发现。** AITER non-MLA EAGLE draft-extend 的 eager fallback 丢弃当前 batch 的 `qo_indptr`，以可复用旧 metadata 传给 unified attention；MI355X、Qwen3.5-397B-A17B-MXFP4、TP2、EAGLE 3 steps/4 drafts、FP8 KV 在 `--disable-cuda-graph` 时 warmup 确定性不 ready 并触发 HIP memory fault。修复后 ready/0 faults；graph max BS 32、64 running requests 的 512-thread GSM8K 实际走 15 个 eager batches，完成 1314/1314、score 0.9414、0 memory fault、mean acceptance 3.5051。缺少新增 unit/doc，CI 快照失败，仍是作者单环境报告。准入依据：量化正确性/liveness 变化（准入线 1）。来源：[PR #36915](https://github.com/sgl-project/sglang/pull/36915)。
3. **FlashInfer #4722｜论文与开源｜动态发现。** 新增 `backend="cake"` Blackwell all-gather matmul，SM100/SM103、BF16/FP16、world size 2/4；prepared API 固定 group/topology/workspace/weight binding，unsupported 或 changed binding fail closed。B300 SXM6、K8192/N2048 的 14 组 cold-L2 CUPTI 对照：TP2 geomean 1.083×、TP4 1.053×，范围 1.005×–1.189×，逐 rank correctness 通过。4×GB300、Llama-3.1-70B、4096 in/32 out、C1 三次 native-A/candidate/native-B：32/32 token ID exact，最大 logprob delta 0.000332，output speedup geomean 1.009×。单一 C1 workload，不能外推通用 serving。准入依据：量化性能变化（准入线 1）。来源：[PR #4722](https://github.com/flashinfer-ai/flashinfer/pull/4722)。
4. **OpenAI Codex rust-v0.151.0｜模型与 Agent｜动态发现（官方 release）。** 正式 release 新增可配置 optional MCP discovery grace period、extension 可在结果到达模型前检查/替换 MCP tool result、catalog 合并仓库级 plugin 配置。修复恢复 permission profile、阻止 `/cd` 弱化 sandbox、以 executor 的实际 home/OS/path 强化 remote sandbox，保留 structured MCP errors；nested subagent token usage 纳入 root goal budget。权限和工具治理的可部署变化，不含性能 benchmark。准入依据：产品/可用性变化（准入线 2）。来源：[release](https://github.com/openai/codex/releases/tag/rust-v0.151.0)。
5. **SGLang issue #37059｜模型与 Agent / 社区｜动态发现（社区一手）。** 具名部署者报告 MiMo-V2.5 在 H200×8、TP8/DP2、DP attention/LM head/encoder、FP8 下，只要一个 request 带 audio 即全服务挂住约 600 s 然后拒绝连接；text-only 与无音轨 video 正常。两次独立复现（官方 FP8 权重和 BF16 export）同签名。根因假设为音频 `RowParallelLinear` 在 full TP reduce、但只有带 audio 的 DP group 进入，造成跨 DP collective desync；watchdog 的 `_ALLGATHER_BASE` 为随后被堵住的 logits gather。报告给出 launch command、stack、错误尺寸和源码定位，尚无维护者确认/修复。准入依据：社区一手信号（准入线 4）。来源：[issue #37059](https://github.com/sgl-project/sglang/issues/37059)。

## 落选者与理由

- **vLLM #54282：** probabilistic draft sampling 的 gumbel noise salt 分离机制和测试强，但仅影响非默认 `draft_sample_method="probabilistic"`，throughput −0.96%至+2.00% 在噪声内，作 correctness 雷达与深读材料。[PR](https://github.com/vllm-project/vllm/pull/54282)
- **vLLM #45457：** GPT-OSS MoE `SparseMatrix` top-k routing metadata reuse 仅有 RTX5090 微基准，无服务 A/B，CUDA graph 可摊薄 launch 影响，降级算子雷达。[PR](https://github.com/vllm-project/vllm/pull/45457)
- **vLLM #50611：** MLA DCP remote-KV route 扩展到三种拓扑并给 GSM8K strict-match sweep，但没有 latency/throughput A/B，作 PD 拓扑雷达。[PR](https://github.com/vllm-project/vllm/pull/50611)
- **vLLM #50488：** 修正 speculative decode 的 default CUDA graph capture size，仅 config tests 与 400 GSM8K 正确性，未提供性能 A/B，作雷达。[PR](https://github.com/vllm-project/vllm/pull/50488)
- **vLLM #54360：** 社区报告 GB10 hybrid GDN 上 MTP/DFlash 可能使 prefix cache hit 从 17,248 降至 0、TTFT 0.64 s→13.9 s；评论指出可能是 prompt geometry 与已开 PR #52244 的组合，需维护者确认，留作跟踪。[issue](https://github.com/vllm-project/vllm/issues/54360)
- **SGLang #37052：** 社区报告 Qwen3.8-Flash-Next NVFP4、2×GB10、TP2、full decode CUDA graph/NEXTN 有五次双 rank assert/Xid 43；全禁 CUDA graph 后 canary 52/52 通过。影响大但仍是较旧 image、无 main 复测和维护者诊断，作雷达。[issue](https://github.com/sgl-project/sglang/issues/37052)
- **FlashInfer #4814：** 社区报告 B300 MXFP4 fused-MoE 的 2-CTA tactic 在 B=2048 可 hang，0.6.17 stress 130 次有 53 hang；未确认，作跟踪，不与 #4722 的正式合入混为一谈。[issue](https://github.com/flashinfer-ai/flashinfer/issues/4814)
- **SGLang #36798 / #36834：** HiCache host-registration chunk 对齐与 live-tree staged-fetch 决策均强化资源安全，但前者无 GPU throughput、后者声明无 speed/accuracy benchmark，降级雷达。[#36798](https://github.com/sgl-project/sglang/pull/36798) [#36834](https://github.com/sgl-project/sglang/pull/36834)
- **SGLang #37066 / #36943：** 前者是 proposal，后者是未确认的 symmetric-memory/NCCL deadlock 社区报告；均不取代有量化且可核验的入选项。

## 深挖题分配

### 深挖 1：silent dispatch/gating 失效——平台与路由门控如何静默破坏 fast path 或整服务

涉及候选：[#36714](https://github.com/sgl-project/sglang/pull/36714) + [#36915](https://github.com/sgl-project/sglang/pull/36915) + [issue #37059](https://github.com/sgl-project/sglang/issues/37059)。

论点：三条候选共享同一失效模式——门控/分发决策在隔离测试中看起来正确，但在特定平台、容量或输入组合下静默禁用 fast path、复用陈旧 metadata 或造成跨组 collective desync。#36714 的 `is_cuda()` 门控让 ROCm 永远走慢路径（正确但慢 2.92×）；#36915 的 eager fallback 复用旧 `qo_indptr`（形状正常但 HIP memory fault）；#37059 的音频 `RowParallelLinear` full TP reduce 只在带 audio 的 DP group 进入（跨 DP desync，全服务挂住 600 s）。analyst 需读三条一手来源全文，提取各自的门控条件、失效前提和可观测信号，给出统一证伪条件：在什么最小可复现配置下能提前暴露这三类静默失效。

### 深挖 2：Agent 工具治理与 sandbox 边界——从隐式约定到可测试契约

涉及候选：[Codex rust-v0.151.0](https://github.com/openai/codex/releases/tag/rust-v0.151.0) + tracker「Agent 长驻控制面」「Agent 请求语义：代理重试与工具解析」。

论点：Codex v0.151.0 把 MCP discovery grace period、extension tool result 拦截、remote sandbox home/OS/path 强化、permission profile 恢复和 nested subagent budget 纳入正式 release，使权限/工具/预算从隐式约定变成可测试契约。analyst 需对照 release notes 与 tracker 中「Agent 长驻控制面」「Agent 请求语义」的触发条件，判断这些变化是否满足 tracker 的准入门槛（权限/预算/队列/恢复机制的正式发布、任务成功率/误调用率/重复请求率/实际计费回归），并标注尚缺的量化回归。

## Executive readout 论点草稿

本期主线是：**平台与路由门控的静默失效**。三条当日事实显示，看起来正确的门控决策在特定条件下会静默禁用 fast path 或挂死整服务。SGLang #36714 中 ROCm 的 `is_cuda()` 检查让 GLM-5.2 MTP 的 fused top-k seed remap 在 gfx942/gfx950 上永远不走 fast path——服务正确但 TPOT 慢 2.92×（23.16→7.94 ms），且无任何报错。SGLang #36915 中 AITER EAGLE draft-extend 的 eager fallback 在 graph 容量外复用旧 `qo_indptr`，形状正常却触发 HIP memory fault，修复后才 ready。SGLang issue #37059 中具名部署者两次独立复现：MiMo-V2.5 只要一个 request 带 audio，音频 `RowParallelLinear` 的 full TP reduce 就与只有带 audio 的 DP group 形成跨 DP collective desync，全服务挂住约 600 s。这三条不是孤立的 kernel bug，而是同一类问题：门控条件（平台、容量、输入模态）在隔离单元测试中不可见，只在真实 serving 的特定组合下暴露。Codex v0.151.0 的 MCP/sandbox 治理变化则从 Agent 侧提供了对照——把隐式约定变成 fail-closed 契约正是 #36714/#36915/#37059 在推理侧还缺少的东西。

## 30 秒结论要点

- SGLang #36714：ROCm `is_cuda()` 门控修复后 GLM-5.2 MTP PD decode TPOT 23.16→7.94 ms（2.92×），fast path 此前在 gfx942/gfx950 完全失效且无报错；CI 快照失败，数字为作者报告。
- SGLang #36915：AITER EAGLE eager fallback 复用旧 metadata 触发 HIP memory fault，修复后 1314/1314 GSM8K、0 fault、mean acceptance 3.5051；CI 快照失败。
- FlashInfer #4722：cake backend Blackwell all-gather matmul，TP2 geomean 1.083×、TP4 1.053×，prepared API fail-closed，逐 rank correctness 通过；单一 C1 workload。
- OpenAI Codex v0.151.0：正式 release，MCP discovery grace period、extension tool result 拦截、remote sandbox 强化、permission profile 恢复、nested subagent budget。
- SGLang issue #37059：具名部署者两次独立复现 MiMo-V2.5 audio 导致跨 DP collective desync，全服务挂住约 600 s；有源码定位，尚无维护者确认/修复。

## 配额真实判定

- 覆盖 ≥3 主题桶：✓ 推理与系统（#36714、#36915）、论文与开源（#4722）、模型与 Agent（Codex、#37059）= 3 桶。
- ≥3 条来自当日动态发现：✓ 5/5 均来自 fallback-discovery 的当日动态窗口。
- ≥1 条来自社区/非官方渠道：✓ #37059 为具名部署者公开报告，含 launch command、stack、源码定位，可链接。
- ≤1 条由固定雷达触发：✓ 0 条固定雷达触发；DeepSeek 官方组织窗口内无 release/权重/模型卡，公开面安静。
- 准入线：5 条分别满足准入线 1（#36714、#36915、#4722 量化性能/正确性）、准入线 2（Codex 产品/可用性）、准入线 4（#37059 社区一手信号）。
- 安静窗口声明：芯片与供应链、AI 基础设施与资本、中文技术与产业三个桶本期无满足准入线的一手事实，不凑桶。

## 本期 KPI

- Top5 新颖度均值：4.40
- 覆盖桶数：3（推理与系统、论文与开源、模型与 Agent）
- 社区源条数：1（#37059）
- 落选候选数：9 组（13 条事项）
- degraded：是，intel-scout 两轮均无首个模型事件，主控降级一手核验，以 fallback-discovery 为候选主来源。
