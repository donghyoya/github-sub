from pydantic import BaseModel, Field
from typing import Optional

class RepositorySchema(BaseModel):
    rid: int
    language: Optional[str] = Field(None, examples="java")
    connectCnt: Optional[int] = Field(None, examples=1)
    repoName: Optional[str] = Field(None, examples="exampleRepository")
    guid: int

    class Config:
        orm_mode = True
