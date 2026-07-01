from langchain.output_parsers import BaseOutputParser
from typing import Any

class CommaSeparatedListParser(BaseOutputParser):
    """解析逗号分隔的列表"""

    def parse(self, text: str) -> list:
        """将文本解析为 Python 列表"""
        # 清理文本
        text = text.strip()
        # 按逗号分割
        items = text.split(",")
        # 清理每个元素
        return [item.strip() for item in items if item.strip()]

    @property
    def _type(self) -> str:
        return "comma_separated_list"

# 使用自定义解析器
parser = CommaSeparatedListParser()

result = parser.parse("苹果, 香蕉, 橙子, 葡萄")
print(result)  # ['苹果', '香蕉', '橙子', '葡萄']
