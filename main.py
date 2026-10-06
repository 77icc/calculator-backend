"""Flask 计算器后端入口。

启动方式：
    本地开发： python main.py
    生产部署： PythonAnywhere WSGI 加载 application 对象
"""
from flask import Flask
from flask_cors import CORS

from app import routes
from app.database import init_db

app = Flask(__name__)
CORS(app)  # 允许跨域，演示期开放所有源

# 启动时初始化数据库表
init_db()

app.register_blueprint(routes.bp, url_prefix="/api")


@app.route("/")
def root():
    return {"service": "calculator-backend", "status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


# PythonAnywhere WSGI 需要的变量名
application = app
