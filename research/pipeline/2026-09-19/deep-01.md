# 2026-09-19 deep-01：满载悬崖与"被回退的优化周"

问题：本周四条独立证据共同指向一个模式——kernel 级收益在真实服务条件下被什么杀死？

| 优化 | 宣称收益 | 真实代价 / 失效条件 | 本周处置 |
|---|---|---|---|
| vLLM CUDA graph 捕获阶梯 #57355 | 默认按 8 倍数捕获 | `max_num_seqs` 非 8 倍数时满载正好落在 PIECEWISE 慢路径；过载服务器稳定跑在 max_num_seqs 并发 → 吞吐随运行衰减 2,922→829 tok/s | 修复后 batch 97 1,523→3,876.85 tok/s（2.55×）；投机解码场景未覆盖 |
| SGLang FlashInfer MoE fused finalize #40105 | 融合 finalize 省短 kernel | 数值精度优先：W4A4 1-token 延迟 +21.75%、16k tokens +12.55%；精度测试"Not run" | 默认 True→False 预防性翻转；可用 env 显式开回 |
| SGLang MI355X GLM-5.2 TopK v2 #40148 | 新 top-k kernel | serving P90 交互性比 HIP Top-K 差 10.0%（吞吐仅 −0.15% 代价） | 官方配方正式撤回，回退默认 |
| vLLM 0.26→0.29 升级 #57680（社区） | 大版本升级 | H100 吞吐 ~1295→~362 tok/s（3.3×恶化），疑似 `aten::copy_` 路径 5× 劣化 | 孤证、无维护者定性，A/B 配置公开 |
| vLLM KV offload 阈值 #57555/#57342 | H100 PCIe 调好的常数 | A30 上 DMA 路径慢 2.4–3.8×（按 page 选路径却按碎片拷贝） | 贡献者提议设备端自适应阈值 |
| llama.cpp sm_75 FA 32-token Q-tile #28761 | 固定 tile cap 护栏 | DKQ=128 时 cap 次优（+3.6% 可得）；DKQ=256 短 KV −37%/长 KV +19–50%，双向伤害 | 基准 + ptxas 寄存器溢出证据公开 |
| Pareto Atlas（arXiv:2609.17863） | 54 配置校准 | 朴素 FP8 KV cache 200 题 0% 正确；n-gram 投机 0.90–0.98× 无收益；AWQ 4-bit 压破质量线 | 负结果公开发表为锚点 |

共性结论：
1. **触发位置比形状本身重要**：#57355 的悬崖只在"满载"触发——性能测试常用的饱和 benchmark 恰好是生产事故形态，而常规 CI 看不到（非满载时无明显异常）。
2. **收益归属层错位**：kernel 层 +21% 可以是 serving P90 −10%；上传层收益（DMA/Triton 阈值）在另一张卡上是反优化。
3. **"先关后证"成为可接受的默认**：#40105 在无精度数据时翻转默认值——维护者用可得性偏差反向操作（宁可损失 10–22% 已知延迟，避免未知精度风险），代价表公开让部署方自行选择。
4. 证伪条件：若 #57355 修复在投机解码开启场景引入新悬崖，或 #57680 被证为 CC-VM 环境特有，则"回退潮"叙事需要收窄为"个别误配置"。

来源：bucket 文件 inference-systems.md、community.md、papers-oss.md 所列 PR/issue/arXiv 链接。
