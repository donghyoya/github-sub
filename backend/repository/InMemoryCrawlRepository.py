class InMemoryCrawlRepository:
    def __init__(self):
        self.result = {}

    def existRepoId(self, id):
        if id in self.result:
            return True
        else:
            return False

    def findRepoById(self, id):
        if id in self.result:
            return self.result[id]
        else:
            return None

    def saveRepoById(self, id, repo):
        if id in self.result:
            return False
        else:
            self.result[id] = repo
            return True