# 2026-09-21 inference-systems 桶候选

## 1. SGLang v0.5.20 正式版发布：SM120 torch fallback 被 DeepGEMM 替换、Blackwell FlashMLA 被 TRT-LLM 内核替代，多处默认行为翻转
- 日期：2026-09-18（22:41 打 tag）｜类型：官方 release（713 个 PR 的季度版）
- 事实：
  - SM120（RTX PRO 6000）：DSV4-Flash 此前唯一可用路径是 torch fallback，现换 DeepGEMM paged-MQA sparse-MLA indexer + DeepGEMM FP4 MoE backend（#29927，opt-in）。4×RTX PRO 6000 decode TPOT 36.1→10.5 ms（batch 1，约 3.4×），TTFT 8K→128K 输入下降 20%。
  - Blackwell：TRT-LLM attention 内核覆盖 DSV4 的 CSA/HCA 层（SM100/SM103），B200 内核级 prefill ~1.2×、decode ~1.45× 快于 FlashMLA（#30805）；FlashInfer MegaMoE 以 `--moe-runner-backend flashinfer_megamoe` 接入，DSV4-Flash NVFP4 TP4/DP4 prefill 吞吐 +11.9%，饱和 decode 与 trtllm runner 差 2% 内（#31470）。
  - 默认行为/回退语义翻转：`/v1/responses` 不再默认驻留内存，未加 `--enable-response-store` 时检索、`previous_response_id` 链、后台请求一律 400，且 PD 部署禁止开启（#39122）；prefill CP v1 删除（#36228）；CUDA 12 轮子/镜像退役，v0.5.19 为最后一版（#38404）。
  - 其他：统一 radix 树 SWA 分支点缓存使 DSV4-Flash 共享系统提示 token 命中率 43.8%→60.8%、mean TTFT 1.57→1.07 s（#34565）；ROCm pageable 拷贝改分阶段暂存后 GLM-5.2 TP4 在 4×MI355X 加载 505.7→40.4 s（#37720）。
- 影响：升级即换默认行为：Responses API/PD 用户必须显式加 flag 否则 400；cu12 需锁 v0.5.19；SM120 与 Blackwell 的 DSV4 用户应按 release notes 切内核路径。
- 来源：https://github.com/sgl-project/sglang/releases/tag/v0.5.20
- 新事实：release 级新证据——SM120"torch fallback 唯一路径"被官方替换（TPOT 3.4×）、FlashMLA 在 B200 被 TRT-LLM 内核替代（decode 1.45×）均为窗口内首次官方核验。

## 2. vLLM #57604：DSV4.1 MegaMoE 8-token staging tile 在小批量反优化，按 ≥64 token 门控
- 日期：2026-09-18 合入｜类型：已合入主线（维护者 WoosukKwon 自报数据）
- 事实：MegaMoE prefill staging 改多 token/tile 并重设 NVFP4 gather 网格。门槛数据（GB200，H5120）：强制 8-token tile 使 2–16 token 内核回归（16 token：2.400→2.752 µs）、32 token 持平、64 token 起改善，8192 token 时 175.616→32.416 µs（约 5.4×）——最终按"≥64 token 才用 8-token tile"门控。NVFP4 gather 在 100K 行时 1/2/4/8 请求 −88%/−76%/−50%/−18%。端到端（GB200×4，作者注明非 serving 吞吐）：Q16K+KV100K −3.51%、B31 −7.45%；GSM8K 1272→1271/1319，DSpark acceptance 3.8281→3.8289。
- 影响：小批量（<64 token）不被新 kernel 伤害；低并发收益 0，高并发 prefill 才有 5× 级内核收益。
- 来源：https://github.com/vllm-project/vllm/pull/57604
- 新事实："新优化在低并发下反优化"的逐点内核数据表与显式门控阈值（64 token）。

## 3. vLLM #57421：Humming 量化 MoE scratch 共享省 97.5% 显存，但作者报告未解释的精度对照异常
- 日期：2026-09-20 合入｜类型：已合入主线（维护者 mgoin 自报数据）
- 事实：Marlin/Humming 持久 workspace 收归 WorkspaceManager。作者报告（B300 单卡，Qwen3.6-35B-A3B-NVFP4，40 MoE 层/256 专家，固定 8 GiB KV + CUDA graphs）：scratch 对象 40→1，8192 token 时 scratch 10330.684→258.267 MiB（−97.5%），初始化后 GPU 分配省 9.836 GiB。正确性：GSM8K 1319 题 91.58%（基线）/91.05%（基线复测）/91.21%（改后）；改后与基线 token 序列完全匹配率 690/1319，而两个基线互相只有 669/1319——作者明确声明"不排除因果精度影响，原因未解决"，且本 PR 不构成 latency 改进证据。
- 影响：NVFP4/Humming grouped MoE 用户获得接近 10 GiB/卡驻留显存返还（可用于 KV）；精度等价性未闭环，量化敏感业务升级后自跑 GSM8K 对照。
- 来源：https://github.com/vllm-project/vllm/pull/57421
- 新事实：带"双基线对照"的一手数据——内存优化引入超过基线噪声的精度位移且原因未明。

## 4. SGLang 主干删除独立 SWA/Mamba radix cache：统一 radix 树成唯一路径
- 日期：2026-09-20 合入（#40313）｜类型：已合入主线
- 事实：独立 SWA/Mamba radix 缓存实现被移除（后续 #40469 等测试修复证实）；统一 radix 树（#34565 分支点缓存）成为唯一路径；配套 #40354（9/20）修复 SWA prealloc 回收经 DSV4 HiSparse 分配器的前向通路。
- 影响：依赖旧独立 SWA 缓存行为的部署无回退选项；SWA+共享前缀负载应实测命中率迁移效果。
- 来源：https://github.com/sgl-project/sglang/pull/40313
- 新事实：把 v0.5.20 的"统一 radix 树收益"落成主干上不可回退删除。

## 安静项
TensorRT-LLM 仍 v1.3.0rc27（无新 release）；FlashAttention beta31（9/16）；FlashInfer v0.7.0rc3（清理级）；PyTorch 2.14.0（9/2）；vLLM #57273（Qwen4Exp QSA sm_90 tuning 表，无 serving A/B）。
