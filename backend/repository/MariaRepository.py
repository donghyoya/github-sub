from repository.ABCSourceRepository import ABCSourceRepository

from sqlalchemy import create_engine, literal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from repository.Entity import SourceCode, GithubUser, Repository
from utils.crawler.GitSrcFiles import GitSrcFiles


class MariaRepository(ABCSourceRepository):
    _instance = None

    def __new__(cls, db_config):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init(db_config=db_config)
        return cls._instance


    def init(self, db_config:dict) -> None:
        self.engine = create_engine(
            'mariadb+mariadbconnector://{}:{}@{}:{}/{}'.format(
                db_config['user'],
                db_config['password'],
                db_config['host'],
                db_config['port'],
                db_config['database']
            )
        )

    def get_session(self):
        Session = sessionmaker(bind=self.engine, autocommit=False)
        session = Session()
        return session

    def existsRepoById(self, repoId: tuple) -> bool:
        with self.get_session() as session:
            q = session.query(SourceCode).filter(SourceCode.username == repoId[0], SourceCode.reponame == repoId[1])
            ret = session.query(literal(True)).filter(q.exists()).scalar()

        return ret

    def findRepoById(self, repoId: tuple):
        with self.get_session() as session:
            q = session.query(SourceCode).filter(SourceCode.username == repoId[0], SourceCode.reponame == repoId[1])
            sourceCodes = q.all()

        if sourceCodes is not None:
            ret = []
            for source in sourceCodes:
                ret.append(
                    GitSrcFiles(
                        url= source.url if source.url else '',
                        title=source.source_name if source.source_name else '',
                        src=source.source_code if source.source_code else '',
                        extension=source.language if source.language else ''
                    )
                )
            return ret



    def saveRepoById(self, repoId: tuple, sources):
        with self.get_session() as session:
            target = []
            username = repoId[0]
            reponame = repoId[1]

            # insert user. but why here?
            q = session.query(GithubUser).filter(GithubUser.username == username)
            if not session.query(literal(True)).filter(q.exists()).scalar():
                g = GithubUser(username=username)
                target.append(g)

            # insert repo. but why here?
            q = session.query(Repository).filter(
                Repository.reponame == reponame, Repository.username == username
            )
            if not session.query(literal(True)).filter(q.exists()).scalar():
                g = Repository(reponame=reponame, username=username)
                target.append(g)

            # insert source codes
            for src in sources:
                source = SourceCode(
                    username = username,
                    reponame = reponame,
                    path = src.directory,
                    language = src.language,
                    source_name = src.title,
                    source_code = src.src,
                    url = src.url
                )
                target.append(source)

            session.add_all(target)

            session.commit()

if __name__== "__main__":
    db_config = {
        'user' : 'admin',
        'password' : 'admin',
        'host' : 'localhost',
        'port' : '3306',
        'database' : 'github_sub'
    }

    repo1 = MariaRepository(db_config)
    repo2 = MariaRepository(db_config)
    print(repo1 is repo2)
    print(id(repo1) == id(repo2))

    target = [
        GitSrcFiles(
            url = "/blob/main/README.java",
            title = "test",
            src="asdfasdf",
            extension="java"
        ),
        GitSrcFiles(
            url="/blob/main/README.java",
            title="test",
            src="asdfasdf",
            extension="java"
        ),
        GitSrcFiles(
            url="/blob/main/README.java",
            title="test",
            src="asdfasdf",
            extension="java"
        ),
        GitSrcFiles(
            url="/blob/main/README.java",
            title="test",
            src="asdfasdf",
            extension="java"
        ),
    ]

    username = "test_user2"
    reponame = "test_repo2"

    # username, reponame
    print(repo1.existsRepoById((username,reponame)))
    repo1.saveRepoById((username,reponame), target)
    sources = repo1.findRepoById((username,reponame))

    for src in sources:
        print(
            src.url, src.directory, src.title, src.src, src.language
        )
