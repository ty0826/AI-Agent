from fastapi import FastAPI
from routers.news import router_news
from routers.users import router_user
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handlers import register_exception_handlers

app = FastAPI()
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许访问的源
    allow_credentials=True,  # 运行携带cookie
    allow_methods=["*"],  # 允许的方法
    allow_headers=["*"],  # 允许的请求头
)
app.include_router(router_news)
app.include_router(router_user)
