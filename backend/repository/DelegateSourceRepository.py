
class DelegateSourceRepository:
    def __init__(self, statusRepository, dataRepository):
        self.delegateDataRepository = dataRepository
        self.delegateStatusRepository = statusRepository

    def saveStatusById(self, id:tuple, status:str):
        self.delegateStatusRepository.saveStatusById(id, status)

    def existStatusById(self, id: tuple):
        # status는 4개가 있다 (추후 enum화 할 것)
            # NONE      : 작업 내역이 없다.
            # WORKING   : 작업 중이다.
            # FAIL      : 작업이 실패하였다
            # DONE      : 작업이 완료되어 완성된 데이터가 있다
        status = None
        status = self.delegateStatusRepository.findStatusById(id)
        if status is not None:
            # redis에 등록된 작업내역이 있음
            return status
        else:
            # redis에 작업내역이 없어도 데이터베이스에 데이터가 있다면 반환
            if self.delegateDataRepository.existRepoById(id):
                return "DONE"
            else:
                return "NONE"

    def findRepoById(self, id:tuple):
        # existStatusById를 사용하여 데이터가 존재함을 미리 확인하고 가져올 것
        # TODO 추후 redis를 사용하여 data cache할 필요가 있음
        return self.delegateDataRepository.findRepoById(id)

    def saveRepoById(self, id, data):
        # status cache의 데이터도 자동으로 갱신함
        self.delegateDataRepository.saveRepoById(id, data)
        self.saveStatusById(id, "DONE")

