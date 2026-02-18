<template>
  <div class="profile-page">
    <div class="page-header">
      <el-icon @click="goBack" class="back-btn"><ArrowLeft /></el-icon>
      <h2>个人中心</h2>
    </div>
    
    <div class="profile-info">
      <div class="avatar-section">
        <div class="avatar">
          {{ userInfo?.username?.[0] || 'U' }}
        </div>
        <div class="user-name">{{ userInfo?.username || '未登录' }}</div>
        <div class="membership-badge" :class="{ vip: isVip }">
          {{ isVip ? 'VIP会员' : '普通用户' }}
        </div>
      </div>
      
      <div class="stats">
        <div class="stat-item">
          <div class="stat-value">{{ stats.todayUsage }}</div>
          <div class="stat-label">今日使用</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ stats.totalUsage }}</div>
          <div class="stat-label">累计使用</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ stats.savedGreetings }}</div>
          <div class="stat-label">收藏文案</div>
        </div>
      </div>
    </div>
    
    <div class="menu-list">
      <div class="menu-item" @click="showVipDialog">
        <span class="menu-icon">👑</span>
        <span class="menu-text">开通VIP</span>
        <el-icon class="menu-arrow"><ArrowRight /></el-icon>
      </div>
      
      <div class="menu-item" @click="showHistory">
        <span class="menu-icon">📜</span>
        <span class="menu-text">历史记录</span>
        <el-icon class="menu-arrow"><ArrowRight /></el-icon>
      </div>
      
      <div class="menu-item" @click="showSettings">
        <span class="menu-icon">⚙️</span>
        <span class="menu-text">设置</span>
        <el-icon class="menu-arrow"><ArrowRight /></el-icon>
      </div>
      
      <div class="menu-item" @click="showAbout">
        <span class="menu-icon">ℹ️</span>
        <span class="menu-text">关于</span>
        <el-icon class="menu-arrow"><ArrowRight /></el-icon>
      </div>
    </div>
    
    <div class="vip-features" v-if="!isVip">
      <h3>VIP特权</h3>
      <ul>
        <li>✨ 无限次生成祝福文案</li>
        <li>🎯 高级文案优化功能</li>
        <li>🎨 个性化定制服务</li>
        <li>🏢 企业批量功能</li>
        <li>📦 专属马年文案包</li>
      </ul>
      <el-button type="warning" @click="showVipDialog" block>
        立即开通 VIP
      </el-button>
    </div>
    
    <el-dialog v-model="vipDialog" title="开通VIP" width="90%">
      <div class="vip-options">
        <div 
          class="vip-option" 
          :class="{ active: selectedVipPlan === 'month' }"
          @click="selectedVipPlan = 'month'"
        >
          <div class="option-title">月度VIP</div>
          <div class="option-price">¥29.9/月</div>
          <div class="option-desc">灵活订阅，随时取消</div>
        </div>
        
        <div 
          class="vip-option" 
          :class="{ active: selectedVipPlan === 'year' }"
          @click="selectedVipPlan = 'year'"
        >
          <div class="option-title">年度VIP</div>
          <div class="option-price">¥199/年</div>
          <div class="option-desc">超值优惠，节省160元</div>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="vipDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          @click="handleVipPurchase"
          :loading="vipLoading"
        >
          确认开通
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { useUserStore } from '../store/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const userInfo = computed(() => userStore.userInfo)
const isVip = computed(() => userStore.isVip())

const stats = ref({
  todayUsage: 0,
  totalUsage: 0,
  savedGreetings: 0
})

const vipDialog = ref(false)
const selectedVipPlan = ref('month')
const vipLoading = ref(false)

const goBack = () => {
  router.back()
}

const showVipDialog = () => {
  if (isVip.value) {
    ElMessage.info('您已经是VIP会员')
    return
  }
  vipDialog.value = true
}

const showHistory = () => {
  ElMessage.info('历史记录功能开发中')
}

const showSettings = () => {
  ElMessage.info('设置功能开发中')
}

const showAbout = () => {
  ElMessage.info('拜年助手 v1.0.0\n2026丙午马年专属')
}

const handleVipPurchase = async () => {
  vipLoading.value = true
  
  setTimeout(() => {
    vipLoading.value = false
    vipDialog.value = false
    ElMessage.success('演示模式：VIP开通成功')
  }, 1000)
}

onMounted(() => {
  if (userInfo.value) {
    stats.value = {
      todayUsage: 5,
      totalUsage: 128,
      savedGreetings: 23
    }
  }
})
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.page-header {
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  color: white;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.back-btn {
  font-size: 24px;
  cursor: pointer;
}

.page-header h2 {
  font-size: 18px;
  margin: 0;
}

.profile-info {
  background: white;
  margin: 15px;
  padding: 25px;
  border-radius: 12px;
}

.avatar-section {
  text-align: center;
  margin-bottom: 25px;
}

.avatar {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 32px;
  font-weight: bold;
  margin: 0 auto 15px;
}

.user-name {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.membership-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  background: #e0e0e0;
  color: #666;
  font-size: 12px;
}

.membership-badge.vip {
  background: linear-gradient(135deg, #ffd700 0%, #ffaa00 100%);
  color: white;
}

.stats {
  display: flex;
  justify-content: space-around;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #ff6b6b;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  color: #999;
}

.menu-list {
  background: white;
  margin: 0 15px 15px;
  border-radius: 12px;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-item:active {
  background: #f5f5f5;
}

.menu-icon {
  font-size: 20px;
  margin-right: 12px;
}

.menu-text {
  flex: 1;
  font-size: 15px;
  color: #333;
}

.menu-arrow {
  color: #ccc;
}

.vip-features {
  background: white;
  margin: 0 15px 15px;
  padding: 20px;
  border-radius: 12px;
}

.vip-features h3 {
  margin-bottom: 15px;
  color: #333;
}

.vip-features ul {
  list-style: none;
  padding: 0;
  margin-bottom: 20px;
}

.vip-features li {
  padding: 8px 0;
  color: #666;
  font-size: 14px;
}

.vip-options {
  display: grid;
  gap: 15px;
}

.vip-option {
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.vip-option.active {
  border-color: #ff6b6b;
  background: #fff5f5;
}

.option-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.option-price {
  font-size: 24px;
  font-weight: bold;
  color: #ff6b6b;
  margin-bottom: 5px;
}

.option-desc {
  font-size: 13px;
  color: #999;
}
</style>
