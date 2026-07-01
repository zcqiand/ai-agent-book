import gradio as gr

def chat_with_sources(message, history):
    """带来源的聊天"""
    result = rag.query(message)

    # 返回回答和来源
    answer = result["answer"]
    sources = result.get("source_documents", [])

    # 格式化来源
    source_text = "\n".join([
        f"- {doc.page_content[:100]}..." for doc in sources[:3]
    ])

    return answer, source_text

# 带来源的界面
with gr.Blocks() as demo:
    gr.Markdown("# 企业知识库问答")

    with gr.Row():
        with gr.Column():
            chatbot = gr.Chatbot(label="对话")
            msg = gr.Textbox(label="请输入问题")
            with gr.Row():
                submit_btn = gr.Button("提交")
                clear_btn = gr.Button("清空")

        with gr.Column():
            sources_box = gr.Textbox(label="参考来源", lines=10)

    def respond(message, chat_history):
        answer, sources = chat_with_sources(message, chat_history)
        chat_history.append((message, answer))
        return "", chat_history, sources

    submit_btn.click(respond, [msg, chatbot], [msg, chatbot, sources_box])
    clear_btn.click(lambda: [None, "", ""], outputs=[chatbot, msg, sources_box])

demo.launch()
