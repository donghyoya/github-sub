const host = import.meta.env.VITE_APP_API_HOST// 'http://localhost:8000'

export const queryApi = (jsonData, successHandler) => {
    const endpoint = `${host}/repo/query`;
    
    fetch(endpoint,
    {
        method : 'POST', 
        headers : {
            'Content-Type' : 'application/json',
        },
        body: jsonData
    }).then(resp=>resp.json())
    .then(data =>{
        successHandler(data);
    });
}

export const pollingApi = (username, reponame, successHandler, failHandler) => {
    const endpoint = `${host}/repo/${username}/${reponame}`;
    fetch(endpoint)
    .then(resp=>resp.json())
    .then(data=>{
        console.log(data);
        if(data.code === "DONE"){
            // code는 api따라 달라질 수있음
            // DONE = 크롤링 완료
            successHandler(data);
        }else if(data.code === "FAIL" || data.code === "NONE"){
            // FAIL = 크롤링 실패
            failHandler();
        }
    })
};