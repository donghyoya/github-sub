from fastapi import FastAPI, Depends
from pydantic_settings import BaseSettings
import openai
from typing import ClassVar
import os

class AiConfig(BaseSettings):
    openai_api_key: str = os.getenv("OPEN_API_KEY")
    model: str = "gpt-3.5-turbo"
    messages: list = []

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"  # 정의되지 않은 필드를 무시
        fields = {
            'openai_api_key': {
                'env': 'OPENAI_API_KEY',
            },
        }
        

    _instance = None
    client: ClassVar[openai.OpenAI] = None

    def __init__(self, **values):
        super().__init__(**values)
        if not AiConfig.client:
            # API 키를 클라이언트에 설정
            openai.api_key = self.openai_api_key
            # openai.Completion 대신 기본 openai 클라이언트 사용
            AiConfig.client = openai


    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def chat(self, prompt, model="gpt-3.5-turbo", max_tokens=50):
        # 인스턴스 메서드로 변경하고, self.messages로 접근
        self.messages.append({
            'role': 'user', 
            'content': prompt
        })
        completion = openai.chat.completions.create(
            model=model,
            messages=self.messages,
            max_tokens=max_tokens
        )
        response = completion.choices[0].message.content
        self.messages.append({
            'role': 'assistant', 
            'content': response
        })
        return response