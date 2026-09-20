# 2026-09-21 selection

窗口 2026-09-19 → 2026-09-21（每两天一期第二期）。8 桶侦察全部走 anysearch CLI 成功、无限速，非 degraded。

## Top 5（按部署影响、证据完整度与桶覆盖排序）

| # | 事实 | 桶 | 准入线 | 类型 |
|---|---|---|---|---|
| 01 | SGLang v0.5.20 正式版：SM120 torch fallback→DeepGEMM（TPOT 3.4×）、Blackwell FlashMLA→TRT-LLM 内核（decode ~1.45×）、`/v1/responses` 默认不驻留（400）、CUDA 12 轮子退役 | inference-systems | 准入 2（正式 release + 量化变化） | 官方 release |
| 02 | Ollama 跨请求提示词泄漏（Strix Halo/HIP，逐字、temperature 0 确定性复现）：三方 commit 级 A/B 指认打包构建、上游源码赦免 | community | 准入 4（具名社区一手，隐私级后果） | 社区报告 |
| 03 | CleanSpark $2.25B 首单 Meta 挂钩垃圾债（8.25–8.5%、4 倍超购、20 年三重净租）+ 弗州 EO 22（25MW 审批/禁 NDA/前期财务承诺）+ DOE 72 小时三道 202(c) 令 | infra-capital | 准入 3（市场文件/监管落地） | 官方文件/市场条款 |
| 04 | vLLM #57413：七月清理把 `--max-num-partial-prefills` 当死配置删除，V1 长上下文 TTFT 队头阻塞；两份独立生产证据 + 社区复活 PR #57427 | community | 准入 4（具名生产证据） | 社区一手 |
| 05 | vLLM 非 Hopper 数值基线重置：#49435 SM100 fp8_ds_mla cache scales、#50455 ROCm logits 塌陷、#57454 DSA NaN 语义、#57667 DSA 去运行时 JIT | deepseek-radar | 准入 1/4（结果级修复，旧精度结果作废） | 已合入主线 |

配额核对：桶覆盖 4（inference-systems、community、infra-capital、deepseek-radar）≥3 ✓；动态发现 5/5 ≥3 ✓；社区源 2 ≥1 ✓；固定雷达触发 1 ≤1 ✓。与 dedup 表核对无原样重复（华为 960/DeepSeek 路由/#57355 等均未重述）。

## 落选与降档理由

- **华为 Hi-ONE/Peerium 补充数字**（chips）：相对上期 960 报道为增量（48,000 模块、OIF 立项、Atlas 950 25.6 万卡部署中），未达"新事件"级，降入芯片分类卡。
- **Qwen3.8-Omni-Flash 定价（音频 −98%）**（models-agents）：满足准入 1，但单点产品定价；并入深挖 03 与模型分类卡。
- **vLLM #57421 Humming scratch −97.5% + 未解释精度位移**（inference-systems）：单条证据强但修复侧未闭环；升格为深挖 01 的"基线噪声"案例 + 算子行。
- **SGLang #40313 SWA/Mamba radix 删除**（inference-systems）：v0.5.20 的衍生事实，并入框架卡与算子行。
- **智谱电话会 50 亿融资/ARR 30 亿**（china-industry）：单一媒体转述电话会，未见官方通稿 → 宏观简讯，标注口径。
- **Codex 0.155 细节补全/0.156 alpha、Antigravity 2.15、Claude Code 计费边界**（models-agents）：迭代类，降入工具卡。
- **SProbe/PreDE/ODA/V4.1-Flash 技术报告**（papers-oss）：论文区主卡（FP4 KV 与上期 Pareto Atlas 负结果的张力进深挖叙述）。
- **HBM4 Micron 传闻**：无权威一手，仅传闻档提及不进正文。

## 深挖分配（3 题，编辑基于桶内一手事实成文）

1. **基线会过期：复现边界的四种失效**——Ollama（构建）、#57413（版本/死配置）、#49435+#50455（硬件数值）、#57604（并发门控）+ #57421（双基线噪声）；含对照表与证伪条件。
2. **算力承诺的条款化续章**——CleanSpark 债券条款、弗州 EO 22、DOE 202(c) 三连发，对照上期 H.R.9340/EEI/IID；从"联邦要求州考虑"到"州行政令落地"与"垃圾债定价锚"。
3. **能力与价格档位的倒挂**——DeepSeek Flash 有视觉/Pro 没有、Qwen Omni-Flash 音频 −98%、智谱 FlashX 提价且出套餐 + 50 亿融资/ARR 上调；降价与提价两端的共同前提仍是国产推理规模化。

## 主线（Executive readout 单一论点）

**基线会过期：结论只在生成它的条件下成立。**同一份源码换个打包构建就跨请求泄漏（Ollama），同个引擎删一行"死配置"就队头阻塞（vLLM #57413），同个模型换张卡数值基线就作废（#49435/#50455），同个 kernel 换个并发就反优化（#57604）；资本侧同一周把"意向"压成"条款"（CleanSpark 8.25% 定价、弗州 25MW 审批）。部署决策要绑定条件采集，而不是继承上周的结论。
