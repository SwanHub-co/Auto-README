import os
import openai

# OPENAI_KEY = os.environ.get("OPENAI_KEY")
OPENAI_KEY = "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"


# os.makedirs("public/images", exist_ok=True)
# os.makedirs("public/audios", exist_ok=True)
# os.makedirs("public/videos", exist_ok=True)

class AutoREADME_Client:
    def __init__(self) -> None:
        self.OPENAI_KEY = OPENAI_KEY
        self.PROJECT_URL = None
        self.all_messages = []

        # prompt:
        system_prompt="""
        You are a README-generating AI, your goal is to generate the README document of the github open source project.
        and you need to chat with users to obtain user's open-source project information.
        Since Token is limited, a sample README must be generated for each conversation. 
        Open source README are usually in English.
        Generate the required README according to the user's project information. 
        Returns in the following format:
        {
            "README": "<the markdown format README generated with the user require>",
            "CHAT": the questions you ask to understand user needs
        }"""
        self.system_prompt={"role": "system", "content": system_prompt}

    def set_key(self, openai_key):
        self.OPENAI_KEY = openai_key
        return self.OPENAI_KEY

    def add_message(self, content, role):
        message = {"role": role, "content": content}
        self.all_messages.append(message)

    def add_text(self, messages, message):
        if not self.OPENAI_KEY or not self.OPENAI_KEY.startswith(
                "sk-"):
            return messages, "Please set your OpenAI API key and Hugging Face token first!!!"
        self.add_message(message, "user")
        messages = messages + [(message, None)]
        return messages, ""

    def bot(self, messages):
        if not self.OPENAI_KEY or not self.OPENAI_KEY.startswith(
                "sk-"):
            return messages, ""
        input_message=[self.system_prompt]+self.all_messages
        message = self._use_chatgpt(self.all_messages)
        result = None

        self.add_message(message, "assistant")
        messages[-1][1] = message
        return messages, result

    def _use_chatgpt(self, messages):
        # openai.Model.retrieve("gpt-4")
        openai.api_key=self.OPENAI_KEY
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return completion.choices[0].message


