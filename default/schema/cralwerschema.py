from pydantic import BaseModel, Field
from typing import Optional

class CrawlerBaseSchema(BaseModel):
    username: str
    reponame: str

    def print(self):
        print(f'username: {self.username} reponame: {self.reponame}')