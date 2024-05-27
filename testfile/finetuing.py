from openai import OpenAI
import os
import json
from collections import OrderedDict
from datetime import datetime

client = OpenAI(
    api_key=os.getenv("OPEN_API_KEY")
)

response = client.completions.create(
    model="g-zIfisGF9c-java-spring-mentor",
    prompt="can you recomend spring version?"
)


# client.models.delete("ft:gpt-3.5-turbo-0125:acemeco:suffix:vi1zS0p505jfbLAHuBnRmsKh")
# client.models.delete("ft:gpt-3.5-turbo:acemeco:suffix:4tOtCopIxESLQrxzOFysrqoV")
# client.models.delete("ft:gpt-3.5-turbo:acemeco:suffix:gYgGeLWBMpx83LBOB4X2365p")

# 파인튜닝할 데이터 업로드
# response1 = client.files.create(
#     file=open("isms2.jsonl","rb"),
#     purpose="fine-tune"
# )

# print(response1)

# 파인튜닝 할 파일을 통해 사용할 모델
# response2 = client.fine_tuning.jobs.create(
#     training_file="file-9P13yNPWOZCv4ZUtOy5y9ktM",
#     model="gpt-3.5-turbo"
# )


# 파인튜닝한 목록
# client.fine_tuning.jobs.list(limit=10)

# 파인튜닝 작업 조회


# 파인튜닝할때 어덯게 작업할건지
'''
client.fine_tuning.jobs(

)
'''

# chatgpt 에게 전송할 메시지 설정
'''
client.completions.create(
    model="" #사용할 gtp 모델

)
'''
