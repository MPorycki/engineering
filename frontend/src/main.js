import Vue from 'vue'
import App from './App.vue'
import router from './router'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './assets/main.css';

Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.prototype.$backend_url = "http://localhost:5000/"

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
