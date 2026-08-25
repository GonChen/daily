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
