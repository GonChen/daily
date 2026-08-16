# Daily AI Intelligence Brief

每天北京时间 **06:00** 由 Codex 自动任务生成一份中文 AI / GPU / 推理系统情报日报，并发布到 GitHub Pages。

## 关注范围

- GPU 与 AI 芯片：NVIDIA、AMD、国产 GPU / 加速器、昇腾、寒武纪、壁仞、沐曦
- 推理框架：SGLang、vLLM、TensorRT-LLM、PyTorch
- 算子库：FlashAttention、FlashInfer、FlashMLA、cuDNN、cuBLAS
- 开放模型：DeepSeek、GLM、Kimi、Qwen
- Agent 与开发工具：OpenAI / Codex、Claude Code、Cursor、pi
- 推理加速：投机解码、KV Cache、PD 分离、稀疏/线性注意力、量化 MoE、调度与算子优化
- 产业资本市场与重要宏观变化

## 工作方式

1. Codex 自动任务每天北京时间 `06:00` 返回同一任务，搜索、筛选并生成日报。
2. Codex 以 `templates/daily-template.html` 为内容密度、栏目结构、交叉跳转与视觉质量基线；不得退化成自动来源摘要页。
3. 当天页面写入 `docs/archive/YYYY-MM-DD.html`，研究底稿写入 `research/`，`docs/index.html` 始终指向最新版。
4. Codex 提交并推送更新后，GitHub Actions 只负责部署 `docs/` 到 GitHub Pages，不调用任何模型。

> 这是本地 Codex 自动任务：计划运行时电脑需保持开机，并让 Codex 可运行。若需要不依赖本机的纯云端运行，可再切回 GitHub Actions + 模型 API。

## 手动更新

在 Codex 中可以随时手动运行同一日报任务；仓库的 **Actions → Publish Daily Brief to Pages → Run workflow** 只会重新发布现有页面。

编辑时先复制 `templates/daily-template.html`，替换日期、事实、来源与编辑判断；保留 Executive readout、30 秒结论、分类雷达、推理加速路线图、深度解读和跟踪清单。发布前检查全部内部锚点、外链、桌面与手机布局。

2026-08-16 的原始高质量报告同时保存在 `docs/archive/2026-08-16.html`，并作为模板冻结保存。

## 可信度约定

- `事实`：官方公告、GitHub Release、监管文件或市场数据
- `报道`：可信媒体报道，尚无正式公告
- `传闻`：市场通讯或二手转述，不能写成定论
- `论文`：预印本作者报告，等待独立复现
- `推断`：编辑分析，明确与事实分开

页面仅用于技术和产业研究，不构成投资建议。
