from sqlalchemy import  Column, String, \
PrimaryKeyConstraint, BigInteger, Text, \
Integer, ForeignKey
from sqlalchemy.orm import relationship

from default.config.dbconfig import Base


class AiResult(Base):
    __tablename__ = "AiResult"
    aid = Column(BigInteger, primary_key=True)
    model = Column(String(10))
    answer = Column(Text)
    score = Column(Integer)
    rid = Column(BigInteger, ForeignKey('Repository.rid'))
    repository = relationship("Repository", back_populates="ai_results")