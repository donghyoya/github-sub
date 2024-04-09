<script>
import RepoResult from './form/RepoResult.vue';
export default{
    components:{
        RepoResult
    },
    data(){
        return {
            username: '',
            reponame: ''
        }
    },
    created(){
        this.username = this.$route.params.username;
        this.reponame = this.$route.params.reponame;
    }
}
</script>

<template>
<RepoResult
    :username="username"
    :reponame="reponame"
/>
</template>