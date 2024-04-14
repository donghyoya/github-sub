from sqlalchemy import  Column, String, \
PrimaryKeyConstraint, BigInteger, Text, \
Integer, ForeignKey
from sqlalchemy.orm import relationship

from default.config.dbconfig import Base

class SourceCode(Base):
    __tablename__ = 'SourceCode'
    sid = Column(BigInteger, primary_key=True,unique=True, autoincrement=True)
    sourceName = Column(String(25))
    sourceCode = Column(Text)
    path = Column(String(100))
    rid = Column(BigInteger, ForeignKey('Repository.rid'))
    repository = relationship("Repository", back_populates="source_codes")