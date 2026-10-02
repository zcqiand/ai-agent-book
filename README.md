# AI智能体从入门到项目实践 - 代码清单

## 关于本书

调用 LLM API 不难，把 AI 真正嵌入工程流程却很难。本书是一本「应用驱动型」的 AI 智能体生产级实战书，聚焦 LangChain + LangGraph 两大框架搭档：LangChain 提供 LLM 抽象、工具、记忆、检索这些「积木」，LangGraph 负责把积木编排成带状态流转和人工介入的复杂 Agent，带读者从「会调用 API」走到「能交付生产级智能体」。全书基于 Python 3.11+、LangChain 1.3.x、LangGraph 1.2.x 撰写，对齐 LangChain 1.x 的 create_agent 入口与 LangGraph 1.2.x 的 StateGraph 编排，避免读者被旧版教程的过时 API 误导。

全书按四卷展开：卷一建立智能体核心认知与框架选型判断；卷二深入 Chain、状态机、Agent 循环、记忆系统与 RAG；卷三补齐代码沙箱、Checkpointer 状态持久化、HITL 中断机制等生产级特性；卷四完整交付三个端到端项目——SQL 自愈系统、SaaS 客服 Agent、A 股量化投研，覆盖数据库运维、多租户客服、金融投研三类典型场景。

如果你具备 Python 编程基础、希望掌握 AI 智能体生产级开发，这本书适合你：需要在企业项目中真正落地智能体的后端与全栈开发者、需要评估与选型 Agent 框架的技术负责人，以及从单一 LLM 调用起步、想建立完整 Agent 系统认知的学习者。

## 本书特点

**第一，聚焦 LangChain + LangGraph 两大框架搭档。** 不堆砌框架数量，而是把「积木与编排」的分工讲透，并在框架选型专章回答什么场景用 Chain、什么场景切换到状态机；GPT / Claude 作为 LangChain 集成的模型选项出现，不在多套原生 API 之间反复切换。

**第二，从入门直通生产级。** 代码沙箱、Checkpointer 状态持久化、HITL 中断机制、多模型路由、成本控制这些生产环境必需的复杂特性逐一讲透，帮读者把 demo 级 Agent 升级为可部署的生产级系统。

**第三，三个完整实战项目。** 卷四的 SQL 自愈系统、SaaS 客服 Agent、A 股量化投研从需求分析到部署监控完整呈现，书中带 source= 标注的代码清单即摘自这三个已冻结 tag 的真实仓库。

**第四，工程诚实边界。** 证据链防幻觉把研究简报锚定在证据上，多模型路由与成本按任务复杂度选模型档位，金标回测评估用人工金标验证情绪判定质量——让读者看到 Agent 的能力边界，也看到控制边界的方法。

## 案例仓库

| 仓库名 | 说明 |
| :--- | :--- |
| [sql-self-healer](https://github.com/zcqiand/sql-self-healer) @ v1.0-008 | LangGraph 状态机编排的 SQL 自愈系统，带 HITL 安全熔断与异步并发接口 |
| [saas-cs-agent](https://github.com/zcqiand/saas-cs-agent) @ v1.0-008 | SaaS 多租户客服 Agent，Checkpointer 状态持久化、tenant_id 隔离与 checkpoint 时间旅行回放 |
| [quant-sentiment-research](https://github.com/zcqiand/quant-sentiment-research) @ v1.0-008 | A 股量化投研系统，金融数据网关、语义情绪打分、多波次状态机，内置证据链防幻觉与多模型路由 |

> 配套案例仓库为独立可跑工程，已冻结 tag，含完整测试与 CI，clone 即跑。

## 代码清单说明

本书所有代码清单均收录于本目录，对应书稿中「代码清单 N-M」标题块。

### 运行环境

```bash
# 本仓代码清单为 Python 片段，需 Python 3.11+；先安装核心依赖
pip install langchain langchain-openai langgraph langgraph-checkpoint-sqlite
# 运行单个清单文件（文件名形如「代码清单N-M_ 描述.py」）
python "src/代码清单11-2_ 创建 StateGraph.py"
```

### 目录结构

```
src/
├── 代码清单1-* … 代码清单33-*   # 第 1-33 章，共 135 个清单文件（命名「代码清单N-M_ 描述.扩展名」）
└── extracted_code_manifest.json   # 全部清单索引（title/lang/chapter_file/line/extracted_file/source）
```
