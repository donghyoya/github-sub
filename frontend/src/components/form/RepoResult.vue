<script>
import RepoSources from './RepoSources.vue';
import { RouterLink } from 'vue-router';
export default{ 
    components:{
        RepoSources
    },
    props: {
        username: String, 
        reponame: String
    },
    data(){
        return{
            failFlag: false,
            pollingFlag: true,
            pollingInterval: null,
            repoDatas : null
        }
    },
    methods : {
        polling(){
            let endpoint = `http://localhost:8000/repo/${this.username}/${this.reponame}`;

            // 크롤링이 끝날때까지 기다려줌
            this.pollingInterval = setInterval(()=>{
                fetch(endpoint)
                .then(resp=>resp.json())
                .then(data=>{
                    console.log(data);
                    if(data.code === "DONE"){
                        // code는 api따라 달라질 수있음
                        // DONE = 크롤링 완료
                        this.pollingFlag = false;
                        this.repoDatas = data.data;
                        clearInterval(this.pollingInterval);
                    }else if(data.code === "FAIL" || data.code === "NONE"){
                        // FAIL = 크롤링 실패
                        this.pollingFlag = false;
                        this.failFlag = true;
                        clearInterval(this.pollingInterval);
                    }
                })
            }, 10*1000);
        }
    },
    created(){
        console.log('start page');
        this.polling();
    },
    computed: {
        submitResult(){
            console.log(this.username);
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
    <router-link :to="`/result/${submitResult}`">
        결과보러가기
    </router-link>
    <h4 v-show="pollingFlag">
        Repository {{ submitResult }}에 대한 정보 추출을 진행중입니다. 조금만 기다려주십시오. 
    </h4>
    <div v-show="!pollingFlag">
        <div v-show="failFlag">
            <h4>
                Repository {{ submitResult }}에 대한 정보 추출이 실패하였습니다. 다시 시도해주십시오. 
            </h4>
        </div>
        <div v-show="!failFlag">
            <h4>
            Repository {{ submitResult }}에 대한 정보 추출이 완료되었습니다. 
            </h4>
            <ul>
                <RepoSources 
                    v-for="data in repoDatas"
                    :src-object="data"
                />
            </ul>
        </div>
    </div>
</div>

</template>

<style scoped>
ul{
    list-style-type: none;
    margin: 0;
    padding: 0;
}
</style>