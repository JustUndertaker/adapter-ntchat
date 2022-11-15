from copy import deepcopy
from enum import IntEnum
from typing import Any, Dict, List
from xml.etree import ElementTree as ET

from nonebot.typing import overrides
from nonebot.utils import escape_tag
from pydantic import BaseModel, root_validator

from nonebot.adapters import Event as BaseEvent

from .message import Message
from .type import EventType, SubType, WxType


class Event(BaseEvent):
    """
    ntchat事件基类
    """

    data: Dict
    """事件原始数据"""
    type: int
    """事件类型"""
    to_me: bool = False
    """
    :说明: 消息是否与机器人有关

    :类型: ``bool``
    """

    @overrides(BaseEvent)
    def get_type(self) -> str:
        try:
            wx_type = EventType(self.type)
            return wx_type.name
        except Exception:
            return str(self.type)

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        try:
            wx_type = EventType(self.type)
            return wx_type.name
        except Exception:
            return str(self.type)

    @overrides(BaseEvent)
    def get_message(self) -> "Message":
        raise ValueError("事件没有message实例")

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return escape_tag(str(self.dict()))

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("事件没有user_id")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        return str(self.type)

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return self.to_me


class MessageEvent(Event):
    """消息事件基类"""

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
    def get_user_id(self) -> str:
        return self.from_wxid

    @overrides(Event)
    def get_message(self) -> "Message":
        return self.message


class TextMessageEvent(MessageEvent):
    """接收文本消息事件"""

    type: int = EventType.MT_RECV_TEXT_MSG
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


class QuoteMessageEvent(MessageEvent):
    """
    引用消息事件，注意此事件原则上属于app事件，但为了方便改为了Message事件
    """

    type: int = EventType.MT_RECV_OTHER_APP_MSG
    wx_sub_type: int = SubType.WX_APPMSG_QUOTE
    """消息子类型"""
    raw_msg: str
    """微信中的原始消息,xml格式"""
    quote_message_id: str
    """被引用消息id"""
    quote_uer_id: str
    """被引用用户id"""

    @root_validator(pre=True, allow_reuse=True)
    def get_pre_message(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        raw_xml = values["raw_msg"]
        xml_obj = ET.fromstring(raw_xml)
        values["message"] = xml_obj.findall("./appmsg/title")[0].text
        refermsg = xml_obj.findall("./appmsg/refermsg")[0]
        values["quote_message_id"] = refermsg.findall("./svrid")[0].text
        values["quote_uer_id"] = refermsg.findall("./chatusr")[0].text
        return values

    @overrides(MessageEvent)
    def get_event_description(self) -> str:
        return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {self.message}"


class PictureMessageEvent(MessageEvent):
    """接收图片消息"""

    type: int = EventType.MT_RECV_PICTURE_MSG
    raw_msg: str
    """微信中的原始消息,xml格式"""
    image_thumb: str
    """图片缩略图路径"""
    image: str
    """图片大图路径"""

    @overrides(MessageEvent)
    def get_event_description(self) -> str:
        msg = "[图片消息]请查看raw_msg"
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {msg}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {msg}"


class VoiceMessageEvent(MessageEvent):
    """接收语音消息"""

    type: int = EventType.MT_RECV_VOICE_MSG
    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(MessageEvent)
    def get_event_description(self) -> str:
        msg = "[语音消息]请查看raw_msg"
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {msg}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {msg}"


class CardMessageEvent(MessageEvent):
    """接收名片消息"""

    type: int = EventType.MT_RECV_CARD_MSG
    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(MessageEvent)
    def get_event_description(self) -> str:
        msg = "[名片消息]请查看raw_msg"
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {msg}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {msg}"


class ViedeoMessageEvent(MessageEvent):
    """接收视频消息"""

    type: int = EventType.MT_RECV_VIDEO_MSG
    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(MessageEvent)
    def get_event_description(self) -> str:
        msg = "[视频消息]请查看raw_msg"
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {msg}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {msg}"


class EmojiMessageEvent(MessageEvent):
    """接收表情消息"""

    type = EventType.MT_RECV_EMOJI_MSG
    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(MessageEvent)
    def get_event_description(self) -> str:
        msg = "[表情消息]请查看raw_msg"
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {msg}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {msg}"


class LocationMessageEvent(MessageEvent):
    """接收位置消息消息"""

    type: int = EventType.MT_RECV_LOCATION_MSG
    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(MessageEvent)
    def get_event_description(self) -> str:
        msg = "[位置消息]请查看raw_msg"
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {msg}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {msg}"


class SystemMessageEvent(Event):
    """接收系统消息"""

    type: int = EventType.MT_RECV_SYSTEM_MSG
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
    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_type(self) -> str:
        return "system"

    @overrides(Event)
    def get_user_id(self) -> str:
        return self.from_wxid

    @overrides(Event)
    def get_event_description(self) -> str:
        msg = "[系统消息]请查看raw_msg"
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {msg}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {msg}"


class OtherMessageEvent(Event):
    """接收其他消息，根据wx_type自行判断"""

    type: int = EventType.MT_RECV_OTHER_MSG
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
    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_type(self) -> str:
        return "other"

    @overrides(Event)
    def get_user_id(self) -> str:
        return self.from_wxid

    @overrides(Event)
    def get_event_description(self) -> str:
        msg = "[其他未知消息]请查看对应type和raw_msg"
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {msg}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {msg}"


class RequestEvent(Event):
    """请求事件基类"""

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

    @overrides(Event)
    def get_type(self) -> str:
        return "request"

    @overrides(Event)
    def get_user_id(self) -> str:
        return self.from_wxid


class FriendAddRequestEvent(RequestEvent):
    """添加好友请求"""

    type: int = EventType.MT_RECV_FRIEND_MSG
    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_event_description(self) -> str:
        msg = "[好友请求消息]请查看raw_msg"
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {msg}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {msg}"


class NoticeEvent(Event):
    """通知事件"""

    @overrides(Event)
    def get_type(self) -> str:
        return "notice"


class RevokeNoticeEvent(NoticeEvent):
    """接收撤回消息"""

    type: int = EventType.MT_RECV_REVOKE_MSG
    wx_type: int
    """消息原始类型"""
    from_wxid: str
    """发送者的wxid"""
    room_wxid: str
    """群聊的wxid"""
    to_wxid: str
    """接收者的wxid"""
    raw_msg: str
    """微信中的原始消息,xml格式"""
    msg_id: str
    """撤回消息id"""

    @overrides(NoticeEvent)
    def get_user_id(self) -> str:
        return self.from_wxid

    @root_validator(pre=True, allow_reuse=True)
    def get_pre_message(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        raw_xml = values["raw_msg"]
        xml_obj = ET.fromstring(raw_xml)
        values["msg_id"] = xml_obj.findall("./revokemsg/newmsgid")[0].text
        return values

    @overrides(NoticeEvent)
    def get_event_description(self) -> str:
        msg = f"[撤回通知]msg_id:{self.msg_id}"
        if self.room_wxid:
            return f"Message  from {self.from_wxid}@[群:{self.room_wxid}]: {msg}"
        else:
            return f"Message  from {self.from_wxid}: {msg}"


class Sex(IntEnum):
    """性别枚举"""

    Man = 0
    """男"""
    Woman = 1
    """女"""


class FriendAddNoticeEvent(NoticeEvent):
    """好友添加通知"""

    type: int = EventType.MT_FRIEND_ADD_NOTIFY_MSG
    account: str
    """微信号"""
    avatar: str
    """头像url"""
    city: str
    """城市"""
    country: str
    """国家"""
    nickname: str
    """微信昵称"""
    remark: str
    """备注"""
    sex: Sex
    """性别"""
    wxid: str
    """微信id"""

    @overrides(NoticeEvent)
    def get_user_id(self) -> str:
        return self.wxid

    @overrides(NoticeEvent)
    def get_event_description(self) -> str:
        return f"[好友添加通知]:{self.dict()}"


class RoomMember(BaseModel):
    """群成员模型"""

    avatar: str
    """头像url"""
    invite_by: str
    """邀请人wxid"""
    nickname: str
    """群内昵称"""
    wxid: str
    """成员wxid"""


class InvitedRoomEvent(NoticeEvent):
    """被邀请入群事件"""

    type: int = EventType.MT_ROOM_INTIVTED_NOTIFY_MSG
    avatar: str
    """群头像url"""
    is_manager: bool
    """你是否为管理员"""
    manager_wxid: str
    """管理员微信id"""
    member_list: List[RoomMember]
    """成员列表"""
    nickname: str
    """群名"""
    room_wxid: str
    """群wxid"""
    total_member: int
    """群内总人数"""

    @overrides(NoticeEvent)
    def get_event_description(self) -> str:
        return f"[被邀请入群通知]：{self.dict()}"


class AppEvent(Event):
    """app事件"""

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

    @overrides(Event)
    def get_type(self) -> str:
        return "app"

    @overrides(Event)
    def get_user_id(self) -> str:
        return self.from_wxid

    @overrides(Event)
    def get_event_name(self) -> str:
        wx_type = WxType(self.wx_type).name
        try:
            sub_type = SubType(self.wx_sub_type).name
        except Exception:
            sub_type = self.wx_sub_type
        return f"AppMessage.{wx_type}.{sub_type}"


class LinkMessageEvent(AppEvent):
    """接收链接消息"""

    type: int = EventType.MT_RECV_LINK_MSG
    wx_sub_type: int = SubType.WX_APPMSG_LINK
    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_event_description(self) -> str:
        msg = "[小程序链接事件]请查看raw_msg"
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {msg}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {msg}"


class FileMessageEvent(AppEvent):
    """接收文件消息"""

    type: int = EventType.MT_RECV_FILE_MSG
    wx_sub_type: int = SubType.WX_APPMSG_FILE
    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_event_description(self) -> str:
        msg = "[接收文件事件]请查看raw_msg"
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {msg}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {msg}"


class MiniAppMessageEvent(AppEvent):
    """接收小程序消息"""

    type: int = EventType.MT_RECV_MINIAPP_MSG
    wx_sub_type: int = SubType.WX_APPMSG_MINIAPP
    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_event_description(self) -> str:
        msg = "[小程序消息]请查看raw_msg"
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {msg}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {msg}"


class WcpayMessageEvent(AppEvent):
    """接收转帐消息"""

    type: int = EventType.MT_RECV_WCPAY_MSG
    wx_sub_type: int = SubType.WX_APPMSG_WCPAY
    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_event_description(self) -> str:
        msg = "[转账消息]请查看raw_msg"
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {msg}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {msg}"


class OtherAppMessageEvent(AppEvent):
    """接收其他应用类型消息,自行判断"""

    type: int = EventType.MT_RECV_OTHER_APP_MSG
    raw_msg: str
    """微信中的原始消息,xml格式"""

    @overrides(Event)
    def get_event_description(self) -> str:
        msg = "[其他应用消息]请查看raw_msg和其他字段"
        if self.room_wxid:
            return f"Message {self.msgid} from {self.from_wxid}@[群:{self.room_wxid}]: {msg}"
        else:
            return f"Message {self.msgid} from {self.from_wxid}: {msg}"
