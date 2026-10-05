"""API 路由定义。

三个接口：
    POST   /api/calculate      提交表达式计算
    GET    /api/history        获取历史记录列表
    DELETE /api/history/{id}   删除单条历史记录
"""
from fastapi import APIRouter, HTTPException

from app.database import delete_history, insert_history, list_history
from app.evaluator import ExpressionError, evaluate, format_result
from app.models import (
    CalculateRequest,
    CalculateResponse,
    DeleteResponse,
    HistoryResponse,
)

router = APIRouter()


@router.post("/calculate", response_model=CalculateResponse)
def calculate(req: CalculateRequest) -> CalculateResponse:
    """接收表达式 -> 后端计算 -> 存库 -> 返回结果。"""
    try:
        value = evaluate(req.expression)
        result_str = format_result(value)
    except ExpressionError as e:
        # 非法表达式不存库，仅返回错误信息
        return CalculateResponse(success=False, message=str(e))

    hid = insert_history(req.expression, result_str)
    return CalculateResponse(
        success=True,
        expression=req.expression,
        result=result_str,
        id=hid,
    )


@router.get("/history", response_model=HistoryResponse)
def get_history() -> HistoryResponse:
    """返回全部历史记录（按时间倒序）。"""
    rows = list_history()
    return HistoryResponse(success=True, data=rows)


@router.delete("/history/{hid}", response_model=DeleteResponse)
def remove_history(hid: int) -> DeleteResponse:
    """按 id 删除单条历史记录。"""
    if hid <= 0:
        raise HTTPException(status_code=400, detail="非法的记录 id")
    ok = delete_history(hid)
    if not ok:
        raise HTTPException(status_code=404, detail="记录不存在或已删除")
    return DeleteResponse(success=True, message="已删除")
