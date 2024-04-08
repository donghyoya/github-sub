import re

class RepoMatcher:

    REPO_URL_PATTERN = r'https?://github.com/[a-zA-Z0-9]+/[a-zA-Z0-9_-]+'
    REPO_NAME_PATTERN = r'github.com/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)'

    def regex_match(self, repo_url):
        if re.match(RepoMatcher.REPO_URL_PATTERN, repo_url):
            return True
        else:
            return False
    def get_repo_name(self, repo_url):
        result = re.findall(RepoMatcher.REPO_NAME_PATTERN, repo_url)
        return result[0]

if __name__ == '__main__':
    url = '/* input your test url in here */'
    repo = RepoMatcher()
    if repo.regex_match(url):
        print(repo.get_repo_name(url))
