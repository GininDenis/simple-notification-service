import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VueSelect from 'vue-select'
import underscore from 'vue-underscore';
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import '@fortawesome/fontawesome-free/css/all.css'

Vue.config.productionTip = false;
Vue.component('v-select', VueSelect);
Vue.use(underscore);

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
