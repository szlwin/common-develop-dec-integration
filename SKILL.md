---
name: common-develop-dec-integration
description: 将 common-develop-opt 已批准的设计阶段 Gate 证据消费为 DEC 三 Provider 的固定 P0 验证链；依次调用 dec-design、dec-java-lite、dec-implementation 的正式工具，输出 Artifact 摘要与真实测试证据，不替代上游流程或 DEC 规范。
---

# common-develop-dec-integration (P0)

本 Skill 仅是跨仓库适配器。研发阶段的 owner、Review、work mode 与 Gate 的权威来源始终是 **common-develop-opt**；DEC canonical YAML 的语义权威是 **dec-design**，代码生成和 Binding 由原 DEC 工具验证。独立 Skill 均可不安装本集成层运行。

1. 阅读 `README.md`、`docs/gate-contract.md`；确认 DEC checkout、Java 21、Python 3.9+、测试 MySQL 环境及输出目录。
2. 要求外部工作流先完成需求、设计与独立 Review，导出实际 `design` PASSED 的 Gate 事实；没有时必须 BLOCKED，不能由本 Skill 自行创建 `native-export` Gate。测试专用 `--demo-fixture-gate` 必须明确标记虚拟。
3. 使用 `python3 scripts/p0_integration.py --dec-root <DEC_CHECKOUT> --gate <GATE_JSON> --output <OUTSIDE_DEC_DIR>` 执行固定 Provider 链；测试时才可使用 `--demo-fixture-gate`。
4. 消费 `p0-report.json` 和实际 logs；任何错误不得改写为 PASSED；`--static-only` 不能表示代码集成完成。`--require-ready` 与 P0 Provider 集成是否通过必须分开记录。
5. 如 canonical YAML 改变，原 Gate 的设计摘要不匹配，停止并让 common-develop-opt 重新确认及 Review。不要用本 Skill 更改 YAML/XML 或独立模拟 Review 通过。生产真实场景测试与归档仍交给上游 workflow。

P0 不支持动态 SPI、Provider 自动发现及上游原生生命周期推进。本地 GitHub Actions 使用 fixture 验证 DEC 路径，绝非 common-develop-opt 原生测试成功证明。
