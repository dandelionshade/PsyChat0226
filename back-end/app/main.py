from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入API路由模块
from .api import users, chat, navigation

app = FastAPI(
    title="PsyChat API",
    description="PsyChat backend API service",
    version="0.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to PsyChat API"}

if __name__ == "__main__":
    import uvicorn
    
    
    # 注册API路由
    app.include_router(users.router, prefix="/api", tags=["users"])
    app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
    app.include_router(navigation.router, prefix="/api/navigation", tags=["navigation"])
    
