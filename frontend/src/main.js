import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import api from './utils/axios'
import { autoLogin } from './utils/auth.js';

import 'lightbox2/dist/css/lightbox.min.css'
import lightbox from 'lightbox2';

import $ from 'jquery';
window.$ = $;
window.jQuery = $;


autoLogin().then(() => {
  const app = createApp(App);
  app.use(router);
  app.config.globalProperties.$api = api;
  app.mount('#app');

  lightbox.option({
    resizeDuration: 200,
    wrapAround: true
  });

  console.log("App initialized after auto-login");
});