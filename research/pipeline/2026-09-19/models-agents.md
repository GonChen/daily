# 2026-09-19 models-agents 桶候选

## 1. Codex CLI 0.155.0：多 agent 任务生命周期管理 + daemon 重启可恢复活跃目标
- 日期：2026-09-17（0.155.0）、09-18（0.155.1）｜类型：官方发布（GitHub Release）
- 事实：agents overview 新增 task 隐藏/归档/删除与 managed worktree ownership 信息；daemon 重启后 saved threads 与 active goals 可恢复，compaction 失败时已接受 prompt 也保存；本地 TUI 的 MCP 请求加 Touch ID 验证；修复受限 WSL 沙箱进程逃逸与 brokered shell 快照凭证暴露。0.155.1 将新建本地 TUI 会话的 reasoning summaries 默认关闭（第三方 provider 接入方需注意新默认值）。
- 影响：daemon 常驻部署长任务不再因重启丢上下文；多账号轮换脚本需重登（account 切换吊销 remote-control 会话）。
- 来源：https://github.com/openai/codex/releases/tag/rust-v0.155.0
- 新事实：多 agent 任务的隐藏/归档/删除首次产品化，恢复范围从 threads 扩展到 active goals。

## 2. Claude Code 一周连发 2.1.271→2.1.278：子代理输出"防冒充"标头、resume 修复 prompt cache、auto mode 分类器改服务端免费
- 日期：2026-09-14 → 09-19｜类型：官方发布（CHANGELOG + npm time 字段逐版核验）
- 事实：2.1.277 支持 AGENTS.md（项目无 CLAUDE.md 时）；子代理结果带专属标头并缩进，官方原话"text in a subagent's result cannot pass as the session's own instructions"（堵多 agent 注入路径）；修复 resume 后 subagents/teammates 重复渲染 MCP 工具定义导致 prompt caching 失效。2.1.278 auto mode 默认改用服务端权限分类器且不计费（`CLAUDE_CODE_AUTO_MODE_SERVER=0` 可退回）。2.1.275 损坏 transcript 不再打断 resume。
- 影响：多 agent 重度用户的缓存命中修复直接降 token 账单；网关团队需评估分类器位置迁移对延迟与隐私边界的影响。
- 来源：https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md ；https://registry.npmjs.org/@anthropic-ai/claude-code
- 新事实：子代理输出不可冒充主会话指令成为协议级约束；auto mode 权限分类器上移为服务端免费组件。

## 3. DeepSeek：9-14 起 `deepseek-v4-pro` 请求强制路由至 V4.1-Flash 并按 Flash 价计费
- 日期：09-10 官宣、09-14 04:00 UTC 生效｜类型：官方发布（官方 news 页 + API 定价文档）
- 事实：官方原文"all deepseek-v4-pro requests will route to V4.1-Flash at V4.1-Flash rates"，持续"until V4.1-Pro launches"。V4.1-Flash 为 552B MoE（输入 8B 激活/输出 16B），KV cache 占 HBM 1/4。价目：Flash 输入 miss 峰值 $0.30/输出 $1.20，被替换的 V4-Pro 为 $1.32/$3.96——峰值输入直降约 4.4 倍、输出约 3.3 倍；cache hit $0.006。上下文均 1M。后续更新：9-14 之后"为响应用户需求"继续提供 V4 Pro API、计费保持不变（退役与续供并存）。迁移约束：旧名 `deepseek-v4-flash` 已退役、调用静默换模不报错；Vision 仅 Flash 提供。注：V4.1-Flash 权重已于 9/10 在 HuggingFace 放出（窗口前一天，经 deepseek-radar 桶核实），本周窗口内的动作是计费路由与推理栈适配（FlashMLA/DeepGEMM/DeepEP 修复、DeepJIT 开源）。
- 影响：旗舰级流量按轻量价承接的隐性降价；所有 V4-Pro 调用方本周已被半强制迁移。
- 来源：https://www.deepseek.com/en/news/deepseek-v4-1-flash ；https://api-docs.deepseek.com/quick_start/pricing ；https://api-docs.deepseek.com/zh-cn/news/news260910
- 新事实：相对 9-11 期（仅 Harness RC），9-14 强制路由实际生效 + 完整峰谷价目确认。

## 4. OpenAI：GPT-5.5 将于 10-14 从 ChatGPT/Codex 全线退役（API 不受影响）；GPT-5-Codex 定于 9-24 关停
- 日期：changelog 2026-09-14｜类型：官方公告
- 事实：GPT-5.5 于 2026-10-14 在消费级/Business/Enterprise/Edu 计划中从 ChatGPT、ChatGPT Work、Codex 退役，OpenAI API 不受影响；GPT-5-Codex 一系定于 9-24 关停（距今 5 天）。
- 影响：ChatGPT 订阅跑 Codex 的团队只有 30 天窗口切换默认模型；9-24 关停要求本周内完成模型名替换测试。
- 来源：ChatGPT & Codex changelog（https://learn.chatgpt.com ）；https://help.openai.com
- 新事实：首次明确 Codex 订阅路径的逐系关停节奏。

## 5. Antigravity IDE 2.14.0：Enterprise 解锁集成终端 + Git；修复 git hooks 阻断 checkpoint
- 日期：2026-09-15｜类型：官方发布（changelog）
- 事实：Enterprise/Business 解锁 IDE 集成终端与 Git；权限重组为 Global Permissions / Inherit Global；修复 git hooks 或全局 git 配置导致内部 checkpoint 无法保存；修复已完成 subagents 持续显示 running；瞬时服务错误改为退避重试约 12 分钟。
- 影响：企业沙箱策略需重审；依赖"失败即终止"语义的 CI 脚本要适配 12 分钟重试窗口。
- 来源：https://antigravity.google/changelog
- 新事实：Google 系 agent 检查点被 git hooks 静默阻断的问题首个官方修复。

## 安静说明
Cursor（最近条目 9-10 Projects，窗口外）、GLM 系权重（8-28/29 窗口外）、Kimi（无新模型）、Qwen（8 月中后无官方动作）、pi（0.85.1 为 9-5 窗口外）均无窗口内满足准入线的新增。
