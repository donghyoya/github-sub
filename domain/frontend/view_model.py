class VMRepository:
    def __init__(self):
        self.username = None
        self.reponame = None
        self.ai_answer = None
        self.ai_score = None
        self.sources = None

    def set_username(self, username):
        self.username = username
        return self

    def set_reponame(self, reponame):
        self.reponame = reponame
        return self

    def set_ai_answer(self, ai_answer):
        self.ai_answer = ai_answer
        return self

    def set_ai_score(self, ai_score):
        self.ai_answer = ai_score
        return self

    def set_sources(self, sources):
        self.sources = sources
        return self

class VMSourceCode:
    def __init__(self):
        self.url = None
        self.sourceName = None
        self.path = None
        self.sourceCode = None
        self.language = None

    def set_url(self, url):
        self.url = url
        return self

    def set_sourceName(self, sourceName):
        self.sourceName = sourceName
        return self

    def set_path(self, path):
        self.path = path
        return self

    def set_language(self, language):
        self.language = language
        return self

    def set_sourceCode(self, sourceCode):
        self.sourcecode = sourceCode
        return self