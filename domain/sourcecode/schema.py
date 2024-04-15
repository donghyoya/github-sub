from pydantic import BaseModel, Field
from typing import Optional


class SourceCodeSchema(BaseModel):
    sid: Optional[int] = Field(None, example=1)
    sourceName: Optional[str] = Field(None, example="HelloWorld")
    sourceCode: Optional[str] = Field(None, example="print('Hello World')")
    path: Optional[str] = Field(None, example="/home/user/helloworld.py")
    url: Optional[str] = Field(None, examples="https://test.test.com")
    rid: int

    class Config:
        orm_mode = True
