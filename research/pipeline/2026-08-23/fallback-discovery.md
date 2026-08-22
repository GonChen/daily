# 2026-08-23 降级动态发现候选

`intel-scout` 的两轮并发启动和一轮串行启动均未在可操作窗口内完成，因此按 source-policy 第 7 节改由主控执行动态发现与一手核验。本文件是 editor 的候选输入，不代表全部进入正文。

## SGLang v0.5.18：启动、TP 通信与缓存迁移同时改变升级成本

- 一句话新事实：8 月 22 日正式发布的 v0.5.18 增加 checkpoint staging 与 CUDA graph capture 重叠；这不同于 8 月 21 日仅限 Kimi-K3 SM107 自动路径的未验收 PR，且给出完整发布级测试口径。
- 关键数字及其边界：官方在 Qwen3-32B/H100 上报告 overlap 比 serial 启动快 8.6–11.7%，比 plain default 快 2.38×（35.6s vs 84.8s）；在 DeepSeek-V4-Pro/B200 decode 上，TP LMHead 时间 320µs→169µs、TPOT 36.97ms→35.67ms；DeepSeek-V4-Flash TP4/Blackwell 小 batch pure-allreduce 最多 +6.9%。均为发布方特定模型、硬件与配置，不是通用收益。
- 为什么值得关注：可减少服务重启/扩容的冷启动时间，并把通信优化从单 kernel 扩到 all-to-all 与 allreduce 路径；但升级同时迁移 torch 2.13、缓存目录与默认 MoE 行为，需要先预热和回归。
- 一手来源 URL：https://github.com/sgl-project/sglang/releases/tag/v0.5.18
- 可信级：事实（官方 release，性能为官方报告）
- 新颖度：5 / 5；物质性：5 / 5；可验证性：5 / 5
- 是否满足 Top 5 准入线：是——量化性能变化与正式发布（第 1、2 项）。

## DeepSeek Harness dsh-v0.1.1-rc.1 / rc.2：多模态接入与 sandbox 修复同时进入候选版

- 一句话新事实：8 月 21 日的 rc.1 新增 `DeepSeek-V4-Flash-Vision-Exp`，修复 Bubblewrap 受限进程可经 `/proc/<pid>/root` 逃逸；同日 rc.2 将图像上传优先迁移至 Files API 并复用已上传文件。
- 关键数字及其边界：无官方性能、成本、可靠性数字；版本仍是 RC，不可等同正式 GA。
- 为什么值得关注：把图像输入、上传复用和隔离边界放在同一可部署适配器里；安全修复的影响是“应升级并验证”而不是可量化性能收益。
- 一手来源 URL：https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.1-rc.1 ，https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.1-rc.2
- 可信级：事实（官方 release candidate）
- 新颖度：4 / 5；物质性：3 / 5；可验证性：5 / 5
- 是否满足 Top 5 准入线：是（谨慎）——新模型可用性和安全修复；必须明确 RC 边界（第 2 项）。

## DeepGEMM #410：社区提出将 MegaMoE 输入改为可分块流式交接

- 一句话新事实：8 月 17 日，GitHub 用户 `0z5a` 在 DeepGEMM 提出 opt-in chunk-ready symmetric-buffer RFC；目标是让 router/TopK/input-layout 生产者与更早 token chunk 的 dispatch 重叠，而不是等待整批输入就绪。
- 关键数字及其边界：没有 benchmark、实现或合入承诺；该设计需要就 progress guarantee 与安全复用达成一致。
- 为什么值得关注：它把 MoE 重叠的边界从 mega-kernel 内部扩展到上游输入生产，若被实现，才可能影响 token 流水线；目前只能作为社区早期信号。
- 一手来源 URL：https://github.com/deepseek-ai/DeepGEMM/issues/410
- 可信级：社区一手信号 / 推断
- 新颖度：4 / 5；物质性：2 / 5；可验证性：3 / 5
- 是否满足 Top 5 准入线：是（谨慎）——具名公开工程讨论中的新事实，但不作性能结论（第 4 项）。

## 固定雷达与落选信息

- Claude Code v2.1.240（8/22）release body 仅写“Bug fixes and reliability improvements”，没有可核验功能或数字；落选。
- Codex 0.150.0-alpha.7（8/22）release body 仅含版本名；落选。
- FlashInfer 近三次均为 nightly；落选。
- DeepEP 最近可见功能提交为 8/4；DeepGEMM 最近主线 release commit 为 7/15；FlashMLA 最近主线 commit 为 7/28；不作为当日主内容。
- 芯片、基础设施、中文产业及论文/开源的动态搜索未找到相对于 dedup 基线足够新且可核验的主卡事实；本期应明确公开面安静，不以旧基线补量。
