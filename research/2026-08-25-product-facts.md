# 2026-08-25 research ledger

## 采集与降级

已完成 8/23、8/24 去重基线和八个新反向搜索角度。两轮八桶 `intel-scout`、一次 `intel-editor` 与两次 `intel-analyst` 均在首个模型事件前停滞，未生成内容；每个线程均在约一分钟观察后停止。`pi auth check --model br/deepseek-v4-flash --json` 返回 `ready`，且进程继承 `HTTP_PROXY`、`HTTPS_PROXY`。降级原因是子代理的模型首事件卡住，**不是**缺少认证或系统代理变量。主控按 source-policy §7 使用 GitHub API、合入 PR 原文与官方工程博客完成动态发现、核验、选题与深挖。完整候选和拒绝见 [fallback discovery](pipeline/2026-08-25/fallback-discovery.md)、[selection](pipeline/2026-08-25/selection.md)、[workload deep dive](pipeline/2026-08-25/deep-workload-unit.md) 与 [warmup deep dive](pipeline/2026-08-25/deep-warmup-correctness.md)。

## 入选事实

- **NVIDIA AgentX，8/24 官方博客：**NVIDIA 称 Vera Rubin NVL72 相对 GB300 NVL72 最多 30× AI-factory throughput/MW；GB300 NVL72 相对 H200 NVL8 在 DeepSeek V4 Pro 1.6T 最多 15×、Kimi K3 2.8T 最多 80×。该口径尝试包含长 context、KV reuse、tool gap 和动态并发，但它是厂商报告，同时改变 GPU 代际、机架规模和软件栈；Vera Rubin 是 preview，不能换算成独立采购 TCO。[official blog](https://developer.nvidia.com/blog/nvidia-vera-rubin-and-blackwell-set-a-new-standard-for-agentic-ai-performance-per-watt/)
- **SGLang #34462，8/24 合入：**对滑动窗口 extend-attention KV loop 加下界。PR 作者在 MI350X/gfx950、ROCm 7.2、gpt-oss-120b TP4、ISL 8192、cc8 中报告 SWA kernel 725.4µs→96.9µs（−86.6%）、总 prefill GPU 551.6ms→499.5ms（−9.4%）；8k/1k 在 cc16 的 p99 −11.9%，而 1k/1k 基本中性。是单一平台/模型的主线 PR 作者 A/B 测量，不是 release 或独立复现。[PR #34462](https://github.com/sgl-project/sglang/pull/34462)
- **vLLM #53247，8/24 合入：**为 batch-invariant persistent matmul 加 Hopper/Ada 离线调优表。作者在 Qwen3-1.7B bf16、vLLM v0.27.0、19,200 点 sweep 中报告 decode kernel 相对 `torch.mm` 从 0.254×→0.768×（RTX 4090 D，3.02×）、0.212×→0.593×（H20，2.79×）；而 3→43 个 specializations 令 engine 初始化增加 14.8 秒。未知架构/dtype 回退旧表；steady-state eager 只在 4090 D 报告 +1.2% 中性。[PR #53247](https://github.com/vllm-project/vllm/pull/53247)
- **FlashInfer #4420，8/24 合入：**为 SM120/SM121 加 NVFP4 SVDQuant GEMM 和 fused BF16 LoRA-up。作者在 RTX PRO 6000、rank 32、CUDA Graph replay、warm L2 的 12 形状 Qwen3-image sweep 中报告相对 BF16 +112.4% 至 +193.3%、相对 FP8 +9.6% 至 +59.3%、fused 对比 unfused +24.2% 至 +211.2%。这些是热缓存的算子延迟，非整模型吞吐，且未覆盖其他 GPU。[PR #4420](https://github.com/flashinfer-ai/flashinfer/pull/4420)
- **vLLM #53361，8/24 合入：**为带量化 MoE experts 和 MTP draft head 的 DeepSeek V4 加 merge=False live-adapter LoRA，修复权重映射与 wrapper 属性路径。作者在两节点 Megatron GRPO E2E 报告 log-prob Pearson 从约 0.43→0.99705/0.9950，接近 merge=True 基线 0.99525/0.99440。它是两步、单一 verl 流程的正确性信号，不是 DeepSeek 官方发布或吞吐测量。[PR #53361](https://github.com/vllm-project/vllm/pull/53361)

## 雷达与落选

- SGLang #34461 与 #34462 同一堆叠分支，虽在 MI350X 作者测量中报告 prefill GPU −13.8%、cc16 TTFT −15.9%，但不单独占据 Top；用于解释组合复测为何必要。[PR #34461](https://github.com/sgl-project/sglang/pull/34461)
- vLLM #53561 把 `VLLM_MAX_AUDIO_CLIP_FILESIZE_MB` 覆盖到所有音频入口并修正 early-rejection 测试 mock；无性能或攻击实测，保留为安全雷达。[PR #53561](https://github.com/vllm-project/vllm/pull/53561)
- DeepSeek 官方组织在 24–72 小时窗口没有新 release、tag 或 commit（harness 最近 push 为 8/21、DeepEP 为 8/20）；Claude Code v2.1.241 与 Codex 0.149.1 无可提取的相对基线正文，均不重复。
- 芯片供应链/资本、中文产业与论文窗口未找到可交叉核验的一手新事实；不以转述、旧消息或单一空版本填充。

## 编辑判断

本期主线是：性能结论的最小可信单位是完整、可复述的工作负载。NVIDIA 的 AgentX 尝试把 session 级因素纳入机架报告；SGLang 则量化展示局部 −86.6% kernel 只传导为 −9.4% prefill GPU；vLLM 展示确定性允许的 3× decode-kernel 改善也同时带来 14.8 秒初始化成本；FlashInfer 和 DeepSeek V4 LoRA 分别把热缓存形状边界与 live adapter 数值语义暴露出来。所有 PR 性能/正确性数值均为作者报告。

**KPI：Top5 新颖度均值 4.60；覆盖桶数 6；社区源条数 4；落选候选数 5；degraded：pi-subagents unavailable（两轮 scout、editor 与两项 analyst 都在首个模型事件前停滞；br 认证与系统 proxy 均已确认）。**
