# PsyChat 开发日志

## 项目概述

PsyChat是一个基于FastAPI和Vue.js开发的心理咨询聊天应用，旨在提供用户友好的心理健康支持平台。项目采用前后端分离架构，后端使用Python FastAPI框架，前端使用Vue.js框架。

## 开发时间线

### 阶段一：数据库设计与实现 (2024-02-26)

#### 1. 技术选型

##### 1.1 主数据库：MySQL
- 选择原因：
  - 简单易用，上手快
  - 成熟稳定，社区支持强大
  - 性能足够支撑文字聊天交互功能
  - 生态系统完善，有多种ORM工具可选

##### 1.2 缓存数据库：Redis
- 主要用途：
  - 存储会话信息
  - 实现API限流
  - 缓存常用数据
- 缓存策略：allkeys-lru

##### 1.3 ORM工具：SQLModel
- 基于SQLAlchemy和Pydantic
- 与FastAPI完美集成
- 支持多种数据库

#### 2. 数据库表结构设计

##### 2.1 用户表 (users)
```sql
id: INT AUTO_INCREMENT PRIMARY KEY
username: VARCHAR(255) UNIQUE NOT NULL
password_hash: VARCHAR(255) NOT NULL
role: ENUM('user', 'admin') DEFAULT 'user'
created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

##### 2.2 导航内容表 (navigation)
```sql
id: INT AUTO_INCREMENT PRIMARY KEY
title: VARCHAR(255) NOT NULL
description: TEXT
url: VARCHAR(2048)
created_by: INT  -- 关联用户表id
```

##### 2.3 聊天记录表 (chat_logs)
```sql
id: INT AUTO_INCREMENT PRIMARY KEY
user_id: INT  -- 关联用户表id
message: TEXT
response: TEXT
timestamp: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

##### 2.4 日志表 (logs)
```sql
id: INT AUTO_INCREMENT PRIMARY KEY
user_id: INT  -- 关联用户表id
action: VARCHAR(255)
timestamp: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

##### 2.5 推荐记录表 (recommendations)
```sql
id: INT AUTO_INCREMENT PRIMARY KEY
user_id: INT  -- 关联用户表id
content_id: INT  -- 关联导航内容表id
timestamp: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

#### 3. 已完成工作

1. 创建了数据库模型文件 `app/models/models.py`
   - 使用SQLModel定义了所有数据表结构
   - 实现了表之间的关系映射
   - 添加了必要的字段验证和索引

2. 创建了数据库配置文件 `app/core/config.py`
   - 配置了MySQL连接参数
   - 设置了Redis缓存配置
   - 添加了安全相关配置
   - 实现了CORS配置

#### 4. 待完成工作

1. 数据库迁移
   - 创建迁移脚本
   - 实现数据库版本控制

2. API实现
   - 用户认证和授权
   - CRUD操作接口
   - 聊天功能接口
   - 推荐系统接口

3. 缓存实现
   - 会话管理
   - 接口限流
   - 数据缓存

4. 测试
   - 单元测试
   - 集成测试
   - 性能测试

### 阶段二：MVP开发计划 (Minimum Viable Product)

#### 1. 后端API开发

1. 在后端项目目录下创建FastAPI应用代码文件 `app/main.py`，实现MVP核心功能：
   - 用户认证API
   - 聊天功能API
   - 导航内容API

2. 使用Swagger文档接口工具（FastAPI默认集成）进行API测试

3. 编写后端单元测试（使用pytest），确保API功能正常运行

4. 代码提交规范：完成一部分API功能后，及时提交代码到本地仓库

#### 2. 前端基础页面搭建

1. 在Vue.js项目中创建路由和基础页面组件：
   - 登录/注册页面
   - 聊天主界面
   - 导航内容展示页面
   - 用户设置页面

2. 搭建页面框架，用于展示数据

3. 代码提交规范：完成前端页面搭建后，及时提交代码

#### 3. 基础功能交互实现 (CRUD)

##### 3.1 后端开发
- 完善后端API，实现完整的CRUD操作
- 确保API接口与前端页面所需的数据格式一致
- 编写更完善的单元测试

##### 3.2 前端开发
- 使用axios等工具调用后端API
- 实现页面的数据交互和CRUD功能
- 添加基本的表单验证和错误处理

##### 3.3 开发规范
- 前后端同步开发
- 频繁提交和推送：每完成一个小的功能模块或修复一个Bug，及时提交代码并推送到GitHub仓库

### 阶段三：优化阶段

#### 1. 性能优化
- 后端API优化：使用缓存、优化数据库查询、代码优化
- 前端性能优化：减少不必要的渲染、优化资源加载

#### 2. 安全性增强
- 完善身份验证和授权机制
- 防止SQL注入、XSS攻击等安全措施
- 实现数据加密和敏感信息保护

#### 3. 用户体验优化
- 改进页面布局和设计
- 添加交互动画和过渡效果
- 优化错误处理和用户反馈机制
- 实现响应式设计，适配不同设备

#### 4. 持续集成/持续部署 (CI/CD)
- 配置CI/CD流程
- 实现代码自动化测试、构建和部署
- 监控系统性能和错误日志

#### 5. 开发规范
- 持续提交和推送代码
- 记录每次优化的内容和效果
- 定期代码审查和重构

## 项目结构

```
PsyChat/
├── back-end/                # 后端项目目录
│   ├── app/                 # 应用代码
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # 数据验证模式
│   │   ├── tests/          # 测试代码
│   │   └── main.py         # 应用入口
│   ├── Dockerfile          # Docker配置
│   └── requirements.txt     # 依赖管理
│
└── front-end/              # 前端项目目录
    ├── public/             # 静态资源
    ├── src/                # 源代码
    │   ├── assets/         # 资源文件
    │   ├── components/     # 组件
    │   ├── App.vue         # 主应用组件
    │   └── main.js         # 入口文件
    ├── package.json        # 依赖管理
    └── vue.config.js       # Vue配置
```

## 技术栈

### 后端
- 语言：Python
- 框架：FastAPI
- 数据库：MySQL, Redis
- ORM：SQLModel
- 测试：pytest

### 前端
- 语言：JavaScript
- 框架：Vue.js
- UI库：待定
- HTTP客户端：axios
- 构建工具：Vue CLI