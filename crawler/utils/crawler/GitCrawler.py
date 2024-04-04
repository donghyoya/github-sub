from queue import Queue

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from crawler.utils.crawler.GitSrcFiles import GitSrcFiles

class GitCrawler:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument('--disable-blink-features=AutomationControlled')


        self.driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)


    def startCrawl(self, rootUrl):
        self.dirSet = set()
        self.srcFileUrls = []
        self.queue = Queue()

        self.queue.put(rootUrl)

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

            if "/tree" in href:
                self.queue.put(href)
            if ".java" in href:
                self.srcFileUrls.append(href)

    def getSrcFiles(self):
        self.srcFiles = []
        for url in self.srcFileUrls:
            srcFile = self.getSrcFile(url)
            self.srcFiles.append(srcFile)

        return self.srcFiles

    def getSrcFile(self, url):
        self.driver.get(url)
        textarea = self.wait.until(
            expected_conditions.presence_of_element_located((By.ID, 'read-only-cursor-text-area'))
        )
        src = textarea.text
        srcName = url.split("/")[-1]
        return GitSrcFiles(
            url, srcName, src
        )


if __name__ == "__main__":
    crawler = GitCrawler()
    crawler.startCrawl("/* input your test code in hear */")
    srcFiles = crawler.getSrcFiles()

    for i in srcFiles:
        print("================================")
        print(i.url)
        print(i.title)
        print(i.src)
        print("================================")