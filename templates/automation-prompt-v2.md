# 自动任务提示词 v2（pi-subagents 增强版）

把本文全文作为 Codex 每日自动任务的 prompt。相对 v1 的变化：采集从"单 agent 六组搜索"升级为"四阶段编辑部流水线"，用 pi-subagents 并行扇出 + 对抗性选题 + 深挖；其余发布、模板、可信度规则不变。规范依据仍是 `templates/source-policy.md`（含第 6–8 节新增准入线与 KPI）。

---

每天北京时间早上 06:00 生成并发布前沿计算情报日报。继续本任务上下文。规范本地仓库位于 /home/gongchen/my_proj/daily：若自动任务环境可写，先在此安全同步 main；若权限隔离导致不可写，则从 https://github.com/GonChen/daily 克隆到新建的 /tmp 临时目录完成当次生成与推送，不修改或删除规范本地仓库，并在结果中提醒本地副本需要 pull。以 templates/daily-template.html、templates/source-policy.md 和 docs/archive/2026-08-16.html 为不可降低的内容密度、栏目结构、交叉跳转与视觉质量基线；禁止恢复已删除的低质量通用生成器，禁止用 RSS 摘要卡片覆盖模板。

采集与选题按 templates/source-policy.md 第 6–8 节执行：动态发现优先、固定雷达兜底；Top 5 有准入线与配额（≥3 桶、≥3 条动态发现、≥1 条社区/非官方渠道、≤1 条固定雷达触发）；版本 bump 与无实质影响的单 PR 不进 Top 5；Executive readout 必须是串联 ≥3 条当日事实的单一论点；每篇深度解读优先连接 ≥2 条独立事实，含 before/after 或对比表、部署/成本含义、证伪条件。

## 流水线执行步骤

### Stage 0｜准备（主 Codex）

1. 同步仓库（见上）。
2. 读最近两期 `research/<DATE>-product-facts.md`，写 `research/pipeline/<DATE>/dedup.md`：已覆盖实体与主题、每项上次出现日期、本期不得原样重复的事实清单。
3. 从 `research/angles.md` 取 6–8 个未用角度，用后移入"已用"并注明日期。

### Stage 1｜并行侦察（8 个 intel-scout 线程）

用 `~/.codex/skills/pi-subagents/pi-subagent` 构造 manifest 并启动（`--cwd` 指向仓库根，使 `.pi/agents/` 生效）：

```bash
~/.codex/skills/pi-subagents/pi-subagent start --manifest /tmp/daily-scouts.json --label daily-scout
~/.codex/skills/pi-subagents/pi-subagent wait --labels daily-scout --timeout-ms 1500000
~/.codex/skills/pi-subagents/pi-subagent list --label daily-scout
```

manifest 为 8 个任务数组，每个 `{"agent": "intel-scout", "cwd": "<repo>", "label": "daily-scout", "timeoutMs": 1200000, "prompt": "<该桶指令>"}`。桶与 prompt 要点：

1. **chips**：GPU/AI 芯片与供应链（NVIDIA、AMD、HBM、网络、昇腾、寒武纪、壁仞、沐曦、ASIC）；注入 1–2 个轮换角度。资本/宏观不再单独侦察：仅当订单、断供或财报指引直接改变芯片供给时附带至多 1 条，并标注"资本面"。
2. **trending**：当日社区热榜广度扫描，四个必查面（HN/GitHub 用 curl，Reddit/X 用 anysearch 或 twitter CLI，均已在 2026-09-19 验证可达）：① Hacker News 首页热榜 `curl -s "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30"`（JSON，含 points/评论数）；② Reddit 热帖：`reddit.com` 对无登录抓取全程人机验证（curl JSON、`r.jina.ai`、anysearch extract 均被挡），改用 `python3 /home/gongchen/.agents/skills/anysearch/scripts/anysearch_cli.py search "site:reddit.com/r/LocalLLaMA <主题词>" --max_results 8` 发现当日热帖（r/LocalLLaMA 首要，r/MachineLearning、r/OpenAI、r/ClaudeAI 按需；多查询合并进一条 `batch_search`），snippet 自带正文片段与热度线索；③ GitHub 热榜 `curl -s "https://github.com/trending?since=daily"`（HTML，直接 grep 仓库路径）+ 新星仓库 `curl -s "https://api.github.com/search/repositories?q=created:>YYYY-MM-DD&sort=stars&order=desc&per_page=15"`；④ X/Twitter 热点：装了 OpenCLI 优先 `opencli twitter search "<主题词>"`，否则 `twitter search`；404（ClientTransaction 上游故障）时改 `twitter user-posts @账号` 扫 research/watchlist-accounts.md，单条公开推文用 `r.jina.ai/<URL>` 读取。产出：与 AI/GPU/推理系统相关的热条目，每条带热度数字（HN pts、Reddit upvotes、GitHub stars、X 互动量）和一行"为什么热、是否有一手事实支撑、值不值得深挖"；与主题无关的纯宏观/创投条目直接丢弃。
3. **models-agents**：开放模型、coding agent、OpenAI/Codex、Claude Code、Cursor、pi 的产品/价格/权限变化。
4. **inference-systems**：推理框架与算法（投机解码、KV cache、PD 分离、量化 MoE、调度）。
5. **papers-oss**：arXiv 新论文、开源实现、可复现 benchmark。
6. **china-industry**：中文公司一手信号（公告、财报、开源、招聘、开发者实测）。
7. **community**：非官方渠道一手深信号，找具名从业者的复现、事故、争论：GitHub issue/PR 中的回归报告与维护者定性、HN/Reddit 讨论串里的对照实验与 A/B 数据、V2EX/知乎/B站中文讨论；X/Twitter 深扫 watchlist（vLLM/SGLang/FlashInfer/DeepSeek/TRT-LLM 维护者、GPU/infra 分析师，见 research/watchlist-accounts.md），降级链同 trending 桶：OpenCLI 优先，`twitter search` 404 时改 `twitter user-posts @账号`，单条公开推文用 `r.jina.ai/<URL>` 读取。
8. **deepseek-radar**：https://github.com/deepseek-ai 组织按 pushed_at/release/tag/PR merge/README diff 扫描（deepseek-harness、DeepSeek-V3/R1/OCR-2、FlashMLA、DeepGEMM、TileKernels、DeepSpec、DeepEP、EPLB/LPLB、DualPipe、3FS、smallpond/open-infra-index），并查其在 vLLM、SGLang、TensorRT-LLM、FlashInfer 的集成 PR；RC 逐日 bump 不算实质变化。

每个 prompt 必须包含：日期窗口（最近 24–72 小时，必要时一周）、dedup.md 路径、分配的角度、输出路径 `research/pipeline/<DATE>/<bucket>.md`。失败线程重试一次；两次失败记录原因并继续。

### Stage 2｜对抗性选题（1 个 intel-editor 线程）

```bash
~/.codex/skills/pi-subagents/pi-subagent start --agent intel-editor --cwd <repo> \
  --label daily-edit --timeout-ms 900000 --prompt "<DATE>；读 research/pipeline/<DATE>/ 全部桶文件与 dedup.md、research/tracker.md；按 source-policy 第 6 节产出 selection.md"
~/.codex/skills/pi-subagents/pi-subagent wait --labels daily-edit --timeout-ms 900000
```

读 `research/pipeline/<DATE>/selection.md`。若宣布安静窗口，按 source-policy 收缩正文。

### Stage 3｜深挖（2–3 个 intel-analyst 并行）

按 selection.md 的深挖分配，为每题启动一个 intel-analyst 线程（同样 --cwd 仓库根），产出 `research/pipeline/<DATE>/deep-NN.md`。等全部完成。

### Stage 4｜组装、质检、发布（主 Codex）

1. 复制 templates/daily-template.html 生成 `docs/archive/YYYY-MM-DD.html`：保留全部必备栏目与交叉跳转，Executive readout/30 秒结论/深度解读锚点到详情或可信来源；按第 6 节可信度约定标注每条。macro 栏目定位为"社区热榜温度 + 中文产业"：汇总当日四榜（HN/Reddit/GitHub/X）的升温话题与整体温度，资本/宏观仅在直接影响芯片供给或推理部署时保留至多 1 条。
2. 合并 pipeline 产物与页面事实写 `research/YYYY-MM-DD-product-facts.md`，末尾记录 KPI 行（Top5 新颖度均值、覆盖桶数、社区源条数、落选数、degraded 与否）与 selection.md 的落选理由摘要。
3. 更新 `docs/index.html` 指向当期；当期首页底部链接归档页；`docs/archive/index.html` 最前面加当期条目（日期、编辑摘要、主题关键词、完整链接）并更新期数；当期归档页可返回归档索引。
4. 运行 `python3 scripts/qa_check.py YYYY-MM-DD`，FAIL 必须修复后重跑至 OK。
5. 质量自评：达到 2026-08-16 模板密度后才提交推送 main；等待 GitHub Pages 部署成功。

## 降级与失败处理

- pi-subagent CLI 缺失、`pi auth` 失败或 scout 线程两轮超时：退回单 agent 流程（source-policy 第 1–5 节），ledger 标注 `degraded: <原因>`，报告说明。
- 来源不足：明确写出窗口安静并收缩正文，不得编造、不得用旧基线或通用摘要填满页面、不得降级覆盖首页。
- 发布失败：在任务报告中说明原因，不强行提交不合格页面。
- 页面仅用于技术和产业研究，不构成投资建议。
