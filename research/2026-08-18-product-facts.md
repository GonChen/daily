# 2026-08-18 前沿计算情报日报｜研究底稿

资料截止：2026-08-18 06:00 CST。优先使用监管文件、公司公告、官方模型卡、官方 GitHub release/PR 与政府数据；媒体稿只用于宏观与市场预期。主线 PR 不写成正式 release，公司/作者 benchmark 不写成独立复现。

## 1. 今日核心判断

今日的共同主题是：AI 基础设施开始把规模口号落到项目级信用风险、模型许可和生产控制面。

- NVIDIA/SB Energy/OpenAI 的俄亥俄项目首次把 4.25 IT-GW、20 年租约和最高 1,050 亿美元或有担保放在同一份 SEC 文件中。
- Qwen3.8 的开放权重已经发布，但 2.4T-A95B 与 27B 的模态、thinking 行为和许可不同，不能笼统称为同一开源产品。
- TensorRT-LLM 同日给出 DSpark 融合微基准和 KV cache 统计/协调修复，说明快路径与控制面必须一起验收。

## 2. NVIDIA / SB Energy / OpenAI PORTS-Pike

一手来源：

- SEC 8-K：https://www.sec.gov/Archives/edgar/data/1045810/000104581026000069/nvda-20260817.htm
- NVIDIA Newsroom：https://nvidianews.nvidia.com/news/nvidia-guarantees-sb-energy-s-ports-pike-technology-campus-in-ohio-to-exclusively-host-nvidia-ai-compute
- SB Energy：https://sbenergy.com/nvidia-ai-compute-ports-pike-ohio/
- 项目页：https://portscampus.com/

可写事实：

- NVIDIA 是 PORTS-Pike 的独家 AI compute infrastructure provider；OpenAI 是租户/客户。
- SB Energy 建设、持有、运营园区，OpenAI 签 20 年租约。
- 首期 4.25 IT-GW；NVIDIA 对另约 3.75GW 提供选择性支持，总目标 8GW。
- 计划从 2028 年开始分阶段上线。
- SB Energy/SoftBank 计划建设至少 10GW 新能源；AEP Ohio 相关区域电网投资至少 42 亿美元。
- NVIDIA 向 SB Energy 投资 15 亿美元；NVIDIA 与 OpenAI 各支持 4,000 万美元社区基金，总额 8,000 万美元。
- SEC 文件披露多份剩余价值担保，NVIDIA 对首期 4.25GW 相关租约的累计付款义务最高 1,050 亿美元。
- 触发包括 OpenAI 破产、违约或不付款；付款计算与替代租赁/处置所得和约定最低值之间的差额有关。
- NVIDIA 可承接租约、推动转租/出售或允许终止；OpenAI 同意偿还/赔偿 NVIDIA 实际代付金额。
- 担保可因 20 周年、租约终止、OpenAI 信用评级达到约定条件等情形终止。

边界：

- $105B 是或有付款累计上限，不是即时支出、已确认负债或管理层预期损失。
- 8GW 是园区目标，不应直接换算成近期 GPU 营收。
- 编辑推断：NVIDIA 的竞争边界正在从供货和软件扩到客户信用与 GPU 残值；需持续看担保余额、客户集中度和替代租户能力。

## 3. Qwen3.8 开放权重

一手来源：

- 官方仓库：https://github.com/QwenLM/Qwen3.8
- 8/17 README 更新：https://github.com/QwenLM/Qwen3.8/commit/2ea10dc725823bf7c3e21ce8557cbe15245132ae
- 官方 Blog：https://qwen.ai/blog?id=qwen3.8
- 2.4T-A95B 模型卡：https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B
- 27B 模型卡：https://huggingface.co/Qwen/Qwen3.8-27B

可写事实：

- 仓库列出 2.4T-A95B 于 8/12 上线、27B 于 8/14 上线，README 于 8/17 更新。
- 2.4T-A95B：2.4T 总参数、95B 激活；原生 262,144 context，可扩至约 1,010,000；纯文本、必须 thinking；许可标识为 `qwen3.8-max`，不是 Apache 2.0。
- 2.4T 结构为 23 ×（3 × Gated DeltaNet→MoE + 1 × Gated Attention→MoE）。
- 27B：27B dense，Apache 2.0；原生视觉语言，可关闭 thinking；原生 262,144 context，可用 YaRN 扩至约 1M。
- 两者均给出 Transformers、vLLM、SGLang、TokenSpeed 路径。

纠错说明：

- 2026-08-17 日报写“Qwen3.6 是当前开放基线”不再成立。今日按官方仓库与模型卡纠正为 Qwen3.8。
- Hosted Qwen3.8-Max 的能力不能自动映射到 2.4T 开放权重；许可、模态、thinking 和服务形态必须分开。
- 模型方 benchmark 仅作为发布方口径，本期不采用其排名作为独立能力结论。

## 4. 推理框架与系统优化

### TensorRT-LLM

- DSpark fusion PR：https://github.com/NVIDIA/TensorRT-LLM/pull/17307
  - Blackwell CuteDSL 自定义算子；SM100/SM103 走融合，其余硬件 PyTorch fallback。
  - B200 内部微基准：sparse attention 312.3μs → 67.5μs（4.63×）；五个 RMSNorm/RoPE 变换 732.2μs → 295.5μs（2.48×）。
  - 10 个 B200、35 个硬件无关测试通过。
  - 边界：主线 PR、内部微基准，不是 release 或端到端吞吐。
- KVCacheManagerV2 PR：https://github.com/NVIDIA/TensorRT-LLM/pull/17391
  - DeepSeek-V4-Flash-NVFP4 调优中，76/4,934（1.5%）最大上下文 warmup dummy 贡献容量平方和的 100%。
  - 含 dummy 的 RMS capacity 130,139，排除后 313；真实序列平均约 530。
  - 错误统计可能要求移动 171GB/rank；一次自然 workload 运行 12,288 prompts、约 3,060 samples/rank，重平衡移动 169.36GB，约 2.55s。
  - 新实现协调 TP/CP/PP/attention-DP。
  - 边界：该自然运行不是 throughput benchmark。

### SGLang

- 正式版仍为 v0.5.17：https://github.com/sgl-project/sglang/releases/tag/v0.5.17
- Kimi-K3 MI35x nightly：https://github.com/sgl-project/sglang/pull/32568
  - 8×MI35x、TP8、ROCm 7.2；GSM8K 1,319 题，并发 64，阈值 0.92；gfx95x only 因原生 MXFP4 不支持 gfx942。
  - 边界：CI 准确率覆盖，不是速度数据。
- HiCache retraction：https://github.com/sgl-project/sglang/pull/34801
  - retraction 后保留 target 与 speculative draft KV；steady-state 路径不变，无速度数据。

### vLLM

- 正式版仍为 v0.27.1：https://github.com/vllm-project/vllm/releases/tag/v0.27.1
- Kimi-K3 DCP + DSpark：https://github.com/vllm-project/vllm/pull/52188
  - target 为 FlashInferMLA/TokenSpeed，draft 为 TokenSpeed；GSM8K exact match 约 0.9606/0.9613/0.9621。
  - 边界：准确率近似持平，不证明吞吐提升。
- DeepEP v2 receiver CPU overhead：https://github.com/vllm-project/vllm/pull/51114
  - PR 没有可引用数值，不写性能倍数。

### PyTorch

- 最新稳定版仍为 v2.13.0（7/8）：https://github.com/pytorch/pytorch/releases/tag/v2.13.0
- 过去 72 小时没有足以改变部署判断的新正式 release。

## 5. 算子库雷达

- FlashAttention：FA4 beta26（8/12），无更新：https://github.com/Dao-AILab/flash-attention/releases/tag/fa4-v4.0.0.beta26
- FlashInfer：8/17 自动 nightly，只有构建说明，不宣称新功能：https://github.com/flashinfer-ai/flashinfer/releases/tag/nightly-v0.6.18-20260817
- FlashMLA：无新正式 release；公开面安静：https://github.com/deepseek-ai/FlashMLA
- cuDNN Frontend：仍为 v1.27.0（8/6）：https://github.com/NVIDIA/cudnn-frontend/releases/tag/v1.27.0
- cuBLAS：沿用 CUDA 13.3 / patch 13.4.1 基线；升级先检查 NVFP4 数值正确性：https://docs.nvidia.com/cuda/cublas-patch-release-notes/contents.html

## 6. 模型雷达

- DeepSeek：官方公开代际仍为 V4；过去 72 小时无新代际：https://www.deepseek.com/en/transparency/
- GLM：5.3 权重继续等待；5.2 是可部署官方基线：https://z.ai/blog/glm-5.2
- Kimi：K3 没有新权重版本，但主流框架正在补 MI35x CI、DCP/DSpark 与融合路径：https://github.com/MoonshotAI/Kimi-K3
- Qwen：见第 3 节，今日为重要基线纠正。

## 7. Agent / 开发工具

- Claude Code v2.1.234：https://github.com/anthropics/claude-code/releases/tag/v2.1.234
  - 自动在 usage limit 重置后续跑（可配置）。
  - 加固 Windows NT namespace 路径检查；修复后台 subagent 权限回答丢失；MCP diagnostics 不再输出 resolved secrets。
  - remote control 同步权限/模型/effort；`/permissions`、`/add-dir` 可 mid-turn 打开。
  - 内置 `claude-api` skill 上下文约 200k+ → 25k，为发布方测量。
- OpenAI Codex 0.148.0-alpha.21：https://github.com/openai/codex/releases/tag/rust-v0.148.0-alpha.21
  - 8/17 19:27 UTC；只有构建标题，不推断具体能力。
- pi：仍为 v0.84.2（8/14）：https://github.com/earendil-works/pi/releases/tag/v0.84.2
- Cursor：过去 72 小时官方 changelog 无可核验重大条目：https://cursor.com/changelog

## 8. 国产 GPU / 加速器

- 华为 Atlas 950 SuperPoD 仍是近月集群基线：https://www.huawei.com/cn/news/2026/7/atlas-950-superpod
  - 1,024 卡、FP8 1 EFLOPS、FP4 2 EFLOPS、256TB 统一内存、3μs RTT；不是今日新消息。
- 截止时间内，壁仞、沐曦、寒武纪官方公开面没有足以改变产品判断的新公告。
- 寒武纪股东会相关内容只等上交所/公司正式披露，不采用市场转述。

## 9. 资本市场与宏观

- Nasdaq 8/17 收盘接口：NVDA $225.01（-0.07%）、AMD $506.00（-1.63%）、AVGO $392.43（-0.14%）、TSM ADR $430.905（+1.07%）、MU $1,011.75（+4.13%）。价格是事实，归因不是。
- Reuters 分析：https://finance.yahoo.com/technology/ai/articles/analysis-big-investors-hunt-tomorrows-050129962.html
  - 汇总预期：hyperscalers 2027 较 2025 年年度经营现金流增量约 $340B，CapEx 增量约 $534B；数据中心建设到收入通常 12–18 个月。
  - 文中一位 CIO 估算 AI 变现需 5–13× 才能支撑投入；这是单一受访者估计，不是共识。
- BLS July CPI：https://www.bls.gov/opub/ted/2026/consumer-prices-up-3-4-over-the-year-in-july-2026.htm
  - CPI 同比 3.4%，核心 2.5%，能源 14.7%。
- Reuters FX/rates：https://finance.yahoo.com/markets/currencies/articles/yen-edges-traders-push-back-004148952.html
  - 9 月加息市场隐含概率 30.6%，一周前 52.2%；美元指数 99.53。
  - 边界：市场概率不是 Fed 承诺。

## 10. 论文窗口

06:00 CST 截止时，arXiv 官方 API 返回 rate exceeded，且尚未获得 8/17 新批次的可靠一手元数据。因此不编造“今日新论文”，保留 8/13 的高价值近周条目：

- OpScale：https://arxiv.org/abs/2608.13499
- DARTree：https://arxiv.org/abs/2608.13524
- Reduced Matrix Multiplication：https://arxiv.org/abs/2608.13426
- Beyond Final Scores：https://arxiv.org/abs/2608.13417

## 11. 编辑决策

- 今日 Top 5：项目级担保、Qwen3.8 权重边界、DSpark fusion、KV cache 控制面、Claude Code 2.1.234。
- 不把 FlashInfer nightly 当功能发布；不为 vLLM/SGLang 主线 PR创造吞吐数字。
- 不把 $105B 当支出，不把 8GW 当近期收入，不把单日股价当产业因果。
- 对 Qwen 昨日基线做显式纠正，不用模糊措辞掩盖。
- 国产 GPU 没有高价值一手新公告时保留“公开面安静”，不以二手消息填版面。
