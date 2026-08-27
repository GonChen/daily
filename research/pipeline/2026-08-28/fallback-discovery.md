# 2026-08-28 fallback discovery

## 采集状态

已按 8/26、8/27 ledger 和 tracker 去重，并轮换八个新反向问题。`intel-scout` 使用 `br/deepseek-v4-flash` 分两轮启动；每轮八线程在超过一分钟后均无首个 assistant event，已停止，未进行第三次启动。`pi auth check --model br/deepseek-v4-flash --json` 返回 `ready`，进程可见 `HTTP_PROXY`、`HTTPS_PROXY`、`http_proxy`、`https_proxy`，所以这是模型首事件停滞，不是认证或系统代理变量缺失。

主控降级为一手 GitHub API 检索：SGLang、vLLM、FlashInfer、TensorRT-LLM 的 closed/merged PR 列表均以 `merged_at >= 2026-08-27T00:00:00Z` 筛选，再读取入选 PR 正文。四组动态检索覆盖新芯片/异构平台、DeepSeek 集成、推理 fast path、MoE/JIT cold start 和服务语义；DeepSeek 官方组织及产业/资本、模型产品、论文检索没有同时满足日期窗口、第一方来源和可量化影响的新增事实，安静处理。

## 合格候选

| 候选 | 一手证据 | 为什么候选 |
|---|---|---|
| SGLang #35634 DeepEPv2 | [PR](https://github.com/sgl-project/sglang/pull/35634) | DeepSeek V4 TP8/DP8/EP8 的 capacity/fail-fast contract，且有 H20/B200 单节点与 2×H20×8 结果。 |
| SGLang #36330 gfx950 MTP attention | [PR](https://github.com/sgl-project/sglang/pull/36330) | MI355X、70k context、TP2 的 kernel 与服务 A/B，明确出现 C16 TPOT 回归。 |
| SGLang #36541 AITER int32 KV wrap | [PR](https://github.com/sgl-project/sglang/pull/36541) | 2 GiB 边界、可重复 NaN 和端到端恢复数据完整；风险是部分 CI 仍失败。 |
| FlashInfer #4789 arch-filtered manifest | [PR](https://github.com/flashinfer-ai/flashinfer/pull/4789) | B200 CUDA 13 cold JIT 1,175.7→226.4 秒，并写出持久 tactic 失效边界。 |
| TensorRT-LLM #17985 hybrid NVFP4 KV | [PR](https://github.com/NVIDIA/TensorRT-LLM/pull/17985) | GB300 AgentX 3,600 秒服务 A/B，并将 staged route 的形状和 graph 条件明确化。 |

## 雷达与落选

- [vLLM #53685](https://github.com/vllm-project/vllm/pull/53685)：DeepSeek V4 Flash、TP4/EP4、1,024/128 random 64 requests 的作者 A/B 仅 +1.40% output tok/s；与 #35634 的 DeepSeek/MoE 主线重叠，不升格。
- [vLLM #54088](https://github.com/vllm-project/vllm/pull/54088)：H200 CUDA Graph GEMM microbenchmark 为 36 个 M=1/2 shape、几何均值 1.28×；没有服务结果。
- [vLLM #54012](https://github.com/vllm-project/vllm/pull/54012)：native CP MLA 的完整 DeepSWE run 有价值，但正文未给出相同配置的服务 A/B。
- [FlashInfer #4442](https://github.com/flashinfer-ai/flashinfer/pull/4442)：CUB top-k claim 指向外部 gist，且依赖未合入的 CCCL PR；不作为稳定事实。
- [TensorRT-LLM #17862](https://github.com/NVIDIA/TensorRT-LLM/pull/17862)：KDA prefill 优化仍是 draft，GPU parity pending；[ #17887](https://github.com/NVIDIA/TensorRT-LLM/pull/17887) 具测试但没有服务量化。

所有性能数据均为 PR 作者报告，未独立复现。
