# 2026-09-19 research ledger

## 采集、去重与流水线

按 2026-09-11 → 2026-09-19 八天窗口采集（上一正式期为 09-11；09-12 流水线仅完成 dedup 基线后中断，其基线并入本期 [dedup](pipeline/2026-09-19/dedup.md)）。八桶并行侦察（chips、infra-capital、models-agents、inference-systems、papers-oss、china-industry、community、deepseek-radar）由 ZCode 子代理（Explore × 8）完成，替换原 pi-subagents 通道；papers-oss 与 deepseek-radar 两桶首次因搜索后端限流失败，各重试一次成功，非 degraded。选题见 [selection](pipeline/2026-09-19/selection.md)；三篇深挖底稿 [deep-01](pipeline/2026-09-19/deep-01.md)、[deep-02](pipeline/2026-09-19/deep-02.md)、[deep-03](pipeline/2026-09-19/deep-03.md)。

与 dedup 表核对：SGLang #39068、vLLM #51692、FlashInfer #4967、Harness dsh-v0.1.5-rc.1（仍 alpha/rc 循环，v0.1.6-alpha.2 未 GA）、SGLang #39087（复核仍 0 评论、未修复，不重复）均无原样重复；8/30 各项无实质触发。

## 入选事实（Top 5）

- **昇腾 960 超节点，9/17 发布｜官方发布：**业界首个 NPO 超节点：灵衢 + Hi-ONE（业界首个量产 NPO，单引擎 7.2T、内置光源），单超节点 4096 卡、8 EFLOPS FP8、1PB HBM、可用度 99.8%；整机 5500 个 Hi-ONE 替代约 4.8 万颗 800G 光模块、互联功耗降超 550 kW。昇腾 960DT 就绪从 2027 Q4 提前三个季度至 2027 Q1，960 超节点风冷/液冷 2027 Q3/Q4；路线图延伸 970/2028、980/2029；部署存量首次官方量化：超 1000 套（910C 超 1000 套、950 规模商用）；多 960 组网最大 51.2 万卡。同场口径：CANN 月活开发者 5200、"跨越生态拐点"。[华为官方新闻稿](https://www.huawei.com/cn/news/2026/9/hc-ascend960-supernode)、[证券时报](https://www.stcn.com/article/detail/4189842.html)
- **H.R. 9340《Ratepayer Protection Act》417:3 通过，9/16｜官方立法：**100MW+ 大负载电网升级前须提供财务担保；提前退出电力合同须承担公用事业有保障的成本回收（exit-fee 式）；1 年内启动审议、2 年内终裁，参议院 11 月前过关概率低。配套：EEI 九月版 25 州已批大负载电价 + 7 州在审；IID 9/15 全票通过 20MW/80% 负载因子/削负载优先序；FERC 六个 RTO 集体延期至 11 月。[Utility Dive](https://www.utilitydive.com/news/house-passes-ratepayer-protection-bill-data-centers/830658)、[EEI](https://www.eei.org/-/media/Project/EEI/Documents/Issues%20and%20Policy/List%20of%20Large%20Customer%20Projects%20and%20Tariffs)
- **vLLM #57355，9/17 合入｜主线提交、作者报告：**CUDA graph 默认按 8 倍数捕获，`max_num_seqs` 非 8 倍数时最后一段 batch 落入 PIECEWISE 慢路径；过载服务器稳定跑在 max_num_seqs 并发 → 吞吐随运行衰减 2,922→829 tok/s。TP4 B200、Mistral-Small-4-119B-2603、8k–127k 混合 prompt：batch 97 修复后 1,523→3,876.85 tok/s（2.55×），与 batch 96 持平。Nsight：PIECEWISE 下 graph-launch 间隙 0.69→5.5 ms、all-reduce 等待 10µs→3.6–4.7 ms。投机解码开启场景未覆盖，未跑模型评测。[PR #57355](https://github.com/vllm-project/vllm/pull/57355)
- **DeepSeek V4-Pro 强制路由，9/14 04:00 UTC 生效｜官方公告：**`deepseek-v4-pro` 请求全部路由 V4.1-Flash 并按 Flash 价计费（峰值输入 $1.32→$0.30 约 −4.4×、输出 $3.96→$1.20 约 −3.3×、cache hit $0.006），持续至 V4.1-Pro 上线；后又宣布 9-14 后继续提供 V4 Pro、计费不变（退役与续供并存）。迁移约束：旧名退役静默换模、Vision 仅 Flash。V4.1-Flash 权重 9/10 已放出；本周推理栈适配：FlashMLA 修 CUDA 13/MSVC LLP64（9/14–15）、DeepGEMM 修 Mega MoE slot 释放顺序（9/14）、DeepEP 修低延迟 doorbell（9/16）、新开源 DeepJIT（CUDA/昇腾 NPU 统一 JIT 编译缓存库）。[官方 news](https://api-docs.deepseek.com/zh-cn/news/news260910)、[DeepJIT](https://github.com/deepseek-ai/DeepJIT)
- **社区双信号，9/17–9/19｜社区一手：**① HN「Cactus Needle 3」"8-29MB 匹敌 DeepSeek V4 Flash"被三组独立对照推翻（Scaevolus 同 230 例：FunctionGemma 90.9%/85.2% 对 Needle 3 W4A8 32.2%/20.4%；viccis 带上下文 5/27 vs 不带 8/27；"call 911"4 种表述 3 种误路由），作者当场认账修补；② vLLM #57680：0.26.0→0.29.0 H100 吞吐 ~1295→~362 tok/s（3.3×恶化）、ITL 6.68→23.88 ms，疑似 `aten::copy_` 5× 劣化，孤证待复现。[HN](https://news.ycombinator.com/item?id=49748553)、[#57680](https://github.com/vllm-project/vllm/issues/57680)

## 分类雷达与落选

- SGLang #40105（FlashInfer MoE fused finalize 默认翻转，W4A4 1-token +21.75%）与 #40148（MI355X GLM-5.2 TopK v2 官方回退，P90 +10.0%）：并入深挖 01。
- vLLM #56562（DSV4.1 元数据 Triton 融合：解码内核 4.13×、并发 1 吞吐 +22.3%、并发 1024 收益 1.4%、逐位一致）；#56853（ROCm HCA 双流：并发 1 TTFT −15.01%、并发 64 +0.96%）；TensorRT-LLM v1.3.0rc27（NVFP4/SM107 静默回退 FP8 KV 等 known-issues）。
- 论文：Pareto Atlas（FP8 KV 200 题 0% 正确、n-gram 投机 0.90–0.98×、AWQ −5.9pp）、PrefixBench-H100（前缀复用收益在缓存压力下被侵蚀）、Ask the Tool, Don't Guess（工具进度信号 p90 TTFT −21%）。
- 工具：Codex 0.155.0/0.155.1（多 agent task 生命周期、daemon 恢复 active goals、reasoning summaries 默认关闭）、Claude Code 2.1.271→278（子代理防冒充标头、AGENTS.md、resume 修 prompt cache、auto mode 服务端分类器免费）、Antigravity 2.14.0（Enterprise 终端/Git、checkpoint 修复）、GPT-5.5 将于 10-14 退役、GPT-5-Codex 9-24 关停。
- 宏观简讯：黄仁勋 9/17 表态 2027 颗数翻倍（$1T 累计口径，非文件）；TSMC 8 月营收 +53.3%（窗口边缘）；沐曦 9/17 解禁收涨 7.85% 但机构净卖出 20 亿+；寒武纪否认涨价；月之暗面/银河同日辟谣报案；智谱 FlashX 提价 2.5×并入深挖 03。
- 落选：PJM ride-through（9/10 窗口边缘，作背景）；DeepJIT 单列（并入 Top5-04 与深挖 03）；Z.ai"10 万卡 3×"零复现（作证伪条件）。

## 编辑判断

本期主线是**承诺与代价同时被制度化**：供给侧第一次出现"提前交付"的路线图修订（昇腾 960DT）、第一次把违约成本写进算力电力立法（H.R. 9340）、把旗舰替代写进计费路由（DeepSeek）；工程侧同一周给出对称证据——满载悬崖（#57355）、预防性默认翻转（#40105）、官方配方回退（#40148）与 HN 对照实测（Cactus），说明"宣称"只有附带条件、日期与代价，才可进入部署决策。

**KPI：Top5 新颖度均值 4.5；覆盖桶数 5（chips、infra-capital、inference-systems、models-agents、community；china-industry 与 deepseek-radar 并入相应条目）；社区/非官方一手 2（HN Cactus 对照、vLLM #57680）；落选候选 8 组；degraded：否（两桶限流后重试一次成功）。**
