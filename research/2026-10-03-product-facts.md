# 2026-10-03 research ledger

## 采集、去重与流水线

按 2026-09-21 → 2026-10-03 十二天窗口采集（09-23 至 10-01 排程未触发，本期补跑；重点最近 72 小时，空档期候选均注明日期）。八桶并行侦察由 ZCode 子代理分批（3+3+2）完成，除 china-industry 桶 1 次摩尔线程聆讯核查回退 1 次内置 WebSearch（结果为无新增）外全部走 anysearch，无限速，非 degraded。选题见 [selection](pipeline/2026-10-03/selection.md)；深挖底稿 [deep-01](pipeline/2026-10-03/deep-01.md)、[deep-02](pipeline/2026-10-03/deep-02.md)、[deep-03](pipeline/2026-10-03/deep-03.md)。

与 dedup 表核对：SGLang v0.5.20、Ollama 泄漏、CleanSpark 债券主事件、#57413、非 Hopper 数值修复、昇腾 960 主体、H.R. 9340、#57355 均未原样重述。上期遗留跟踪项复核：Ollama 根因（Ollama 侧仍无确认）、#57427 合入状态（无窗口内更新）、SGLang #39087 与 vLLM #57680（仍无新复现）、CleanSpark 债券二级（无可核验异动）、参议院（静默）。

## 口径更正

- **GPT-5-Codex"9/24 关停"**（9/19 期口径）：官方弃用页核实 `gpt-5-codex` API 实际关停日为 2026-07-23；9/24 按公告关停的是 Sora 2 全系快照 + Videos API。9/19 期引用的是 ChatGPT/Codex 产品侧 changelog 口径，与 API 弃用页不一致，以 API 弃用页为准。
- **智谱 9 月 50 亿美元融资**（9/21 期标注"单一媒体转述、待官方确认"）：实为 **9/13 港交所公告**（配售价 714 港元 + 零息 CB 转股价 892.50 港元），早于电话会报道；9/21 期的"待确认"状态升级为"已有官方公告"。

## 入选事实（Top 5）

- **FlashMLA 2026.09.30 + 同日昇腾使能批次，9/30｜官方 release：**移除 Hopper 与 V3/V3.2/V4.0 支持、更改 FP8/FP4 KV cache 格式（与旧版互不兼容，旧平台钉 `ba89a34`）；同发布昇腾 950 稀疏注意力算子（作者报告：prefill 410 TFLOPS/95% 峰值、decode 360 TFLOPS/83% 峰值）。同日 TileKernels（同一 Python API 运行时自动选 NVIDIA/昇腾后端，昇腾要求 950 NPU + CANN 9.2.0+、NVIDIA 要求 SM90/SM100 + CUDA 13.1+）与 DeepSelect（昇腾 TopK 内核）同批上线，org 页十个仓库同日更新。[FlashMLA](https://github.com/deepseek-ai/FlashMLA)、[TileKernels](https://github.com/deepseek-ai/TileKernels)、[DeepSelect](https://github.com/deepseek-ai/DeepSelect)
- **OpenAI DevDay，9/29（Astra 10/1 放行）｜官方发布：**"Dots" 常驻自主 Agent 覆盖全部付费档；新 Pro 档；GPT-6.1 Sol 降价；GPT-6-Astra 因安全事件暂扣 3 天后正式发布。CFO 披露 Q3 环比增长 70%、企业业务自 7 月翻倍。[DevDay recap](https://openai.com/index/devday-2026-recap/)
- **SGLang v0.5.21（10/2）+ vLLM v0.30.0（9/22）｜官方 release：**SGLang：PD 实例运行中免重启切换 prefill/decode 角色（#28403）；prefix cache 默认 Rust 内核 + 统一 radix tree 全模型默认（双默认翻转，Breaking）；V4.1 长上下文首 token 快 22%（#40352）；Kimi K3 PD prefill +20.6%；ROCm GLM-5.2 decode TPOT 23→8 ms（8×MI355X）；AMD Lean attention 默认开启（可关）。vLLM：`--return-sampling-mask` 修复约 2× RL step-time 回归（#54901）；SM100/103 NVFP4 W4A16 默认后端 Marlin→FlashInfer CuTeDSL（#53014）；V4.1-Flash 头条新模型 + SM100 整份 KV MXFP8 + V4 CPU 后端（AVX512/AMX）；破坏性：GPTQ g_idx 删除、YaRN 不再重缩放 max_model_len、scale-out 显式开关。[v0.5.21](https://github.com/sgl-project/sglang/releases/tag/v0.5.21)、[v0.30.0](https://github.com/vllm-project/vllm/releases/tag/v0.30.0)
- **neocloud 债务定价三档 + 管线与透明度，9/25–10/2｜官方文件/市场条款：**Lambda $1bn 投资级 DDTL 固定 6.78%（J.P. Morgan）；Sharon AI $365m GPU-SPV 固定 9.95%（Jarden，68,000 GPU 计划首笔，offtake TCV 超 $8.8bn）——与 CleanSpark Meta 债 8.25% 构成"担保品类型"三点定价标尺。Crusoe Jayton $4.8bn 递件（TDLR TABS2027002494/2499，2027/1 开工、2029 投运），Project Hyper 两地合计约 $12bn。Raskin 9/29 侦调信（指控 Amazon 空壳公司隐藏项目角色）后 3 天，AWS 10/2 宣布弃用数据中心 NDA + 自付公用设施升级保居民电价 + $1bn 社区投入；DOE 9/25 第四道 202(c) 令把 Craig 1 号机延至 12/25（首次列入 SPP）。[DCD](https://www.datacenterdynamics.com/en/news/sharon-ai-and-lambda-secure-gpu-backed-debt-funding/)、[Raskin 信](https://democrats-judiciary.house.gov/sites/evo-subsites/democrats-judiciary.house.gov/files/evo-media-document/2026-09-29-raskin-to-jassy-amazon-re-data-center-ndas.pdf)、[DOE 202(c)](https://www.energy.gov/ceser/2026-doe-202c-orders)
- **社区失效模式三连，9/28–10/2｜社区一手：**①vLLM #59305：FlashMLA 上游 V4.1 同步（commit c112cc1）静默回滚 `num_sm_parts>1` OOM 守卫，经 pin bump 被动引入；H200 实测 T=32768 瞬时分配 8,208 MiB、与公式 `(b+num_sm_parts)*s_q*h_q*d_v*4` 吻合，恢复守卫后 2052→0 MiB 且输出 bit-identical；②vLLM #59104：DSpark `sample_from_anchor=false` 下 lookahead 少留 1 槽位，drafter 越界写可覆写其他请求 KV（H200 稳定复现 + 仪器化确认，修复 PR #59105，无维护者回应）；③llama.cpp #29774：CPU FA 小批次路径 F16 累加器静默 -inf/NaN（`-fa off` 对照正常），直接 F32 修复付 17% decode 代价、offset 方案打平 master。[#59305](https://github.com/vllm-project/vllm/issues/59305)、[#59104](https://github.com/vllm-project/vllm/issues/59104)、[#29774](https://github.com/ggml-org/llama.cpp/issues/29774)

## 分类雷达与落选

- Supermicro Rubin NVL72 出货（9/23：72 GPU + 36 CPU、20.7 TB HBM4/架、SU=1,152 GPU/331 TB）——芯片分类头条。
- vLLM-Ascend v0.27.1rc1（9/24：950DT 兼容矩阵 W4A8C8/两节点 1P1D、明示排除 A2；MiniMax-M3 上游实证）+ 壁仞 1.74 亿元招标中标（9/23：评分 89.71、45 天供货、H1 营收 12.36 亿元 +1997.6%）——并入深挖 01 与中文产业卡。
- TRT-LLM rc28/rc29（9/23、9/29：11 条 Known Issues 含 PD serving 跨请求内容错乱；rc29 修 Qwen3.5 回归、移除 AutoDeploy）→ 算子行。
- FlashInfer v0.7.0（9/22：FP8 grouped GEMM M≤32 正确性警告、无单独禁用开关；Autotuner v2 启动 410.7→165.3 s）→ 算子行。
- Anthropic Opus 5.5/Sonnet 5.5 双发（9/22、9/28：快 30%+、成本至多省 30%、同价）+ Claude Code 2.1.288 无人值守语义 + Codex 0.160.0 → 工具卡与深挖 03。
- deepseek-harness 五连发至 v0.2.0-rc.2（Messages-API-only 破坏性迁移、默认模型列表移除 V4 Flash 系）→ 工具卡。
- 华为"下一代 900 系列仅限中国市场"报道（9/24，中等置信）+ AMD MI450 Oracle 首批到货（9/9 窗口外背景）→ 芯片卡。
- 论文四篇：Periodic Weak Spots（分块 KV 压缩相位敏感 40pp）、KL/翻转率（TV 1.05 直对应、KL 11% 配对误判）、STEPQuant（Delta-rule 状态量化、SGLang 集成、内存 −68.7%）、ALR-IRA（off-policy 块投机监督失效、+36.5% 接受长度）+ 理论负结果（一致亚二次注意力近似不存在）→ 论文区。
- Cursor bots（9/23）、Mistral 平台弃用 GLM 5.2（9/28）→ 简讯。

## 编辑判断

本期主线是**栈在收敛，生态在分化**：DeepSeek 官方算子栈 9/30 同日把昇腾 950 变成第二后端（FlashMLA/TileKernels/DeepSelect），同时在 NVIDIA 侧砍掉 Hopper 与 V3 系并破坏 KV 格式——同一模型栈收敛到更少硬件代际（Blackwell + Ascend 950 双头），却在两套生态上分化出可复现路径（vLLM-Ascend 交出 950DT 兼容矩阵，壁仞拿到招标级订单）。OpenAI 用 DevDay 把 agent 从会话制改成长驻制、用 10/23 大限把旧模型收敛进 5.6 系；Anthropic 同周双发 5.5 系。债务市场给 GPU 担保品定出 6.78%/8.25%/9.95% 三档价格——收敛降低维护面，分化决定买谁，部署决策必须同时回答两个问题。社区侧三条失效模式（守卫回滚、KV 覆写、CPU 数值损坏）再次说明：升级决策的证据在 issue 区，不在 release note。

**KPI：Top5 新颖度均值 4.6；覆盖桶数 5（deepseek-radar、models-agents、inference-systems、infra-capital、community；china-industry 并入深挖与分类）；社区/非官方一手 3（#59305、#59104、#29774）；落选候选 9 组；degraded：否（8 桶 anysearch 成功，1 次单点核查回退内置搜索已注明）。**
