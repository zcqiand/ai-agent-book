import gradio as gr
from your_rag_module import RAGSystem

# 初始化 RAG 系统
rag = RAGSystem()

def chat_fn(message, history):
    """聊天函数"""
    response = rag.query(message)
    return response

# 创建界面
demo = gr.ChatInterface(
    fn=chat_fn,
    title="企业知识库问答",
    description="基于 RAG 的智能问答系统",
    examples=[
        ["公司的年假政策是什么？"],
        ["如何申请报销？"],
        ["加班调休有哪些规定？"]
    ],
    theme="soft"
)

# 启动
demo.launch(server_name="0.0.0.0", server_port=7860)
