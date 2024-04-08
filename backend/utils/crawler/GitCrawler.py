import re
from queue import Queue

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from .GitSrcFiles import GitSrcFiles
class GitCrawler:
    SOURCE_EXTENSION_PATTERN = r"\.([a-zA-Z0-9]+)$"
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument('--disable-blink-features=AutomationControlled')


        self.driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)


    def startCrawl(self, rootUrl, extensionOption):
        self.dirSet = set()
        self.srcFileUrls = []
        self.queue = Queue()

        self.queue.put(rootUrl)

        self.extensionOption = set(extensionOption)

        while not self.queue.empty():
            url = self.queue.get()
            self.searchTreeDir(url)


    # queue에다가 다 넣고 반환
    def searchTreeDir(self, url):
        self.driver.get(url)
        atags = self.wait.until(
            expected_conditions.presence_of_element_located((By.TAG_NAME, "table"))
        ).find_elements(By.TAG_NAME, "a")
        self.findNextUrls(atags)


    def findNextUrls(self, atags):
        for atag in atags:
            href = atag.get_attribute("href")
            if href is None:
                continue
            if href in self.dirSet:
                continue
            self.dirSet.add(href)

            srcExtension = re.findall(GitCrawler.SOURCE_EXTENSION_PATTERN, href)
            if len(srcExtension) == 1:
                if srcExtension[0] in self.extensionOption:
                    self.srcFileUrls.append((href, srcExtension[0]))
            if "/tree" in href:
                self.queue.put(href)

    def getSrcFiles(self):
        self.srcFiles = []
        for url,extension in self.srcFileUrls:
            srcFile = self.getSrcFile(url, extension)
            self.srcFiles.append(srcFile)

        return self.srcFiles

    def getSrcFile(self, url, extension):
        self.driver.get(url)
        textarea = self.wait.until(
            expected_conditions.presence_of_element_located((By.ID, 'read-only-cursor-text-area'))
        )
        src = textarea.text
        srcName = url.split("/")[-1]
        return GitSrcFiles(
            url, srcName, src, extension
        )


if __name__ == "__main__":
    crawler = GitCrawler()
    url = "/* input your test url in here */"
    extensionOption = [
        "java"
    ]
    crawler.startCrawl(url, extensionOption)
    srcFiles = crawler.getSrcFiles()

    for i in srcFiles:
        print("================================")
        print(i.url)
        print(i.title)
        print(i.src)
        print(i.language)
        print("================================")