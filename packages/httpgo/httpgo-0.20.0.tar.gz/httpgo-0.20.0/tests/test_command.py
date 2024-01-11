from typer.testing import CliRunner
from httpgo.main import app


runner = CliRunner()


def test_argument():
    """测试必填参数"""
    result = runner.invoke(app, ["http://api.tanghaibing.cn/testsuite/getAll"])
    assert result.exit_code == 0
    assert "200" in result.stdout
    assert "'success': True" in result.stdout


def test_option():
    """测试基本可选项"""
    result = runner.invoke(
        app,
        [
            "http://api.tanghaibing.cn/user/login",
            "-m",
            "POST",
            "-j",
            "{'username':'admin','password':'123456'}",
            "-v",
        ],
    )
    assert result.exit_code == 0
    assert "200" in result.stdout
    assert "'success': True" in result.stdout
    assert "Request Headers:" in result.stdout
    assert "'username': 'admin'" in result.stdout