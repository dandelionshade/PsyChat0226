# PsyChat - 项目概览

> 本文档提供项目的整体架构和技术设计，包含静态信息。开发进度请参阅 `DEVELOPMENT_PROGRESS.md`，开发日志请参阅 `DEVELOPMENT_LOG.md`。

## 项目简介

PsyChat是一个基于FastAPI和Vue.js开发的心理咨询聊天应用，旨在提供用户友好的心理健康支持平台。
项目采用前后端分离架构，后端使用Python FastAPI框架，前端使用Vue.js框架。

## 技术栈

### 后端
- **框架**: FastAPI (Python)
- **数据库**: 
  - 主数据库: MySQL (选择原因：简单易用，成熟稳定，社区支持强大，性能足够支撑文字聊天交互功能)
  - 缓存数据库: Redis (用途：存储会话信息，实现API限流，缓存常用数据；缓存策略：allkeys-lru)
- **ORM**: SQLModel (基于SQLAlchemy和Pydantic，与FastAPI完美集成)
- **认证**: JWT (python-jose)
- **密码哈希**: passlib (bcrypt)
- **数据库迁移**: Alembic
- **其他依赖**:
  - uvicorn (ASGI服务器)
  - pydantic (数据验证)
  - python-multipart (文件上传)
  - email-validator (邮箱验证)
  - requests (HTTP客户端)

### 前端
- **框架**: Vue.js 3
- **HTTP客户端**: axios
- **路由**: vue-router v4
- **状态管理**: vuex
- **UI库**: Element Plus
- **构建工具**: Vite
- **CSS预处理**: Sass
- **代码检查**: ESLint
- **代码格式化**: Prettier

## 项目结构

```
PsyChat0226/
├── front-end/              # Vue.js前端
│   ├── public/             # 静态资源
│   ├── src/                # 源代码
│   │   ├── assets/         # 资源文件
│   │   ├── components/     # Vue组件
│   │   ├── views/          # Vue视图/页面
│   │   ├── utils/          # 工具函数
│   │   ├── App.vue         # 主应用组件
│   │   └── main.js         # 应用入口
│   ├── package.json        # NPM依赖和脚本
│   └── vite.config.js      # Vite配置
│
├── back-end/               # FastAPI后端
│   ├── app/                # 应用代码
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # 数据验证模式
│   │   ├── tests/          # 测试代码
│   │   └── main.py         # 应用入口
│   ├── migrations/         # 数据库迁移
│   ├── Dockerfile          # Docker配置
│   ├── alembic.ini         # Alembic配置
│   └── requirements.txt    # Python依赖
```

## API端点参考

### 用户认证
- `POST /api/register` - 注册新用户
- `POST /api/login` - 用户登录
- `GET /api/me` - 获取当前用户信息
- `PUT /api/me` - 更新当前用户信息

### 聊天功能
- `POST /api/chat/send` - 发送消息
- `GET /api/chat/history` - 获取聊天历史
- `GET /api/chat/history/{chat_id}` - 获取特定聊天记录
- `DELETE /api/chat/history/{chat_id}` - 删除聊天记录

### 资源导航
- `GET /api/navigation/{navigation_id}` - 获取特定导航资源
- `PUT /api/navigation/{navigation_id}` - 更新导航资源
- `DELETE /api/navigation/{navigation_id}` - 删除导航资源
- `POST /api/navigation/` - 创建导航资源
- `GET /api/navigation/` - 获取导航资源列表

## 数据库结构

### users表
```sql
id: INT AUTO_INCREMENT PRIMARY KEY
username: VARCHAR(255) UNIQUE NOT NULL
password_hash: VARCHAR(255) NOT NULL
role: ENUM('user', 'admin') DEFAULT 'user'
created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### navigation表
```sql
id: INT AUTO_INCREMENT PRIMARY KEY
title: VARCHAR(255) NOT NULL
description: TEXT
url: VARCHAR(2048)
created_by: INT  -- 关联用户表id
```

### chat_logs表
```sql
id: INT AUTO_INCREMENT PRIMARY KEY
user_id: INT  -- 关联用户表id
message: TEXT
response: TEXT
timestamp: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### logs表
```sql
id: INT AUTO_INCREMENT PRIMARY KEY
user_id: INT  -- 关联用户表id
action: VARCHAR(255)
timestamp: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### recommendations表
```sql
id: INT AUTO_INCREMENT PRIMARY KEY
user_id: INT  -- 关联用户表id
content_id: INT  -- 关联导航内容表id
timestamp: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

## 本地开发指南

### 后端
```bash
cd back-end
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 前端
```bash
cd front-end
npm install
npm run dev
```

### API文档
启动后端后访问:
- Swagger文档: `http://localhost:8000/docs`
- ReDoc文档: `http://localhost:8000/redoc`

## 相关文档

- [`DEVELOPMENT_PROGRESS.md`](./DEVELOPMENT_PROGRESS.md): 开发进度与路线图，包含已完成和计划功能
- [`DEVELOPMENT_LOG.md`](./DEVELOPMENT_LOG.md): 开发日志，记录技术决策和实现细节
