# 2026-10-03 deep-03：Agent 从会话制到常驻制

问题：一周内四家厂商同时改写 agent 的"运行时长与无人值守"语义；护栏的归属从产品层移到运维层。

| 厂商 | 常驻/无人值守能力 | 护栏语义变化 | 迁移代价 |
|---|---|---|---|
| OpenAI（DevDay 9/29） | "Dots" 常驻自主 Agent 覆盖全付费档 | 安全侧首次"暂扣旗舰模型 3 天后放行"（Astra 9/28→10/1），发布节奏引入安全门 | always-on 任务的审计与预算护栏需自建；新 Pro 档改变成本封顶 |
| Anthropic（Claude Code 2.1.288，10/2） | 交互会话（终端/桌面/IDE）不再有时限；时限只作用于无人值守会话 | 无人值守失败长流 3 次超时封顶（此前重试数小时）；API 中途超时不再废掉整回合、从部分响应续跑；auto mode 超长自动压缩 | 交互侧要自建 budget/超时外层；重试封顶降低僵尸重试烧钱 |
| OpenAI（Codex 0.160.0，10/1） | daemon 恢复扩展后，Guardian 评审可回捞更早用户指令与 agent 交接上下文 | 审计向：历史指令喂给评审通道；权限按工作区还原 | 合规团队需评审 Guardian 回捞范围 |
| DeepSeek（Harness v0.2.0-rc.2，9/29） | headless NDJSON、SSH 远端工作区、浏览器/Computer Use 后端 | 官方适配器强制迁移 Messages API（破坏 Chat Completions 接入）；默认模型列表移除 V4 Flash 系 | 五个 pre-release 未到 GA；第三方接入需改造 |

部署/成本含义：
1. **会话制的"一次任务一次计费"心智失效**：常驻 agent 的成本是速率问题——预算护栏（额度、超时、重试上限）必须外置到编排层，Claude Code 把重试封顶内建正是承认这一点。
2. **审计面扩大**：常驻 + Guardian 回捞 + Computer Use 后端意味着 agent 的可回放历史变长、权限面变宽；企业接入前先定"回捞范围"与"浏览器后端白名单"。
3. **安全门成为发布变量**：Astra 暂扣 3 天表明旗舰模型的发布时间可被安全事件移动——依赖最新旗舰的 pipeline 要有"模型不可用日"的降级预案。
4. 证伪条件：若 Dots 在非 Pro 档出现配额/时长硬限制的公开文档，"全付费档常驻"叙事收窄；若 Harness 0.2.0 GA 后恢复 Chat Completions 兼容层，迁移代价下调。

来源：bucket 文件 models-agents.md、deepseek-radar.md 所列链接。
