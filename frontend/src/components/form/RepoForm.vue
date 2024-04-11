<script>
import RepoResult from './RepoResult.vue';
import { queryApi } from '../api/RepositoryApi';

export default{
    components:{
        RepoResult
    },
    data(){
        return{
            repoUrl: '',
            checkedOptions: [],
            options : [
                {label: 'java',value : 'java'},
                {label: 'python',value : 'py'},
                {label: 'javascript',value : 'js'}
            ],
            resultFlag: false,
            username: '',
            reponame: '',
        }
    },
    methods : {
        submit(){
            let jsonData = JSON.stringify({
                url : this.repoUrl,
                options: this.checkedOptions
            });
            
            console.log(jsonData);

            queryApi(jsonData, this.successHandler);
        },
        successHandler(data){
            this.username = data.username;
            this.reponame = data.reponame;
            this.resultFlag = false;
            setTimeout(()=>{
                this.resultFlag = true;
            },5)
        }
    },
}
</script>

<template>
    <div>
        <h3>Github-Sub </h3>
        <p>현 버전에서는 'https://'이 포함된 완전한 url만을 취급합니다.</p>
    </div>
    <!-- begin:form -->
    <form @submit.prevent="submit">
        <input name="repoUrl" id="repoUrl" type="text" v-model="repoUrl" >
        <!-- begin:check options -->
        <p>분석하고 싶은 코드의 언어를 선택하세요.</p>
        <ul>
            <li v-for="option in options">
                <input  type="checkbox" v-model="checkedOptions" :value="option.value" :id="option.label">
                <label :for="option.label">
                    {{ option.label }}
                </label>
            </li>    
        </ul>
        <!-- end:check options -->
        <button type="submit">제출하기</button>
    </form>
    <!-- end:form -->

    <RepoResult v-if="resultFlag"
        :username="username" :reponame="reponame"
    />
</template>

<style scoped>
ul{
    list-style-type: none;
    margin: 0;
    padding: 0;
}
</style>