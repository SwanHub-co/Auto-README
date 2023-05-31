import os

import gradio as gr

os.makedirs("public/images", exist_ok=True)
os.makedirs("public/audios", exist_ok=True)
os.makedirs("public/videos", exist_ok=True)

OPENAI_KEY = os.environ.get("OPENAI_KEY")


css = ".json {height: 527px; overflow: scroll;} .json-holder {height: 527px; overflow: scroll;}"
with gr.Blocks(css=css) as demo:
    state = gr.State(value={"client": Client()})
    gr.Markdown("<h1><center>Enjoy Auto README!</center></h1>")
    gr.Markdown("<p align='center'><img src='./resource/logo.png' height='25' width='95'></p>")
    gr.Markdown(
        "<p align='center' style='font-size: 20px;'> A Smart README Generate AI Power by <a href='https://chat.openai.com/'>ChatGPT</a>.</p>")
    gr.HTML(
        '''<center>Note: Online OpenAI API may sometimes not be available. The author provides his own OpenAI key for everyone to test! Thanks to the author!</center>''')
    if not OPENAI_KEY:
        with gr.Row().style():
            with gr.Column(scale=0.85):
                openai_api_key = gr.Textbox(
                    show_label=False,
                    placeholder="The author has limited funds, try to use his own OpenAI API",
                    lines=1,
                    type="password"
                ).style(container=False)
            with gr.Column(scale=0.15, min_width=0):
                btn1 = gr.Button("Submit").style(full_height=True)

    with gr.Row().style():
        with gr.Column(scale=0.6):
            chatbot = gr.Chatbot([], elem_id="chatbot").style(height=500)
        with gr.Column(scale=0.4):
            results = gr.Code(elem_classes="markdown")

    with gr.Row().style():
        with gr.Column(scale=0.85):
            txt = gr.Textbox(
                show_label=False,
                placeholder="Enter text and press enter. The url must contain the media type. e.g, https://example.com/example.jpg",
                lines=1,
            ).style(container=False)
        with gr.Column(scale=0.15, min_width=0):
            btn2 = gr.Button("Send").style(full_height=True)


    def set_key(state, openai_api_key):
        return state["client"].set_key(openai_api_key)


    def add_text(state, chatbot, txt):
        return state["client"].add_text(chatbot, txt)


    def set_token(state, hugging_face_token):
        return state["client"].set_token(hugging_face_token)


    def bot(state, chatbot):
        return state["client"].bot(chatbot)


    if not OPENAI_KEY:
        openai_api_key.submit(set_key, [state, openai_api_key], [openai_api_key])
        btn1.click(set_key, [state, openai_api_key], [openai_api_key])

    if not HUGGINGFACE_TOKEN:
        hugging_face_token.submit(set_token, [state, hugging_face_token], [hugging_face_token])
        btn3.click(set_token, [state, hugging_face_token], [hugging_face_token])

    txt.submit(add_text, [state, chatbot, txt], [chatbot, txt]).then(bot, [state, chatbot], [chatbot, results])
    btn2.click(add_text, [state, chatbot, txt], [chatbot, txt]).then(bot, [state, chatbot], [chatbot, results])

    gr.Examples(
        examples=[
            "Please generate a README template for me",
            ],
        inputs=txt
    )

demo.launch()