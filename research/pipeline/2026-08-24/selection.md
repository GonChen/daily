# 2026-08-24 选题定稿

降级说明：八个 `intel-scout` 线程两轮均在首个响应窗口内无工具活动；`web-search` 与 `intel-editor` 也未产生首个模型事件。`pi auth check --model br/deepseek-v4-flash --json` 返回 ready，系统 HTTP(S) proxy 已存在；本期按 source policy 第 7 节使用直接一手核验并由主控筛选。

## 入选与配额

| 候选 | 新颖度 | 物质性 | 可验证性 | 准入项 | 桶 | 结论 |
|---|---:|---:|---:|---|---|---|
| FlashInfer #4593：SM100/103 VSA | 5 | 5 | 4 | 量化性能变化 | 芯片/硬件路径 | 入选；开源作者报告 |
| FlashInfer #4686：W4A16 dense GEMM | 5 | 4 | 4 | 量化性能变化 | 推理内核 | 入选；开源作者报告 |
| Claude Code v2.1.239 | 4 | 4 | 5 | 量化成本口径、稳定产品更新 | 模型与 Agent | 入选；稳定 release |
| SGLang #34237：LFM2 工具解析 | 5 | 4 | 4 | 具名公开工程事实 | 模型与 Agent | 入选；主线正确性修复 |
| SGLang #35405：SM107 MXFP8 | 4 | 3 | 4 | — | 推理框架 | 落选；无性能/任务级数据，且接近 8/21 主题 |
| vLLM #53460 / #52209 | 4 | 3 | 4 | — | 开源模型 | 落选；无可提取量化影响或产品 release |

- Top 条数：4，不凑满 5。
- 桶覆盖：芯片/硬件路径、推理内核、模型与 Agent = 3 桶。
- 动态发现：4 条，均在 8/21–8/23 新发现窗口内；社区/非官方一手：2 条（FlashInfer 公开合入 PR 的作者基准）；固定雷达无变化触发：0 条。

## Top 4

1. **FlashInfer #4593**：SM100/103 block-sparse VSA 的 16 个 canonical kernel/API 行几何均速 1.902192×，但 FastWan 全生成端到端仅 1.015714×。这是作者在指定环境的同步测量，不是通用模型吞吐。[PR](https://github.com/flashinfer-ai/flashinfer/pull/4593)
2. **FlashInfer #4686**：B300/SM103 W4A16 dense GEMM 在 16 个形状中报 1.029759×几何均速，15/16 改善；冷启动 autotuning profile time 同时增加 2.12×。无端到端模型基准、仅单 B300，因此必须把首次调优成本纳入部署评估。[PR](https://github.com/flashinfer-ai/flashinfer/pull/4686)
3. **Claude Code v2.1.239**：`/cost`、状态行及 `--max-budget-usd` 计入 1.1× US-only-inference premium；修复特定 Bedrock 代理路径可能静默重复 non-streaming 请求的计费风险，以及 SSO profile 下 `HTTPS_PROXY` 启动挂起。前者是价格口径，后者是特定错误路径，不应外推成普遍降本。[release](https://github.com/anthropics/claude-code/releases/tag/v2.1.239)
4. **SGLang #34237**：LFM2/LFM2.5 tool-call parser 针对真实 SWE-agent/shell traces 将若干 valid-call silent drop 改为值保真恢复或 fail-closed 拒绝；19 个新增 regression cases 与 42-payload differential harness 通过。没有任务成功率或时延数据，不能宣称 agent 成功率已提升。[PR](https://github.com/sgl-project/sglang/pull/34237)

## 深挖题

1. **“局部更快”何时能成为“工作流更快”**：对比 FlashInfer #4593 的 kernel/API 与 FastWan E2E 数据，及 #4686 的 kernel gain 与 cold autotune 成本；给出部署阈值、对比表和证伪条件。
2. **Agent 成本与正确性需要统一成请求语义**：连接 Claude Code 的价格/代理重试与 SGLang 的 tool-call salvage；分析“显示预算”“重复请求”和“丢工具调用”的不同失真，明确不把它们写成统一性能收益。
