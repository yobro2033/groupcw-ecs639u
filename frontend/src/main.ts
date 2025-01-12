import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import {createPinia} from 'pinia';
import axios from 'axios';
import {API_BASE_URL} from './config';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';



const app = createApp(App)
const pinia = createPinia();
// 将 axios 挂载到 Vue 实例的原型上，这样可以在组件中通过 this.$axios 访问
app.config.globalProperties.$axios = axios;
app.config.globalProperties.$apiBaseUrl = API_BASE_URL;
app.use(router)
app.use(pinia);
app.mount('#app')
