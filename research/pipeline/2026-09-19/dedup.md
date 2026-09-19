# 2026-09-19 dedup baseline

窗口说明：上一期正式发布为 2026-09-11；09-12 流水线只完成 dedup 基线后中断，未发布。本期扫描窗口为 **2026-09-11 至 2026-09-19**（8 天），与最近两期正式 ledger（09-11、08-30）及下表去重。

## 最近两期已覆盖：不得原样重述

| 事实 / 主题 | 最近出现 | 本期处理规则 |
|---|---:|---|
| SGLang #39068：DSpark V4.1 fused verify 761.03→853.49 tok/s（模拟 acceptance） | 2026-09-11 | 仅在有 GPU CI、自然 acceptance、含 prefill 的 serving A/B 或新硬件数据时更新 |
| vLLM #51692：MI350 ROCm bpreshuffled FP8、DPA/EP QPS 区间 | 2026-09-11 | 仅在解除 AITER FP8BMM gate、release 或新 route/负载实测时更新 |
| FlashInfer #4967：B200/B300 Cake KDA ≈1.05×，默认仍 CuTe DSL | 2026-09-11 | 仅在 release、服务 A/B、backend hit rate 或新形状证据时更新 |
| DeepSeek Harness dsh-v0.1.5-rc.1：V4.1-Flash、可续聊子代理、proxy 继承 | 2026-09-11 | RC 逐日 bump 不入选；只跟踪 GA、兼容性事故或实质功能变化 |
| SGLang issue #39087：量化 DFlash2 accept rate 0.004 坍塌 | 2026-09-11 | 只跟踪维护者确认、patch 或独立复现 |
| 8/30 ROCm PD fused top-k、AITER eager metadata、MiMo audio collective | 2026-08-30 | 只跟踪 CI、修复或独立复现；不回顾旧 benchmark |
| 8/30 Codex MCP/sandbox 治理、FlashInfer Blackwell all-gather binding | 2026-08-30 | 仅在实质功能或行为变化时更新 |

## 本期动态发现重点

优先寻找 2026-09-11 至 2026-09-19 的新 release、合入 PR、官方模型/产品资料、监管或公司披露，以及具名社区复现。8 天窗口内任何候选必须明确说明相对本表的新事实；写不出"相对上两期的新事实"即降级。特别核查 tracker.md 中 50+ open 事项是否在窗口内有 CI 转绿、维护者确认或独立复现等触发。
