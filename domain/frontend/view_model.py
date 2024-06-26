from domain.repository.model import Repository


class VMRepository:
    def __init__(self):
        self.repoid = None
        self.username = None
        self.reponame = None
        self.ai_answer = None
        self.ai_score = None
        self.sources = None

    def set_repoid(self, repoid):
        self.repoid = repoid
        return self

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
        self.ai_score = ai_score
        return self

    def set_sources(self, sources):
        self.sources = sources
        return self

    def to_dict(self):
        data = self.__dict__
        sources = []
        if self.sources is not None:
            for source in self.sources:
                sources.append(source.to_dict())
            data['sources'] = sources
        return data

    def from_dict(self, data:dict):
        self.username = data['username']
        self.reponame = data['reponame']
        self.ai_answer = data['ai_answer']
        self.ai_score = data['ai_score']
        self.sources = []
        for src_data in data['sources']:
            self.sources.append(
                VMSourceCode().from_dict(src_data)
            )
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
        self.sourceCode = sourceCode
        return self

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data:dict):
        self.url = data['url']
        self.sourceName = data['sourceName']
        self.path = data['path']
        self.sourceCode = data['sourceCode']
        self.language = data['language']
        return self
