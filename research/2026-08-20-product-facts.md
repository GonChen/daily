# 2026-08-20 research ledger

Window: 2026-08-17 06:00 to 2026-08-20 06:00 CST. Dynamic discovery ran before fixed radar: six bilingual Exa searches covering chips/supply chain, infrastructure/capital, models/agent, inference/systems, papers/open source and Chinese industry. Candidates without a new primary fact were demoted to radar/background.

## Main facts used

1. **NVIDIA / SB Energy / OpenAI Ohio — SEC 8-K, 2026-08-17.** NVIDIA reports residual-value guarantees for leases covering about **4.25 IT-GW** at PORTS-Pike; its aggregate payment obligation is capped at **$105B** for the initial commitment, conditional on ready-for-service, expected from 2028. OpenAI is tenant and has agreed to reimburse/indemnify actual payments. NVIDIA may elect credit support for about **3.8GW** more. Boundary: guarantee cap is neither current cash spend nor booked revenue. Sources: [8-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000069/nvda-20260817.htm), [NVIDIA explanation](https://blogs.nvidia.com/blog/securing-the-infrastructure-of-intelligence/).
2. **DeepSeek Harness RC.8 — official release, 2026-08-19.** Adds configurable native image requests, image inputs in goal/plan, installable Claude Code/Codex profile bundles, Codex non-interactive permission modes/named instances, concurrent web search and persistent Windows PowerShell. SQLite structure is incompatible. Source: [release](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.0-rc.8).
3. **Cursor cloud agents — official changelog, 2026-08-19.** Event subscriptions for PRs/Slack/schedules, long-lived goals, custom modes and isolated cloud subagents. Boundary: no published success rate, cost, or autonomous-merge guarantee. Source: [Cursor changelog](https://cursor.com/changelog).
4. **Claude Code 2.1.236 — official release, 2026-08-19.** Adds `ANTHROPIC_DEFAULT_MODEL`, one-shot cross-session `notify_when_idle`, and macOS sandbox wildcard read-deny precedence; includes background-session and MCP-log repairs. Source: [release](https://github.com/anthropics/claude-code/releases/tag/v2.1.236).
5. **SGLang NPU speculative path — merged PRs, 2026-08-19.** #35570 adds `SGLANG_SPEC_V2_ZERO_BUBBLE` support on NPU and pinned/non-blocking metadata transfers; #35572 adds batch-matmul-transpose autotune configs. Accuracy/speed results were not supplied, therefore no performance claim. Sources: [#35570](https://github.com/sgl-project/sglang/pull/35570), [#35572](https://github.com/sgl-project/sglang/pull/35572).

## Fixed radar, only material changes

- DeepSeek official organization scan: `deepseek-harness` pushed/released on 8/19; DeepGEMM, DeepEP, FlashMLA, DeepSpec, 3FS, DualPipe, EPLB/LPLB had no newly qualifying release/tag/merged main-card fact in the window. Source: [organization](https://github.com/deepseek-ai).
- vLLM release remains v0.27.1; a 8/19 Kimi K3 MoE benchmark config bugfix (#50082) allows its benchmark script to read 896 experts/top-k 16, but is not a runtime speed claim. Source: [#50082](https://github.com/vllm-project/vllm/pull/50082).
- TensorRT-LLM remains v1.3.0rc24; PyTorch stable remains 2.13.0; FlashInfer published a nightly with no feature notes. These are tracked, not Top-5 content.
- OpenAI Codex released 0.149.0-alpha.1 but its release body contains no functional notes. Source: [release](https://github.com/openai/codex/releases/tag/rust-v0.149.0-alpha.1).

## Market snapshot

Nasdaq official secondary close for 2026-08-19: NVDA $217.56 (-0.99%), AMD $466.42 (-3.71%), AVGO $362.48 (-4.61%). Prices are facts only; no causal attribution is made. Sources: [NVDA](https://api.nasdaq.com/api/quote/NVDA/info?assetclass=stocks), [AMD](https://api.nasdaq.com/api/quote/AMD/info?assetclass=stocks), [AVGO](https://api.nasdaq.com/api/quote/AVGO/info?assetclass=stocks).
