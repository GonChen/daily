# 2026-08-23 选题定稿

降级说明：`intel-scout` 两轮并发与一轮串行均未在可操作窗口内完成；候选池来自 `fallback-discovery.md`，并由 `intel-editor` 独立复核。只有三条满足准入线，因此本期不补足为五条。

| 候选 | 新颖度 | 物质性 | 可验证性 | 准入项 | 结论 |
|---|---:|---:|---:|---|---|
| SGLang v0.5.18 | 5 | 5 | 5 | 量化性能、正式发布 | 入选 |
| DeepSeek Harness dsh-v0.1.1-rc.1/rc.2 | 4 | 3 | 5 | 产品/可用性变化 | 入选，须标 RC |
| DeepGEMM #410 | 4 | 2 | 3 | 具名社区一手信号 | 入选，仅作信号 |
| Claude Code v2.1.240 | — | — | — | 无 | 落选：仅笼统 bug-fix 说明 |
| Codex 0.150.0-alpha.7 | — | — | — | 无 | 落选：仅版本名 |
| FlashInfer nightly | — | — | — | 无 | 落选：nightly 不是主内容 |
| DeepEP / DeepGEMM 主线 / FlashMLA | — | — | — | 无 | 公开面安静 |

## 入选

1. **SGLang v0.5.18**（推理与系统）：官方发布在特定 Qwen3-32B/H100、DeepSeek-V4-Pro/B200 和 DeepSeek-V4-Flash/TP4 Blackwell 配置下给出启动和通信路径数据。升级同时改变 torch、缓存目录和默认 MoE 行为，收益不应外推为通用值。[release](https://github.com/sgl-project/sglang/releases/tag/v0.5.18)
2. **DeepSeek Harness RC1/RC2**（模型与 Agent）：RC1 引入 Vision-Exp 适配并修复 Bubblewrap `/proc/<pid>/root` 逃逸；RC2 优先使用 Files API 上传和复用图像。无官方性能数字，RC 不等于 GA。[RC1](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.1-rc.1) / [RC2](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.1-rc.2)
3. **DeepGEMM #410**（开源社区）：具名用户提出 opt-in chunk-ready symmetric-buffer RFC，设想令早期 token chunk 的 dispatch 与上游生产重叠。没有 benchmark、实现或合入承诺，不能据此作性能结论。[issue](https://github.com/deepseek-ai/DeepGEMM/issues/410)

## 配额检查

- Top 条数：3；按准入线收缩，未凑数。
- 主题桶：推理与系统、模型与 Agent、论文与开源社区，共 3 个。
- 动态发现：3 条；社区一手来源：1 条；固定雷达无变化触发：0 条。

## 深挖题

- 已发布的启动/TP 通信重叠，和仍为 RFC 的 MoE 输入流式交接，在成熟度、指标和证伪条件上有何区别？
- DeepSeek Harness 在同一 RC 中组合多模态输入、文件复用和 sandbox 修复，对部署验证意味着什么？
