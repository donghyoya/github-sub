from fastapi import FastAPI
from starlette.background import BackgroundTasks

from repository.InMemoryCrawlRepository import InMemoryCrawlRepository
from utils.RepoMatcher import RepoMatcher
from form.RepoForm import *
from utils.crawler.GitCrawler import GitCrawler
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

repoRepository = InMemoryCrawlRepository()
repoMatcher = RepoMatcher()

def crawlBackgroundService(form: RepoForm, repoId):
    if repoRepository.existRepoId(repoId):
        return
    crawler = GitCrawler()
    crawler.startCrawl(form.url)
    sources = crawler.getSrcFiles()
    repoRepository.saveRepoById(repoId, sources)

@app.get("/")
async def root():
    return {"endfoints": ["/repo"]}

@app.get("/repo")
def repo_root():
    return {
        "endfoints" : {
            "/repo/query" : {
                "method" : "POST",
                "description" : "query할 repository를 입력하는 endpoint",
                "parameter" : {
                    "url" : "repository의 url. 현 버전에서는 https://까지 포함되어야함"
                }
            },
            "/repo/<user-name>/<repo-name>":{
                "method" : "GET",
                "description" : "크롤링된 repository 확인할 수 있다.",
            }
        }
    }

@app.post("/repo/query")
async def query_repo(
        crawlTask: BackgroundTasks,
        form: RepoForm
    ):
    if repoMatcher.regex_match(form.url):
        repoInfo = repoMatcher.get_repo_name(form.url)
        crawlTask.add_task(crawlBackgroundService, form, repoInfo)
    return {'username' : repoInfo[0], 'reponame' : repoInfo[1]}

@app.get("/repo/{username}/{reponame}")
async def get_repo(username: str, reponame: str):
    if repoRepository.existRepoId((username, reponame)):
        return {
            "code" : 1,
            "data" : repoRepository.findRepoById((username, reponame))
        }
    else:
        return {
            "code" : 2,
            "message" : "not yet"
        }
