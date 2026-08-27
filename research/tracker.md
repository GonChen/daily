# 跟踪清单

| 事项 | 首次日期 | 触发条件 | 状态 |
|---|---:|---|---|
| NVIDIA / OpenAI Ohio 项目融资 | 2026-08-20 | 新 SEC 文件、ready-for-service、并网、租约、担保或实际容量变化 | open |
| DeepSeek Harness | 2026-08-19 | RC 转正式、SQLite 迁移说明、Codex/Claude profile 权限变化或事故报告 | open |
| DeepGEMM #410 输入流式交接 RFC | 2026-08-23 | benchmark、实现 PR、合入、维护者采纳或明确拒绝 | open |
| SGLang Kimi-K3 SM107 MXFP4 | 2026-08-21 | 数值、显存、吞吐或端到端资格验证数据 | open |
| vLLM FlashInfer MoE token 上界 | 2026-08-21 | 端到端 benchmark、回归或 release note | open |
| DeepSeek GitHub 系统仓库 | 2026-08-21 | release、tag、合入 PR、README/模型卡或集成 PR 的实质变化 | open |
| Agent 长驻控制面 | 2026-08-20 | 权限/预算/队列/恢复机制的正式发布、事故或具名复现 | open |
| FlashInfer SM100/SM103 VSA | 2026-08-24 | stable release、独立复现、更多 GPU/模型的端到端生成数据 | open |
| FlashInfer W4A16 dense GEMM autotune 权衡 | 2026-08-24 | stable release、B200/SM100 复测、端到端吞吐与冷启动 ROI | open |
| Agent 请求语义：代理重试与工具解析 | 2026-08-24 | 任务成功率、误调用率、重复请求率、实际计费回归 | open |
| NVIDIA AgentX 机架级 throughput/MW | 2026-08-25 | 可复现实验配置、独立第三方复测、相同模型/功耗/拓扑对比与正式可用性 | open |
| SGLang gfx950 SWA attention 下界 | 2026-08-25 | stable release、MI355X/其他模型复测、#34461 与 #34462 合并后的 served A/B | open |
| vLLM batch-invariant persistent matmul | 2026-08-25 | 生产 request mix 下的 cold-start 摊销、更多架构/shape、稳定 release | open |
| FlashInfer SM120 NVFP4 SVDQuant LoRA | 2026-08-25 | cold-cache/非 graph 与模型端到端测量、更多 GPU、stable release | open |
| vLLM DeepSeek V4 live-adapter LoRA | 2026-08-25 | 更长训练、更多 rank/adapter swap 的 merge=False 等价与吞吐/显存数据 | open |
| SGLang DP FlashInfer EXTEND rank-local warmup | 2026-08-26 | stable release、不同 DP/shape 下的 cold/warm ROI、C128 高 CV 根因与独立复测 | open |
| vLLM DeepSeek V4 FlashInfer MoE-EP | 2026-08-26 | sequence-parallel stack、跨 checkpoint accuracy、SM100/EP8/NVSHMEM 约束下的独立 serving 复测 | open |
| vLLM TP batch invariance fallback | 2026-08-26 | #50505 deterministic path 的实际吞吐、长 prompt/更大 TP 的 bit-exact 复测 | open |
| FlashInfer SM120 NVFP4 attention LSE API | 2026-08-26 | 下游 `return_lse` 兼容性、同 run baseline、冷/端到端 attention 数据 | open |
| DeepSeek V4 shared-expert fusion topology gate | 2026-08-26 | EP per-rank shared slot 实现、稳定 CI、GB200 TP4 之外的 TTFT/ITL 数据 | open |
| Speculative sampling request admission | 2026-08-26 | TensorRT-LLM fail-closed 后的 admission 失败率、非 speculative fallback 和用户影响 | open |
| Hopper MXFP4 MoE scale OOB guard | 2026-08-27 | SM100 分支 sanitizer、主 CI 全绿、+14 MB capacity impact 与独立 gpt-oss serving 复测 | open |
| vLLM DP pause device-idle contract | 2026-08-27 | #52957 burst 缩减的合入、更多 DP/EP 的 resolve-to-idle/p99/死锁复测、非 torch.accelerator 后端覆盖 | open |
| SGLang TP FlashInfer autotune consensus | 2026-08-27 | 大 TP cold-tuning ROI、cache digest 漏变量、真实 request mix 的 p99 与 tactic divergence | open |
| FlashInfer SM12x MSA chunked top-k | 2026-08-27 | 端到端 serving、非 MTP/不同 batch、scratch 压力、SM120/121 独立复测 | open |
| FlashInfer Cake KDA piece-persistent M128 | 2026-08-27 | CUDA Graph/explicit workspace fallback 比率、29-shape 独立 campaign、服务 TTFT/ITL 与状态语义复测 | open |
| FP8 K-cache token_id int64 overflow guard | 2026-08-27 | <4.2M tokens 的独立回绕复现、DSA/DSV4 之外同型 kernel 覆盖、长上下文服务 A/B | open |
| TensorRT-LLM KV host-tier world-rank consensus | 2026-08-27 | 用户工作负载/性能数字、attention-DP 子组一致性、fallback/rebuild 的事故与尾时延复测 | open |
| SGLang DeepEPv2 ElasticBuffer capacity/fail-fast 契约 | 2026-08-28 | H20/B200 之外平台复测、支持/拒绝组合的实际验证、多节点同 fabric legacy 基线、capture hit/p99 | open |
| SGLang gfx950 Qwen3.5 MTP attention | 2026-08-28 | C16 TPOT 回归根因、非准入形状误 dispatch、更多 MI355X 模型与并发的 served A/B | open |
| AITER int32 KV seqused_k 2 GiB wrap | 2026-08-28 | <2 GiB 是否也失败、int64 在 >2.87 GiB 的地址覆盖、AITER 上游强制 int64、CI 全绿 | open |
| FlashInfer trtllm-gen MoE cubin manifest arch 过滤 | 2026-08-28 | filtered manifest/运行时 dispatch 一致性、persisted tactic 升级迁移、sm107/sm103 AOT 复测 | open |
| TensorRT-LLM MiniMax-M3 hybrid NVFP4/FP8 KV staged route | 2026-08-28 | mixed batch/decode q>8 误选、长运行 scratch/graph replay、GB300 之外平台与独立服务复测 | open |
| vLLM DeepSeek V4 Humming SwiGLU clamp | 2026-08-28 | 更多 request mix、不同 TP/EP 与硬件的 serving A/B，确认 +1.40% 是否超过噪声 | open |
| vLLM Hopper low-latency GEMM microbenchmark | 2026-08-28 | Kimi 服务 workload、冷启动和不同 token bucket 的端到端结果 | open |
| vLLM native CP MLA decode | 2026-08-28 | 同配置 serving A/B、DCP 故障/尾时延和更多模型/拓扑的验证 | open |
| FlashInfer CUB variable-length top-k | 2026-08-28 | CCCL 依赖合入、稳定 release、同 run 服务与 JIT cost A/B | open |
| TensorRT-LLM KDA prefill beta-sigmoid/metadata path | 2026-08-28 | draft GPU parity/CI 结果、端到端收益和 fallback 条件 | open |
