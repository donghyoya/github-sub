from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class AiResultSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    model: Optional[str] = Field(None, example="ModelX")
    answer: Optional[str] = Field(None, example="Answer Example")
    score: Optional[int] = Field(None, example=85)
    rid: int

class AiSettingSchema(BaseModel):

    model: Optional[str] = Field(None, example="turbo3.5")
    answer: Optional[str] = Field(None, "blabla")