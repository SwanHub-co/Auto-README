import gradio as gr

from auto_readme import AutoREADME_Client


css = ".json {height: 527px; overflow: scroll;} .json-holder {height: 527px; overflow: scroll;}"
with gr.Blocks(css=css) as demo:
    state = gr.State(value={"client": AutoREADME_Client()})
    gr.Markdown("<h1><center>Enjoy Auto README!</center></h1>")
    gr.Markdown("<p align='center'><img src='./resource/logo.png' height='25' width='95'></p>")
    gr.Markdown(
        "<p align='center' style='font-size: 20px;'> A Smart README Generate AI Power by <a href='https://chat.openai.com/'>ChatGPT</a>.</p>")
    gr.HTML(
        '''<center>Note: Online OpenAI API may sometimes not be available. The author provides his own OpenAI key for everyone to test! Thanks to the author!</center>''')
    with gr.Row().style():
        with gr.Column(scale=0.85):
            openai_api_key = gr.Textbox(
                show_label=False,
                placeholder="The author has limited funds, recommon to use your own OpenAI API",
                lines=1,
                type="password"
            ).style(container=False)
        with gr.Column(scale=0.15, min_width=0):
            key_btn = gr.Button("Submit").style(full_height=True)

    with gr.Row().style():
        with gr.Column(scale=0.6):
            chatbot = gr.Chatbot([], elem_id="chatbot").style(height=500)
            with gr.Column(scale=0.85):
                chat_txt = gr.Textbox(
                    show_label=False,
                    placeholder="Enter text and press enter. The url must contain the media type. e.g, https://example.com/example.jpg",
                    lines=1,
                ).style(container=False)
            with gr.Column(scale=0.15, min_width=0):
                chat_btn = gr.Button("Send").style(full_height=True)
        with gr.Column(scale=0.4):
            results = gr.Markdown('# Your`s README')

    def set_key(state, openai_api_key):
        return state["client"].set_key(openai_api_key)

    def add_text(state, chatbot, txt):
        return state["client"].add_text(chatbot, txt)

    def bot(state, chatbot):
        return state["client"].bot(chatbot)


    openai_api_key.submit(set_key, [state, openai_api_key], [openai_api_key])
    key_btn.click(set_key, [state, openai_api_key], [openai_api_key])

    chat_txt.submit()
    chat_btn.click()
    results.update()
    gr.Examples(
        examples=[
            "Please generate a README template for me",
            ],
        inputs=chat_txt
    )

demo.launch()