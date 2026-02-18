import { defineStore } from 'pinia'
import { ref } from 'vue'

// 用户状态管理 Store
export const useUserStore = defineStore('user', () => {
  // 从本地存储中读取 token 和用户信息
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))

  // 设置用户 token
  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  // 设置用户信息
  function setUserInfo(info) {
    userInfo.value = info
    localStorage.setItem('userInfo', JSON.stringify(info))
  }

  // 退出登录：清除 token 和用户信息
  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  // 检查用户是否已登录
  function isLoggedIn() {
    return !!token.value
  }

  // 检查用户是否为 VIP 会员
  function isVip() {
    return userInfo.value?.membership_type === 'vip'
  }

  return {
    token,
    userInfo,
    setToken,
    setUserInfo,
    logout,
    isLoggedIn,
    isVip
  }
})
