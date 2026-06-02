import gradio as gr
import time

def chat_with_loading(message, history):
    """带加载状态的聊天"""
    try:
        # 显示加载状态
        yield "正在思考中...", gr.update(visible=True), ""

        # 执行查询
        result = rag.query(message)

        # 返回结果
        answer = result["answer"]
        sources = "\n".join([
            f"[{i+1}] {doc.page_content[:150]}..."
            for i, doc in enumerate(result.get("source_documents", [])[:3])
        ])

        yield answer, gr.update(visible=False), sources

    except Exception as e:
        yield f"抱歉，发生了错误：{str(e)}", gr.update(visible=False), ""

# 优化的界面
with gr.Blocks() as demo:
    gr.Markdown("# 企业知识库问答系统")

    # 加载指示器
    loading = gr.LoadingRequest()

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="对话历史")
            msg = gr.Textbox(label="输入问题", placeholder="请输入您的问题...")
            with gr.Row():
                submit_btn = gr.Button("提交", variant="primary")
                clear_btn = gr.Button("清空")

        with gr.Column(scale=2):
            gr.Markdown("### 参考来源")
            sources_box = gr.Textbox(lines=15, show_label=False)

            gr.Markdown("### 操作")
            export_btn = gr.Button("导出对话")
            export_file = gr.File()

    def respond(message, chat_history):
        answer, _, sources = chat_with_loading(message, chat_history)
        chat_history.append((message, answer))
        return "", chat_history, sources

    def export_conversation(chat_history):
        """导出对话"""
        if not chat_history:
            return None

        content = "# 对话记录\n\n"
        for user, assistant in chat_history:
            content += f"**用户**: {user}\n\n"
            content += f"**助手**: {assistant}\n\n---\n\n"

        # 保存到临时文件
        filepath = "/tmp/conversation.md"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath

    submit_btn.click(respond, [msg, chatbot], [msg, chatbot, sources_box])
    clear_btn.click(lambda: [None, "", ""], outputs=[chatbot, msg, sources_box])
    export_btn.click(export_conversation, [chatbot], [export_file])

demo.launch()