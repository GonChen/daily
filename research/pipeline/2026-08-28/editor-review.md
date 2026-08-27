# 2026-08-28 选题审校（intel-editor 只读复核）

审校对象：`fallback-discovery.md`、`selection.md`、`deep-control.md`、`deep-fastpath.md`，以及 8/26、8/27 ledger 与 `research/tracker.md`。未修改任何现有文件，未创建日报页面。

## 总结论

**准予发稿，带两处必须更正、三处结构补齐与一处配额口径收紧。** 五条 Top 5 候选均为 8/27 合入的新 PR，相对 8/25–8/27 ledger 无主体重复，准入线逐条满足；性能口径整体已标"作者报告、无独立复现"，深挖的限制、证伪条件与推断分层合规。但 `selection.md` 未按 agent 指令产出完整结构（缺打分表、落选节、Executive readout、30 秒结论、KPI），且本期"社区/非官方源"配额口径需收紧说明。dedup.md 缺失，雷达项与 Top 5 事项均未入 tracker。

## 1 去重核对

本期无独立 `dedup.md`，`fallback-discovery.md` 声明"已按 8/26、8/27 ledger 和 tracker 去重"。逐条核验：

- #35634（DeepEPv2 ElasticBuffer）、#36541（AITER int32 KV wrap）、#36330（gfx950 MTP attention）、#4789（arch-filtered cubin manifest）、#17985（MiniMax-M3 hybrid NVFP4 KV）均未出现在 8/25、8/26、8/27 任何 ledger、selection 或 deep 文件中。
- 唯一名称重叠是"MiniMax-M3"：8/27 的 #18262 是 MSA plan reuse 的回滚（无 GPU runtime test），#17985 是 hybrid NVFP4/FP8 KV 的 staged route（有 3,600s 服务 A/B）。两者事实主体不同，不构成重复。
- #35634 的 DeepEPv2 与 8/18 ledger 提及的 vLLM #51114 "DeepEP v2 receiver CPU overhead" 是同一底层协议但不同仓库、不同事实主体（vLLM 侧 receiver CPU overhead 无数值 vs SGLang 侧 ElasticBuffer capacity/fail-fast 契约有 A/B），不构成重复。

**去重通过。** 但应补一份 `dedup.md` 写明基线（policy §7 stage 1 要求），当前以 fallback-discovery 一行声明代替，可接受但不规范。

## 2 Top 5 配额核对（policy §6）

| 配额项 | 要求 | 实际 | 判定 |
|---|---|---|---|
| 覆盖桶数 | ≥3 | selection.md 用非标准桶名（分布式/控制面、异构硬件 fast path、构建与冷启动、KV/graph 内存路径）；映射到 policy §1 标准桶后实际仅覆盖 2 桶：推理与系统（#35634/#36330/#36541/#17985）、论文与开源（#4789） | **不满足 ≥3**（见 §6） |
| 当日动态发现 | ≥3 | 5/5 来自 8/27 合入 PR 的 GitHub API 检索 | OK |
| 社区/非官方源 | ≥1 | 5/5 为官方仓库合入的维护者 PR 作者报告；无具名从业者复现、无公开事故报告、无开源讨论一手信号 | **口径需收紧**（见 §5） |
| 固定雷达触发 | ≤1 且实质变化 | 0（DeepSeek 组织、芯片/资本/模型/中文产业/论文窗口均安静） | OK |
| 准入线 | 每条满足 §6 四项之一 | 见下 | OK |

准入线逐条：#35634 命中①（H20/B200 decode -0.9%~-2.8%、prefill +2.9%~+3.2% 量化 A/B + fail-fast 契约）；#36330 命中①（decode attention -37.5%/-38.3%、服务 tok/s/gpu +2.9%/+9.6%/+3.0%、C16 TPOT +5.4% 回归）；#36541 命中①（2 GiB 临界点、accept len 1.03→3.53、TPOT 12.99→5.45ms 的量化正确性恢复）；#4789 命中①（冷 JIT 1175.7→226.4s、manifest 6862→3476）；#17985 命中①（GB300 AgentX 3600s A/B，P90 TPOT -15.31%、tok/s/GPU +7.09%）。

## 3 必须更正：性能/能力口径

**(A) #35634 — selection.md Top 5 第 1 行未提 decode 回退，易被读成纯收益。**
`deep-control.md` 明确：H20×8 decode 4,339 vs legacy 4,379（-0.9%），B200×8 decode 8,429 vs 8,675（-2.8%）；prefill +2.9%~+3.2%。`selection.md` 第 1 行只写"固定 capacity shape 使 decode graph 可捕获……fail-fast"，未点明 decode 吞吐小幅回退。建议补："decode 吞吐 -0.9%~-2.8%、prefill +2.9%~+3.2%，收益是 graph 可捕获与 fail-fast 契约，非 decode 速度提升。"

**(B) #35634 — 多节点 hybrid 不可作为对 legacy 的提升结论。**
`deep-control.md` 已正确写明"2×H20×8 hybrid 无同 fabric legacy 基线，不要把 4,610 tok/s 当作对 legacy 的提升结论"。`selection.md` 未涉及多节点数字，无夸大。但若正文沿用 4,610 tok/s，必须保留该限制句。**发稿前核对正文。**

#36330（C16 TPOT +5.4% 回归已写入 selection）、#36541（accept 坍塌已写入）、#4789（persisted tactic 不兼容已写入）、#17985（route 条件清楚、dynamic-tree 显式拒绝在 deep-fastpath 已写）在 selection 表中限制标注充分，无需改。

## 4 深挖论点与限制复核

**`deep-control.md`（#35634 + #36541）：合规。** 论点"固定 capacity 使 decode graph 可捕获 + int32 截断在 2 GiB 静默 NaN"由两条独立 SGLang PR 串联，形成"MoE 控制面契约与 speculative 路径的静默失败边界"单一论点。#36541 的 bug 链路（int32 截断→offset wrap→NaN→accept 坍塌）有 kernel 级 fp32 参照（2.0 GiB int32 NaN、int64 1.0e-4）和端到端 bisect（8,380,416/8,404,992）双重确认，可信级"高"判定合理。#35634 的 fail-fast 组合清单、`SGLANG_DEEPEP_V2_NUM_MAX_DISPATCH_TOKENS_PER_RANK` 是内存预留而非语义上限的区分、多节点无可比基线均已披露。证伪条件逐条给出。**未夸大。**

**`deep-fastpath.md`（#36330 + #4789 + #17985）：合规。** 论点"异构硬件 fast path 的准入形状/variant/route 条件被显式编码"由三条串联。#36330 的 C16 回归、#4789 的 persisted tactic 失效、#17985 的 dynamic-tree 拒绝均为作者自报限制并已写入。推断部分（C16 回归源在 attention 之外、5.2× 外推到 sm107/sm103、scratch 容量与并发解耦）已单列"来源未明文陈述，不可作为事实"。**未夸大。**

两份深挖均仅用各 PR 正文作为一手来源，所有数字标"作者报告、无独立复现"，符合 policy §5。

## 5 社区源配额口径收紧

policy §6 第四项原文为"具名从业者复现、公开事故报告、开源讨论中出现的新事实，有链接可查"。本期 5 条均为官方仓库（sgl-project/sglang、flashinfer-ai/flashinfer、NVIDIA/TensorRT-LLM）合入的维护者 PR 作者报告，属于"开源一手"而非"非官方社区信号"。

- 8/25–8/27 沿用口径将开源 PR 作者报告计入社区一手，且 8/27 的 #52914 另含作者生产报告，更贴合第四项本意。
- 本期没有任何一条带具名从业者复现、公开事故报告或非官方讨论信号。严格按第四项本意，社区/非官方源条数应记 0，配额不满足。

**判定**：按前几期沿用口径记 5（含开源 PR 作者报告）可接受，但 KPI 必须加注"口径含开源 PR 作者报告，无非官方社区信号"；严格口径下本期 Top 5 不满足 ≥1 社区/非官方源配额。建议发稿时在 selection.md 明确写出口径选择，避免读者误以为存在从业者复现或事故报告。

## 6 结构缺口（必须补齐）

`selection.md` 当前只有"Top 5"列表与"编辑口径"两节，未按 agent 指令产出完整结构。缺项：

1. **打分表**：缺三项目分（新颖度/物质性/可验证性）与准入判定列。8/26、8/27 selection 均有此表，本期应一致。
2. **落选者与理由**：当前落选理由散落在 `fallback-discovery.md` "雷达与落选"节（#53685、#54088、#54012、#4442、#17862、#17887）。应在 `selection.md` 补一节逐条一行拒绝理由。
3. **深挖题分配带来源 URL**：当前两份深挖文件已存在（deep-control.md、deep-fastpath.md），但 `selection.md` 未列出深挖题分配与涉及候选的 PR URL。建议补一节列出每题涉及的候选与 `https://github.com/.../pull/<n>`。
4. **Executive readout 论点草稿**：缺。应写一段串联 ≥3 条当日事实的单一论点。素材已有：可由"fast path 准入被编码为形状/variant/route 静态条件"（#36330+#4789+#17985）或"MoE/speculative 控制面的静默失败与 fail-fast 契约"（#35634+#36541）形成。
5. **30 秒结论要点**：缺。
6. **本期 KPI**：缺。按 policy §8 应记：Top5 新颖度均值、覆盖桶数、社区源条数、落选候选数、是否 degraded。

## 7 桶命名与覆盖桶数

`selection.md` "编辑口径"节使用"分布式/控制面""异构硬件 fast path""构建与冷启动""KV/graph 内存路径"四个非标准桶名。policy §1 标准桶为：芯片与供应链、AI 基础设施与资本、模型与 Agent、推理与系统、论文与开源、中文技术与产业。

映射后：#35634→推理与系统、#36330→推理与系统、#36541→推理与系统、#4789→论文与开源、#17985→推理与系统。**实际仅覆盖 2 个标准桶，不满足 ≥3 配额。**

补救路径：若把 #36330/#36541 的 gfx950/MI355X 与 AITER 归入"芯片与供应链"（异构硬件平台），则可凑到 3 桶，但这与 policy §1"芯片与供应链"指代 NVIDIA/AMD/HBM/国产 GPU 产品/订单/供电的语义不符。更诚实的做法是承认本期覆盖桶数不足 3，按红线"宁可 Top 5 不足 5 条"应收缩——但本期 5 条准入线均满足、且均为当日动态发现，收缩会损失信息。

**建议**：发稿时统一到标准桶名，KPI 覆盖桶数如实记 2（推理与系统、论文与开源），并在编辑口径中说明本期候选集中在推理系统侧、芯片/资本/模型/中文产业四桶安静。不强行凑桶。

## 8 tracker 核对

**缺口 1：本期 5 个 Top 5 事项均未入 tracker。** 应各补一行：
- #35634：事项"SGLang DeepEPv2 ElasticBuffer capacity/fail-fast 契约"，首次 2026-08-28，触发条件"H20/B200 之外平台独立复现、fail-fast 组合实际可跑通的证伪、多节点同 fabric legacy 基线"。
- #36541：事项"AITER int32 KV seqused_k 2 GiB wrap"，首次 2026-08-28，触发条件"<2 GiB 也出错的 case、int64 在 >2.87 GiB 仍 wrap、AITER 上游强制 int64"。
- #36330：事项"SGLang gfx950 Qwen3.5 MTP attention kernel"，首次 2026-08-28，触发条件"C16 TPOT 回归根因、非准入形状误 dispatch、MI355X 之外 gfx950 复测"。
- #4789：事项"FlashInfer trtllm-gen MoE cubin manifest arch 过滤"，首次 2026-08-28，触发条件"过滤后 manifest 与运行时 dispatch 一致性、persisted tactic 升级后失效、sm107/sm103 AOT 复测"。
- #17985：事项"TensorRT-LLM MiniMax-M3 hybrid NVFP4/FP8 KV staged route"，首次 2026-08-28，触发条件"mixed batch/decode q>8 误选、长运行 scratch 越界、GB300 之外平台复测"。

**缺口 2：落选雷达项未入 tracker。** #53685、#54088、#54012、#4442、#17862、#17887 在 fallback-discovery 声明为雷达/落选，按指令应入表。

**到期事项检查**：tracker 中"SGLang gfx950 SWA attention 下界"（2026-08-25）触发条件含"MI355X/其他模型复测、#34461 与 #34462 合并后的 served A/B"。本期 #36330 是 MI355X 上 Qwen3.5 MTP 的 served A/B，但针对 MTP attention 而非 SWA，不构成该事项的结果，不标 resolved。其余 open 事项本期无新结果。无到期需标 resolved 者。

## 30 秒结论要点（供 readout）

- 8/27 合入的五条 PR 共同显示 fast path 准入正被编码为静态可求值的形状/variant/route 条件：#36330 的 gfx950 MTP 形状门、#4789 的 module variant manifest 过滤、#17985 的 staged route graph 条件；不满足时回退或显式拒绝（#17985 拒绝 dynamic-tree）。
- #35634 与 #36541 从控制面侧补充：固定 capacity shape 使 decode graph 可捕获但 decode 吞吐 -0.9%~-2.8%；int32 KV 偏移在 2 GiB 静默 wrap 导致 speculative acceptance 坍塌，是可行动的静默失败修复。
- 所有数字为 PR 作者报告、无独立复现；#36330 的 C16 TPOT +5.4% 回归未定位根因。
- DeepSeek 官方、芯片/资本、模型/Agent、中文产业、论文五桶安静，已明确收缩，未用旧料填充。
- 严格口径下本期无非官方社区源；覆盖标准桶数 2，不满足 ≥3，建议如实记录而非凑桶。

## 本期 KPI（建议值，待补入 selection.md）

- Top5 新颖度均值：待打分表补齐后计算；从候选强度看 #35634 DeepEPv2 新后端 5、#36330 新平台 served A/B 4.5、#36541 静默 NaN 修复 5、#4789 冷 JIT 5.2× 4.5、#17985 混合精度 KV staged 4.5，均值约 4.7。
- 覆盖标准桶数：2（推理与系统、论文与开源）。**不满足 ≥3 配额。**
- 社区源条数：5（口径含开源 PR 作者报告；严格口径下 0，无非官方社区信号）。
- 落选候选数：6（#53685、#54088、#54012、#4442、#17862、#17887）。
- degraded：是（fallback-discovery 记录 scout 模型首事件停滞，主控降级执行；认证与系统 proxy 已确认正常）。
