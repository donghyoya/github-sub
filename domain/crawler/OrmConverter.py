from domain.frontend.view_model import VMSourceCode

from default.config import dbconfig

from domain.sourcecode.model import SourceCode
from domain.sourcecode import service as SourceCodeService



def get_db():
    try:
        db = dbconfig.SessionLocal()
        yield db
    finally:
        db.close()

def conv2orm(src_files):
    sources = []

    for src in src_files:
        source = SourceCode()
        source.sourceName = src.title
        source.path = src.directory
        source.sourceCode = src.src

        SourceCodeService.create_source_code(get_db(),source)