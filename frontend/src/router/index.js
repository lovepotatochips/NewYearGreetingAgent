import { createRouter, createWebHistory } from 'vue-router'

// 定义应用路由配置
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('../views/Chat.vue')
  },
  {
    path: '/greeting',
    name: 'Greeting',
    component: () => import('../views/Greeting.vue')
  },
  {
    path: '/tools',
    name: 'Tools',
    component: () => import('../views/Tools.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue')
  }
]

// 创建路由实例，使用 HTML5 History 模式
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
