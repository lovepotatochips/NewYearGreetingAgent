import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// Vite 配置文件
export default defineConfig({
  plugins: [vue()],
  resolve: {
    // 配置路径别名，使用 @ 代替 src 目录
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 5174,
    // 配置代理，将 /api 请求转发到后端服务器
    proxy: {
      '/api': {
        target: 'http://localhost:8003',
        changeOrigin: true
      }
    }
  }
})
