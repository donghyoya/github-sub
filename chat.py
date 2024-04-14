import openai
import os

# OpenAI API 키 설정
openai.api_key = os.getenv("OPEN_API_KEY")

class ChatBot():
    def __init__(self, model=os.getenv("OUTPUT_MODEL")):
        self.model = model
        self.messages = []
        
    def ask(self, question):
        self.messages.append({
            'role': 'user', 
            'content': question
        })
        res = self.__ask__()
        return res
        
    def __ask__(self):
        completion = openai.chat.completions.create(
            # model 지정d
            model=self.model,
            messages=self.messages
        )
        response = completion.choices[0].message.content
        self.messages.append({
            'role': 'assistant', 
            'content': response
        })
        return response
    
    def show_messages(self):
        return self.messages
    
    def clear(self):
        self.messages.clear()

chatbot = ChatBot(model=os.getenv("OUTPUT_MODEL"))

while(True):
    userinput = input("나: ")
    if(userinput==""):
        break
    resmsg = chatbot.ask(userinput)
    print(resmsg)