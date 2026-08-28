# 2026-08-29 选题审校（intel-editor 只读复核）

审校对象：`dedup.md`、`fallback-discovery.md`、`selection.md`、`research/tracker.md`，对照 8/27、8/28 ledger/selection 与 `templates/source-policy.md`。未修改任何现有文件，未创建日报页面。

## 总结论

**准予发稿，带一处配额口径必须修正、两处结构补齐、一处深挖未产出需跟进、一处 tracker 描述需对账。** 五条 Top 5 候选相对 8/27、8/28 ledger 无主体重复，准入线逐条满足；本期首次出现一条真正的非官方社区源（#36807 具名公开最小复现），满足 policy §6 第四项本意；性能口径整体已标"作者报告"、限制与反例写入充分。主要问题：(1) `selection.md` 把 #36657、#54168 两条 kernel/系统级问题归入"芯片与供应链"桶，按 policy §1 语义应归"推理与系统"，修正后实际覆盖标准桶数为 2，不满足 ≥3 配额；(2) `selection.md` 缺"落选者与理由"节、深挖题分配未带来源 URL；(3) 两份深挖文件（`deep-liveness.md`、`deep-selection.md`）尚未产出，论点与证伪条件无法复核；(4) tracker 中"fast_topk_v2 4,096 candidate silent truncation"与 #36807 的"k=2048/64×256K 64/64 rows"描述需对账确认是否同一事项。

## 1 去重核对

dedup.md 基线为 8/27、8/28 ledger 与 tracker，禁重清单覆盖 8 条（SGLang #35634/#36330/#36541、FlashInfer #4789、TensorRT-LLM #17985、SGLang #36456、vLLM #52914、SGLang #35343、FlashInfer #4030/#4728）。逐条核验：

- #36094（MI355X DSV4 decode split-K heuristic）、#36657（Blackwell MegaMoE SM reserve liveness）、#53333（vLLM P/D NIXL async KV post-forward submission）、#54168（B300 TP8 Kimi-K3 low-M tail）、#36807（SGLang issue fast_topk_v2 B200 静默错行）均未出现在 8/27、8/28 任何 ledger、selection、deep 文件中（grep 确认）。
- 名称近似项：8/28 有"SGLang gfx950 Qwen3.5 MTP attention"（#36330），本期 #36094 也是 MI355X/gfx950 上的 kernel，但模型（DeepSeek-V4-Pro vs Qwen3.5）、算子（decode split-K heuristic vs MTP attention）、事实主体不同，不构成重复。8/28 有"AITER int32 KV 2 GiB wrap"（#36541），本期无 KV 地址类候选，不重复。
- dedup.md 末尾"本期优先检查"列出异步 KV load/fence、DeepSeek V4 Hopper/AMD 路径、Blackwell MoE grid barrier、dynamic-tree/speculative、agent/API security/streaming 语义。#53333 命中异步 KV load、#36657 命中 Blackwell MoE grid barrier、#36094 命中 DSV4 AMD 路径，覆盖良好。

**去重通过。** dedup.md 已独立成文（policy §7 stage 1），优于 8/28 的缺失状态。

## 2 Top 5 配额核对（policy §6）

| 配额项 | 要求 | 实际 | 判定 |
|---|---|---|---|
| 覆盖标准桶数 | ≥3 | selection.md 标 3（芯片与供应链、推理与系统、论文与开源），但 #36657、#54168 实为 kernel/系统级，应归"推理与系统"；修正后实际 2（推理与系统、论文与开源） | **不满足 ≥3**（见 §6） |
| 当日动态发现 | ≥3 | 5/5 来自 8/28 合入 PR 的 GitHub API 检索 + issue 检索；scout 两轮无首事件，主控降级一手核验 | OK（沿用 8/27、8/28 降级口径） |
| 社区/非官方源 | ≥1 | #36807 为 SGLang issue 区具名公开最小复现（B200 64/64 错行 + 最小脚本 + 低/高长度对照），属 policy §6 第四项"具名从业者复现"本意 | **OK**（本期首次真正满足；与 8/28 严格口径下为 0 形成对比） |
| 固定雷达触发 | ≤1 且实质变化 | 0（DeepSeek 组织、芯片/资本/模型/中文产业窗口安静，fallback-discovery 未报雷达命中） | OK |
| 准入线 | 每条满足 §6 四项之一 | 见 §3 | OK |

## 3 准入线逐条

- **#36094** 命中①：MI355X 5 并发点服务 A/B，C4–64 吞吐 +0.8%~+4.3%、TPOT −0.8%~−4.2%，plain TP8 全部 <1%（反例已给），38 unit cases。量化服务 A/B + 反例，影响 gfx950 部署决策。**强合格。**
- **#36657** 命中①（兼④苗头）：GB300 liveness repro，reserve=0 可重现 grid-sync timeout，reserve 2 SM 后 >23k requests 0 error。属可复现 liveness 故障修复，影响 Blackwell MoE 部署稳定性。**强合格。**
- **#53333** 命中①：两节点 P/D GSM8K C64 A/B，TPOT −4.92%、TTFT +0.07%，并明确 sync/mixed step 保持旧排序（限制）。量化服务 A/B + 边界。**强合格。**
- **#54168** 命中①但**偏弱，建议编辑确认**：证据为"B300 TP8 kernel trace + 1,319 GSM8K full model"。-25.1% 是 kernel trace（exposed critical chain）的微基准级数字，whole-tail CUDA event 近乎不变；"full-model evaluation"疑为正确性/任务完成评测，非服务吞吐 A/B。若 1,319 GSM8K 仅做正确性而不给服务吞吐/时延对比，则本条更像"kernel 诊断 + 正确性 eval"，与 8/28 被拒的 #54088（仅微基准无服务 workload）口径接近。selection 已自标可验证性 4.0（5 条中最低）并写明"不能将前者写成全服务收益"，限制到位。**建议编辑在正文/selection 显式写明 #54168 的准入依据是"low-M tail critical chain 的量化诊断 + full-model 正确性"，而非服务吞吐 A/B；若 full-model 实为吞吐 A/B 则补数字。**
- **#36807** 命中④：社区 issue 具名公开最小复现，B200 上 64×256K、k=2048 时 fast_topk_v2 64/64 rows 静默错行，含最小脚本与低/高长度对照。属"具名从业者复现、开源讨论新事实、可链接"。**合格**（silent correctness error，物质性高；可验证性 4.0 因尚无维护者确认/独立复现，合理）。

## 4 性能口径与限制复核

整体：fallback-discovery 末行"所有 PR 数字均为作者报告；#36807 为社区报告，尚未有维护者修复或独立复现"已声明；selection 30 秒结论逐条带反例/边界。逐条：

- **#36094**：30 秒结论含 plain TP8 <1% 反例，未外推为通用 AMD decode 收益。合规。
- **#36657**：给 reserve=0 故障与 reserve 2 SM 0 error 两端，未报吞吐收益数字（只说 kernel perf），不构成"变快"误读。合规。
- **#53333**：TPOT −4.92%/TTFT +0.07% + sync/mixed 保持旧排序限制。合规。
- **#54168**：exposed chain −25.1% 与 whole-tail CUDA event 近乎不变并陈，明确"不能写成全服务收益"。合规，但见 §3 准入弱提示。
- **#36807**：标"尚待维护者核验/修复"，未升格为确认 bug。合规。

**无需强制更正的口径错误。** 与 8/28（#35634 decode 回退漏写）不同，本期限制标注整体到位。

## 5 社区源配额口径

本期与 8/28 的关键差异：#36807 是 issue 区具名公开复现（非官方仓库合入 PR），含最小脚本与对照，直接命中 policy §6 第四项"具名从业者复现、公开事故报告、开源讨论中出现的新事实，有链接可查"。**社区/非官方源条数记 1，口径严格且无争议。** 无需 8/28 那样的"口径含开源 PR 作者报告"加注。其余 4 条为官方仓库合入 PR 作者报告，不计入社区源，分类正确。

## 6 桶命名与覆盖桶数（必须修正）

`selection.md` 打分表"桶"列将 #36657、#54168 标为"芯片与供应链"，KPI 据此记覆盖 3 桶。按 policy §1，"芯片与供应链"指"NVIDIA / AMD / HBM / network / 国产 GPU / ASIC + 产品、订单、供电、互连、制造或供应链变化"。#36657（Blackwell MegaMoE whole-grid barrier、SM reserve liveness）与 #54168（B300 TP8 Kimi-K3 low-M tail kernel trace）均为 kernel/系统级 liveness 与性能诊断，不涉及产品/订单/供电/互连/制造，应归"推理与系统"。8/28 editor-review §7 已对 gfx950/MI355X kernel 作同样判定，本期应沿用。

修正后桶分布：#36094 推理与系统、#36657 推理与系统、#53333 推理与系统、#54168 推理与系统、#36807 论文与开源。**实际覆盖标准桶数 = 2（推理与系统、论文与开源），不满足 ≥3 配额。**

补救判断：5 条准入线均满足、4 条为当日动态发现的服务 A/B 或 liveness 修复、1 条真社区源，信息密度高，按红线"宁可不足 5 条"收缩会损失高价值事实。**建议**：发稿时把 #36657/#54168 桶名改回"推理与系统"，KPI 覆盖桶数如实记 2，并在编辑口径说明"本期候选集中在推理系统侧，芯片/资本/模型/中文产业四桶安静，未凑桶"。不强行凑 3。

## 7 结构缺口（应补齐）

`selection.md` 当前节：Top 5 与打分 / 编辑结论 / 深挖分配 / 30 秒结论 / 配额与 KPI。较 8/28 已补打分表、30 秒结论、KPI，但仍有缺口：

1. **落选者与理由节缺失**：6 条落选理由现仅存于 `fallback-discovery.md`"雷达与落选"节（#36738、#36583、#53409/#53141、#4494/#17870、#17434、#36764）。agent 指令要求 `selection.md` 含"落选的高分候选逐条写一行拒绝理由"。应在 selection.md 补一节，逐条一行。
2. **深挖题分配未带来源 URL**：当前只写候选编号（#36657 + #53333 等）。agent 指令要求"每题给出涉及的候选与来源 URL"。应补 `https://github.com/.../pull/<n>` 或 `.../issues/<n>`。
3. **Executive readout 论点草稿**：`编辑结论`节已串联 5 条事实成单一论点（"异步与稀疏 fast path 的失败…缺少可保留的资源余量、顺序或候选集"），满足"串联 ≥3 条、单一论点非逐条罗列"。**合规**，但建议节名改为"Executive readout 论点草稿"以匹配指令结构。

## 8 深挖未产出（需跟进）

`selection.md` 深挖分配引用 `deep-liveness.md`（#36657 + #53333）与 `deep-selection.md`（#36094 + #54168 + #36807），但 `research/pipeline/2026-08-29/` 下两文件均未生成（ls 确认只有 dedup/fallback-discovery/selection）。`intel-analyst` 阶段尚未执行，论点细化、证伪条件、推断分层无法复核。

- deep-liveness 论点方向"资源可驻留与 forward/transfer order 的 liveness contract"合理：#36657 的 SM residency 与 #53333 的 forward/transfer order 同属"保留余量与顺序"主题，具备串联基础。
- deep-selection 论点方向"capture-time/low-M/radix selection 如何在未知运行时状态下失效或降级"合理：#36094 capture-time split-K、#54168 low-M SIMT 切换、#36807 fixed candidate buffer 静默错误，同属"静态选择在运行时状态未知时失效"。

**建议**：发稿前由 intel-analyst 产出两份 deep 文件；若 scout/analyst 模型仍停滞，主控降级补写，并保持"作者报告、无独立复现"标注与证伪条件单列。

## 9 tracker 核对

本期 tracker 维护明显优于 8/28：5 条 Top 5 事项已全部入表（SGLang MI355X DSV4 split-K、SGLang Blackwell MegaMoE SM reserve、vLLM async KV post-forward、vLLM Kimi-K3 low-M tail、SGLang fast_topk_v2 4,096 candidate silent truncation），2 条雷达项（#36738 HiCache fence、#36764 docker image bloat）也已入表。

**需对账（1 处）**：tracker 记"SGLang fast_topk_v2 **4,096 candidate silent truncation**"，但 selection/fallback 的 #36807 描述为"B200 上 **k=2048/64×256K** fast_topk_v2 **64/64 rows 静默错行**"。两者数字（4096 candidate vs k=2048）与现象（silent truncation vs 64/64 错行）措辞不一致。需确认：(a) 若为同一 issue，统一描述（候选数、k 值、错行率以 #36807 原文为准）；(b) 若为不同 issue，tracker 缺一条。建议编辑核对 #36807 正文后修正 tracker 该行事项名。

**落选雷达项未入 tracker（可选项）**：#36583（H200 KV pool size，fallback 自述"数字强但接近 8/28 容量主题"）、#53409/#53141、#4494/#17870、#17434 未入表。按 8/28 review 口径雷达项宜入表，但这些条目准入线未达（无服务 A/B 或无可量化部署影响），入表价值低，**建议仅 #36583 入表**（有强数字，仅因主题重叠落选，后续值得回访），其余可不入。

**到期事项检查**：逐条比对 open 事项触发条件与本期候选——
- "SGLang gfx950 SWA attention 下界"（8/25，触发含 MI355X served A/B）：#36094 是 MI355X DSV4 split-K，非 SWA attention，不构成结果，保持 open。
- "SGLang gfx950 Qwen3.5 MTP attention"（8/28）：#36094 模型/算子不同，不构成结果。
- "FlashInfer SM12x MSA chunked top-k"（8/27）、"FlashInfer CUB variable-length top-k"（8/28）：#36807 是 SGLang fast_topk_v2，不同仓库不同 kernel，不构成结果。
- 其余 open 事项本期无新结果。

**无到期需标 resolved 者，无回访条目生成。**

## 30 秒结论要点（供 readout）

- 8/28 合入的五条事实共同显示：fast path 失效的根因是"缺少可保留的资源余量、顺序或候选集"。#36657 给 Blackwell grid barrier 留 2 SM residenc，reserve=0 可重现 timeout；#53333 把 async KV 提交排到 forward 后但仅对 async-only step，sync/mixed 保持旧序；#36094 用 capture-time split-K 安全近似，plain TP8 收益 <1% 作反例。
- #54168 在 low-M tail 暴露 −25.1% critical chain，whole-tail CUDA event 近乎不变，是诊断而非全服务收益；#36807 社区复现 B200 fast_topk_v2 在 64×256K/k=2048 下 64/64 rows 静默错行，尚待维护者确认。
- 所有数字为作者报告、无独立复现；#36807 为社区报告。
- 首次出现真正非官方社区源（#36807），满足社区配额；但覆盖标准桶数修正后为 2（推理与系统、论文与开源），不满足 ≥3，建议如实记录而非凑桶。
- DeepSeek 官方、芯片/资本、模型/Agent、中文产业四桶安静，已明确收缩；scout 两轮无首事件，主控降级执行。

## 本期 KPI（建议修正值）

- Top5 新颖度均值：4.70（selection 自报，复核认同：#36094 4.5、#36657 5.0、#53333 4.5、#54168 4.5、#36807 5.0）。
- 覆盖标准桶数：**2**（推理与系统、论文与开源），修正 selection 自报的 3。**不满足 ≥3 配额。**
- 社区源条数：1（#36807，具名公开最小复现，严格口径下成立）。
- 落选候选数：6（#36738、#36583、#53409、#53141、#4494/#17870、#17434、#36764；fallback-discovery 将 #4494/#17870 与 #53409/#53141 各并一行，按条目计为 7，按"候选"计为 6，建议统一口径）。
- degraded：是（scout 两轮无首个 assistant event，`pi auth check` ready、proxy 已继承，主控降级一手核验与审校）。
