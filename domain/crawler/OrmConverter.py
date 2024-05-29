from domain.sourcecode.model import SourceCode
from typing import List

def conv2orm(src_files) -> List[SourceCode]:
    sources = []

    for src in src_files:
        source = SourceCode()
        source.sourceName = src.title
        source.path = src.directory
        source.url = src.url
        source.sourceCode = src.src
        source.language = src.language

        sources.append(source)

    return sources