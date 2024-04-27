const resultRepo = document.getElementById('result-repo');
const resultCode = document.getElementById('result-code');
const resultAi = document.getElementById('result-ai');

document.getElementById("repo-form").addEventListener("submit", (event) =>{
  event.preventDefault();
    clearResult();
  const form = document.getElementById("repo-form");

  const formData = new FormData(form);
  const formJsonData = {};
  formData.forEach((value,key) => {
      formJsonData[key] = value;
  });

  const jsonData = JSON.stringify(formJsonData);

  fetch('/ui/mock/crawl',{
      method: 'POST',
      headers:{
          'Content-Type': 'application/json'
      },
      body:jsonData
  }).then(resp=>resp.json())
  .then(data=>{
      console.log('응답', data);
      let state = checkWorkState(data['status']);
      if(state === 100){
          // 작업 중
          pollingCrawl(data['username'], data['reponame']);
      }else if(state === 110){
          // 크롤링은 완료됨 -> AI api를 요청
          successCrawl(data['username'], data['reponame']);
      }else if(state === 200){
          // AI 작업 중 (크롤링은 완료됨)
          pollingAi(data['username'], data['reponame']);
      }else if(state === 210){
          // AI작업까지 완료
          successAi(data['username'], data['reponame']);
      }else if(state === -1){
          // 잘못된 api 요청
          document.getElementById("form-info").innerText = "실패했습니다. 링크를 확인해주십시오";
          console.log("fail");
      }

  }).catch(error=>{
      console.log('오류', error);
  })
}); /* end of form event */

const clearResult = () => {
    resultRepo.innerHTML = '';
    resultCode.innerHTML = '';
    resultAi.innerHTML = '';
}

/* crawling request */

const pollingCrawl = (username, reponame) => {
    const repo = `${username}/${reponame}`
    const pollingEndpoint = `/ui/mock/polling/${repo}`;

    const pollingFetch = () => {
        fetch(pollingEndpoint, {
            method: 'GET',
            headers : {
                'Content-Type' : 'application/json',
            }
        }).then(resp=>resp.json())
        .then(data =>{
            state = checkWorkState(data['status'])
            if(state === -1){
                clearPolling();
            }
            if(state === 110){
                clearPolling();
                successCrawl(username, reponame);
            }
        });
    }

    const interval = setInterval(()=>{
        pollingFetch();
    },10*1000);

    const clearPolling = () => {
        clearInterval(interval);
    };
}

const successCrawl = (username, reponame) => {
    const repo = `${username}/${reponame}`
    getSourceCode(repo);
}

/* ai request */

const pollingAi = (username, reponame) => {
    console.log('polling ai');
}

const successAi = (username, reponame) => {
    console.log('success ai');
}


/* utils */
const checkWorkState = (status) => {
    console.log(status);
    if(status === 'WORKING'){
        // crawling 작업 중
        return 100;
    }else if(status === 'CRAWLING_COMPLETE'){
        // 크롤링 완료
        return 110;
    }else if(status === 'AI_WORKING'){
        // AI 작업 중
        return 200;
    }else if(status === 'AI_COMPLETE'){
        // AI 작업 완료
        return 210;
    }else{
        // 실패
        return -1;
    }
}

/* template fragment */

const getSourceCode = (repository) => {
    fetch(`/ui/frag/${repository}/source`,{
        method: 'GET'
    }).then(resp=>resp.text())
    .then(data=>{
        resultCode.innerHTML = data;
        hljs.highlightAll();
    })
}

const getRepoHeader = (repository) => {
    fetch(`/ui/frag/${repository}/repository`,{
        method: 'GET'
    }).then(resp=>resp.text())
    .then(data=>{
        resultRepo.innerHTML = data;
    })
}

const getAiResult = (repository) => {
    fetch(`/ui/frag/${repository}/ai`,{
        method: 'GET'
    }).then(resp=>resp.text())
    .then(data=>{
        resultAi.innerHTML = data;
    })
}
