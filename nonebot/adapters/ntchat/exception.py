"""adapter异常
"""

from typing import Optional

from nonebot.exception import AdapterException
from nonebot.exception import NetworkError as BaseNetworkError


class OneBotAdapterException(AdapterException):
    def __init__(self):
        super().__init__("ntchat")


class NotInteractableEventError(OneBotAdapterException):
    """非可交互事件错误"""

    def __init__(self, msg: Optional[str] = None):
        super().__init__()
        self.msg: Optional[str] = msg
        """错误原因"""

    def __repr__(self):
        return f"<NotInteractableEventError message={self.msg}>"

    def __str__(self):
        return self.__repr__()


class NetworkError(BaseNetworkError, OneBotAdapterException):
    """网络错误。"""

    def __init__(self, msg: Optional[str] = None):
        super().__init__()
        self.msg: Optional[str] = msg
        """错误原因"""

    def __repr__(self):
        return f"<NetWorkError message={self.msg}>"

    def __str__(self):
        return self.__repr__()
