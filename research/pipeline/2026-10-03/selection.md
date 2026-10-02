# 2026-10-03 selection

窗口 2026-09-21 → 2026-10-03（12 天断档期；重点最近 72 小时，空档期候选均注明日期）。8 桶侦察全部 anysearch 完成（china-industry 桶 1 次摩尔线程核查回退内置 WebSearch，结果为无新增），无限速，非 degraded。

## Top 5（按部署影响、证据完整度与桶覆盖排序）

| # | 事实 | 桶 | 准入线 | 类型 |
|---|---|---|---|---|
| 01 | FlashMLA 2026.09.30：移除 Hopper 与 V3/V3.2/V4.0、KV cache 格式破坏性变更；同日 TileKernels/DeepSelect 上线 Ascend 950 双后端（9/30 协调使能批次） | deepseek-radar | 准入 2（官方 release，改变复现/部署边界） | 官方 release |
| 02 | OpenAI DevDay（9/29）："Dots" 常驻自主 Agent 全付费档 + 新 Pro 档 + GPT-6.1 Sol 降价；GPT-6-Astra 安全暂扣 3 天后 10/1 放行 | models-agents | 准入 2（产品/可用性/价格变化） | 官方发布 |
| 03 | SGLang v0.5.21（10/2：PD 角色热切换、Rust prefix cache + 统一 radix 双默认翻转）与 vLLM v0.30.0（9/22：RL 采样掩码 2× 回归修复、NVFP4 默认翻转、V4 CPU 后端） | inference-systems | 准入 1/2（量化变化 + 破坏性清单） | 官方 release |
| 04 | neocloud 债务定价三档成形：Lambda $1bn 投资级 6.78%、Sharon AI $365m GPU 抵押 9.95%（10/2），与已报 CleanSpark Meta 垃圾债 8.25% 构成担保品定价标尺；Crusoe Project Hyper 升格 ~$12bn；AWS 侦调信后弃 NDA | infra-capital | 准入 3（市场条款/监管文件） | 官方文件/市场条款 |
| 05 | 社区失效模式三连：vLLM #59305 上游内核同步静默回滚 OOM 守卫（8 GiB，与 #01 直接联动）、#59104 DSpark lookahead off-by-one 跨请求 KV 覆写、llama.cpp #29774 CPU FA F16 累加器静默 -inf | community | 准入 4（具名一手，含对照组与公式级证据） | 社区一手 |

配额核对：桶覆盖 5（deepseek-radar、models-agents、inference-systems、infra-capital、community）≥3 ✓；动态发现 5/5 ≥3 ✓；社区源 1 组 3 条 ≥1 ✓；固定雷达触发 1 ≤1 ✓。与 dedup 表核对无原样重复。

## 落选与降档理由

- **vLLM-Ascend v0.27.1rc1 950DT 兼容矩阵 + 壁仞 1.74 亿招标订单**（china-industry）：满足准入 1/2，但与 Top5-01 同属"昇腾 950 可复现化"主线，为避免同主题占两席，并入深挖 01 与中文产业分类卡（950DT 矩阵含具体量化/拓扑参数，是本期最可复现的国产栈证据）。
- **TRT-LLM rc28/rc29**（inference-systems）：PD serving 跨请求内容错乱 known-issue 重大但属 rc 通道条件披露 → 算子行 + 深挖 02。
- **FlashInfer v0.7.0 FP8 grouped GEMM 正确性警告**（inference-systems）：单点条件警告 → 算子行。
- **Claude Code 2.1.288 / Codex 0.160.0 / Anthropic 5.5 双发**（models-agents）：5.5 定价与 Claude Code 无人值守语义为强迭代 → 工具卡 + 深挖 03。
- **弃用时间线更正**（models-agents）：GPT-5-Codex API 实际 7/23 已关停、9/24 为 Sora 2/Videos API——对上期口径的更正 → 模型分类卡 + ledger 更正记录。
- **Supermicro Rubin NVL72 出货**（chips）：交付状态变化，满足准入 2 → 芯片分类头条（不占 Top5 因其规格为厂商口径、缺第三方核验）。
- **华为"900 系仅限中国"报道**（chips）：中等置信媒体报道 → 芯片分类卡，标注置信度。
- **论文四篇**（papers-oss）：Periodic Weak Spots（相位 40pp）、KL/翻转率、STEPQuant、ALR-IRA → 论文区双卡。
- **智谱融资口径更正**：50 亿美元官宣实为 9/13 港交所公告（配售+CB），早于电话会报道 → ledger 更正，宏观简讯。

## 深挖分配（3 题，编辑基于桶内一手事实成文）

1. **昇腾 950 的"同日批次"：官方栈双后端化与可复现边界**——FlashMLA/TileKernels/DeepSelect 9/30 批次 + vLLM-Ascend 0.27.1rc1 矩阵（W4A8C8、两节点 1P1D、A2 排除）+ 壁仞招标订单 + "仅限中国"报道；对照表：组件 × NVIDIA 侧 × Ascend 侧 × 复现条件。
2. **支持面收窄的代价清单**——FlashMLA 砍 Hopper/V3 系 + KV 格式破坏、TRT-LLM PD 串扰、OpenAI 10/23 大限映射、#59305 上游同步回滚、llama.cpp CPU FA；迁移检查清单。
3. **Agent 从会话制到常驻制**——DevDay Dots + Claude Code 2.1.288 无人值守语义重划 + Codex 0.160 Guardian + Harness 0.2.0-rc.2 Messages-only；护栏对照表。

## 主线（Executive readout 单一论点）

**栈在收敛，生态在分化。**DeepSeek 官方算子栈 9/30 同日把昇腾 950 变成第二后端、同时砍掉 Hopper 与 V3 系并改掉 KV 格式——同一模型栈收敛到更少硬件代际，却在两套生态上分化出可复现路径（vLLM-Ascend 交出 950DT 兼容矩阵）；OpenAI 用 DevDay 把 agent 从会话制改成长驻制、用 10/23 大限把旧模型收敛进 5.6 系；债务市场同步给 GPU 担保品定出 6.78%/8.25%/9.95% 三档价格。收敛降低维护面，分化决定买谁——部署决策要同时回答两个问题。
