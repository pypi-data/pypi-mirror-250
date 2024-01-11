import re, ast, typer
from click import ParamType
from rich import print
from ._exception import UrlVerifyError

# from pydantic import HttpUrl, validate_arguments


# @validate_arguments
# def url(value: HttpUrl) -> HttpUrl:
#     """自定义Url类型提示,
#        使用pydantic对入参进行验证

#     Args:
#         value (HttpUrl): 控制台入参


#     Returns:
#         HttpUrl: 校验后直接return
#     """
#     return value
class UrlType(ParamType):
    """URL类型提示"""

    name = "URL"

    # def url_check(self, url: str):
    #     """基本的检查url格式

    #     Args:
    #         url (str): URL

    #     Raises:
    #         UrlVerifyError: _description_

    #     Returns:
    #         _type_: _description_
    #     """
    #     url_pattern = re.compile(
    #         r"^(https?|ftp)://"  # 协议部分，支持 http、https、ftp
    #         r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # 域名部分
    #         r"localhost|"  # localhost
    #         r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # IP 地址
    #         r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # IPv6 地址
    #         r"(?::\d+)?"  # 端口部分
    #         r"(?:/?|[/?]\S+)$",  # 路径和查询字符串部分
    #         re.IGNORECASE,
    #     )
    #     if url_pattern.match(url):
    #         return url
    #     else:
    #         raise UrlVerifyError

    def convert(self, value, param, ctx):
        # try:
        #     return self.url_check(value)
        # except UrlVerifyError as e:
        #     print("[bold red]Error:[/bold red]", e)
        #     raise typer.Exit()
        return value


class NameValueType(ParamType):
    """键值类型提示"""

    name = "<NAME VALUE>"

    def convert(self, value, param, ctx):
        return value


class JsonType(ParamType):
    """JSON类型提示并解析"""

    name = "JSON"

    def parse_powershell_input(self, key_value: tuple):
        """对powershell输入进行操作

        Args:
            key_value (tuple): k,v元组

        Returns:
            _type_: _description_
        """
        key, value = key_value
        return (
            key,
            str(value) if isinstance(value, int) or isinstance(value, float) else value,
        )

    def convert(self, value, param, ctx):
        try:
            # 使用 ast.literal_eval 将字符串转换为字典
            dict_data = ast.literal_eval(value)
        except Exception:
            # 使用正则表达式提取键值对
            pattern = re.compile(r"{\s*([^:{}]+)\s*:\s*([^{}]+)\s*}")
            matches = pattern.findall(value)
            # 进行解析
            dict_data = dict(map(self.parse_powershell_input, matches))
        return dict_data
