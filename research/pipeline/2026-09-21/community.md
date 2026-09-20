# 2026-09-21 community 桶候选

## 1. "跨请求提示词泄漏"事件反转：逐 commit A/B 隔离出 Ollama 打包构建是元凶，llama.cpp 源码被赦免
- 日期：9/18 首发，9/19–9/20 A/B 收敛｜平台/作者：GitHub llama.cpp #29092（具名 jgoellermaximus）；复现者具名 huppiflupp、pwilkin（llama.cpp contributor）；衍生 ollama/ollama #18528
- 事实：生产环境（Ollama）发现 AMD Strix Halo（gfx1151）HIP 后端下，fused Gated DeltaNet 算子把上一请求的循环状态带入复用 server slot——前一用户的文档文本逐字出现在下一请求补全里，temperature 0 确定性复现（跨用户提示词泄漏，隐私级）。72 小时内完成三方对照矩阵：huppiflupp 同硬件 commit 级 A/B（#28604 修复提交父提交 5d806aa vs d4389a4dd，均无泄漏）；报告者换官方 master 1af554f8f + 系统 ROCm 7.1 + Q4_K_M 复测无泄漏；huppiflupp 固定 ROCm 7.2 三方对照——官方 llama.cpp 干净、Ollama 0.34.1 打包版泄漏，把嫌疑从 llama.cpp 源码和 ROCm runtime 双双排除，指向 Ollama 自己的 ggml-hip 构建/补丁/fused-op resolver。9/20 又有 dougmaitelli 报告 lemonade 的 llamacpp-rocm 也有约一个月泄漏（关联 #27422）。
- 可信度：高（三方具名、同硬件、commit 级隔离、量化轴交叉验证，结论已收敛；待 Ollama 侧确认根因）。
- 来源：https://github.com/ggml-org/llama.cpp/issues/29092 ；https://github.com/ollama/ollama/issues/18528
- 新事实：本周新完成的三方 A/B 把"跨请求状态泄漏"从上游源码嫌疑改判为 Ollama 打包构建独有缺陷（同代码不同二进制不同行为）。

## 2. vLLM V1 调度器删掉"死配置"后长上下文 TTFT 队头阻塞：两位生产操作者出生产证据，社区自发复活修复 PR
- 日期：9/17 开帖，9/18–9/19 迭代｜平台/作者：vLLM #57413（具名 javimp2003）；佐证具名 alvarogarciapiz、devtyagi3909
- 事实：生产环境（GLM 系 MoE、TP=4 × 4×B200、V1 引擎、中位 100k–180k token 长提示、生成 <1k）报告严重 TTFT 尾延迟：V1 调度器没有并发 partial prefill 上限，短请求被 7–12 个调度步的长 prefill 队头阻塞且无法交错。追查发现 `--max-num-partial-prefills` 在 7 月 V0 清理 #49244 中被当"dead config"删除（无 V1 消费者），恢复 PR #49075 挂起未 rebase、#55256 被关闭、#39737 自 4 月无人回应。第二位操作者独立给出同构生产证据（GLM-5.3-Flash on 4×B200：尾 TTFT 大涨时 KV 占用低、GPU 利用率高）。用户把 #55256 的 `max_concurrent_prefills` rebase 成新 PR #57427 并与报告者对拉生产流量验证。
- 可信度：高（两处独立生产环境、完整参数、调度步数量化、因果链有 PR 号可查；修复未合入、无维护者裁决）。
- 来源：https://github.com/vllm-project/vllm/issues/57413 ；https://github.com/vllm-project/vllm/pull/57427
- 新事实：七月清理把仍在用的调度上限当死代码删除，导致长上下文队头阻塞；与已报 #57680（升级回归孤证）不同条目。

## 3. HN 热榜（371 分）：Pirate Face 镜像站上线 + "abliterated 重量化会部分恢复拒绝行为"的具名技术反驳
- 日期：9/20｜平台/作者：HN（提交者 skepticalgenius；技术发言具名 wren6991、nperez）；站点 pirateface.co
- 事实：pirateface.co 上线——校验和验证的 magnet 索引 + 回源 HuggingFace 的镜像站。热度之外的技术增量：wren6991 论证 abliteration 无需改权重——对激活做拒绝方向正交化在数学上等价（每层点积+广播乘加）；并给出可检验主张：对已 QAT/预量化模型（DeepSeek V4、Kimi K2.5/K3）改权重后重量化会部分恢复拒绝行为且精度次优，应把"基座权重 + 拒绝方向向量"分开分发；引用 antirez 的 DS4 运行时 dir-steering（已核实 README：每层一条归一化 hidden-width 方向的 f32 矩阵）。nperez 称维护激活侧 abliteration 的 llama.cpp fork。反方 derefr：abliterated 权重流行是因为托管平台"盲加载"。
- 可信度：中高（数学自洽、DS4 支持可核验；"重量化恢复拒绝"是主张、无公开对照数据）。
- 来源：https://news.ycombinator.com/item?id=49776699 ；https://github.com/antirez/ds4/blob/main/dir-steering/README.md
- 新事实：热量之外的增量是"abliterated 权重 → 激活侧运行时方向抵消"等价性论证 + 重量化恢复拒绝行为的可复验主张。

## 4. Cactus Needle 3 后续：作者公开自认"不是真推理"（9/19 期已报主事件）
- 日期：9/18–9/20｜平台：HN 同帖
- 事实：增量：① IanCal 用 6 条自然语言变体做增量对照（"I need a wee"被理解成音乐流派、厕所指令路由到咖啡机）；② 作者公开承认"Reasoning isn't *true* reasoning… more like grounding… can often become nonsensical"；③ rohansood15 要求给一个预设外成功案例，作者未能给出。标题主张被作者自己的措辞降级。
- 来源：https://news.ycombinator.com/item?id=49748553
- 新事实：对已报道事件的增量，不宜独立成篇，并入相关条目。

## 未达准入线
中文侧（知乎/V2EX）无满足准入线的一手新增；HN 其余热榜（Samsung HBM4 产能翻倍 248 分为二手商业报道；GPT-6/Tao 博文非推理系统）。SGLang #39087、vLLM #57680 窗口内未见新复现，维持待复现。
