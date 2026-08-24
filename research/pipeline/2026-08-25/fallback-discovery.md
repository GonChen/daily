# 2026-08-25 直接发现与核验

## 执行记录

八桶 `intel-scout` 连续两轮均未记录首个 assistant/model 事件；每轮观察约一分钟后强制停止。`pi auth check --model br/deepseek-v4-flash --json` 为 `ready`，进程环境含 `HTTP_PROXY` 与 `HTTPS_PROXY`，因此不能归因为缺少认证或系统代理。按 source-policy §7 退回主控的一手发现。

## 已核验候选

### 1. NVIDIA AgentX：机架级 agentic 效率主张

- 新事实：NVIDIA 于 8 月 24 日发布 AgentX 结果；称 Vera Rubin NVL72 相对 GB300 NVL72 最多 30× AI-factory throughput/MW，GB300 NVL72 相对 H200 NVL8 在 DeepSeek V4 Pro 1.6T 最多 15×、Kimi K3 2.8T 最多 80×。
- 边界：厂商博客；比较对象同时改变 GPU 代际、机架规模和系统软件；Vera Rubin 是 preview 结果，不能视作独立采购 TCO。
- 桶：chips / infra-capital；来源：[NVIDIA technical blog](https://developer.nvidia.com/blog/nvidia-vera-rubin-and-blackwell-set-a-new-standard-for-agentic-ai-performance-per-watt/)；可信级：厂商一手报告；新颖度 5，物质性 5；Top 5：是（量化能力变化）。

### 2. SGLang #34462：对滑动窗口 attention 的无效 tile 设下界

- 新事实：8 月 24 日合入；在 MI350X/gfx950、ROCm 7.2、gpt-oss-120b TP4、ISL 8192、cc8 的作者 A/B 测量中，SWA `_fwd_kernel` 从 725.4µs 至 96.9µs（−86.6%），总 prefill GPU 从 551.6ms 至 499.5ms（−9.4%）；8k/1k p99 在 cc16 为 −11.9%，1k/1k 基本中性。
- 边界：主线 PR 作者报告，单一 AMD 平台和模型；不是正式 release 或独立复现。
- 桶：inference-systems / community；来源：[SGLang PR #34462](https://github.com/sgl-project/sglang/pull/34462)；可信级：开源作者报告；新颖度 5，物质性 4；Top 5：是（量化性能变化）。

### 3. vLLM #53247：保持 batch invariance 的 persistent matmul 重调优

- 新事实：8 月 24 日合入；Qwen3-1.7B bf16、vLLM v0.27.0、19,200 点 sweep 的作者报告中，decode kernel 相对 `torch.mm` 从 0.254× 至 0.768×（RTX 4090 D，3.02×）和 0.212× 至 0.593×（H20，2.79×）；但增加 40 个 specializations，engine 初始化增加 14.8 秒。
- 边界：作者在 H20/RTX 4090 D 的离线表；未知架构与 dtype 保留旧配置；steady-state eager 仅在 RTX 4090 D 报告 +1.2% 中性。
- 桶：inference-systems / community；来源：[vLLM PR #53247](https://github.com/vllm-project/vllm/pull/53247)；可信级：开源作者报告；新颖度 5，物质性 4；Top 5：是（量化性能与成本变化）。

### 4. FlashInfer #4420：SM120/121 NVFP4 SVDQuant 与 LoRA-up 融合

- 新事实：8 月 24 日合入；RTX PRO 6000、rank 32、CUDA Graph replay、warm L2、Qwen3-image 12 形状 sweep 中，作者报告 `svdquant_linear` 相对 BF16 +112.4% 至 +193.3%，相对 FP8 +9.6% 至 +59.3%；fused 对比 unfused 快 +24.2% 至 +211.2%。
- 边界：仅 RTX PRO 6000；是算子/线性层延迟而非模型端到端吞吐；warm-cache 口径。
- 桶：chips / papers-oss / community；来源：[FlashInfer PR #4420](https://github.com/flashinfer-ai/flashinfer/pull/4420)；可信级：开源作者报告；新颖度 4，物质性 4；Top 5：是（量化性能变化）。

### 5. vLLM #53361：DeepSeek V4 的 live-adapter LoRA 正确性

- 新事实：8 月 24 日合入；修复量化 MoE experts/MTP draft head 的 merge=False LoRA 映射和 wrapper 属性问题。作者在两节点 Megatron GRPO E2E 报告 log-prob Pearson 从约 0.43 升至 0.99705/0.9950，并与 merge=True 基线 0.99525/0.99440 对齐。
- 边界：只报两步 Pearson 与单一 verl 流程；并非 DeepSeek 官方模型发布、也不是适配器吞吐测量。
- 桶：models-agents / deepseek-radar / community；来源：[vLLM PR #53361](https://github.com/vllm-project/vllm/pull/53361)；可信级：开源作者报告；新颖度 4，物质性 4；Top 5：是（量化能力/正确性变化）。

### 6. vLLM #53561：音频输入大小限制补齐

- 新事实：8 月 24 日合入，把 `VLLM_MAX_AUDIO_CLIP_FILESIZE_MB` 从 STT upload 扩展到文件、bytes、base64 和 HTTP 下载路径，并修正了未真正执行 early-rejection 的测试 mock。
- 边界：没有性能或攻击实测；只适合安全雷达。
- 桶：models-agents；来源：[vLLM PR #53561](https://github.com/vllm-project/vllm/pull/53561)；可信级：主线安全修复；新颖度 4，物质性 3；Top 5：否（补齐边界但缺可量化影响）。

## 明确拒绝与安静窗口

- SGLang #34461 同为 MI350X attention tile 优化，作者报告 prefill GPU −13.8%、cc16 TTFT −15.9%；与 #34462 同一堆叠分支且主题重合，保留在深度交叉分析，不独占 Top 5。[PR #34461](https://github.com/sgl-project/sglang/pull/34461)
- FlashInfer #4576、#4699、#4660 与 vLLM #53318 只有特性或调优标题，未找到足以独立写作的完整端到端边界；不补量。
- DeepSeek 官方组织最近 push 停在 deepseek-harness 8 月 21 日、DeepEP 8 月 20 日，最近 24–72 小时无 release、tag 或 commit；官方雷达安静。
- Claude Code v2.1.241 与 Codex 0.149.1 仅有版本递增，未出现相对上期可核验的实质正文；不重复。
- 中文产业、独立论文与数据中心/资本检索未找到本窗口内足以交叉核验的新一手事实；不将搜索结果中的转述或旧日期材料写入正文。
