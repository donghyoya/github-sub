from repository.ABCSourceRepository import ABCSourceRepository

class DictionaryCrawlRepository(ABCSourceRepository):
    def __init__(self):
        self.result = {}

    def existsRepoById(self, repoId: tuple):
        if repoId in self.result:
            return True
        else:
            return False

    def findRepoById(self, repoId: tuple):
        if repoId in self.result:
            return self.result[repoId]
        else:
            return None

    def saveRepoById(self, repoId: tuple, sources):
        if repoId in self.result:
            return False
        else:
            self.result[repoId] = sources
            return True