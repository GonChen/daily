# 深挖 B：deepseek-harness v0.1.1-rc.1 / rc.2 边界与部署含义

## 发生了什么

2026-08-21，deepseek-ai/deepseek-harness 连发两个候选版本：rc.1（commit `528c682`，21 Aug 07:12 UTC）与 rc.2（commit `b150a55`，21 Aug 12:35 UTC）。两者均标注 **Pre-release**，由 `imccyu` 发布，标记为 immutable release。rc.1 引入多模态视觉模型与一项 Bubblewrap 沙箱逃逸修复；rc.2 仅含两项图像上传体验优化。截至 rc.2，仓库统计 Fork 20.4k / Star 185k（GitHub 页面显示，非性能指标）。

## 数字与对比

| 维度 | rc.1 | rc.2 |
|---|---|---|
| 发布时间 | 08-21 07:12 UTC | 08-21 12:35 UTC（间隔约 5h23m）|
| commit | `528c682` | `b150a55` |
| 新增功能 | 1（Vision-Exp 适配器）| 0 |
| 问题修复 | 2（布局、Bubblewrap 逃逸）| 0 |
| 体验优化 | 3 | 2（Files API 图像上传、预处理）|
| 贡献者 | 5（Kingwl、07akioni、LegGasai、pku-xht、yixiangihsiang）| 1（CreatixChu）|
| Changelog 范围 | `dsh-v0.1.0-rc.8...dsh-v0.1.1-rc.1` | `dsh-v0.1.1-rc.1...dsh-v0.1.1-rc.2` |
| 发布状态 | Pre-release | Pre-release |

注：rc.1 页面显示 "35 commits to master since this release"，rc.2 未显示该计数（页面渲染差异，非版本属性）。仓库 Fork/Star 数为页面快照，非作者报告的性能数字。

## 对部署/成本/能力意味着什么

**Vision-Exp（rc.1）**：DeepSeek 适配器新增 `DeepSeek-V4-Flash-Vision-Exp`，名称带 `-Exp` 后缀，属实验性多模态视觉理解模型。部署含义：使用 deepseek-harness 作为前端/适配层的用户，升级到 rc.1 后可在同一 harness 内调用视觉理解，无需另接独立多模态客户端。但 `-Exp` 表明该模型未稳定，API 形态、上下文长度、并发限制均未在 release notes 中给出，生产负载不应直接切换。推断（单列）：若 Vision-Exp 走 DeepSeek 官方推理后端，则图像输入会带来额外 token 计费与延迟，具体口径待官方模型文档确认。

**Bubblewrap `/proc/<pid>/root` 逃逸修复（rc.1）**：修复由 `@Kingwl` 提交，描述为"受限进程可经 `/proc/<pid>/root` 绕过 Bubblewrap 限制"。Bubblewrap（bwrap）是 Linux 用户态命名空间沙箱，`/proc/<pid>/root` 是内核暴露的进程根目录视图，历史上是沙箱逃逸的常见路径。部署含义：任何在 deepseek-harness 中以 Bubblewrap 隔离不可信子进程（如子代理、工具执行）的部署，**rc.1 之前版本存在已知逃逸路径**，应视为安全相关缺陷；升级到 rc.1 可关闭该路径。release notes 未给出 CVE 编号、影响版本下界、可利用性证明或触发前置条件，因此无法判定是否需紧急回溯补丁——这是待验证项，不是已确认的紧急漏洞。推断（单列）：若 harness 默认以 bwrap 运行工具调用，则多租户/共享主机场景应优先升级。

**Files API 图像上传复用（rc.2）**：DeepSeek 适配器优先经 Files API 上传图像，并可复用已上传文件；同时按模型要求自动缩放与格式转换。部署含义：对同一图像的多次引用（如多轮对话、批量评测）从"每次重新上传"变为"上传一次、引用 file id"，可降低上行带宽与首字延迟。复用前提是后端 Files API 返回稳定 file id 且 harness 持久化该映射——release notes 未说明映射生命周期（进程内/落盘），亦未给出命中率或节省比例的任何数字，故不得声称具体收益。推断（单列）：在图像密集型工作流中，复用可减少重复 I/O，但量化收益需实测。

## 什么证据会推翻它

- 若 DeepSeek 官方后续公告表明 `V4-Flash-Vision-Exp` 从未作为独立模型提供，或 `-Exp` 仅为内部代号，则"前端可调用视觉理解"的部署含义不成立。
- 若 Bubblewrap 上游或安全公告指出 `/proc/<pid>/root` 路径在 deepseek-harness 实际配置下不可达（如已 bind-mount `/proc` 为空），则"rc.1 之前存在可利用逃逸"需降级为"理论路径"。
- 若 Files API 实际不支持跨会话复用（file id 有短 TTL），则"复用已上传文件"的部署收益被高估。
- 待验证项：rc.1 是否为首个含该 Bubblewrap 修复的版本（changelog 范围 `dsh-v0.1.0-rc.8...rc.1`，但中间 rc.8→rc.1 的提交未在 notes 列出）。

## 可信级与来源列表

可信级：**B（单一来源，作者 release notes，未独立复现）**。所有功能描述均来自 GitHub release 页面原文，未引入第三方转述数字。性能、破坏性变更均未在来源中出现，故本报告不给出任何性能数字或破坏性变更判断。

来源：
1. https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.1-rc.1 （rc.1，2026-08-21 07:12 UTC，commit 528c682）
2. https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.1-rc.2 （rc.2，2026-08-21 12:35 UTC，commit b150a55）

红线声明：rc.1、rc.2 均为 Pre-release，**RC 不等于 GA**；本报告不将候选版本包装为正式发布，不杜撰性能数字，不臆造破坏性变更。超出 release notes 的推断已标"推断"并单列。
