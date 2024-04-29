from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import re

class GitCrawler:
    SOURCE_EXTENSION_PATTERN = r"\.([a-zA-Z0-9]+)$"

    def __init__(self, driver):
        self.driver = driver

    def start_crawl(self, root_url):
        self.dir_set = set()
        self.src_file_urls = []
        self.queue = []

        self.queue.append(root_url)
        self.extension_option = set(GitSrcFiles.EXTENSTION_TO_LANG.values())

        while self.queue:
            # print("self queue: ", self.queue)
            url = self.queue.pop(0)
            self.search_tree_dir(url)

    def search_tree_dir(self, url):
        # print('search_tree_dir')
        self.driver.get(url)
        atags = self.driver.find_element(By.TAG_NAME, "table").find_elements(By.TAG_NAME,"a")
        # atags = EC.presence_of_element_located((By.TAG_NAME, "table")).find_elements(By.TAG_NAME, "a")
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
        textarea = self.driver.find_element(By.ID, 'read-only-cursor-text-area')
        # textarea = EC.presence_of_element_located((By.ID, 'read-only-cursor-text-area'))
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
        'cs':'cs', # highlight js에서 cs라고 지정
        'c':'c',
        'cpp':'c++',
        'go':'golang',
        'jsx':'jsx',
        'kt':'kotlin',
        'php' : 'php',
        'sql':'sql',
        'ts':'typescript'
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
