import openai
import os

class AiConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # 인스턴스가 없는 경우에만 openai.OpenAI 객체를 생성합니다.
            cls._instance = super(AiConfig, cls).__new__(cls)
            # 여기에 OpenAI API 키를 설정합니다.
            openai.api_key = os.getenv("OPEN_API_KEY")
            # 필요한 경우 추가적인 클라이언트 구성을 여기서 수행할 수 있습니다.
        return cls._instance

# 클라이언트 인스턴스를 얻는 방법
client = AiConfig()

# 같은 인스턴스인지 확인
client2 = AiConfig()
print(client is client2)  # True 출력