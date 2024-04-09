from abc import ABC, abstractmethod

class ABCSourceRepository(ABC):
    """
    Abstract class for sources(in git repositories) repository
    git repository 크롤링 결과를 저장하는 추상 리포지토리 객체
    """
    @abstractmethod
    def existsRepoById(self, repoId: tuple) -> bool:
        """
        repository에 데이터가 존재하는 지 반환하는 메서드
        :param repoId: repository아이디. tuple 형식이며 repoId[0]=username, repoId[1]=reponame
        :return: true면 데이터베이스에 해당 repository가 있음
        """
        pass

    @abstractmethod
    def findRepoById(self, repoId: tuple):
        """
        데이터베이스에서 source 있는대로 다 가지고 오는 메서드
        :param repoId: repository아이디. tuple 형식이며 repoId[0]=username, repoId[1]=reponame
        :return: 데이터베이스에서 가져온 repository의 모든 sources
        """
        pass

    @abstractmethod
    def saveRepoById(self, repoId: tuple, sources):
        """
        crawling한 source 데이터를 저장하는 객체
        :param repoId: repository아이디. tuple 형식이며 repoId[0]=username, repoId[1]=reponame
        :param sources: 저장할 repository의 sources 객체
        :return:
        """
        pass