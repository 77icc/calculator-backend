"""Pydantic 数据模型，统一接口出入参结构。

所有接口返回 JSON，并统一包含 success 字段：
    成功 success=True，可能携带 data / result 等
    失败 success=False，携带 message 说明错误
"""
from typing import List, Optional

from pydantic import BaseModel, Field


class CalculateRequest(BaseModel):
    """计算接口入参。"""
    expression: str = Field(..., description="待计算的表达式字符串")


class CalculateResponse(BaseModel):
    """计算接口返回。"""
    success: bool
    expression: Optional[str] = None
    result: Optional[str] = None
    id: Optional[int] = None
    message: Optional[str] = None


class HistoryItem(BaseModel):
    """单条历史记录。"""
    id: int
    expression: str
    result: str
    created_at: str


class HistoryResponse(BaseModel):
    """历史列表接口返回。"""
    success: bool
    data: List[HistoryItem] = []
    message: Optional[str] = None


class DeleteResponse(BaseModel):
    """删除接口返回。"""
    success: bool
    message: Optional[str] = None
