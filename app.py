import gradio as gr

from auto_readme import AutoREADME_Client

css = ".json {height: 527px; overflow: scroll;} .json-holder {height: 527px; overflow: scroll;}"
with gr.Blocks(css=css) as demo:
    state = gr.State(value={"client": AutoREADME_Client()})
    gr.Markdown("<h1><center>Enjoy Auto README!</center></h1>")
    gr.Markdown("<img src='/Users/shaohon/PycharmProjects/readmegenerator/resources/logo.png'>")
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
        with gr.Column(scale=0.6):
            with gr.Row().style():
                chatbot = gr.Chatbot([], elem_id="chatbot").style(height=500)
            with gr.Row().style():
                with gr.Column(scale=0.85):
                    chat_txt = gr.Textbox(
                        show_label=False,
                        placeholder="Tell me about your project information",
                        lines=1,
                    ).style(container=False)
                with gr.Column(scale=0.15, min_width=0):
                    chat_btn = gr.Button("Submit").style()
            with gr.Row().style():
                chat_clear_btn = gr.Button("Clear").style()
        with gr.Column(scale=0.4):
            with gr.Row():
                edit_readme_btn = gr.Button('EDIT README')
            with gr.Row():
                readme = gr.Markdown("MarkDown?")

    def chat_with_gpt(key, state, chatbot, txt):
        state["client"].set_key(key)
        return state["client"].chat_with_gpt(chatbot, txt)


    def clear_dialog(chatbot):
        chatbot = []
        return chatbot, ""


    chat_txt.submit(chat_with_gpt, [openai_api_key, state, chatbot, chat_txt], [chatbot, chat_txt, readme])
    chat_btn.click(chat_with_gpt, [openai_api_key, state, chatbot, chat_txt], [chatbot, chat_txt, readme])
    chat_clear_btn.click(clear_dialog, [chatbot], [chatbot, chat_txt])

    gr.Examples(
        examples=[
            "Please generate a README template for me",
        ],
        inputs=chat_txt
    )

demo.launch()
