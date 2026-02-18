<template>
  <div class="home">
    <!-- 页面头部区域，包含Logo和标题 -->
    <div class="header-section">
      <div class="header-content">
        <div class="logo">
          <span class="logo-icon">🧧</span>
          <h1>拜年助手</h1>
        </div>
        <p class="tagline">2026丙午马年 · AI智能春节祝福</p>
      </div>
      
      <!-- 装饰性元素，增加页面视觉效果 -->
      <div class="header-decoration">
        <div class="decoration-item"></div>
        <div class="decoration-item"></div>
        <div class="decoration-item"></div>
      </div>
    </div>
    
    <!-- 主内容区域 -->
    <div class="main-content">
      <div class="welcome-card">
        <div class="welcome-text">
          <h2>春节拜年，一触即发</h2>
          <p>智能对话生成祝福，让每一句话都温暖人心</p>
        </div>
        <!-- 快捷操作卡片 -->
        <div class="quick-actions">
          <!-- AI对话卡片 -->
          <div class="action-card chat" @click="goToChat">
            <div class="card-icon">
              <span>💬</span>
            </div>
            <div class="card-content">
              <h3>AI对话</h3>
              <p>智能对话生成祝福</p>
            </div>
            <div class="card-arrow">→</div>
          </div>
          
          <!-- 祝福生成卡片 -->
          <div class="action-card greeting" @click="goToGreeting">
            <div class="card-icon">
              <span>🎊</span>
            </div>
            <div class="card-content">
              <h3>祝福生成</h3>
              <p>按人群风格定制文案</p>
            </div>
            <div class="card-arrow">→</div>
          </div>
          
          <!-- 实用工具卡片 -->
          <div class="action-card tools" @click="goToTools">
            <div class="card-icon">
              <span>🛠️</span>
            </div>
            <div class="card-content">
              <h3>实用工具</h3>
              <p>习俗礼仪送礼建议</p>
            </div>
            <div class="card-arrow">→</div>
          </div>
        </div>
      </div>
      
      <!-- 登录/注册按钮区域 -->
      <div class="login-section" v-if="!isLoggedIn">
        <el-button type="primary" size="large" @click="handleLogin">
          登录 / 注册
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import { ElMessage } from 'element-plus'

// 获取路由实例和用户状态管理
const router = useRouter()
const userStore = useUserStore()

// 计算属性：检查用户是否已登录
const isLoggedIn = computed(() => userStore.isLoggedIn())

// 跳转到AI对话页面
const goToChat = () => {
  router.push('/chat')
}

// 跳转到祝福生成页面
const goToGreeting = () => {
  router.push('/greeting')
}

// 跳转到实用工具页面
const goToTools = () => {
  router.push('/tools')
}

// 处理登录按钮点击（演示模式）
const handleLogin = () => {
  ElMessage.info('演示模式，直接使用功能')
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(180deg, #ff6b6b 0%, #ff8e53 50%, #ffa726 100%);
  overflow-x: hidden;
}

.header-section {
  position: relative;
  padding: 60px 20px 40px;
  text-align: center;
  color: white;
}

.header-content {
  position: relative;
  z-index: 2;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 16px;
}

.logo-icon {
  font-size: 48px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
}

.logo h1 {
  font-size: 32px;
  font-weight: 700;
  margin: 0;
  letter-spacing: 2px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tagline {
  font-size: 15px;
  opacity: 0.95;
  font-weight: 300;
  letter-spacing: 1px;
}

.header-decoration {
  position: absolute;
  top: 20px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 20px;
  z-index: 1;
}

.decoration-item {
  width: 8px;
  height: 8px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.decoration-item:nth-child(2) {
  animation-delay: 0.3s;
}

.decoration-item:nth-child(3) {
  animation-delay: 0.6s;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.2);
  }
}

.main-content {
  position: relative;
  padding: 0 16px 40px;
}

.welcome-card {
  background: white;
  border-radius: 24px;
  padding: 32px 24px;
  margin-bottom: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.welcome-text {
  text-align: center;
  margin-bottom: 32px;
}

.welcome-text h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
  letter-spacing: 0.5px;
}

.welcome-text p {
  font-size: 14px;
  color: #666;
  margin: 0;
  line-height: 1.6;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.action-card {
  display: flex;
  align-items: center;
  padding: 20px;
  border-radius: 16px;
  background: #fafafa;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
}

.action-card:hover {
  background: white;
  transform: translateX(4px);
}

.action-card:active {
  transform: scale(0.98);
}

.action-card.chat {
  border-left: 4px solid #ff6b6b;
}

.action-card.greeting {
  border-left: 4px solid #ff8e53;
}

.action-card.tools {
  border-left: 4px solid #ffa726;
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  flex-shrink: 0;
}

.action-card.chat .card-icon {
  background: rgba(255, 107, 107, 0.1);
}

.action-card.greeting .card-icon {
  background: rgba(255, 142, 83, 0.1);
}

.action-card.tools .card-icon {
  background: rgba(255, 167, 38, 0.1);
}

.card-icon span {
  font-size: 24px;
}

.card-content {
  flex: 1;
}

.card-content h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 4px 0;
}

.card-content p {
  font-size: 13px;
  color: #999;
  margin: 0;
}

.card-arrow {
  font-size: 20px;
  color: #ddd;
  font-weight: bold;
  transition: all 0.3s;
}

.action-card:hover .card-arrow {
  color: #666;
  transform: translateX(4px);
}

.login-section {
  text-align: center;
  padding: 24px 0 8px;
}

.login-section .el-button {
  width: 200px;
  height: 48px;
  border-radius: 24px;
  font-size: 15px;
  font-weight: 500;
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
  border: none;
  box-shadow: 0 4px 16px rgba(255, 107, 107, 0.3);
  transition: all 0.3s;
}

.login-section .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
}

.login-section .el-button:active {
  transform: translateY(0);
}
</style>
