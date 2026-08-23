# 深挖二：Agent 的预算、代理与工具调用必须共享同一条请求语义链

## 两类不同的失真

| 层面 | 新事实 | 失真方式 | 正确动作 |
|---|---|---|---|
| 价格/传输 | Claude Code v2.1.239 | 数据驻留 workspace 的 1.1× premium 可能未进入成本显示；特定 Bedrock proxy 对 response `Content-Type` 的处理可触发 non-streaming 重跑 | 将价格地域、retry 原因与实际请求 ID 纳入预算/审计 |
| 解析/执行 | SGLang #34237 | Python-like tool call 可因语法/序列化缺陷静默丢失、参数被截断或被转换为无效 JSON | 对可确定的格式错误值保真恢复；对非有限值、位置参数和歧义结构 fail closed |

## 解释

`/cost` 的 1.1× premium 是预算展示的价格口径更新；Bedrock 重跑错误是特定代理路径的重复请求风险。两者都不能被缩写为“v2.1.239 降低 10% 成本”。前者使上限更接近真实计费，后者是排除一个可能翻倍的错误条件。

SGLang #34237 处理的是另一端：模型已经产生看似工具调用的输出，却因解析器遇到 `+7`、set、没有占位符的 f-string、raw newline 或嵌套引号而丢弃调用或损坏参数。该 PR 的可靠性约束是：确定性、可 AST 验证的恢复才允许通过；歧义结构和非 JSON 值必须被拒绝。这比“尽力猜测”更适合会执行工具的运行时。

二者相连的地方在于：Agent 的成本和正确性都依赖一条可审计请求链。一个逻辑任务应能关联模型请求、代理重试、计费、解析后的 tool call、实际工具执行和用户可见结果。缺任一段，预算可能低估，或执行表面成功而实际遗漏动作。

## 验收与证伪

- 成本面：按 region、provider、HTTP status、retry reason 和 request ID 比对账单，确认 premium 与重试语义；若代理缺失 header 时没有重跑或供应商账单不重复，则“翻倍风险”只保留为历史 bug 描述。
- 工具面：在真实 LFM2/LFM2.5 任务上测量 valid-call recall、parameter exact-match、ambiguous-call reject rate 和 task success；19 个 unit regression 或 42-payload diff 不能替代任务成功率。
- 安全面：fail-closed 的拒绝必须显示给调用方，而不是再次静默吞掉调用；恢复链路须记录原始输出、改写规则与最终参数。

来源：[Claude Code v2.1.239](https://github.com/anthropics/claude-code/releases/tag/v2.1.239)；[SGLang #34237](https://github.com/sgl-project/sglang/pull/34237)。
