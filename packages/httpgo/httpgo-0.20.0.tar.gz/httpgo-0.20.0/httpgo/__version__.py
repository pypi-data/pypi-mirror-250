from .utils._exception import VersionError

try:
    from importlib.metadata import metadata
except ImportError:
    raise VersionError("Make sure the python version is greater than 3.7")

# 获取当前项目的版本号
package_version = metadata("httpgo").get(name="Version")
package_name = metadata("httpgo").get(name="Name")
