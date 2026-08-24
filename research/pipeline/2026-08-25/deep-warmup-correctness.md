# 深挖：热路径速度、冷启动和 live-adapter 正确性是三道独立门

## 对比

| 变更 | 作者报告的 before / after | 不能省略的条件 |
|---|---|---|
| vLLM #53247 | Qwen3-1.7B bf16，decode kernel 相对 `torch.mm`：RTX 4090 D 0.254×→0.768×（3.02×），H20 0.212×→0.593×（2.79×）；但 persistent matmul specializations 3→43，engine 初始化 +14.8s。 | 19,200 点 sweep；配置只覆盖 Hopper/Ada 的五个 weight shape；未知架构/dtype 回退旧表。 |
| FlashInfer #4420 | RTX PRO 6000、rank 32、CUDA Graph replay、warm L2 的 12 形状 Qwen3-image sweep：相对 BF16 +112.4% 至 +193.3%，相对 FP8 +9.6% 至 +59.3%，fused 对比 unfused +24.2% 至 +211.2%。 | 算子延迟而非端到端；warm-cache，不报告首请求、模型吞吐或更多 GPU。 |
| vLLM #53361 | 两节点 Megatron GRPO 中，DeepSeek V4 merge=False LoRA 的 log-prob Pearson 从约 0.43→0.99705/0.9950，贴近 merge=True 的 0.99525/0.99440。 | 两个 step、单一 verl 流程；正确性信号，不是吞吐/成本结果。 |

## 判断

这三条不能被压缩成“量化/LoRA 更快”。#53247 的 3×是被确定性约束限定的 kernel 相对值，却以 14.8 秒一次性初始化为代价；#4420 证明融合可在热 L2、CUDA Graph 的算子范围降低时延，却没有证明冷请求或整模型获益；#53361 提醒更快的 live adapter 没有意义，若 weight mapping 让训练和 rollout 的数值语义分叉。它们是上线顺序，不是可相互替代的指标。

## 部署 / 成本含义

多租户弹性服务必须把一次性成本按 restart 频率、模型数和 cache 生命周期摊销。#53247 的 14.8 秒若每次 worker 重启均支付，会侵蚀只服务短会话的收益；#4420 需要用 cold/warm、graph/no-graph、形状分布分别记录，不能把 warm-L2 算子倍数写成 token 成本降幅；adapter 服务则要在性能 gate 之前运行 merge=False 与 merge=True 或离线参考的数值/任务等价测试。建议上线 gate 顺序为：**输出/训练语义正确 → cold TTFT 与初始化预算 → warm TTFT/TPOT/p99 → fleet 每瓦吞吐**。

## 证伪条件

1. 若 #53247 在含初始化的整机滚动重启、目标模型形状和生产 request mix 中没有正净收益，则不应启用更大的配置表。
2. 若 #4420 在 cold L2、无 CUDA Graph 或模型端到端回放中收益消失，说明它是特定热路径优化，不能用于成本预测。
3. 若更长的 GRPO、不同 LoRA rank 或真实 online adapter swap 重新出现 merge=False/merge=True 偏差，则 #53361 的两步相关性不足以证明 production parity。

来源：[vLLM #53247](https://github.com/vllm-project/vllm/pull/53247)；[FlashInfer #4420](https://github.com/flashinfer-ai/flashinfer/pull/4420)；[vLLM #53361](https://github.com/vllm-project/vllm/pull/53361)。
