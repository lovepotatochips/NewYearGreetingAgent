import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../store/user'

// 创建 axios 实例，配置基础 URL 和超时时间
const request = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 请求拦截器：在发送请求前添加认证 token
request.interceptors.request.use(
  config => {
    const userStore = useUserStore()
    if (userStore.token) {
      // 如果用户已登录，在请求头中添加 Bearer token
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器：处理响应数据和错误
request.interceptors.response.use(
  response => {
    const data = response.data
    // 如果响应包含有效数据，直接返回数据部分
    if (data && (data.message || data.conversation || data.greetings || data.suggestions || data.recommendations || data.menu_suggestions || data.schedule || data.answer || data.guidance)) {
      return data
    }
    return response.data
  },
  error => {
    // 统一处理 HTTP 错误
    if (error.response) {
      const { status, data } = error.response
      
      if (status === 401) {
        // 401 未授权：清除登录状态，跳转到首页
        const userStore = useUserStore()
        userStore.logout()
        ElMessage.error('登录已过期，请重新登录')
        window.location.href = '/'
      } else if (status === 403) {
        // 403 禁止访问：提示需要 VIP 会员
        ElMessage.error('权限不足，需要VIP会员')
      } else {
        // 其他错误：显示错误详情
        ElMessage.error(data.detail || '请求失败')
      }
    } else {
      // 网络错误：提示稍后重试
      ElMessage.error('网络错误，请稍后重试')
    }
    
    return Promise.reject(error)
  }
)

export default request
