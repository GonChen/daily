# AI / 芯片情报日报：事实台账

资料截点：2026-08-16 早间（CST）。本文件用于页面制作核验；HTML 内的 `事实`、`报道`、`传闻`、`推断` 标签以此为准。

## 强时效事实（过去 24–72 小时）

- 2026-08-14 美股收盘：NVDA 225.16 美元（-0.04%）、AMD 514.39 美元（+6.52%）、AVGO 392.99 美元（-5.93%）、TSM ADR 426.35 美元（-0.96%）。行情数据仅说明价格变化，不证明变动原因。
- AMD 宣布/提交 47.5 亿美元多期高级无担保债：2029 年 12.5 亿美元（4.60%）、2031 年 15 亿美元（5.00%）、2033 年 10 亿美元（5.25%）、2036 年 10 亿美元（5.50%）。用途为一般公司用途及偿债；没有披露将资金专门投向某项 AI 芯片计划。
- “Google 与 AMD 探索 TPU v10 合作、Broadcom TPU 产量预期下修”来自市场通讯和二手转述，Google、AMD、Broadcom 均未公开证实。只能标为传闻，不能当作 AMD 上涨或 AVGO 下跌的确定原因。
- Claude Code npm 版 2.1.233 于 2026-08-14 发布；其公开变更记录包括 GitLab MR worktree、Linux Bash 工具内存上限、MCP 与高 CPU 占用修复、安全修复等。
- pi 0.84.2 于 2026-08-14 发布；公开说明包括全屏 transcript 搜索、defaultTools 配置和实验性严格 JSON Schema 工具采样。
- Codex 0.148.0-alpha.13 至 alpha.19 在 8 月 13–15 日连续发布；最新稳定版仍是 0.147.0（8 月 7 日）。alpha 页面未提供足以解释功能变化的详细说明。
- GLM-5.3 开源权重据 Axios 报道延后两周发布；CyberGym 84.5% 及发现 2,400 个漏洞（其中约 1,000 个严重/高危）属于模型方口径，尚非独立复现实验。
- 美国 7 月零售销售环比 -0.6%；7 月 CPI 同比 3.4%、环比 0.1%；PPI 环比持平。由此得到的货币政策含义属于推断。

## 推理框架与算子库

- SGLang v0.5.17 于 2026-08-08 发布：582 个 PR、194 位贡献者；包括 Kimi K3 day-0 支持、Rust 服务前端、DCP 通信后端、session-aware Radix Cache、MoE prefill DWDP。1.92×、模型加载 35 分钟降到 6 分 20 秒等均为项目方特定配置数据。
- vLLM v0.27.1 于 2026-08-11 发布，是 0.27.0 的补丁版，公开变更为支持量化 DSpark Markov heads。
- TensorRT-LLM v1.3.0rc24 于 2026-08-12 发布，加入 Kimi K3 等支持，同时公开列出 torch.compile × CUDA Graph、SM120 MLA+MTP、低精度多 GPU MoE 等已知问题；它是 RC，不写成稳定生产版。
- PyTorch 最新稳定版为 2.13.0（2026-07-08）。官方亮点包括 FlexAttention MPS 稀疏模式特定测试最高约 12×、CuTeDSL Native DSL 原型、LinearCrossEntropyLoss 最高减少 4× 峰值显存。
- FlashAttention 4 beta26 于 2026-08-12 发布，以 SM90/100/110 backward、SM100 varlen/block-sparse/SplitKV deadlock、动态 shape 正确性等修复为主。
- FlashInfer v0.6.17 于 2026-08-11 发布：MoE expert parallel 的 vLLM 生产路径、SM12x fused-MoE NVFP4 精度修复、MXFP4 W4A8/W4A16 和 Kimi K3 MLA decode。
- FlashMLA 没有正式 GitHub Release；最近可核验提交为 2026-07-28，把 decode-combine num_splits bucket 从 160 扩展到 256。
- cuDNN Frontend v1.27.0 于 2026-08-06 发布：Python-native pygraph、FROST engines、GDN linear attention。DeepSeek-V3 MLA 的 SM100 SDPA kernel 820 useful TFLOPS / 约 1.5× 为 NVIDIA 特定测试数据。
- 最新 CUDA 13.3 文档中，cuBLAS 报告 Blackwell Ultra FP4 matmul 几何平均 +5%、Blackwell/Ultra TF32 几何平均 +27%；另有官方 13.4.1 patch 修复 13.2 Update 1 的 NVFP4 tensor-wide scaling 正确性问题。

## 主流开放模型

- Kimi K3 官方仓库：2.8T 总参数、104B 激活、896 experts / top-16、69 KDA + 24 gated MLA、1M context、原生 MXFP4 weights / MXFP8 activations；benchmark 为模型方与其引用来源口径。官方给出 vLLM、SGLang 部署路径。
- DeepSeek 官方透明度页面列出 V4 于 2026-04-24 发布；API 提供 V4-Pro 和 V4-Flash。过去 72 小时没有新的官方代际发布。
- GLM-5.2 官方于 2026-06-16 发布，公开权重、1M context；IndexShare 2.9× FLOPs 降低和 MTP 接受长度最高 +20% 为官方口径。GLM-5.3 仍按媒体报道标注。
- Qwen 官方当前开放基线为 Qwen3.6：35B-A3B 与 27B，Apache 2.0，官方仓库给出 SGLang/vLLM 部署示例。过去 72 小时没有新的官方代际发布。

## 新论文（预印本，作者报告）

- OpScale, arXiv:2608.13499：生产轨迹规模最高 40×A100 + 24×GB200；作者报告在满足 SLO 时最多减少 36.3% GPU 与 28% 能耗，或固定成本下提高 44% 吞吐。
- DARTree, arXiv:2608.13524：作者报告每轮验证最多接收 12.97 tokens，相对本地 AR 解码最高 9.73× 无损加速。
- Reduced Matrix Multiplication, arXiv:2608.13426：无训练、输入自适应矩阵切片；A100 自定义内核，覆盖 1B–70B 模型。摘要未给出统一速度倍数。
- Beyond Final Scores, arXiv:2608.13417：7 个前沿模型、36 项长时程 AI R&D 任务；结论强调当前 agent 更像工程优化器，运行方差和 harness 设计影响显著。
- 近月补充 arXiv:2607.23089：面向 Ascend NPU 的 Triton kernel 诊断优化；37 个条目，几何平均 4.35×、中位数 2.73×，数据集较窄。

## 背景与观察节点

- Data Center Watch 统计 2026 Q1 至少 75 个美国数据中心项目被阻断或推迟，项目名义价值约 1,300 亿美元。该数字不是已实现损失，且“推迟”不等于“取消”。
- 华为 7 月发布 Atlas 950 SuperPoD：1024 卡、FP8 1 EFLOPS、FP4 2 EFLOPS、256TB 统一内存、3μs RTT，作为近月技术基线，而非过去 72 小时新闻。
- 寒武纪股东会定于 2026-08-17；NVIDIA FY2027 Q2 财报电话会定于 2026-08-26。壁仞、沐曦近 72 小时未检索到高可信重大公开公告。

## 编辑原则

- 优先公司公告、官方 changelog、监管文件、论文原文；媒体用于补充未正式发布的交易/市场信息。
- 价格变化与新闻同日出现不等于因果；所有因果解释均使用“可能”“市场解读”等措辞。
- 论文数字均是作者报告，需等待独立复现；公司 benchmark 均是公司口径。
- 页面不构成投资建议。
