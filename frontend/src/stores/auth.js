import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/services/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('glf_admin_token') || null)
  const loading = ref(false)
  const error = ref(null)

  // A token in storage means we are authenticated — user data loads lazily via fetchMe.
  // We don't require user.value to be loaded yet, to avoid a race on page refresh.
  const isAuthenticated = computed(() => !!token.value)

  async function login(email, password) {
    loading.value = true
    error.value = null
    try {
      const res = await authApi.login(email, password)
      token.value = res.data.access_token
      user.value = res.data.user
      localStorage.setItem('glf_admin_token', res.data.access_token)
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error?.message || 'Login failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      await authApi.logout()
    } catch (_) {
      // Ignore logout errors
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem('glf_admin_token')
    }
  }

  async function fetchMe() {
    if (!token.value) return
    try {
      const res = await authApi.me()
      user.value = res.data
    } catch (_) {
      // Token invalid — clear it
      token.value = null
      user.value = null
      localStorage.removeItem('glf_admin_token')
    }
  }

  // Initialize on store creation
  if (token.value) {
    fetchMe()
  }

  return { user, token, loading, error, isAuthenticated, login, logout, fetchMe }
})
