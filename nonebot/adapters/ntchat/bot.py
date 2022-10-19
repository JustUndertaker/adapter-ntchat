import asyncio
import re
from io import BytesIO
from pathlib import Path
from typing import Any, Callable, Union

from nonebot.message import handle_event
from nonebot.typing import overrides

from nonebot.adapters import Bot as BaseBot

from .event import Event, TextMessageEvent
from .exception import NotInteractableEventError
from .message import Message, MessageSegment
from .utils import log


def _check_at_me(bot: "Bot", event: TextMessageEvent) -> None:
    """检查消息开头或结尾是否存在 @机器人，去除并赋值 `event.to_me`。

    参数:
        bot: Bot 对象
        event: TextMessageEvent 对象
    """
    if not isinstance(event, TextMessageEvent):
        return

    if bot.self_id in event.at_user_list:
        event.to_me = True


def _check_nickname(bot: "Bot", event: TextMessageEvent) -> None:
    """检查消息开头是否存在昵称，去除并赋值 `event.to_me`。

    参数:
        bot: Bot 对象
        event: TextMessageEvent 对象
    """
    first_text = event.msg
    nicknames = set(filter(lambda n: n, bot.config.nickname))
    if nicknames:
        # check if the user is calling me with my nickname
        nickname_regex = "|".join(nicknames)
        m = re.search(rf"^({nickname_regex})([\s,，]*|$)", first_text, re.IGNORECASE)
        if m:
            nickname = m.group(1)
            log("DEBUG", f"User is calling me {nickname}")
            event.to_me = True
            loc = m.end()
            event.msg = first_text[loc:]


async def send(
    bot: "Bot",
    event: Event,
    message: Union[str, MessageSegment, Message],
    **params: Any,  # extra options passed to send_msg API
) -> Any:
    """默认回复消息处理函数。"""
    try:
        from_wxid: str = getattr(event, "from_wxid")
        room_wxid: str = getattr(event, "room_wxid")
    except AttributeError:
        raise NotInteractableEventError("该类型事件没有交互对象，无法发送消息！")
    wx_id = from_wxid if room_wxid == "" else room_wxid

    if isinstance(message, str) or isinstance(message, MessageSegment):
        message = Message(message)

    task = []
    for segment in message:
        api = f"send_{segment.type}"
        segment.data["to_wxid"] = wx_id
        task.append(bot.call_api(api, **segment.data))

    return await asyncio.gather(*task)


class Bot(BaseBot):
    """
    ntchat协议适配。
    """

    send_handler: Callable[["Bot", Event, Union[str, MessageSegment]], Any] = send

    async def handle_event(self, event: Event) -> None:
        """处理收到的事件。"""
        if isinstance(event, TextMessageEvent):
            _check_at_me(self, event)
            _check_nickname(self, event)

        await handle_event(self, event)

    @overrides(BaseBot)
    async def send(
        self,
        event: Event,
        message: Union[str, MessageSegment],
        **kwargs: Any,
    ) -> Any:
        """根据 `event` 向触发事件的主体回复消息。

        参数:
            event: Event 对象
            message: 要发送的消息
            kwargs: 其他参数

        返回:
            API 调用返回数据

        异常:
            NetworkError: 网络错误
            ActionFailed: API 调用失败
        """
        return await self.__class__.send_handler(self, event, message, **kwargs)

    async def send_image(
        self, to_wxid: str, file_path: Union[str, bytes, BytesIO, Path]
    ):
        """
        说明:
            发送图片

        参数:
            * `to_wxid`：接收方的wx_id，可以是好友id，也可以是room_id
            * `file`：图片内容，支持url，本地路径，bytes，BytesIO
        """
        data = MessageSegment.image(file_path=file_path).data
        data["to_wxid"] = to_wxid
        return await self.call_api("send_image", **data)

    async def send_file(
        self, *, to_wxid: str, file_path: Union[str, bytes, BytesIO, Path]
    ):
        """
        说明:
            发送文件

        参数:
            * `to_wxid`：接收人id
            * `file_path`：文件内容，支持url，本地路径，bytes，BytesIO
        """
        data = MessageSegment.file(file_path=file_path).data
        data["to_wxid"] = to_wxid
        return await self.call_api("send_file", **data)

    async def send_video(
        self, *, to_wxid: str, file_path: Union[str, bytes, BytesIO, Path]
    ):
        """
        说明:
            发送视频

        参数:
            * `to_wxid`：接收人id
            * `file_path`：视频内容，支持url，本地路径，bytes，BytesIO
        """
        data = MessageSegment.video(file_path=file_path).data
        data["to_wxid"] = to_wxid
        return await self.call_api("send_video", **data)

    async def send_gif(self, *, to_wxid: str, file: Union[str, bytes, BytesIO, Path]):
        """
        说明:
            发送gif图片

        参数:
            * `to_wxid`：接收人id
            * `file`：图片内容，支持url，本地路径，bytes，BytesIO
        """
        data = MessageSegment.gif(file=file).data
        data["to_wxid"] = to_wxid
        return await self.call_api("send_gif", **data)
