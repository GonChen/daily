# 2026-08-27 research ledger

## 采集、去重与子代理状态

已以 8/25、8/26 ledger 与 tracker 作为去重基线，并轮换八个新反向问题。动态发现覆盖 GitHub API 的 SGLang、vLLM、FlashInfer、TensorRT-LLM、DeepSeek 组织和四组官方 Web 搜索。DeepSeek 官方组织在窗口内无新 push/release；芯片资本、模型/Agent 产品、中文产业和论文没有同时满足窗口、一手来源和量化影响的新增事实，安静处理。

两轮八桶 `intel-scout` 均在超过一分钟后无首条模型事件，已停止。`pi auth check --model br/deepseek-v4-flash --json` 返回 `ready`，进程继承 `HTTP_PROXY`、`HTTPS_PROXY`，故降级原因是 **scout 模型首事件停滞，不是认证或系统代理变量缺失**。主控完成一手 GitHub API/PR 核验；两项 `intel-analyst` 已完成控制面和 fast-path 深挖，`intel-editor` 复核结果见 pipeline。

完整候选和落选见 [fallback discovery](pipeline/2026-08-27/fallback-discovery.md)、[selection](pipeline/2026-08-27/selection.md)、[control-plane deep dive](pipeline/2026-08-27/deep-control-plane.md) 与 [fast-path deep dive](pipeline/2026-08-27/deep-fast-path.md)。

## 入选事实

- **SGLang #36456，8/26 合入：**Hopper 的 MXFP4 MoE scale kernel 在 `block_k=128`、gpt-oss hidden K=2,880 时会按 23 tile 走到 2,944；末 expert 可在 17.7 MB scale allocation 外读取 3,072 B。PR 以 scale-K 90→92 pad（每 GPU +14 MB）修复。作者在 4×H200、gpt-oss-120b TP4、flush-cache serving 中报告三种形状吞吐 −0.05% 至 +0.64%，明确称为噪声；compute-sanitizer 66→0，模拟 H100 内存的 CI coredump 3→0。修复前的 GPQA 0.0 是 coredump 令每个请求为空、评测无法完成的结果，修复后为 0.6313；不是能力基线。SM100 `BLACKWELL_SCALE` 未覆盖，PR 快照仍有部分 CI 红灯；所有数字为作者报告。[PR #36456](https://github.com/sgl-project/sglang/pull/36456)
- **vLLM #52914，8/26 合入：**DP `pause_generation()` 曾以 CPU `has_work()`/gloo predicate resolve，但 idle engine 会为 consensus 启动 32 个未被 queue 追踪的 dummy forwards。作者在 DP2+EP、PowerMoE-3b、H200、把 dummy batch 放大约 110ms 的 A/B 中报告 pause 3.40s 后 baseline device 仍 busy；加入 all-worker `synchronize_device` barrier 后 pause/drain 返回均 idle。该 PR 不缩短 burst，关联 #52957 才报告 0.17s；它是控制面正确性而非模型性能结论。[PR #52914](https://github.com/vllm-project/vllm/pull/52914)
- **SGLang #35343，8/26 合入：**FlashInfer autotune 在 TP4 每 rank 用本地 timing argmin，使 gpt-oss-120b、4×GB300 的 20/20 tactic bucket 分叉。PR 对每 tactic timing 做 TP all-reduce，并对 cache digest+env stamp 分歧整体失效缓存；分叉变 0/20。作者报告单流 509.56±0.72→510.68±0.13 output tok/s，c32 22,956→23,130 tok/s；cold autotune 79→106s。结论是稳定性和无回归，不应表述为稳态速度提升。[PR #35343](https://github.com/sgl-project/sglang/pull/35343)
- **FlashInfer #4030，8/26 合入：**SM120/121 MSA indexer 以 chunked top-k、q-tiled partial 和 in-kernel causal offset 覆盖小 batch/长序列。作者用 RTX PRO 6000 Server、RTX 5080、GB10、cold-L2 CUPTI GPU-time 对比 vLLM：batch1 MTP 2k–32k ratio 0.73–0.98→1.20–1.36；new top-k 对被替换 kernel 的 decode 为 1.4–2.2×、8k–32k prefill 为 1.2–2.1×。`per_token_nvp`、shape 边界或 scratch 超 128 MB 回退；batch128 由 proxy 主导，端到端 ratio 仅 1.00–1.03。不是整服务吞吐。[PR #4030](https://github.com/flashinfer-ai/flashinfer/pull/4030)
- **FlashInfer #4728，8/26 合入：**Cake KDA M128 recurrence-piece persistent route 只对 CC10.0/10.3、148/152 SM、uniform eager、caller-owned in-place initial state、无 workspace/`seq_order` 及 roofline 有利时开放；CUDA Graph 保持旧 route。作者以 29 shapes、四种 GPU、cold-L2 CUPTI complete public API GPU-time 报相对 FlashKDA 2.568×–2.725×，相对 frozen #4605 仅 1.018×–1.045×，BF16 tolerance 1e-2。它不是端到端 inference，且 route 条件是行为契约。[PR #4728](https://github.com/flashinfer-ai/flashinfer/pull/4728)

## 雷达与落选

- SGLang #30859 将三处 FP8 K-cache kernel 的 `token_id` 扩为 int64；typical stride 512 时约 4.2M token 可避免 int32 回绕。H200 focused 34 passed、76 subtests，TP4+EAGLE GSM8K 1,319 examples 96.66%/zero error；没有服务 A/B，因此不升格。[PR #30859](https://github.com/sgl-project/sglang/pull/30859)
- TensorRT-LLM #18092 令 KV cache V2 host-tier 初始化在 world rank 上收敛 `KEEP_HOST`/`USE_NO_HOST`/`ABORT`，有 31 unit 和 2-rank attention-DP/MPI 测试；没有用户工作负载、性能或事故量化，作为控制面雷达。[PR #18092](https://github.com/NVIDIA/TensorRT-LLM/pull/18092)
- SGLang #36233 仅加入 CUDA 13.4 developer-preview/Rubin 容器，且预期 FlashInfer JIT startup 变长；vLLM #53942 仅有 CUDA Graph kernel sweep；TRT-LLM #18262 回滚 MSA reuse 但无 GPU runtime tests 和影响数字，均不占 Top 5。

## 编辑判断

本期主线是：fast path 需要在进入前证明**地址与资源合法**，在退出时证明**所有相关 rank 与 device 真正完成**。#36456 和 #4030 把 K tile、scratch 与形状范围编码为准入/回退；#4728 把 eager/state/CUDA Graph 边界写进 route；#52914、#35343 与 #18092 则将局部完成信号升级为 group-level proof。实现的可靠性优先于局部微基准；fast path 的 fallback、同步和 cold-start 成本必须一同计量。

**KPI：Top5 新颖度均值 4.30；标准桶覆盖数 3；社区一手来源 5（口径含开源 PR 作者报告）；落选候选数 5；degraded：是，intel-scout unavailable（两轮均无首个模型事件；认证与系统 proxy 已确认；主控发现、两项 analyst 和 editor 审校正常）。**
