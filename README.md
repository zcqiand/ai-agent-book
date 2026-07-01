# AI智能体从入门到项目实践 - 代码清单

> **本书配套代码示例库** — 从章节中提取的完整可运行代码

## 关于本书

本书是国内首部覆盖四大主流 AI 智能体框架（LangChain、LangGraph、OpenAI Agents SDK、Anthropic Claude SDK）的实战指南，基于 2025-2026 最新版本编写。

LangChain、LangGraph、OpenAI Agents SDK、Anthropic Claude SDK——每个框架都有自己的设计哲学和使用逻辑。盲目选择会导致技术债，错误组合会引发维护噩梦。本书通过 42 章内容，帮助你建立框架选择的直觉，掌握生产级 AI 应用开发能力。

## 本书特点

**第一，框架选择有判断力。** 不是功能的简单罗列，而是通过大量对比表格和决策框架帮你建立选择直觉——什么场景用 LangChain、什么场景用 LangGraph、什么场景必须上 OpenAI Agents SDK。

**第二，两个完整生产级项目。** 智能文档分析与问答系统覆盖 RAG、知识库、对话记忆全流程；多智能体协作与自动化任务系统展示复杂 Agent 协作的真实落地方案。

**第三，版本最新。** 所有代码基于 2025-2026 年最新框架版本编写，涵盖各框架最新特性和 API 变化。

## 谁应该读这本书

如果你是一名有 Python 基础的开发者，希望将 AI 智能体能力应用到实际业务场景，这本书适合你。你可能是：

- 后端/全栈工程师，希望在项目中集成 AI 智能体能力
- 技术负责人，需要评估和选型合适的 AI 框架
- 对 AI 智能体感兴趣的学习者，希望系统化建立知识体系

## 代码清单说明

本目录包含从书籍章节中提取的 210 个代码示例文件，涵盖四大主流框架的核心知识点。

### 📊 代码统计

- **总文件数**: 210 个
- **涉及章节**: 第 1-42 章（第 2、8 章无代码清单）
- **清单索引**: `extracted_code_manifest.json`（含 title / lang / chapter_file / line / extracted_file）

### 📋 按编程语言分类

| 语言 / 类型 | 文件数 | 后缀 | 说明 |
| ----------- | ------ | ---- | ---- |
| Python | 200 | .py | 主体代码（LangChain / LangGraph / OpenAI / Claude SDK） |
| Markdown | 3 | .md | 配置/说明类清单 |
| 纯文本（未标注语言） | 3 | .txt | 章节未声明语言的代码块 |
| Dockerfile | 2 | .dockerfile | 容器构建文件 |
| YAML | 1 | .yaml | 编排配置 |
| JSON | 1 | .json | 消息格式定义 |
| Mermaid | 1 | .mmd | 时序图 |
| Bash | 1 | .sh | 命令示例 |

### 📂 章节覆盖

- **第 1-9 章**: AI智能体基础与核心概念
- **第 10-19 章**: LangChain 与 LangGraph 深度实践
- **第 20-28 章**: OpenAI Agents SDK 与生产级Agent
- **第 29-35 章**: 案例一：智能文档分析与问答系统
- **第 36-42 章**: 案例二：多智能体协作与自动化任务系统

### 📖 技术框架覆盖

| 框架 | 版本 | 核心内容 |
|------|------|---------|
| LangChain | 0.3.x | Chain、Agent、Memory、RAG |
| LangGraph | 0.2.x | 状态机、节点编排、条件分支 |
| OpenAI Agents SDK | 1.x | Agent定义、Handoffs、Guardrails、Sandbox |
| Anthropic Claude SDK | 0.26.x | Claude Agent开发、工具调用 |

## 如何使用代码

### 环境准备

- **Python**: 3.11+
- **相关框架**: `pip install langchain langchain-openai langgraph openai anthropic`

### 运行示例

```bash
# 安装依赖
pip install langchain langchain-openai langgraph openai anthropic

# 运行示例（文件名形如「代码清单N-M_ 描述.py」）
python "src/代码清单11-2_ 创建 StateGraph.py"
```

## 配套资源

- **读者交流**: 1282301776@qq.com

## ⚠️ 注意事项

1. **代码版本**: 代码基于 2025-2026 年最新框架版本编写，部分 API 可能有更新
2. **依赖安装**: 请确保安装对应章节所需的依赖包
3. **安全审查**: 生产环境使用前请审查代码，特别是涉及认证和数据处理的部分
4. **环境差异**: 部分代码可能需要根据实际环境调整

---

**最后更新**: 2026年7月1日
**书籍版本**: 1.0
**代码来源**: 由 `extract_listings.py` 从 `../output/xr-know-008/chapters/` 全量提取
