class VersionError(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class FormatError(Exception):
    def __init__(self) -> None:
        super().__init__("格式错误。example:limit=20")

class UrlVerifyError(Exception):
    def __init__(self) -> None:
        super().__init__("URL格式验证失败,请检查格式.")