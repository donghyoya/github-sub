from pydantic import BaseModel, Field
from typing import Optional

class AiResultSchema(BaseModel):
    aid: int
    model: Optional[str] = Field(None, example="ModelX")
    answer: Optional[str] = Field(None, example="Answer Example")
    score: Optional[int] = Field(None, example=85)
    rid: int

    class Config:
        orm_mode = True
