# 深挖：正确性契约——TP 回退、LSE 默认与 fail-closed 采样

## 发生了什么

2026-08-25 同日合入三条互不相关但同向的修复：vLLM #51292 在 TP>1 下对请求 batch invariance 显式回退 FlashInfer fused all-reduce+RMSNorm；FlashInfer #4502 把 SM120 attention 的 `return_lse` 默认从 True 改为 False；TensorRT-LLM #17955 让 speculative `SpecSampler` 在 admission 阶段拒绝非中性 `min_length`/`bad_words`/`no_repeat_ngram_size`/`embedding_bias`/`top_p_decay`。三者共同把"静默错算/静默丢字段"改为"显式拒绝或显式签名"。

## 数字与对比

| 维度 | #51292 修复前 | #51292 修复后 | #4502 旧默认 | #4502 新默认 | #17955 旧路径 | #17955 新路径 |
|---|---|---|---|---|---|---|
| 行为 | TP>1 fused 路径产生多 distinct 输出 | 请求 invariance 时回退 | `return_lse=True` | `return_lse=False` | 静默丢弃非中性采样约束 | admission 拒绝 |
| 正确性口径 | H100/Qwen2.5-7B/TP4/2k prompts×8：8 distinct bit-exact | 同条件：1 | 调用方隐式拿 `(out,lse)` | 必须显式传 `return_lse=True` | 约束被吞，输出仍返回 | 报错，不服务 |
| 性能（作者报告） | decode 7B 18,355 tok/s、70B 1,618 tok/s | 7B 7,450、70B 935；#50505 deterministic 1-stage 约 97% of fused | — | — | — | — |

#51292 的 97% 与 #4502 的 kernel 时延均为 PR 作者报告，无独立复现。

## 对部署/成本/能力意味着什么

- **TP 集群**：开 batch invariance 的服务方现在必须为 TP>1 接受约 0.6×–0.58× 的 decode 吞吐（7B/70B 作者报告），或改走 #50505 的 deterministic 1-stage 把损失压到约 3%。这是正确性从"概率相同"升级为"bit-exact"的直接代价；做 A/B、评测重放、安全审计的管线不能再依赖 fused fast path。
- **FlashInfer 调用方**：任何依赖 attention LSE 的下游必须在升级 #4502 后显式传 `return_lse=True`；新默认只返回 attention output，不应被解释为仍提供 LSE。调用方需要兼容性测试；不能从 PR 推断已发生静默错算。该默认变更是 API 契约，不是端到端性能结论。
- **TensorRT-LLM speculative**：使用 `min_length` 等约束的请求在 speculative 路径会从"被忽略但返回"变成"被拒绝"。调用方需在客户端做约束剥离或退回非 speculative 路径；否则 admission 失败率上升。

三条合起来定义了一条请求契约：**调用方必须显式声明正确性需求（invariance、LSE、采样约束），框架不再替调用方猜。**

## 什么证据会推翻它

- #51292：独立复现下 #50505 1-stage 在 TP>1 decode 的吞吐显著低于作者报告的 97%，或 bit-exact 在更长 prompt/更大 TP 下复现失败。
- #4502：若已发布下游仍假设默认返回 LSE，升级时的实际兼容性行为应由集成测试或 issue 核验；PR 本身没有报告事故或端到端影响。
- #17955：speculative 路径在拒绝非中性值后，实际 admission 失败率或回退非 speculative 的吞吐损失未被报告，需服务侧日志量化。

## 可信级与来源列表

- vLLM #51292：主线 PR 作者报告；吞吐与 97% 单一来源，未独立复现。https://github.com/vllm-project/vllm/pull/51292
- FlashInfer #4502：主线 PR 作者报告；kernel 时延单一来源。https://github.com/flashinfer-ai/flashinfer/pull/4502
- TensorRT-LLM #17955：主线语义修复；有参数化双向测试，无吞吐/事故数据。https://github.com/NVIDIA/TensorRT-LLM/pull/17955
- 与 dedup 对照：三条均未出现在 2026-08-24/25 已覆盖事实中，新事实陈述成立。
