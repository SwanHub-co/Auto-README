import json
import os
import openai

# OPENAI_KEY = os.environ.get("OPENAI_KEY")

# os.makedirs("public/images", exist_ok=True)
# os.makedirs("public/audios", exist_ok=True)
# os.makedirs("public/videos", exist_ok=True)

class AutoREADME_Client:
    def __init__(self):
        self.OPENAI_KEY = None
        self.system_prompt = "Your task is to modify the content of the README file of his open source project according to the user's needs." \
                             "When you think there is not enough information to write a README, ask the user to get the information they need. " \
                             "Guide users how to write README when necessary." \
                             "Try to modify it according to the existing readme and the information it provides, rather than completely re-upgrade the car for you" \
                             "Unless specified by the user, try to write the README in English, but communicate with the user according to the user's language." \
                             "When you want to output the readme, use the function\n\n"

    def set_key(self, openai_api_key):
        self.OPENAI_KEY = openai_api_key
        return openai_api_key

    def set_system_prompt(self, system_prompt):
        self.system_prompt = system_prompt
        return system_prompt

    def chat_with_gpt(self, chat_history, message, readme):
        if not self.OPENAI_KEY or not self.OPENAI_KEY.startswith(
                "sk-"):
            return chat_history, "Please set your OpenAI API key and Hugging Face token first!!!", readme

        # chat_history.append((message, "Please set your OpenAI API key and Hugging Face token first!!!"))

        messages = [
            {"role": "system", "content": self.system_prompt},
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
            {
                "role": "system", "content":self._readme_prompt(readme)
            }
        )
        messages.append(
            {"role": "user", "content": message}
        )
        return_message, func = self._use_chatgpt(messages)
        chat_history.append((message, return_message))
        if func is None:
            readme = readme
        else:
            # func = json.loads(str(func))
            arguments =func['arguments']
            readme=json.loads(arguments)['readme_str']
            # raise 'stop'

        return chat_history, "", readme

    def _readme_prompt(self,readme):
        prompt=f"The markdown code of the current README is as follows:\n{readme}\n\n"
        return prompt

    def _use_chatgpt(self, messages):
        # openai.Model.retrieve("gpt-3.5")
        openai.api_key = self.OPENAI_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=[
                {
                    "name": "write_readme",
                    "description": "Write down the markdown format README file",
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
                }
            ]
        )
        content = response.choices[0].message["content"]
        if content is None:
            return "WRITING README...", response.choices[0].message["function_call"]
        return response.choices[0].message["content"], None
