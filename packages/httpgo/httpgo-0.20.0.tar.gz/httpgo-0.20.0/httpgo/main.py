import requests
import typer
import time
from typing import List
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from json.decoder import JSONDecodeError
from .utils._callback import process_list_data, version_callback
from .utils._enum import HttpMethod
from .utils._type import UrlType, NameValueType, JsonType


app = typer.Typer(add_completion=False)


@app.command()
def main(
    url: str = typer.Argument(
        help="目标URL",
        show_default=False,
        click_type=UrlType(),
    ),
    method: HttpMethod = typer.Option(
        "GET",
        "--method",
        "-m",
        help="请求方法.",
    ),
    params: List[str] = typer.Option(
        None,
        "--params",
        "-p",
        help="请求（查询）参数,可以有多个参数.example: -p page=2 -p limit=30",
        show_default=False,
        click_type=NameValueType(),
    ),
    data: List[str] = typer.Option(
        None,
        "--data",
        "-d",
        help="请求体Form数据,可以有多个参数.example: -d name=admin",
        show_default=False,
        click_type=NameValueType(),
    ),
    json: str = typer.Option(
        None,
        "--json",
        "-j",
        help='请求体使用JSON数据.example: -j \'{"name":"admin"}\'',
        show_default=False,
        click_type=JsonType(),
    ),
    headers: str = typer.Option(
        None,
        "--headers",
        "-h",
        help="设置请求头.example: -h \"{'Content-Type':'application/json'}\"",
        show_default=False,
        click_type=JsonType(),
    ),
    timeout: float = typer.Option(
        None,
        "--timeout",
        "-t",
        help="超时时间,单位秒(s).example: -t 3.2",
        show_default=False,
    ),
    cookies: str = typer.Option(
        None,
        "--cookies",
        help="cookie包含在请求中.example: --cookies \"{'your cookie name':'your cookies'}\"",
        show_default=False,
        click_type=JsonType(),
    ),
    proxies: str = typer.Option(
        None,
        "--proxies",
        "-P",
        help="设置代理请求服务器.",
        show_default=False,
        click_type=UrlType(),
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="输出详细信息.",
        show_default=False,
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="输出版本信息.",
        show_default=False,
        is_eager=True,
        callback=version_callback,
    ),
):
    """requests cli工具"""
    # 格式化列表为字典
    if params:
        params = process_list_data(params)
    if data:
        data = process_list_data(data)
    try:
        first_time = time.time()
        # 请求
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Requesting...", total=None)
            res = requests.request(
                method=method,
                url=url,
                params=params,
                json=json,
                data=data,
                headers=headers,
                timeout=timeout,
                cookies=cookies,
                proxies=proxies,
            )
        last_time = time.time() - first_time
    except Exception as e:
        print("[bold red]Error:[/bold red]", e)
        raise typer.Exit()
    # 打印url
    print(method, res.status_code, url, f"ResponseTime:{last_time}s", end="\n\n")
    # 判断verbose
    if verbose:
        # 打印请求头
        print("[bold blue]Request Headers:[/bold blue]")
        for k, v in res.request.headers.items():
            print(f"{k}:{v}")

        # 换行用
        print()
    # 打印响应头
    print("[bold blue]Response Headers:[/bold blue]")
    for k, v in res.headers.items():
        print(f"{k}:{v}")
    # 换行用
    print()
    # 打印响应体
    try:
        print("[bold blue]Response Body:[/bold blue]")
        print(res.json(), end="\n\n")
    except JSONDecodeError:
        print(res.text, end="\n\n")


if __name__ == "__main__":
    app()
