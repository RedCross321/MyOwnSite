import { createRouter, createWebHistory } from 'vue-router'
import Home from './Home.vue'
import Login from './Login.vue'
import Register from './Register.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [{
      path: "/",
      name: "index",
      component: Home
    },
    {
      path: "/login",
      name: "login-page",
      component: Login
    },
    {
      path: "/register",
      name: "reg-page",
      component: Register
    }
  ],
})

export default router
