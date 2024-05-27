from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class GithubUserSchema(BaseModel):
    uid: Optional[int] = Field(None, description="")
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

class GithubUserReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: int
    username: str
    site: str
    connectCnt: int
    follower: int
    following: int

# Update용 스키마
class GithubUserUpdateSchema(BaseModel):
    username: Optional[str] = Field(None, example="updatedusername")
    site: Optional[str] = Field(None, example="https://github.com/updateddonghyoya")
    connectCnt: Optional[int] = Field(None, example=2)
    follower: Optional[int] = Field(None, example=2)
    following: Optional[int] = Field(None, example=2)
