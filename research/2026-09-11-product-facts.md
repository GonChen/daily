# 2026-09-11 research ledger

## 采集、去重与降级

按 9/8–9/11 窗口扫描 SGLang、vLLM、FlashInfer、TensorRT-LLM 和 DeepSeek 官方组织；与 8/29、8/30 ledger 及 tracker 去重。详见 [dedup](pipeline/2026-09-11/dedup.md)、[fallback discovery](pipeline/2026-09-11/fallback-discovery.md)、[selection](pipeline/2026-09-11/selection.md)、[deep gating](pipeline/2026-09-11/deep-gating.md)。芯片/供应链、基础设施/资本、中文产业没有满足准入线的一手新增事实，保持安静。

八桶 `intel-scout` 及一次补齐大写代理变量后的 scout 重试，均在首条模型事件前以 `pi API error: Connection error` 失败；`intel-editor` 同样失败。`br/deepseek-v4-flash` 认证为 ready，重试仍失败，故不将问题归因于代理变量。日报按主控对 GitHub PR、issue、release 的一手核验降级完成。

## 入选事实

- **SGLang #39068，9/11 合入｜主线提交、作者报告：**为 DeepSeek-V4.1 的 DSpark target verify 合并 compression、indexer 与 projection 等短 kernel。4×GB300、TP4/EP4、BS1、4,096 input/1,024 output、`SGLANG_SIMULATE_ACC_LEN=5.5` 下，记录基线 761.03→853.49 streamed decode tok/s（+12.15%）；C2 进一步比 802.38 提高 6.37%。33 tests +4 subtests pass，但 GPU CI 未跑；吞吐排除 prefill，模拟接受率不能代表自然接受率或质量。[PR #39068](https://github.com/sgl-project/sglang/pull/39068)
- **vLLM #51692，9/10 合入｜主线提交、作者报告：**ROCm bpreshuffled blockscaled FP8 GEMM 在符合 shape/tuning 条件时启用。8×MI350、DeepSeek-V3、1k/1k：TP8+DPA 各并发 QPS +4.61%–8.14%，TP8+EP -0.39%–9.01%；GSM8K flexible exact 0.9477 对 nightly 0.9439。作者要求临时设 `VLLM_ROCM_USE_AITER_FP8BMM=0`，数字不外推到该前提以外。[PR #51692](https://github.com/vllm-project/vllm/pull/51692)
- **FlashInfer #4967，9/11 合入｜主线提交、作者报告：**B200/B300 的 fused KDA decode Cake backend。相对 CuTe DSL，B200 官方 21-shape subset 1.0491×、B300 21-shape composite 1.0504×；B200 1,315-case composite 1.0241×。默认仍 `cute-dsl`，Cake 需显式或满足 host-known state-index 条件的自动选择；综合表含未重测案例。[PR #4967](https://github.com/flashinfer-ai/flashinfer/pull/4967)
- **DeepSeek Harness dsh-v0.1.5-rc.1，9/10 发布｜官方 RC：**新增 DeepSeek-V4.1-Flash adapter，支持图文及历史 system prompt 更新；可续聊子代理支持排队、编辑、单条/全部 Steer 与停止；动态 system prompt 在模型声明支持时保持 KV cache；外发请求遵从启动环境的 `HTTP_PROXY`、`HTTPS_PROXY`、`ALL_PROXY`、`NO_PROXY`。这是预发布，非 GA，且未给出任务成功率/性能对照。[release](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.5-rc.1)
- **SGLang issue #39087，9/11｜社区一手报告，未确认：**报告者在 2×RTX3090、TP2、Qwen3.8 target 上比较同一 DFlash2 模型：compressed-tensors draft 的 accept len 1.03（422 batches）、rate 0.004、约38 tok/s；BF16 draft 为 3.71（100 batches）、0.61、约171 tok/s。功能测试可通过而投机收益坍塌；无维护者确认/修复，不能作为普遍结论。[issue #39087](https://github.com/sgl-project/sglang/issues/39087)

## 雷达与落选

- TensorRT-LLM #18541 将 KVCM2 长序列 resize 拆为拓扑选择 copier 和 background resize，并通过 78 C++、220 Python tests；无端到端 A/B，暂作工程雷达。
- vLLM #48247 声称 MI300 uniform DP batch 的 TPOT 约 +3%，但仅 DP group，且与 #51692 同类，保留为 ROCm 雷达。
- FlashInfer #4784 是 B200 多节点 NVLink MoE all-to-all backend 的正确性/集成工作，没有服务吞吐数据，不挤占 #4967。

## 编辑判断

本期主线是：**先发布快路径的命中条件，再发布速度数字。** #39068 用模拟接受率获得 +12.15% decode，#51692 的 TP8+DPA 与 TP8+EP收益区间不同，#4967 的 Cake 默认不替换 CuTe DSL；三者都说明硬件、shape、并行拓扑或 backend 选择不能被省略。Harness RC 则把同一原则带到 agent：代理队列、Steer 与系统代理的继承必须成为显式运行时契约。#39087 提醒，即使生成输出仍正确，量化 draft 的接受率坍塌也会变成吞吐事故。

**KPI：Top5 新颖度均值 4.20；标准桶覆盖数 3（推理与系统、开源算子、模型与 Agent）；社区/非官方一手 1（#39087）；落选候选 3 组；degraded：是，所有 pi 侦察/编辑线程均因连接错误在首事件前失败，主控以一手来源核验继续。**
