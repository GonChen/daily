# 2026-08-27 选题卡

## 打分表

分值为 1–5。标准桶采用 source-policy 的六桶定义；所有数字均为 PR 作者报告。

| 候选 | 标准桶 | 新颖度 | 物质性 | 可验证性 | 准入判定 |
|---|---|---:|---:|---:|---|
| SGLang #36456 | 芯片与供应链 | 5.0 | 5.0 | 5.0 | 入选：sanitizer 66→0、coredump 3→0；吞吐为噪声。GPQA 0.0 是 coredump 令评测无法完成，非能力基线。 |
| vLLM #52914 | 推理与系统 | 4.5 | 5.0 | 4.5 | 入选：device-idle 契约与生产报告；3.40s A/B，不缩短 burst。 |
| SGLang #35343 | 推理与系统 | 4.5 | 4.0 | 5.0 | 入选：20/20→0/20 tactic 分歧；收益降格为稳定性，cold tuning 79→106s。 |
| FlashInfer #4030 | 论文与开源 | 4.0 | 4.0 | 4.0 | 入选：shape/scratch gate 与量化 GPU-time；同 PR 作者 vLLM kernel 基线，非整服务。 |
| FlashInfer #4728 | 论文与开源 | 3.5 | 3.5 | 5.0 | 入选：29-shape/frozen baseline；CUPTI GPU-time 非端到端。 |

## Top 5

| 顺位 | 事实 | 桶 | 证据和编辑判断 |
|---:|---|---|---|
| 1 | SGLang #36456 Hopper MXFP4 MoE scale 越界读修复 | 芯片与供应链 | 从 66 sanitizer errors、3 coredumps 到 0，且性能中性；GPQA 0.0 为修复前 coredump 令评测无法完成，非能力基线。 |
| 2 | vLLM #52914 DP pause completion device barrier | 推理与系统 | 控制面“完成”与 device idle 不一致可造成 weight-sync race；复现、A/B probe 和不缩短 burst 的限制完整。 |
| 3 | SGLang #35343 TP autotune consensus | 推理与系统 | 20/20 的 rank 分歧变成 0/20，性能收益应降格为稳定性收益，并明确 27s cold-start 成本。 |
| 4 | FlashInfer #4030 SM12x MSA indexer | 论文与开源 | 基线为同 PR 作者 vLLM kernel，非整服务吞吐；batch128 端到端 ratio 1.00–1.03。 |
| 5 | FlashInfer #4728 KDA M128 eager prefill | 论文与开源 | 29-shape、四 GPU、同进程 frozen baseline；CUPTI GPU-time 非 end-to-end，vs frozen #4605 仅 1.018×–1.045%。 |

所有性能、精度和事故数字均为合入 PR 作者报告，尚无独立复现。Top 5 覆盖 3 个标准桶，且全部为维护者公开 PR；社区一手口径含 PR 作者报告，#52914 另含具名生产报告。未将版本发布、无量化回滚或 kernel-only `eh_proj` sweep 填入 Top 5。

## 深挖任务

1. **完成语义是一条 barrier，还是一个状态位？** 比较 [vLLM #52914](https://github.com/vllm-project/vllm/pull/52914)、[SGLang #35343](https://github.com/sgl-project/sglang/pull/35343) 和 [TensorRT-LLM #18092](https://github.com/NVIDIA/TensorRT-LLM/pull/18092)；输出线上控制面应保证的顺序和可观测信号。
2. **性能 fast path 的边界如何被编码？** 比较 [SGLang #36456](https://github.com/sgl-project/sglang/pull/36456)、[SGLang #30859](https://github.com/sgl-project/sglang/pull/30859)、[FlashInfer #4030](https://github.com/flashinfer-ai/flashinfer/pull/4030) 和 [FlashInfer #4728](https://github.com/flashinfer-ai/flashinfer/pull/4728)；输出准入、fallback、测试与指标要求。

## 落选者与理由

- SGLang #36233：CUDA 13.4 developer-preview/Rubin 容器，预期 FlashInfer JIT startup 变长；没有可比较服务测量。
- vLLM #53942：Kimi K3 `eh_proj` 仅 CUDA Graph kernel sweep，未给端到端或 request-level 影响。
- TensorRT-LLM #18262：MiniMax-M3 MSA reuse 回滚只有 IMA 描述；无 GPU runtime test 或影响量化。
- TensorRT-LLM #18140、vLLM #53838：读取范围内无完整、可比较 workload 与结果，不以标题升格。
- DeepSeek 组织、芯片资本、模型/Agent 产品、中文产业和论文窗口：没有窗口内、可量化的一手新增事实，保持安静。

## Executive readout 论点草稿

#36456、#4030 与 #4728 先将地址、shape、scratch、state 和 CUDA Graph 编码成准入或回退；#52914、#35343 与 #18092 再将局部“完成”升级为跨 worker/rank 的证明。收益只在这些前提成立时发生；生产上应计量 legality、fallback、barrier 与 cold-start 的全链路成本。

## 30 秒结论

- Hopper MXFP4 的非整齐 K tile 可在末 expert 越界；#36456 将 sanitizer 66→0、coredump 3→0，吞吐中性。
- vLLM pause resolve 必须等 device idle；DP 的 3.40s dummy burst 不是已完成状态。
- TP autotune 的主要改进是 tactic 一致性（20/20→0/20），不是可外推的吞吐提升。
- FlashInfer #4030/#4728 的数字受 GPU、shape、cache 与 API 口径约束；不等于通用 serving 速度。
- DeepSeek、芯片资本、中文产业和论文窗口无合格新增一手事实。

## KPI

**Top5 新颖度均值 4.30；标准桶覆盖数 3；社区一手来源 5（口径含开源 PR 作者报告）；落选候选数 5；degraded：是，八桶 scout 两轮均无首个模型事件。**
