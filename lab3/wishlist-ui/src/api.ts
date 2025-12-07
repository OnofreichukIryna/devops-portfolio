import axios, { type InternalAxiosRequestConfig } from 'axios'
import { useAuthStore } from './store/auth'

// ВИПРАВЛЕННЯ: Використовуємо VITE_API_URL, як налаштували на Vercel
const API_BASE = (import.meta.env.VITE_API_URL as string) || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
})

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const auth = useAuthStore()
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  return config
})

export default api