# 2026-08-17 前沿计算情报日报 · 研究底稿

资料窗口：截至 2026-08-17 06:00 CST。优先 24–72 小时；周末无 arXiv 新投递、无美股新交易日，因此对高价值事项补充至近一周，并在正文中显式标注。

## 编辑主线

1. 资本：NVIDIA 把 AI factory 变成可由独立资本方承销的基础设施资产。
2. 电力：800 VDC 从长期方向进入 H2 2026 / 2027 的产品时间表。
3. 软件：vLLM 主线同日出现平台优化与正确性回退，说明有效算力取决于可靠路由。
4. 推理：NeMo Switchyard 把降本边界从单模型 kernel 扩展到跨模型路由。
5. 催化：Hot Chips 2026 将在 8/24–25 集中给出多家下一代架构材料。

## 一手来源与事实摘录

### NVIDIA compute 融资

- 官方公告（2026-08-10）：https://nvidianews.nvidia.com/news/nvidia-partners-with-apollo-blackrock-blackstone-brookfield-goldman-sachs-and-kkr-to-establish-ai-compute-infrastructure-financing-platforms-to-mobilize-over-500-billion-of-third-party-capital
- 官方解释（2026-08-11）：https://blogs.nvidia.com/blog/nvidia-ai-factory-compute/
- 事实：Apollo、BlackRock、Blackstone、Brookfield、Goldman Sachs、KKR 与 NVIDIA 签署 MOU，拟建立独立 compute financing platforms。
- 事实：目标是“over $500 billion”第三方资本，随时间动员；不是 NVIDIA 营收、不是单一基金，也不是对单一客户的承诺。
- 事实：金融机构按项目独立评估客户、需求、利用率、现金流和残值。
- 事实：部分机会中 NVIDIA 可提供最高 25% 的残值支持，逐案评估。
- 编辑判断：融资成本和残值可能成为 GPU 平台竞争变量；MOU 不等于已经建设或已承诺 CapEx。

### 800 VDC

- 官方博客（2026-08-11）：https://blogs.nvidia.com/blog/800-vdc-power-architecture-ai-factory/
- 事实：NVIDIA、Google、Microsoft 经 OCP 协作；80+ 厂商按规范开发产品。
- 事实：MGX-compatible 800 VDC power rack 计划 H2 2026 到货，可接入既有 AC 基础设施，在行内向 compute rack 提供 800 VDC。
- 事实：row power center 预计 2027 年可用，支持每排最高 2MW。
- 编辑判断：近期可行路径是分阶段改造行内供电；真实价值仍需效率、故障域、互操作和认证数据。

### vLLM 主线（均非新正式版）

- MI355X / DeepSeek-V4 sparse-MLA PR（2026-08-16 合入）：https://github.com/vllm-project/vllm/pull/52212
- 事实：专用于 gfx950/MI355X 的 Triton sparse-MLA decode 路径；40-shape kernel acceptance 通过。
- 作者 A/B：8×MI355X、TP8、concurrency 64、8k/1k、640 个计分请求、单轮每 arm；吞吐 1,155.242 → 1,187.054 tok/s（+2.754%），P99 TTFT −7.919%，P90 TTFT +4.092%。PR 自述这不是统计一致性主张。
- FA4 回退 PR（2026-08-16 合入）：https://github.com/vllm-project/vllm/pull/52050
- 事实：FA4 的 SM100 2-CTA kernel 对 head-dim 256 不支持 `seqused_q/k`，vLLM 暂时让该 shape 回退 FA2；FA4 继续用于 head-dim 128 和受支持 MLA 192/128。
- 编辑判断：吞吐数字必须连同单轮限制、尾延迟分位与 fallback 一起报告。

### SGLang 主线

- PR #34696（2026-08-16 22:05 UTC 合入）：https://github.com/sgl-project/sglang/pull/34696
- 事实：DSpark speculative decoding 支持 OpenAI-compatible logprobs；传递 accepted-token logprobs 与 top logprobs，并恢复 sanity coverage。
- 最新正式版仍为 v0.5.17（2026-08-08）：https://github.com/sgl-project/sglang/releases/tag/v0.5.17

### 框架 / 算子版本核验

- vLLM v0.27.1（2026-08-11）：https://github.com/vllm-project/vllm/releases/tag/v0.27.1
- TensorRT-LLM v1.3.0rc24（2026-08-12，预发布）：https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc24
- PyTorch v2.13.0（2026-07-08）：https://github.com/pytorch/pytorch/releases/tag/v2.13.0
- FlashAttention FA4 beta26（2026-08-12）：https://github.com/Dao-AILab/flash-attention/releases/tag/fa4-v4.0.0.beta26
- FlashInfer 0.6.18 nightly（2026-08-16）：https://github.com/flashinfer-ai/flashinfer/releases/tag/nightly-v0.6.18-20260816
  - 发布页只有“Automated nightly build for version 0.6.18”，不得推断具体功能。
- FlashInfer 稳定版 0.6.17（2026-08-11）：https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.17
- FlashMLA：官方仓库无正式 release，过去 72 小时无提交：https://github.com/deepseek-ai/FlashMLA
- cuDNN frontend v1.27.0（2026-08-06）：https://github.com/NVIDIA/cudnn-frontend/releases/tag/v1.27.0
- cuBLAS / CUDA 官方 notes：https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/ 与 https://docs.nvidia.com/cuda/cublas-patch-release-notes/contents.html

### Nemotron 3.5 Lightning / NeMo Switchyard

- 官方博客（2026-08-11）：https://blogs.nvidia.com/blog/nemotron-lightning-switchyard-rtx-dgx/
- Switchyard：https://github.com/NVIDIA-NeMo/Switchyard
- 事实：Lightning 为 30B-A3B MoE 开放模型；Switchyard 为开源 agent model-routing library。
- 公司 benchmark：最高 4× 输出速度、agentic task completion 快 30%；Switchyard 内部测试成本接近 Opus 4.8 单模型的三分之一。
- 边界：数字来自 NVIDIA / 合作方测试，不是独立通用结论，需自有 workload 复测。

### Agent 开发工具

- Claude Code v2.1.233（2026-08-14）：https://github.com/anthropics/claude-code/releases/tag/v2.1.233
  - GitLab MR worktree、Linux Bash memory cgroup、MCP v2 重连与安全修复。
- pi v0.84.2（2026-08-14）：https://github.com/earendil-works/pi/releases/tag/v0.84.2
  - configurable default tools、实验性 strict JSON-schema constrained sampling、transcript search。
- OpenAI Codex 0.148.0-alpha.20（2026-08-16）：https://github.com/openai/codex/releases/tag/rust-v0.148.0-alpha.20
  - 页面只有 release 标题；不得推断功能。稳定版仍为 0.147.0。

### Hot Chips 2026

- 官方议程：https://hotchips.org/
- 时间：tutorial 8/23，conference 8/24–25（PDT）。
- 8/24 GPU session：NVIDIA Rubin、AMD MI400 GPU 与 system architecture、Intel Crescent Island。
- 8/25：NVIDIA BlueField-4 / Spectrum-X、Microsoft Maia 200、Google 第八代 TPU、OpenAI chip talk。
- 边界：当前只使用议程题目；规格与性能必须等待 slides / 正式演讲。

### 论文与宏观沿用窗口

- 2026-08-14—16 arXiv 官方 API 查询在 cs.DC / cs.LG / cs.CL 的目标条件下返回 0 条周末新投递，因此保留 8/13 的高价值预印本并明确日期。
- OpScale：https://arxiv.org/abs/2608.13499
- DARTree：https://arxiv.org/abs/2608.13524
- Reduced Matrix Multiplication：https://arxiv.org/abs/2608.13426
- Beyond Final Scores：https://arxiv.org/abs/2608.13417
- 周末无美股新交易日，ticker 保留 8/14 close 并标注“周末无新收盘”。宏观数据仅作上周基线，不伪造周末更新。

## 去重与不采用项

- Google–AMD TPU v10 仍无三家公司正式确认：不再作为首页主 headline，仅留跟踪项。
- FlashInfer nightly 只有自动构建说明：不写不存在的 feature list。
- 公开模型 DeepSeek / GLM / Kimi / Qwen 在目标窗口没有可核验的新代际发布：模型雷达明确“无新发布”，保留部署基线。
- 不把论文作者、NVIDIA 或合作方 benchmark 改写成独立复现结论。
