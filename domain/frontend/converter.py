from domain.frontend.view_model import VMSourceCode, VMRepository
from domain.repository.model import Repository
from domain.sourcecode.model import SourceCode

# Use for gitCrawler

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

# Use for frontend/service

def convert_repository_to_vm(repository: Repository) -> VMRepository:
    """
        orm model Repository를 dto(View Model)로 변환
    """
    vm_repo = VMRepository()
    vm_repo.set_username(repository.github_user.username)

    (vm_repo
        .set_repoid(repository.rid)
        .set_reponame(repository.repoName)
    )
    source_codes = []
    for source in repository.source_codes:
        source_codes.append(convert_source_code_to_vm(source))
    vm_repo.set_sources(source_codes)
    return vm_repo

def convert_source_code_to_vm(source_code: SourceCode) -> VMSourceCode:
    """
        orm model (SourceCode)를 dto(View Model)로 변환
    """
    return (VMSourceCode()
            .set_sourceName(source_code.sourceName)
            .set_sourceCode(source_code.sourceCode)
            .set_url(source_code.url)
            .set_language(source_code.language)
            .set_path(source_code.path)
        )
