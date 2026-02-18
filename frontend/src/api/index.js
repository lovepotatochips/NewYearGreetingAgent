import request from './request'

export const authApi = {
  login: (data) => request.post('/auth/login', data),
  register: (data) => request.post('/auth/register', data),
  getUserInfo: () => request.get('/auth/me')
}

export const conversationApi = {
  createConversation: (data) => request.post('/conversations', data),
  getConversations: (params) => request.get('/conversations', { params }),
  getConversation: (id) => request.get(`/conversations/${id}`),
  updateConversation: (id, data) => request.put(`/conversations/${id}`, data),
  deleteConversation: (id) => request.delete(`/conversations/${id}`),
  chat: (data) => request.post('/conversations/chat', data)
}

export const greetingApi = {
  getGreetings: (params) => request.get('/greetings', { params }),
  generateGreeting: (data) => request.post('/greetings/generate', data),
  optimizeGreeting: (data) => request.post('/greetings/optimize', data),
  customGreeting: (data) => request.post('/greetings/custom', data),
  saveGreeting: (id) => request.post(`/greetings/${id}/save`)
}

export const toolApi = {
  queryCustom: (data) => request.post('/tools/custom', data),
  queryEtiquette: (data) => request.post('/tools/etiquette', data),
  suggestGift: (data) => request.post('/tools/gift', data),
  suggestRedPacket: (data) => request.post('/tools/redpacket', data),
  suggestNewYearMenu: (data) => request.post('/tools/menu', data),
  suggestSchedule: (data) => request.post('/tools/schedule', data)
}
