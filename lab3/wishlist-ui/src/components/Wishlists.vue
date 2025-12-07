<template>
  <div class="max-w-3xl mx-auto p-6">
    <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">Your Wishlists</h2>

    <!-- Create new wishlist form -->
    <form @submit.prevent="createList" class="flex mb-6 space-x-2">
      <input
        v-model="title"
        type="text"
        placeholder="New wishlist title"
        required
        class="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <button
        type="submit"
        class="px-4 py-2 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white font-semibold rounded-lg shadow-md transition duration-150 transform active:scale-95"
      >
        Create
      </button>
    </form>

    <!-- Error message -->
    <p v-if="error" class="text-red-600 mb-4 text-center">{{ error }}</p>

    <!-- Wishlists -->
    <ul class="space-y-3">
      <li
        v-for="wl in wishlists"
        :key="wl.id"
        class="bg-white p-4 rounded-xl shadow hover:shadow-md transition duration-150 flex justify-between items-center"
      >
        <div>
          <router-link
            :to="`/wishlists/${wl.id}`"
            class="text-blue-600 font-medium hover:underline"
          >
            {{ wl.title }}
          </router-link>
          <p class="text-gray-500 text-sm mt-1">
            Created: {{ formatDate(wl.created_at) }} | Items: {{ wl.items_count }}
          </p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import api from '../api'
import { useRoute } from 'vue-router'

interface WishListResponse {
  id: number
  title: string
  user_id: number
  created_at: string  
  owner_name?: string
  items_count: number
}

const wishlists = ref<WishListResponse[]>([])
const title = ref<string>('')
const error = ref<string | null>(null)
const route = useRoute()

async function fetchWishlists() {
  try {
    let url = '/wishlists'
    if (route.path === '/my-wishlists') {
      url = '/my-wishlists'   
    }
    const res = await api.get(url)
    wishlists.value = res.data
  } catch (e) {
    error.value = 'Failed to load wishlists'
  }
}

async function createList(): Promise<void> {
  if (!title.value.trim()) return  // HTML та додаткова JS валідація

  try {
    const res = await api.post('/wishlists', { title: title.value })
    wishlists.value.push(res.data)
    title.value = ''
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Create failed'
  }
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

watch(() => route.fullPath, () => {
  fetchWishlists()
})

onMounted(fetchWishlists)
</script>
