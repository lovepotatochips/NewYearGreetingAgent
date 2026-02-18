# 拜年助手 - 快速启动指南

## 🚀 快速启动

### 前置要求

1. Python 3.8+
2. Node.js 16+
3. MySQL 5.7+

### 步骤一：配置数据库

1. 创建MySQL数据库
```sql
CREATE DATABASE newyear_greeting DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 配置后端环境变量
```bash
cd backend
cp .env.example .env
```

3. 编辑 `.env` 文件，修改数据库连接信息
```
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/newyear_greeting
SECRET_KEY=your-secret-key-here
AI_API_KEY=your-openai-api-key
```

### 步骤二：启动后端

1. 安装Python依赖
```bash
cd backend
pip install -r requirements.txt
```

2. 初始化数据库
```bash
python init_db.py
```

3. 启动后端服务
```bash
python -m app.main
```

后端将在 http://localhost:8000 启动

### 步骤三：启动前端

1. 安装前端依赖（如果还没安装）
```bash
cd frontend
npm install
```

2. 启动前端开发服务器
```bash
npm run dev
```

前端将在 http://localhost:5174 启动

## 📱 访问应用

打开浏览器访问：http://localhost:5174

## 🎯 功能测试

### 1. 首页功能
- 点击"AI对话"进入智能对话界面
- 点击"祝福生成"进入文案生成页面
- 点击"实用工具"查看各种实用功能

### 2. AI对话测试
在对话界面输入：
- "帮我生成给长辈的拜年文案"
- "除夕有什么习俗？"
- "如何给领导拜年？"

### 3. 祝福生成测试
选择目标人群、风格、格式，点击"生成祝福"
- 可以复制生成的文案
- 可以点击"优化"按钮进行文案优化

### 4. 实用工具测试
- 习俗问答：输入"拜年有什么讲究？"
- 礼仪指导：输入"敬酒礼仪"
- 送礼建议：选择"长辈"
- 红包建议：选择"吉利数字"
- 年夜饭：输入人数
- 行程安排：输入"大年初一"

## 📖 API文档

后端启动后访问：http://localhost:8000/docs

## 🔧 开发说明

### 后端项目结构
```
backend/
├── app/
│   ├── api/              # API路由
│   ├── core/             # 核心配置（数据库、认证等）
│   ├── models/           # 数据库模型
│   ├── schemas/          # Pydantic数据验证模型
│   ├── services/         # 业务逻辑层
│   └── utils/            # 工具函数
├── init_db.py           # 数据库初始化脚本
├── requirements.txt     # Python依赖
└── .env.example         # 环境变量示例
```

### 前端项目结构
```
frontend/
├── src/
│   ├── api/             # API请求封装
│   ├── components/      # 可复用组件
│   ├── router/          # 路由配置
│   ├── store/           # Pinia状态管理
│   ├── styles/          # 全局样式
│   ├── utils/           # 工具函数
│   └── views/           # 页面组件
├── index.html
├── vite.config.js       # Vite配置
└── package.json         # 依赖配置
```

## ⚠️ 注意事项

1. **数据库连接**：确保MySQL服务已启动，且用户名密码配置正确
2. **AI服务**：如果没有配置OpenAI API Key，系统会使用模拟回复
3. **端口占用**：如果端口被占用，Vite会自动尝试其他端口
4. **跨域问题**：前端已配置代理，无需担心跨域

## 🎨 自定义开发

### 添加新的祝福模板
在 `backend/init_db.py` 中的 `sample_greetings` 数组添加新数据

### 修改AI回复
在 `backend/app/services/ai_service.py` 中的 `_mock_response` 方法修改

### 添加新页面
1. 在 `frontend/src/views/` 创建新组件
2. 在 `frontend/src/router/index.js` 添加路由

## 📞 技术支持

遇到问题请查看：
1. 后端日志：终端输出
2. 前端日志：浏览器控制台
3. API文档：http://localhost:8000/docs

## 🎉 开始使用

现在您可以开始使用拜年助手了！祝您2026马年快乐！🐴
