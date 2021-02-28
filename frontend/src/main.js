import Vue from 'vue'
import App from './App.vue'
import router from './router'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './assets/main.css';
import firebase from 'firebase'

Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(require('vue-cookies')) // https://github.com/cmp-cc/vue-cookies
Vue.prototype.$backend_url = "http://localhost:5000/"
Vue.mixin({
  methods: {
    getUserHeaders() {
      return { headers: {account_id: this.$cookies.get('user-id'), session_id: this.$cookies.get('session-id')}}
    }
  }
});

new Vue({
  router,
  render: h => h(App),
  created() {
    // Your web app's Firebase configuration
    var firebaseConfig = {
      apiKey: "AIzaSyAB7fXb4mw73hcyZYcGXtwmTezMglHwag0",
      authDomain: "salonymarcopolo.firebaseapp.com",
      projectId: "salonymarcopolo",
      storageBucket: "salonymarcopolo.appspot.com",
      messagingSenderId: "1049631200726",
      appId: "1:1049631200726:web:45b0be378568b157734077"
    };
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
  }
}).$mount('#app')