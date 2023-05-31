import openai


class ReadmeGenerator:
    def __init__(self):
        self.start_prompt = """
        You are a README.md generator whose goal is to generate README resource code in the style of GitHub open-resource projects. 
        You must generate the README based on user input regarding project information and key code, 
        leaving unknown information blank by using "X". The README should be written in English, not other language.
         A good README must include the following sections:
        Project logo or icon (required, need provide a sample program.)
        Introduction (required)
        Changelog (optional)
        Get Started (required)
        Contact or Citation (required)
        Contribute (optional)
        License (default to GPL if not provided)
        Only return an example README.md using Markdown resource code.\n\n
        """

    def run(self, project_information: dict):
        information = "Here is the open-resource project information which will include this README:\n"
        for k in project_information.keys():
            information += "P{} : {}\n\n".format(k.upper(), project_information[k])
        self.start_prompt += information
        return self.use_chatgpt(self.start_prompt)

    def use_chatgpt(self, text):
        # openai.Model.retrieve("gpt-3.5")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"{text}"}
            ]
        )
        return completion.choices[0].message


if __name__ == '__main__':
    import os

    openai.api_key = os.getenv("OPENAI_KEY")
    # openai.organization = os.getenv("OPENAI_ORG")
    # openai.proxy = {
    #     "http": "http://127.0.0.1:7890",
    #     "https": "http://127.0.0.1:7890",
    # }

    generate = ReadmeGenerator()
    project={
        "Introduce":"""
        照片主题AI模型，目前支持的类标包括： ['childlike', 'christmas', 'city', 'dragonboat', 'east_building', 'excting_sport', 'food', 'inhome', 'leisure_sport', 'nature', 'night', 'pet', 'portrait', 'shop', 'snow', 'spring', 'transport', 'west_building']
        """,
        "get start":"""
        环境依赖：仅测试了python 3.8以上版本。理论上无python版本限制 需要使用的package：

pip install numpy
pip install torch
pip install torchvision
pip install opencv-python
pip install onnx
pip install onnxruntime
# 可选
pip install gradio
运行命令：
python onnx_infer.py
会返回所有支持的类标号，测试结果对各个类标的置信度，以及最终预测标签（有序）
        """,
        'contact me':"""
        作者：陈少宏，邮件：611699999@qq.com
        """

    }
    print(generate.run(project))