<script>
import RepoSources from './RepoSources.vue';
import { pollingApi } from '../api/RepositoryApi';
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
            pollingApi(
                this.username,
                this.reponame,
                this.pollingSuccess,
                this.pollingFail
            )

            // 크롤링이 끝날때까지 기다려줌
            if(this.pollingFlag){
                this.pollingInterval = setInterval(()=>{
                    pollingApi(
                        this.username,
                        this.reponame,
                        this.pollingSuccess,
                        this.pollingFail
                    )
                }, 10*1000);
            }
        },
        pollingSuccess(data){
            console.log("success");
            this.pollingFlag = false;
            this.repoDatas = data.data;
            this.clearPolling();
        },
        pollingFail(){
            console.log("fail");
            this.pollingFlag = false;
            this.failFlag = true;
            this.clearPolling();
        },
        clearPolling(){
            if(this.pollingInterval !== null)
                clearInterval(this.pollingInterval);

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