# 2026-08-21 research ledger

Dynamic discovery ran six bilingual searches across chips, infrastructure, model/agent, inference/system, papers/open-source and Chinese industry before fixed radar.

- **vLLM #52989, merged 8/20:** FlashInfer CUTLASS expert paths used default `tune_max_num_tokens=8192` despite a larger vLLM parallel-aware maximum. The PR forwards the actual bound to FP8/BF16/LoRA/MXINT4 paths; focused tests pass, end-to-end performance rerun pending. [PR](https://github.com/vllm-project/vllm/pull/52989)
- **SGLang #35554, merged 8/20:** extends Kimi‑K3 packed-MXFP4 automatic FlashInfer MoE selection to SM107. The PR says stock artifact numeric/memory/performance qualification is pending; no performance claim. [PR](https://github.com/sgl-project/sglang/pull/35554)
- **Codex 0.149.0, 8/20:** official stable release adds interactive agents dashboard, queue, cwd commands and expanded doctor; resumed/forked threads preserve permission profiles. [release](https://github.com/openai/codex/releases/tag/rust-v0.149.0)
- **Claude Code 2.1.238, 8/20:** releases stale subagent tool results from long sessions, adds runner/proxy controls and makes cross-session refusal/queue drops explicit. [release](https://github.com/anthropics/claude-code/releases/tag/v2.1.238)
- **ATFlash, author paper:** reports frequency-window attention ports for FA4/FlashInfer; Qwen2.5-7B-1M setting reports 1.31x whole-request speedup at 1M context. Not an upstream release or independent reproduction. [paper](https://arxiv.org/html/2608.02947v1)
- **DeepSeek official radar:** organization metadata showed DeepEP push timestamp 8/20, but GitHub commits API’s newest visible commit remains 8/4; no qualifying new release/tag/merged fact was promoted. [organization](https://github.com/deepseek-ai)
