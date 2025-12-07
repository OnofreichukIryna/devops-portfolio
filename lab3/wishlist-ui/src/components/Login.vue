<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-50 to-blue-100">
    <div class="w-full max-w-md p-8 bg-white rounded-2xl shadow-xl border border-gray-200">
      <h2 class="text-3xl font-bold text-center text-gray-800 mb-6">Login</h2>
      <form @submit.prevent="onSubmit" class="space-y-5">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            required
            placeholder="you@example.com"
            class="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="********"
            class="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
          />
        </div>
        <button
          type="submit"
          class="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md transition-all duration-200 transform hover:-translate-y-0.5"
        >
          Login
        </button>
      </form>
      <p v-if="error" class="mt-4 text-center text-red-500">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'

const email = ref<string>('')
const password = ref<string>('')
const error = ref<string | null>(null)

const auth = useAuthStore()
const router = useRouter()

async function onSubmit(): Promise<void> {
  error.value = null
  try {
    await auth.login(email.value, password.value)
    router.push('/my-wishlists')
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Login failed'
  }
}
</script>
