from pydantic import BaseModel

class RepoForm(BaseModel):
    url : str
    options: list
