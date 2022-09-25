import re
from pathlib import Path
from typing import Any, Callable, Union

from nonebot.adapters import Bot as BaseBot
from nonebot.message import handle_event
from nonebot.typing import overrides
from yarl import URL

from .event import Event, TextMessageEvent
from .message import MessageSegment
from .store import ImageCache
from .utils import log

image_cache = ImageCache()
"""图片缓存辅助"""


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
    message: Union[str, MessageSegment],
    **params: Any,  # extra options passed to send_msg API
) -> Any:
    """默认回复消息处理函数。"""
    if isinstance(message, str):
        message = MessageSegment.text(message)

    api = f"send_{message.type}"
    message.data["to_wxid"] = event.from_wxid

    return await bot.call_api(api, **message.data)


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

    async def send_image(self, to_wxid: str, file: Union[str, Path, bytes]):
        """
        说明:
            发送图片接口，对原有接口进行封装，方便发送

        参数:
            * `to_wxid`：接收方的wx_id，可以是好友id，也可以是room_id
            * `file`：图片文件，支持url，本地路径，bytes
        """
        if isinstance(file, str):
            url = URL(file)
            if url.scheme == "http" or url.scheme == "https":
                cache_path = Path(self.config.chache_path)
                image = await image_cache.get(url)
                file = await image_cache.save_image(cache_path, image)
            else:
                file = Path(file)
        elif isinstance(file, bytes):
            cache_path = Path(self.config.chache_path)
            file = await image_cache.save_image(cache_path, file)

        await self.call_api("send_image", to_wxid=to_wxid, file_path=file.absolute())
