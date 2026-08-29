# 深挖 2：Agent 工具治理与 sandbox 边界——Codex rust-v0.151.0 把隐式约定变成可测试契约

## 发生了什么

2026-08-29，OpenAI Codex 发布正式 release `rust-v0.151.0`（相对 `rust-v0.150.0`）。该 release 把 MCP 工具发现、tool result 拦截、remote sandbox 路径语义、permission profile 恢复和 nested subagent 预算从隐式约定转为显式、fail-closed 的契约。不含任何吞吐或时延 benchmark；不构成性能收益。

## 正式变化与数字（作者报告，单一来源）

| 维度 | v0.150.0 及以前 | v0.151.0 |
|---|---|---|
| optional MCP 发现 | 共享隐式等待 | `mcp_optional_startup_grace_ms`，默认 1,000 ms；0 = 关闭，退回各 server `startup_timeout_sec`（#41199） |
| MCP tool result | 直达模型 | extension 经 `on_mcp_tool_result` 在 completion 发布前检查/替换成功与错误结果（#41202） |
| plugin catalog | 单一来源 | 合并仓库级配置，报告无效 marketplace 但不隐藏合法 plugin（#41208） |
| restored permission profile | 以 legacy sandbox override 表示，`/cd` 可能弱化 | 区分保留 restored profile，`/cd` 无法安全表示时拒绝（#41192） |
| remote sandbox 路径/OS | 发起侧约定 | 用 executor 实际 home/OS/path；deny-read 按 executor 语义匹配；malformed/不兼容/unresolved/invalid glob **fail closed**（#41196 #41204 #41207 #41209） |
| nested subagent 预算 | 未计入 root | 子代含孙代 token usage 滚入 root goal 预算，idle/active 均计入，换 goal 时重置基线（#41183） |

## 与推理侧 fail-closed 契约的对照（推断）

本期推理侧三条失效（#36714 `is_cuda()` 静默禁 fast path、#36915 eager fallback 复用旧 `qo_indptr`、#37059 跨 DP collective desync）共同特征是门控/陈旧状态在真实组合下静默走错而无报错。Codex v0.151.0 的 #41196 把 cached Guardian 分类绑定到当前 authorization 状态、#41209 给非法路径 fail-closed，正是推理侧还缺的同型防御：状态变化后陈旧授权不再放行，配置不可表示时拒绝而非降级。两者同为"fail closed vs 静默走错"的分野。

## 与 dedup/tracker 的核对

dedup 本期优先项"Agent/API 的权限、恢复、流式协议或价格是否出现可部署的正式变化"成立：本 release 为权限/恢复/预算的正式 GA 变化。tracker「Agent 长驻控制面」(2026-08-20) 触发条件"权限/预算/队列/恢复机制的正式发布"部分满足：permission profile 恢复与 subagent 预算正式发布。tracker「Agent 请求语义：代理重试与工具解析」(2026-08-24) 触发条件"任务成功率/误调用率/重复请求率/实际计费回归"未满足：release 无任何量化率或计费回归。

## 仍缺的指标与证据

任务成功率、误调用率、重复请求率、实际计费回归均无数字（直接卡住「Agent 请求语义」闭合）。nested subagent 累计 token 的实际计费影响未量化。permission profile 在无 `/cd` 长会话或 crash-recover 路径下的保持未给端到端复现。全部数字为作者报告，无独立部署者复测；#41202 的 result 替换是否改变模型下游行为未给对照。单一来源。

## 证伪条件

1. restored 全限定 profile 在某 `/cd` 序列后静默退化为更弱 sandbox 模式而无 reject → 推翻 #41192。
2. optional MCP server 在超出 grace 后仍进入 tool catalog 且未标不可用 → 推翻 #41199。
3. MCP completion 在 extension `on_mcp_tool_result` 运行前发布，或替换结果未进入模型输入 → 推翻 #41202。
4. nested 孙代 token usage 逃出 root goal 预算或换 goal 后基线未重置 → 推翻 #41183 及预算闭环声明。
5. 权限状态变化后陈旧 Guardian 分类仍授权当前已拒绝的动作 → 推翻 #41196 stale-classification 防御。
6. Windows deny-read 对非 UTF-8 或 canonical 链接目标漏判而不 fail closed → 推翻 #41209。

## 可信级与来源

B+（正式 release tag + 16 个 PR 描述含测试声明；单一来源、单一 bot 作者、无独立复现、无量化回归）。未引入第三方转述数字。以下超出 release 直接陈述的为推断并单列：与推理侧 fail-closed 的对照为推断，依据是同型失效模式的类比，非 release 文本声明。

来源：
- release：https://github.com/openai/codex/releases/tag/rust-v0.151.0
- full changelog：https://github.com/openai/codex/compare/rust-v0.150.0...rust-v0.151.0
- #41192 permission profile：https://github.com/openai/codex/pull/41192
- #41196 sandbox/MCP/cached approvals：https://github.com/openai/codex/pull/41196
- #41183 subagent budget：https://github.com/openai/codex/pull/41183
- #41199 MCP grace：https://github.com/openai/codex/pull/41199
- #41202 extension tool result：https://github.com/openai/codex/pull/41202
- #41208 per-repo plugin catalog：https://github.com/openai/codex/pull/41208
- #41204 executor home：https://github.com/openai/codex/pull/41204
- #41207 executor OS：https://github.com/openai/codex/pull/41207
- #41209 deny-read path semantics：https://github.com/openai/codex/pull/41209
