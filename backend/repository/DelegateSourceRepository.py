
class DelegateSourceRepository:
    def __init__(self, statusRepository, sourceRepository):
        self.delegateSourceRepository = sourceRepository
        self.delegateStatusRepository = statusRepository

    def saveStatusById(self, repoId:tuple, status:str):
        self.delegateStatusRepository.saveStatusById(repoId, status)

    def existsRepoById(self, repoId: tuple):
        # status는 4개가 있다 (추후 enum화 할 것)
            # NONE      : 작업 내역이 없다.
            # WORKING   : 작업 중이다.
            # FAIL      : 작업이 실패하였다
            # DONE      : 작업이 완료되어 완성된 데이터가 있다
        status = self.delegateStatusRepository.findStatusById(repoId)
        if status is not None:
            # redis에 등록된 작업내역이 있음
            return status
        else:
            # redis에 작업내역이 없어도 데이터베이스에 데이터가 있다면 반환
            if self.delegateSourceRepository.existsRepoById(repoId):
                return "DONE"
            else:
                return "NONE"

    def findRepoById(self, repoId:tuple):
        # existStatusById를 사용하여 데이터가 존재함을 미리 확인하고 가져올 것
        # TODO 추후 redis를 사용하여 data cache할 필요가 있음
        return self.delegateSourceRepository.findRepoById(repoId)

    def saveRepoById(self, repoId: tuple, sources):
        # status cache의 데이터도 자동으로 갱신함
        self.delegateSourceRepository.saveRepoById(repoId, sources)
        self.saveStatusById(repoId, "DONE")

