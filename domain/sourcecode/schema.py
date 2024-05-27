from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class SourceCodeSchema(BaseModel):
    sid: Optional[int] = Field(None, example=1)
    sourceName: Optional[str] = Field(None, example="HelloWorld")
    sourceCode: Optional[str] = Field(None, example="print('Hello World')")
    path: Optional[str] = Field(None, example="/home/user/helloworld.py")
    url: Optional[str] = Field(None, examples="https://test.test.com")
    rid: int

    class Config:
        from_attributes = True
class SourceCodeReadSchema(BaseModel):
    sid: int
    sourceName: str
    sourceCode: str
    path: str
    url: str
    language: str
    rid: int
    

    def config() -> ConfigDict:
        return ConfigDict(from_attributes=True)