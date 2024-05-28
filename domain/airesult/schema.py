from pydantic import BaseModel, Field, ConfigDict,\
    StringConstraints
from typing import Optional
from typing_extensions import Annotated

class AiResultSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    model: Optional[str] = Field(None, example="ModelX")
    answer: Optional[str] = Field(None, example="Answer Example")
    score: Optional[int] = Field(None, example=85)
    rid: int

class AiSettingSchema(BaseModel):
    model: Optional[str] = Field(None, example="turbo3.5")
    answer: Optional[str] = Field(None, example="blabla")

class AiResultBaseSchema(BaseModel):
    aid: int
    model: str
    answer: str
    score: int
    rid: int

    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     from_attributes=True
