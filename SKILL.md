---
name: common-develop-dec-integration
description: 将 common-develop-opt 已批准的设计阶段 Gate 证据消费为 DEC 三 Provider 的固定 P0 验证链；依次调用 dec-design、dec-java-lite、dec-implementation 的正式工具，输出 Artifact 摘要与真实测试证据，不替代上游流程或 DEC 规范。
---

# common-develop-dec-integration (P0)

本 Skill 仅是跨仓库适配器。研发阶段的 owner、Review、work mode 与 Gate 的权威来源始终是 **common-develop-opt**；DEC canonical YAML 的语义权威是 **dec-design**，代码生成和 Binding 由原 DEC 工具验证。独立 Skill 均可不安装本集成层运行。

1. 阅读 `README.md`、`docs/gate-contract.md`；确认 DEC checkout、Java 21、Python 3.9+、测试 MySQL 环境及输出目录。
2. 要求原生 common-develop-opt 通过自身 `wk start/begin/progress`、独立 Review 及 `long_task.py finalize-phase` 完成真实设计阶段。当前 Gitee Skill 基线：`b26715f6779b373b4f840b519ba9725fed5d789a`。其正式结果为事件账本的 `STAGE_OUTCOME_FINALIZED`，不是自定义 Gate JSON。
3. 正式交接必须同时提供 `--gate`（只作为跨格式 Artifact SHA/Revision 映射）、`--native-opt-root`（真实 Skill 根目录）、`--native-task-dir`（实际 task）。适配器调用官方 `long_task.py validate` 和 `task-events`，核对最近一次 design/PASSED StageOutcome 和输出 revision；未知/缺失阻断。只有 `--demo-fixture-gate` 的 CI 演示不能视为原生通过。
4. 使用 `python3 scripts/p0_integration.py --dec-root <DEC_CHECKOUT> --gate <GATE_JSON> --native-opt-root <OPT_SKILL> --native-task-dir <TASK_DIR> --output <OUTSIDE_DEC_DIR>` 执行固定 Provider 链；测试时才可使用 `--demo-fixture-gate`。
5. 消费 `p0-report.json`、`artifact-manifest.json` 和实际 logs；任何错误不得改写为 PASSED；`--static-only` 不能表示代码集成完成。`--require-ready` 与 P0 Provider 集成是否通过必须分开记录。
6. 如 canonical YAML 改变，原 Gate 的设计摘要不匹配，停止并让 common-develop-opt 重新确认及 Review。不要用本 Skill 更改 YAML/XML 或独立模拟 Review 通过。生产真实场景测试与归档仍交给上游 workflow。

P0 不支持动态 SPI、Provider 自动发现及上游原生生命周期推进。本地 GitHub Actions 使用 fixture 验证 DEC 路径，绝非 common-develop-opt 原生测试成功证明。


## P0 真正正向验收

真实审查记录及原生阶段产物必须由 common-develop-opt 的正式 CLI 与独立 Reviewer 产生。设计阶段发布 Revision 必须绑定当前 DEC YAML 目录的 SHA-256；详见 [原生正向验收操作说明](docs/native-positive-runbook.md)。对于适合公开的脱敏 Demo，可以手动触发 `.github/workflows/p0-native-positive.yml`，其结果必须通过 `scripts/check_native_positive_evidence.py` 核实。没有真实获批任务的负向 CI 绿灯不构成 P0 完成。
