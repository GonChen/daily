# 2026-08-26 去重基线

## 最近两期已覆盖，不可作为主事实重复

- 2026-08-25：NVIDIA AgentX 厂商报告的 Vera Rubin/GB300/H200 throughput-per-MW 结果（30×/15×/80×）。
- 2026-08-25：SGLang #34462 的 MI350X/gfx950 sliding-window KV loop 下界，−86.6% SWA kernel、−9.4% prefill GPU、8k/1k cc16 p99 −11.9%。
- 2026-08-25：vLLM #53247 batch-invariant persistent matmul，4090 D/H20 decode kernel 3.02×/2.79×与 +14.8s 初始化。
- 2026-08-25：FlashInfer #4420 的 RTX PRO 6000 warm-L2 SM120 NVFP4 SVDQuant 算子结果。
- 2026-08-25：vLLM #53361 的 DeepSeek V4 merge=False LoRA Pearson 对齐。
- 2026-08-24：FlashInfer #4593 VSA、#4686 W4A16 autotune；Claude Code v2.1.239；SGLang #34237 工具调用 parser。

## 本期约束

只有相对上列事实出现新的、可链接的一手 release、合入 PR、模型/产品文件、监管/财报文件或独立复测才可入 Top。不能把 #34461 与 #34462 的相同堆叠分支重写成新卡；不能把版本递增、nightly 或没有正文的 release 写入主内容。性能需带模型、硬件、形状、并发、缓存/预热和数值/测试边界。上期芯片供应链、中文产业、论文与资本窗口缺合格事实；本期仍须真实动态发现，不以旧闻补量。
