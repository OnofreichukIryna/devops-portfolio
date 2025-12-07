import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Wishlists from '../components/Wishlists.vue'
import WishlistDetail from '../components/WishlistDetail.vue'
import Welcome from '../components/Welcome.vue'
import { useAuthStore } from '../store/auth'

// Define routes array type
const routes: Array<RouteRecordRaw> = [
  { path: '/', component: Welcome },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/wishlists', component: Wishlists, meta: { all: true, requiresAuth: true } },
  { path: '/my-wishlists', component: Wishlists, meta: { all: false, requiresAuth: true } },
  { path: '/wishlists/:id', component: WishlistDetail, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard for auth
router.beforeEach(async (to, _from, next) => {
  const auth = useAuthStore()
  
  // If token exists but user is not loaded, fetch user
  if (!auth.user && auth.token) {
    try {
      await auth.fetchUser()
    } catch (e) {
      auth.logout()
    }
  }
  
  // Redirect to login if route requires auth and user is not logged in
  if (to.meta.requiresAuth && !auth.user) {
    return next('/login')
  }
  
  next()
})

export default router