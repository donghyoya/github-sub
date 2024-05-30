import re

# utils
REPO_URL_PATTERN = r'https?://github.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+'
REPO_NAME_PATTERN = r'github.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)'

def url_checker(url: str):
    """
    url이 github url인가 체크
    """
    if re.match(REPO_URL_PATTERN, url):
        print("return value" ,re.findall(REPO_NAME_PATTERN, url)[0])
        return re.findall(REPO_NAME_PATTERN, url)[0]
    else:
        return None