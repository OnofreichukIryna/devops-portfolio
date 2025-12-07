import axios, { type InternalAxiosRequestConfig } from 'axios'
import { useAuthStore } from './store/auth'

const API_BASE = import.meta.env.VITE_API_BASE as string || 'http://localhost:8000'

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