# 2026-10-03 community 桶候选

## 1. vLLM FlashMLA 稀疏解码在 Hopper 重新吃掉 8 GiB 瞬时显存——上游内核同步静默回滚了旧 OOM 守卫
- 日期：9/29 issue、修复 PR 同日已提｜平台/作者：vLLM #59305，作者 drakosha（CONTRIBUTOR）
- 事实：FlashMLA 上游 V4.1 同步（FlashMLA#20，commit c112cc1）删掉了 #19 引入的 `num_sm_parts > 1` 分配守卫；vLLM 经 #56893 pin bump 被动引入后，SM90 混合批次路径恢复为每次调用分配随 `--max-num-batched-tokens` 线性增长的 split-KV 累加器。H200 NVL 实测（fp8_ds_mla、top-k 2048）：T=1024→256.5 MiB、T=8192→2052 MiB、T=32768→8208 MiB，与公式 `(b+num_sm_parts)*s_q*h_q*d_v*4` 精确吻合；#53413 当年正因此 OOM。对照：恢复守卫的 FlashMLA#29 修复后 8192 tokens 下 2052 MiB→0，输出 bit-identical。
- 可信度：高（环境完整、数字与公式闭合、修复可对照、附测量脚本）。
- 来源：https://github.com/vllm-project/vllm/issues/59305
- 新事实：新失效模式——"上游内核库同步静默回滚已知修复"；与 FlashMLA 9/30 破坏性收窄直接联动，是 DeepSeek MLA 用户升级 pin 前的检查点。

## 2. llama.cpp CPU 端 Flash Attention 小批次路径 F16 累加器溢出 → 静默输出 -inf/NaN；三次迭代修复
- 日期：9/30 issue、10/1 确认+修复｜平台/作者：llama.cpp #29774，报告者 rafacarrascosa；复现/修复者 ServeurpersoCom、jeffbolznv（具名 CONTRIBUTOR）
- 事实：CPU FA 的 one-chunk（小批次/decode/长 prompt 尾部）内核用 F16 而非 F32 累加，Nemotron 3 Nano 4B Q8_0 在 8196 token 重复词 prompt 上 sum=-inf、输出全坏；`-fa off` 对照正常、CUDA 正常。修复迭代：第一版直接 F32 累加——x86 16k 上下文 decode 掉速最高 17%；第二版 F16 数学+每 256 位 folding 进 F32——repro 干净；第三版按 CUDA/Vulkan 的 `FATTN_KQ_MAX_OFFSET` 思路——Ryzen 9 9950X3D 上 0/8k/16k 三点 10.37-11.57 t/s 与 master 打平。
- 可信度：高（第二方独立复现、量化了正确性修复的性能代价、一键复现脚本）。
- 来源：https://github.com/ggml-org/llama.cpp/issues/29774
- 新事实：纯 CPU 推理长 prompt 的 FA 数值静默损坏（不是变慢而是结果错）；首次披露"直接修正确性要付 17% decode 代价"的量化权衡。

## 3. llama.cpp GLM-5.3-Flash 在 Apple M5/Metal 上解码间歇停顿 1–9 秒/token——融合 Lightning Indexer 静默回退 CPU，自动探测被硬编码关闭
- 日期：10/02｜平台/作者：llama.cpp #29867，报告者匿名，label bug-unconfirmed
- 事实：M5 上 GLM-5.3-Flash UD-IQ3_XXS（-ngl 999 -fa on -c 65536）每几十 token 后停顿 1-9 s/token，均值 ~31 t/s→0.5-10 t/s。根因：Metal lightning indexer 内核只支持恰好 64 个 indexer heads（ggml-metal-impl.h#L133），GLM-5.3-Flash 只有 32 个 → `supports_op` false → 回退 CPU；但 `fused_lid` 硬编码启用、`auto_flid=false`，本可捕获回退的探测永远不跑，历史逃生口 `LLAMA_FUSED_LID_DISABLE` 不再暴露。对照：关掉融合 indexer 停顿消失；本地改一行 `auto_flid=true` 恢复 ~31 t/s。
- 可信度：中（单报告者、bug-unconfirmed；症状量化完整、根因落到行号、修复自验）。
- 来源：https://github.com/ggml-org/llama.cpp/issues/29867
- 新事实：新失效模式——"融合算子头部数不匹配 → 静默 CPU 回退 + 自动探测被硬编码绕过"，GLM-5.3-Flash 在 Apple Silicon 上 30 倍量级损失。

## 4. vLLM DSpark 投机解码 lookahead 少留 1 个槽位 → drafter 越界写，可覆写其他请求的 KV cache
- 日期：9/28｜平台/作者：vLLM #59104，作者 notimesea（NONE，声明 Codex 辅助），0 评论、无维护者回应；随附修复 PR #59105
- 事实：`sample_from_anchor=false` 的 DSpark checkpoint 下 drafter 用 N+1 个 query 位置（bonus token + N draft），`num_lookahead_tokens` 只预留 N；137 prompt + 7 draft + 16-token 块时调度器分配 144 槽而 drafter 还要写 position 144，可从空闲表尾读到陈旧 block ID、覆写另一请求的目标 KV，表现为重复畸形输出。环境：H200、vLLM 0.30.1rc1.dev284、gemma-4-31B-it + dspark speculator、FA4、eager。对照：第 9 批稳定复现；修复后 3 次冷启动 × 20 批 × 16 请求零事故；无权重合成 CUDA 复现器修复前 fail/修复后 pass；GPU instrumentation 单独确认 KV 覆写。
- 可信度：中（复现充分但孤证、AI 辅助、无维护者确认，"N vs N+1"是否适用所有锚点模式待核）。
- 来源：https://github.com/vllm-project/vllm/issues/59104
- 新事实：投机解码分配器 off-by-one 可造成跨请求 KV 串写——投机路径的槽位预留是新暴露的隔离性失效面。

## 5.（次级）llama.cpp qwen4exp indexer 分数一次性物化：131k 上下文约 4 GB 中间张量，修复后 compute buffer 减半
- 日期：10/01 PR（open）｜作者 ServeurpersoCom、确认者 LucaAmigoni（具名）
- 事实：indexer 一次算完所有 head 分数再整份拷贝，131k ctx 下约 4 GB 中间量只为产出 0.5 GB 结果（8 倍），是全图最大 buffer；改逐 head 就地 relu 增量累加后 CUDA compute buffer 3.0→1.5 GiB（131k/ub2048）、11.7→5.6 GiB（262k/ub4096），logits bit-exact，速度不变，双卡不再 OOM。
- 来源：https://github.com/ggml-org/llama.cpp/pull/29825
- 新事实：量化披露"长上下文 indexer 分数物化"显存爆炸点。

## 6.（边缘）Magnitude（YC S25）Launch HN：自优化推理引擎发布当天遭遇"装不上/载不动"反例
- 日期：9/30-10/2｜HN 194 分 97 评，创始团队具名回应
- 事实：官方宣称比 llama.cpp 快至 2×（M4 Pro decode 30→57 tok/s）；评论区 M1 16GB 五个模型载不进、Win11+RTX PRO 1000 硬件检测失败；创始人承认"M5+ Mac 已知问题"与"多处显存超预留 bug"。反例未量化，可信度中低。
- 来源：https://news.ycombinator.com/item?id=49911995
- 新事实："发布性能主张 vs 可复现性"连续剧新样本。

## 排除
vllm-ascend #1728"18% 回归"为 2025-07 旧 issue；Reddit/知乎窗口内无可准入命中；SGLang #39087、Ollama 泄漏根因、#57427 状态均无窗口内更新。
