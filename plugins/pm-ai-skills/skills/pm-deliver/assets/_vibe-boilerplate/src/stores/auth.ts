import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface UserInfo {
  id: number
  username: string
  name: string
  avatar: string
  role: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('arco-pro-token'))
  const user  = ref<UserInfo | null>(null)

  const isLoggedIn = computed(() => !!token.value)

  function login(username: string, _password: string): boolean {
    // Mock：admin / 123456
    if (username === 'admin' || username === '管理员') {
      token.value = 'mock-token-vibe-pro'
      localStorage.setItem('arco-pro-token', 'mock-token-vibe-pro')
      user.value = {
        id: 1,
        username: 'admin',
        name: 'Vibe Admin',
        avatar: '',
        role: '管理员',
      }
      return true
    }
    return false
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('arco-pro-token')
  }

  return { token, user, isLoggedIn, login, logout }
})
