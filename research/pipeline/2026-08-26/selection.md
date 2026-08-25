# 2026-08-26 选题决议（主控降级执行）

## Top 5

| 排名 | 事实 | 桶 | 新颖度 | 物质性 | 可验证性 | 准入线 |
|---:|---|---|---:|---:|---:|---|
| 1 | SGLang #36219：DP rank-local EXTEND warmup | inference-systems | 5 | 5 | 5 | 1，量化 served TPS 与准确性 |
| 2 | vLLM #49636：DeepSeek V4 FlashInfer MoE-EP | models-agents / deepseek | 5 | 5 | 4 | 1，量化 HTTP serving 与 accuracy gate |
| 3 | vLLM #51292：TP batch invariance 回退 | inference-systems | 5 | 5 | 5 | 1，bit-exact 输出与吞吐权衡 |
| 4 | FlashInfer #4502：SM120 NVFP4 attention | chips / papers-oss | 4 | 4 | 4 | 1，量化 kernel 与 API 行为 |
| 5 | SGLang #35505：DeepSeek V4 shared-expert fusion | models-agents / deepseek | 5 | 4 | 4 | 1，量化 served latency 与 correctness guard |

配额结论：Top 5 全部来自当天动态发现；覆盖 inference-systems、models-agents、deepseek-radar、chips、papers-oss 五桶；五条都是可审阅的开源作者一手报告；固定雷达触发为 0。所有性能结果都保留 PR 作者报告标记，不替代独立复现或正式 release benchmark。

## 编辑主线

**性能 fast path 只有在它与真实 per-rank shape、并行拓扑和请求语义同时匹配时才成立；不匹配时，正确产品行为是受控回退或 fail-closed。** #36219 修正 DP worker 的 warmup shape；#49636 对 backend/capture/EP 设 config gate；#51292 在 TP 下关闭无法 bit-exact 的 fusion；#35505 在缺少 per-rank shared slot 的 EP 下拒绝 fusion。#4502 补出 API 返回值默认变更，说明调用边界也要被显式签名。

## 深挖题

1. `deep-shape-topology.md`：将 #36219 的 32,768/8,192 per-rank warmup、#49636 的 tokens/rank crossover 和 #35505 的 no-EP guard 比较，说明为何全局上限和局部 fast path 不能混用；写部署动作与证伪条件。
2. `deep-correctness-contract.md`：将 #51292 的 TP deterministic fallback、#4502 的 `return_lse` API 默认和 TensorRT-LLM #17955 的 fail-closed sampling 放在同一请求契约下，比较正确性、性能和兼容性成本。

## 落选

- TensorRT-LLM #17955：语义改动强，但无量化服务影响；作为框架/Agent 雷达和深挖证据，不占 Top。
- vLLM #53649：缺 GPU、batch、context 等复现实验条件，不能独立承载 33.6% headline。
- vLLM #52388：只有 microbenchmark，无端到端服务数据。
- 前两期已覆盖的 SGLang/vLLM/FlashInfer 事实，以及 DeepSeek 官方组织的安静窗口，不重复。
