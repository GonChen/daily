# 2026-08-29 research ledger

## 采集、去重与子代理状态

已以 8/27、8/28 ledger、pipeline 与 tracker 去重，详情见 [dedup](pipeline/2026-08-29/dedup.md)、[fallback discovery](pipeline/2026-08-29/fallback-discovery.md) 和 [selection](pipeline/2026-08-29/selection.md)。动态发现扫描 SGLang、vLLM、FlashInfer、TensorRT-LLM 的 8/28 merged PR，并以四组社区 issue 检索补齐非官方信号。基础设施/资本、模型/Agent 产品、中文产业和论文没有同时满足窗口、第一方或可复现证据与量化影响的新增事实，安静处理。

两轮八桶 `intel-scout` 均在超过一分钟后无首个模型事件，已停止。`pi auth check --model br/deepseek-v4-flash --json` 返回 `ready`，进程继承 `HTTP_PROXY`、`HTTPS_PROXY`；降级原因是 **scout 模型首事件停滞，不是认证或系统代理变量缺失**。主控一手核验、`intel-editor` 与两项 analyst 审校继续执行。

## 入选事实

- **SGLang #36094，8/28 合入：**DSV4 MI355X decode 的 `_kv_splits_heuristic` 原先对 H=128、T=32/64/128 过分 split；PR 将 `target_wg_per_cu` 2.0→1.5、`_MAX_KV_SPLITS` 64→16。T1–256×KV128/512/1024 的 capture-time sweep 中 geomean regret 33.5%→3.7%、worst 119%→36%；残余 3.7% 是不读取 runtime tensor 的 CUDA Graph 安全代价。MI355X、DeepSeek-V4-Pro、TP8+DP8 attention+EP8/MoRI+EAGLE、8,192/1,024 serving 作者 A/B：C4/8/16/32/64 throughput +1.5%/+2.5%/+0.8%/+1.8%/+4.3%，TPOT −1.7%/−1.8%/−0.8%/−1.6%/−4.2%；plain TP8 全部在 ±1% 内。GSM8K 两次 0.958/0.946、invalid 0；新增 38 unit cases。Base/Extra CI 快照为失败、AMD 进行中；所有数字为作者报告。[PR #36094](https://github.com/sgl-project/sglang/pull/36094)
- **SGLang #36657，8/28 合入：**Blackwell DeepGEMM MegaMoE 的 even clustered whole-grid barrier 若用尽 SM，side stream 临时占用一个 SM 可令部分 cluster 永远不能 resident，最终 grid-sync timeout/CUDA launch failure。PR 仅在 SM100+ 的实际 MegaMoE call 周围 reserve 两 SM、round active SM 到偶数，并保证 exception 后还原 process-wide override；SM90 不变。作者 GB300 side-stream repro：reserve=0 block，reserve=2 在 side stream 存活时完成；100 iter kernel 0.059546→0.059393ms。overlap scheduler 从 timeout 到 warmup 12,748/12,748、profiled 11,052 requests 0 error、约126.7K tok/s/GPU；CUDA Graph/SBO 12,345 requests 0 error、约69.5K tok/s/GPU。PR 快照 CI 仍进行中；数字为作者报告。[PR #36657](https://github.com/sgl-project/sglang/pull/36657)
- **vLLM #53333，8/28 合入：**P/D decode worker 的 NIXL async KV load posting 曾在 `pre_forward()` 阻塞 host；TP8 9 个 remote requests 可形成 72 handles，约5ms且偶发48ms。PR 只在 step 没有 sync load 时将 `start_load_kv()` 后移到 forward launch 后；sync 或 mixed step 保守维持 pre-forward，`no_forward` 仍只启动一次。作者两节点 Qwen3-0.6B TP1 producer/TP1 decoder、1,319 GSM8K、C64 A/B：TTFT 14,471.9→14,481.5ms（+9.6ms，+0.07%），TPOT 4.940→4.697ms（−4.92%），ITL 4.939→4.701ms（−4.83%），E2E 15,077.9→15,053.3ms（−0.16%）。这是 async-only KV I/O overlap，不是所有 connector 的普遍加速。[PR #53333](https://github.com/vllm-project/vllm/pull/53333)
- **vLLM #54168，8/28 合入：**Kimi-K3 SM100/B300 low-M fused latent-MoE tail 对 M≤5 专用 one-pass skinny BF16 up-projection、right-size Lamport consumer，并提早 PDL；M≥6 留 WGMMA path，M8 static/dynamic 7.193/5.794μs。8×B300 SXM6 AC TP8、CUDA Graph、L2 外 rotating weight 的 Nsight exposed collective→GEMV→Lamport chain 12.096→9.056μs（−25.1%），skinny GEMV −11%至−14%，Lamport standalone −73.8%；slowest-rank whole-tail CUDA event M1 16.384→16.352μs，几乎不变，不能写为同等 E2E 收益。GSM8K 1,319/1,319 无 retry，strict 0.9606；评测暂用未提交 `super().__init__()` workaround 绕开 main 的无关 startup issue，限制必须保留。所有数字为作者报告。[PR #54168](https://github.com/vllm-project/vllm/pull/54168)
- **SGLang issue #36807，8/28 社区报告：**具名报告称 `fast_topk_v2` 的 fixed 4,096-entry shared-memory candidate buffer 在 coarse threshold bucket 溢出时丢弃候选；bounds guard 避免 OOB，但 kernel 仍返回形状正常、无重复却错误的 top-k set。作者用 stock `sglang-kernel 0.4.6.post1+cu130`、B200×8、64 rows×262,144 columns、k=2,048 复现 64/64 rows 错，threshold bucket 4,178–4,448，错误候选每行6–42；65,536 columns 为0/64错、1,048,576 columns为64/64错且每行98–157。影响 DeepSeek V3.2 DSA 的 unfused 或 miss-JIT top-k path。报告有最小脚本与环境，但尚无维护者修复或独立复现，不能当作已确认缺陷。[issue #36807](https://github.com/sgl-project/sglang/issues/36807)

## 雷达与落选

- SGLang #36738 为 HiCache load-back 增加 forward-stream fence，以避免已释放/重分配 KV page 与 transfer stream restore 竞争；PR 明确无稳定数值复现。#36583 修复 H200 weight-loader references 令 KV pool 1,741→349,377 tokens，但与前一期 allocation/address 主线过近，均作雷达。
- vLLM #53409 修复 fused SiLU block quant 的 int32 token offset overflow，focused test 1 passed、full kernel file 331 passed，但没有服务影响；#53141 在 Llama-3.3-70B MXFP4 TP8/1k/1k 的单一 steady-state 配置报 +15% tok/s、TPOT −13%，覆盖范围不足。
- FlashInfer #4494/#4666 和 TensorRT-LLM #17870 缺少同配置服务 A/B；TensorRT-LLM #17434 的 RL endpoint HMAC auth 虽有测试，未提供可量化部署影响；社区 #36764 的 374.2MB image pull 报告未证明 current main 与 measured latest 为同一 commit。

## 编辑判断

本期主线是：异步与稀疏 fast path 的正确性取决于**可保留的资源余量、顺序和候选集**。#36657 保留 SM residency 使 grid barrier 不失活；#53333 只对 async-only KV load 后移提交；#36094 用 capture-time scalar 做安全近似；#54168 只在 low-M 选择 SIMT；#36807 提醒 bounds guard 可能从 OOB 退化为静默选择错误。每项收益只在给定硬件、shape、拓扑和 route 下成立。

**KPI：Top5 新颖度均值 4.70；标准桶覆盖数 3（芯片与供应链、推理与系统、论文与开源）；社区/非官方一手 1（#36807 具名公开最小复现）；落选候选数 6；degraded：是，intel-scout 两轮无首个模型事件，认证和系统 proxy 已确认，主控一手发现与审校继续。**
