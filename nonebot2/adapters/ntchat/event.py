from copy import deepcopy
from typing import Any, Dict, List, Type

from nonebot.adapters import Event as BaseEvent
from nonebot.typing import overrides
from nonebot.utils import escape_tag
from pydantic import root_validator

from .message import Message
from .type import EventType, SubType, WxType


class EventRister:
    """事件注册器"""

    event_dict: dict[int, Type["Event"]] = {}
    """事件映射字典"""

    @classmethod
    def rister(cls, type: EventType):
        def _rister(event):
            cls.event_dict[type] = event
            return event

        return _rister

    @classmethod
    def get_event(cls, json_data: Dict) -> "Event":
        event = cls.event_dict.get(json_data["type"])
        if not event:
            raise TypeError("未找到对应event。")
        return event.parse_obj(json_data["data"])


class Event(BaseEvent):
    """
    ntchat事件基类
    """

    timestamp: int
    """时间戳"""
    wx_type: int
    """消息原始类型"""
    from_wxid: str
    """发送者的wxid"""
    room_wxid: str
    """群聊的wxid"""
    to_wxid: str
    """接收者的wxid"""
    msgid: str
    """消息id"""
    to_me: bool = False
    """
    :说明: 消息是否与机器人有关

    :类型: ``bool``
    """

    @overrides(BaseEvent)
    def get_type(self) -> str:
        try:
            wx_type = WxType(self.wx_type)
            return wx_type.name
        except Exception:
            return str(self.wx_type)

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        try:
            wx_type = WxType(self.wx_type)
            return wx_type.name
        except Exception:
            return str(self.wx_type)

    @overrides(BaseEvent)
    def get_message(self) -> "Message":
        raise ValueError("消息没有message实例")

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return escape_tag(str(self.dict()))

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        return self.from_wxid

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        if self.room_wxid:
            return f"group_{self.room_wxid}_{self.from_wxid}"
        else:
            return f"{self.from_wxid}"

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return self.to_me


class MessageEvent(Event):
    """消息事件基类"""

    message: Message
    """消息message对象"""
    to_me: bool = False
    """
    :说明: 消息是否与机器人有关

    :类型: ``bool``
    """

    @root_validator(pre=True, allow_reuse=True)
    def check_message(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if "msg" in values:
            values["message"] = deepcopy(values["msg"])
        else:
            values["message"] = ""
        return values

    @overrides(Event)
    def get_type(self) -> str:
        return "message"

    @overrides(Event)
    def get_message(self) -> "Message":
        return self.message


@EventRister.rister(EventType.MT_RECV_TEXT_MSG)
class TextMessageEvent(MessageEvent):
    """接收文本消息事件"""

    at_user_list: List[str]
    """在群里@的wxid列表"""
    msg: str
    """消息文本内容"""

    @overrides(MessageEvent)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.msg)}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.msg)}"


@EventRister.rister(EventType.MT_RECV_PICTURE_MSG)
class PictureMessageEvent(MessageEvent):
    """接收图片消息"""

    raw_msg: str
    """微信中的原始消息,xml格式"""
    image_thumb: str
    """图片缩略图路径"""
    image: str
    """图片大图路径"""

    @overrides(MessageEvent)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.image)}"
        else:
            return (
                f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.image)}"
            )


@EventRister.rister(EventType.MT_RECV_VOICE_MSG)
class VoiceMessageEvent(MessageEvent):
    """接收语音消息"""

    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(MessageEvent)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.raw_msg)}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.raw_msg)}"


@EventRister.rister(EventType.MT_RECV_CARD_MSG)
class CardMessageEvent(MessageEvent):
    """接收名片消息"""

    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(MessageEvent)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.raw_msg)}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.raw_msg)}"


@EventRister.rister(EventType.MT_RECV_VIDEO_MSG)
class ViedeoMessageEvent(MessageEvent):
    """接收视频消息"""

    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(MessageEvent)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.raw_msg)}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.raw_msg)}"


@EventRister.rister(EventType.MT_RECV_EMOJI_MSG)
class EmojiMessageEvent(MessageEvent):
    """接收表情消息"""

    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(MessageEvent)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.raw_msg)}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.raw_msg)}"


@EventRister.rister(EventType.MT_RECV_LOCATION_MSG)
class LocationMessageEvent(MessageEvent):
    """接收位置消息消息"""

    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(MessageEvent)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.raw_msg)}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.raw_msg)}"


@EventRister.rister(EventType.MT_RECV_FRIEND_MSG)
class FriendRquestEvent(Event):
    """接收加好友请求"""

    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_type(self) -> str:
        return "request"

    @overrides(Event)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.raw_msg)}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.raw_msg)}"


@EventRister.rister(EventType.MT_RECV_SYSTEM_MSG)
class SystemMessageEvent(Event):
    """接收系统消息"""

    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_type(self) -> str:
        return "system"

    @overrides(Event)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.raw_msg)}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.raw_msg)}"


@EventRister.rister(EventType.MT_RECV_REVOKE_MSG)
class RevokeMessageEvent(Event):
    """接收撤回消息"""

    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_type(self) -> str:
        return "notice"

    @overrides(Event)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.raw_msg)}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.raw_msg)}"


@EventRister.rister(EventType.MT_RECV_OTHER_MSG)
class OtherMessageEvent(Event):
    """接收其他消息，根据wx_type自行判断"""

    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_type(self) -> str:
        return "other"

    @overrides(Event)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.raw_msg)}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.raw_msg)}"


class AppEvent(Event):
    """app事件"""

    wx_sub_type: int
    """消息子类型"""

    @overrides(Event)
    def get_type(self) -> str:
        return "app"

    @overrides(Event)
    def get_event_name(self) -> str:
        wx_type = WxType(self.wx_type)
        try:
            sub_type = SubType(self.wx_sub_type)
        except Exception:
            sub_type = self.wx_sub_type
        return f"Message.{wx_type.name}.{sub_type.name}"


@EventRister.rister(EventType.MT_RECV_LINK_MSG)
class LinkMessageEvent(AppEvent):
    """接收链接消息"""

    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.raw_msg)}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.raw_msg)}"


@EventRister.rister(EventType.MT_RECV_FILE_MSG)
class FileMessageEvent(AppEvent):
    """接收文件消息"""

    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.raw_msg)}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.raw_msg)}"


@EventRister.rister(EventType.MT_RECV_MINIAPP_MSG)
class MiniAppMessageEvent(AppEvent):
    """接收小程序消息"""

    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.raw_msg)}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.raw_msg)}"


@EventRister.rister(EventType.MT_RECV_WCPAY_MSG)
class WcpayMessageEvent(AppEvent):
    """接收转帐消息"""

    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.raw_msg)}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.raw_msg)}"


@EventRister.rister(EventType.MT_RECV_OTHER_APP_MSG)
class OtherAppMessageEvent(AppEvent):
    """接收其他应用类型消息,自行判断"""

    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_event_description(self) -> str:
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {escape_tag(self.raw_msg)}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {escape_tag(self.raw_msg)}"
