from sqlalchemy import  Column, String, \
PrimaryKeyConstraint, BigInteger, Text, \
Integer, ForeignKey
from sqlalchemy.orm import relationship

from default.config.dbconfig import Base


class Repository(Base):
    __tablename__ = 'Repository'
    rid = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    language = Column(String(10))
    connectCnt = Column(Integer)
    repoName = Column(String(25))
    guid = Column(BigInteger, ForeignKey('GithubUser.uid'))
    github_user = relationship("GithubUser", back_populates="repositories")