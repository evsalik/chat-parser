import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import Upload from './components/Upload.vue';
import Statistics from './components/Statistics.vue';

const routes = [
  { path: '/', component: Upload },
  {
    path: '/statistics',
    name: 'Statistics',
    component: Statistics,
    props: true
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);
app.use(router);
app.mount('#app');
