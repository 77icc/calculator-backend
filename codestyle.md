# 后端代码规范 (codestyle.md)

本仓库 Python 代码遵循以下规范，提交前请对照自查。

## 一、规范来源

1. **PEP 8** — Python 官方代码风格指南
   https://peps.python.org/pep-0008/

2. **PEP 257** — Docstring 规范
   https://peps.python.org/pep-0257/

3. **The Zen of Python (PEP 20)** — Python 设计哲学
   https://peps.python.org/pep-0020/

## 二、关键约定摘要

### 1. 命名

| 类型     | 风格            | 示例             |
| -------- | --------------- | ---------------- |
| 模块、函数、变量 | snake_case      | `insert_history`|
| 类       | PascalCase      | `ExpressionError`|
| 常量     | UPPER_SNAKE     | `DB_PATH`        |
| 私有     | 单下划线前缀    | `_eval(node)`    |

### 2. 排版

- 缩进：4 个空格，禁止 Tab。
- 行宽：≤ 99 字符。
- import 顺序：标准库 → 第三方库 → 本项目模块，组间空行。
- 函数/类之间空两行；方法之间空一行。

### 3. 字符串与格式化

- 统一使用双引号 `"`。
- 优先使用 f-string，避免 `%` 和 `str.format` 拼接。

### 4. 类型注解

- 公开函数应标注参数与返回类型：
  ```python
  def evaluate(expression: str) -> float: ...
  ```

### 5. 异常

- 不使用裸 `except:`，至少 `except Exception:`。
- 业务异常自定义类（如 `ExpressionError`），便于上层捕获。
- 非业务必要不吞异常，必须捕获时记录上下文。

### 6. 文档字符串

- 模块、类、公开函数必须有 docstring，说明用途、参数、返回值。

### 7. 安全

- 严禁 `eval()` / `exec()` 处理用户输入。
- SQL 必须使用参数化查询（`?` 占位符），禁止字符串拼接。

## 三、自查工具

- `ruff check .` — 静态检查（PEP 8 + 常见错误）
- `black .` — 自动格式化
- `pytest -q` — 运行单元测试

## 四、Git 提交规范

- 提交信息格式：`<type>: <description>`
- type ∈ feat / fix / docs / refactor / test / chore
- 示例：`feat: 实现表达式 ast 白名单解析器`
