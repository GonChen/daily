# AGENTS.md — daily（前沿计算情报日报）

本仓库每天自动生成并发布一期中文 AI / GPU / 推理系统情报日报。完整业务规范以 README.md、`templates/automation-prompt-v2.md`、`templates/source-policy.md` 为准，本文件只约束 **agent 的执行方式**，优先级高于任务书中的通用做法。

## 1. 子代理并发上限（硬约束）

- 通过 Agent/Task 工具启动 subagent 时，**任何时刻在跑的子代理不得超过 3 个**。
- 大批量任务（如日报流水线的 8 桶侦察）必须分批执行：3 + 3 + 2，上一批全部返回后再启动下一批；失败重试同样计入并发额度。
- 原因：更高并发会触发模型服务限速（返回 `[1302] 您的账户已达到速率限制`），导致整批侦察报废；2026-09-19 期 8 桶并发即命中此限，两桶首跑失败。
- 不要在单个子代理的 prompt 里再指示它并发派出更小的子任务。

## 2. 网络搜索工具优先级

1. **首选 anysearch**（本机已配置 API key，经 `runtime.conf` 路由到 Python CLI）。主 agent 可通过 Skill 调用；子代理没有 Skill 工具，直接用 Bash 调 CLI：

   ```bash
   # 通用搜索（--max_results 1-10，默认 10）
   python3 /home/gongchen/.agents/skills/anysearch/scripts/anysearch_cli.py search "query" --max_results 5
   # 并行批量搜索
   python3 /home/gongchen/.agents/skills/anysearch/scripts/anysearch_cli.py batch_search --query "q1" --query "q2" --max_results 3
   # 网页正文抽取（输出即 Markdown；不支持 PDF/图片/音视频）
   python3 /home/gongchen/.agents/skills/anysearch/scripts/anysearch_cli.py extract "https://example.com/page"
   ```

   垂直领域（财经、学术、代码等）先 `get_sub_domains --domain <domain>` 发现 sub_domain 再搜，规则见该目录 `SKILL.md`。

2. **备用：内置 WebSearch / WebFetch**。仅在 anysearch 不可用（配额耗尽、服务错误、CLI 全部运行时失败）时使用，或在任务报告/台账中注明降级原因。

- 给子代理写侦察 prompt 时，必须把上面的 CLI 命令路径直接写进 prompt，不要只写"用 anysearch"。
- 搜索请求频率保持克制：能合并的查询用 `batch_search`，单桶控制在必要次数内。

## 3. 发布流程速查（详见 automation-prompt-v2.md）

dedup 基线与角度轮换 → 分批侦察落盘 `research/pipeline/<DATE>/` → selection 配额核对 → 深挖 → 生成 `docs/archive/<DATE>.html` → `python3 scripts/qa_check.py <DATE>` 必须 OK → commit（`daily: publish <DATE>`）并 push → `gh run watch` 确认 Pages 部署、`curl -sL` 验证线上 200。
