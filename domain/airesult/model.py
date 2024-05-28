from sqlalchemy import  Column, String, \
PrimaryKeyConstraint, BigInteger, Text, \
Integer, ForeignKey
from sqlalchemy.orm import relationship, \
    Mapped, mapped_column

from default.config.dbconfig import Base


class AiResult(Base):
    __tablename__ = "AiResult"
    aid = Column(BigInteger, primary_key=True, autoincrement=True)
    model = Column(String(100))
    answer = Column(Text)
    score = Column(Integer)
    rid = Column(BigInteger, ForeignKey('Repository.rid'))
    repository = relationship("Repository", back_populates="ai_results")

    def print(self):
        print(f"ID: {self.aid}, Model: {self.model}, Answer: {self.answer}, Score: {self.score}, Repository ID: {self.rid}")

        