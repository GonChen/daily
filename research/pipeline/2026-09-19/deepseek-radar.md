# 2026-09-19 deepseek-radar 桶候选

结论：窗口内无模型权重层面新开源动作（V4.1-Flash 权重 9/10 已放出，在窗口前一天），但出现 1 个实质新开源组件（DeepJIT，明确支持昇腾 NPU）与 FlashMLA/DeepGEMM/DeepEP 围绕 V4.1 推理栈的 4 个实质合入修复。deepseek-harness 无 GA。

## 1. 官方新仓库 DeepJIT 开源：统一 CUDA/昇腾 NPU 的 kernel JIT 编译库
- 日期：9/14 更新（org 页面显示近期新增，main 共 3 commit）｜类型：官方新开源
- 事实：DeepJIT — "A lightweight library for xPU kernel JIT compilation"：header-only C++20 JIT runtime，为 CUDA GPU 与华为昇腾 NPU 提供统一运行时编译/缓存（内存+磁盘+分布式共享）/加载/launch，含 pybind11 PyTorch 集成与 PTX/SASS 诊断导出；作者 guyan364、kurisu6912、LyricZhao。
- 影响：唯一"超出日常 bump"的官方新增。"xPU"措辞 + 昇腾 NPU 一等公民后端，表明 DeepSeek 开源推理基础设施走硬件中立路线；与本周华为"CANN 生态拐点"口径形成同周对齐。
- 来源：https://github.com/deepseek-ai/DeepJIT
- 新事实：DeepSeek 官方新增同时支持 NVIDIA CUDA 与华为昇腾 NPU 的 kernel JIT 库。

## 2. FlashMLA：V4.1 kernel 合入后 48 小时内连续两笔工具链兼容修复
- 日期：9/14（063a9f0，CUDA 13.0 编译修复）、9/15（ba89a34/#224，MSVC LLP64 下 128-bit st.async PTX 用 longlong2）｜类型：合入 PR
- 事实：承接 9/10 "Add kernels for DeepSeek v4.1"（#221）；无新 release tag。
- 影响：V4.1-Flash 开源推理支持在新工具链（CUDA 13、Windows/MSVC）上收口——"权重开源→推理栈适配"的开源侧对应动作。
- 来源：https://github.com/deepseek-ai/FlashMLA/commits/main
- 新事实：V4.1 kernel 的 CUDA 13 / MSVC LLP64 兼容修复。

## 3. DeepGEMM：26/09 public release 后首笔跟进——Mega MoE 释放顺序修复
- 日期：9/14（#441，作者 zheanxu）｜类型：合入 PR
- 事实：修复 Mega MoE 路径 task info slot 释放顺序；前一笔为 9/10 "Public Release 26/09"（#432）。
- 影响：确认官方 GEMM 栈存在活跃维护的 Mega MoE 路径（大概率与 V4.1 MoE 推理相关）。
- 来源：https://github.com/deepseek-ai/DeepGEMM/commits/main
- 新事实：26/09 release 处于积极修补期。

## 4. DeepEP：低延迟路径 doorbell 语义修复（简讯）
- 日期：9/16（a56d615/#752）｜类型：合入 PR
- 事实：修复低延迟 get 路径"最后一次 get 未触发 doorbell"；DeepEP 自 8/4 以来窗口内唯一 commit。
- 来源：https://github.com/deepseek-ai/DeepEP/commits/main
- 新事实：低延迟 MoE 推理正确性修复。

## 已核查、无实质变化清单
- deepseek-harness：v0.1.6-alpha.1（9/15）、v0.1.6-alpha.2（9/17），仍全为 pre-release；v0.1.5 停在 rc.2 未转正、直接开 0.1.6 alpha 线——按"只报 GA/事故/实质功能"标准不单列。
- awesome-deepseek-agent（9/17 更新）：无新增可报事实。
- DeepSpec/TileKernels/EPLB/LPLB/DualPipe/3FS/smallpond/open-infra-index/DeepSeek-V3/R1：无窗口内 push。
- deepseek-recipe/DeepSelect：最后更新 9/10（窗口前一天）。

## 待核实（不计入）
SGLang "Support DeepSeek-V4.1-Flash" PR 搜索结果给出编号 #56214，访问 404，无法确证，不引用；vLLM recipes 已有 V4.1 day-0 recipe（"不支持 torch.compile、仅 uniform-batch CUDA graph"，二手转述）。
