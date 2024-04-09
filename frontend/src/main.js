import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import 'highlight.js/styles/stackoverflow-light.css'
import 'highlight.js/lib/common';
import hljsVuePlugin from "@highlightjs/vue-plugin";

import {createRouter, createWebHistory} from 'vue-router';
import RepoForm from './components/form/RepoForm.vue';
import RepoResultWrapper from './components/RepoResultWrapper.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path : '/', component: RepoForm},
        {path : '/result/:username/:reponame', component: RepoResultWrapper}
    ]
});

const app = createApp(App);
app.use(router);
app.use(hljsVuePlugin)
app.mount('#app');

