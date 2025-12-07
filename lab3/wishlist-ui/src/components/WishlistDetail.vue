<template>
  <div class="max-w-3xl mx-auto p-6">
    <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">
      Wishlist: {{ wishlist?.title }}
    </h2>

    <!-- Add new item form -->
    <form @submit.prevent="addItem" class="flex mb-6 space-x-2">
      <input
        v-model="newItem.title"
        type="text"
        placeholder="Item title"
        required
        class="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <input
        v-model="newItem.url"
        type="url"
        placeholder="URL (optional)"
        class="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <button
        type="submit"
        class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-semibold shadow-md transition duration-150 transform active:scale-95"
      >
        Add Item
      </button>
    </form>

    <!-- Error message -->
    <p v-if="error" class="text-red-600 mb-4 text-center">{{ error }}</p>

    <!-- Items list -->
    <ul class="space-y-3">
     <li
  v-for="item in items"
  :key="item.id"
  class="bg-white p-4 rounded-xl shadow hover:shadow-md transition duration-150 flex justify-between items-center"
>
  <div>
    <p
      class="font-medium text-gray-800 transition-all duration-300"
      :class="{
        'line-through text-gray-400': item.marked,
        'no-underline text-gray-800': !item.marked
      }"
    >
      {{ item.title }}
    </p>
    <a
      v-if="item.url"
      :href="item.url"
      target="_blank"
      class="text-blue-600 hover:underline text-sm"
    >
      link
    </a>
  </div>

  <div class="flex gap-2">
    <!-- Mark / Unmark -->
    <button
      @click="toggleMark(item)"
      class="p-2 bg-yellow-500 hover:bg-yellow-600 text-white rounded-md flex items-center justify-center"
      :title="item.marked ? 'Unmark' : 'Mark'"
    >
      <Check v-if="!item.marked" class="w-5 h-5"/>
      <X v-else class="w-5 h-5"/>
    </button>

    <!-- Delete -->
    <button
      @click="deleteItem(item)"
      class="p-2 bg-red-600 hover:bg-red-700 text-white rounded-md flex items-center justify-center"
      title="Delete"
    >
      <X class="w-5 h-5"/>
    </button>

    <!-- History -->
    <button
      @click="showHistory(item)"
      class="p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md flex items-center justify-center"
      title="History"
    >
      <Clock class="w-5 h-5"/>
    </button>
  </div>
</li>

    </ul>

    <!-- Status history modal -->
    <div
      v-if="historyVisible"
      class="fixed inset-0 flex items-center justify-center bg-black/50 z-50"
    >
      <div class="bg-white rounded-xl p-6 w-full max-w-lg shadow-lg">
        <h3 class="text-xl font-bold mb-4">Status history for {{ historyItem?.title }}</h3>
        <ul class="space-y-2 mb-4 max-h-64 overflow-y-auto">
          <li
            v-for="s in statuses"
            :key="s.id"
            class="text-gray-700 text-sm"
          >
            {{ s.user_name }} — <span :class="s.marked ? 'text-green-600' : 'text-gray-500'">{{ s.marked ? 'marked' : 'unmarked' }}</span> ({{ formatDateTime(s.created_at) }})
          </li>
        </ul>
        <button
          @click="closeHistory"
          class="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'
import { Check, X, Clock } from 'lucide-vue-next'

interface Item {
  id: number
  title: string
  url?: string
  marked: boolean
}

interface Status {
  id: number
  user_name: string
  marked: boolean
  created_at: string
}

interface Wishlist {
  id: number
  title: string
}

const route = useRoute()
const router = useRouter()
const wishlist = ref<Wishlist | null>(null)
const items = ref<Item[]>([])
const newItem = ref<{ title: string; url: string }>({ title: '', url: '' })
const error = ref<string | null>(null)

const historyVisible = ref(false)
const historyItem = ref<Item | null>(null)
const statuses = ref<Status[]>([])

async function fetchWishlist() {
  try {
    const res = await api.get(`/wishlists/${route.params.id}`)
    wishlist.value = res.data
  } catch {
    error.value = 'Wishlist not found'
    router.push('/wishlists')
  }
}

// async function fetchItems() {
//   try {
//     const res = await api.get(`/wishlists/${route.params.id}/items`)
//     items.value = res.data
//   } catch {
//     error.value = 'Failed to load items'
//   }
// }


async function fetchItems() {
  try {
    const res = await api.get(`/wishlists/${route.params.id}/items`)
    items.value = res.data.map((i: any) => ({
      ...i,
      marked: i.is_marked,
      url: i.description
    }))
  } catch {
    error.value = 'Failed to load items'
  }
}


async function addItem() {
  if (!newItem.value.title.trim()) return
  try {
    const res = await api.post(`/wishlists/${route.params.id}/items`, {
      title: newItem.value.title,
      description: newItem.value.url  
    })
    items.value.push(res.data)
    newItem.value.title = ''
    newItem.value.url = ''
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Add item failed'
  }
}
async function deleteItem(item: Item) {
  const confirmDelete = confirm(`Delete "${item.title}"?`)
  if (!confirmDelete) return
  try {
    await api.delete(`/wishlists/${route.params.id}/items/${item.id}`)
    items.value = items.value.filter(i => i.id !== item.id)
  } catch {
    error.value = 'Delete failed'
  }
}

async function toggleMark(item: Item) {
  try {
    const res = await api.post(`/wishlists/${route.params.id}/items/${item.id}/mark`)
    item.marked = res.data.marked
  } catch {
    error.value = 'Mark failed'
  }
}

async function showHistory(item: Item) {
  try {
    const res = await api.get(`/wishlists/${route.params.id}/items/${item.id}/statuses`)
    statuses.value = res.data
    historyItem.value = item
    historyVisible.value = true
  } catch {
    error.value = 'Failed to load history'
  }
}

function closeHistory() {
  historyVisible.value = false
  historyItem.value = null
}

function formatDateTime(dateStr: string) {
  const date = new Date(dateStr)
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(async () => {
  await fetchWishlist()
  await fetchItems()
})
</script>
