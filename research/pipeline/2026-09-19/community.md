# 2026-09-19 community 桶候选

## 1. "8-29MB 小模型匹敌 DeepSeek V4 Flash"主张在 HN 被多组对照实测推翻，作者当场认账并打补丁
- 日期：2026-09-18（评论持续到 9-19）｜平台/作者：HN「Show HN: Cactus Needle 3」（198 pts/88 评论），作者 HenryNdubuaku（Cactus Compute）；反方 Scaevolus、viccis、gs17、ash_091、poly2it 等可溯历史记录用户
- 事实：三组独立对照：① Scaevolus 同 230 例精调对照——FunctionGemma BF16 tool-shape 正确 209/230（90.9%）、exact args 196/230（85.2%），Needle 3 W4A8 仅 74/230（32.2%）、47/230（20.4%）；② viccis ~36 场景套件——"25 minute timer"被照抄成 25 秒（置信度 100%），带上下文 5/27 vs 不带 8/27（自带对照组，加上下文反而更差）；③ 安全反例——gs17"make it hot"把恒温器 20→18；ash_091 测 4 种"call 911"表述 3 种被错误路由；poly2it"My car crashed I need help"返回 play_music（置信度 1.0）。作者承认 reasoning 非真推理、tool 定义有问题，当场加专用 911 工具、参数 min/max 限制并更新 preset。
- 可信度：高（多方独立测试、有对照与数字、作者在场并已修复；被证伪的是营销标题而非所有场景）。
- 来源：https://news.ycombinator.com/item?id=49748553 ；https://cactuscompute.com/needle
- 新事实：本周最热端侧模型宣传被三条独立对照路线量化击穿，以作者现场打补丁收场。

## 2. vLLM #57680：0.26.0→0.29.0 解码吞吐 3.3 倍回归（H100），疑似 `aten::copy_` 路径劣化
- 日期：2026-09-19 新开（0 评论）｜作者：yeighta（具名 GitHub 账号）
- 事实：Qwen3.6-35B-A3B-FP8、H100、Confidential Computing VM、并发 12：吞吐 ~1295→~362 tok/s（3.3×恶化），ITL 6.68→23.88 ms；profiler 显示 `aten::copy_` 单次约 5 倍耗时；已排除 CUDA 版本、MoE/attention backend、cudagraphs；另有双峰不稳定测量（41.4/60.8 tok/s 交替），CC 环境 CUPTI 不可用无法下钻 kernel 级。
- 可信度：中（环境非典型、孤证、无维护者定性；A/B 复现配置完整，48 小时内值得跟踪）。
- 来源：https://github.com/vllm-project/vllm/issues/57680
- 新事实：窗口内最新大版本升级回归事故，可直接照抄的版本对照。

## 3. vLLM #57555/#57342：KV offload 内置 DMA/Triton 阈值被贡献者自己的 A30 扫描推翻（仅按 H100 PCIe 调参）
- 日期：2026-09-17/09-18｜作者：hyunnnchoi（KV offload 方向贡献者，具名）
- 事实：路径选择器硬编码 `THRESHOLD_BYTES = 28*1024`、`MIN_N = 16`（只在 H100 PCIe Gen5 调过）；A30 扫描显示 canonical KV 布局走 DMA 反而比直接加载慢 2.4–3.8 倍（按 page 选路径却按碎片拷贝），Triton 在 N=16 也常输；提议设备端 profiling 自适应阈值。
- 可信度：中高（相关代码路径贡献者、附独立基准脚本、#57555 有 5 条讨论）。
- 来源：https://github.com/vllm-project/vllm/issues/57555 ；https://github.com/vllm-project/vllm/issues/57342
- 新事实："H100 上调好的常数在别的卡上是反优化"首次有成对 issue + 扫描数据支撑。

## 4. Z.ai《GLM 自建推理基础设施》HN 大讨论：3x/成本主张零复现，客户侧"API 慢"与厂商吞吐叙事反差
- 日期：2026-09-17（403 pts/280 评论）｜来源：HN + https://z.ai/blog/glm-built-its-inference-infrastructure
- 事实：厂商主张"10 万+ 国产加速器、~10T tokens/天、E2E serving 提升 3x、单 token 成本对标 NVIDIA GPU"。评论区无具名推理引擎维护者独立复现：verdverm 只做 ~100M tokens/设备/天背包估算；konart/esafak/reacharavindh 报告 z.ai API 慢/配额消耗快；yorwba 反驳为跨用户大批量、吞吐优先的取舍；Argonautlabs（披露自推）M5 Max 128G 用 NVMe 流式专家跑 GLM-5.3 744B：单盘 ~2 tok/s → 四盘 RAID 3.5 → 内部版 4.2 tok/s，输出 byte-identical。
- 可信度：中低（作为"推翻"不成立；作为"厂商主张悬置 + 客户体感反差"可靠）。
- 来源：https://news.ycombinator.com/item?id=49737922
- 新事实：本周传播最广的厂商推理效率叙事仍是零复现状态。

## 5. llama.cpp #28761：sm_75 FlashAttention 的 32-token Q-tile 上限被双向基准证伪（附 ptxas 寄存器溢出证据）
- 日期：2026-09-11｜作者：kksfvk
- 事实：DKQ=128 时 tile64 即使短 KV 也更快（8K 处 +3.6%）；DKQ=256 时短 KV tile64 惨败（8K 处 −37%）但长 KV 大胜（+19–50%）——固定 cap 两个方向都次优；ptxas 显示寄存器溢出（348B）只发生在 head_dim=256。
- 可信度：中（单人报告但基准 + 汇编证据链齐全；Turing 小众但可复现）。
- 来源：https://github.com/ggml-org/llama.cpp/issues/28761
- 新事实：外部实测修正维护者内嵌假设的典型样本。

## 已查未过线 / 排除
- SGLang #39087（已报道的量化 DFlash2 坍塌）：重新核验仍 0 评论、未关闭、关联 PR #39254 未见合并——无实质新事实，本期不重复。
- SGLang #36599（GLM-5.3-Flash NVFP4 NextN 量化 bug）：窗口内无新评论。
- Swift-Qwen3.8-27B（HN 9-16 x1.95）：所称 Reddit 独立评测原帖无法核实，不达"独立对照"标准。
- 知乎 DFlash/DSpark vLLM 实测文（1.96–2.09x）：发布于 08-07/更新 08-23，窗口外。
- 盲区：V2EX/知乎两次抓取超时；X 无命中。
