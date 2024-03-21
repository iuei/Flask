import Vue from 'vue';
import App from './App.vue';
import ElementUI from 'element-ui';
import store from "./app/store";
import router from './router/index';
import 'element-ui/lib/theme-chalk/index.css';
import JsonExcel from 'vue-json-excel'

Vue.use(ElementUI);
Vue.prototype.$baseUrl = 'http://localhost:5000/';
Vue.prototype.$message = ElementUI.Message;
// 关闭生产提示
Vue.config.productionTip = false;
Vue.component('downloadExcel', JsonExcel)

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app');
