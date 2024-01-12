# Import libraries
from openai import OpenAI
import ast

# Create client
client = OpenAI()

# Define Chatbot class
class Chatbot:
    def __init__(self, model="gpt-3.5-turbo-1106", temperature=0.7, custom_instructions="You are a helpful assistant.", chatbot_name = "Assistant"):
        self.model = model
        self.temperature = temperature
        self.custom_instructions = custom_instructions
        self.chatbot_name = chatbot_name
        self.context = [{'role':'system', 'content':f'{custom_instructions}'}]

    def chat(self, prompt):
        self.context.append({"role": "user", "content":f'{prompt}'})
        if self.model == 'gpt-4-vision-preview':
            response = client.chat.completions.create(
                model=self.model,
                messages=self.context,
                temperature=self.temperature,
                max_tokens=2048
            )
        else:
            response = client.chat.completions.create(
                model=self.model,
                messages=self.context,
                temperature=self.temperature
            )
        self.context.append({"role": "assistant", "content":f'{response.choices[0].message.content}'})
        print(f"\n{self.chatbot_name}: {response.choices[0].message.content}\n")

    def chat_image(self, prompt, url):
        self.context.append({"role": "user", "content": [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": url
                }
            }
        ]})
        response = client.chat.completions.create(
            model=self.model,
            messages=self.context,
            temperature=self.temperature,
            max_tokens=300
        )
        self.context.append({"role": "assistant", "content":f'{response.choices[0].message.content}'})
        print(f"\n{self.chatbot_name}: {response.choices[0].message.content}")

    def save(self, file_path):
        with open(file_path, "w") as fp:
            fp.write(f"""{{"model": "{self.model}"}}\n"""\
                    f"""{{"custom_instructions": "{self.custom_instructions}"}}\n"""\
                    f"""{{"chatbot_name": "{self.chatbot_name}"}}\n"""\
                    f"""{{"temperature": "{self.temperature}"}}\n""") 
            for message in self.context:
                fp.write("%s\n" % message)
            print(f'\n\nChat history saved at {file_path}')
        with open("path_memory.txt", "r") as memory:
            lines = memory.readlines()
        with open("path_memory.txt", "w") as memory:
            for line in lines:
                if line.strip() != file_path.strip():
                    memory.write(line)
        with open("path_memory.txt", "a") as memory:
             memory.write(file_path + "\n")

    def load(self, file_path):
        settings = []
        messages = []

        with open(file_path, "r") as fp:
            for line in fp.readlines()[0:4]:
                x = ast.literal_eval(line[:-1])
                settings.append(x)
        with open(file_path, "r") as fp:
            for line in fp.readlines()[4:]:
                x = ast.literal_eval(line[:-1])
                messages.append(x)

        self.model = settings[0]['model']
        self.custom_instructions = settings[1]['custom_instructions']
        self.chatbot_name = settings[2]['chatbot_name']
        self.temperature = float(settings[3]['temperature'])
        self.context = messages

    def print_messages(self):
        for i in range(1, len(self.context) - 1):
            if self.context[i]['role'] == 'user':
                print(f"\nUser: {self.context[i]['content']}")
            else:
                print(f"\n{self.chatbot_name}: {self.context[i]['content']}")
        print("")

    def print_context(self):
        for i in range(0, len(self.context)):
            if self.context[i]['role'] == 'user':
                print(f"\nUser: {self.context[i]['content']}")
            elif self.context[i]['role'] == 'system':
                print(f"\nSystem: {self.context[i]['content']}")
            else:
                print(f"\n{self.chatbot_name}: {self.context[i]['content']}")
        print("")
