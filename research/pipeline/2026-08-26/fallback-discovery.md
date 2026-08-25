# 2026-08-26 直接发现与核验

## 执行记录

八桶 `intel-scout` 连续两轮均未记录首个 assistant/model 事件；每轮约一分钟后停止。`pi auth check --model br/deepseek-v4-flash --json` 是 `ready`，进程继承 `HTTP_PROXY`、`HTTPS_PROXY`。按 source-policy §7 降级为主控一手发现：GitHub API 扫描 SGLang、vLLM、FlashInfer、TensorRT-LLM 和 DeepSeek 组织；另检索芯片/基础设施、模型/Agent、中文产业与论文窗口。

## 已核验候选

### 1. SGLang #36219：DP prefill 用本地 scheduler shape 做 EXTEND warmup

- 新事实：8 月 25 日合入；DP 全局/本地 chunk 为 32768/8192 时，EXTEND autotune 从错误的 32768 token 改为每 rank 的 8192 token buffer，并补齐 PD prefill 和 text-only wrapper。
- 数字与边界：Qwen3.5-397B-A17B-NVFP4、GB300、DEP4 prefill+DEP4 decode、RadixCache、OSL1、同一 frozen manifest，TPS/chip 在 C4–64 增加 4.940%–6.767%；C128 的 +3.662% 因 candidate wave CV 3.954% 超过预注册 1% 门槛而排除。GSM8K 200 题 0.985、零 retract/error。
- 桶：inference-systems / community；来源：[SGLang #36219](https://github.com/sgl-project/sglang/pull/36219)；可信级：主线 PR 作者报告；新颖度 5，物质性 5；Top 5：是（量化部署性能）。

### 2. vLLM #49636：DeepSeek V4 opt-in FlashInfer MoE-EP backend

- 新事实：8 月 25 日合入；增加两个 runtime `moe_backend`，并对 SM100、NVSHMEM、EPLB 和 capture config 做显式约束。`fi_dg` 作为集成层 control；`fi_cutedsl` 是不同 NVFP4 checkpoint 的 kernel 路径。
- 数字与边界：vLLM 0.25.1、1×8 B200、TP8+EP8 的重复 HTTP serving 中，V4-Flash 对 native 为 1.049×–1.199×，V4-Pro 为 1.170×–1.305×；GSM8K 200 题的 Flash 为 0.965/0.965/0.965，Pro 为 0.880/0.880/0.890。数字来自 pre-sequence-parallel stack 且是跨 checkpoint 比较；吞吐需由 accuracy gate 限制。
- 桶：models-agents / deepseek-radar / community；来源：[vLLM #49636](https://github.com/vllm-project/vllm/pull/49636)；可信级：主线 PR 作者报告；新颖度 5，物质性 5；Top 5：是（量化能力/吞吐）。

### 3. vLLM #51292：batch invariance 在 TP 下禁用 nondeterministic fusion

- 新事实：8 月 25 日合入；Hopper/Blackwell 的 FlashInfer fused all-reduce+RMSNorm 在 TP>1 时使 byte-identical run 产生不同 logprob/token；请求 batch invariance 时现在显式回退。
- 数字与边界：H100、Qwen2.5-7B、TP4、2,000 prompts 重复 8 次，修复前 8 个 distinct bit-exact outputs，修复后为 1；在没有 #50505 的历史 fallback 下，decode-heavy 7B 为 18,355→7,450 tok/s、70B 为 1,618→935 tok/s。作者称 #50505 的 deterministic 1-stage path 接近 fused 的约 97%，但该数值需独立核对。
- 桶：inference-systems / community；来源：[vLLM #51292](https://github.com/vllm-project/vllm/pull/51292)；可信级：主线 PR 作者报告；新颖度 5，物质性 5；Top 5：是（量化正确性/成本权衡）。

### 4. FlashInfer #4502：SM120 NVFP4 attention score-slot reuse 与 LSE 默认

- 新事实：8 月 25 日合入；SM120 attention 把 N64/N64 score slot 复用，且 `return_lse=False` 成为默认。调用方若需要原来的 `(out,lse)` 必须显式传 `return_lse=True`。
- 数字与边界：RTX PRO 6000 Blackwell Server Edition、BF16、D128、CUDA-Graph attention-only、10 warmups 后 100 次 median：对 CuTe DSL report，B1/H8/S32768 causal 2.516→2.207ms（−12.3%），noncausal 4.398→4.079ms（−7.3%）；相对 #3640 report 最高 −26.0%。基线不是同一 run 重测；排除 QKV quantization，16 tests 通过。
- 桶：chips / papers-oss / community；来源：[FlashInfer #4502](https://github.com/flashinfer-ai/flashinfer/pull/4502)；可信级：主线 PR 作者报告；新颖度 4，物质性 4；Top 5：是（量化性能与 API 行为）。

### 5. SGLang #35505：无 EP 的 shared-expert fusion

- 新事实：8 月 25 日合入；DeepSeek-V4-Flash 在 `flashinfer_mxfp4` / trtllm-gen 路径把 shared expert 放入 slot 256，同一 MoE kernel/stream 执行，少约 4 次 kernel launch 与 2 次 stream sync；EP 未提供 per-rank shared slots 时直接拒绝 fusion，避免静默错算。
- 数字与边界：GB200 TP4、1024in/512out，QPS 1/4/8 的 TTFT 分别 −13.4%/−14.0%/−21.0%，QPS4 p99 ITL −52.6%；GSM8K 和 AIME25 结果相近。PR 作者报告；仅 GB200 TP4，无 EP fast path，主 CI 描述中仍有失败标记。
- 桶：models-agents / deepseek-radar / community；来源：[SGLang #35505](https://github.com/sgl-project/sglang/pull/35505)；可信级：主线 PR 作者报告；新颖度 5，物质性 4；Top 5：是（量化性能与正确性 guard）。

### 6. TensorRT-LLM #17955：speculative path 改为拒绝不可实现的采样请求

- 新事实：单模型 speculative `SpecSampler` 先前会静默丢弃 `min_length`、`bad_words`、`no_repeat_ngram_size`、`embedding_bias`、`top_p_decay`，现在在 request admission 只拒绝非中性值。
- 边界：有参数化双向测试；无吞吐、用户成功率或事故数据。
- 桶：models-agents / community；来源：[TensorRT-LLM #17955](https://github.com/NVIDIA/TensorRT-LLM/pull/17955)；可信级：主线语义修复；新颖度 4，物质性 4；Top 5：否（缺量化部署结果，进入雷达）。

## 拒绝与安静窗口

- vLLM #53649 报 0.770→0.576s、33.6% batch-invariant latency 改善，但 PR 没有明确 GPU、batch、context 或 pre/post initialization 口径；不将标题数字独立升格。
- vLLM #52388 的 Kimi K3 Mamba metadata microbenchmark 6.67×–7.55×，没有端到端服务数据；只进算子雷达。
- SGLang #34461/#34462、vLLM #53247、FlashInfer #4420 与 #53361 都是前一期已覆盖主题，且没有新一手变化；不重复。
- DeepSeek 官方组织最近 push 仍停在 harness 8/21、DeepEP 8/20；无 release/tag/commit。芯片供应链/资本、中文产业、论文和 Agent 产品 release 未发现合格一手新事实；保持安静。
