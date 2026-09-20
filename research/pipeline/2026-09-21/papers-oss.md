# 2026-09-21 papers-oss 桶候选

4 篇候选均确认 v1 时间戳（9/16 晚–9/17 提交，9/18–9/21 公告期）。数字均为作者报告，未独立复现。

## 1. SProbe: Syndrome Decoding for Silent Data Corruption in Quantized Integer GPU Arithmetic（arXiv:2609.19743）
- 日期：2026-09-17 提交｜类型：论文（系统容错 × 量化推理，H100 实测）
- 事实：GPU tensor core INT32 累加器无 parity/ECC，瞬态故障产生"合法但错误"的整数且不触发中断。SProbe 在 vendor GEMM 输出后挂校验 kernel：Freivalds 门（61-bit 素域 3 个独立求值点）漏检率 ≤2^-141；触发后三素数幂和综合征 + Reed-Solomon 链定位每行至多 4 个碰撞错误的列与精确幅值，可就地修复或重算。H100 上 7 类注入故障 × 4 种矩阵规模全检出，包括 TR-ABFT 构造性检不出的模式、加权网格码检得出但修不了的模式；明确"无权行列校验和对双轴抵消错误构造性盲"；所有测试配置下重算快于就地修复（恢复成本由诊断主导）；门开销为 cuBLASLt GEMM 的 49%（N=16384）/11%（N=65536）；INT8 医疗 LLM 消除全部观测静默损坏，代价 30% 吞吐；作者还报告了自己校验器的缺陷。
- 启示：为量化推理部署提供"哪些校验方案在何种错误模式下必然失效"的可引用锚点；30% 吞吐给出 INT8 生产保护成本上界。
- 来源：https://arxiv.org/abs/2609.19743
- 新事实：GPU 整数算路静默损坏方向首次覆盖；ABFT 盲区/重算优于修复/诊断主导成本三个失效条件成为可引用负结果清单。

## 2. DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression（arXiv:2609.19969）
- 日期：2026-09-17 提交｜类型：模型+技术报告（权重已开源）
- 事实：552B backbone 多模态 MoE，1M token 上下文；CED 架构 decode 激活 16B/prefill 仅激活 8B。KV 压缩组合：CSA2 跨层 KV 复用 + FP4 KV cache。45T token 预训练。HBM 常驻全局 KV 890 bytes/token（约为 DeepSeek-V4-Flash 的 1/4）；SWA Bounded Replay 将 SSD/主存侧持久 KV 降至约 1/8；性能"显著优于基线"（作者报告）。checkpoint 在 HF 发布。
- 启示：与上期已报 Pareto Atlas（含"FP8 KV 全错"负结果）形成直接张力——同窗口一线实验室把 KV 压到 FP4 上生产，说明 Atlas 的 FP8-KV 负结果是栈特定的；后续 KV 量化结论必须绑定具体注意力结构。
- 来源：https://arxiv.org/abs/2609.19969 ；https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash
- 新事实：FP4 KV 从论文主张变成可下载的生产级锚点（890 B/token），并反向限定已报 FP8-KV 负结果的适用范围。

## 3. PreDE: Predict Before You Deploy（arXiv:2609.19441）
- 日期：2026-09-16 提交｜类型：论文+开源代码（量化失效预测，机器人 WAM）
- 事实：对视频生成骨干 WAM 量化时，用小型开发集闭环校准两个阈值，之后仅凭离线动作偏差对新量化配置给接受/拒绝/搁置三值决策。负结果锚点：5 个 WAM × 4 基准上，量化任务损失既不能由位宽单独解释、也不存在跨策略共享的偏差阈值；28 个 held-out 配置 21 个在闭环前出判（75%）且全部与实测一致，被搁置候选里既有可接受的也有 33 个百分点损失的；450 次 Franka Research 3 真机试验：开环高偏差组全部显著退化、低偏差组无显著退化；W4A4 真机 1.37× 动作查询加速、峰值内存 −44%。代码开源。
- 启示：把"量化何时伤任务"从逐配置闭环转为离线校准；"无共享阈值、必须按策略校准"是后续量化部署论文可直接引用的前提。
- 来源：https://arxiv.org/abs/2609.19441 ；https://github.com/jiuyixu25/PreDE
- 新事实：首次给出"位宽单变量解释失败 + 跨策略无共享阈值"的可引用负锚点 + 真机验证与开源实现。

## 4. On-Demand Attention (ODA): Language Models Know When to Recall（arXiv:2609.20734）
- 日期：2026-09-17 提交｜类型：论文+系统实现（稀疏注意力/KV 复用，vLLM 集成）
- 事实：预训练模型解码态已包含"本次全局读取对下一 token 是否有益"的可预测信息；训轻量 recall head（不动预训练权重、保留完整历史 KV），在 vLLM 做 GPU 侧条件执行按需唤醒全局注意力。Qwen/Gemma（含混合注意力骨干）上，局部注意力质量损失大部分被选择性召回恢复，全局读取量大幅下降，长上下文解码相对全注意力有实际加速（摘要未给具体倍数）。失效条件：门控质量决定上限；失败可回退全注意力。
- 启示：稀疏注意力收益判定从"离线曲线"转为运行时自门控；本窗口唯一带 vLLM 条件执行实现。
- 来源：https://arxiv.org/abs/2609.20734
- 新事实：运行时自门控稀疏注意力 + vLLM 落地路径。

## 备查
Zarya（2609.19868，AR+掩码扩散混合，0.6B/1.7B/4B 权重已放出，解决 MDM 不能复用 KV cache）；D-Quant（2609.19880，熵编码 KV 量化，无数字无代码）。
