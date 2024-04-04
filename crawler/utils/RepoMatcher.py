import re

class RepoMatcher:

    REPO_URL_PATTERN = r'https?://github.com/[a-zA-Z0-9]+/[a-zA-Z0-9_-]+'
    REPO_NAME_PATTERN = r'/[a-zA-Z0-9]+/[a-zA-Z0-9_-]+'

    def __init__(self, repoUrl):
        self.repoUrl = repoUrl

    def regex_match(self):
        if re.match(RepoMatcher.REPO_URL_PATTERN, self.repoUrl):
            return True
        else:
            return False

if __name__ == '__main__':
    repo = RepoMatcher('https://github.com/js990311/sync-tab-light')
    print(repo.regex_match())