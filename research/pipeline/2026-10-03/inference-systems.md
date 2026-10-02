# 2026-10-03 inference-systems 桶候选

## 1. FlashMLA 2026.09.30：移除 Hopper 与 V3/V3.2/V4.0 支持、KV cache 格式破坏性变更；同发布昇腾 950 算子
- 日期：2026-09-30｜类型：官方 release（含 breaking change）
- 事实：移除 Hopper 架构及更早模型（DeepSeek V3/V3.2/V4.0）支持，更改 FP8/FP4 KV cache 格式且与旧版互不兼容，旧模型/旧格式需回退固定 commit `ba89a34`。同一发布在华为昇腾 950 NPU 上开源稀疏注意力 prefill/decode 算子（作者报告：prefill 410 TFLOPS、95% 硬件峰值；decode 360 TFLOPS、83% 峰值，附技术报告），fused norm-RoPE-attn-RoPE-cast decode kernel 再优化 10-15%。
- 影响：H100/H200 上的 MLA 服务与所有 V3 系模型必须钉住旧 commit，升级前 KV cache 需重建；此前所有基于 FlashMLA 的 decode 对比（含已报 SGLang v0.5.20 "TRT-LLM 替代 FlashMLA decode 1.45×"）只对旧 commit 成立。
- 来源：https://github.com/deepseek-ai/FlashMLA
- 新事实：官方把支持面收窄到 Blackwell + V4.1 且 KV 格式不兼容；同日 TileKernels/DeepSelect 亦上线昇腾 950 后端（见 deepseek-radar 桶）——协调的昇腾使能批次。

## 2. TensorRT-LLM v1.3.0rc28/rc29：Known Issues 收窄 PD 分离与低精度主张
- 日期：rc28 9/23、rc29 9/29｜类型：官方 release（rc28 首次公开 11 条 Known Issues）
- 事实：rc28 已知问题含：**重叠 TinyLlama PD serving 可能返回同批次另一个 prompt 的内容（跨请求数据错乱）**、Qwen3.5-4B CP+异构 TP 掉精度、DeepSeek-V4-Flash NVFP4 KV 初始化间歇 illegal memory access、Qwen3-30B-A3B skip-softmax 0.9 稀疏度+FP8 KV 挂起、8-rank 非对称 NIXL KV 间歇失败、Nemotron-3 Super FP8 C++ Mamba cache 掉精度（回退：Python Mamba cache）。rc29 修复 Qwen3.5 gather/scatter 性能回归（#19578）、移除 AutoDeploy（BREAKING）、升级 PyTorch 2.14/Triton 3.8/C++20。rc28 将 KV-cache manager V2 设为 Llama/Llama4 默认、新增 DFlash 2。
- 影响：PD 分离、NVFP4、FP8 KV 的官方叙事附带一整页"在哪些 shape/拓扑下不成立"；跨请求数据串扰对多租户服务是直接红线。
- 来源：https://github.com/NVIDIA/TensorRT-LLM/releases
- 新事实：首次系统性地以 Known Issues 给出正确性/回退边界，含 PD serving 跨请求内容错乱。

## 3. vLLM v0.30.0（9/22 正式发布）：RL 采样掩码 ~2× 回归修复、NVFP4 默认后端翻转、多项破坏性变更
- 类型：官方 release（762 commits）｜事实：①`--return-sampling-mask` 改 GPU 压缩，修复约 2× RL step-time 回归（#54901）；②SM100/103 NVFP4 W4A16 默认后端 Marlin→FlashInfer CuTeDSL（#53014）；③图捕获期间冻结 gc：捕获 12s→2s、H200 引擎初始化 28.9s→8.2s（#54646，作者报告）；④HiSparse 主机侧 KV 分层（#53781）；`--load-format ipc_cache` 常驻权重缓存（#54921）；MTP/EAGLE3/DFlash/DSpark 支持流水线并行（#50514）、draft 投机器在线接受率自适应验证（#52228）。破坏性：GPTQ 激活顺序（g_idx）支持删除（#54809）、YaRN 对齐后厂商别名不再重缩放 max_model_len（#56446）、scale-out 需 `--enable-scale-out` 显式开启。DeepSeek 相关：V4.1-Flash 头条新模型 + SM100 整份 KV MXFP8（FlashMLA V4.1 路径，#56893）+ V4 CPU 后端（AVX512/AMX，#55355）。Kimi K3 链路作者报告：混合批 gather/scatter 移除 +5.2-7.7% E2E、FP8 MLA cache 插入内核 4-6×。
- 影响：GPTQ 旧检查点与 YaRN 隐式缩放配置会静默变行为，升级前需回归；RL 管线尽快吃到 #54901。
- 来源：https://github.com/vllm-project/vllm/releases/tag/v0.30.0
- 新事实：把已报零散 PR 线索固化为带破坏性清单的版本；V4.1 MXFP8 全 KV 与 V4 CPU 后端同版落地。

## 4. SGLang v0.5.21（10/2 正式发布）：PD 角色热切换、Rust prefix cache 与统一 radix tree 双默认翻转
- 类型：官方 release（779 PRs）｜事实：①PD 实例运行中在 prefill/decode 角色间切换、无需重启（#28403）；②prefix cache 默认 Rust 内核（#39627）、统一 radix tree 扩展为全模型默认（#35081，Breaking）；③作者报告：DeepSeek-V4.1 长上下文首 token 快 22%（#40352）、Kimi K3 PD prefill 吞吐 +20.6%（#40045）、RL 采样掩码 overlap 调度 Qwen3-8B decode +17%/+52%（#36631）、ROCm GLM-5.2 分离式 decode TPOT 23ms→8ms（8×MI355X，#36714）、AMD Lean attention 默认开启（MI355X 吞吐至多 1.52×、ITL 至多降 3.62×，`SGLANG_DISABLE_LEAN_ATTENTION=1` 可关，#33576）；④已报 #40105 正式落地；⑤torch 2.13.0 + triton 3.7.1，内核缓存收拢 `SGLANG_CACHE_DIR`（升级后首次启动重编译，Breaking）。
- 影响：升级触发缓存层行为变化与一次性重编译；PD 热切换改变容量规划假设（不再需要固定 prefill:decode 比例）。
- 来源：https://github.com/sgl-project/sglang/releases/tag/v0.5.21
- 新事实：PD 免重启热切换 + 两个缓存默认翻转。

## 5. FlashInfer v0.7.0（9/22 正式发布）：FP8 grouped GEMM 正确性警告收窄性能主张
- 类型：官方 release + 作者报告｜事实：①release notes 正式警告（issue #4396）：CUTLASS `gemm_fp8_nt_groupwise` 在 SM100/SM103、M ≤ 32 且 scale_granularity_mnk=(1,128,128) 时可能间歇性输出错误，0.7.0 仍存在，**无文档化开关可单独禁用该 CUTLASS 快速路径**；②Autotuner v2 共享缓存：Qwen3-8B-FP8 TP2 B200 调优窗口冷启动 128s→重启 1s、总启动 410.7s→165.3s（作者报告，opt-in）；③实验后端不再自动选中（需 `FLASHINFER_ALLOW_EXPERIMENTAL_AUTO_BACKENDS=1`）；④MiniMax-M3 稀疏注意力 B200 内核级 2.45× geomean（作者报告）；⑤PrimTS 把 TRT-LLM Gen MoE 内核以可读 Python 源码发布；v0.7.1rc 线新增 Rubin SM107 分片、MNNVL MoE all-to-all。
- 影响：小 batch FP8 MoE/GEMM 用户需按 shape 白名单验证或换后端；autotune 缓存把集群重启调优成本降一个量级（opt-in）。
- 来源：https://github.com/flashinfer-ai/flashinfer/releases
- 新事实：#4396 正确性警告进入正式 release notes 且明示"无单独禁用开关"。

## 安静项
FlashAttention（无新 release）、PyTorch（2.14.0 后无新版本）；窗口内无满足准入线的独立 serving 复测。
