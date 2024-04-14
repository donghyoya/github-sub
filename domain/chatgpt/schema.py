from pydantic import BaseModel, ConfigDict
from typing import Optional

class ChatBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    question: Optional[str]
    answer: Optional[str]

class ReqChat(ChatBase):

    question: str

class ResChat(ChatBase):

    answer: str