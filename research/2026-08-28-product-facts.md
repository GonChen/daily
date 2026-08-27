# 2026-08-28 research ledger

## 采集、去重与子代理状态

已以 8/26、8/27 ledger 与 tracker 作为去重基线，并轮换八个新反向问题。动态发现通过 GitHub API 扫描 SGLang、vLLM、FlashInfer、TensorRT-LLM 的 8/27 合入 PR，再读取候选原文；完整候选和落选见 [fallback discovery](pipeline/2026-08-28/fallback-discovery.md) 与 [selection](pipeline/2026-08-28/selection.md)。芯片资本、模型/Agent 产品、中文产业和论文没有同时满足日期窗口、第一方来源和量化影响的新增事实，安静处理。

两轮八桶 `intel-scout` 均在超过一分钟后无首个模型事件，已停止，且未第三次重试。`pi auth check --model br/deepseek-v4-flash --json` 返回 `ready`，进程继承 `HTTP_PROXY`、`HTTPS_PROXY`，因此降级原因是 **scout 模型首事件停滞，不是认证或系统代理变量缺失**。主控完成一手 GitHub API/PR 核验；编辑与两项分析审校见 pipeline。

## 入选事实

- **SGLang #35634，8/27 合入：**DeepEP v2 ElasticBuffer 为 `DeepseekV3ForCausalLM`、`DeepseekV4ForCausalLM`、`Qwen3MoeForCausalLM` 加 `deepep_v2` direct/hybrid backend；固定 capacity communication shape 使 decode CUDA Graph 可捕获。`SGLANG_DEEPEP_V2_NUM_MAX_DISPATCH_TOKENS_PER_RANK` 是 memory reservation，不是语义 token limit；启动检查 canonical prefill budget、graph batch、每 DP rank running-request bound 和 speculative width，runtime rows 仍为权威 guard。BF16、MXFP8、non-DeepGEMM、deterministic 与 draft worker 不支持并 fail-fast。作者在 H20×8/B200×8 的 DeepSeek V4 Flash FP8 TP8/DP8/EP8 A/B 报 H20 decode 4,379→4,339 tok/s（−0.9%）、prefill 21,651→22,353 in_tok/s（+3.2%），B200 decode 8,675→8,429（−2.8%）、prefill 31,533→32,447（+2.9%）；2×H20×8 RoCE hybrid 4,610 tok/s decode、20,688 in_tok/s prefill，但无同 fabric legacy baseline。204 tests +15 subtests 通过；PR 快照仍有 CI lane 失败/进行中。所有数字为作者报告。[PR #35634](https://github.com/sgl-project/sglang/pull/35634)
- **SGLang #36330，8/27 合入：**gfx950 的 Qwen3.5 MTP target verification（q≤4、16 Q/1 KV head、D256、page16、BF16 query、FP8 KV）以前由 generic AITER 3D attention 逐 query reload KV；新 Triton path 每 workgroup 处理两个 query 并复用 KV tile。仅匹配 gfx950、非 sliding、无 softcap/sink 的形状，其他留在 AITER。作者在 MI355X batch20/q4 microbenchmark 报 K=8,192/40,960/89,088 为 117.5→51.3μs（2.29×）、367.5→186.4μs（1.97×）、684.1→347.6μs（1.97×）。MI355X TP2、70k input/300 output serving 中 C4/C8/C16 total tok/s +2.9%/+9.6%/+3.0%，TTFT −7.6%/−13.5%/−3.5%，但 C16 median TPOT +5.4%；不能表述为通用 AMD decode 提升。[PR #36330](https://github.com/sgl-project/sglang/pull/36330)
- **SGLang #36541，8/27 合入：**AITER EAGLE-v2 draft-extend 默认 unified attention 将 KV indptr difference cast 为 int32；per-layer KV buffer 到 2 GiB 后地址链回绕并静默产生 NaN，target 仍可输出正确文本但 draft accept collapse。作者以 Qwen3.5-397B-A17B-MXFP4、MI355X×2 TP2、EAGLE、FP8 KV/page16、ISL4096/OSL256/C4 在 8,404,992 tokens（2.004 GiB per-layer KV）复现 accept length 1.03→3.53；median E2E 3,871.34→1,592.91ms、TTFT 552.31→293.27ms、TPOT 12.99→5.45ms。8,380,416 token（2.000GiB 略下）不触发；改 `seqused_k` 为 int64。PR 的 base CI 绿但 extra/AMD CI 失败，且无新增 unit/doc checklist，不可视为全面覆盖。[PR #36541](https://github.com/sgl-project/sglang/pull/36541)
- **FlashInfer #4789，8/27 合入：**合并 cubin pack 令 trtllm-gen BMM manifest 约从 3,476 翻倍到 6,850 entries；其中非 POD config 迫使 host compiler 对每条生成动态 initializer，唯一 include TU 占 fused-MoE JIT critical path 99.96%。PR 按 module variant（不是编译机 GPU）过滤不可能 dispatch 的架构，两个 variant 完整分割 manifest。作者在 B200/CUDA13 cold `fused_moe_trtllm_sm100` build 中报 manifest 6,862/29.2MB→3,476/14.8MB、主要 TU 1,175.2→205.1s、whole module 1,175.7→226.4s（5.2×）；11 text-transform tests 与 82 all-tactics numeric tests 通过。persisted `FLASHINFER_TACTICS_BLOCKLIST` 或保存的 autotune result 因 configIndex 重排可能陈旧，属于升级边界。[PR #4789](https://github.com/flashinfer-ai/flashinfer/pull/4789)
- **TensorRT-LLM #17985，8/27 合入：**MiniMax-M3 hybrid KV cache 让 57 sparse target 层用 NVFP4/P128、3 dense target 层用 FP8/P128、Eagle draft 层用 FP8/P32。pure decode 时可把 selected NVFP4 pages 转为 graph-stable FP8 scratch 并使用 preplanned MSA FP8 kernel；只有 q=1–8、P128、16:1 Q/KV head、staging operator 和 plan 都具备时启用，prefill/mixed/不合资格形状留 direct NVFP4。作者的 GB300 AgentX 3,600s A/B（1 CTX TP4+2 GEN TP4、C60、仅 sparse decode consumer 不同）报 served tok/s/GPU 31,543.67→33,780.86（+7.09%）、P90 TPOT 8.713→7.379ms（−15.31%）、P90 E2EL 19,513.46→16,036.29ms（−17.82%）；两 profile `submission_valid:true`。150/150 layout 和 169/169 changed-file tests 通过；所有数字为作者报告。[PR #17985](https://github.com/NVIDIA/TensorRT-LLM/pull/17985)

## 雷达与落选

- vLLM #53685 在 DeepSeek V4 Flash、TP4/EP4、1,024/128 random 64 requests/C16 的三轮作者 A/B 为 output tok/s 661.39→670.64（+1.40%）；与 #35634 的 DeepSeek/MoE 主线重叠，作为雷达。[PR #53685](https://github.com/vllm-project/vllm/pull/53685)
- vLLM #54088 为 H200 CUDA Graph、M1/2 的 36 个 GEMM shape microbenchmark，geomean 1.28×、1.04×–1.97×，没有服务 workload；FlashInfer #4442 的 top-k 数据指向外部 gist 且依赖未合入 CCCL；TensorRT-LLM #17862 是 GPU parity pending 的 draft，#17887 没有服务量化，均不升格。

## 编辑判断

本期主线是：fast path 的真实输入不只是模型和 GPU，而是 **容量、地址空间、consumer 和启动状态**。#35634 把模型/精度/runner/topology 的不相容组合前置为 fail-fast；#36541 表明内存配置可跨越整数地址临界点；#17985 的 staged cache 把 consumer 与 phase 写进 route；#4789 则把“不会被 dispatch 的编译工作”从冷启动预算中移除。#36330 说明即使 shape 严格受控、服务吞吐向上，也要保留 C16 TPOT 的反例。所有数字为开源 PR 作者报告，而非独立复现。

**KPI：Top5 新颖度均值 4.70；标准桶覆盖数 2（推理与系统、论文与开源；本窗口其余桶无合格新增事实）；开源一手 PR 作者报告 5，严格非官方社区信号 0；落选候选数 6；degraded：是，intel-scout 两轮均无首个模型事件，认证与系统 proxy 已确认，主控一手发现与审校流程继续。**
