# 2026-10-03 deep-02：支持面收窄的代价清单

问题：本期多笔官方动作共同收窄"什么还能用"；每一次收窄都把迁移成本转嫁给部署方。

| 收窄动作 | 砍掉了什么 | 直接代价 | 迁移动作 |
|---|---|---|---|
| FlashMLA 2026.09.30 | Hopper 全系 + V3/V3.2/V4.0 + 旧 KV 格式 | H100/H200 MLA 服务与 V3 系必须钉旧 commit `ba89a34`；升级前重建 KV cache；基于 FlashMLA 的旧性能对比全部只对旧 commit 成立 | 迁移前盘点模型代际与 KV 格式；新格式做精度回归 |
| TRT-LLM rc28 Known Issues | PD 分离与低精度组合的隐含承诺 | **重叠 TinyLlama PD serving 可能返回同批次另一 prompt 的内容（跨请求数据错乱）**——多租户红线；NVFP4 KV 初始化间歇 IMA 等 11 条 | PD/多租户上线前逐条对 known-issue；关注 rc29 修复 |
| OpenAI 10/23 大限 | gpt-4o(05-13)/gpt-4 全系/o1/o3-mini/o4-mini 等 | 统一映射 `gpt-5.6-sol/terra/luna`；改模型名之外还有行为回归 | 10/23 前完成迁移 + 回归；可付费专属容量延命 |
| vLLM #59305（上游同步） | FlashMLA#19 的 OOM 守卫被上游 V4.1 同步静默回滚 | H200 实测 T=32768 时 8,208 MiB 瞬时分配随 pin bump 回归；公式级吻合 | 升级 FlashMLA pin 前跑显存曲线；盯 #59305 修复合入 |
| llama.cpp CPU FA #29774 | F16 累加器的静默 -inf/NaN | 结果错误（非变慢）；直接 F32 修复曾付 17% decode 代价，offset 方案最终打平 | CPU 长上下文用户跟进修复版 |
| llama.cpp #29867 | 融合 Lightning Indexer 的头部数适配 | GLM-5.3-Flash 在 M5 上 1–9 s/token 停顿（~30×），自动探测被硬编码绕过 | Apple Silicon 用户暂关融合 indexer |

共性结论：
1. **收窄的官方理由都是"聚焦"，但成本端是静默的**：KV 格式不兼容、映射表、pin bump——三者的共同点是默认路径变了而错误不一定报错（格式错会崩，守卫回滚和 CPU 回退是静默的）。
2. **跨请求隔离性是本周反复出现的红线**：TRT-LLM PD 串扰（官方 known-issue）、DSpark #59104 KV 覆写（社区）、上期 Ollama 泄漏（打包构建）——多租户部署的隔离性测试应升级为发布门禁。
3. **显存曲线要随 pin 重测**：#59305 证明"内核库版本"本身就是容量变量，公式 `(b+num_sm_parts)*s_q*h_q*d_v*4` 可直接进容量模型。
4. 证伪条件：若 TRT-LLM 在 rc30 修复 PD 串扰并公布根因为测试性问题，红线降级；若 #59305 被证为特定 batch 形态特有，显存检查点收窄。本页未声称独立复现。

来源：bucket 文件 inference-systems.md、community.md、models-agents.md 所列链接。
