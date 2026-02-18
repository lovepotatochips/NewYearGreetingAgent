<template>
  <div class="chat-page">
    <!-- 聊天页面头部 -->
    <div class="chat-header">
      <el-icon @click="goBack" class="back-btn"><ArrowLeft /></el-icon>
      <h2>AI对话</h2>
    </div>
    
    <!-- 消息列表容器 -->
    <div class="chat-container" ref="chatContainer">
      <!-- 循环显示所有消息 -->
      <div 
        v-for="msg in messages" 
        :key="msg.id" 
        :class="['message', msg.role]"
      >
        <div class="message-content">
          {{ msg.content }}
        </div>
        <div class="message-time">
          {{ formatTime(msg.created_at) }}
        </div>
      </div>
      
      <!-- AI思考中的加载状态 -->
      <div v-if="loading" class="message assistant">
        <div class="message-content loading">
          <span>正在思考中...</span>
        </div>
      </div>
    </div>
    
    <!-- 输入区域 -->
    <div class="chat-input">
      <el-input
        v-model="inputMessage"
        type="textarea"
        :rows="2"
        placeholder="输入您的问题，比如：帮我生成给长辈的拜年文案"
        @keyup.enter.ctrl="sendMessage"
      />
      <el-button 
        type="primary" 
        @click="sendMessage"
        :loading="loading"
        class="send-btn"
      >
        发送
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { conversationApi } from '../api'
import { ElMessage } from 'element-plus'

// 获取路由实例
const router = useRouter()

// 响应式数据
const chatContainer = ref(null)  // 聊天容器引用
const messages = ref([])  // 消息列表
const inputMessage = ref('')  // 输入框内容
const loading = ref(false)  // 加载状态
const currentConversationId = ref(null)  // 当前对话ID

// 返回上一页
const goBack = () => {
  router.back()
}

// 格式化时间显示（HH:MM）
const formatTime = (time) => {
  const date = new Date(time)
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  return `${hours}:${minutes}`
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim()) {
    ElMessage.warning('请输入内容')
    return
  }
  
  // 获取用户输入并清空输入框
  const userMessage = inputMessage.value.trim()
  inputMessage.value = ''
  
  // 添加用户消息到列表
  messages.value.push({
    id: Date.now(),
    role: 'user',
    content: userMessage,
    created_at: new Date().toISOString()
  })
  
  // 滚动到底部
  scrollToBottom()
  
  // 设置加载状态
  loading.value = true
  
  try {
    // 调用API发送消息
    const response = await conversationApi.chat({
      message: userMessage,
      conversation_id: currentConversationId.value
    })
    
    console.log('API响应:', response)
    
    // 处理API响应
    if (response && response.conversation && response.message) {
      currentConversationId.value = response.conversation.id
      
      // 添加AI回复到消息列表
      messages.value.push({
        id: response.message.id || Date.now(),
        role: response.message.role || 'assistant',
        content: response.message.content || '抱歉，我无法理解您的问题。',
        created_at: response.message.created_at || new Date().toISOString()
      })
    } else {
      messages.value.push({
        id: Date.now(),
        role: 'assistant',
        content: '抱歉，我无法理解您的问题，请重新表述。',
        created_at: new Date().toISOString()
      })
    }
    
    scrollToBottom()
  } catch (error) {
    console.error('发送失败:', error)
    ElMessage.error('发送失败，请重试')
    messages.value.push({
      id: Date.now(),
      role: 'assistant',
      content: '抱歉，出现了一些问题，请稍后重试。',
      created_at: new Date().toISOString()
    })
    scrollToBottom()
  } finally {
    loading.value = false
  }
}

// 组件挂载时初始化欢迎消息
onMounted(() => {
  messages.value.push({
    id: Date.now(),
    role: 'assistant',
    content: '您好！我是拜年助手，很高兴为您服务。我可以帮您：\n\n🎊 生成各种拜年祝福文案\n✨ 优化和改写文案\n📖 解答春节习俗问题\n📋 提供礼仪指导\n🎁 推荐礼物和红包\n🍲 推荐年夜饭菜单\n\n请告诉我您需要什么帮助？',
    created_at: new Date().toISOString()
  })
})
</script>

<style scoped>
.chat-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.chat-header {
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  color: white;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.back-btn {
  font-size: 24px;
  cursor: pointer;
}

.chat-header h2 {
  font-size: 18px;
  margin: 0;
  flex: 1;
}

.chat-container {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
}

.message {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
}

.message.user {
  align-items: flex-end;
}

.message.assistant {
  align-items: flex-start;
}

.message-content {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.5;
  word-wrap: break-word;
  white-space: pre-wrap;
}

.message.user .message-content {
  background: #ff6b6b;
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant .message-content {
  background: white;
  color: #333;
  border-bottom-left-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.message-content.loading {
  color: #999;
  font-style: italic;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
  padding: 0 5px;
}

.chat-input {
  background: white;
  padding: 15px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.chat-input .el-textarea {
  flex: 1;
}

.send-btn {
  height: 40px;
  border-radius: 8px;
  padding: 0 20px;
}
</style>
