<template>
  <div class="greeting-page">
    <div class="page-header">
      <el-icon @click="goBack" class="back-btn"><ArrowLeft /></el-icon>
      <h2>祝福生成</h2>
    </div>
    
    <div class="greeting-form">
      <el-form :model="form" label-position="top">
        <el-form-item label="目标人群">
          <el-select v-model="form.targetGroup" placeholder="请选择">
            <el-option label="长辈" value="elder" />
            <el-option label="领导/客户" value="leader" />
            <el-option label="同事/伙伴" value="colleague" />
            <el-option label="朋友/闺蜜" value="friend" />
            <el-option label="老师/学生" value="teacher" />
            <el-option label="群发通用" value="general" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="风格">
          <el-select v-model="form.style" placeholder="请选择">
            <el-option label="正式稳重" value="formal" />
            <el-option label="高情商得体" value="high_eq" />
            <el-option label="简短高级" value="short" />
            <el-option label="幽默搞笑" value="humor" />
            <el-option label="温暖走心" value="warm" />
            <el-option label="古风文雅" value="classic" />
            <el-option label="商务官方" value="business" />
            <el-option label="可爱俏皮" value="cute" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="格式">
          <el-select v-model="form.formatType" placeholder="请选择">
            <el-option label="短句类" value="sentence" />
            <el-option label="长文类" value="long" />
            <el-option label="对联类" value="couplet" />
            <el-option label="朋友圈文案" value="moments" />
            <el-option label="视频文案" value="video" />
            <el-option label="红包封面语" value="red_packet" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="关键词（可选）">
          <el-input 
            v-model="form.keywords" 
            placeholder="如：健康、顺利、马年、事业"
          />
        </el-form-item>
        
        <el-form-item label="生成数量">
          <el-slider v-model="form.count" :min="1" :max="10" />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            @click="generateGreeting"
            :loading="loading"
            block
          >
            生成祝福
          </el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <div v-if="greetings.length > 0" class="greeting-results">
      <h3>生成结果</h3>
      <div 
        v-for="(greeting, index) in greetings" 
        :key="index"
        class="greeting-card"
      >
        <div class="greeting-content">{{ greeting }}</div>
        <div class="greeting-actions">
          <el-button 
            size="small" 
            @click="copyText(greeting)"
            :icon="CopyDocument"
          >
            复制
          </el-button>
          <el-button 
            size="small" 
            @click="optimizeText(greeting)"
          >
            优化
          </el-button>
        </div>
      </div>
    </div>
    
    <el-dialog v-model="optimizeDialog" title="文案优化" width="90%">
      <el-form :model="optimizeForm">
        <el-form-item label="目标风格">
          <el-select v-model="optimizeForm.targetStyle" placeholder="保持原风格" clearable>
            <el-option label="正式稳重" value="formal" />
            <el-option label="高情商得体" value="high_eq" />
            <el-option label="简短高级" value="short" />
            <el-option label="幽默搞笑" value="humor" />
            <el-option label="温暖走心" value="warm" />
            <el-option label="古风文雅" value="classic" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="目标人群">
          <el-select v-model="optimizeForm.targetGroup" placeholder="保持原人群" clearable>
            <el-option label="长辈" value="elder" />
            <el-option label="领导/客户" value="leader" />
            <el-option label="朋友" value="friend" />
            <el-option label="群发通用" value="general" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <div class="original-text">
        <h4>原文：</h4>
        <p>{{ optimizeForm.content }}</p>
      </div>
      
      <div class="optimized-result" v-if="optimizedText">
        <h4>优化后：</h4>
        <p>{{ optimizedText }}</p>
      </div>
      
      <template #footer>
        <el-button @click="optimizeDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          @click="doOptimize"
          :loading="optimizeLoading"
        >
          优化
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, CopyDocument } from '@element-plus/icons-vue'
import { greetingApi } from '../api'
import { ElMessage } from 'element-plus'

const router = useRouter()

const form = ref({
  targetGroup: '',
  style: '',
  formatType: '',
  keywords: '',
  count: 3
})

const loading = ref(false)
const greetings = ref([])

const optimizeDialog = ref(false)
const optimizeForm = ref({
  content: '',
  targetStyle: '',
  targetGroup: '',
  avoidDuplicate: false
})
const optimizeLoading = ref(false)
const optimizedText = ref('')

const goBack = () => {
  router.back()
}

const generateGreeting = async () => {
  if (!form.value.targetGroup || !form.value.style || !form.value.formatType) {
    ElMessage.warning('请完善选项')
    return
  }
  
  loading.value = true
  
  try {
    const response = await greetingApi.generateGreeting({
      target_group: form.value.targetGroup,
      style: form.value.style,
      format_type: form.value.formatType,
      keywords: form.value.keywords ? form.value.keywords.split(',').map(k => k.trim()) : [],
      count: form.value.count
    })
    
    console.log('祝福生成响应:', response)
    
    if (response && response.greetings) {
      greetings.value = response.greetings
      ElMessage.success(`成功生成${greetings.value.length}条祝福`)
    } else {
      ElMessage.error('生成失败，请重试')
    }
  } catch (error) {
    console.error('生成失败:', error)
    ElMessage.error('生成失败，请重试')
  } finally {
    loading.value = false
  }
}

const copyText = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    ElMessage.success('已复制到剪贴板')
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}

const optimizeText = (text) => {
  optimizeForm.value.content = text
  optimizedText.value = ''
  optimizeDialog.value = true
}

const doOptimize = async () => {
  optimizeLoading.value = true
  
  try {
    const response = await greetingApi.optimizeGreeting({
      content: optimizeForm.value.content,
      target_style: optimizeForm.value.targetStyle || undefined,
      target_group: optimizeForm.value.targetGroup || undefined,
      avoid_duplicate: optimizeForm.value.avoidDuplicate
    })
    
    console.log('优化响应:', response)
    
    if (response && response.optimized) {
      optimizedText.value = response.optimized
      ElMessage.success('优化成功')
    } else if (response && response.suggestions && response.suggestions.length > 0) {
      optimizedText.value = response.suggestions[0]
      ElMessage.success('优化成功')
    } else {
      ElMessage.error('优化失败，请重试')
    }
  } catch (error) {
    console.error('优化失败:', error)
    ElMessage.error('优化失败，请重试')
  } finally {
    optimizeLoading.value = false
  }
}
</script>

<style scoped>
.greeting-page {
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

.greeting-form {
  background: white;
  margin: 15px;
  padding: 20px;
  border-radius: 12px;
}

.greeting-results {
  padding: 0 15px 20px;
}

.greeting-results h3 {
  margin-bottom: 15px;
  color: #333;
}

.greeting-card {
  background: white;
  border-radius: 12px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.greeting-content {
  line-height: 1.8;
  color: #333;
  margin-bottom: 12px;
  white-space: pre-wrap;
}

.greeting-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.original-text, .optimized-result {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
  margin: 10px 0;
}

.original-text h4, .optimized-result h4 {
  margin-bottom: 10px;
  color: #666;
}

.original-text p, .optimized-result p {
  line-height: 1.6;
  color: #333;
  white-space: pre-wrap;
}
</style>
