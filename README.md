# Calculator Backend

前后端分离计算器系统的**后端服务**，基于 FastAPI + SQLite 实现。

> 配套前端仓库请见博客或仓库主页链接。

## 一、项目介绍

提供计算器后端能力：

- 接收前端提交的表达式字符串

- 后端完成表达式解析与计算（**不使用** **`eval`/`exec`**，基于 `ast` 模块白名单求值）

- 计算结果持久化保存到 SQLite 数据库

- 提供历史记录查询、删除接口

## 二、技术栈

| 组件     | 选型                      |
| ------ | ----------------------- |
| Web 框架 | FastAPI 0.110           |
| ASGI   | Uvicorn 0.27            |
| 数据库    | SQLite 3（标准库 `sqlite3`） |
| 数据校验   | Pydantic 2.6            |
| 解析器    | Python `ast` 标准库        |
| 语言     | Python 3.10+            |

## 三、环境要求

- Python ≥ 3.10

- pip ≥ 21

- （可选）虚拟环境：venv / conda

## 四、本地开发

```bash
# 1. 进入项目根目录
cd calculator-backend

# 2. 创建并激活虚拟环境（推荐）
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动开发服务器（自动热重载）
uvicorn main:app --reload

# 5. 浏览器访问
#    接口文档（Swagger UI）： http://127.0.0.1:8000/docs
#    健康检查：                http://127.0.0.1:8000/
#    历史记录：                http://127.0.0.1:8000/api/history
```

数据库文件首次启动时自动创建于 `data/calculator.db`，无需手动初始化。

## 五、数据库初始化

SQLite 表会在应用启动时自动创建（见 `app/database.py` 的 `init_db`）。

如需手动重置本地数据，删除 `data/calculator.db` 文件后重启服务即可。

表结构：

| 字段          | 类型      | 说明                |
| ----------- | ------- | ----------------- |
| id          | INTEGER | 主键，自增             |
| expression  | TEXT    | 表达式字符串            |
| result      | TEXT    | 计算结果（字符串形式）       |
| created\_at | TEXT    | 计算时间（UTC ISO8601） |

## 六、API 接口说明

统一返回 JSON，成功 `success: true`，失败 `success: false` 并携带 `message`。

### 1. POST `/api/calculate` 提交表达式计算

请求体：

```json
{ "expression": "1+2*3" }
```

成功响应（200）：

```json
{
  "success": true,
  "expression": "1+2*3",
  "result": "7",
  "id": 1
}
```

失败响应（200，业务错误）：

```json
{ "success": false, "message": "除零错误：除数不能为 0" }
```

### 2. GET `/api/history` 获取历史记录

响应（200）：

```json
{
  "success": true,
  "data": [
    {
      "id": 2,
      "expression": "(1+2)*3",
      "result": "9",
      "created_at": "2026-10-03T10:00:00+00:00"
    }
  ]
}
```

按时间倒序返回，最多 100 条。

### 3. DELETE `/api/history/{id}` 删除单条记录

成功响应（200）：

```json
{ "success": true, "message": "已删除" }
```

记录不存在（404）：

```json
{ "detail": "记录不存在或已删除" }
```

## 七、前后端对接

1. 启动后端后，默认监听 `http://127.0.0.1:8000`。
2. 前端通过 `fetch` 调用上述三个接口。
3. 后端已开启 CORS，允许任意源访问（演示用）。
4. 前端把表达式以 `*` `/` 形式传输，UI 上显示 `×` `÷` 由前端负责转换。

## 八、部署

本项目部署在 [Render](https://render.com)，使用 `render.yaml` 一键配置：

- Web Service（Python 环境）

- 持久化磁盘 1GB（挂载到 `data/` 目录，保存 SQLite 数据库文件）

部署步骤见博客部署章节。

## 九、目录结构

```
calculator-backend/
├── app/
│   ├── __init__.py
│   ├── database.py     # SQLite 数据访问层
│   ├── evaluator.py    # ast 白名单表达式解析器
│   ├── models.py       # Pydantic 数据模型
│   └── routes.py       # API 路由
├── data/               # SQLite 数据库文件（运行时生成）
├── main.py             # FastAPI 入口
├── requirements.txt
├── Procfile            # 兼容 Heroku/Render 启动命令
├── render.yaml         # Render Blueprint 配置
├── codestyle.md
├── README.md
└── .gitignore
```

