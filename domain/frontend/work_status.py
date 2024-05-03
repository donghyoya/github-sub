from enum import Enum

class WorkStatus(Enum):
    NONE = "NONE"
    CRAWLING_NOW = "CRAWLING_NOW"
    CRAWLING_SUCCESS = "CRAWLING_SUCCESS"
    CRAWLING_FAIL = "CRAWLING_FAIL"
    AI_API_NOW = "AI_API_NOW"
    AI_API_SUCCESS = "AI_API_SUCCESS"
    AI_API_FAIL = "AI_API_FAIL"

    def needCrawling(self):
        """
            status를 체크해서
        """
        return self in [WorkStatus.NONE, WorkStatus.CRAWLING_FAIL]

    def needAiApi(self):
        return self in [WorkStatus.AI_API_FAIL, WorkStatus.CRAWLING_SUCCESS]

    @classmethod
    def from_string(cls, string):
        for status in cls:
            if status.value == string.upper():
                return status
        raise WorkStatus.NONE


if __name__ == "__main__":
    status = WorkStatus.NONE
    if status.needCrawling():
        print("NONE need Crawling", status.value)

    status = WorkStatus.CRAWLING_FAIL
    if status.needCrawling():
        print("CRAWLING FAIL need Crawling", status.value)

    status = WorkStatus.CRAWLING_SUCCESS
    if status.needAiApi():
        print("CRAWLING SUCCESS need AI API", status.value)

    status = WorkStatus.AI_API_FAIL
    if status.needAiApi():
        print("AI_API_FAIL need AI API", status.value)

    status_str = "CRAWLING_SUCCESS"
    print(WorkStatus.from_string(status_str))