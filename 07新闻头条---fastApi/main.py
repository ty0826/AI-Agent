from fastapi import FastAPI
from routers.news import router_news
from routers.users import router_user
from routers.chatAi import router_chatAI
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handler import register_exception_handler
from utils.auth import register_auth_middleware
app = FastAPI()
register_exception_handler(app)
# 先注册鉴权中间件，再注册 CORS，保证 CORS 在最外层，401 响应也带跨域头
register_auth_middleware(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许访问的源
    allow_credentials=True,  # 运行携带cookie
    allow_methods=["*"],  # 允许的方法
    allow_headers=["*"],  # 允许的请求头
)
app.include_router(router_news)
app.include_router(router_user)
app.include_router(router_chatAI)
