from fastapi import FastAPI, Depends
from pydantic_settings import BaseSettings
import openai
from typing import ClassVar

class AiConfig(BaseSettings):
    openai_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

    _instance = None
    client: ClassVar[openai.Completion] = None  # ClassVar 타입 어노테이션 추가

    def __init__(self, **values):
        super().__init__(**values)
        if not AiConfig.client:
            # OpenAI 클라이언트 초기화
            AiConfig.client = openai.Completion()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def chat(self, prompt, model="gpt-3.5-turbo", max_tokens=50):
        return AiConfig.client.create(
            engine=model,
            prompt=prompt,
            max_tokens=max_tokens
        )
