import os
import openai

# OPENAI_KEY = os.environ.get("OPENAI_KEY")
OPENAI_KEY = "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"


# os.makedirs("public/images", exist_ok=True)
# os.makedirs("public/audios", exist_ok=True)
# os.makedirs("public/videos", exist_ok=True)

class AutoREADME_Client:
    def __init__(self):
        self.OPENAI_KEY = None
        self.system_prompt = "you are a assistant AI"

    def set_key(self, openai_api_key):
        self.OPENAI_KEY = openai_api_key
        return openai_api_key

    def set_system_prompt(self, system_prompt):
        self.system_prompt = system_prompt
        return system_prompt

    def chat_with_gpt(self, chat_history, message):
        if not self.OPENAI_KEY or not self.OPENAI_KEY.startswith(
                "sk-"):
            return chat_history, "Please set your OpenAI API key and Hugging Face token first!!!", "Your`s Readme"

        # chat_history.append((message, "Please set your OpenAI API key and Hugging Face token first!!!"))

        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        for user, assistant in chat_history:
            messages.append(
                {"role": "user", "content": user}
            )
            messages.append(
                {"role": "assistant", "content": assistant}
            )
        messages.append(
            {"role": "system", "content": self.system_prompt}
        )
        messages.append(
            {"role": "user", "content": message}
        )
        return_message = self._use_chatgpt(messages)
        chat_history.append((message, return_message))
        return chat_history, "", "# I`m here"  # readme

    def _use_chatgpt(self, messages):
        # openai.Model.retrieve("gpt-3.5")
        openai.api_key = self.OPENAI_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages
        )
        return response.choices[0].message["content"]
