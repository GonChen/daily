# 2026-08-26 research ledger

## 采集与降级

已完成 8/24、8/25 去重基线与八个新反向搜索角度。两轮八桶 `intel-scout` 和一次 `intel-editor` 均在首个模型事件前停滞；`pi auth check --model br/deepseek-v4-flash --json` 返回 `ready`，进程继承 `HTTP_PROXY`、`HTTPS_PROXY`。因此 Stage 1–2 降级为主控的一手发现；两项 `intel-analyst` 在本期成功完成并写出深挖。主控通过 GitHub API 扫描 SGLang、vLLM、FlashInfer、TensorRT-LLM、DeepSeek 组织，并检索芯片/基础设施、模型/Agent、中文产业和论文窗口。完整候选与落选见 [fallback discovery](pipeline/2026-08-26/fallback-discovery.md)、[selection](pipeline/2026-08-26/selection.md)、[shape/topology deep dive](pipeline/2026-08-26/deep-shape-topology.md)、[correctness contract deep dive](pipeline/2026-08-26/deep-correctness-contract.md)。

## 入选事实

- **SGLang #36219，8/25 合入：**DP prefill 的 FlashInfer EXTEND autotune 不再把全局 32,768 token budget 当作每 rank shape；全局/本地 chunk 32,768/8,192 时改为预热 8,192，并补齐 PD prefill 和 text-only wrapper。作者在 Qwen3.5-397B-A17B-NVFP4、GB300、DEP4 prefill+DEP4 decode、同一 frozen manifest 的 A/B 中报告 C4–64 TPS/chip +4.940% 至 +6.767%；C128 的 +3.662% 因 CV 3.954% 超过预注册 1% 门槛被排除。GSM8K 200 题 0.985、零 retract/error。是主线 PR 作者报告，不是独立复现。[PR #36219](https://github.com/sgl-project/sglang/pull/36219)
- **vLLM #49636，8/25 合入：**为 DeepSeek V4 加 opt-in FlashInfer MoE-EP backend；后端、SM100、NVSHMEM、EPLB 与 capture 限制成为显式 config gate。作者在 vLLM 0.25.1、1×8 B200、TP8+EP8、重复 HTTP serving 中报告 V4-Flash 对 native 1.049×–1.199×、V4-Pro 1.170×–1.305×。这些为 pre-sequence-parallel stack，且 `fi_cutedsl` 是跨 checkpoint 比较；GSM8K 200 题 Flash 0.965/0.965/0.965，Pro 0.880/0.880/0.890 是其可比性 gate，不是独立证明。[PR #49636](https://github.com/vllm-project/vllm/pull/49636)
- **vLLM #51292，8/25 合入：**请求 `VLLM_BATCH_INVARIANT=1` 时，TP>1 的 FlashInfer fused all-reduce+RMSNorm 会因 runtime reduction order 产生不同 logprob/token，现在显式关闭该 fusion 并回退。作者在 H100、Qwen2.5-7B、TP4、2,000 prompts 重复 8 次中报告 distinct bit-exact outputs 8→1；没有 #50505 的历史 fallback 中，decode-heavy 7B 为 18,355→7,450 tok/s，70B 为 1,618→935 tok/s。作者称 #50505 的 deterministic 1-stage path 约为 fused 的 97%，仍需独立核验。[PR #51292](https://github.com/vllm-project/vllm/pull/51292)
- **FlashInfer #4502，8/25 合入：**SM120 NVFP4 attention 使用 N64/N64 score-slot reuse，且 API 默认 `return_lse=False`；需要 LSE 的调用方必须显式传 `return_lse=True`。作者在 RTX PRO 6000 Blackwell Server Edition、BF16、D128、CUDA Graph attention-only、10 warmup 后 100 次 median 报 B1/H8/S32768 causal 2.516→2.207ms（相对 CuTe DSL report −12.3%），noncausal 4.398→4.079ms（−7.3%）；相对 #3640 report 最高 −26.0%。基线不是同一 run 重测，排除 QKV quantization；16 tests 通过。[PR #4502](https://github.com/flashinfer-ai/flashinfer/pull/4502)
- **SGLang #35505，8/25 合入：**DeepSeek-V4-Flash `flashinfer_mxfp4` / trtllm-gen 路径把 shared expert 作为 slot 256 放进同一 MoE kernel/stream，约少 4 次 launch、2 次 stream sync；缺少 per-rank shared slot 的 EP 直接拒绝 fusion，避免静默错算。作者在 GB200 TP4、1024in/512out 中报告 QPS 1/4/8 TTFT −13.4%/−14.0%/−21.0%，QPS4 p99 ITL −52.6%，GSM8K/AIME25 与基线相近。仅 GB200 TP4，主 CI 描述仍有失败标记。[PR #35505](https://github.com/sgl-project/sglang/pull/35505)

## 雷达与落选

- TensorRT-LLM #17955 让 one-model speculative path 在 admission 阶段拒绝无法实现的非中性 `min_length`、`bad_words`、`no_repeat_ngram_size`、`embedding_bias`、`top_p_decay`，替代此前“静默丢约束仍返回”的行为；有参数化测试，但没有吞吐、失败率或事故数据，进入请求语义雷达。[PR #17955](https://github.com/NVIDIA/TensorRT-LLM/pull/17955)
- vLLM #53649 的 33.6% latency headline 没有 GPU、batch、context 或初始化口径；#52388 仅有 Kimi K3 Mamba metadata microbenchmark，没有端到端服务测量，均不升格。
- #34461/#34462、#53247、#4420、#53361 和 NVIDIA AgentX 均为前一期已覆盖主题且没有新一手变化；DeepSeek 官方组织最近 push 仍为 harness 8/21、DeepEP 8/20。芯片供应链/资本、中文产业、论文和 Agent 产品 release 没有合格新一手事实，保持安静。

## 编辑判断

本期主线是：fast path 的前提不是“硬件支持”，而是它看到的每 rank shape、TP/EP 拓扑与请求契约均与生产状态一致。#36219 的全局/本地 32,768/8,192 错配、#49636 的 backend/capture gate、#51292 的 deterministic fallback 和 #35505 的 EP fail-closed 都把隐含前提转为显式准入。#4502 进一步提醒 API 返回值默认也属于性能集成的一部分。所有性能、准确性与 97% 数字均为开源 PR 作者报告。

**KPI：Top5 新颖度均值 4.80；覆盖桶数 5；社区源条数 5；落选候选数 5；degraded：scout/editor pi-subagents unavailable（两轮 scout 和 editor 均在首个模型事件前停滞；本期两项 analyst 成功；br 认证与系统 proxy 均已确认）。**
