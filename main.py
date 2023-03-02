from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import openai
import uuid

try:
    #config file contains env var to test in local also contains credentials
    # if u clone directly from github, there is no config file there. please ask the dev.
    
    from config import load_env_var #in gitignore
    load_env_var()
    print("In Local Dev",flush=True)
except:
    print("In Cloud or missing config.py file",flush=True)

app = FastAPI()

class ChatMessage(BaseModel):
    content: str

class Chat:
    def __init__(self, title):
        self.title = title
        self.id = str(uuid.uuid4())
        self.system_prompt = "You are a helpful assistant."
        self.messages = [{"id":0,"data":{"role":"system","content": "You are a helpful assistant."}}]
        self.__auth()
        self.total_token = 0

    def __auth(self):
        openai.api_key = os.environ["OPENAI_API_KEY"]
    
    def __add_id(self):
        return len(self.messages)

    def __get_data_values(self):
        return [message['data'] for message in self.messages]

    def __get_openai_reply(self):
        try:
            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.__get_data_values())
            answer = completion["choices"][0]["message"]["content"]
            self.total_token = completion["usage"]["total_tokens"]
            print(answer)
        except Exception as err:
            print(f"Error getting OpenAI reply: {err}")
            answer = "Sorry, Internal Server Issue"
       
        return answer

    def add_message(self, content):
        message = {"id":self.__add_id(),"data":{"role": "user", "content": content}}
        self.messages.append(message) 
        reply = {"id":self.__add_id(),"data":{"role": "assistant", "content": self.__get_openai_reply()}}
        self.messages.append(reply)

chat = Chat("My Chat")

@app.post("/message")
async def add_message(message: ChatMessage):
    chat.add_message(message.content)
    return {"message": "Message added successfully."}

@app.get("/messages")
async def get_messages():
    return {"messages": chat.messages}