from pydantic import BaseModel, Field
from typing import Optional

class GithubUserSchema(BaseModel):
    uid: Optional[int]
    username: Optional[str] = Field(None, examples="testusername")
    site: Optional[str] = Field(None, examples="https://github/donghyoya")
    connectCnt: Optional[str] = Field(None, 1)
    follower: Optional[str] = Field(None, 1)
    following: Optional[str] = Field(None, 1)

    class Config:
        orm_mode = True

class CreateUserSchema(GithubUserSchema):
    username: str
    site: str
    connectCnt: int
    follower: int
    following: int


