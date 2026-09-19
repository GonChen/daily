# 2026-09-12 dedup baseline

## 最近两期已覆盖：不得原样重述

| 事实 / 主题 | 最近出现 | 本期处理规则 |
|---|---:|---|
| SGLang #39068：DSpark V4.1 simulated decode 761.03→853.49 tok/s | 2026-09-11 | 仅在有 GPU CI、自然 acceptance、完整 serving A/B 或新硬件数据时更新 |
| vLLM #51692：MI350 ROCm bpreshuffled FP8、DPA/EP QPS 区间 | 2026-09-11 | 仅在解除 AITER gate、release 或新 route/负载实测时更新 |
| FlashInfer #4967：B200/B300 Cake KDA 约1.05× | 2026-09-11 | 仅在 release、服务 A/B、backend hit rate 或新形状证据时更新 |
| DeepSeek Harness dsh-v0.1.5-rc.1：V4.1-Flash、连续子代理、proxy 继承 | 2026-09-11 | RC 日常 bump 不入选；只跟踪 GA、兼容性事故或实质功能变化 |
| SGLang #39087：量化 DFlash2 接受率坍塌 | 2026-09-11 | 只跟踪维护者确认、patch 或独立复现 |
| 8/30 的 ROCm PD fused top-k、AITER eager metadata、MiMo audio collective | 2026-08-30 | 只跟踪 CI、修复或独立复现；不回顾旧 benchmark |

## 本期动态发现重点

优先寻找 2026-09-11 至 2026-09-12 的新 release、合入 PR、官方模型/产品资料、监管或公司披露，以及具名社区复现。任何候选必须明确说明相对本表的新事实。
