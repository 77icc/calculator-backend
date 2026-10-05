"""SQLite 数据库访问层。

历史记录表结构：
    id          主键自增
    expression  表达式字符串
    result      计算结果（字符串形式，保留小数）
    created_at  计算时间（UTC ISO8601）

数据库文件路径优先取自环境变量 DB_PATH，便于在 Render 持久化磁盘上保存。
"""
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

# 默认数据库文件位于项目根目录的 data/ 子目录下
_DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "calculator.db"
DB_PATH = Path(os.environ.get("DB_PATH", str(_DEFAULT_DB_PATH)))


def _connect() -> sqlite3.Connection:
    """打开数据库连接，并确保目录存在。"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """首次启动时建表。"""
    conn = _connect()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                expression  TEXT    NOT NULL,
                result      TEXT    NOT NULL,
                created_at  TEXT    NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def insert_history(expression: str, result: str) -> int:
    """插入一条历史记录，返回新记录的主键 id。"""
    now = datetime.now(timezone.utc).isoformat()
    conn = _connect()
    try:
        cur = conn.execute(
            "INSERT INTO history (expression, result, created_at) VALUES (?, ?, ?)",
            (expression, result, now),
        )
        conn.commit()
        return int(cur.lastrowid)
    finally:
        conn.close()


def list_history(limit: int = 100) -> list[dict]:
    """按时间倒序返回历史记录列表。"""
    conn = _connect()
    try:
        rows = conn.execute(
            "SELECT id, expression, result, created_at "
            "FROM history ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def delete_history(hid: int) -> bool:
    """按主键删除一条记录，返回是否成功删除。"""
    conn = _connect()
    try:
        cur = conn.execute("DELETE FROM history WHERE id = ?", (hid,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()
