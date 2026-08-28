# 2026-08-29 fallback discovery

## 采集状态

按 8/27、8/28 ledger 与 tracker 去重，完成 SGLang、vLLM、FlashInfer、TensorRT-LLM 的 8/28 merged-PR API 扫描与原文核验，并进行四组社区 issue 动态检索。两轮八桶 `intel-scout` 均超过一分钟无首个 assistant event，已停止；`pi auth check --model br/deepseek-v4-flash --json` 返回 `ready`，HTTP(S) proxy 均已继承。因此降级原因是模型首事件停滞，不是鉴权或代理缺失。

## 合格候选

| 候选 | 桶 | 一手证据与新事实 |
|---|---|---|
| SGLang #36094 | 推理与系统 | MI355X DeepSeek-V4-Pro DP attention 的 split-K capture-time heuristic，5 并发点服务 A/B 与 accuracy/unit test。 |
| SGLang #36657 | 芯片与供应链 | Blackwell MegaMoE whole-grid barrier 在 side stream 占 SM 时会 grid-sync timeout；reserve 2 SM 的 liveness/E2E 验证。 |
| vLLM #53333 | 推理与系统 | P/D NIXL async KV submission 后移至 forward launch 后，含两节点 GSM8K serving A/B。 |
| vLLM #54168 | 芯片与供应链 | B300 TP8 Kimi-K3 low-M tail 的 exposed critical chain 和 full-model evaluation。 |
| SGLang issue #36807 | 论文与开源 / 社区 | 具名公开复现：B200 上 k=2048/64×256K fast_topk_v2 静默错误 64/64 rows；含最小脚本与对照。 |

## 雷达与落选

- [SGLang #36738](https://github.com/sgl-project/sglang/pull/36738)：HiCache load-back/forward stream race 有明确机制但无稳定的数值复现；作控制面雷达。
- [SGLang #36583](https://github.com/sgl-project/sglang/pull/36583)：H200 KV pool size 修复的数字强，但已接近 8/28 的 allocation/address 主题，避免连续同一容量主题占 Top5。
- [vLLM #53409](https://github.com/vllm-project/vllm/pull/53409)：int32 activation offset 修复有 focused test，但没有服务影响；[vLLM #53141](https://github.com/vllm-project/vllm/pull/53141) 仅一个 Llama 70B steady-state 配置。
- [FlashInfer #4494](https://github.com/flashinfer-ai/flashinfer/pull/4494)、[TensorRT-LLM #17870](https://github.com/NVIDIA/TensorRT-LLM/pull/17870) 没有同配置服务 A/B；[TensorRT-LLM #17434](https://github.com/NVIDIA/TensorRT-LLM/pull/17434) 增加 RL endpoint HMAC auth，但没有可量化真实部署影响。
- [SGLang issue #36764](https://github.com/sgl-project/sglang/issues/36764)：发布镜像被报告多拉取 374.2MB（2.64%），有一分钟复现；因 reporter 未验证 `latest` 与当前 main 是同一 commit，不作 Top5 的确定变更。

所有 PR 数字均为作者报告；#36807 为社区报告，尚未有维护者修复或独立复现。
