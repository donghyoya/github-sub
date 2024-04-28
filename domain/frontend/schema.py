from pydantic import BaseModel


class RepositoryForm(BaseModel):
    url : str

class RequestAiForm(BaseModel):
    username : str
    reponame : str