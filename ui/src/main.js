import Vue from 'vue';
import App from './App.vue'
import VueRouter from "vue-router";
import Main from './components/Main.vue';
import Simulator from './components/Simulator.vue';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(VueRouter);
const router = new VueRouter({
  mode: "hash",
  routes: [
    {
      path: '/',
      component: Main,
      name: "Main"
    },
    {
      path: '/simulator',
      component: Simulator,
      name: "Simulator"
    },
  ]
})

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');

