# 2026-08-24 去重基线

比较窗口：2026-08-21、2026-08-23 两期 ledger。下列事实没有新的、一手且可核验的变化时，只能写入雷达状态或跟踪清单，不得原样进入本期 Top 内容。

| 实体/主题 | 上次出现 | 已覆盖事实 | 本期不得原样重复的内容 |
|---|---:|---|---|
| SGLang | 2026-08-23 | v0.5.18 的 checkpoint staging、TP LMHead all-to-all、MNNVL allreduce，及 torch/cache/MoE 升级边界 | 35.6s vs 84.8s、320µs→169µs、+6.9% 原样改写 |
| DeepSeek Harness | 2026-08-23 | dsh v0.1.1-rc.1/rc.2 的 Vision-Exp、Bubblewrap `/proc/<pid>/root` 修复、Files API 图像复用 | RC 内容本身，除非有 GA、CVE、兼容性或独立复现的新事实 |
| DeepGEMM #410 | 2026-08-23 | chunk-ready symmetric-buffer RFC，无实现、无 benchmark | 将 RFC 写成已提速或再次作为主卡 |
| vLLM / FlashInfer | 2026-08-21 | #52989 token 上界透传；端到端重跑待定 | 8,192 / 16,384 上界故事，除非新的 benchmark/release |
| SGLang SM107 MXFP4 | 2026-08-21 | #35554 自动选择扩展，资格验证未完成 | 未验证路径作为性能结果 |
| Agent 工具 | 2026-08-21 / 23 | Codex 0.149.0 控制面；Claude Code 2.1.238；8/22 版本 bump 无事实 | 仅版本号或笼统 bug fix |
| 芯片/基础设施 | 2026-08-20 / 23 | Ohio 项目融资、供电与市场基线；8/23 无主卡 | 旧融资/价格叙事，除非新文件/合同/投运 |
| 论文与开源 | 2026-08-21 / 23 | ATFlash 作者报告；8/23 无新合格论文 | 旧预印本或单作者数字填充 |

本期重点：优先寻找新 release、模型/API、合入并带数据的系统变化、监管/合同文件或具名社区复现。没有新增证据时，明确写“公开面安静”。
