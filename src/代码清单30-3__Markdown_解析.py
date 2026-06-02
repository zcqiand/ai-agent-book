from langchain_community.document_loaders import UnstructuredMarkdownLoader
import re

class MarkdownParser:
    """Markdown 解析器"""

    def parse(self, file_path: str) -> list:
        """解析 Markdown"""
        loader = UnstructuredMarkdownLoader(file_path)
        return loader.load()

    def parse_with_structure(self, file_path: str) -> dict:
        """保留标题结构的解析"""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 按标题分割
        sections = re.split(r"^#{1,6}\s+", content, flags=re.MULTILINE)

        # 提取标题和内容
        headings = re.findall(r"^#{1,6}\s+(.+)$", content, re.MULTILINE)

        result = []
        for i, heading in enumerate(headings):
            if i < len(sections) - 1:
                result.append({
                    "heading": heading,
                    "level": heading.count("#"),
                    "content": sections[i + 1].strip()
                })

        return result

md_parser = MarkdownParser()
sections = md_parser.parse_with_structure("README.md")
print(f"解析了 {len(sections)} 个章节")