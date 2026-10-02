# 2026-10-03 deepseek-radar 桶候选

## 1. SGLang v0.5.21（10/2）：DeepSeek-V4.1 Flash 进入正式支持清单，长上下文首 token 提速 22%
- 类型：release 级集成（详见 inference-systems 桶）｜事实：V4.1 Flash 列为新模型（LLM/VLM 双形态 + cookbook），Key Features 明确"22% faster first token on long prompts"（#40352）；DeepSeek 相关实质项：DSV4 Breakable CUDA Graph 下 C4 Indexer 捕获内存降 58% 至 18 GB（#36534）；DeepEP v2 MXFP8 dispatch + 延迟路由加权（#40030）、BF16 与 batch-invariant 推理（#38160）、按 rank 的 prefill dispatch 上界可由模型包声明（#41201）；DSA pooled-indexer DP attention breakable prefill 修复（#41311）；MXFP8-KV 跳过 CUDA-graph 保留槽写入修复（#35351）。release 由 Fridge003 于 10/02 01:09 签名发布。
- 来源：https://github.com/sgl-project/sglang/releases
- 新事实：SGLang 首个把 V4.1 Flash + DeepEP v2 MXFP8/BF16 语义收进正式 release 的版本。

## 2. vLLM v0.30.0（9/22）：DeepSeek-V4.1-Flash 头条新模型，KV 全量 MXFP8 + V4 CPU 后端
- 类型：release 级集成（详见 inference-systems 桶）｜事实：Highlights 以 V4.1-Flash 打头（#56214/#56228/#56208）；SM100 经 "FlashMLA V4.1 record" 整份 KV 以 MXFP8 存储（#56893）；DeepGEMM Mega-mHC（#56962）；Engram 异步预取 + DP 分片（#56512）；DeepSeek-V4 CPU 后端用 AVX512/AMX 实现 sparse MLA、indexer、mHC、compressor 内核（#55355）——无 GPU 可跑 V4 推理。细节：`--kv-cache-dtype auto` 在 FlashMLA 下解析为 fp8_ds_mla（#45091）、fused MLA epilogue 可选 Q-norm + group_size=32 FP8 打包量化（#56215）。
- 来源：https://github.com/vllm-project/vllm/releases/tag/v0.30.0
- 新事实：V4.1 的 MXFP8 全 KV 路径（技术报告 FP4 KV 之外的第二个官方量化 KV 档位）与 x86 CPU 后端同版落地。

## 3. deepseek-harness 八天五发（v0.1.7-alpha.2 → v0.2.0-rc.2）：逼近 0.2.0 但仍无 GA，v0.1.7-rc.1 含破坏性迁移
- 日期：9/22、9/23、9/24、9/28、9/29 五连发（全部 Pre-release）｜类型：官方工具链迭代
- 事实：v0.1.7-rc.1（9/23）为最大节点：官方 DeepSeek 适配器改为仅 Messages API 并经 Files API 复用已上传图片（旧 `protocol` 配置与 Chat Completions 地址需迁移，破坏性）；默认模型列表移除 V4 Flash 与 V4 Flash Vision Exp；MCP 升级官方 SDK v2；新增 headless（stdin/--session-id/--json NDJSON）、SSH 远端工作区、实验性 Playwright/Chrome DevTools/Stagehand 浏览器后端与 Computer Use、插件管理器运行时装卸。v0.2.0-rc.1（9/28）自动化任务改可选插件包；v0.2.0-rc.2（9/29）桌面端内置 dsh 命令、实验性异步问答。
- 影响：仍无 GA；"默认模型列表移除 V4 Flash 系"是 V4 实验型号退场旁证；Messages-API-only 打破所有 Chat Completions 第三方接入。
- 来源：https://github.com/deepseek-ai/deepseek-harness/releases
- 新事实：五连发至 v0.2.0-rc.2；官方适配器强制迁移 Messages API。

## 4. 9/30 官方内核库"昇腾同日批量推送"：TileKernels 新增 Ascend 950 双后端、DeepSelect 补昇腾 TopK
- 日期：9/30｜类型：内核库平台扩展
- 事实：org 页显示 TileKernels、DeepSelect、DeepGEMM、DeepGEMM-Ascend、DeepEP、DeepEP-Ascend、DeepJIT、FlashMLA 等十个仓库同日 "Updated Sep 30, 2026"，同一批量 push 形态。已核实两处 README News：TileKernels（TileLang 官方算子库：MoE 路由、Engram 门控、mHC/Sinkhorn、FP8/FP4 量化+fused SwiGLU、RoPE，"全部算子已用于内部训练与推理"）9/30 新增华为昇腾支持——同一套 Python API 在 NVIDIA 与昇腾间运行时自动选后端，昇腾侧要求 Ascend 950 NPU + CANN 9.2.0+，NVIDIA 侧要求 SM90/SM100 + CUDA 13.1+；DeepSelect（DSA/采样器 TopK，对 torch.topk 提速 2-20 倍，覆盖 V3.2/V4/V4.1 lightning indexer 与采样场景）9/30 发布昇腾 NPU TopK 内核。
- 影响：与 FlashMLA 2026.09.30 昇腾条目互证——官方算子栈从"NVIDIA 为主、个别移植"转为双后端一等公民，清一色瞄准 Ascend 950/CANN 9.2，V4.1 系的非 NVIDIA 复现与部署边界被正式打开。
- 来源：https://github.com/deepseek-ai/TileKernels ；https://github.com/deepseek-ai/DeepSelect
- 新事实：协调的昇腾使能批次（两仓库初始开源日期未能核实、可能早于窗口，9/30 增量为窗口内确证）。

## 5. 核实结论：V4.1-Pro 查无实据
- 核实于 10/3：官方 news（9/10）与多家媒体一致确认 V4.1-Flash 为现役旗舰（模型名 deepseek-flash）；V4 Pro 自 9/14 起 API 请求全部转 V4.1-Flash；窗口内无任何 "V4.1 Pro" 发布/权重/API 动作。结论：截至 10/3 官方产品线仅 V4.1-Flash，Flash 即顶配、Pro 已实质退役。

## 已核查、无实质变化
DeepSeek-V3（最后 push 2025-08-28）、V3.2-Exp（2025-11）、R1（2025-06）、DeepSpec（7/9 后无动作）、awesome-deepseek-agent（9/17）、deepseek-recipe（9/10）、3FS/Engram/DualPipe/LPLB/OCR 系（窗口外）；DeepJIT/DeepGEMM(-Ascend)/DeepEP(-Ascend) 9/30 有 push（疑似同批昇腾使能，未逐 commit 核实）。
