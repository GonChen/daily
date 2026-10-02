# 2026-10-03 deep-01：昇腾 950 的"同日批次"——官方栈双后端化与可复现边界

问题：9/30 DeepSeek 官方内核库出现协调的昇腾使能批次；叠加第三方兼容矩阵与招标订单，国产算力从"口径"进入"可复现工件"阶段。

| 组件 | NVIDIA 侧 | Ascend 侧（9/30 批次） | 复现条件 |
|---|---|---|---|
| FlashMLA | 砍掉 Hopper 与 V3/V3.2/V4.0，KV 格式破坏性变更，仅保 Blackwell + V4.1 | 稀疏注意力 prefill 410 TFLOPS（95% 峰值）、decode 360 TFLOPS（83%），作者报告 | 昇腾 950 NPU + CANN 9.2.0+；旧平台钉 `ba89a34` |
| TileKernels | SM90/SM100 + CUDA 13.1+ | 同一 Python API 运行时自动选后端（MoE 路由、Engram 门控、mHC/Sinkhorn、FP8/FP4+fused SwiGLU、RoPE） | "全部算子已用于内部训练与推理"（口径） |
| DeepSelect | 对 torch.topk 提速 2–20× | 昇腾 NPU TopK 内核（V3.2/V4/V4.1 indexer 与采样场景） | 源码可复跑 |
| vLLM-Ascend v0.27.1rc1（9/24，第三方） | — | DeepSeek-V4-Flash 仅限 950DT：W4A8C8、两节点 1P1D DSpark + KV Cache Pool、DSA-CP；MiniMax-M3 上 A3/950DT（W8A8C8）；**明示 Atlas 800 A2 不在验证范围** | release 附部署指南，可独立复测 |
| 交付侧信号 | — | 壁仞 1.74 亿元智算中心独家中标（9/23 定标：评分 89.71、45 天供货、27.98 万/台起）；H1 营收 12.36 亿元（+1997.6%） | 招标文件级可核算 |

三条旁证与一个限定：
1. **供应范围**：媒体报道下一代昇腾 900 系列仅面向中国市场（9/24，中等置信，待华为直接声明确认）——产能全部留给内部交付，可交付量估算剔除海外变量。
2. **W4A8C8/W8A8C8 是本期最硬的可复现锚点**：第三方框架给出量化方案与两节点拓扑，意味着外界可第一次按公开配置独立复测 950DT 的吞吐与精度，检验华为口径。
3. **老代际被主动放弃**：FlashMLA 砍 Hopper、vLLM-Ascend 排除 A2——两个生态同时收窄支持面，向 Blackwell + Ascend 950 双头收敛。
4. 限定与证伪：Ascend 侧数字目前均为官方/作者报告，尚无第三方 serving 复测；"同日批次"中部分仓库初始开源日期可能早于窗口。若 CANN 9.2 环境下的独立复测达不到 FlashMLA 报告的 95%/83% 峰值，或 vLLM-Ascend 矩阵在两节点 1P1D 下复现失败，则"可复现化"叙事收窄为"接口可用"。来源：bucket 文件 deepseek-radar.md、inference-systems.md、china-industry.md、chips.md。
