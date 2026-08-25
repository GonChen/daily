# 深挖：per-rank shape、并行拓扑与 fast path 的不可混用

## 发生了什么

2026-08-25 同日合入三条都触及"全局上限 vs 局部 fast path"边界的修复：SGLang #36219 修正 DP prefill 的 EXTEND warmup shape；vLLM #49636 为 DeepSeek V4 的 FlashInfer MoE-EP backend 加 runtime config gate；SGLang #35505 在缺少 per-rank shared expert slot 的 EP 拓扑下直接拒绝 fusion。三者共同结论：fast path 的正确性前提是它看到的 shape、并行度与请求语义必须与真实 per-rank 状态一致；不一致时正确产品行为是 fail-closed 或受控回退，而不是用全局上限静默继续。

## 数字与对比

| 维度 | #36219 warmup shape | #49636 EP backend gate | #35505 no-EP guard |
|---|---|---|---|
| 错配形态 | DP 全局 32768 token 被当作单 rank buffer | backend/capture/EPLB/NVSHMEM 未显式约束 | EP 无 per-rank shared slot 仍走 fusion |
| 修正 | 改为每 rank 8192 token buffer，补 PD prefill 与 text-only wrapper | `moe_backend` runtime 开关 + SM100/NVSHMEM/EPLB/capture 显式约束 | EP 不提供 shared slot 时拒绝 fusion，避免静默错算 |
| 拓扑/硬件 | Qwen3.5-397B-A17B-NVFP4、GB300、DEP4 prefill+DEP4 decode | vLLM 0.25.1、1×8 B200、TP8+EP8 | GB200 TP4、1024in/512out |
| 性能（作者报告） | TPS/chip C4–C64 +4.940%–6.767%；C128 +3.662% 因 CV 3.954% > 1% 门槛排除 | V4-Flash 1.049×–1.199×、V4-Pro 1.170×–1.305×（HTTP serving，pre-SP stack） | QPS1/4/8 TTFT −13.4%/−14.0%/−21.0%，QPS4 p99 ITL −52.6% |
| 正确性 guard | GSM8K 200 题 0.985、零 retract/error | GSM8K 200 题 Flash 0.965×3、Pro 0.880/0.880/0.890 | GSM8K 与 AIME25 与 baseline 相近；主 CI 仍有失败标记 |

## 对部署/成本/能力意味着什么

1. **warmup shape 必须按 per-rank 重新校准，不能继承全局上限。** #36219 表明 DP 全局 32768/局部 8192 的配置下，旧路径用全局值预热会得到错误的 autotune 状态；修正后 C4–C64 每芯片 TPS +5%–7%。部署方在 DP>1 且全局/局部 chunk 不等时必须重新跑 warmup，否则 fast path 在低并发段直接损失 5% 量级吞吐。
2. **MoE-EP fast path 是 opt-in 且受拓扑约束，不是默认开启。** #49636 把 `fi_dg`/`fi_cutedsl` 拆成两个 runtime `moe_backend`，并对 SM100、NVSHMEM、EPLB、capture 做显式约束。部署方升级 vLLM 0.25.1 后必须显式设置 `moe_backend` 并核对 SM100/EP8/NVSHMEM 前置条件，否则不会拿到 1.05×–1.30× 吞吐；吞吐数字受 accuracy gate 限制（Flash 0.965、Pro 0.880–0.890），不能单独引用 headline。
3. **shared-expert fusion 在 EP 下必须 fail-closed。** #35505 把 shared expert 放入 slot 256 同 kernel/stream 执行，省约 4 次 launch 与 2 次 sync；但 EP 不提供 per-rank shared slot 时直接拒绝 fusion。部署方在 EP 拓扑下不能假设 fusion 一定生效，需在容量规划里把"EP 下回退到非 fusion 路径"作为基线，把 TP4 的 TTFT/ITL 改善当作条件性收益。
4. **跨拓扑外推不成立。** 三条的数字都绑定具体硬件/并行度：GB300 DEP4、B200 TP8+EP8、GB200 TP4。把任一数字外推到其他卡或 EP>1 拓扑属于推断，必须重新测量。

## 什么证据会推翻它

- #36219：独立复现若在 C4–C64 段测得 TPS/chip 增益 <1% 或 CV 持续 >1%，则 warmup shape 修正的部署意义被削弱；C128 段已被作者自己按 CV 门槛排除，独立复现需确认该排除合理。
- #49636：独立 HTTP serving 若在 sequence-parallel stack 上测得 Flash/Pro 吞吐增益 <1.05× 或 accuracy 跌破 0.95，则 opt-in backend 的净收益不成立；SM100 之外的卡若能跑通也说明约束过紧。
- #35505：独立复现若在 EP 下仍能正确执行 fusion（即存在 per-rank shared slot 的实现路径），则 no-EP guard 是过度保守；若 TP4 之外测不到 TTFT/ITL 改善，则 fusion 收益仅限 GB200 TP4。
- 三者共同证伪条件：若后续 release 把这些 guard 默认开启且无 accuracy 回归，说明 fail-closed 是正确基线；反之若出现静默错算事故，说明 guard 仍不完整。

## 可信级与来源列表

- 可信级：三条均为主线 PR 作者报告，无独立复现；#36219 与 #35505 的 C128/CI 失败标记由作者自报，#49636 的吞吐受 accuracy gate 限制。跨拓扑外推标"推断"。
- 来源：
  - [SGLang #36219](https://github.com/sgl-project/sglang/pull/36219)
  - [vLLM #49636](https://github.com/vllm-project/vllm/pull/49636)
  - [SGLang #35505](https://github.com/sgl-project/sglang/pull/35505)
- 去重对照：dedup.md 列出的最近两期事实不含这三条；本选题的新事实陈述成立。
