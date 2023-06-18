import json
import openai
import tiktoken


# OPENAI_KEY = os.environ.get("OPENAI_KEY")

# os.makedirs("public/images", exist_ok=True)
# os.makedirs("public/audios", exist_ok=True)
# os.makedirs("public/videos", exist_ok=True)

class AutoREADME_Client:
    def __init__(self, max_history=20):
        self.OPENAI_KEY = None
        self.MODEL_NAME = "gpt-3.5-turbo-0613"
        self.MAX_HISTORY = max_history
        self.system_prompt = "Your task is to modify the content of the README file of his open source project according to the user's needs." \
                             "When you think there is not enough information to write a README, ask the user to get the information they need. " \
                             "Guide users how to write README when necessary." \
                             "Try to modify it according to the existing readme and the information it provides, rather than completely re-upgrade the car for you" \
                             "Unless specified by the user, try to write the README in English, but communicate with the user according to the user's language." \
                             "Whenever user want to generate or modify the readme code,You must use the function: 'output_readme'!!\n\n"

    def set_key(self, openai_api_key):
        self.OPENAI_KEY = openai_api_key
        return openai_api_key

    def set_model(self, model_name):
        assert model_name in ["gpt-3.5-turbo-0613", "gpt-4-0613"], NotImplementedError(
            f"""set_model() is not presently implemented for model {self.MODEL_NAME}.
                  See https://github.com/openai/openai-python/blob/main/chatml.md for 
                  information on how messages are converted to tokens.""")
        self.MODEL_NAME = model_name
        return model_name

    def set_system_prompt(self, system_prompt):
        self.system_prompt = system_prompt
        return system_prompt

    def chat_with_gpt(self, chat_history, message, readme):
        if not self.OPENAI_KEY or not self.OPENAI_KEY.startswith(
                "sk-"):
            return chat_history, "Please set your OpenAI API key first!!!", readme

        messages = [
            {"role": "system", "content": self.system_prompt},
        ]
        for user, assistant in chat_history[-self.MAX_HISTORY:]:
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
            {"role": "function", "name": "get_current_readme", "content": f"{readme}"}
        )
        messages.append(
            {"role": "user", "content": message}
        )
        delete_num = 0
        # while self._num_tokens_from_messages(messages) < 3500:


        return_message, func = self._use_chatgpt(messages)
        chat_history.append((message, return_message))
        if func is None:
            readme = readme
        else:
            # func = json.loads(str(func))
            if func['name'] == 'output_readme':
                arguments = func['arguments']
                readme = json.loads(arguments)['readme_str']
            else:
                readme = readme

        return chat_history, "", readme

    def _readme_prompt(self, readme):
        prompt = f"The markdown code of the current README is as follows:\n{readme}\n\n"
        return prompt

    def _use_chatgpt(self, messages):
        # openai.Model.retrieve("gpt-3.5")
        openai.api_key = self.OPENAI_KEY
        response = openai.ChatCompletion.create(
            model=self.MODEL_NAME,
            messages=messages,
            functions=[
                {
                    "name": "output_readme",
                    "description": "output README to user when user asking for generate a new readme or modify current readme",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "readme_str": {
                                "type": "string",
                                "description": "the markdown format string"
                            },
                        },
                        "required": ["readme_str"]
                    }
                },
                # {
                #     "name": "get_current_readme",
                #     "description": "Get the user's current readme and return it as a string",
                #     "parameters": {
                #         "type": "object",
                #         "properties": {
                #         },
                #     }
                # }
            ],
        )
        if response.get("function_call"):
            func = response.choices[0].message["function_call"]
            return "WRITING README...", func
        return response.choices[0].message["content"], None

    def _num_tokens_from_messages(self, messages):
        """Returns the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model_name=self.MODEL_NAME)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if self.MODEL_NAME == "gpt-3.5-turbo-0613":  # note: future models may deviate from this
            num_tokens = 0
            for message in messages:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        else:
            raise NotImplementedError(
                f"""num_tokens_from_messages() is not presently implemented for model {self.MODEL_NAME}.
      See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
