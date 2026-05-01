import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || null)
  const user  = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('access_token', newToken)
  }

  function clearToken() {
    token.value = null
    user.value  = null
    localStorage.removeItem('access_token')
  }

  async function login(email, password) {
    const data = await authApi.login(email, password)
    setToken(data.access_token)
  }

  async function register(email, password, fullName) {
    await authApi.register(email, password, fullName)
  }

  function logout() {
    clearToken()
  }

  return { token, user, isAuthenticated, login, register, logout }
})
