# 2026-08-30 去重基线

## 最近两期已覆盖

- **2026-08-28：**SGLang DeepEPv2 ElasticBuffer 容量/graph 准入、MI355X Qwen3.5 MTP attention、AITER 2 GiB int32 KV 地址回绕、FlashInfer trtllm-gen manifest 冷编译、TensorRT-LLM MiniMax-M3 混合 NVFP4 KV。
- **2026-08-29：**SGLang MI355X DSV4 split-K、Blackwell MegaMoE SM reserve liveness、vLLM post-forward async KV、B300 Kimi-K3 low-M tail、SGLang `fast_topk_v2` 4,096-candidate 静默错选社区复现。

## 本期不得原样重复的事实

- 不重述上述 PR 的原有 benchmark；只有新合入修复、独立复现、CI 结果、release 或明确的新部署边界才能回访。
- 不将相同的 AMD decode、Blackwell MegaMoE、P/D KV overlap、low-M tail 或长 row top-k 再作为 Top 5，除非有不同模型/硬件/故障模式的新增一手证据。
- 对 DeepSeek V4、Kimi K3、Qwen3.5 的普通集成提交，只有新模型资产、数值/性能 A/B、拓扑限制或正式发布才计入候选。

## 本期优先检查

- 新硬件/容器/互连路径是否给出可量化的服务约束，而不是仅增加架构名称。
- 资源隔离、异步搬运、MoE/MLA 与 speculative 路径是否出现新的 correctness、liveness 或 P99 证据。
- Agent/API 的权限、恢复、流式协议或价格是否出现可部署的正式变化。
- 社区是否出现具名、可链接、能反驳的事故或复现；DeepSeek 官方组织是否有实际 release、模型卡或工程变化。
