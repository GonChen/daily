# 2026-08-23 去重基线

比较窗口：2026-08-20、2026-08-21 两期 ledger。以下事实若没有新的、一手且可核验的变化，只能写入雷达状态或跟踪清单，不得再次进入 Top 5。

| 实体/主题 | 上次出现 | 已覆盖事实 | 本期不得原样重复的内容 |
|---|---:|---|---|
| NVIDIA / OpenAI / SB Energy Ohio | 2026-08-20 | PORTS-Pike 初始约 4.25 IT-GW 租约的累计最多 $105B residual-value guarantee；2028 起分阶段触发 | 将担保上限写成当前投资、收入或现金支出；无新 SEC/合同/投运条件时重写该事件 |
| DeepSeek Harness | 2026-08-20 | RC.8 的图像请求、Codex/Claude profile、并发搜索、Windows PowerShell 与 SQLite 不兼容 | 仅凭 RC.8 版本号或既有功能进入正文 |
| Cursor cloud agents | 2026-08-20 | PR/Slack/计划任务订阅、长驻目标、隔离 cloud subagent | 无新价格、权限、可用性或事故证据时重复 |
| Claude Code | 2026-08-21 | 2.1.238 释放长会话 stale subagent 结果、runner/proxy 控制、跨会话队列状态；此前 2.1.236 的通知与 sandbox | 普通版本递增、无实质 release note |
| Codex | 2026-08-21 | 0.149.0 的 agents dashboard、队列、cwd、doctor、权限配置保留 | 无新正式功能、价格或可靠性证据 |
| vLLM / FlashInfer MoE | 2026-08-21 | #52989 将真实 token 上界传给 CUTLASS expert 路径；focused tests pass，端到端性能待重跑 | 将 PR 合入写成性能提升；无量化结果重复 |
| SGLang / Kimi-K3 / NPU | 2026-08-21 | #35554 的 SM107 packed-MXFP4 自动路径，仍待数值/内存/性能资格验证；此前 NPU speculative 接口 | 无验收数据时声称可部署或更快 |
| ATFlash | 2026-08-21 | 作者在 Qwen2.5-7B-1M 场景报告 1.31× whole-request speedup | 把作者报告写成独立复现或上游发布 |
| DeepSeek 官方雷达 | 2026-08-21 | DeepEP 元数据 push 与可见 commit 不一致；没有合格 release/tag/merged fact | 单纯 pushed_at、RC 日更或一般 activity |

## 本期去重检查

- 只有能写出“相较以上事实的新一手变化”的候选才可进入选题池。
- 连续窗口未出现实质新事实的固定雷达项目，合并写为“公开面安静”。
- Top 5 仍须满足 source-policy 第 6 节：至少三桶、至少三条动态发现、至少一条社区一手信号、固定雷达触发不超过一条。
