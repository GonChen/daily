# 2026-08-19 前沿计算情报日报｜研究底稿

资料截止 2026-08-19 06:00 CST。按 `templates/source-policy.md` 先做六组中英文动态搜索（芯片/供应链、基础设施/资本、模型/Agent、推理系统、论文/开源、中文产业），再以官方 GitHub、产品文档、PJM 文件和 Nasdaq 数据核验。Top 5 中 vLLM PCP、SGLang Kimi 工具调用、PJM、DeepSeek API/Harness、MI325X KDA 均有相对前两期的新一手事实。

## 1. vLLM：DeepSeek V3.2 的 PCP

- PR：https://github.com/vllm-project/vllm/pull/52046
- 8/18 合入；正式版仍是 v0.27.1。
- 事实：sparse MLA 和 indexer 采用 sequence shard 的 PCP；新生成 KV 仍需 gather `kv_c`、`k_pe`、`indexer_k` 后才写入保持复制的 KV cache；MHA 路径禁用 PCP。
- 性能（PR 作者报告）：在叠加 GLM‑5.2→DeepSeek V3.2 routing 的 B300、GLM‑5.2 NVFP4、32k max batched tokens、16k long-prefill threshold、prefill-only profile 中，PCP8 p50 366.9ms，TP8 p50 973.9ms，即 2.65×。
- 边界：主线提交、特定硬件/模型/配置的 prefill profile；不得写成全工作负载吞吐或正式 release。

## 2. SGLang：Kimi‑K3 tool-call 正确性

- PR：https://github.com/sgl-project/sglang/pull/34881
- 8/18 合入；正式版仍是 v0.5.17。
- 事实：一个 Kimi‑K3 agent workload 约有 190 条 tool-call parsing error/日；作者找出四类问题：
  1. native-format 输出错误进入 JSON-array decoder；
  2. `tool_choice=required` 与 `response_format`/regex/EBNF 同时使用时 tool constraint 被丢弃；
  3. think-close 前的完整 tool section 被算入 reasoning；
  4. 截断 tool section 在 stream-end 时静默丢失。
- 新行为：不可满足的 required/named tool + output constraint 返回 400；auto 保持 warning；截断/零完整调用路径改为告警并释放保留文本。
- 测试：PR 报告修复前 8 failed/6 passed，修复后 0 failed；相关 CPU suites 180 passed、53 subtests passed。
- 边界：无速度/准确率 benchmark；“190/日”来自该工作负载，不外推为全局错误率。

## 3. PJM：新大负载的 IRAS 框架

- 官方说明：https://insidelines.pjm.com/pjm-proposes-framework-to-connect-data-centers-without-compromising-reliability-affordability/
- Reuters：https://www.reuters.com/business/energy/pjm-proposes-plan-buy-more-power-data-centers-2026-08-13/
- PJM 8/13 提交提案：为未带来新增供电、也未被 Reliability Backstop Procurement 覆盖的新 Large Load 建立 Interim Resource Adequacy Service（IRAS）。
- 电网接近危险供给时，PJM 将通知 LSE 减少或转移这些新的大负载需求，先于对传统消费者的措施。
- PJM 估计 2024–2030 年 32GW 预测新增负载中 30GW 来自数据中心，并请求 FERC 60 天内接受。
- 边界：这是 PJM 提案，不是已生效条例；不应推断所有数据中心或已有容量客户都会被同样削减。

## 4. DeepSeek：API、价格、官方 GitHub harness

- Changelog：https://api-docs.deepseek.com/updates/
- Pricing：https://api-docs.deepseek.com/quick_start/pricing
- Official org：https://github.com/deepseek-ai
- Harness RC：https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.0-rc.7
- V4‑Pro 在 8/13 已于 App、Web、API GA，调用名为 `deepseek-v4-pro`。
- 价格表：V4‑Pro context 1M、max output 384k；cache-hit input 为 peak $0.044 / off-peak $0.022 每 1M token；V4‑Flash 对应 $0.014/$0.007。并列出 V4‑Flash‑0731、V4‑Pro‑0813。
- `deepseek-harness` v0.1.0-rc.7（8/17）：插件可注册 settings card；Codex/Claude Code 子代理接入 Job Panel；MCP/ACP 支持持久图片与 PTC nested image forwarding；DeepSeek 新增 `low` reasoning effort，默认 `high`。
- 边界：API model/价格可变；harness 为 RC。上述依赖官方 API/docs 与 GitHub release，而非透明度页。

## 5. vLLM：MI325X fused KDA decode

- PR：https://github.com/vllm-project/vllm/pull/52293
- 8/18 合入；将 Kimi‑K3 fused KDA decode 从 gfx950 扩到 gfx942（MI325X），kernel body 不变。
- PR 报告：KDA block 从约 16 kernels、~73.96μs/layer，变为 1 kernel、7.77μs/layer（约 9.5×）；TP8、256 input/256 output、max concurrency 4 下 mean TPOT 425.95→422.66ms（-0.77%），P99 427.64→424.19ms（-0.81%），output 9.29→9.36 tok/s（+0.75%）。
- 解释（作者）：MXFP4 MoE、MLA 和 TP8 collectives 是当前主导成本；局部 KDA 少了约 66μs/layer，不等于整体 decode 同比例变快。
- 边界：主线 PR、具体测试；正确性/评测结果在 PR 正文列为尚待填充的人工验证事项，不能写成已经完整验收。

## 6. 国产 GPU：沐曦 Qwen3.8 Day‑0 适配

- 官方：https://www.metax-tech.com/ndetail/12639.html
- 8/13 公告：沐曦与 FlagOS 完成 Qwen3.8‑2.4T‑A95B 的 Day‑0 部署/精度对齐验证；提供 vLLM‑plugin‑FL 和 SGLang‑plugin‑FL。
- 官方示例为 INT8 模型、TP16、PP2、`max_num_batched_tokens=8192`、`max_num_seqs=32`。
- 边界：是部署配方与厂商验证，不含与 NVIDIA/AMD 的同任务横评，不写性能领先。

## 7. Agent 工具

- Claude Code v2.1.235：https://github.com/anthropics/claude-code/releases/tag/v2.1.235
  - 加可选 spellcheck；修 language-server 重连时 whole-prompt cache invalidation；修 permission comment Shift+Tab 意外 session-wide edit；大 SendMessage 提前拒绝而非静默丢失；减少后台 cloud session 反复扫描/渲染的 CPU/内存。
- Codex alpha.22/.23：release 页面只有构建标题，不写功能判断。

## 8. 框架/库覆盖

- SGLang 最新正式版 v0.5.17；vLLM v0.27.1；TensorRT‑LLM v1.3.0rc24；PyTorch v2.13.0。
- TensorRT‑LLM 8/18 主线：sparse FMHA forward 移除 spurious sync（无端到端性能数）；image-edit serving endpoint；Kimi attention residual snapshot preallocation。来源：https://github.com/NVIDIA/TensorRT-LLM
- FlashInfer 8/18 有 nightly v0.6.18 构建，但无 feature notes；FlashAttention/FlashMLA/cuDNN/cuBLAS 无足以改变判断的当天正式发布。

## 9. 市场

- Nasdaq 8/18 收盘：NVDA $219.74 (-2.34%)、AMD $484.39 (-4.27%)、AVGO $379.83 (-3.21%)、TSM ADR $413.37 (-4.08%)、MU $940.76 (-7.02%)。
- 仅记录价格事实；不对单日共同下跌赋予单一新闻因果。

## 10. 论文窗口与编辑决策

- 本轮 arXiv 新批次未得到足以替换主论文区的一手可靠元数据，因此保留 8/13 的 OpScale、DARTree、Reduced Matrix Multiplication、Beyond Final Scores，并明确为近周背景、作者报告。
- 不重复 8/18 的 NVIDIA/SB Energy 担保与 Qwen3.8 权重新闻为 Top 5；它们没有新增的一手事实。
- 本期标题与深度解读围绕“admission control”：PCP/KV、agent tool schema、PJM large-load 三个层面都以可见的约束取代静默失败。
