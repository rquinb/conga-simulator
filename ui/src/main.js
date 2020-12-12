import Vue from 'vue';
import App from './App.vue'
import VueRouter from "vue-router";
import titleMixin from './mixins/titleMixin.js'
import Main from './components/Main.vue';
import SimulationsPage from './SimulationsPage.vue'
import StatisticsPage from './components/StatisticsPage.vue';
import StatisticsTable from './components/StatisticsTable.vue';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(VueRouter);
Vue.mixin(titleMixin)
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
      component: SimulationsPage,
      name: "SimulationsPage"
    },
    {
      path: '/games-statistics/:simulationId',
      component: StatisticsPage,
      name: "Statistics"
    },
    {
      path: '/games-statistics',
      component: StatisticsTable,
      name: "StatisticsTable"
    }
  ]
})

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');

