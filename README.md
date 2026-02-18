# 拜年助手

2026丙午马年专属AI智能春节祝福助手

## 项目简介

拜年助手是一个面向全人群的AI过年全能助手，以智能对话为核心交互载体，聚焦春节拜年全场景，提供话术生成、文案定制、文案优化、习俗咨询、礼仪指导、实用安排相关功能。

## 技术栈

### 后端技术栈
- **Python 3.8+**：后端开发语言
- **FastAPI 0.109.0+**：高性能异步Web框架
- **SQLAlchemy 2.0+**：ORM数据库操作框架
- **Pydantic 2.5+**：数据验证和序列化
- **Pydantic-Settings 2.0+**：配置管理
- **SQLite**：轻量级数据库（默认使用SQLite，支持切换为MySQL）
- **JWT认证**：基于python-jose和passlib实现用户认证
- **Uvicorn 0.27.0+**：ASGI服务器
- **HTTPX 0.26.0+**：异步HTTP客户端（用于调用AI API）
- **Python-dateutil & Pytz**：日期时间处理

### 前端技术栈
- **Vue 3.4.0+**：渐进式JavaScript框架
- **Vite 5.0.0+**：下一代前端构建工具
- **Vue Router 4.2.5+**：官方路由管理器
- **Pinia 2.1.7+**：Vue官方状态管理库
- **Element Plus 2.5.0+**：基于Vue 3的UI组件库
- **@element-plus/icons-vue 2.3.1+**：Element Plus图标库
- **Axios 1.6.5+**：HTTP客户端

### AI服务
- **OpenAI GPT-3.5-turbo**：AI文案生成（可配置API密钥）
- **模拟响应系统**：无API密钥时使用预设回复

## 核心功能

### 1. AI智能对话
- **多轮对话理解**：支持模糊、口语化提问
- **上下文记忆**：自动适配用户偏好
- **快速响应**：支持文字、语音双模式
- **历史记录与回溯**：保存完整对话历史

### 2. 祝福文案生成
- **按人群分类**：长辈、领导、同事、朋友、老师、通用
- **按风格分类**：正式稳重、高情商、简短高级、幽默搞笑、温暖走心、古风文雅、商务官方、可爱俏皮
- **按格式分类**：短句、长文、对联、朋友圈、视频文案、红包封面
- **2026马年专属优化**：融入马年元素和丙午年特色

### 3. 文案智能优化
- **基础优化**：润色、风格切换、长度调整、人群适配
- **高级优化**：定制化优化、企业批量优化（VIP专属）

### 4. 实用工具
- **过年习俗问答**：解答各种春节传统习俗
- **拜年礼仪指导**：走亲戚顺序、敬酒礼仪、红包礼仪等
- **送礼建议**：针对不同人群的礼物推荐
- **红包建议**：吉利数字推荐、金额寓意说明
- **年夜饭菜单推荐**：根据人数推荐菜单
- **春节行程安排**：从除夕到初七的行程建议

### 5. 个性化定制
- **基础定制**：根据关键信息生成专属祝福
- **高级定制**：结合过往经历的深度定制（VIP专属）

### 6. 会员体系
- **普通会员**：基础功能，有次数限制（每日50次）
- **VIP会员**：全功能解锁，无限制使用
- **单次付费**：满足低频增值需求

## 项目结构

```
NewYearGreetingAgent/
├── backend/                        # 后端项目
│   ├── app/
│   │   ├── api/                    # API路由
│   │   │   ├── auth.py            # 认证相关接口（登录、注册、用户信息）
│   │   │   ├── conversation.py    # 对话相关接口
│   │   │   ├── greeting.py        # 祝福生成接口
│   │   │   └── tool.py            # 实用工具接口
│   │   ├── core/                   # 核心配置
│   │   │   ├── config.py          # 应用配置
│   │   │   ├── database.py        # 数据库连接
│   │   │   ├── deps.py            # 认证依赖
│   │   │   ├── deps_anonymous.py  # 匿名访问依赖
│   │   │   └── security.py        # 安全相关（JWT、密码加密）
│   │   ├── models/                 # 数据模型（ORM）
│   │   │   ├── user.py            # 用户模型
│   │   │   ├── greeting.py        # 祝福语模型
│   │   │   ├── conversation.py    # 对话模型
│   │   │   ├── tool.py            # 工具相关模型
│   │   │   ├── knowledge.py       # 知识库模型
│   │   │   └── usage.py           # 使用记录模型
│   │   ├── schemas/                # Pydantic模式（数据验证）
│   │   │   ├── user.py            # 用户相关Schema
│   │   │   ├── greeting.py        # 祝福相关Schema
│   │   │   ├── conversation.py    # 对话相关Schema
│   │   │   └── tool.py            # 工具相关Schema
│   │   ├── services/               # 业务逻辑层
│   │   │   ├── ai_service.py      # AI服务（调用OpenAI）
│   │   │   ├── user_service.py    # 用户服务
│   │   │   ├── greeting_service.py # 祝福生成服务
│   │   │   ├── greeting_templates.py # 祝福模板
│   │   │   ├── conversation_service.py # 对话服务
│   │   │   ├── tool_service.py    # 工具服务
│   │   │   ├── tool_templates.py  # 工具模板
│   │   │   └── knowledge_service.py # 知识库服务
│   │   ├── main.py                 # FastAPI应用入口
│   │   └── __init__.py
│   ├── init_db.py                  # 数据库初始化脚本
│   ├── requirements.txt            # Python依赖
│   ├── .env.example                # 环境变量示例
│   └── newyear_greeting.db         # SQLite数据库文件（自动生成）
│
├── frontend/                       # 前端项目
│   ├── src/
│   │   ├── api/                    # API请求封装
│   │   │   ├── request.js         # Axios实例配置
│   │   │   └── index.js           # API接口定义
│   │   ├── router/                 # 路由配置
│   │   │   └── index.js           # 路由定义
│   │   ├── store/                  # Pinia状态管理
│   │   │   └── user.js            # 用户状态
│   │   ├── styles/                 # 全局样式
│   │   │   └── global.css
│   │   ├── views/                  # 页面组件
│   │   │   ├── Home.vue           # 首页
│   │   │   ├── Chat.vue           # AI对话页面
│   │   │   ├── Greeting.vue       # 祝福生成页面
│   │   │   ├── Tools.vue          # 实用工具页面
│   │   │   └── Profile.vue        # 个人中心页面
│   │   ├── App.vue                # 根组件
│   │   └── main.js                # 应用入口
│   ├── index.html                  # HTML模板
│   ├── vite.config.js             # Vite配置
│   ├── package.json               # 依赖配置
│   └── package-lock.json
│
├── README.md                       # 项目说明文档
└── START.md                        # 快速启动指南
```

## 快速开始

### 环境要求

- **Python 3.8+**
- **Node.js 16+**
- **npm 或 yarn**

### 后端启动

#### 1. 安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 2. 配置环境变量（可选）

```bash
cp .env.example .env
```

编辑 `.env` 文件，修改以下配置：

```env
# 数据库配置（默认使用SQLite，无需额外配置）
DATABASE_URL=sqlite:///./newyear_greeting.db

# 如果需要使用MySQL，取消注释并配置以下内容：
# DATABASE_URL=mysql+pymysql://root:password@localhost:3306/newyear_greeting

# JWT密钥（生产环境必须修改）
SECRET_KEY=your-secret-key-change-in-production

# OpenAI API密钥（可选，不配置则使用模拟响应）
AI_API_KEY=your-openai-api-key

# Redis配置（可选）
REDIS_URL=redis://localhost:6379/0

# CORS跨域配置
CORS_ORIGINS=http://localhost:5173,http://localhost:5174,http://localhost:8080
```

#### 3. 初始化数据库

```bash
python init_db.py
```

此脚本会：
- 创建SQLite数据库文件（如果使用SQLite）
- 初始化所有数据表
- 插入示例数据（祝福模板、工具模板等）

#### 4. 启动后端服务

```bash
python -m app.main
```

或者使用uvicorn直接运行：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

后端服务将在 `http://localhost:8003` 启动

### 前端启动

#### 1. 安装前端依赖

```bash
cd frontend
npm install
```

#### 2. 启动开发服务器

```bash
npm run dev
```

前端服务将在 `http://localhost:5174` 启动（如果端口被占用，Vite会自动尝试其他端口）

### 访问应用

打开浏览器访问：http://localhost:5174

## API文档

后端启动后，可以通过以下地址访问交互式API文档：

- **Swagger UI**：http://localhost:8003/docs
- **ReDoc**：http://localhost:8003/redoc

## API端点说明

### 认证接口

#### POST /api/auth/login
用户登录

**请求体**：
```json
{
  "phone": "13800138000",
  "openid": null
}
```

**响应**：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "1380****8000",
    "membership_type": "free",
    "is_active": true
  }
}
```

#### POST /api/auth/register
用户注册

#### GET /api/auth/me
获取当前用户信息（需要认证）

### 对话接口

#### POST /api/conversations
创建新对话

**请求头**：
```
Authorization: Bearer {access_token}
```

**请求体**：
```json
{
  "title": "给长辈的祝福"
}
```

#### POST /api/conversations/{conversation_id}/messages
发送消息

**请求体**：
```json
{
  "content": "帮我生成给长辈的拜年文案"
}
```

### 祝福生成接口

#### POST /api/greeting/generate
生成祝福文案

**请求体**：
```json
{
  "target_group": "elder",
  "style": "formal",
  "format_type": "long",
  "keywords": ["健康", "平安"],
  "count": 3
}
```

#### POST /api/greeting/optimize
优化文案

**请求体**：
```json
{
  "content": "祝您新年快乐",
  "target_style": "warm",
  "length_adjust": "long"
}
```

### 实用工具接口

#### POST /api/tools/custom
查询春节习俗

**请求体**：
```json
{
  "question": "除夕有什么习俗？",
  "region": null
}
```

#### POST /api/tools/gift
推荐礼物

**请求体**：
```json
{
  "target_group": "elder",
  "budget": "500-1000"
}
```

#### POST /api/tools/red_packet
红包金额建议

**请求体**：
```json
{
  "amount_type": "lucky",
  "relationship": "friend"
}
```

#### POST /api/tools/menu
年夜饭菜单推荐

**请求体**：
```json
{
  "people_count": 6
}
```



## 配置说明

### 数据库配置

项目默认使用SQLite数据库，无需额外配置。如需切换到MySQL：

1. 安装PyMySQL：`pip install pymysql`
2. 修改 `.env` 文件中的 `DATABASE_URL`：
   ```
   DATABASE_URL=mysql+pymysql://username:password@localhost:3306/database_name
   ```
3. 创建MySQL数据库：
   ```sql
   CREATE DATABASE newyear_greeting DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

### AI服务配置

项目支持两种模式：

1. **使用OpenAI API**：配置 `AI_API_KEY` 环境变量
2. **使用模拟响应**：不配置 `AI_API_KEY`，系统使用预设回复

### 用户限制配置

在 `.env` 文件中配置：

```env
FREE_USER_DAILY_LIMIT=50  # 免费用户每日请求次数
VIP_USER_DAILY_LIMIT=-1   # VIP用户请求次数（-1表示无限制）
```

## 常见问题

### 1. 端口被占用怎么办？

后端默认端口是8003，前端默认端口是5174。如果端口被占用：

- 后端：修改启动命令中的 `--port` 参数
- 前端：修改 `vite.config.js` 中的 `server.port` 配置

### 2. 如何切换到MySQL数据库？

参考上文"数据库配置"部分

### 3. AI回复不正确怎么办？

- 确保已正确配置 `AI_API_KEY`
- 检查网络连接
- 如果API调用失败，系统会自动使用模拟响应

### 4. 如何重置数据库？

删除 `backend/newyear_greeting.db` 文件，然后重新运行 `python init_db.py`

## 技术支持

- 查看后端日志：终端输出
- 查看前端日志：浏览器开发者工具控制台
- API文档：http://localhost:8003/docs

## 许可证

MIT License
