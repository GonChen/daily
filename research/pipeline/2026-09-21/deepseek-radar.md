# 2026-09-21 deepseek-radar 桶候选

总判断：官方 GitHub 窗口内（9/18–9/21）零 push，全部实质变化在集成面（vLLM/SGLang）；窗口内 vLLM 合并 24 个 DeepSeek 相关 PR、SGLang 26 个，其中约 6 笔直接改写 V4.1 推理栈的复现条件。

## 1. vLLM #57667：DSA 路径移除运行时 JIT（offset candidate end buffers）
- 日期：9/19 合并｜类型：Bugfix/部署依赖边界（作者 WoosukKwon，label bug+ready）
- 事实：DSA 推理路径中 offset candidate end buffers 分配不再走运行时 JIT 编译，改预编译路径。
- 影响：V4.x 的 DSA 前向不再依赖运行时编译器，冷启动确定性与无编译环境可复现性提升；复现基准不再需把 JIT 状态纳入变量。
- 来源：https://github.com/vllm-project/vllm/pull/57667
- 新事实：DeepJIT（9/14 开源）之后第一笔落地的下游脱钩——运行时 JIT 被从 DSA 热路径剥离。

## 2. vLLM #57604：DSV4.1 MegaMoE staging 与 NVFP4 cache gathers（与 inference-systems 桶同源）
- 日期：9/18 合并｜类型：Perf/数值路径
- 事实：staging 缓冲与 NVFP4 反量化 cache gather 重构优化（详见 inference-systems 桶：≥64 token 门控、内核 5.4×）。
- 影响：V4.1 FP4 推理的吞吐与数值序列同时改变；旧 commit 复现 NVFP4 基准将对不上。
- 来源：https://github.com/vllm-project/vllm/pull/57604
- 新事实：与 9/14 DeepGEMM 仓库侧 Mega MoE 修复合起来构成 V4.1 MegaMoE 推理栈的新版本边界。

## 3. vLLM #57454：DSv4.1 保留 NaN 分数的候选块索引（DSA TopK）
- 日期：9/18 合并｜类型：Bugfix/数值正确性（另有 #52500 ragged decode padded 路径，9/19）
- 事实：DSA 稀疏注意力候选选择中，得分为 NaN 的候选块索引不再被错误丢弃/重排。
- 影响：极长上下文/异常输入下 DSA 候选集合选择恢复确定性；DeepSelect（DSA TopK）在 vLLM 侧的语义对齐修复。
- 来源：https://github.com/vllm-project/vllm/pull/57454 ；https://github.com/vllm-project/vllm/pull/52500
- 新事实：NaN 传播语义被显式定义——代码层面首次明确 DSA TopK 对非法分数的处理契约。

## 4. vLLM 跨硬件 MLA 数值边界修复：SM100 fp8_ds_mla cache scales + ROCm sparse-indexer logits collapse
- 日期：9/20（#49435）/9/18（#50455）合并｜类型：Bugfix/数值正确性（另有 #57434 ROCm DSv4.1 decode topk ragged metadata 复用，9/20）
- 事实：#49435 修复 SM100（B200）上 fp8_ds_mla 的 KV cache scales 错误；#50455 修复 gfx950/gfx942 上 DSv4 sparse-indexer logits 整体塌陷。
- 影响：Blackwell 与 AMD MI300+/MI350 级硬件上 V4/V4.1 的 FP8 MLA 数值基线被重置；此前在这两类卡上跑出的精度结果不可作为对照。
- 来源：https://github.com/vllm-project/vllm/pull/49435 ；https://github.com/vllm-project/vllm/pull/50455
- 新事实：两大非 Hopper 平台各一笔"结果级"修复——V4.1 在 H100 之外的复现此前并不成立。

## 5. SGLang #40353：mHC 上下文移出非 V4 的 compiled MoE forward
- 日期：9/19 合并（Collaborator BBuf）｜类型：Bugfix/隔离性
- 事实：V4 引入的 mHC（hyper-connection）上下文此前会泄漏进非 V4 模型的 torch.compile MoE 前向，现按模型隔离。
- 影响：非 V4 模型编译图不再被 V4 结构污染；复现非 V4 模型基准应跳过 9/19 前的窗口版本。
- 来源：https://github.com/sgl-project/sglang/pull/40353
- 新事实："反向复现"修复：V4 新结构改变了同仓其他模型的数值行为。

## 已核查、无实质变化（9/18–9/21）
deepseek-harness（最近 push 9/17，v0.1.6-alpha.2 已报道）、DeepEP（9/16）、FlashMLA（9/15）、DeepJIT/DeepGEMM（9/14）、DeepSelect/deepseek-recipe（9/10）、DeepSeek-V3/TileKernels/smallpond/DeepSpec/3FS（远早于窗口）。V4.1 Pro 无上线迹象。
## 未尽事项
TensorRT-LLM 与 FlashInfer 的窗口内 DeepSeek PR 因抓取预算未单独核查，留待下期。
