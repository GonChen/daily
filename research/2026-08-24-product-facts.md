# 2026-08-24 research ledger

## 采集与降级

已完成 8/21、8/23 的去重基线与八个新搜索角度。两轮八桶 `intel-scout`、一次 `web-search` 兜底和一次 `intel-editor` 均在首个模型事件前停滞，未写出候选。`pi auth check --model br/deepseek-v4-flash --json` 返回 `ready`，且进程继承 `HTTP_PROXY`、`HTTPS_PROXY`；因此降级原因是子代理模型执行首事件卡住，不是认证或系统代理变量缺失。主控改用 GitHub API、官方 release 与已合入 PR 直接发现、核验与选题。完整候选和拒绝见 [fallback discovery](pipeline/2026-08-24/fallback-discovery.md) 与 [selection](pipeline/2026-08-24/selection.md)。

## 入选事实

- **FlashInfer #4593，8/23 合入：**为 SM100/SM103 增加优化的 block-sparse VSA attention。PR 作者在 16 个 canonical kernel/API 行报告 1.902192×几何均速（最小 1.029429×）；FastWan 两个全生成 ABBA/BAAB 工作流、含 61 帧 materialization，汇总为 1.015714×。这些是特定环境、形状和作者测量，不是独立复现或通用模型吞吐。[PR #4593](https://github.com/flashinfer-ai/flashinfer/pull/4593)
- **FlashInfer #4686，8/23 合入：**SM100/SM103 W4A16 dense GEMM 改为 O3 并将 raster direction 扩展到 30 个 tactics。一张 B300/SM103 的 16 形状 A/B/A CUPTI 测量报告 1.029759×几何均速，范围 0.996866–1.060623×，15/16 改善；cold autotuning profile time 却由 196.68s 增至 417.83s（2.12×）。没有端到端模型测试、B200/SM100 最终测量或全库测试。[PR #4686](https://github.com/flashinfer-ai/flashinfer/pull/4686)
- **Claude Code v2.1.239，8/21 稳定发布：**成本显示与 `--max-budget-usd` 纳入数据驻留 workspace 的 1.1× US-only-inference premium；修复了 Bedrock 代理剥离 response `Content-Type` 后重跑 non-streaming、可能静默重复计费的错误路径，并让 SSO profile 的 credential pre-check 尊重 `HTTPS_PROXY`。1.1×是价格口径；重复计费是特定 bug 风险，不能外推成普遍降本。[official release](https://github.com/anthropics/claude-code/releases/tag/v2.1.239)
- **SGLang #34237，8/23 合入：**针对真实 LFM2/LFM2.5 SWE-agent 与 shell-command traces，将已知 Python-like tool-call 格式偏差中的 silent drop 改为可验证、值保真的恢复或 fail-closed 拒绝；新增 19 个 regression cases，与 vLLM 同类 parser 的 42-payload differential harness 对齐。没有公开 task success-rate、时延或成本数据。[PR #34237](https://github.com/sgl-project/sglang/pull/34237)

## 雷达与落选

- SGLang #35405 修复 SM107 MXFP8 activation 的 FlashInfer producer/consumer 合约，4 个 focused tests 在 real weights 上通过；没有速度或任务级数据，且接近 8/21 已覆盖主题，只入雷达。[PR #35405](https://github.com/sgl-project/sglang/pull/35405)
- vLLM #53460 完成 Dots3 NOTE Omni 的 cache/encoder 修复和 8×H100 end-to-end evaluation，但没有吞吐、时延或 API/模型发布数据；#52209 支持 gpt-oss 的逐专家加载但没有可提取指标。均不进入 Top。[#53460](https://github.com/vllm-project/vllm/pull/53460) [#52209](https://github.com/vllm-project/vllm/pull/52209)
- SGLang v0.5.18、DeepSeek Harness RC1/RC2、DeepGEMM #410、vLLM #52989 及 Ohio 基础设施事实均无新一手变化，遵守去重不重复。Codex alpha.7 与 Claude Code v2.1.241 缺少实质公开正文；FlashInfer nightly、旧 release、TensorRT-LLM RC 不构成当日主内容。
- 芯片供应链、数据中心/资本、中文产业、论文窗口没有找到相对基线足够新的主卡级一手事实；正文明确标注安静，不用旧闻补量。

## 编辑判断

本期四条事实说明：推理加速的真实单位不是最快 kernel，而是完整请求和完整生命周期。局部计算只在它占据关键路径时才会传递到 end-to-end；cache/预热使热路径收益和首次成本分离；Agent 的成本、重试、解析和工具执行则必须在同一请求审计链上判断。两个 FlashInfer 性能结果均为公开 PR 作者报告；Claude 与 SGLang 项分别是稳定 release 与主线正确性修复，均未被包装成统一性能结论。

**KPI：Top5 新颖度均值 4.75；覆盖桶数 3；社区源条数 2；落选候选数 4；degraded：pi-subagents unavailable（两轮 scout、web-search 与 editor 均在首个模型事件前停滞；br 认证与系统 proxy 均已确认）。**
