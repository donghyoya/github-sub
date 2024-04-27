const resultRepo = document.getElementById('result-repo');
const resultCode = document.getElementById('result-code');
const resultAi = document.getElementById('result-ai');


/* start form event */
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

    /**
     * 크롤링 요청은 편의상 form 객체에서 진행함
     */
    fetch('/ui/mock/crawl',{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body:jsonData
    }).then(resp=>resp.json())
    .then(data=>{
        /**
         * form 요청의 결과물로 상태정보를 가져옴
         * 상태정보에 맞게 적절한 조치를 취함
         */
        console.log('응답', data);
        let state = checkWorkState(data['status']);
        if(state === 100){
            /**
             * 크롤링 진행 중 -> polling으로 상태정보를 갱신
             */
            pollingStatus(data['username'], data['reponame']); // 상태 갱신
        }else if(state === 110){
            /**
             * 크롤링 완료 + ai 진행 안되어있음
             * ai request하고
             * 크롤링 완료처리를 함
             */
            requestAi(data['username'], data['reponame']);// ai request
            getSourceCode(data['username'], data['reponame']); // 크롤링 완료 처리
            pollingStatus(data['username'], data['reponame']); // 상태 갱신
        }else if(state === 200){
            /**
             * AI 작업 중
             * = 작업 순서상 크롤링은 완료되었음 => 크롤링 코드 받아오기
             * = AI request도 이미 완료되었음 => AI request는 안해도 되고 status만 갱신
             */
            getSourceCode(data['username'], data['reponame']); // 크롤링 데이터 받아오기
            pollingStatus(data['username'], data['reponame']); // 상태 갱신
        }else if(state === 210){
            /**
             * AI작업까지 완료
             * = 크롤링 데이터 가져오기
             * = AI 데이터 가져오기
             */
            getSourceCode(data['username'], data['reponame']); // 크롤링 데이터 받아오기
            getAiResult(data['username'], data['reponame']); // ai 데이터 가져오기
        }else if(state === -1){
            // 잘못된 api 요청
            document.getElementById("form-info").innerText = "실패했습니다. 링크를 확인해주십시오";
            console.log("fail");
        }
    }).catch(error=>{
        console.log('오류', error);
    })
});
/* end of form event */

const clearResult = () => {
    /**
     * form 리퀘스트가 날라가면 result tag에 있는 내용물 제거한다
     */
    resultRepo.innerHTML = '';
    resultCode.innerHTML = '';
    resultAi.innerHTML = '';
}

/* start polling status */
const pollingStatus = (username, reponame) => {
    /**
     * 서버로부터 작업의 상태정보를 가져오고 해당 상태에 걸맞는 적절한 메서드를 호출한다
     *
     */
    const repo = `${username}/${reponame}`
    const pollingEndpoint = `/ui/mock/polling/${repo}`;

    /* start of pollingStatus */
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
            } else if(state === 110){
                /**
                 * 크롤링 완료 + ai 진행 안되어있음
                 * ai request하고
                 * 크롤링 완료처리를 함
                 */
                requestAi(username, reponame)// ai request하기
                getSourceCode(username, reponame); // 크롤링 데이터 받아오기
            } else if(state == 210){
                /**
                 * ai 완료
                 * 프로그램의 로직상 크롤링 데이터는 이미 받아져있음
                 */
                getAiResult(username, reponame);
                clearPolling();
            }
        });
    }
    /* end of pollingStatus */

    // start interval
    const interval = setInterval(()=>{
        pollingFetch();
    },10*1000);

    // stop interval
    const clearPolling = () => {
        clearInterval(interval);
    };
}
/* end polling status */


/* insert template fragment */
const getSourceCode = (username, reponame) => {
    const repository = `${username}/${reponame}`;
    fetch(`/ui/frag/${repository}/source`,{
        method: 'GET'
    }).then(resp=>resp.text())
    .then(data=>{
        resultCode.innerHTML = data;
        hljs.highlightAll();
    })
}

const getRepoHeader = (username, reponame) => {
    const repository = `${username}/${reponame}`;
    fetch(`/ui/frag/${repository}/repository`,{
        method: 'GET'
    }).then(resp=>resp.text())
    .then(data=>{
        resultRepo.innerHTML = data;
    })
}

const getAiResult = (username, reponame) => {
    const repository = `${username}/${reponame}`;
    fetch(`/ui/frag/${repository}/ai`,{
        method: 'GET'
    }).then(resp=>resp.text())
    .then(data=>{
        resultAi.innerHTML = data;
    })
}

/* request ai */

const requestAi = (username, reponame) => {
    const endpoint = `/ui/mock/${username}/${reponame}/ai`;

    fetch(endpoint, {
       method: 'GET'
    }).then(resp => resp.json())
        .then(data=>{
            console.log('request ai', data);
        });
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

