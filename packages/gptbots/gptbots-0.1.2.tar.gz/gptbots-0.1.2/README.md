# gptbots

A simple Python package for creating and interacting with GPT-based chatbots

Make sure your OpenAI API key is setup (see [OpenAI's Quickstart tutorial](https://platform.openai.com/docs/quickstart?context=python)).

## Usage

`bot = Chatbot()`: create a chatbot instance with default attributes
`bot = Chatbot(model, temperature, custom_instructions, chatbot_name)`: create a chatbot instance with custom attributes

### Attributes
- model: default is "gpt-3.5-turbo-1106"; see [OpenAI's documentation on models](https://platform.openai.com/docs/models/) for valid model names
- temperature: default is 0.7; ranges from 0.0 to 1.0; higher generally means more creative
- custom\_instructions: default is "You are a helpful assistant."
- chatbot\_name: default is "Assistant"
- context: contains custom instructions, user messages, and chatbot responses

## Functions
- `chat(prompt)`: prints chatbot response to string prompt
- `chat_image(prompt, url)`: prints chatbot response to string prompt + image URL (when using "gpt-4-vision-preview" (aka GPT-4 Turbo with vision)
- `save(file_path)`: saves chat history and settings to preferred file
- `load(file_path)`: loads chat history and settings from preferred file
- `print_messages()`: prints context without custom instructions in a prettier format
- `print_context()`: prints context in a prettier format
