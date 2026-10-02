# 2026-10-03 models-agents 桶候选

## 1. OpenAI DevDay 2026（9/29）："Dots" 常驻自主 Agent 全付费档上线；GPT-6-Astra 安全暂扣 3 天后放行
- 日期：9/29 DevDay；9/28 暂扣报道；10/1 Astra 发布｜类型：官方发布
- 事实：20+ 项公告：①"Dots"——官方常驻（always-on）自主 Agent，覆盖全部付费档；②新 Pro 档上线；③GPT-6.1 Sol 宣布降价；④Astra 剧情：9/28 报道 OpenAI"因安全事件放弃发布最新 Astra 模型"，Altman 在 DevDay 亲自解释暂扣决定，10/1 官方社区正式发布 GPT-6-Astra。另 CFO 披露 Q3 环比增长 70%、企业业务自 7 月翻倍、新一轮融资早期洽谈。
- 影响：Agent 形态从"会话制"转向"常驻制"，运维要为 always-on 任务准备审计与预算护栏；模型代际向 5.6/6-Astra 收敛，与 10/14 GPT-5.5 退役、10/23 API 大限叠加成迁移窗口。
- 来源：https://openai.com/index/devday-2026-recap/ ；https://www.cnbc.com/2026/09/29/openai-devday-2026-live-updates.html ；https://community.openai.com/t/devday-2026-announcements-and-developer-resources/1402006
- 新事实：断档 12 天内最大事件——Dots、新 Pro 档、Sol 降价、Astra"暂扣→放行"全程均为未报内容。

## 2. Anthropic 一周双发：Opus 5.5（9/22）→ Sonnet 5.5（9/28）
- 类型：官方发布｜事实：Sonnet 5.5 比 Sonnet 5 快 30%+、多数工作成本至多省 30%、价格维持不变；AWS/GCP/Azure 全平台同步；Artificial Analysis 智能指数 56。注意：Claude Code auto-mode 分类器不允许 pin 到 5.5 系列，会回落 Sonnet 5（2.1.288 changelog），计费分类用量与主模型需分开核算。
- 影响：Sonnet 档"加量不加价+提速 30%"直接下移日常 Agent 成本封顶。
- 来源：https://www.anthropic.com/claude-sonnet-5-5 ；https://artificialanalysis.ai/articles/claude-sonnet-5-5
- 新事实：两个 5.5 模型及其定价/平台可用性均为新事实（此前只报过 Claude Code 2.1.278）。

## 3. Claude Code 2.1.280→2.1.288（9/22–10/2，10 天 9 版）：无人值守长跑边界重划
- 类型：官方发布｜事实：2.1.288（10/2）：后台命令时限只作用于无人值守会话（-p/Agent SDK/CI/cloud），终端/桌面/VS Code 会话不再有时限；无人值守会话对失败长流改为 3 次超时封顶（此前会重试数小时）；API 中途超时不再废掉整个回合，非交互会话与 subagent 从部分响应续跑；auto mode 对话超长自动压缩；--resume 系列修复。2.1.287（10/1）新增 Claude Mods 与旁观侧 agent。
- 影响：交互会话无限时后要自建 budget/超时外层控制；重试封顶降低"僵尸重试"烧钱；续跑修复减少长任务 token 浪费。
- 来源：https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
- 新事实：280→288 的"时限范围收缩 + 3 次重试封顶 + 部分响应续跑"是运行边界实质变化。

## 4. Codex CLI 稳定版 0.160.0（10/1），alpha 线 36 小时冲到 0.162.0-alpha.7
- 类型：官方发布（npm + GitHub 双核验）｜事实：稳定版从 0.155.1 四连跳至 0.160.0；alpha 0.162.0-alpha.7（10/2）。亮点：agent command center "Show more" 翻旧任务；Guardian 评审可回捞更早的用户指令与 agent 交接上下文（审计向）；非项目目录按工作区默认开会话、resume 还原已存权限；Windows 沙箱 PowerShell 回退与长路径修复。
- 影响：Guardian 历史回捞涉及把历史指令喂给评审通道，合规团队需过目。
- 来源：https://github.com/openai/codex/releases/tag/rust-v0.160.0 ；https://registry.npmjs.org/@openai/codex
- 新事实：稳定线与 alpha 线均推进 4-6 个版本。

## 5. 计划事件落锤与更正：9/24 关停的是 Sora 2/Videos API；gpt-5-codex API 实际 7/23 已关停；10/23 大限映射到 5.6 系
- 类型：官方弃用页全量实抓｜事实：①官方弃用页：`gpt-5-codex` API 关停日为 2026-07-23（与 gpt-5.1/5.2-codex 一批，替代 `gpt-5.6-sol`）——**更正**：9/19 期所报"9/24 关停 GPT-5-Codex"实为 Codex 产品侧公告口径，API 侧 9/24 按公告关停的是 Sora 2 全系快照 + Videos API；②9/28 gpt-3.5-turbo-instruct 等已关停；③10/1 gpt-5.4-cyber 已移除；④10/23 大限：gpt-4o(05-13)、gpt-4 全系、gpt-4.1-nano、o1/o1-pro/o3-mini/o4-mini → 统一映射 `gpt-5.6-sol/terra/luna`（pro 走 reasoning.mode: pro），可付费专属容量延命。
- 影响：10/23 前完成老快照迁移（改模型名 + 回归测试）。
- 来源：https://developers.openai.com/api/docs/deprecations
- 新事实：更正 9/24 口径；首次给出完整 5.6 系替代映射表。

## 计划事件核查清单（截至 10/3）
- GPT-5.5 10/14 退役（消费计划，不含 API）：确有其事、未到期；迁移目标 gpt-5.6-sol（价格不变）。
- DeepSeek：V4.1-Pro 仍未上线（10/3 实抓价格表：flash 高峰输入 2 元/输出 8 元、空闲半价；v4-pro 高峰 9/27 元）；**注意张力**：价格表已不再附"路由 Flash 计费"说明，而 9/10 公告仍在线——实际计费以账单为准。
- Anthropic：9/30 通知 Sonnet 4.5 用户即将从 API 退役（日期未见）。
- GLM/Kimi/Qwen/Mistral/Antigravity/pi：无窗口内新旗舰；Cursor 9/23 上线两款 bots（Rollouts 部署监控）；Mistral 平台 9/28 弃用 GLM 5.2（10/31 退役，GLM 5.3 接替）。
- 传闻（不采信）：Reddit 称 gpt-5.1/5.4-nano/5.3-codex 将于 2027-04-01 关停，官方页无对应公告。
