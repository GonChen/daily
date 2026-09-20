# 2026-09-21 research ledger

## 采集、去重与流水线

按 2026-09-19 → 2026-09-21 窗口采集（每两天一期第二期）。八桶并行侦察由 ZCode 子代理（Explore × 8，分批 3+3+2，全程遵守 AGENTS.md 并发上限）完成，**全部使用 anysearch CLI，未动用内置 WebSearch/WebFetch 兜底，未触发限速**。选题见 [selection](pipeline/2026-09-21/selection.md)；深挖底稿 [deep-01](pipeline/2026-09-21/deep-01.md)、[deep-02](pipeline/2026-09-21/deep-02.md)、[deep-03](pipeline/2026-09-21/deep-03.md)。

与 dedup 表核对：昇腾 960 超节点、H.R. 9340/EEI/IID、vLLM #57355、DeepSeek V4-Pro 路由主事件、DeepJIT、SGLang #40105/#40148、Cactus 主事件、#57680 均未原样重述；SGLang #39087 与 vLLM #57680 复核仍无新复现，维持待复现状态。角度池 8 个新角度（含 trending 热榜角度）已用并注明 2026-09-21。

## 入选事实（Top 5）

- **SGLang v0.5.20，9/18 发布｜官方 release：**713 个 PR 季度版。SM120（RTX PRO 6000）DSV4-Flash 从 torch fallback 换 DeepGEMM paged-MQA sparse-MLA indexer + FP4 MoE backend（#29927）：4 卡 decode TPOT 36.1→10.5 ms（约 3.4×）、TTFT 8K→128K 下降 20%。Blackwell：TRT-LLM attention 内核覆盖 DSV4 CSA/HCA 层，B200 prefill ~1.2×、decode ~1.45× 快于 FlashMLA（#30805）；FlashInfer MegaMoE 接入 NVFP4 prefill +11.9%（#31470）。默认翻转：`/v1/responses` 不再默认驻留（未开 `--enable-response-store` 一律 400、PD 禁止开启，#39122）；prefill CP v1 删除；CUDA 12 轮子退役（v0.5.19 最后一版）。统一 radix 树 SWA 分支点缓存：DSV4-Flash 共享系统提示命中率 43.8%→60.8%、mean TTFT 1.57→1.07 s；ROCm 分阶段暂存拷贝使 4×MI355X GLM-5.2 加载 505.7→40.4 s。[release notes](https://github.com/sgl-project/sglang/releases/tag/v0.5.20)
- **Ollama 跨请求提示词泄漏，9/18–9/20 收敛｜社区一手：**Strix Halo（gfx1151）HIP 后端 fused Gated DeltaNet 把上一请求循环状态带入复用 slot，前一用户文档逐字进入下一请求补全（temperature 0 确定性复现，隐私级）。三方对照矩阵（源码 commit × ROCm runtime × 量化，具名 jgoellermaximus/huppiflupp/pwilkin）：官方 llama.cpp 干净、Ollama 0.34.1 打包版泄漏——嫌疑收敛到 Ollama 自有 ggml-hip 构建/fused-op resolver；lemonade 的 llamacpp-rocm 亦报告类似问题。[llama.cpp #29092](https://github.com/ggml-org/llama.cpp/issues/29092)、[ollama #18528](https://github.com/ollama/ollama/issues/18528)
- **CleanSpark $2.25B 首单 Meta 挂钩垃圾债 + 弗州 EO 22 + DOE 三道 202(c)，9/17–9/18｜官方文件/市场条款：**CSDC Finance I LLC 5 年期高级担保票据 ~$2.25B、最终定价 ~8.25%（初步 ~8.5%）、约 100 亿美元订单 4 倍超购，资金建设佐治亚 175 MW 园区、整租 Meta 子公司 Anviran 20 年三重净租（合同总额 $6.6B）。弗州州长 9/18 签署 EO 22：禁州项目 NDA（即时）、>25MW 地方审批/前期财务承诺/PJM 成本归因数据中心（2027 立法）。DOE 9/17–9/18 对 PJM/CenterPoint/Duke 连发三道 FPA 202(c) 紧急令，Culley 2 号机授权至 12/18。[Bloomberg](https://www.bloomberg.com/news/articles/2026-09-17/meta-tied-data-center-taps-us-junk-bonds-for-the-first-time)、[弗州州长办公室](https://www.governor.virginia.gov/newsroom/news-releases/2026/september-releases/name-1123696-en.html)、[DOE 202(c)](https://www.energy.gov/ceser/2026-doe-202c-orders)
- **vLLM #57413：删除"死配置"致长上下文队头阻塞，9/17–9/19｜社区生产证据：**七月 V0 清理 #49244 把 `--max-num-partial-prefills` 当死代码删除，V1 调度器无并发 partial prefill 上限：GLM 系 MoE、TP4×4×B200、中位 100k–180k token 长提示下短请求被 7–12 调度步长 prefill 阻塞（TTFT 尾延迟）；第二位操作者同构证据（GLM-5.3-Flash on 4×B200，KV 占用低/GPU 利用率高）；社区把 #55256 rebase 为 [PR #57427](https://github.com/vllm-project/vllm/pull/57427) 并对拉生产流量验证，未合入。[issue #57413](https://github.com/vllm-project/vllm/issues/57413)
- **vLLM 非 Hopper 数值基线重置，9/18–9/20 合入｜主线提交：**#49435 修复 SM100（B200）fp8_ds_mla KV cache scales 错误；#50455 修复 gfx950/gfx942 DSv4 sparse-indexer logits 整体塌陷；#57454 显式 DSA TopK 的 NaN 候选块语义（保留 NaN 分数索引）；#57667 将 DSA offset candidate end buffers 从运行时 JIT 改预编译（DeepJIT 路线后的下游脱钩）；SGLang #40353 把 V4 mHC 上下文按模型隔离（此前泄漏进非 V4 模型 compiled MoE）。修复前非 Hopper 平台与非 V4 模型的精度结果不可作对照。[PR 列表](https://github.com/vllm-project/vllm/pull/49435)

## 分类雷达与落选

- vLLM #57604（MegaMoE staging ≥64 token 门控：<64 token 回归 2.400→2.752µs、8192 token 5.4×）；#57421（Humming scratch −97.5%/省 9.8 GiB，双基线噪声 669 vs 690/1319、作者自认精度原因未明）；SGLang #40313（SWA/Mamba 独立 radix cache 删除）。
- 华为 Hi-ONE（7.2 TB/s、48,000 光模块削减、66%/90%、OIF 12.8T 立项）与 Peerium/Atlas 950 SuperCluster 25.6 万卡部署中——960 叙事增量。
- 定价与倒挂：DeepSeek 价目表（Flash 有视觉/Pro 没有、vision-exp 接管、并发 2500/500）；Qwen3.8-Omni-Flash（音频 −98%/AV −93%）；智谱积分制与非高峰半扣、FlashX 出套餐。
- 论文：SProbe（INT32 SDC、ABFT 盲区、重算>修复、INT8 +30% 吞吐代价）、PreDE（位宽不解释任务损失、无跨策略共享阈值）、ODA（vLLM 条件执行稀疏注意力）、V4.1-Flash 技术报告（FP4 KV 890 B/token，与上期 Pareto Atlas FP8-KV 负结果构成栈特定张力）。
- 工具：Antigravity 2.15.x（Windows 沙箱、被杀命令审计修正）；Codex 0.155 细节（Touch ID/Bedrock 凭证/账号切换失效）+ 0.156.0-alpha.9（9/20）；Claude Code 2.1.278 计费边界（服务端分类器不计费、回退告警、/status 可见）；DeepSeek Harness 开发者预览。
- 简讯：智谱电话会（9 月融资 50 亿美元、ARR 指引 24→30 亿、当前 18 亿，单一媒体转述未获官方通稿证实）；沐曦剩余限售股近九成锁至 2028 且盈利挂钩；DeepSeek V4.1 Pro 截至 9/21 未上线；HBM4 Micron 传闻不采信（无权威一手）。

## 编辑判断

本期主线是**基线会过期**：同一份源码换个打包构建就跨请求泄漏（Ollama），同一个引擎删一行"死配置"就队头阻塞（#57413），同一个模型换张卡数值基线就作废（#49435/#50455），同一个 kernel 换个并发就反优化（#57604）；SGLang v0.5.20 则从发布侧一次性翻转多个默认。资本侧同一周把意向压成条款（CleanSpark 定价锚、弗州 25MW 审批、DOE 202(c) 常态化）。部署决策的条件采集清单应包含：二进制来源、版本 diff（含被删除项）、硬件+修复版本、并发位置。

**KPI：Top5 新颖度均值 4.4；覆盖桶数 4（inference-systems、community、infra-capital、deepseek-radar；models-agents/china-industry 并入分类与深挖）；社区/非官方一手 2（Ollama 泄漏链、#57413 生产证据）；落选候选 8 组；degraded：否（8 桶 anysearch 全成功）。**
