<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-r from-green-50 to-green-100">
    <div class="w-full max-w-md p-8 bg-white rounded-2xl shadow-lg border border-gray-200">
      <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">Register</h2>
      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-gray-700 font-medium mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            required
            placeholder="you@example.com"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-400"
          />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">
            Full Name <span class="text-gray-400 text-sm">(optional)</span>
          </label>
          <input
            v-model="fullName"
            type="text"
            placeholder="John Doe"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-400"
          />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">Password</label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="********"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-400"
          />
        </div>
        <button
          type="submit"
          class="w-full px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg shadow-md transition-all duration-200 transform hover:-translate-y-0.5"
        >
          Register
        </button>
      </form>
      <p v-if="message" class="text-green-600 mt-4 text-center">{{ message }}</p>
      <p v-if="error" class="text-red-600 mt-4 text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'

const email = ref<string>('')
const fullName = ref<string>('')
const password = ref<string>('')
const message = ref<string | null>(null)
const error = ref<string | null>(null)

const auth = useAuthStore()
const router = useRouter()

async function onSubmit(): Promise<void> {
  error.value = null
  message.value = null
  try {
    const payload: any = {
      email: email.value,
      password: password.value
    }
    
    // Додаємо full_name тільки якщо воно не пусте
    if (fullName.value.trim()) {
      payload.full_name = fullName.value
    }
    
    await auth.register(payload)
    message.value = 'Registered successfully. Please login.'
    setTimeout(() => router.push('/login'), 900)
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Registration failed'
  }
}
</script>