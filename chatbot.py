from text_gen_api import TextGenAPI

class Chatbot:
    def __init__(self, text_gen_api):
        self.text_gen_api = text_gen_api

    def chat(self, user_input):
        response = self.text_gen_api.generate_text(user_input)
        return response

# 示例用法
if __name__ == "__main__":
    text_gen_api = TextGenAPI(base_url="http://localhost:7860")
    chatbot = Chatbot(text_gen_api)

    while True:
        user_input = input("You: ")
        response = chatbot.chat(user_input)
        print(f"Bot: {response}")