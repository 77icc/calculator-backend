"""Flask 路由定义。

三个接口：
    POST   /api/calculate      提交表达式计算
    GET    /api/history        获取历史记录列表
    DELETE /api/history/<id>   删除单条历史记录
"""
from flask import Blueprint, jsonify, request

from app.database import delete_history, insert_history, list_history
from app.evaluator import ExpressionError, evaluate, format_result

bp = Blueprint("api", __name__)


@bp.post("/calculate")
def calculate():
    """接收表达式 -> 后端计算 -> 存库 -> 返回结果。"""
    body = request.get_json(silent=True) or {}
    expression = body.get("expression", "")

    try:
        value = evaluate(expression)
        result_str = format_result(value)
    except ExpressionError as e:
        return jsonify(success=False, message=str(e)), 200

    hid = insert_history(expression, result_str)
    return jsonify(
        success=True,
        expression=expression,
        result=result_str,
        id=hid,
    ), 200


@bp.get("/history")
def get_history():
    """返回全部历史记录（按时间倒序）。"""
    rows = list_history()
    return jsonify(success=True, data=rows), 200


@bp.delete("/history/<int:hid>")
def remove_history(hid: int):
    """按 id 删除单条历史记录。"""
    if hid <= 0:
        return jsonify(success=False, message="非法的记录 id"), 400
    ok = delete_history(hid)
    if not ok:
        return jsonify(success=False, message="记录不存在或已删除"), 404
    return jsonify(success=True, message="已删除"), 200
