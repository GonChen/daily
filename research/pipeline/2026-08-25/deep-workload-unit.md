# 深挖：性能的可信单位是完整工作负载，不是单个倍数

## 对比

| 层级 | 新事实与数字 | 已知边界 |
|---|---|---|
| 机架 / agent 会话 | NVIDIA 在 AgentX 上称 Vera Rubin NVL72 相对 GB300 NVL72 最多 30× throughput/MW；GB300 NVL72 相对 H200 NVL8 在 DeepSeek V4 Pro 1.6T 最多 15×、Kimi K3 2.8T 最多 80×。 | 厂商报告；GPU 代际、节点规模、软件栈同时变化；Vera Rubin 为 preview。 |
| served prefill | SGLang #34462：MI350X/gfx950、ROCm 7.2、gpt-oss-120b TP4、ISL 8192、cc8，SWA kernel 725.4µs→96.9µs（−86.6%），总 prefill GPU 551.6ms→499.5ms（−9.4%）。 | PR 作者 A/B 测量，非正式 release；单一模型与平台。 |
| 用户请求 | 同一 #34462 的 8k/1k 在 cc16：p50 −5.5%、p99 −11.9%、output tok/s +1.5%；1k/1k 在各并发度内约 ±2.6%。 | 不应从 8k/1k 外推到其他 context、并发或 decode 主导服务。 |
| 同层互补优化 | 堆叠的 #34461 在同平台作者测量中将总 prefill GPU 654.6ms→564.1ms（−13.8%），cc16 TTFT −15.9%。 | 与 #34462 同分支，缺少合并后组合 benchmark；两个降幅不能相加。 |

## 判断

AgentX 的价值在于它把长 context prefill、KV reuse、tool-call gap 和动态并发放到同一会话，而 SGLang 的数据给出同一原则的反例：一个已减少 86.6% 的局部 SWA kernel，穿过完整 prefill 后只剩 9.4%，再穿过排队、网络、decode 与并发后，8k 请求的 p99 改善仍是约 0.6% 至 11.9%。这不是优化失败，而是 Amdahl 定律和服务工作负载的正常结果。

## 部署 / 成本含义

容量模型不应把 kernel 微基准乘到每瓦或每 token。先以生产 trace 分出 prefill、decode、通信、排队和工具等待；再在每个请求形状、并发与 cache-hit 分桶内报告 TTFT、TPOT、p50/p99、每瓦吞吐。若服务的请求主要是 1k/1k，则 #34462 的收益可能接近噪声；若是 8k prefill 且并发上升，先验更强。机架级数字只可用于提出验证假设，不可替代同模型、同并发、同功耗边界的复测。

## 证伪条件

1. 在 MI350X 以外的 AMD GPU 或不同模型/滑动窗口比例复测后，若 8k 的 TTFT 与 p99 不改善，则局部机制没有转化为该工作负载收益。
2. 在相同模型、参数、请求回放、机架规模和功耗测量边界下复测 AgentX；若 NVIDIA 的优势消失或显著收窄，厂商跨系统比较不能用作采购收益。
3. 对 #34461/#34462 合并后直接作 A/B/A；若组合收益低于任一单项的可重复变化，不能将单 PR 结果叠加进容量计划。

来源：[NVIDIA AgentX](https://developer.nvidia.com/blog/nvidia-vera-rubin-and-blackwell-set-a-new-standard-for-agentic-ai-performance-per-watt/)；[SGLang #34462](https://github.com/sgl-project/sglang/pull/34462)；[SGLang #34461](https://github.com/sgl-project/sglang/pull/34461)。
