# 2026-08-30 主控一手发现与初筛

动态窗口：2026-08-29 合入 PR、同日新开 issue 与官方 release。首轮八桶 scout 在超过三分钟后无首条模型事件，已停止并发起唯一重试；以下为主控对 GitHub API 和原文的降级核验，不以搜索摘要替代来源。

## 候选

1. **SGLang #36714｜推理与系统｜主线提交，作者报告。** ROCm 原先被 `is_cuda()` 排除，令 GLM-5.2 MTP IndexShare 的 PD decode-local DSA fused top-k seed remap 在 gfx942/gfx950 永远失效；改为 CUDA 或 HIP，NPU 仍拒绝。MI355X×8、GLM-5.2-MXFP4、TP2、1P1D、PD+EAGLE/MTP、C4 的 300 s 作者 A/B 报 TPOT 23.16→7.94 ms（2.92×），TTFT 2125.5→2112.3 ms（基本持平），accept length 3.12 不变、0 request error。LongBench-v2 short 180 条为 0.6000→0.6111，配对 95% CI −5.4 至 +7.6 pp，不能证明稀疏精度提升；GSM8K 1319 为 +0.08 pp、CI −1.1 至 +1.3 pp。MI 硬件验证和 CPU tests 通过，但 PR Base/Extra/AMD CI 快照均失败，数字均为作者报告。新事实不同于 8/29 的 `fast_topk_v2` 静默错误：这里是 ROCm 的 fused seed remap 门控与 PD decode 性能。来源：[PR #36714](https://github.com/sgl-project/sglang/pull/36714)。
2. **SGLang #36915｜推理与系统｜主线提交，作者报告。** AITER non-MLA EAGLE draft-extend 的 eager fallback 丢弃当前 batch 的 `qo_indptr`，以可复用旧 metadata 传给 unified attention；MI355X、Qwen3.5-397B-A17B-MXFP4、TP2、EAGLE 3 steps/4 drafts、FP8 KV 在 `--disable-cuda-graph` 时 warmup 确定性不 ready 并触发 HIP memory fault。修复后相同 A/B 为 ready/0 faults；又在 graph max BS 32、64 running requests 的 512-thread GSM8K 中实际走 15 个 eager batches，完成 1314/1314、score 0.9414003044、0 memory fault、0 scheduler exception、mean acceptance 3.5051。缺少新增 unit/doc，CI 快照失败，仍是作者单环境报告。与 8/28 的 int64 KV 地址回绕不同，这是 graph 容量外的 eager metadata 路径。来源：[PR #36915](https://github.com/sgl-project/sglang/pull/36915)。
3. **FlashInfer #4722｜论文与开源｜主线提交，作者报告。** 新增 `backend="cake"` Blackwell all-gather matmul，SM100/SM103、BF16/FP16、world size 2/4；prepared API 固定 group/topology/workspace/weight binding，unsupported 或 changed binding fail closed。B300 SXM6、K8192/N2048 的 14 组 cold-L2 CUPTI 对照，TP2 geomean 1.083×、TP4 1.053×，范围 1.005×–1.189×，逐 rank correctness 通过。4×GB300、Llama-3.1-70B、4096 in/32 out、C1 同服务器 native-A/candidate/native-B 三次：32/32 token ID exact，最大 logprob delta 0.000331656，小于0.05；output speedup 1.005869×/1.016553×/1.006085×、geomean 1.009490×。单一 C1 workload，不能外推通用 serving。来源：[PR #4722](https://github.com/flashinfer-ai/flashinfer/pull/4722)。
4. **OpenAI Codex rust-v0.151.0｜模型与 Agent｜官方发布。** 正式 release 新增可配置 optional MCP discovery grace period、extension 可在结果到达模型前检查/替换 MCP tool result、catalog 合并仓库级 plugin 配置。修复恢复 permission profile、阻止 `/cd` 弱化 sandbox、以 executor 的实际 home/OS/path 强化 remote sandbox，并保留 structured MCP errors；同时把 nested subagent token usage 纳入 root goal budget。它是权限和工具治理的可部署变化，不含性能 benchmark。来源：[release](https://github.com/openai/codex/releases/tag/rust-v0.151.0)。
5. **SGLang issue #37059｜模型与 Agent / 社区一手报告，未确认。** 具名部署者报告 MiMo-V2.5 在 H200×8、TP8/DP2、DP attention/LM head/encoder、FP8 下，只要一个 request 带 audio 即全服务挂住约600 s，然后拒绝连接；text-only 与无音轨 video 正常。两次独立复现（官方 FP8 权重和 BF16 export）同签名。其根因假设为音频 `RowParallelLinear` 在 full TP reduce、但只有带 audio 的 DP group 进入，造成跨 DP collective desync；watchdog 的 `_ALLGATHER_BASE` 为随后被堵住的 logits gather。该报告给出 launch command、stack、错误尺寸和源码定位，尚无维护者确认/修复。来源：[issue #37059](https://github.com/sgl-project/sglang/issues/37059)。

## 雷达与落选

- **vLLM #54282：**probabilistic draft sampling 的 gumbel noise 以前与 target 复用 Philox offset，可能使 rejection residual 偏离 target；加 salt 分离 stream，4×GB200/5 model A/B throughput −0.96%至+2.00%、acceptance −0.61%至+0.15%。机制和测试强，但仅影响非默认 `draft_sample_method="probabilistic"`，作为 correctness radar 与深读材料，不占 Top5。[PR](https://github.com/vllm-project/vllm/pull/54282)
- **vLLM #45457：**GPT-OSS MoE reuse `SparseMatrix` top-k routing metadata，RTX5090 微基准每层约省200μs、20→9 kernel、43.0%–43.6%；无服务 A/B，且 CUDA graph 可摊薄 launch 影响，降级为算子雷达。[PR](https://github.com/vllm-project/vllm/pull/45457)
- **vLLM #50611：**MLA DCP remote-KV route 扩展到 replicated/sharded 三种拓扑并给 DeepSeek-V2-Lite GSM8K strict-match sweep；没有 latency/throughput A/B，作 PD 拓扑雷达。[PR](https://github.com/vllm-project/vllm/pull/50611)
- **vLLM #50488：**修正 speculative decode 的 default CUDA graph capture size，以覆盖 `max_num_seqs × (1 + num_speculative_tokens)` 和动态 tier；仅 config tests、400 GSM8K 正确性，未提供性能 A/B，作雷达。[PR](https://github.com/vllm-project/vllm/pull/50488)
- **vLLM #54360：社区报告称 GB10 hybrid GDN 上 MTP/DFlash 可能使 prefix cache hit 从 APC-only 17,248 降至 0，TTFT 0.64 s 变 13.9 s；评论指出可能是 prompt geometry 与已开 PR #52244 的组合。需维护者确认，留作跟踪。[issue](https://github.com/vllm-project/vllm/issues/54360)
- **SGLang #37052：社区报告称 Qwen3.8-Flash-Next NVFP4、2×GB10、TP2、full decode CUDA graph/NEXTN 有五次双 rank assert/Xid 43；全禁 CUDA graph 后合成 canary 52/52、2,357,058 prompt tokens 通过。影响大但仍是较旧 image、无 main 复测和维护者诊断，作雷达。[issue](https://github.com/sgl-project/sglang/issues/37052)
- **FlashInfer #4814：社区报告 B300 MXFP4 fused-MoE 的 2-CTA tactic 在 B=2048 可 hang，0.6.17 stress 130 次有53 hang；未确认，作跟踪，不与 #4722 的正式合入混为一谈。[issue](https://github.com/flashinfer-ai/flashinfer/issues/4814)
- **SGLang #36798/#36834：**HiCache host-registration chunk 对齐与 live-tree staged-fetch 决策均强化资源安全，但前者无 GPU throughput、后者声明无 speed/accuracy benchmark，降级雷达。[#36798](https://github.com/sgl-project/sglang/pull/36798) [#36834](https://github.com/sgl-project/sglang/pull/36834)
- **SGLang #37066/#36943：**前者是 proposal，后者是未确认的 symmetric-memory/NCCL deadlock 社区报告；均不取代有量化且可核验的入选项。

## 公开面安静

- DeepSeek 官方组织最近 push 为 8/27 的 deepseek-harness 和 DeepGEMM，窗口内没有可进入 Top5 的官方 release、权重、模型卡或工程资产。
- 基础设施/资本、中文产业未找到同时满足日期窗口、第一方来源与量化部署/商业影响的新增事实。
