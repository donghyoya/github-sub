from dotenv import load_dotenv
import os
from selenium import webdriver

load_dotenv(".env")

SELENIUM_HUB_URL = os.getenv("SELENIUM_HUB_URL")

def get_crawling_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.set_capability('browserName', 'chrome')

    # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver = webdriver.Remote(command_executor=SELENIUM_HUB_URL, options=options)
        driver.implicitly_wait(10) # seconds
        return driver
    except Exception as e:
        print(SELENIUM_HUB_URL,e)



