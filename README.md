# [AI智能体从入门到项目实践](https://www.amazon.com/dp/B0H3LX9N21) - 代码清单

> **本书配套代码示例库** — 从章节中提取的完整可运行代码片段索引

## 关于本书

调用 LLM API 不难，把 AI 真正嵌入工程流程却很难。本书定位为「应用驱动型」AI 智能体生产级实战技术书，聚焦 **LangChain + LangGraph** 两大框架搭档——LangChain 提供 LLM 抽象、工具、记忆、检索这些「积木」，LangGraph 负责把积木编排成带状态流转和人工介入的复杂 Agent，帮助读者从「会调用 API」走到「能交付生产级智能体」。

本书基于 Python 3.11+、LangChain 1.3.x、LangGraph 1.2.x（2025-2026 最新版本）撰写，对齐 LangChain 1.x 的 `create_agent` 入口与 LangGraph 1.2.x 的 StateGraph 编排，避免读者被旧版教程的过时 API 误导。GPT / Claude 在本书中作为 LangChain 集成的模型选项出现。

## 本书特点

**第一，聚焦 LangChain + LangGraph 两大框架搭档。** 不堆砌框架数量，而是把这对搭档讲透：积木与编排的分工，并在第 6 章专讲框架选型——什么场景用 Chain，什么场景切换到状态机。

**第二，从入门到生产级。** 涵盖代码沙箱、Checkpointer 状态持久化、HITL 中断机制、多模型路由、成本控制等生产环境必需的复杂特性，帮助读者把 demo 级 Agent 升级为可部署的生产级系统。

**第三，三个完整实战项目。** 卷四交付 SQL 自愈系统、SaaS 客服 Agent、A 股量化投研三个真实项目，从需求分析到部署监控完整呈现，覆盖数据库运维、多租户客服、金融投研三类典型场景，配套三个 tag 过的可跑代码仓（见下文「配套案例仓库」）。

**第四，工程诚实边界。** 证据链防幻觉、多模型路由与成本、金标回测评估等章节，让读者看到 Agent 的能力边界，也看到控制边界的方法。

## 谁应该读这本书

如果你具备 Python 编程基础，希望掌握 AI 智能体生产级开发，这本书适合你。你可能是：

- 具备 Python 基础的后端与全栈开发者，需要在企业项目中真正落地 AI 智能体
- 技术负责人，需要评估和选型合适的 Agent 框架
- 从单一 LLM 调用起步、想建立完整 Agent 系统认知的学习者

## 代码清单说明

本目录包含从书籍章节中提取的 **134** 个代码片段文件，对应书稿中「代码清单 N-M」标题块，涵盖 LangChain + LangGraph 全栈开发核心知识点。

### 📊 代码统计

- **总块数**: 134 个
- **涉及章节**: 第 1-33 章（第 2、6、34 章无代码清单）
- **清单索引**: `extracted_code_manifest.json`（含 title / lang / chapter_file / line / extracted_file / source）

### 📋 按编程语言分类

| 语言 | 块数 | 说明 |
|------|------|------|
| python | 124 | 主体代码（LangChain 积木 / LangGraph 编排 / 三大实战项目） |
| bash | 10 | 命令/脚本（运行示例、测试命令） |

### 📂 章节覆盖

- **卷一（第 1-7 章）**: AI 智能体基础与核心概念——智能体概述、核心组件、增强型 LLM、架构模式、LangChain 入门、框架选型、第一个 AI 助手
- **卷二（第 8-17 章）**: LangChain 与 LangGraph 深度实践——Chain、状态管理与节点设计、Agent 实现、工具、记忆、输出解析器、RAG、LangSmith、评估、研究型 Agent
- **卷三（第 18-21 章）**: 生产级 Agent 特性——代码沙箱、Checkpointer 状态持久化、HITL 中断机制、生产部署与可观测安全
- **卷四（第 22-34 章）**: 实战案例——SQL 自愈、SaaS 客服 Agent、A 股量化投研三个端到端项目

### 🗂️ 配套案例仓库

卷四的三个实战项目均为**独立可运行**的完整工程，书中带 `source=` 标注的代码清单即摘自这些仓库（已 tag、全量测试真绿，clone 即跑）。本目录共 **37** 个代码清单标注了 `source=` 来源。

| 案例 | 书中清单数 | 技术栈 | 仓库地址 |
|------|-----------|--------|---------|
| SQL 自愈系统 | 14 | LangGraph 状态机 / HITL 安全熔断 / 异步并发接口 | [sql-self-healer](https://github.com/zcqiand/sql-self-healer) @ v1.0-008 |
| SaaS 客服 Agent | 7 | Checkpointer 持久化 / 多租户隔离 / 时间旅行 | [saas-cs-agent](https://github.com/zcqiand/saas-cs-agent) @ v1.0-008 |
| A 股量化投研 | 16 | 金融数据网关 / 语义情绪打分 / 多波次状态机 / 证据链防幻觉 / 多模型路由 | [quant-sentiment-research](https://github.com/zcqiand/quant-sentiment-research) @ v1.0-008 |

本目录（ai-agent-book）是**章节代码摘录的索引**；上面的案例仓才是**完整可跑工程**。读者想看真实实现请去案例仓。

## 如何使用代码

### 环境准备

- **Python**: 3.11+
- **核心依赖**: `pip install langchain langchain-openai langgraph langgraph-checkpoint-sqlite`

### 运行示例

```bash
# 安装依赖
pip install langchain langchain-openai langgraph langgraph-checkpoint-sqlite

# 运行示例（文件名形如「代码清单N-M_ 描述.py」）
python "src/代码清单11-2_ 创建 StateGraph.py"
```

完整项目的运行方式请参考各案例仓库的 README。

## 重新生成 src/

```bash
python .claude/scripts/extract_code.py output/xr-know-008 code/code-listings/ai-agent-book
```

## 配套资源

- **读者交流**: 1282301776@qq.com

## ⚠️ 注意事项

1. **代码版本**: 基于 LangChain 1.3.x + LangGraph 1.2.x，API 可能随版本更新
2. **依赖安装**: 完整项目运行请参考各案例仓库的 README
3. **安全审查**: 生产环境使用前请审查代码，特别是认证、租户隔离与权限相关部分
4. **环境差异**: 部分代码可能需要根据实际环境（模型 Key、数据库等）调整

---

**最后更新**: 2026年07月09日
**书籍版本**: Python 3.11+ / LangChain 1.3.x / LangGraph 1.2.x
**代码来源**: 由 `extract_code.py` 从 `output/xr-know-008/chapters/` 全量提取
