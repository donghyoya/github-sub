from default.config.crawlerconfig import get_crawling_driver
from domain.crawler.crawler import GitCrawler


def git_crawling(url: str, result_converter):
    """
    결과물을 크롤링하는 장치

    Args:
        url (str) : crawling 타겟에 대한 url
        result_converter (function) : crawling 결과물을 필요한 자료구조로 변경하는 함수

    Returns:
        result_converter에 의해서 변경된 클래스
    """

    try:
        # crawling logic
        driver = get_crawling_driver()
        crawler = GitCrawler(driver)
        crawler.start_crawl(url)
        src_files = crawler.get_src_files()
        crawler.close()

        # 결과물을 원하는 객체로 convert해서 보내줌
        ret = result_converter(src_files)
        return ret

    except Exception as e:
        print("exception", e)
        raise e

