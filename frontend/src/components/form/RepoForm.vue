<script>
export default{
    data(){
        return{
            repoUrl: '',
            username: '',
            reponame: '',
            pollingFlag: true,
            pollingInterval: null,
            repoDatas : null
        }
    },
    methods : {
        submit(){

            let jsonData = JSON.stringify({url : this.repoUrl});
            console.log(`${jsonData}`);

            fetch('http://localhost:8000/repo/query',
            {
                method : 'POST', 
                headers : {
                    'Content-Type' : 'application/json',
                },
                body: jsonData
            }).then(resp=>resp.json())
            .then(data =>{
                this.username = data.username;
                this.reponame = data.reponame;
                this.polling();
            });
        },

        polling(){
            let endpoint = `http://localhost:8000/repo/${this.username}/${this.reponame}`;

            // 크롤링이 끝날때까지 기다려줌
            this.pollingInterval = setInterval(()=>{
                fetch(endpoint)
                .then(resp=>resp.json())
                .then(data=>{
                    console.log(data)
                    if(data.code === 1){
                        // code는 api따라 달라질 수있음
                        // code 1은 완성이라는 뜻 
                        this.pollingFlag = false;
                        this.repoDatas = data.data;
                        clearInterval(this.pollingInterval);
                    }
                })
            }, 2000);
        }
    },
    computed: {
        submitResult(){
            if(this.username == '') return '';
            else{
                return `${this.username}/${this.reponame}`;
            }
        }
    }
}
</script>

<template>
    <div>
        <h3>Github-Sub</h3>
        <p>현 버전에서는 'https://'이 포함된 완전한 url만을 취급합니다.</p>
    </div>
    <form @submit.prevent="submit">
        <input name="repoUrl" id="repoUrl" type="text" v-model="repoUrl" >
        <button type="submit">제출하기</button>
    </form>
    <div v-show="submitResult !== ''">
        <h4 v-show="pollingFlag">
            Repository {{ submitResult }}에 대한 정보 추출을 진행중입니다. 조금만 기다려주십시오. 
        </h4>
        <div v-show="!pollingFlag">
            <h4>
                Repository {{ submitResult }}에 대한 정보 추출이 완료되었습니다. 
            </h4>
            <ul>
                <li v-for="data in repoDatas">
                    <h4>
                        <a :href="data.url">{{ data.directory }}</a>
                        <p>filename : {{ data.title }}</p>
                    </h4>
                    <p>
                        {{ data.src }}
                    </p>
                </li>
            </ul>
        </div>
    </div>
</template>

