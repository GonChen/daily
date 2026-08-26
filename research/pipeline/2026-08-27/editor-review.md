# 2026-08-27 选题审校（intel-editor 只读复核）

审校对象：`dedup.md`、`fallback-discovery.md`、`selection.md`、`deep-control-plane.md`、`deep-fast-path.md`，以及最近两期（08-25、08-26）ledger 与 `research/tracker.md`。未修改任何现有文件。

## 总结论

**准予发稿，带三处必须更正与两处结构补齐。** 去重、Top 5 配额、准入线、深挖论点强度与限制标注均合规；性能口径整体已标"作者报告、无独立复现"，但 `selection.md` 的 Top 5 表有两处措辞会被误读为能力/性能提升，且 `selection.md` 未按 agent 指令产出完整结构（缺打分表、落选节、Executive readout、30 秒结论、KPI）。radar 项 #30859、#18092 声明为雷达但未入 tracker。

## 1 去重核对

dedup 禁用清单为 08-25/08-26 两期事实：#36219、#49636、#51292、#4502、#35505、AgentX、SWA 下界、persistent matmul、SVDQuant LoRA、live-adapter LoRA、speculative sampling admission。本期 Top 5（#36456、#52914、#35343、#4030、#4728）与雷达（#30859、#18092）均不在清单内，无混同。dedup.md 对 #30859"不与上期 return_lse 或共享专家事实混同"的边界声明正确。**去重通过。**

## 2 Top 5 配额核对（policy §6）

| 配额项 | 要求 | 实际 | 判定 |
|---|---|---|---|
| 覆盖桶数 | ≥3 | correctness/chips、runtime/agents、inference-systems/community、acceleration/chips、kernels/papers-oss | OK（≥3，但桶命名含斜杠合并、非标准桶名，见 §6） |
| 当日动态发现 | ≥3 | 5/5 来自 08-26 GitHub API 合入 PR（fallback 组 1–4） | OK |
| 社区/非官方源 | ≥1 | 5/5 为开源 PR 作者具名报告；#52914 另含作者生产报告 | OK（口径沿用前两期，见 §5 注） |
| 固定雷达触发 | ≤1 且实质变化 | 0（DeepSeek 组 5、NVIDIA blog 均无窗口内新动态） | OK |
| 准入线 | 每条满足 §6 四项之一 | 见下 | OK |

准入线逐条：#36456 命中①（量化正确性变化：sanitizer 66→0、coredump 3→0）与④；#52914 命中①（device-idle 契约修复，wall 3.40s 事故）与④（生产报告）；#35343 命中①（tactic 分歧 20/20→0/20 的量化稳定性变化）与④；#4030 命中①（ratio 0.73–0.98→1.20–1.36、decode 1.4–2.2×）；#4728 命中①（29-shape 几何均值 2.568×–2.725× vs FlashKDA）。

## 3 必须更正：性能/能力口径

以下三处在 `selection.md` Top 5 表中措辞可能被误读，发稿前应改。更正文本身写在表内对应行。

**(A) #36456 — "GPQA 0.0→0.6313" 必须注明 0.0 的成因。**
`fallback-discovery.md` 与 `deep-fast-path.md` 已正确说明：0.0 是修复前 CI 在 H100 内存 shim 下 coredump 无法完成评测的结果，不是模型基线能力。`selection.md` Top 5 表第 1 行只写"从 66 sanitizer errors、3 coredumps 到 0，且性能中性"，未提 GPQA 数字；但 dedup.md 与 deep 均出现该数字。若正文沿用，须写作"修复前因 coredump 无法完成 GPQA 评测（记 0.0），修复后 0.6313"，不得表述为"GPQA 从 0 提升至 0.63"式的能力跃迁。吞吐 −0.05%~+0.64% 已正确标为噪声。

**(B) #4030 — 基线同 PR 作者、batch128 端到端无移动 须在 Top 5 表显式呈现。**
`deep-fast-path.md` 给出完整限制：比值基线为 vLLM 同一 PR 作者的 kernel，不是整服务吞吐；batch128 端到端 ratio 1.00–1.03 即吞吐持平。`selection.md` 第 4 行只写"提供 GPU/shape/cache/基线，且披露 batch128 无显著端到端移动"，未点明"基线=同 PR 作者 vLLM kernel"。建议补一行限制："基线为同 PR 作者 vLLM kernel，非整服务吞吐；batch128 端到端 ratio 1.00–1.03。"

**(C) #4728 — GPU time 非 end-to-end 须在 Top 5 表显式呈现。**
`deep-fast-path.md` 指出 29-shape 数字为 public API GPU time（CUPTI cold-L2），不是 end-to-end inference；相对 frozen #4605 仅 1.018×–1.045×，说明对已用 Cake 的用户增量有限。`selection.md` 第 5 行写"29-shape、四 GPU、同进程 frozen baseline；必须保留 eager/state/CUDA Graph 的 admission 条件"，未提"GPU time 非 e2e"。建议补："数字为 CUPTI GPU time 非 end-to-end；vs frozen #4605 仅 1.018×–1.045×。"

#35343（吞吐降格为稳定性收益、cold autotune 79→106s 代价）与 #52914（不缩短 burst，#52957 才降至 0.17s）在 selection 表中已正确标注限制，无需改。

## 4 深挖论点与限制复核

**`deep-control-plane.md`：合规。** 论点"完成信号先做集合操作再置位"由 #52914、#35343、#18092 三条当日事实串联，形成单一机制论点而非逐条罗列。可信级分层正确（控制面语义高可信、性能/事故数字中可信），#52914 的 3.40s 与 dummy batch 放大约 110ms 的人为放大已披露，#35343 作者自述"no regression rather than speedup"已引用。证伪条件逐条给出。**未夸大。**

**`deep-fast-path.md`：合规。** 论点"准入条件静态可求值、回退共享正确性口径、CUDA Graph 显式边界"由 #36456、#4030、#4728、#30859 四条串联。推断部分（"维护者社区隐式工程约定"）已单列并标注"来源未明文陈述，不可作为事实引用"。每条限制与证伪条件完整。**未夸大。**

两份深挖使用雷达项（#18092、#30859）作为综合证据，与 08-26 用 #17955 作深挖证据的做法一致，允许。

## 5 结构缺口（必须补齐）

`selection.md` 当前只有"Top 5"表与"深挖任务"两节，未按 agent 指令产出完整结构。缺项：

1. **打分表**：缺三项目分（新颖度/物质性/可验证性）与准入判定列。08-25、08-26 ledger 均有此表，本期应一致。
2. **落选者与理由**：当前落选理由散落在 `fallback-discovery.md` "拒绝和安静桶"节（#36233、#53942、#18262、#18140、#53838 等）。应在 `selection.md` 补一节逐条一行拒绝理由。
3. **深挖题分配带来源 URL**：当前深挖题只列题面与涉及 PR 编号，未附 PR URL（policy §5 要求每条说明来源）。建议每题列出涉及的候选与 `https://github.com/.../pull/<n>`。
4. **Executive readout 论点草稿**：缺。应写一段串联 ≥3 条当日事实的单一论点。素材已有：可由"控制面完成语义升级为集合屏障"（#52914+#35343+#18092）或"fast path 准入静态化"（#36456+#4030+#4728）任一形成。
5. **30 秒结论要点**：缺。
6. **本期 KPI**：缺。按 policy §8 应记：Top5 新颖度均值、覆盖桶数、社区源条数、落选候选数、是否 degraded。

社区源条数口径注：policy §6 第四项原文为"具名从业者复现、公开事故报告、开源讨论中出现的新事实"。开源 PR 作者报告计入社区一手信号是 08-25/08-26 沿用口径，本期保持一致可接受；但严格说这些是官方仓库合入的维护者 PR，更接近"开源一手"而非"非官方社区"——#52914 的作者生产报告更贴合第四项本意。建议 KPI 行社区源条数记 5，并加注"口径含开源 PR 作者报告"。

## 6 tracker 核对

本期 5 个 Top 5 事项已入 tracker 表（"Hopper MXFP4 MoE scale OOB guard"等 6 条 2026-08-27 行），触发条件具体，OK。

缺口：**#30859（长序列 FP8 KV 指针 int64 扩展）与 #18092（host-tier KV 初始化 world-rank 共识）在 `fallback-discovery.md` 声明为雷达，但未入 tracker。** 按指令"雷达/跟踪清单"应入表。建议各补一行：
- #30859：事项"FP8 k-cache token_id int64 扩展溢出阈值"，首次 2026-08-27，触发条件"<4.2M tokens 处独立回绕复现、DSA/DSV4 之外同型 kernel 覆盖、服务 A/B"。
- #18092：已在深挖用作证据，但作为雷达项本身也应入表，触发条件"用户工作负载/性能数字、attention-DP 子组共识复测"。

到期事项检查：tracker 表中 08-20/08-21 早期条目（Ohio 融资、DeepSeek Harness、DeepGEMM #410 RFC 等）本期无新结果（fallback 组 5 确认 DeepSeek 仓库无新动态），无到期需标 resolved 者，可接受。

## 7 桶命名（次要）

Top 5 表桶列出现 "correctness / chips"、"inference systems / community"、"acceleration / chips"、"kernels / papers-oss" 等斜杠合并桶名。policy §1 的标准桶为芯片与供应链、AI 基础设施与资本、模型与 Agent、推理与系统、论文与开源、中文技术与产业。建议统一到标准桶名（多数应归"推理与系统"或"论文与开源"），避免一条候选同时挂两桶造成覆盖桶数虚高。不影响配额合规（即使去重后仍 ≥3）。

## 30 秒结论要点（供 readout）

- 08-26 合入的三条控制面 PR（vLLM #52914、SGLang #35343、TRT-LLM #18092）共同把"完成"从 CPU 谓词升级为集合屏障，是本期最强论点；性能数字中可信，语义结论高可信。
- 两条 FlashInfer PR（#4030、#4728）与 SGLang #36456 共同显示 fast path 准入正被编码为静态可求值的形状/语义条件；但 #4030 基线同作者、#4728 非 end-to-end，讴歌前须看端到端。
- DeepSeek 官方、NVIDIA blog、中文产业、芯片资本四桶安静，已明确收缩，未用旧料填充。

## 本期 KPI（建议值，待补入 selection.md）

- Top5 新颖度均值：待打分表补齐后计算；从候选强度看预计 ≥4（#36456 正确性修复+5、#52914 契约修复+4、#35343 稳定性+4、#4030 +4、#4728 +4，均值约 4.2）。
- 覆盖桶数：≥3（按标准桶去重后约 3–4）。
- 社区源条数：5（口径含开源 PR 作者报告；#52914 含生产报告）。
- 落选候选数：≥5（#36233、#53942、#18262、#18140、#53838，及安静桶各主题）。
- degraded：是（fallback-discovery 记录 scout 模型首事件停滞，主控降级执行，非认证或代理问题）。
