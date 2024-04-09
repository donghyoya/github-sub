class DictionaryStatusRepository:
    def __init__(self):
        self.conn = {}

    def findStatusById(self, id: tuple):
        if id in self.conn:
            return self.conn[id]
        else:
            return None

    def saveStatusById(self, id: tuple, status: str):
        self.conn[id] = status