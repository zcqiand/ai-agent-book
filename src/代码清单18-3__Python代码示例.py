from langsmith import Client

client = Client()

# 创建数据集
dataset = client.create_dataset(
    project_name="agent-evaluation",
    description="Agent 评估数据集"
)

# 添加测试用例
test_cases = [
    {
        "inputs": {"question": "什么是AI？"},
        "outputs": {"expected": "AI是人工智能的缩写..."}
    },
    {
        "inputs": {"question": "如何学习编程？"},
        "outputs": {"expected": "学习编程的建议：1. 选择语言..."}
    },
    {
        "inputs": {"question": "大语言模型有哪些？"},
        "outputs": {"expected": "主要的大语言模型包括GPT、BERT、Claude等..."}
    },
]

for case in test_cases:
    client.create_example(
        inputs=case["inputs"],
        outputs=case["outputs"],
        dataset_id=dataset.id
    )

print(f"数据集创建成功，包含 {len(test_cases)} 个测试用例")