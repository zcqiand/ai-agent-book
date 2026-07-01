from agents import Agent
from agents.sandbox import sandbox, SandboxConfiguration

# 配置安全的 Sandbox
config = SandboxConfiguration(
    timeout=60,
    memory_limit="512MB",
    allowed_packages=["pandas", "numpy", "matplotlib", "scipy"],
    blocked_modules=["os", "sys", "subprocess", "socket"]
)

# 创建数据分析 Agent
data_analyst = Agent(
    name="data_analyst",
    instructions="""你是一个专业的数据分析师。你的职责：
    1. 理解用户的数据分析需求
    2. 编写 Python 代码进行分析
    3. 在 sandbox 中安全执行代码
    4. 返回清晰的分析结果

    代码规范：
    - 使用 pandas 处理数据
    - 使用 numpy 进行计算
    - 使用 matplotlib 生成图表（保存为 PNG）
    - 打印关键统计结果

    安全规则：
    - 不读取用户未指定的文件
    - 不执行任何系统命令
    - 不访问网络""",
    tools=[sandbox(config=config)]
)

def analyze_sales_data(csv_path: str, analysis_type: str):
    """分析销售数据"""
    prompt = f"""请分析销售数据文件 {csv_path}：

    分析类型：{analysis_type}

    请生成并执行 Python 代码：
    1. 读取CSV文件
    2. 进行{analysis_type}分析
    3. 生成可视化图表
    4. 打印关键指标"""

    result = data_analyst.run(prompt)
    return result

# 使用示例
result = analyze_sales_data("sales.csv", "月度汇总")
print(result)
