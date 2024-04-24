document.getElementById("repo-form").addEventListener("submit", (event) =>{
  event.preventDefault();

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
      polling(data);
  }).catch(error=>{
      console.log('오류', error);
  })
});

const polling = (data) => {
    const repo = `${data['username']}/${data['reponame']}`
    const pollingEndpoint = `/ui/mock/polling/${repo}`;
    const sourceCodeEndpoint = `/ui/${data['username']}/${data['reponame']}/source`;

    const pollingFetch = () => {
        fetch(pollingEndpoint, {
            method: 'GET',
            headers : {
                'Content-Type' : 'application/json',
            }
        }).then(resp=>resp.json())
        .then(data =>{
            if(data['status'] == 'CRAWLING_COMPLETE'){
                clearPolling();
                fetch(sourceCodeEndpoint,{
                    method: 'GET'
                }).then(resp=>resp.text())
                    .then(data=>{
                        document.getElementById('result').innerHTML = data;
                        hljs.highlightAll();
                    })
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
