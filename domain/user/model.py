from sqlalchemy import  Column, String, \
PrimaryKeyConstraint, BigInteger, Text, \
Integer

from default.config.dbconfig import Base

class GithubUser(Base):
    __tablename__ = 'GithubUser'
    uid = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    username = Column(String(255))
    site = Column(String(255))
    ConnectCnt = Column(Integer)
    follower = Column(Integer)
    following = Column(Integer)