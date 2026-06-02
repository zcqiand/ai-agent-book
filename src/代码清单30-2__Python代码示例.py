from langchain_community.document_loaders import UnstructuredWordDocumentLoader

class WordParser:
    """Word 文档解析器"""

    def parse(self, file_path: str) -> list:
        """解析 Word"""
        loader = UnstructuredWordDocumentLoader(file_path)
        docs = loader.load()
        return docs

    def parse_with_structure(self, file_path: str) -> list:
        """保留结构的解析"""
        from docx import Document

        doc = Document(file_path)

        chunks = []
        current_heading = None
        current_content = []

        for para in doc.paragraphs:
            if para.style.name.startswith("Heading"):
                # 保存之前的段落
                if current_content:
                    chunks.append({
                        "heading": current_heading,
                        "content": "\n".join(current_content)
                    })

                current_heading = para.text
                current_content = []
            else:
                current_content.append(para.text)

        # 保存最后一段
        if current_content:
            chunks.append({
                "heading": current_heading,
                "content": "\n".join(current_content)
            })

        return chunks

word_parser = WordParser()
chunks = word_parser.parse_with_structure("document.docx")
print(f"解析了 {len(chunks)} 个章节")