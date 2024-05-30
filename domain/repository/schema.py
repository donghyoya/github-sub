from pydantic import BaseModel, Field
from typing import Optional

class RepositorySchema(BaseModel):
    rid: Optional[int] = Field(None, description="")
    language: Optional[str] = Field(None, examples="java")
    connectCnt: Optional[int] = Field(None, examples=1)
    repoName: Optional[str] = Field(None, examples="exampleRepository")
    guid: int

    class Config:
        from_attributes = True

class RepositoryRead(BaseModel):
    rid: Optional[int] = Field(None, description="The unique identifier of the repository")
    language: Optional[str] = Field(None, examples="java")
    connectCnt: Optional[int] = Field(None, examples=1)
    repoName: Optional[str] = Field(None, examples="exampleRepository")
    guid: Optional[int]

class RepositoryUpdate(BaseModel):
    language: Optional[str] = Field(None, examples="java")
    connectCnt: Optional[int] = Field(None, examples=1)
    repoName: Optional[str] = Field(None, examples="exampleRepository")