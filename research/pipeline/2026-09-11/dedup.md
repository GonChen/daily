# 2026-09-11 去重基线

## 最近两期已覆盖

- **2026-08-29：**MI355X DSV4 split-K、Blackwell MegaMoE SM reserve liveness、vLLM async KV post-forward、B300 Kimi-K3 low-M tail、SGLang fast-topk 长 row 静默错选。
- **2026-08-30：**ROCm GLM-5.2 PD fused top-k gate、AITER EAGLE eager metadata、FlashInfer Cake Blackwell all-gather、Codex 0.151 MCP/sandbox、MiMo audio DP collective 社区事故。

## 本期不得原样重复

- 只有新 release、独立复现、修复合入、不同硬件/模型/拓扑的可量化 A/B 或明确的维护者确认，才可回访上述主题。
- 不把普通版本递增、纯代码整理、无端到端影响的 kernel microbenchmark 或旧社区问题再次列入 Top5。

## 本期优先检查

- 2026-09-08 至 09-11 的官方 release、合入 PR、模型/产品可用性、监管或公司一手披露。
- 长上下文、KV/PD、MoE、speculative 与异构 GPU 路径是否新增 correctness/liveness 或 serving 指标。
- 具名社区是否提供可复现的部署事故、回归或对官方性能主张的反例。
- DeepSeek 官方组织和主要框架是否新增模型、内核、分布式或评测资产。
