from domain.frontend.view_model import VMSourceCode


def convert_to_vm(src_files):
    """
    GitCrawler 객체를 ViewModel로 변경
    Args:
        src_files (list) : git cralwer의 개체
    Returns:
        sources : 변경된 list(VMSourceCode)
    """
    sources = []
    for src in src_files:
        source = VMSourceCode()
        source.set_url(src.url)
        source.set_sourceName(src.title)
        source.set_path(src.directory)
        source.set_sourceCode(src.src)
        source.set_language(src.language)

        sources.append(source)

    return sources