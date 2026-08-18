# 每日采集与选题策略

目标不是“把固定地址更新一遍”，而是每天重新发现值得解释的新变化；固定雷达只负责验证覆盖是否有盲区。

## 1. 每日先做动态发现

在读取固定 watchlist 前，围绕过去 24–72 小时重新发起至少 **6 组** 搜索，其中至少 4 组必须来自下面不同的主题桶：

| 主题桶 | 搜索方向示例 | 目标 |
|---|---|---|
| 芯片与供应链 | NVIDIA / AMD / HBM / network / 国产 GPU / ASIC + date | 产品、订单、供电、互连、制造或供应链变化 |
| AI 基础设施与资本 | AI data center / cloud / financing / energy / SEC / earnings | 合同、CapEx、融资、并网、财报与风险转移 |
| 模型与 Agent | open weights / coding agent / OpenAI / Claude Code / Cursor / pi | 模型、产品、协议、价格、权限与执行能力变化 |
| 推理与系统 | inference / speculative decoding / KV cache / MoE / MLA / quantization | 可部署的系统、算法与性能变化 |
| 论文与开源 | arXiv / GitHub + inference kernel / systems / evaluation | 新论文、实现、复现与工程化落地 |
| 中文技术与产业 | 中文公司名 + 发布/公告/财报/开源/招聘/开发者 | 昇腾、寒武纪、壁仞、沐曦及国内模型公司的高价值一手信号 |

搜索必须同时使用中文与英文关键词；每天轮换实体、技术路线和反向问题（例如“谁在解决 KV 搬运”而非只搜索某个框架名）。候选进入正文前必须被一手来源、监管文件、官方仓库或可信媒体交叉核验。

## 2. 主内容的配额与去重

- Top 5 至少 **3 条** 来自当日动态发现；最多 2 条可由固定雷达触发，且必须存在实质变化（release、commit/PR 合入、模型卡、合同、财报、产品公告或可复现 benchmark）。
- Executive readout 与至少 2 篇深度解读必须建立在当天新发现上；不能仅改写昨日的同一事实。
- 同一主体/事件在连续两期中若没有新增一手事实，只能出现在“公开面安静 / 值得跟踪”一行，不得再次进入 Top 5。
- 固定源的 nightly、版本号递增、浏览量/星标、一般性 roadmap 都不构成主内容；除非随附可验证的功能、正确性、性能或商业影响。
- 每条候选先写一行“与过去两期相比的新事实是什么”；写不出来就降级或删除。

## 3. 固定雷达：覆盖而不是选题发动机

每期仍检查 SGLang、vLLM、TensorRT-LLM、PyTorch；FlashAttention、FlashInfer、FlashMLA、cuDNN、cuBLAS；DeepSeek、GLM、Kimi、Qwen；Codex、Claude Code、pi、Cursor。其用途是：

1. 发现实质 release/提交；
2. 核验动态搜索得到的线索；
3. 明确写出重要方向的“无新一手动态”。

不要把每个项目都写成卡片。只有有新增事实的项目进入分类正文；其余合并成一句雷达状态。

## 4. DeepSeek 官方 GitHub 雷达

DeepSeek 的每日主入口是 [deepseek-ai GitHub organization](https://github.com/deepseek-ai)，按 `pushed_at`、release、tag、PR merge 和 issue/公告活动扫描。至少覆盖以下分层：

| 分层 | 优先仓库/对象 | 每日要问的问题 |
|---|---|---|
| 模型与评测 | `DeepSeek-V3`、`DeepSeek-R1`、`DeepSeek-OCR-2`、`deepseek-harness` | 是否有权重、模型卡、评测配方、工具调用或 harness 变化？ |
| 推理内核 | `FlashMLA`、`DeepGEMM`、`TileKernels`、`DeepSpec` | shape、精度、kernel、投机解码或 fallback 是否有真实变化？ |
| 分布式与 MoE | `DeepEP`、`EPLB`、`LPLB`、`DualPipe` | 通信、负载均衡、expert parallel、重叠执行是否改变？ |
| 数据与存储 | `3FS`、`smallpond`、`open-infra-index` | 训练/推理数据面、存储或可复现基础设施是否变化？ |

执行方式：每日查询组织仓库的最近 push/release，再只打开有变化的仓库的 commits、release notes、PR 或 README diff；必要时检查其在 vLLM、SGLang、TensorRT-LLM、FlashInfer 中的集成 PR。官方透明度中心和 API changelog 仅在新模型/API 代际时补充，不作为日常雷达的主卡。

## 5. 写作门槛

- 每条都说明：发生了什么、可核验事实/数字、为什么影响部署或产业判断、来源和边界。
- 版本控制提交和论文数字分别标成“主线提交”“作者报告”；不把它们包装为正式发布或独立复现。
- 如果动态搜索没有找到足够的高价值事实，明确写出窗口安静并减少正文，不用旧基线填满页面。
