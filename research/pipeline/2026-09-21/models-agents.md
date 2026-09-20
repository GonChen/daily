# 2026-09-21 models-agents 桶候选

版本核验基线（npm registry 实测 9/21）：`@openai/codex` latest 仍 0.155.1（0.156.0-alpha.9 于 9/20 开跑，稳定版未升）；`@anthropic-ai/claude-code` latest 2.1.278（9/19）。

## 1. Antigravity 2.15.0/2.15.1：Windows 沙箱上线 + 自定义 agent 可关默认工具 + 被杀命令审计修正
- 日期：2.15.0=9/18、2.15.1=9/19｜类型：官方发布
- 事实：2.15.1 为 Windows 引入文件与网络沙箱（此前仅其他平台）；2.15.0 允许自定义 agent 关闭默认 prompt 段与默认工具、按需加回，所选 agent reload 后保持；修复权限设置重复条目累积、应用重启时被杀命令曾记为"成功完成"（现正确报 canceled）、虚假崩溃恢复提示等。
- 影响：Windows 终端 agent 首获同等隔离边界；自定义 agent 精简工具面直接减少权限暴露；审计修正消除假阳性恢复记录。
- 来源：https://antigravity.google/changelog/
- 新事实：已报止于 2.14.0；新增 Windows 沙箱、工具开关、killed-command 审计修正。

## 2. 阿里 Qwen3.8-Omni-Flash：音频输入每小时 API 价格降超 98%、音视频联合输入降超 93%
- 日期：9/17 深夜（美西）/9/18（北京）｜类型：官方发布（媒体转述官方数字，三个独立来源交叉）
- 事实：全模态模型（文本/图像/音频/视频输入），1M 上下文；音频输入每小时 API 价格较前代降超 98%，音频+视频联合输入降超 93%，视频输入降约 89%；官方称每小时成本按"2 分钟素材单价×30"折算；另报 29 项评测平均成绩提升。
- 影响：把长音视频处理的单位任务成本压到可规模化区间；与智谱 FlashX 同周"一提价一降价"形成定价分化样本。
- 来源：https://finance.sina.com.cn/tech/roll/2026-09-19/doc-inisiwwe7633820.shtml ；https://zhuanlan.zhihu.com/p/2084655690472224326
- 新事实：全新模型+定价发布（此前未报）。

## 3. Claude Code 2.1.278（9/19，窗口内）：auto mode 服务端分类器不计费的完整边界
- 日期：9/19 03:10｜类型：官方发布
- 事实：对 Claude API/Enterprise 及 Bedrock、Vertex、Foundry 与网关接入，auto mode 默认改用服务端分类器且分类器开销不计费；`CLAUDE_CODE_AUTO_MODE_SERVER=0` 可退出（限 Bedrock/Vertex/Foundry/网关）；回退到本地计费分类器时会告警；`/status` 新增 "Auto mode server" 行可当场核验。附官方计费文档。
- 影响：高频审批分类的 token 开销从账单剔除（可测量的单位任务成本下降），且首次给出退出开关与状态可视化。
- 来源：https://github.com/anthropics/claude-code/releases ；https://code.claude.com/docs/en/auto-mode-classifier-billing
- 新事实：2.1.278 版本号已列过，但"不计费、计费回退告警、opt-out、/status 可见性"四点是 release 正文新增细节。

## 4. Codex：0.155.0 权限/恢复细节补全，0.156.0-alpha.9 已开跑
- 日期：0.155.0=9/18、0.155.1=9/19、0.156.0-alpha.9=9/20｜类型：官方发布
- 事实：已报三件事之外，release 正文补充：受支持 Mac 上 MCP 请求需 Touch ID 验证；Amazon Bedrock 支持从配置命令获取 AWS 凭证（带缓存/到期刷新/认证恢复）；切换账号即失效前一身份的 remote-control 会话、缓存 WebSocket 状态与模型目录；自动审批审查完整保留动作与授权证据并区分"审查失败"与"不安全动作"；封堵受限 WSL 沙箱的 Windows 进程逃逸。
- 影响：本地 agent 信任边界收紧；Bedrock 凭证命令化降低企业接入摩擦。
- 来源：https://github.com/openai/codex/releases ；https://registry.npmjs.org/@openai/codex/latest
- 新事实：Touch ID、Bedrock 凭证命令化、账号切换会话失效、WSL 逃逸封堵、0.156 alpha 时间戳。

## 5. DeepSeek 价目表现状核验（9/21）：vision-exp 旧名也在接管范围，"Flash 有视觉、Pro 没有"能力倒挂
- 日期：页面核验于 9/21｜类型：官方文档（一手）
- 事实：现行价目表仅 `deepseek-flash`（=V4.1-Flash，1M 上下文/最大输出 384K/支持图像理解）与 `deepseek-v4-pro`（=V4-Pro-0813，不支持图像理解）。脚注确认旧名 `deepseek-v4-flash` 与 `deepseek-v4-flash-vision-exp` 均已下线、由 V4.1-Flash 按 Flash 价承接。价格：输入缓存命中高峰 0.04 元（Flash）/0.30 元（Pro）、空闲一律半价；输出高峰 8 元/27 元；并发 Flash 2500 / Pro 500。未见 V4.1-Pro 上架。
- 影响：原 vision-exp 用户被静默切到带视觉的 Flash 且单价骤降，留在 Pro 的用户反而失去唯一带视觉的选项——视觉能力与价格档位出现"倒挂"；半价空闲窗与 5 倍并发差是可调度的成本杠杆。
- 来源：https://api-docs.deepseek.com/zh-cn/quick_start/pricing/
- 新事实：新增 vision-exp 接管范围、Flash/Pro 视觉能力倒挂、精确峰谷价差与并发额度。

## 6. 智谱文档补强：GLM Coding Plan 转积分制，非高峰（含周末全天）只扣 50% 积分
- 日期：文档核验于 9/21｜类型：官方文档
- 事实：GLM-5.3-Flash 额度增至 3 倍；新版 Coding Plan 采用积分配额制；非高峰时段（含周末全天）调用仅消耗标准积分 50%；GLM-5.3-FlashX 暂未进入套餐（只能 API 付费）。
- 影响：订阅用户把任务调度到非高峰窗口得 2 倍有效额度；FlashX 排除在套餐外意味着高速档对重订阅用户实际提价幅度高于表面 2.5×。
- 来源：https://docs.bigmodel.cn/cn/guide/models/vlm/glm-5.3-flash
- 新事实：积分制、非高峰半扣、Flash 额度 3×、FlashX 不进套餐四个配额细节。

## 安静确认
Cursor（最新 9/10 Projects，窗口内无新发布）、Kimi/月之暗面（无新动作）、DeepSeek Harness（无新版本）。
