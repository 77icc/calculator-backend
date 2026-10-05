"""基于 ast 模块的安全表达式求值器。

实现思路：
    1. 用 `ast.parse(expression, mode='eval')` 把表达式解析为 AST；
    2. 递归遍历 AST 节点，只允许以下类型：
        - Expression        顶层包装
        - BinOp             二元运算 + - * /
        - UnaryOp           一元正负号 +x / -x
        - Constant          数字字面量（int / float）
       其余节点（函数调用、属性访问、变量名等）一律抛错。
    3. 运算通过 operator 模块完成，绝不调用 eval/exec。

这样既支持运算符优先级、括号、负数和小数，又能彻底阻断任意代码执行。
"""
import ast
import operator as _op


class ExpressionError(Exception):
    """非法表达式或运算过程中的错误。"""


_BIN_OPS = {
    ast.Add: _op.add,
    ast.Sub: _op.sub,
    ast.Mult: _op.mul,
    ast.Div: _op.truediv,
}

_UNARY_OPS = {
    ast.UAdd: _op.pos,
    ast.USub: _op.neg,
}


def _eval(node) -> float | int:
    """递归求值，遇到不允许的节点立刻报错。"""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise ExpressionError(f"不支持的运算符: {op_type.__name__}")
        left = _eval(node.left)
        right = _eval(node.right)
        try:
            return _BIN_OPS[op_type](left, right)
        except ZeroDivisionError:
            raise ExpressionError("除零错误：除数不能为 0")

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ExpressionError(f"不支持的一元运算符: {op_type.__name__}")
        return _UNARY_OPS[op_type](_eval(node.operand))

    # Python 3.8+ 用 Constant
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):  # bool 是 int 的子类，需排除
            raise ExpressionError("不支持的表达式元素: 布尔常量")
        if isinstance(node.value, (int, float)):
            return node.value
        raise ExpressionError(f"不支持的常量类型: {type(node.value).__name__}")

    raise ExpressionError(f"不支持的表达式元素: {type(node).__name__}")


def evaluate(expression: str):
    """对外接口：传入表达式字符串，返回数值结果。

    任何非法输入都会抛出 ExpressionError，由调用方捕获。
    """
    if expression is None or not expression.strip():
        raise ExpressionError("表达式不能为空")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as e:
        raise ExpressionError(f"表达式语法错误: {e.msg}") from None

    return _eval(tree)


def format_result(value) -> str:
    """把数值格式化为展示用字符串。

    - 整数结果去掉小数尾零；
    - 浮点结果四舍五入到 10 位小数，避免 0.1+0.2 这类尾数。
    """
    if isinstance(value, bool):
        raise ExpressionError("非法结果")
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return str(round(value, 10))
    return str(value)
