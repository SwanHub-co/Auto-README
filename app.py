import gradio as gr

from auto_readme import AutoREADME_Client

css = ".json {height: 527px; overflow: scroll;} .json-holder {height: 527px; overflow: scroll;}"
with gr.Blocks(css=css) as demo:
    state = gr.State(value={"client": AutoREADME_Client(), "history_readme": None})
    gr.Markdown("<h1><center>Enjoy Auto README!</center></h1>")
    gr.Markdown("<img src='./resources/logo.png'>")
    gr.Markdown(
        "<p align='center' style='font-size: 20px;'> A Smart README Generate AI Power by <a href='https://chat.openai.com/'>ChatGPT</a>.</p>")
    gr.HTML(
        '''<center>Note: Online OpenAI API may sometimes not be available. The author provides his own OpenAI key for everyone to test! Thanks to the author!</center>''')
    with gr.Row().style():
        openai_api_key = gr.Textbox(
            show_label=False,
            placeholder="The author has limited funds, recommon to use your own OpenAI API",
            lines=1,
            type="password"
        ).style(container=False)

    with gr.Row().style():
        with gr.Column(scale=0.7):
            gr.Markdown("## Edit your readme with markdwon format.")
            with gr.Tab("Markdown Code"):
                readme = gr.TextArea( interactive=True)
            with gr.Tab("rendering"):
                readme_markdown = gr.Markdown()
        with gr.Column(scale=0.3):
            gr.Markdown("## Use GPT to help you modify README")
            with gr.Row().style():
                chatbot = gr.Chatbot([], elem_id="chatbot").style(height=500)
            with gr.Row().style():
                with gr.Column(scale=0.8):
                    chat_txt = gr.Textbox(
                        show_label=False,
                        placeholder="Tell me about your project information",
                        lines=1,
                    ).style(container=False)
                with gr.Column(scale=0.2):
                    with gr.Column(scale=0.5):
                        chat_btn = gr.Button("send").style()
                    with gr.Column(scale=0.5):
                        undo_readme_btn = gr.Button("Undo change").style()
            with gr.Row().style():
                chat_clear_btn = gr.Button("clear dialog").style()
            with gr.Row().style():
                gr.Examples(
                    examples=[
                        "Please give me an empty readme template",
                        "Please help me polish the README content",
                        "Please help me translate the README into Russian",
                        "请帮我将README翻译成英文",
                        "構文エラーの修正を手伝ってください",
                    ],
                    inputs=chat_txt
                )
            # with gr.Row().style():



    def update_readme_markdown(readme_code):
        return readme_code, readme_code


    def chat_with_gpt(key, state, chatbot, txt, readme):
        state["history_readme"] = readme
        state["client"].set_key(key)
        dialog_history, dialog_txt, new_readme = state["client"].chat_with_gpt(chatbot, txt, readme)
        return dialog_history, dialog_txt, new_readme


    def clear_dialog(chatbot):
        chatbot = []
        return chatbot, ""


    def undo_readme_change(state, readme):
        if state["history_readme"] is None:
            return readme
        readme = state["history_readme"]
        state["history_readme"] = None
        return readme


    readme.change(update_readme_markdown, inputs=[readme], outputs=[readme_markdown, readme])
    chat_txt.submit(chat_with_gpt, [openai_api_key, state, chatbot, chat_txt, readme], [chatbot, chat_txt, readme])
    chat_btn.click(chat_with_gpt, [openai_api_key, state, chatbot, chat_txt, readme], [chatbot, chat_txt, readme])
    chat_clear_btn.click(clear_dialog, [chatbot], [chatbot, chat_txt])
    undo_readme_btn.click(undo_readme_change, [state, readme], [readme])

demo.launch()
