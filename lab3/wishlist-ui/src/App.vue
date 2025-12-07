<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-white border-b shadow-sm">
      <div class="max-w-6xl mx-auto flex items-center justify-between px-6 py-4">
        <!-- Logo / Title -->
        <router-link
          to="/"
          class="text-2xl font-bold text-blue-600 hover:text-blue-800 transition"
        >
          WishList
        </router-link>

        <!-- Navigation -->
        <nav class="flex items-center gap-6">
          <router-link
            to="/"
            class="nav-link"
          >
            Home
          </router-link>

          <template v-if="auth.user">
            <router-link
              to="/my-wishlists"
              class="nav-link"
            >
              My Wishlists
            </router-link>

            <router-link
              to="/wishlists"
              class="nav-link"
            >
              All Wishlists
            </router-link>

            <button
              @click="logout"
              class="ml-4 px-3 py-1 bg-red-500 text-white rounded-lg hover:bg-red-600 transition"
            >
              Logout
            </button>
          </template>

          <template v-else>
            <router-link
              to="/login"
              class="nav-link"
            >
              Login
            </router-link>

            <router-link
              to="/register"
              class="nav-link"
            >
              Register
            </router-link>
          </template>
        </nav>
      </div>
    </header>

    <!-- Main -->
    <main class="flex-1 max-w-6xl mx-auto p-6">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from './store/auth'

const auth = useAuthStore()

function logout() {
  auth.logout()
  window.location.href = '/login'
}
</script>

<style scoped>
.nav-link {
  @apply relative text-gray-700 hover:text-blue-600 transition;
}
.nav-link.router-link-active {
  @apply font-semibold text-blue-600;
}
.nav-link.router-link-active::after {
  content: '';
  @apply absolute left-0 -bottom-1 w-full h-0.5 bg-blue-600;
}
</style>
