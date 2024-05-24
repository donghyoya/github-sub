from domain.sourcecode.model import SourceCode


def conv2orm(src_files):
    sources = []

    for src in src_files:
        source = SourceCode()
        source.sourceName = src.title
        source.path = src.directory
        source.sourceCode = src.src

    return sources