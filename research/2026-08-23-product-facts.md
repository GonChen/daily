# 2026-08-23 research ledger

## 采集与降级

先完成过去两期去重基线、八个主题角度的动态发现和固定雷达核验。`intel-scout` 的第一轮八个并发线程、第二轮四个重试线程以及一轮串行线程均未在运行窗口内给出可用结论，故依 `source-policy.md` 第 7 节降级为主控直接发现与一手来源核验；`intel-editor` 随后独立完成筛选。候选与拒绝记录见 [fallback discovery](pipeline/2026-08-23/fallback-discovery.md) 和 [selection](pipeline/2026-08-23/selection.md)。

## 入选事实

- **SGLang v0.5.18，8/22 正式发布：**checkpoint staging 可与 CUDA graph capture 重叠。官方在 Qwen3-32B/H100 上报告比 serial 启动快 8.6–11.7%，比 plain default 快 2.38×（35.6s vs 84.8s）；在 DeepSeek-V4-Pro/B200 decode 上报告 TP LMHead 320µs→169µs、TPOT 36.97ms→35.67ms；DeepSeek-V4-Flash TP4/Blackwell 小 batch pure-allreduce 最多 +6.9%。这是发布方在特定模型、硬件和配置下的测试口径，不代表通用收益。升级还迁移至 torch 2.13、统一 `SGLANG_CACHE_DIR`，并改变默认 MoE deferred finalize 行为；先预热与回归是部署前提。[官方 release](https://github.com/sgl-project/sglang/releases/tag/v0.5.18)
- **DeepSeek Harness dsh-v0.1.1-rc.1 / rc.2，8/21：**RC1 新增 `DeepSeek-V4-Flash-Vision-Exp` 适配，并修复 Bubblewrap 受限进程可经 `/proc/<pid>/root` 逃逸的问题；RC2 优先把图像上传迁移到 Files API，并复用既有上传文件。两者均是候选版，没有性能、成本或可靠性量化，也不等同 GA。[RC1](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.1-rc.1) [RC2](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.1-rc.2)
- **DeepGEMM #410，8/17 社区 RFC：**用户 `0z5a` 提出 opt-in chunk-ready symmetric-buffer protocol，目标是让 router/TopK/input-layout 的生产和早期 token chunk 的 dispatch 重叠，而不是等待完整 batch。这是公开工程讨论；没有 benchmark、实现或合入承诺，且仍需定义 progress guarantee 与安全复用条件。只作为早期跟踪信号。[GitHub issue #410](https://github.com/deepseek-ai/DeepGEMM/issues/410)

## 雷达与落选

- Claude Code v2.1.240 的说明仅为 “Bug fixes and reliability improvements”；Codex 0.150.0-alpha.7 仅有版本名。两者缺少可核验的功能、性能或可用性事实。
- FlashInfer 最近为 nightly；DeepEP、DeepGEMM 主线和 FlashMLA 没有窗口内的合格 release、合入事实或数据。均只记为公开面安静。
- 芯片、基础设施、中文产业和论文方向没有找到相对 8/20–8/21 基线足够新、且有主卡级一手证据的事实，因此未用旧闻填充正文。

## 编辑判断

本期三条信号共同提示：运行时重叠的工程边界正在从 kernel 内部延展到冷启动、TP 通信和 MoE 输入生产；但成熟度不同。SGLang 是可立即评估、但须回归的发布级变更；Harness 是必须按 RC 验证的安全与输入边界变更；DeepGEMM RFC 只值得跟踪，尚不构成部署依据。

**KPI：Top5 新颖度均值 4.33；覆盖桶数 3；社区源条数 1；落选候选数 4；degraded：pi-subagents unavailable（两轮 scout 并发与一轮串行均未在运行窗口内完成）。**
