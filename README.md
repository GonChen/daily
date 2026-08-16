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
2. 生成器采集公开 GitHub Releases、Google News RSS 与 arXiv 数据；Codex 负责编辑判断与质量检查。
3. 当天页面写入 `docs/archive/YYYY-MM-DD.html`，结构化结果写入 `docs/data/`，`docs/index.html` 始终指向最新版。
4. Codex 提交并推送更新后，GitHub Actions 只负责部署 `docs/` 到 GitHub Pages，不调用任何模型。

> 这是本地 Codex 自动任务：计划运行时电脑需保持开机，并让 Codex 可运行。若需要不依赖本机的纯云端运行，可再切回 GitHub Actions + 模型 API。

## 手动生成

在 Codex 中可以随时手动运行同一日报任务；仓库的 **Actions → Publish Daily Brief to Pages → Run workflow** 只会重新发布现有页面。

本地运行：

```bash
python scripts/generate_daily.py
```

没有模型令牌时，生成器会生成来源摘要版页面，便于自动任务继续编辑与检查。

## 可信度约定

- `事实`：官方公告、GitHub Release、监管文件或市场数据
- `报道`：可信媒体报道，尚无正式公告
- `传闻`：市场通讯或二手转述，不能写成定论
- `论文`：预印本作者报告，等待独立复现
- `推断`：编辑分析，明确与事实分开

页面仅用于技术和产业研究，不构成投资建议。
