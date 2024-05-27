from fastapi import FastAPI, Depends
from pydantic_settings import BaseSettings, SettingsConfigDict
import openai
from typing import ClassVar, Optional, List
import os

class AiConfig(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",  env_file_encoding='utf-8',
        env_ignore_empty=True,
        extra="ignore")

    openai_api_key: str
    output_model: str
    messages: List[dict] = []
        
    _instance: ClassVar[Optional['AiConfig']] = None
    client: ClassVar[Optional[openai.OpenAI]] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls.client = openai.OpenAI(api_key=cls._instance.openai_api_key)
        return cls._instance

    def chat(self, prompt, max_tokens=50):
        # 인스턴스 메서드로 변경하고, self.messages로 접근
        self.messages.append({
            'role': 'user', 
            'content': prompt
        })

        completion = self.client.chat.completions.create(
            model=self.output_model,
            messages=self.messages,
            max_tokens=max_tokens
        )
        response = completion.choices[0].message.content
        self.messages.append({
            'role': 'assistant', 
            'content': response
        })
        return response