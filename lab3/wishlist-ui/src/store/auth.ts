import { defineStore } from 'pinia'
import api from '../api'

interface User {
  id: number
  email: string
}

interface RegisterPayload {
  email: string
  password: string
  full_name?: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    token: (localStorage.getItem('token') || null) as string | null,
  }),
  actions: {
    async login(email: string, password: string) {
      const form = new URLSearchParams()
      form.append('username', email)
      form.append('password', password)
      const res = await api.post<{ access_token: string }>('/token', form)
      this.token = res.data.access_token
      localStorage.setItem('token', this.token)
      await this.fetchUser()
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    },

    async register(payload: RegisterPayload) {
      await api.post<User>('/register', payload)
      await this.login(payload.email, payload.password)
    },

    

    async fetchUser() {
      if (!this.token) return
      const res = await api.get<User>('/users/me')
      this.user = res.data
    },
  },
})
