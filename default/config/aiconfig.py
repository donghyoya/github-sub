from fastapi import FastAPI, Depends
from pydantic_settings import BaseSettings, SettingsConfigDict
import openai
from typing import ClassVar
import os

class AiConfig(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env")

    openai_api_key: str
    model: str
    messages: list = []
        
    _instance = None
    client: ClassVar[openai.OpenAI] = None


    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def chat(self, prompt, max_tokens=50):
        # 인스턴스 메서드로 변경하고, self.messages로 접근
        self.messages.append({
            'role': 'user', 
            'content': prompt
        })

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=max_tokens
        )
        response = completion.choices[0].message.content
        self.messages.append({
            'role': 'assistant', 
            'content': response
        })
        return response