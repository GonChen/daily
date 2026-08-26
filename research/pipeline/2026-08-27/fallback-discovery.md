# 2026-08-27 主控一手发现

## 采集状态

八个 `intel-scout` 线程均以 `br/deepseek-v4-flash` 启动；两轮各等待超过一分钟，均无首条 assistant 事件。`pi auth check --model br/deepseek-v4-flash --json` 返回 `ready`，环境包含 `HTTP_PROXY` 与 `HTTPS_PROXY`。因此本阶段降级为主控一手发现；原因记录为**模型首事件停滞**，不是认证或系统代理变量缺失。

## 动态搜索组

1. GitHub API：`sgl-project/sglang` 在 8/26 合入 PR。候选包括 #36233、#35377、#30859、#36456、#35343。
2. GitHub API：`vllm-project/vllm` 在 8/26 合入 PR。候选包括 #53942、#52914、#53838、#53311。
3. GitHub API：`flashinfer-ai/flashinfer` 在 8/26 合入 PR。候选包括 #4030、#4728、#4610。
4. GitHub API：`NVIDIA/TensorRT-LLM` 在 8/26 合入 PR。候选包括 #18262、#18092、#18140。
5. GitHub API：`deepseek-ai` 组织仓库。DeepGEMM 最近 push 为 8/11、DeepEP 为 8/20、Harness 为 8/21；窗口内无新 push/release。
6. 官方 Web 搜索：NVIDIA Technical Blog 的最新直接相关项为 8/25 的 Shadow Engine Recovery；不在本轮 8/26–8/27 窗口，未入选。AI 数据中心、中文产业和论文检索没有得到具备一手时间戳、测量口径和新事实的材料。

## 合格候选

- **SGLang #36456**：Hopper 的 MXFP4 MoE scale kernel 在 `K=2880`、`block_k=128` 时实际遍历 2,944，末 expert 可能越界 3,072 B；4×H200、gpt-oss-120b TP4 的 compute-sanitizer 报错 66→0，模拟 H100 内存的 CI coredump 3→0、GPQA 0.0→0.6313。修复本身端到端吞吐在三种请求形状中为 −0.05% 至 +0.64%，作者明确称处于噪声范围。限制：仅 SM90；SM100 路径未处理；PR 快照仍有部分 CI 红灯。[PR #36456](https://github.com/sgl-project/sglang/pull/36456)
- **SGLang #35343**：FlashInfer tactic autotune 在 TP4 每 rank 独立 argmin，GB300 的 20/20 shape bucket 出现 tactic 分歧。共享每 tactic 时间并在 cache digest 不同处失效缓存后为 0/20；gpt-oss-120b、4×GB300 单流为 509.56±0.72→510.68±0.13 output tok/s，c32 为 22,956→23,130 tok/s，代价是 cold autotune 79→106s。限制：作者报告，TP4/GB300；稳态不应表述为速度提升。[PR #35343](https://github.com/sgl-project/sglang/pull/35343)
- **vLLM #52914**：DP `pause_generation()` 曾只等 CPU predicate，且 idle engine 的 32 dummy forwards 仍运行；DP2+EP、PowerMoE-3b、H200 的复现中 pause 返回后 device busy，wall time 3.40s。加入 all-worker device barrier 后返回和 drain 均为 idle；它不缩短 3.40s，独立 PR #52957 才把 cadence burst 降至 0.17s。限制：复现人为把 dummy batch 放大约 110ms；作者 A/B 和生产报告，非模型质量测量。[PR #52914](https://github.com/vllm-project/vllm/pull/52914)
- **FlashInfer #4030**：SM120/121 MSA indexer 以 chunked top-k、q-tiled partial 和 in-kernel causal offset 改善小 batch/长序列。RTX PRO 6000 Server、RTX 5080、GB10 的 CUPTI cold-L2 GPU-time 对 vLLM ratio：MTP batch1 的 2k–32k 从 0.73–0.98 提至 1.20–1.36；new top-k 对被替代 kernel 为 decode 1.4–2.2×、8k–32k prefill 1.2–2.1×。batch128 proxy 主导时端到端 ratio 仍 1.00–1.03。限制：比值基线为 vLLM，同一 PR 作者；不是整服务吞吐。[PR #4030](https://github.com/flashinfer-ai/flashinfer/pull/4030)
- **FlashInfer #4728**：Cake KDA 的 M128 eager prefill 专用 route 要求 uniform eager、caller-owned in-place initial state、没有显式 workspace/`seq_order`，CUDA Graph 继续走旧 route。B200/B300/GB200/GB300 的 29 shapes 全量 cold-L2 CUPTI 几何均值，对 FlashKDA 为 2.568×/2.712×/2.695×/2.725×；相对 frozen #4605 仅 1.018×–1.045×。限制：public API GPU time，不是 end-to-end inference；BF16 tolerance 1e-2，且从语义约束触发 fallback。[PR #4728](https://github.com/flashinfer-ai/flashinfer/pull/4728)
- **SGLang #30859（雷达）**：3 个 FP8 K-cache kernel 把 `token_id` 扩成 int64，以避免典型 stride 512 在约 4.2M tokens 溢出。H200 focused 34 passed、76 subtests，4×H200 TP4+EAGLE GSM8K 1319 examples 的 accuracy 96.66%、errors 0。没有服务性能 A/B，故不占 Top 5。[PR #30859](https://github.com/sgl-project/sglang/pull/30859)
- **TensorRT-LLM #18092（雷达）**：host-tier KV 初始化在某 rank fallback 时以 `KEEP_HOST`/`USE_NO_HOST`/`ABORT` 取世界 rank 共识；2-rank attention-DP/MPI 和 31 unit tests 覆盖。没有用户工作负载或性能/事故数字，保持请求语义雷达。[PR #18092](https://github.com/NVIDIA/TensorRT-LLM/pull/18092)

## 拒绝和安静桶

- SGLang #36233 只提供 CUDA 13.4 developer-preview/Rubin 容器和 nightly 依赖，预期 FlashInfer JIT startup 变长，没有服务测量。
- vLLM #53942 为 Kimi K3 `eh_proj` kernel sweep：m=1 25.2%、m=2 12.9%，但仅 CUDA Graph replay kernel 微测，未入选。
- TensorRT-LLM #18262 回滚 MiniMax-M3 MSA plan reuse，理由只有 feature-branch IMA，且无 GPU runtime tests 或影响量化，保留为维护者回滚信号。
- TensorRT-LLM #18140、vLLM #53838 等项在读取范围内没有完整、可比较的原始工作负载和结果；不以标题入选。
- 芯片资本、模型/Agent 产品、中文产业和论文桶没有满足窗口、一手来源、可量化影响三项的新增事实，安静处理。
