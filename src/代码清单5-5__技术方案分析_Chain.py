from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import JsonOutputParser

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 步骤1：问题分析
analyze_template = ChatPromptTemplate.from_template(
    """作为技术架构师，请分析以下技术问题：
    
    问题描述：{problem}
    
    请从以下维度进行分析：
    1. 问题的根本原因是什么？
    2. 有哪些已知的约束条件？
    3. 需要考虑哪些非功能性需求（性能、安全、成本等）？
    
    请用结构化方式输出分析结果。"""
)

# 步骤2：方案生成
solution_template = ChatPromptTemplate.from_template(
    """基于以下分析，生成3种可行的技术方案：
    
    【问题分析】
    {analysis}
    
    【要求】
    - 方案A：激进方案（追求最佳性能，可能有较高风险）
    - 方案B：平衡方案（性能和风险的平衡点）
    - 方案C：保守方案（最低风险，可能牺牲一些性能）
    
    每种方案请说明：核心技术思路、优缺点、适用场景。"""
)

# 步骤3：推荐最优
recommend_template = ChatPromptTemplate.from_template(
    """基于以下分析和候选方案，推荐最优方案：
    
    【问题分析】
    {analysis}
    
    【候选方案】
    {solutions}
    
    请推荐最优方案，并说明推荐理由。考虑在实际场景中，可维护性和扩展性往往比极致性能更重要。"""
)

# 组合 Chain
analysis_chain = analyze_template | llm
solution_chain = (
    {"analysis": analysis_chain, "problem": lambda x: x["problem"]}
    | solution_template
    | llm
)
full_chain = (
    {"analysis": analysis_chain, "problem": lambda x: x["problem"]}
    | solution_template
    | llm
    | (lambda prev: {"analysis": analysis_chain.invoke({"problem": prev["problem"]}), "solutions": prev})
    | recommend_template
    | llm
)

# 运行
result = full_chain.invoke({
    "problem": "我们的电商系统在大促期间经常出现数据库瓶颈，导致响应延迟增加和偶发性超时"
})
print(result.content)