"""adapter异常
"""

from typing import Optional

from nonebot.exception import AdapterException
from nonebot.exception import ApiNotAvailable as BaseApiNotAvailable
from nonebot.exception import NetworkError as BaseNetworkError


class NtchatAdapterException(AdapterException):
    def __init__(self) -> None:
        super().__init__("ntchat")


class NotInteractableEventError(NtchatAdapterException):
    """非可交互事件错误"""

    def __init__(self, msg: Optional[str] = None) -> None:
        super().__init__()
        self.msg: Optional[str] = msg
        """错误原因"""

    def __repr__(self) -> str:
        return f"<NotInteractableEventError message={self.msg}>"

    def __str__(self) -> str:
        return self.__repr__()


class NetworkError(BaseNetworkError, NtchatAdapterException):
    """网络错误。"""

    def __init__(self, msg: Optional[str] = None) -> None:
        super().__init__()
        self.msg: Optional[str] = msg
        """错误原因"""

    def __repr__(self) -> str:
        return f"<NetWorkError message={self.msg}>"

    def __str__(self) -> str:
        return self.__repr__()


class ApiNotAvailable(BaseApiNotAvailable, NtchatAdapterException):
    """API 连接不可用"""
