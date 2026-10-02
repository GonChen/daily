# 2026-10-03 papers-oss 桶候选

## 1. Periodic Weak Spots: Phase Sensitivity from Chunked KV-Cache Compression（arXiv:2609.36322，9/28）
- 类型：论文（65 页 preprint，自训模型族，无公开代码）｜事实：分块 KV 压缩在 token 位置之外引入"相位"坐标（token 相对压缩窗口边界的位置）。同信息在某相位易检索、另一相位系统性失败：**带分块压缩的开源大模型长上下文检索精度跨相位可差 40 个百分点，平均分基准完全掩盖该周期性弱点**；作者从零预训练一族 transformer、覆盖多种 KV 压缩设计，相位敏感性全部复现；因果干预显示不同注意力组件对不同源相位贡献不对称。
- 启示：任何带 chunked 压缩的推理栈做长上下文评测必须按压缩相位扫描；"平均精度高"与"存在系统性位置性失败"可共存。
- 来源：https://arxiv.org/abs/2609.36322
- 新事实：首次给出"压缩窗口相位"这一失效维度，直接打击"平均分评测"惯例。

## 2. How Divergence Becomes Decision Flips in Compressed Language Models（arXiv:2610.00694，9/30）
- 类型：论文+大规模评测工件｜事实：压缩质量报告惯用 KL 散度——作者证明其失效：**argmax 翻转率与总变差（TV）以中位数 1.05 比例直接对应（无拟合常数），KL 只能经不稳定因子间接关联**；两个翻转率差 ≥10% 的压缩器，KL 在 11% 配对中把更小散度判给翻转更多决策者（TV 仅 1%）。实验：802 个压缩副本 × 19 模型 × 5 语料 × 9 类扰动；预注册边界：held-out 代码语料上 TV 比例全模型成立、KL 三条预测对半数模型失败。应用：vLLM 投机解码中 teacher-forcing TV 预测 greedy draft 接受率平均相对误差 1.1-2.4%，无需任务特定校准。
- 启示：压缩上线验收改报 TV/翻转率而非 KL；投机解码可用 TV 做免校准接受率先验。
- 来源：https://arxiv.org/abs/2610.00694
- 新事实：攻击"KL 报告惯例"这一评测方法论本身 + 免校准 TV→接受率通道。

## 3. STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization（arXiv:2609.38169，9/29）
- 类型：论文+代码+SGLang 集成｜事实：**失效条件：对 Delta-rule 循环状态直接低位宽量化会严重掉精度（量化误差经后续状态更新传播放大）**。误差沿时间维（长寿命记忆跨解码步存续）与空间维（状态幅值沿行/列剧烈变化）分解；对策为时空 PTQ：按误差量级与记忆寿命分配精度、联合拟合 key 行/value 列 scale。Qwen3.8-27B 与 Kimi-Linear-48B-A3B 上 6-bit 拟合 FP32-state 精度、4-bit 配置胜过均匀 INT8；集成 SGLang+优化 kernel 后状态压缩 >5×、服务总内存最高降 68.7%（作者报告）。
- 启示：跑 Delta-rule/线性注意力模型不必强守 FP32 状态，但均匀量化是死路——需按行/列/时间异构分配位宽；SGLang 已有可运行路径。
- 来源：https://arxiv.org/abs/2609.38169 ；https://github.com/Dreamer-Toby/STEPQuant
- 新事实：把循环状态本身确立为独立量化对象 + 误差时空归因 + 可运行工件。

## 4. Recovering Off-Policy Supervision for Speculative Decoding（ALR-IRA，arXiv:2609.38795，9/30）
- 类型：论文+代码｜事实：**失效条件：块投机解码普遍在"外部模型写的 off-policy 语料"上训练，块内单个 off-policy token 即使其后所有槽位监督信号全部失效**；现有"丢弃分歧槽位"做法造成系统性监督损失。对策：Anchor-Label Relabelling 用 greedy target rollout 重标注语料 + In-Rollout Anchors 复用特征。数字：greedy 接受长度比 DFlash 最高 +36.5%；单 epoch 胜过最优 erase 调度；3 epoch 追平"target 重生成语料"上限（作者报告）。
- 启示：自训 draft 团队在固定语料上训练时，"丢弃分歧槽位"默认清洗是精度损失源；重标注是近零额外 target 开销的修法。
- 来源：https://arxiv.org/abs/2609.38795 ；https://github.com/js-lee-AI/ALR-IRA
- 新事实：首次量化训练数据侧的监督失效条件（与已报解码侧改进正交）。

## 理论负结果（无代码，选型参考）
Efficiently Approximating Attention Is Hard（arXiv:2609.37261，9/29）：标准复杂度假设下，不存在真正亚二次算法能对 softmax attention 给出任意非平凡的一致（全输入均匀）加性/相对近似保证，即使允许多项式预处理；"识别稀疏注意力下承载大部分注意力的少量 key"同样不可能高效完成。启示：一切稀疏注意力有效性保证必然依赖输入结构假设，"uniform worst-case"话术可从采购评估中剔除。
