"""FastAPI 计算器后端入口。

启动方式：
    本地开发： uvicorn main:app --reload
    生产部署： uvicorn main:app --host 0.0.0.0 --port $PORT
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import routes
from app.database import init_db

app = FastAPI(
    title="Calculator Backend API",
    description="前后端分离计算器 - 后端服务",
    version="1.0.0",
)

# 允许前端跨域访问。作业演示期间允许任意源；生产环境应限定为前端域名。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _on_startup() -> None:
    """应用启动时初始化数据库表。"""
    init_db()


@app.get("/")
def root():
    return {"service": "calculator-backend", "status": "ok"}


app.include_router(routes.router, prefix="/api")
