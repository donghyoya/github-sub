from fastapi import APIRouter, BackgroundTasks, Query
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import re

router = APIRouter(
    tags=["crawler"]
    )

class GitCrawler:
    SOURCE_EXTENSION_PATTERN = r"\.([a-zA-Z0-9]+)$"

    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 10000)

    def start_crawl(self, root_url, extension_option):
        self.dir_set = set()
        self.src_file_urls = []
        self.queue = []

        self.queue.append(root_url)
        self.extension_option = set(extension_option)

        while self.queue:
            # print("self queue: ", self.queue)
            url = self.queue.pop(0)
            self.search_tree_dir(url)

    def search_tree_dir(self, url):
        # print('search_tree_dir')
        self.driver.get(url)
        atags = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        ).find_elements(By.TAG_NAME, "a")
        # atags = self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
        self.find_next_urls(atags)
        # print('search_tree_dir2')

    def find_next_urls(self, atags):
        for atag in atags:
            try:
                href = atag.get_attribute("href")
                if href and href not in self.dir_set:
                    self.dir_set.add(href)
                    src_extension = re.findall(self.SOURCE_EXTENSION_PATTERN, href)
                    if src_extension and src_extension[0] in self.extension_option:
                        self.src_file_urls.append((href, src_extension[0]))
                    elif "/tree" in href:
                        self.queue.append(href)
            except StaleElementReferenceException:
                # 요소가 stale 상태인 경우, 재시도
                self.driver.refresh()  # 페이지 새로고침
                self.search_tree_dir(self.driver.current_url)  # 현재 URL에서 재시도
                break  # 반복 중단

    def close(self):
        self.driver.quit()

    def get_src_files(self):
        src_files = []
        for url, extension in self.src_file_urls:
            # print(url, extension)
            src_file = self.get_src_file(url,extension)
            src_files.append(src_file)
        return src_files

    def get_src_file(self, url, extension):
        # print("get_src",url,extension)
        self.driver.get(url)
        textarea = self.wait.until(
            EC.presence_of_element_located((By.ID, 'read-only-cursor-text-area'))
        )
        # print("textarea",textarea)
        src = textarea.text
        # print("textarea", src)
        srcName = url.split("/")[-1]
        # print(srcName)
        return GitSrcFiles(
            url, srcName, src, extension
        )

class GitSrcFiles:
    GIT_TREE_PATTERNS = r'/blob/\w+/([a-zA-Z0-9\/-_]+)/'
    EXTENSTION_TO_LANG = {
        'java': 'java',
        'js': 'javascript',
        'py': 'python',
    }

    def __init__(self, url, title, src, extension):
        self.url = url
        dir = re.findall(GitSrcFiles.GIT_TREE_PATTERNS, url)
        self.directory = dir[0] if len(dir) == 1 else ''
        self.title = title
        self.src = src
        if extension in GitSrcFiles.EXTENSTION_TO_LANG:
            self.language = GitSrcFiles.EXTENSTION_TO_LANG[extension]
        else:
            self.language = extension

def crawl_git_repository(background_tasks: BackgroundTasks, url: str, extensions: list):
    try:
        crawler = GitCrawler()
        crawler.start_crawl(url, extensions)
        src_files = crawler.get_src_files()
        crawler.close()
        # for src in src_files:
        #     print(src.src)
        return src_files
    except Exception as e:
        print(e)

@router.get("/crawl")
async def perform_crawl(background_tasks: BackgroundTasks, url: str, extensions: List[str] = Query(...)):
    # 비동기 작업으로 크롤링 실행
    background_tasks.add_task(crawl_git_repository, background_tasks, url, extensions)
    return {"message": "Crawling started", "url": url, "extensions": extensions}