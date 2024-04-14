from fastapi import FastAPI, Depends
from pydantic import BaseSettings
import openai
import os

class AiConfig(BaseSettings):
    openai_api_key: str

    class Config:
        # 환경 변수의 이름을 명시적으로 지정할 수 있습니다.
        # 이 경우, 'OPENAI_API_KEY' 환경 변수의 값을 'openai_api_key' 필드에 로드합니다.
        env_file = ".env"
        env_file_encoding = 'utf-8'
        fields = {
            'openai_api_key': {
                'env': 'OPENAI_API_KEY',
            },
        }

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            # OpenAI 클라이언트의 API 키 설정
            openai.api_key = cls._instance.openai_api_key
        return cls._instance
