from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, configure_mappers

# 모델 정의를 가져옵니다.
from default.config.dbconfig import Base
from domain.airesult import model
from domain.repository import model
from domain.user import model
from domain.sourcecode import model

# .env 파일에서 데이터베이스 URL을 로드하기 위한 준비
from dotenv import load_dotenv
import os

# 환경 변수 로딩
load_dotenv(".env")

# 데이터베이스 연결 URL을 환경 변수에서 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

# 데이터베이스 엔진 생성
engine = create_engine(DATABASE_URL)

configure_mappers()

# 데이터베이스 세션 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

print("모든 테이블이 데이터베이스에 생성되었습니다.")
