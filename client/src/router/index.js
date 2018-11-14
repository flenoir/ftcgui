import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Jobs from '@/components/Jobs';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Jobs',
      component: Jobs,
    },
    {
      path: '/',
      name: 'Ping',
      component: Ping,
    },
  ],
  mode: 'history',
});
