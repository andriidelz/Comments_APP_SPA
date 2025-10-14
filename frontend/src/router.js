import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue' 
import CommentForm from './components/CommentForm.vue'
import Login from './components/Login.vue'

const routes = [
  { path: '/', component: HomeView }, 
  { path: '/login', component: Login },
  { path: '/comments', component: CommentForm }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router