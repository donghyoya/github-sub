import re


class GitSrcFiles:
    GIT_TREE_PATTERNS = r'/blob/\w+/([a-zA-Z0-9\/-_]+)/'
    EXTENSTION_TO_LANG = {
        'java' : 'java',
        'js' : 'javascript',
        'py' : 'python',
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


if __name__ == '__main__':
    url = '/* input your test url in here */'
    src = GitSrcFiles(url, 'title', 'src')
    print(src.directory)
