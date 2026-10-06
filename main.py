"""Flask 计算器后端入口。

启动方式：
    本地开发： python main.py
    生产部署： PythonAnywhere WSGI 加载 application 对象

同一个 Flask 应用同时提供：
    - /api/*          计算器 API（表达式计算、历史记录增删查）
    - /, /style.css, /script.js   前端静态页面（托管在另一个独立仓库）
"""
import os
from pathlib import Path

from flask import Flask, send_from_directory
from flask_cors import CORS

from app import routes
from app.database import init_db

app = Flask(__name__)
CORS(app)  # 允许跨域，演示期开放所有源

# 启动时初始化数据库表
init_db()

app.register_blueprint(routes.bp, url_prefix="/api")

# 前端静态文件目录。
# - 生产（PythonAnywhere）：/home/77icc/calculator-frontend
# - 本地开发：同项目目录的 ../calculator-frontend
_FRONTEND_DIR = Path(
    os.environ.get(
        "FRONTEND_DIR",
        str(Path(__file__).resolve().parent.parent / "calculator-frontend"),
    )
)


@app.route("/")
def index():
    """前端首页。"""
    return send_from_directory(str(_FRONTEND_DIR), "index.html")


@app.route("/style.css")
def style():
    return send_from_directory(str(_FRONTEND_DIR), "style.css")


@app.route("/script.js")
def script():
    return send_from_directory(str(_FRONTEND_DIR), "script.js")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


# PythonAnywhere WSGI 需要的变量名
application = app
