from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from functools import singledispatch

Base = declarative_base()

class A(Base):
    __tablename__ = 'table_a'
    id = Column(Integer, primary_key=True)
    value = Column(Integer)
    
    def getOne(self):
        return self.value

class B(Base):
    __tablename__ = 'table_b'
    id = Column(Integer, primary_key=True)
    value = Column(Integer)
    
    def getThree(self):
        return self.value

# 데이터베이스 엔진 설정 (SQLite 사용)
engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

# 세션 생성
Session = sessionmaker(bind=engine)
session = Session()

# 데이터 추가를 위한 함수 오버로딩
@singledispatch
def add_to_database(entity, session):
    raise NotImplementedError("Unsupported type")

@add_to_database.register(A)
def _(entity: A, session):
    session.add(entity)
    session.commit()
    print(f"Added A with value {entity.getOne()}")

@add_to_database.register(B)
def _(entity: B, session):
    session.add(entity)
    session.commit()
    print(f"Added B with value {entity.getThree()}")

# 테스트 데이터 추가
a_instance = A(value=1)
b_instance = B(value=3)

add_to_database(a_instance, session)
add_to_database(b_instance, session)
