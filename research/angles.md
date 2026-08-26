# 搜索角度轮换池

每次生成日报时从本文件取 6–8 个未用角度分配给各 scout（在各桶 prompt 里注入），用过的移到"已用"并注明日期。scout 也可以基于当日语境派生新角度，新角度用完追加回池子。目标是避免每天用同样的实体名搜索、看到同样的结果。

## 未用角度（反向问题与非实体问法）

本轮角度已全部分配；下一期需补充新的反向问题，避免重复实体搜索。

## 已用

- 2026-08-27 · chips：哪个新 GPU、互连或精度路径本周暴露出生成请求中未被峰值表格捕获的拥塞、兼容或损失？
- 2026-08-27 · infra-capital：哪个 AI 数据中心承诺本周因并网、租约、PUE 或设备交付获得或失去可验证约束？
- 2026-08-27 · models-agents：哪个 agent 或 runtime 本周让权限、恢复、队列或状态传播变成可测的契约？
- 2026-08-27 · inference-systems：哪种 fast path 本周因 priority、oversubscription、preemption 或 P99 而需要新增隔离？
- 2026-08-27 · papers-oss：哪个开源系统本周给出 request-level 或 cluster-level 的可复现性，而不只是 kernel 测量？
- 2026-08-27 · china-industry：哪个中国模型或 GPU 推理路径暴露出确定性、格式或运行时兼容性边界？
- 2026-08-27 · community：哪位维护者公开了带可行动数字的 CI 回滚、回归或部署事故？
- 2026-08-27 · deepseek-radar：DeepSeek 生态集成本周可见的负载形状或通信交换约束是什么？

- 2026-08-26 · chips：哪一项 scale-up / scale-out 互连或精度路径在本周被证明受形状、拓扑或数值门限限制？
- 2026-08-26 · infra-capital：哪个 AI 基建项目在本周从融资或容量承诺进入交付、用电或合同的可核验条件？
- 2026-08-26 · models-agents：哪个模型或 Agent API 本周新增了可复现的权限、兼容性、缓存或用量控制边界？
- 2026-08-26 · inference-systems：哪种投机、MoE 或 KV 优化本周需要显式 fallback、验证或资源上限才可部署？
- 2026-08-26 · papers-oss：哪项新开源实现把端到端时延、尾延迟和正确性放到同一个可运行实验中？
- 2026-08-26 · china-industry：哪一份中文一手材料揭示国产卡迁移中的具体算子、精度或运行时限制？
- 2026-08-26 · community：哪位维护者或部署者公开了可链接的回归、回滚或与宣传相反的复现数据？
- 2026-08-26 · deepseek-radar：DeepSeek 的第三方集成在本周新增了什么 shape、通信或 adapter 兼容性约束？

- 2026-08-25 · chips：谁把 NVFP4、MXFP4 或新互连的精度/带宽约束变成了可复现的部署回退？
- 2026-08-25 · infra-capital：哪份本周一手文件把 AI 数据中心的供电、交付或融资从承诺变成了硬约束？
- 2026-08-25 · models-agents：本周哪个模型或 Agent API 的输入、缓存、权限或计费边界变得可验证？
- 2026-08-25 · inference-systems：哪些推理优化在 P99、冷启动或长上下文时失效，维护者给出了什么证据？
- 2026-08-25 · papers-oss：新论文是否给出可运行代码、端到端测量和可反驳的硬件/负载边界？
- 2026-08-25 · china-industry：国产环境部署在本周出现了什么可复现的兼容性异常或性能分歧？
- 2026-08-25 · community：维护者或部署者本周公开了哪种回滚、事故、豁免或不可接受的权衡？
- 2026-08-25 · deepseek-radar：DeepSeek 相关 MoE、PD、DeepEP 或 3FS 集成在本周出现了什么实际变更或失败模式？

- 2026-08-24 · chips：量化（NVFP4/MXFP4/INT8）在真实负载下的精度损失本周有什么新复现？
- 2026-08-24 · infra-capital：哪些“上周的故事”本周出现了反例或续集？
- 2026-08-24 · models-agents：开源模型与闭源 API 的同任务成本差本周有什么新测量？
- 2026-08-24 · inference-systems：谁在把投机解码推到生产，正确率代价是什么？
- 2026-08-24 · papers-oss：算子库之间（FA/FlashInfer/TRT-LLM kernel）同一算子的实测差距本周有什么新数据？
- 2026-08-24 · china-industry：中文社区（知乎/V2EX/B站/公众号）本周在激烈争论什么与推理/芯片有关的议题？
- 2026-08-24 · community：长 context 的真实成本曲线本周有什么新测量？
- 2026-08-24 · deepseek-radar：prefill/decode 分离架构本周有什么新部署或新失败模式？

- 2026-08-23 · chips：HBM/先进封装供给本周有什么一手信号（订单、产能、良率）？
- 2026-08-23 · infra-capital：AI 数据中心并网/供电本周有什么监管或合同文件落地？
- 2026-08-23 · models-agents：agent 框架的权限/沙箱边界本周有什么新事故或新设计？
- 2026-08-23 · inference-systems：谁在解决 KV cache 搬运/卸载成本，本周有什么新证据？
- 2026-08-23 · papers-oss：MoE expert 负载不均衡本周有什么新解法或数据？
- 2026-08-23 · china-industry：国产 GPU 上跑大模型的实测（非厂商通稿）本周有什么新出现？
- 2026-08-23 · community：本周哪些推理部署事故/回滚被公开讨论了？
- 2026-08-23 · deepseek-radar：训练 infra（通信、容错、checkpoint）本周有什么开源新物？
