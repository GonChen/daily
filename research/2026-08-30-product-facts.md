# 2026-08-30 research ledger

## 采集、去重与子代理状态

已以 8/28、8/29 ledger、pipeline 与 tracker 去重，详见 [dedup](pipeline/2026-08-30/dedup.md)、[fallback discovery](pipeline/2026-08-30/fallback-discovery.md)、[selection](pipeline/2026-08-30/selection.md)、[deep gating](pipeline/2026-08-30/deep-gating.md) 与 [deep agent](pipeline/2026-08-30/deep-agent.md)。动态发现扫描 8/29 合入 PR、同日公开 issue 和官方 release；DeepSeek 官方组织、芯片/供应链、基础设施/资本、中文产业在窗口内没有满足准入线的一手新增事实，保持安静。

两轮八桶 `intel-scout` 都在首条模型消息前停滞，已停止且不再重试。`pi auth check --model br/deepseek-v4-flash --json` 返回 `ready`，进程继承系统 HTTP(S) proxy；故障不是认证或系统代理变量缺失。主控按一手 GitHub API/PR/issue/release 继续核验，`intel-editor` 和两项 `intel-analyst` 深挖完成。

## 入选事实

- **SGLang #36714，8/29 合入｜主线提交、作者报告：**`is_cuda()` 错把 ROCm 排除，GLM-5.2 MTP IndexShare 的 PD decode-local DSA fused top-k seed remap 在 gfx942/gfx950 永远不启用；改为 CUDA 或 HIP，NPU 仍拒绝。MI355X×8、GLM-5.2-MXFP4、TP2、1P1D、PD+EAGLE/MTP、C4、300 s A/B：TPOT 23.16→7.94 ms（2.92×），TTFT 2125.5→2112.3 ms，accept length 3.12 不变、0 request error。GSM8K/LongBench-v2 的置信区间跨零，不把它写成精度提升。PR Base/Extra/AMD CI 快照失败，数字为作者报告。[PR #36714](https://github.com/sgl-project/sglang/pull/36714)
- **SGLang #36915，8/29 合入｜主线提交、作者报告：**AITER non-MLA EAGLE draft-extend 的 eager fallback 曾复用旧 `qo_indptr`，在 MI355X/Qwen3.5-397B-A17B-MXFP4/TP2/EAGLE/FP8 KV 的 graph-off warmup 中确定性不 ready、2 次 HIP memory fault；修复后 ready、0 fault。graph max BS 32、64 running requests 的 512-thread GSM8K 实际走到15个 eager batch，完成1314/1314、score 0.9414003044、0 fault/exception、mean accept 3.5051。无新增 unit/doc，PR CI 快照失败或进行中。[PR #36915](https://github.com/sgl-project/sglang/pull/36915)
- **FlashInfer #4722，8/29 合入｜主线提交、作者报告：**新增 Blackwell `cake` all-gather matmul，SM100/103、BF16/FP16、TP2/4，prepared API 固定 binding，变化或不支持输入 fail closed。B300 K8192/N2048 冷 L2 CUPTI 对照 TP2 geomean 1.083×、TP4 1.053×；4×GB300/Llama-3.1-70B/4096 in/32 out/C1 三次 native-A/candidate/native-B output speedup geomean 1.009490×，32/32 token exact，max logprob delta 0.000331656。单一 C1 负载不外推为通用 serving 提升。[PR #4722](https://github.com/flashinfer-ai/flashinfer/pull/4722)
- **OpenAI Codex rust-v0.151.0，8/29 发布｜官方 release：**新增 `mcp_optional_startup_grace_ms`（默认1000ms）、extension 在 MCP completion/model input 前检查或替换 tool result、仓库级 plugin catalog 合并；修复 restored permission profile、`/cd` 不能安全表示时拒绝、remote sandbox executor home/OS/path 语义与 stale authorization，并将嵌套 subagent token 使用计入 root goal budget。正式产品治理变化，无性能或任务成功率 benchmark。[release](https://github.com/openai/codex/releases/tag/rust-v0.151.0)
- **SGLang issue #37059，8/29｜社区一手报告，未确认：**具名部署者在 H200×8、TP8/DP2、MiMo-V2.5、FP8 下两次复现：任何 audio request 令全服务约600s 后死亡，text-only/无音轨 video 正常。报告定位 audio `RowParallelLinear` 在 full TP reduce 而只有一个 DP group 进入编码器，造成 collective desync；有 launch command、源码、stack 与错误大小，但无维护者确认或修复。[issue #37059](https://github.com/sgl-project/sglang/issues/37059)

## 雷达与落选

- vLLM #54282 分离 probabilistic draft/target Gumbel stream，性能变化跨零且仅影响非默认模式；#45457 的 GPT-OSS routing reuse 只有微基准；#50611 MLA DCP、#50488 speculative graph sizing 只有功能/正确性证据，均不占 Top5。
- 社区 #54360（GB10 hybrid GDN spec+APC hit 17,248→0）、#37052（2×GB10 full graph/NEXTN 五次断服）、FlashInfer #4814（B300 2-CTA 130 次53 hang）均有重要线索，尚未获维护者确认或存在旧镜像/配置边界，作为 tracker。
- SGLang #36798/#36834 的 HiCache host registration/staged-fetch 改进缺服务量化；#37066 为 proposal、#36943 为未确认 community deadlock，均落选。

## 编辑判断

本期主线是：**平台、容量和模态门控的静默失效**。#36714 让 ROCm 不再静默走慢的 DSA fused path；#36915 修复 graph 容量外 reuse 的陈旧 metadata；#37059 则显示模态不对称会把 full-TP collective 变成全服务 hang。#4722 的 prepared binding fail-closed 与 Codex 0.151.0 的 MCP/sandbox 拒绝策略说明：fast path、工具和权限都应在条件不成立时显式拒绝，而非静默错路。PR 数字均为作者报告；#37059 仍是未确认社区报告。

**KPI：Top5 新颖度均值 4.40；标准桶覆盖数 3（推理与系统、论文与开源、模型与 Agent）；社区/非官方一手 1（#37059）；落选候选 9 组/13事项；degraded：是，intel-scout 两轮均无首个模型事件，认证与系统 proxy 正常，主控一手核验和编辑深挖继续。**
