# 2026-08-24 降级动态发现候选

`intel-scout` 八桶两轮均在首个响应窗口内无工具活动或候选文件；`web-search` 兜底线程同样无首个模型事件。因此主控按 source policy 第 7 节以公开 GitHub API、release 与 merged PR 作直接发现和核验。本文件是编辑筛选输入，不代表全部进入正文。

## A. FlashInfer #4593：SM100/SM103 block-sparse attention 的公开端到端基准

- 新事实：8 月 23 日合入的 PR 为 SM100/SM103 增加优化的 block-sparse VSA attention，并在 canonical 与 FastWan 场景公开同步计时。
- 数据与边界：作者在 16 个 canonical 行的 kernel/API 测量报 1.902192× 几何均速（最小 1.029429×）；FastWan 两组全生成 ABBA/BAAB 含 61 帧 materialization 的端到端总计仅 1.015714×。环境、硬件、baseline 与输入形状均在 PR 中；这不是通用模型吞吐结果，也不是独立复现。
- 为什么值得关注：局部 attention 核心的倍数收益，在真实视频生成端到端路径收缩为约 1.6%，说明优化项目必须同时呈现 kernel 与完整工作流的数字。
- 来源：https://github.com/flashinfer-ai/flashinfer/pull/4593
- 可信级：合入的开源 PR；性能为作者报告。
- 评分：新颖度 5 / 物质性 5 / 可验证性 4；准入：第 1 项量化性能变化；桶：芯片/硬件路径。

## B. FlashInfer #4686：B300/SM103 W4A16 dense GEMM 用更大的 autotune 空间换取小而稳定的单核收益

- 新事实：8 月 23 日合入的 PR 将 SM100/SM103 W4A16 dense GEMM 由显式 O2 改为 O3，并把 raster direction 扩至 30 个策略。
- 数据与边界：一张 B300/SM103 GPU、两种投影、16 个形状的 A/B/A CUPTI 计时报告 1.029759× 几何均速，范围 0.996866–1.060623×；15/16 改善。但冷启动 autotuning profile time 由 196.68s 升至 417.83s（2.12×），且没有端到端模型吞吐测试、没有 B200/SM100 的最终测量、全库测试未跑。
- 为什么值得关注：它把“低精度 kernel 更快”改写为部署权衡：持久化 cache 命中时有小收益，首次形状发现却要付更高的调优成本。
- 来源：https://github.com/flashinfer-ai/flashinfer/pull/4686
- 可信级：合入的开源 PR；性能为作者报告。
- 评分：新颖度 5 / 物质性 4 / 可验证性 4；准入：第 1 项量化性能变化；桶：推理内核。

## C. SGLang #34237：LFM2 工具调用解析器从“静默丢调用”转为按调用恢复或拒绝

- 新事实：8 月 23 日合入的修复针对真实 LFM2/LFM2.5 SWE-agent 与 shell-command traces 中的 Python-like tool output，恢复此前因一元正号、set、无变量 f-string、raw newline、leading-zero int、嵌套引号等而丢失的调用；非有限数值、位置参数或歧义嵌套则显式跳过/拒绝。
- 数据与边界：PR 给出 19 个新 regression cases、Lfm2Detector 40 项与 PythonicDetector 17 项通过；42-payload differential harness 与 vLLM 同类 parser 结果一致。它没有端到端 agent task success-rate、时延或成本数据，且 recovery 只在 `ast.parse` 失败后执行。
- 为什么值得关注：可靠性改进的关键不是“多猜一次”，而是将 silent drop 改成值保真恢复或 fail closed；真实生产收益仍需用任务级成功率与误调用率证明。
- 来源：https://github.com/sgl-project/sglang/pull/34237
- 可信级：合入的开源 PR，包含真实 trace 与测试；不是正式 release。
- 评分：新颖度 5 / 物质性 4 / 可验证性 4；准入：第 4 项具名公开工程事实；桶：模型与 Agent。

## D. Claude Code v2.1.239：成本显示、代理可靠性与会话控制面出现可核验修复

- 新事实：8 月 21 日稳定版将数据驻留 workspace 的 1.1× US-only-inference premium 纳入 `/cost`、状态行和 `--max-budget-usd`；并修复了 Bedrock 代理丢失 response `Content-Type` 时重跑 non-streaming、可能让 API 调用静默翻倍的路径，以及 SSO profile 下 `HTTPS_PROXY` 未被 credential pre-check 尊重导致启动挂起的问题。
- 数据与边界：1.1×是显示/预算口径的已知溢价；“doubled billed API calls”是该错误路径的风险描述，并非所有请求的实测降本。完整 release 还包含插件同步命名、Musl add-on、远程会话等更新。
- 为什么值得关注：Agent 成本控制依赖真实计费、代理与重试语义。只显示预算而不修复重复请求，无法构成可靠的成本上限。
- 来源：https://github.com/anthropics/claude-code/releases/tag/v2.1.239
- 可信级：官方稳定 release。
- 评分：新颖度 4 / 物质性 4 / 可验证性 5；准入：第 1、2 项；桶：模型与 Agent。

## E. SGLang #35405：SM107 MXFP8 activation producer/consumer 合约修复

- 新事实：8 月 23 日合入的 PR 让没有 route/quant handoff 的 SM107 GPT-OSS 使用 FlashInfer MXFP8 quantizer，而不是可能产生不兼容激活布局的 Triton 路径；并修正 `torch.compile` fake custom-op 的 scale buffer shape。
- 数据与边界：4 个 focused regression tests 在 SM107 real weights 上通过，未提供 speed benchmark；保留 Kimi K3 fused handoff、其他 SM10x Triton 路径与 padded hidden 维度行为。
- 来源：https://github.com/sgl-project/sglang/pull/35405
- 判断：进入框架雷达，不进 Top。它是重要正确性修复，但缺 release、任务级或性能量化，且 SM107 MXFP4 自动路径已在 8/21 期覆盖，需避免同一主题重复。

## F. vLLM #53460 / #52209：合入但不作为主内容

- #53460：8/23 修正 Dots3 NOTE Omni KV cache layout 并优化 vision/audio encoder，附 8×H100 端到端通过；没有吞吐、时延或用户 API 变化。来源：https://github.com/vllm-project/vllm/pull/53460
- #52209：8/23 为 gpt-oss RL engine 支持逐专家加载，附 e2e test 图片但无可提取指标。来源：https://github.com/vllm-project/vllm/pull/52209
- 判断：两者是积极的主线进展，但当前公开事实不足以越过本期 Top 准入线，放入雷达。

## 固定雷达与安静面

- SGLang 最新正式 release 仍为 8/22 的 v0.5.18；不重复昨日的启动/TP 通信数据。
- vLLM 最新 release 仍为 8/11 的 v0.27.1；FlashInfer v0.6.17 为 8/11；TensorRT-LLM 最新 RC 为 8/12；均无本窗口正式 release。
- DeepSeek 官方组织最新实质 release 仍为 8/21 harness RC.2，DeepEP/DeepGEMM/FlashMLA 未出现窗口内合格变化；不重复昨日 RC/RFC。
- Codex alpha.7 和 Claude Code v2.1.241 均只有笼统版本/bug-fix 说明；不进主内容。
- 芯片、基础设施、中文产业及新论文未发现相对去重基线有主卡级一手事实；正文应明确安静。
