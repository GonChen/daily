# 2026-09-11 fallback discovery

## 子代理降级记录

八个 `intel-scout` 在首条模型事件前全部失败，错误均为 `pi API error: Connection error`。在继承现有小写代理变量外，又显式注入 `HTTP_PROXY`、`HTTPS_PROXY`、`ALL_PROXY`、`NO_PROXY` 后，单个 `intel-scout` 与 `intel-editor` 复测仍失败。`pi auth check --model br/deepseek-v4-flash --json` 返回 `ready`。这证明此轮失败不能归因于缺少大写系统代理变量；没有据此推断上游服务的根因。

主控改用 GitHub API 和网页检索读取合入 PR、官方 release 与具名 issue，并保留每条来源的类型与限制。

## 候选与事实

| 候选 | 类型 | 可用事实 | 边界 | 结论 |
|---|---|---|---|---|
| [SGLang #39068](https://github.com/sgl-project/sglang/pull/39068) | 已合入 PR；作者报告 | 4×GB300、TP4/EP4、BS1、4,096/1,024、模拟 acceptance=5.5：streamed decode 761.03→853.49 tok/s（+12.15%）；C2 比前一版本 +6.37% | 不含 prefill；模拟 acceptance 不测自然接受率/质量；GPU CI 未运行 | Top5 |
| [vLLM #51692](https://github.com/vllm-project/vllm/pull/51692) | 已合入 PR；作者报告 | 8×MI350、DeepSeek-V3、1k/1k：TP8+DPA 各并发 QPS +4.61% 至 +8.14%；TP8+EP -0.39% 至 +9.01%；GSM8K 约 0.948 对 nightly 0.943 | `VLLM_ROCM_USE_AITER_FP8BMM=0` 是已知前提；作者环境 | Top5 |
| [FlashInfer #4967](https://github.com/flashinfer-ai/flashinfer/pull/4967) | 已合入 PR；作者报告 | B200 21-shape 1.0491×、B300 21-shape 1.0504×（candidate / CuTe DSL latency）；全组 1,315 B200 cases 1.0241× | Cake 为显式/条件自动路径，默认仍 CuTe DSL；综合表含未重测行 | Top5 |
| [DeepSeek Harness dsh-v0.1.5-rc.1](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.5-rc.1) | 官方预发布 | 默认 DeepSeek-V4.1-Flash；可续聊子代理排队、编辑、Steer/停止；动态 system prompt 不失 KV cache；外发请求遵从 HTTP(S)/ALL/NO_PROXY | RC，非正式 GA；无任务成功率或性能数字 | Top5，明确预发布 |
| [SGLang #39087](https://github.com/sgl-project/sglang/issues/39087) | 具名社区一手报告 | 2×RTX3090 TP2：量化 DFlash2 accept len 1.03（n=422）、rate 0.004、约 38 tok/s；同模型 BF16 draft 3.71（n=100）、0.61、约171 tok/s | 未确认、未修复；仅一组模型/硬件 | Top5，风险信号 |
| [TensorRT-LLM #18541](https://github.com/NVIDIA/TensorRT-LLM/pull/18541) | 已合入 PR | KVCM2 长序列 burst resize 的 topology-aware copier 与并发 API；78 C++ +220 Python tests pass | 无服务 A/B 数字 | 雷达 |
| [vLLM #48247](https://github.com/vllm-project/vllm/pull/48247) | 已合入 PR；作者报告 | 8×MI300、DP attention + TP experts，1k/1k 的 TPOT 约改善 3% | 仅 uniform batch、DP group；与 #51692 同类 ROCm 服务优化 | 雷达 |
