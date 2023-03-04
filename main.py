from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import os
import openai
import uuid
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from typing import List, Dict
import json
import requests


##todo
#reset 
#migrate to azure functions or aws equivalent


try:
    #config file contains env var to test in local 
    # if u clone directly from github, there is no config file there. please ask the dev.
    
    from config import load_env_var #in gitignore
    load_env_var()
    print("In Local Dev",flush=True)
except:
    print("In Cloud or missing config.py file",flush=True)

## initialization-----------------------
FRONT_END_URL = os.environ["FRONT_END_URL"]

origins = [
FRONT_END_URL
]

# here we using starllette middleware instead of FastAPI built in  middleware because of bug
middleware = [
    Middleware(CORSMiddleware, allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])
]

app = FastAPI(middleware=middleware)


class Data(BaseModel):
    role:str
    content:str

class ChatItem(BaseModel):
    id:int
    data:Data

class ChatItems(BaseModel):
    message:List[ChatItem] #not really sure here
    key:str

class Chat:
    def __init__(self,key):
        self.key = key
        self.id = str(uuid.uuid4())
        self.total_token = 0

    def __get_openai_reply(self,whole_messages):
        try:
            url = "https://api.openai.com/v1/chat/completions"

            payload = json.dumps({
                "model": "gpt-3.5-turbo",
                "messages": jsonable_encoder([message.data for message in whole_messages])
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.key}'
            }

            completion= requests.request("POST", url, headers=headers, data=payload).json()
            answer = completion["choices"][0]["message"]["content"]
            self.total_token = completion["usage"]["total_tokens"]
            
        except Exception as err:
            print(f"Error getting OpenAI reply: {err}")
            answer = f"Sorry, Internal Server Issue: {err}"
       
        return answer


    def send_messages(self, whole_messages):
        """
        whole_messages is Array of Dicts
        """
        
        reply = {"id":len(whole_messages),"data":{"role": "assistant", "content": self.__get_openai_reply(whole_messages)}} #will wait until get reply

        return reply



@app.post("/message2")
async def send_messages(messages: ChatItems):
    ##message is array of dictionaries
    
    chat = Chat(key=messages.key)
    response = chat.send_messages(whole_messages=messages.message)
    return {"message": response} # return back the reply only

