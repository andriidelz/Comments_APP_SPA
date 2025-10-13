import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
// import 'lightbox2/dist/css/lightbox.min.css'

axios.defaults.timeout = 5000 // 5 seconds
const app = createApp(App)
app.use(router)
app.mount('#app')

// createApp(App).use(router).mount('#app')