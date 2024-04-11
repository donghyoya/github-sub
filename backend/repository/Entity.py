from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, PrimaryKeyConstraint, literal
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class GithubUser(Base):
    __tablename__ = "github_users"

    username = Column(String, primary_key=True)

class Repository(Base):
    __tablename__ = "repositories"
    __table_args__ = (PrimaryKeyConstraint('username', 'reponame', name = 'username_pkey'),)

    reponame = mapped_column(String, nullable=False)
    username = mapped_column(String, ForeignKey("github_users.username"), nullable=False)

class SourceCode(Base):
    __tablename__ = "source_codes"
    __table_args__ = (PrimaryKeyConstraint('source_id','username', 'reponame', name = 'username_pkey'),)

    source_id = mapped_column(Integer, autoincrement=True)
    reponame = mapped_column(String, ForeignKey('repositories.reponame'), nullable=False)
    username = mapped_column(String, ForeignKey('repositories.username'),nullable=False)
    path = mapped_column(String, nullable=False)
    source_name = mapped_column(String, nullable=False)
    source_code = mapped_column(Text, nullable=False)
    url = mapped_column(String, nullable=False)
    language = mapped_column(String, nullable=False)

if __name__ == '__main__':
    engine = create_engine('mariadb+mariadbconnector://admin:admin@localhost:3306/github_sub')
    Session = sessionmaker(bind=engine, autocommit=False)
    session = Session()

    username = "test_user"
    reponame = "test_repo"
    source = {
        "username": username,
        "reponame": reponame,
        "path" : "test_path",
        "sourceCode": "test_sourceCode",
        "sourceName": "test_sourceName",
        "url" : "test_url",
        "language": "java"
    }

    gq = session.query(GithubUser).filter(GithubUser.username == username)
    dq = session.query(Repository).filter(Repository.username == username)
    sq = session.query(SourceCode).filter(SourceCode.username == username, SourceCode.reponame == reponame)
    if not session.query(literal(True)).filter(gq.exists()).scalar():
        g = GithubUser(username=username)
        session.add(g)
    if not session.query(literal(True)).filter(dq.exists()).scalar():
        r = Repository(username=username, reponame=reponame)
        session.add(r)
    if not session.query(literal(True)).filter(sq.exists()).scalar():
        s = SourceCode(
            username = username,
            reponame = reponame,
            path = source["path"],
            source_code = source["sourceCode"],
            source_name = source["sourceName"],
            language = source["language"],
            url = source["url"]
        )
        session.add(s)
    session.commit()

    ret = session.query(SourceCode).filter_by(
        username=username,
        reponame=reponame
    ).all()

    for src in ret:
        print(
            src.username,
            src.reponame,
            src.path,
            src.source_name,
            src.source_code,
            src.url,
            src.language
        )
