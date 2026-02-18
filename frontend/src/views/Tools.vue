<template>
  <div class="tools-page">
    <div class="page-header">
      <el-icon @click="goBack" class="back-btn"><ArrowLeft /></el-icon>
      <h2>实用工具</h2>
    </div>
    
    <div class="tools-grid">
      <div class="tool-card" @click="openTool('custom')">
        <div class="tool-icon">📖</div>
        <h3>习俗问答</h3>
        <p>查询春节传统习俗</p>
      </div>
      
      <div class="tool-card" @click="openTool('etiquette')">
        <div class="tool-icon">🤝</div>
        <h3>礼仪指导</h3>
        <p>拜年礼仪详细说明</p>
      </div>
      
      <div class="tool-card" @click="openTool('gift')">
        <div class="tool-icon">🎁</div>
        <h3>送礼建议</h3>
        <p>推荐合适礼物</p>
      </div>
      
      <div class="tool-card" @click="openTool('redpacket')">
        <div class="tool-icon">🧧</div>
        <h3>红包建议</h3>
        <p>推荐金额和文案</p>
      </div>
      
      <div class="tool-card" @click="openTool('menu')">
        <div class="tool-icon">🍲</div>
        <h3>年夜饭</h3>
        <p>推荐菜单和祝酒词</p>
      </div>
      
      <div class="tool-card" @click="openTool('schedule')">
        <div class="tool-icon">📅</div>
        <h3>行程安排</h3>
        <p>春节活动安排建议</p>
      </div>
    </div>
    
    <el-dialog 
      v-model="dialogVisible" 
      :title="currentTool.title" 
      width="90%"
      @close="resetForm"
    >
      <el-form :model="toolForm" label-position="top">
        <el-form-item :label="currentTool.inputLabel">
          <el-input
            v-if="currentTool.inputType === 'text'"
            v-model="toolForm.input"
            :placeholder="currentTool.placeholder"
            type="textarea"
            :rows="3"
          />
          <el-select
            v-else-if="currentTool.inputType === 'select'"
            v-model="toolForm.input"
            :placeholder="currentTool.placeholder"
            style="width: 100%"
          >
            <el-option
              v-for="option in currentTool.options"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item v-if="currentTool.hasSecondInput" :label="currentTool.secondInputLabel">
          <el-input
            v-model="toolForm.secondInput"
            :placeholder="currentTool.secondPlaceholder"
          />
        </el-form-item>
        
        <el-form-item v-if="currentTool.hasThirdInput" :label="currentTool.thirdInputLabel">
          <el-select v-model="toolForm.thirdInput" placeholder="请选择" style="width: 100%">
            <el-option label="通用" value="general" />
            <el-option label="南方" value="south" />
            <el-option label="北方" value="north" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <div v-if="result" class="result-content">
        <h4>结果：</h4>
        <p>{{ result }}</p>
      </div>
      
      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
        <el-button 
          type="primary" 
          @click="submitTool"
          :loading="loading"
        >
          查询
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { toolApi } from '../api'
import { ElMessage } from 'element-plus'

const router = useRouter()

const tools = {
  custom: {
    title: '习俗问答',
    inputType: 'text',
    inputLabel: '您的问题',
    placeholder: '例如：除夕有什么习俗？',
    api: 'queryCustom'
  },
  etiquette: {
    title: '礼仪指导',
    inputType: 'text',
    inputLabel: '场景描述',
    placeholder: '例如：如何给长辈拜年？',
    api: 'queryEtiquette'
  },
  gift: {
    title: '送礼建议',
    inputType: 'select',
    inputLabel: '送礼对象',
    placeholder: '请选择送礼对象',
    options: [
      { label: '长辈', value: '长辈' },
      { label: '领导', value: '领导' },
      { label: '朋友', value: '朋友' },
      { label: '孩子', value: '孩子' },
      { label: '同事', value: '同事' }
    ],
    hasSecondInput: true,
    secondInputLabel: '预算范围（可选）',
    secondPlaceholder: '例如：200-500元',
    api: 'suggestGift'
  },
  redpacket: {
    title: '红包建议',
    inputType: 'select',
    inputLabel: '金额类型',
    placeholder: '请选择金额类型',
    options: [
      { label: '吉利数字', value: '吉利数字' },
      { label: '普通金额', value: '普通金额' },
      { label: '特殊寓意', value: '特殊寓意' }
    ],
    hasSecondInput: true,
    secondInputLabel: '关系（可选）',
    secondPlaceholder: '例如：长辈、朋友、孩子',
    api: 'suggestRedPacket'
  },
  menu: {
    title: '年夜饭菜单',
    inputType: 'text',
    inputLabel: '用餐人数',
    placeholder: '例如：6人',
    hasSecondInput: true,
    secondInputLabel: '口味偏好（可选）',
    secondPlaceholder: '例如：清淡、麻辣、不限制',
    hasThirdInput: true,
    thirdInputLabel: '地区（可选）',
    api: 'suggestNewYearMenu'
  },
  schedule: {
    title: '行程安排',
    inputType: 'text',
    inputLabel: '日期',
    placeholder: '例如：大年初一',
    hasSecondInput: true,
    secondInputLabel: '地区（可选）',
    secondPlaceholder: '例如：北京、上海',
    api: 'suggestSchedule'
  }
}

const dialogVisible = ref(false)
const currentTool = ref({})
const toolForm = ref({
  input: '',
  secondInput: '',
  thirdInput: ''
})
const loading = ref(false)
const result = ref('')

const goBack = () => {
  router.back()
}

const openTool = (toolKey) => {
  currentTool.value = tools[toolKey]
  dialogVisible.value = true
}

const resetForm = () => {
  toolForm.value = {
    input: '',
    secondInput: '',
    thirdInput: ''
  }
  result.value = ''
}

const submitTool = async () => {
  if (!toolForm.value.input) {
    ElMessage.warning('请填写必要信息')
    return
  }
  
  loading.value = true
  
  try {
    const apiMethod = toolApi[currentTool.value.api]
    const params = {}
    
    if (currentTool.value.inputType === 'select') {
      params.target_group = toolForm.value.input
      params.amount_type = toolForm.value.input
      params.people_count = parseInt(toolForm.value.input)
      params.date = toolForm.value.input
      params.scenario = toolForm.value.input
      params.question = toolForm.value.input
    } else {
      params.question = toolForm.value.input
      params.scenario = toolForm.value.input
      params.people_count = parseInt(toolForm.value.input)
      params.date = toolForm.value.input
    }
    
    if (currentTool.value.hasSecondInput && toolForm.value.secondInput) {
      params.budget = toolForm.value.secondInput
      params.relationship = toolForm.value.secondInput
      params.taste_preference = toolForm.value.secondInput
      params.region = toolForm.value.secondInput
      params.meaning = toolForm.value.secondInput
    }
    
    if (currentTool.value.hasThirdInput && toolForm.value.thirdInput) {
      params.region = toolForm.value.thirdInput
    }
    
    console.log('工具查询参数:', params)
    
    const response = await apiMethod(params)
    
    console.log('工具查询响应:', response)
    
    if (response.answer) {
      result.value = response.answer
    } else if (response.guidance) {
      result.value = response.guidance
    } else if (response.suggestions) {
      result.value = Array.isArray(response.suggestions) 
        ? response.suggestions.join('\n') 
        : response.suggestions
    } else if (response.recommendations) {
      result.value = Array.isArray(response.recommendations) 
        ? response.recommendations.join('\n') 
        : response.recommendations
    } else if (response.menu_suggestions) {
      result.value = Array.isArray(response.menu_suggestions) 
        ? response.menu_suggestions.join('\n') 
        : response.menu_suggestions
    } else if (response.schedule) {
      result.value = response.schedule
    } else {
      result.value = '抱歉，查询失败，请重试'
    }
    
    ElMessage.success('查询成功')
  } catch (error) {
    console.error('工具查询失败:', error)
    ElMessage.error('查询失败，请重试')
    result.value = '抱歉，查询失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.tools-page {
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

.tools-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  padding: 20px 15px;
}

.tool-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.tool-card:active {
  transform: scale(0.95);
}

.tool-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.tool-card h3 {
  font-size: 16px;
  margin: 10px 0 5px;
  color: #333;
}

.tool-card p {
  font-size: 12px;
  color: #999;
}

.result-content {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
  margin-top: 15px;
}

.result-content h4 {
  margin-bottom: 10px;
  color: #666;
}

.result-content p {
  line-height: 1.6;
  color: #333;
  white-space: pre-wrap;
}
</style>
