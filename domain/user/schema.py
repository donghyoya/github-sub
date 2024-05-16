from pydantic import BaseModel, Field
from typing import Optional

class GithubUserSchema(BaseModel):
    username: Optional[str] = Field(None, examples="testusername")
    site: Optional[str] = Field(None, examples="https://github/donghyoya")
    connectCnt: Optional[int] = Field(None, examples=1)
    follower: Optional[int] = Field(None, examples=1)
    following: Optional[int] = Field(None, examples=1)

    class Config:
        from_attributes = True

class CreateUserSchema(GithubUserSchema):
    username: str
    site: str
    connectCnt: int
    follower: int
    following: int

