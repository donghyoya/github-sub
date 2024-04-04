from django.http import HttpResponseNotAllowed
from django.shortcuts import render

from .utils.crawler.GitCrawler import GitCrawler
from .utils.RepoMatcher import RepoMatcher

# Create your views here.
def index(request):
    return render(request, "crawls/inputRepoForm.html");

def queryRepository(request):
    if request.method == "POST":
        repoUrl = request.POST.get('repo-url')
        repoMatcer = RepoMatcher(repoUrl)

        if repoMatcer.regex_match():
            print("it is git")
            crawler = GitCrawler()
            crawler.startCrawl(repoUrl)
            srcFiles = crawler.getSrcFiles()
            context = {
                "sources" : srcFiles
            }
            return render(request, "crawls/result.html", context)
        else:
            print("it is not git")
        return render(request, 'crawls/inputRepoForm.html')
    else:
        return HttpResponseNotAllowed(['POST'])
