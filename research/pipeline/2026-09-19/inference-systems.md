# 2026-09-19 inference-systems 桶候选

窗口说明：vLLM v0.29.0（9/9）、SGLang v0.5.19（9/5）、PyTorch 2.14.0（9/2）、cuDNN 9.26.0（9/9）、FlashInfer v0.7.0rc3（9/16，仅清理 trace-registry，低于准入线）等 release 落在窗口外或低于准入线。以下为窗口内合入/发布。

## 1. vLLM #57355：CUDA graph 捕获阶梯导致满载吞吐悬崖——batch 非 8 倍数时 2.55× 修复
- 日期：2026-09-17 合入｜类型：已合入主线 bugfix（作者报告）
- 事实：默认 CUDA graph 按 8 的倍数捕获；`max_num_seqs` 非 8 倍数时最后一段 batch（如 100 时的 97~100）落入 PIECEWISE 慢路径——过载服务器恰好稳定跑在 max_num_seqs 并发上，长期卡在慢路径且吞吐随运行衰减（2,922→829 tok/s）。作者数据（TP4 B200，Mistral-Small-4-119B-2603，8k–127k 混合 prompt）：batch 97 吞吐 1,523→3,876.85 tok/s（2.55×），与 batch 96 持平；Nsight 归因 PIECEWISE 下 graph-launch 间隙 ~0.69→5.5 ms、MNNVL all-reduce 等待 ~10µs→3.6–4.7 ms。修复仅覆盖投机解码关闭场景；未跑模型评测。
- 影响：升级前自查 `max_num_seqs % 8`；旧版即时缓解是对齐到 8 的倍数。满载 + 混合长度是最真实的服务形态。
- 来源：https://github.com/vllm-project/vllm/pull/57355
- 新事实：触发条件是"满载（=max_num_seqs）"而非 batch 形状本身；给出服务级衰减曲线证据。

## 2. SGLang #40105：FlashInfer MoE fused finalize 默认改回 unfused（数值精度优先），附各量化档位性能代价表
- 日期：2026-09-18 合入｜类型：已合入主线（默认行为翻转）
- 事实：`SGLANG_FLASHINFER_MOE_FUSED_FINALIZE` 默认 True→False，理由"更好的数值精度"，确定性模式强制关闭。代价表（单卡 B300/SM103，DeepSeek-V3 MoE shape，模拟 EP=8）：1 token 时 CuTe W4A4 per-tensor 延迟 +21.75%；16,384 tokens 时 CUTLASS +7.82%、CuTe W4A4 per-tensor +12.55%、per-token +10.70%，CuTe W4A16 反而 −9.20%。精度测试标注"Not run"——默认翻转是预防性的，作者自警单次 sweep 不足以断言。
- 影响：W4A4/W4A8 小 batch 档位可能损失 10–22% MoE finalize 延迟；精度预算充足可显式开回。
- 来源：https://github.com/sgl-project/sglang/pull/40105
- 新事实：罕见"先关后证"默认翻转：逐档位性能代价公开，精度动机本身无公开数字。

## 3. vLLM #56562：DSV4.1 元数据准备 Triton 融合——解码内核 4.13×、并发 1 吞吐 +22.3%，但并发 1024 收益缩到 1.4%
- 日期：2026-09-12 合入｜类型：已合入主线（作者报告）
- 事实：token→request 映射与扁平化 indexer 解码元数据从 PyTorch op 链改为 Triton 直写缓冲。4×GB200 TP4、FP8 KV、DeepSeek-V4.1-Flash：元数据内核 191.10→46.27µs（4.13×）、launch 77→17；E2E batch-1 TPOT −5.82%（DSpark 自适应验证下 −18.20%）；SPEED-Bench 8K/1K 并发 1 吞吐 304.9→373.0 tok/s；并发 1024 收益仅 1.4%、并发 8 TTFT −0.48% 轻微回退。24 个 builder 用例与基线 rtol=atol=0 逐位一致；GSM8K 96.82–96.97% 仅 sanity。
- 影响：单流/低并发与 DSpark 投机部署收益最大；高并发部署不要期待 E2E 变化。逐位一致可无风险滚动升级。
- 来源：https://github.com/vllm-project/vllm/pull/56562
- 新事实：少见的"完整并发扫描 + 逐位等价 + 明示收益消失点（conc≥1024）"三件套。

## 4. TensorRT-LLM v1.3.0rc27：精度回归 known-issue 配套禁用/回退语义
- 日期：2026-09-18 release｜类型：官方 release（rc 通道）
- 事实：Qwen3-235B NVFP4 on B200 开 all-reduce autotuning 可能间歇丢精度（workaround `TLLM_DISABLE_ALLREDUCE_AUTOTUNE=1`）；NVFP4 KV cache 在 SM107 上静默回退 FP8 KV（容量规划按 FP8 算）；MiniMax-M3 MXFP8 + piecewise CUDA graph + Triton 稀疏注意力在 B300/GB300 初始化崩溃（建议改 MSA）；GPT-OSS Eagle3 投机多卡可能挂起/丢精度；多卡 PD 分离 GB200 启动可能挂起；调度语义变化：每个未缓存 prefix 仅准入一个 context；移除废弃双模型投机解码（BREAKING）。全篇无吞吐数字。
- 影响：NVFP4 + 多卡 + 投机/PD 组合上线前逐条对 known-issue；SM107 容量测算按 FP8。
- 来源：https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc27
- 新事实：本窗口唯一把"精度代价→环境变量禁用→实现回退"三层语义写进 release note 的项目。

## 5. vLLM #56853：ROCm DeepSeek-V4 HCA 双流重叠——并发 1 TTFT −15.01%，收益随并发单调衰减
- 日期：2026-09-17 合入｜类型：已合入主线（作者报告）
- 事实：压缩器拆到辅助流与 wqa/wkv GEMM→RMSNorm→RoPE→SWA KV 插入并行，稀疏 MLA attention 前汇合。gfx950/MI355X 级、TP=8、FP8 KV、全 piecewise CUDA graph：并发 1 吞吐 69.61→72.00 tok/s（+3.43%）、TTFT −15.01%、TPOT −2.95%；并发 4/16/64 增益降至 +2.68%/+1.56%/+0.96%。GSM8K 门禁通过。
- 影响：默认路径收益为正、无需开关；又一条"并发越高收益越小"，高并发 ROCm DSV4 不应据此预估。
- 来源：https://github.com/vllm-project/vllm/pull/56853
- 新事实：与已报道 #51692（量化路径）不同优化（双流重叠），首次给出 HCA 层并发衰减曲线。

## 6. SGLang #40148：MI355X GLM-5.2 MXFP4 配方回退 Top-K v2——HIP Top-K 使 P90 交互性 +10.0%、吞吐仅 −0.15%
- 日期：2026-09-18 合入｜类型：已合入主线（配方/文档，附 serving 数字）
- 事实：GLM-5.2 MI355X MXFP4 cookbook 四场景全部移除 `SGLANG_OPT_USE_TOPK_V2=true` 回退 HIP Top-K 默认；镜像 bump 20260916。作者报告：并发 8 下 HIP Top-K 相比 Top-K v2 P90 交互性 +10.0%、吞吐 −0.15%。#39406 文档随之撤销。
- 影响：MI355X GLM-5.2 用户跟随新镜像保持默认；与 #40105 同构——尾时延/精度在真实 mix 下压过内核收益。
- 来源：https://github.com/sgl-project/sglang/pull/40148
- 新事实：给"何时应禁用"提供现成答案：官方配方正式撤回上周的新内核优化。

## 雷达（低于准入线但有跟踪价值）
- vLLM #44890（9/17）：`release_kv_cache_memory()` KV-only 部分休眠（保权重、清 KV、暂停调度），动机 RL 权重更新峰值显存；失败语义 fail-closed；无 serving 基准。
- vLLM #57647（9/19）：Laguna DFlash NVFP4 acceptance 参考从 3.55 修正为实测 3.05；MI355X 仿真 NVFP4（3.051/0.895）与 GB300 原生 NVFP4（3.0495/0.890）在 200 题 GSM8K 三位有效数字一致。注：这是 vLLM 自家测试，不构成对 SGLang #39087（DFlash2 量化 0.004）的修复或复现，仅说明量化投机 draft 在 NVFP4 下可保持健康 acceptance。
- SGLang #38409（9/14）：修复 DeepSeek V4 K cache 位置读取未等待 PDL 完成的竞态。
- FlashAttention fa4-v4.0.0.beta31（9/16）：SM100 Flash MLA 补 attention sink（#2768）；SM100 hd256 2-CTA 支持 seqused_q/k 与 paged-KV（#2810）。
- SGLang #40034（9/18）：agentic rollout 模拟器与离线 explorer 基准设施，尚无结论性数字。
