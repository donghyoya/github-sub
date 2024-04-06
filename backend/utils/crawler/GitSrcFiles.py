import re


class GitSrcFiles:
    GIT_TREE_PATTERNS = r'/blob/\w+/([a-zA-Z0-9\/-_]+)/'

    def __init__(self, url, title, src):
        self.url = url
        self.directory = re.findall(GitSrcFiles.GIT_TREE_PATTERNS, url)[0]
        self.title = title
        self.src = src

if __name__ == '__main__':
    url = 'https://github.com/js990311/spring-shortener/blob/develop/src/main/java/com/toyproject/shortener/dto/form/CreateUrlForm.java'
    src = GitSrcFiles(url, 'title', 'src')
    print(src.directory)
