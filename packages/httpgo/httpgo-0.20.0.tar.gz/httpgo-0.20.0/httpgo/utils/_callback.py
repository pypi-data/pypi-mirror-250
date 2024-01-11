import json
import typer
from ..__version__ import package_version, package_name
from ..utils._exception import FormatError


def process_list_data(value: list) -> dict:
    """处理列表"""
    try:
        list_to_dict = dict(map(lambda item: item.split("="), value))
        return list_to_dict
    except ValueError:
        raise FormatError


# def process_json_data(value: str) -> str:
#     """处理json"""
#     # 如果字符串以单引号或双引号包裹，则去掉外围的引号
#     try:
#         if value.startswith("'") and value.endswith("'"):
#             value = value[1:-1]
#         elif value.startswith('"') and value.endswith('"'):
#             value = value[1:-1]
#     # 如果json为空，就返回空对象
#     except AttributeError:
#         return None
#     # 将单引号替换为双引号
#     value_with_double_quotes = value.replace("'", '"')
#     # 解析为 Python 对象
#     return json.loads(value_with_double_quotes)


def version_callback(value: bool):
    """--version 回调函数

    Args:
        value (bool): _description_

    Raises:
        typer.Exit: _description_
    """
    if value:
        print(f"{package_name} Version: {package_version}")
        raise typer.Exit()
