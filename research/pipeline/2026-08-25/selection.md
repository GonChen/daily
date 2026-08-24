# 2026-08-25 选题决议（主控降级执行）

## Top 5

| 排名 | 事实 | 桶 | 新颖度 | 物质性 | 可验证性 | 准入线 |
|---:|---|---|---:|---:|---:|---|
| 1 | NVIDIA AgentX 的 NVL72 throughput/MW 主张 | chips / infra | 5 | 5 | 4 | 1，厂商量化报告 |
| 2 | SGLang #34462 绑定 SWA KV loop | inference | 5 | 4 | 4 | 1，开源作者量化报告 |
| 3 | vLLM #53247 的 batch-invariant matmul 表 | inference | 5 | 4 | 4 | 1，开源作者量化报告 |
| 4 | FlashInfer #4420 的 SM120 NVFP4 SVDQuant | chips / papers-oss | 4 | 4 | 4 | 1，开源作者量化报告 |
| 5 | vLLM #53361 的 DeepSeek V4 live-adapter LoRA | models-agents / deepseek-radar | 4 | 4 | 4 | 1，开源作者量化正确性报告 |

配额结论：5/5 来自当日动态发现；覆盖 chips、infra、inference、papers-oss、models-agents、deepseek-radar 六桶；开源 PR 作者报告 4 条，为社区一手信号；固定雷达触发 0 条。NVIDIA 数字是厂商在多代际、多机架比较中的宣传性结果，必须显著标出而不能折算成通用 TCO。

## 编辑主线

**从 kernel 到 AI factory，性能结论的最小可信单位是完整、可复述的工作负载。** NVIDIA 的 AgentX 将长上下文、缓存、工具间隙和动态并发纳入机架级声明；SGLang 的 served profile 显示一个 −86.6% SWA kernel 变化只传导为 −9.4% prefill GPU；vLLM 则证明确定性约束能以 3× decode-kernel 速度和 14.8 秒初始化成本同时出现。FlashInfer 和 DeepSeek V4 LoRA 补足量化/适配器的形状与正确性边界。

## 深挖题

1. `deep-workload-unit.md`：比较 AgentX 的系统级口径与 SGLang #34462/#34461 的局部、prefill 和 served 指标，解释为何不能把同一“倍数”跨层相加；给出复测条件。
2. `deep-warmup-correctness.md`：比较 vLLM #53247 的 steady-state/初始化取舍、FlashInfer #4420 的 warm-L2 CUDA Graph 口径和 vLLM #53361 的 merge=False 正确性；给出上线门槛。

## 落选

- SGLang #34461：数值扎实但与 #34462 同一堆叠分支，避免同主体同日重复占 Top。
- vLLM #53561：安全边界值得关注，但没有量化攻击、性能或可用性数据，进入框架雷达。
- DeepSeek 官方组织：24–72 小时无 release/tag/commit。
- Claude Code / Codex 小版本：无相对基线的实质正文。
- 中文产业、论文、数据中心/资本：无可核验一手新事实；明确安静。
