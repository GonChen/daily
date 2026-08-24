# 2026-08-25 去重基线

## 最近两期已覆盖，不可作为主事实重复

- 2026-08-24：FlashInfer #4593 的 SM100/SM103 block-sparse VSA，作者报告 canonical 1.902192×、FastWan E2E 1.015714×。
- 2026-08-24：FlashInfer #4686 的 SM100/SM103 W4A16 dense GEMM，B300 几何均速 1.029759×，冷调优 196.68s→417.83s。
- 2026-08-24：Claude Code v2.1.239 的 1.1×数据驻留 premium、Bedrock proxy 重试/重复计费修复和 HTTPS_PROXY 凭证检查。
- 2026-08-24：SGLang #34237 的 LFM2 工具调用 parser，19 个 regression case、42 payload differential harness。
- 2026-08-23：SGLang v0.5.18 TP 数据、DeepSeek Harness RC1/RC2、DeepGEMM #410 RFC、vLLM #52989，以及 NVIDIA/OpenAI Ohio 项目。

## 选题约束

只接受相对上述事实具有可链接新一手事实的候选。性能数字必须带硬件、负载、测量范围与局限；单个夜构、版本号递增或无用户/部署影响的 PR 仅可入雷达。8/24 在芯片供应链、数据中心/资本、中文产业和论文窗口均为安静，不能用旧闻补量。
