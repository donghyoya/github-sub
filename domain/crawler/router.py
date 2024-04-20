from fastapi import APIRouter, BackgroundTasks
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

router = APIRouter(tags=["crawler"])

class GitCrawler:
    SOURCE_EXTENSION_PATTERN = r"\.([a-zA-Z0-9]+)$"

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def start_crawl(self, root_url, extension_option):
        self.dir_set = set()
        self.src_file_urls = []
        self.queue = []

        self.queue.append(root_url)
        self.extension_option = set(extension_option)

        while self.queue:
            url = self.queue.pop(0)
            self.search_tree_dir(url)

    def search_tree_dir(self, url):
        self.driver.get(url)
        atags = self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
        self.find_next_urls(atags)

    def find_next_urls(self, atags):
        for atag in atags:
            href = atag.get_attribute("href")
            if href and href not in self.dir_set:
                self.dir_set.add(href)
                src_extension = re.findall(self.SOURCE_EXTENSION_PATTERN, href)
                if src_extension and src_extension[0] in self.extension_option:
                    self.src_file_urls.append((href, src_extension[0]))
                elif "/tree" in href:
                    self.queue.append(href)

    def close(self):
        self.driver.quit()

    def get_src_files(self):
        src_files = []
        for url, extension in self.src_file_urls:
            self.driver.get(url)
            src = self.driver.page_source
            title = url.split("/")[-1]
            src_files.append(GitSrcFiles(url, title, src, extension))
        return src_files

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
    crawler = GitCrawler()
    crawler.start_crawl(url, extensions)
    src_files = crawler.get_src_files()
    crawler.close()
    return src_files

@router.get("/crawl/")
async def perform_crawl(background_tasks: BackgroundTasks, url: str, extensions: list = ["py"]):
    # 비동기 작업으로 크롤링 실행
    background_tasks.add_task(crawl_git_repository, background_tasks, url, extensions)
    return {"message": "Crawling started", "url": url, "extensions": extensions}
