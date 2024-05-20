from sqlalchemy import  Column, String, \
PrimaryKeyConstraint, BigInteger, Text, \
Integer
from sqlalchemy.orm import relationship

from default.config.dbconfig import Base

class GithubUser(Base):
    __tablename__ = "GithubUser"
    uid = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    username = Column(String(255))
    site = Column(String(255))
    connectCnt = Column(Integer)
    follower = Column(Integer)
    following = Column(Integer)
    repositories = relationship("Repository", back_populates="github_user")
