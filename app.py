import gradio as gr

from auto_readme import AutoREADME_Client

css = ".json {height: 527px; overflow: scroll;} .json-holder {height: 527px; overflow: scroll;}"
with gr.Blocks(css=css) as demo:
    state = gr.State(value={"client": AutoREADME_Client(), "history_readme": None})
    gr.HTML("""
    <div align="center">
    <img src="file/resources/logo.png" width=300>
    <p align='center' style='font-size: 20px;'> A Smart README Generate AI Power by <a href='https://chat.openai.com/'>ChatGPT</a>.</p>
    <center>Note: Online OpenAI API may sometimes not be available. The author provides his own OpenAI key for everyone to test! Thanks to the author!</center>
    </div>
    """)

    # Select Type of OpenAI API
    with gr.Row().style():
        select_model = gr.Radio(["gpt-3.5-turbo-0613", "gpt-4-0613"], value="gpt-3.5-turbo-0613", label="Select Model")


    # Input OpenAI API Token
    with gr.Row().style():
        openai_api_key = gr.Textbox(
            show_label=False,
            placeholder="The author has limited funds, recommon to use your own OpenAI API",
            lines=1,
            type="password"
        ).style(container=False)

    with gr.Row(visible=False) as org_row:
        with gr.Column(scale=4):
            openai_org_key = gr.Textbox(
                show_label=False,
                placeholder="optional",
                lines=1,
                type="password"
            ).style(container=False)
        with gr.Column(scale=1):
            openai_org_btn = gr.Button("set org", variant="secondary")

    with gr.Row().style():
        # README Textbox and Markdown preview
        with gr.Column(scale=2):
            gr.Markdown("## Edit your readme with markdwon format.")
            with gr.Tab("Markdown Code"):
                readme = gr.TextArea(lines=30, interactive=True)
            with gr.Tab("rendering"):
                readme_markdown = gr.Markdown()

        # Chat Area
        with gr.Column(scale=1):
            gr.Markdown("## Use GPT to help you modify README")
            chatbot = gr.Chatbot([], elem_id="chatbot").style(height=500)
            chat_txt = gr.Textbox(
                show_label=False,
                placeholder="Tell me about your project information",
                lines=1,
            ).style(container=False)
            chat_btn = gr.Button("send", variant="primary")

            with gr.Row():
                undo_readme_btn = gr.Button("Undo change", variant="secondary").style(size="sm")
                chat_clear_btn = gr.Button("clear dialog", variant="secondary").style(size="sm")

            with gr.Row().style():
                gr.Examples(
                    examples=[
                        "Please create an readme template",
                        "Please help me polish the README content",
                        "Please help me translate the README into Russian",
                        "请帮我将README翻译成英文",
                        "構文エラーの修正を手伝ってください",
                    ],
                    inputs=chat_txt
                )


    def update_readme_markdown(readme_code):
        return readme_code


    def set_org_key(state, key):
        state["client"].set_org_key(key)
        return key


    def chat_with_gpt(key, model, state, chatbot, txt, readme):
        state["history_readme"] = readme
        state["client"].set_key(key)
        state["client"].set_model(model)
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

    def change_model(select_model_option):
        if select_model_option == "gpt-4-0613":
            return {org_row: gr.update(visible=True)}
        else:
            return {org_row: gr.update(visible=False)}

    select_model.input(change_model, inputs=[select_model], outputs=[org_row])
    openai_org_btn.click(set_org_key, inputs=[state, openai_org_key], outputs=[openai_org_key])
    readme.change(update_readme_markdown, inputs=[readme], outputs=[readme_markdown])
    chat_txt.submit(chat_with_gpt, [openai_api_key, select_model, state, chatbot, chat_txt, readme],
                    [chatbot, chat_txt, readme])
    chat_btn.click(chat_with_gpt, [openai_api_key, select_model, state, chatbot, chat_txt, readme],
                   [chatbot, chat_txt, readme])
    chat_clear_btn.click(clear_dialog, [chatbot], [chatbot, chat_txt])
    undo_readme_btn.click(undo_readme_change, [state, readme], [readme])

demo.launch()
