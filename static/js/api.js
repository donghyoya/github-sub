const resultRepo = document.getElementById('result-repo');
const resultCode = document.getElementById('result-code');
const resultAi = document.getElementById('result-ai');


/* start form event */
document.getElementById("repo-form").addEventListener("submit", (event) =>{
    event.preventDefault();
    clearResult();

    const form = document.getElementById("repo-form");
    const formData = new FormData(form);
    const targetUrl = formData.get("url");
    const endpoints = `/crawler/crawling?url=${targetUrl}`

    console.log(endpoints);
    setCrawlingProcessBox(true);

    /**
     * 크롤링 요청은 편의상 form 객체에서 진행함
     */
    fetch(endpoints,{
        method: 'GET',
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
            pollingStatus(data['repoid']); // 상태 갱신
        }else if(state === 110){
            /**
             * 크롤링 완료 + ai 진행 안되어있음
             * ai request하고
             * 크롤링 완료처리를 함
             */
            getAiResult(data['repoid']);
            getSourceCode(data['repoid']); // 크롤링 데이터 받아오기
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
const pollingStatus = (rid) => {
    /**
     * 서버로부터 작업의 상태정보를 가져오고 해당 상태에 걸맞는 적절한 메서드를 호출한다
     *
     */
    const repo = `${rid}`
    const pollingEndpoint = `/ui/polling/${repo}`;

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
                getSourceCode(rid); // 크롤링 데이터 받아오기
                getAiResult(rid);
                clearPolling();
            }
        });
    }
    /* end of pollingStatus */

    // start interval
    const interval = setInterval(()=>{
        pollingFetch();
    },20*1000);

    // stop interval
    const clearPolling = () => {
        clearInterval(interval);
    };
}
/* end polling status */


/* insert template fragment */
const getSourceCode = (rid) => {
    const repository = `${rid}`;
    fetch(`/ui/frag/${repository}/source`,{
        method: 'GET'
    }).then(resp=>resp.text())
    .then(data=>{
        resultCode.innerHTML = data;
        hljs.highlightAll();
        setCrawlingProcessBox(false);
    })
}

const getAiResult = (rid) => {
    const repository = `${rid}`;
    fetch(`/ui/${repository}/ai`,{
        method: 'POST'
    }).then(resp=>resp.text())
    .then(data=>{
        resultAi.innerHTML = data;
        setAiProcessBox(false);
    })
}
/* utils */
const checkWorkState = (status) => {
    console.log("checkWorkState", status);
    if(status === 'CRAWLING_NOW'){
        // crawling 작업 중
        return 100;
    }else if(status === 'CRAWLING_SUCCESS'){
        // 크롤링 완료
        return 110;
    }else if(status === 'AI_API_NOW'){
        // AI 작업 중
        return 200;
    }else if(status === 'AI_API_SUCCESS'){
        // AI 작업 완료
        return 210;
    }else{
        // 실패
        return -1;
    }
}

