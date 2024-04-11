from fastapi import FastAPI
from starlette.background import BackgroundTasks

from repository.DelegateSourceRepository import DelegateSourceRepository
from repository.DictionaryCrawlRepository import DictionaryCrawlRepository
from repository.DictionaryStatusRepository import DictionaryStatusRepository
from repository.MariaRepository import MariaRepository
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

# repository 작성 후
datasource = {
    'user': 'admin',
    'password': 'admin',
    'host': 'localhost',
    'port': '3306',
    'database': 'github_sub'
}
sourceRepository = MariaRepository(datasource) # 이 객체만 교체하면 가능함
statusRepository = DictionaryStatusRepository()
repository = DelegateSourceRepository(statusRepository, sourceRepository)

repoMatcher = RepoMatcher()

def crawlBackgroundService(form: RepoForm, repoId:tuple):
    work_status = repository.existsRepoById(repoId)

    if work_status != "NONE" and work_status != "FAIL":
        # 작업이 이미 진행중이고, 실패하지 않았다면 새 작업을 시작하지 않음
        return
    else:
        repository.saveStatusById(repoId, "WORKING")

    try:
        crawler = GitCrawler()
        crawler.startCrawl(form.url, form.options)
        sources = crawler.getSrcFiles()
        repository.saveRepoById(repoId, sources)
    except Exception as e:
        # 에러 발생시 fail
        repository.saveStatusById(repoId, "FAIL")

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
    id = (username, reponame)
    status = repository.existsRepoById((username, reponame))
    if status == "DONE":
        # 작업 완료
        data = repository.findRepoById(id)
        return {
            "code" : "DONE",
            "message": "There is Git Repository",
            "data" : data
        }
    elif status == "FAIL":
        # 작업 실패
        return {
            "code" : "FAIL",
            "message" : "Crawling Failed. Checked Your Request and Please try again"
        }
    elif status == "WORKING":
        return {
            "code" : "WORKING",
            "message" : "Crawling data now. wait some minute"
        }
    else:
        return {
            "code" : "NONE",
            "message" : "There is no such git repository"
        }
