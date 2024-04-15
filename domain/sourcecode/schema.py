from pydantic import BaseModel, Field
from typing import Optional

class SourceCode(BaseModel):
    sid: int | None
    sourceName: str | None = Field(None, examples="testRepository.java")
    path: str | None = Field(None, examples="/src/main/java/com/company/project/domain/user/repository/")
    rid: int | None

    class Config:
        orm_mode = True

