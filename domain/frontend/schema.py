from pydantic import BaseModel


class RepositoryForm(BaseModel):
    url : str
