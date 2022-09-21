from pathlib import Path
from typing import Iterable, List, Type, Union

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment
from nonebot.typing import overrides


class MessageSegment(BaseMessageSegment["Message"]):
    """ntchat MessageSegment 适配。具体方法参考https://www.showdoc.com.cn/579570325733136/3417108506295223。"""

    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @overrides(BaseMessageSegment)
    def __str__(self) -> str:
        type_ = self.type
        data = self.data.copy()
        return f"[{type_}]: {data}"

    @overrides(BaseMessageSegment)
    def __add__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return Message(self) + (
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @overrides(BaseMessageSegment)
    def __radd__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return (
            MessageSegment.text(other) if isinstance(other, str) else Message(other)
        ) + self

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        return self.type == "text"

    @staticmethod
    def at(wx_id: str) -> "TextSegment":
        """at某人"""
        return TextSegment("text", at_list=[wx_id], data={"text": "{$@}"})

    @staticmethod
    def text(text: str) -> "TextSegment":
        """文字消息"""
        return TextSegment("text", data={"text": text})

    @staticmethod
    def card(wx_id: str) -> "MessageSegment":
        """名片消息"""
        return MessageSegment("card", {"card_wxid": wx_id})

    @staticmethod
    def link(title: str, desc: str, url: str, image_url: str) -> "MessageSegment":
        """
        说明:
            链接消息

        参数:
            tittle：标题
            desc：说明文字
            url：链接url
            image_url：图片url
        """
        return MessageSegment(
            "link", {"title": title, "desc": desc, "url": url, "image_url": image_url}
        )

    @staticmethod
    def image(file: Union[str, Path]) -> "MessageSegment":
        """图片消息"""
        if isinstance(file, str):
            file = Path(file)
        return MessageSegment("image", {"file": file})

    @staticmethod
    def file(file: Union[str, Path]) -> "MessageSegment":
        """文件消息"""
        if isinstance(file, str):
            file = Path(file)
        return MessageSegment("file", {"file": file})

    @staticmethod
    def video(file: Union[str, Path]) -> "MessageSegment":
        """视频消息"""
        if isinstance(file, str):
            file = Path(file)
        return MessageSegment("video", {"file": file})

    @staticmethod
    def gif(file: Union[str, Path]) -> "MessageSegment":
        """gif消息"""
        if isinstance(file, str):
            file = Path(file)
        return MessageSegment("file", {"file": file})


class TextSegment(MessageSegment):
    """文字消息段"""

    at_list: List[str] = []
    """at列表"""

    def __add__(self, other: Union[str, "TextSegment"]) -> "TextSegment":
        if isinstance(other, str):
            self.data["text"] += other
            return self
        if isinstance(other, TextSegment):
            if other.at_list:
                self.at_list += other.at_list
            self.data["text"] += other.data["text"]
            return self

    def __radd__(self, other: Union[str, "TextSegment"]) -> "TextSegment":
        if isinstance(other, str):
            self.data["text"] += other
            return self
        if isinstance(other, TextSegment):
            if other.at_list:
                self.at_list += other.at_list
            self.data["text"] += other.data["text"]
            return self


class Message(BaseMessage[MessageSegment]):
    """ntchat 协议 Message 适配。"""

    @classmethod
    @overrides(BaseMessage)
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @overrides(BaseMessage)
    def __add__(
        self, other: Union[str, MessageSegment, Iterable[MessageSegment]]
    ) -> "Message":
        return super(Message, self).__add__(
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @overrides(BaseMessage)
    def __radd__(
        self, other: Union[str, MessageSegment, Iterable[MessageSegment]]
    ) -> "Message":
        return super(Message, self).__radd__(
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @overrides(BaseMessage)
    def __iadd__(
        self, other: Union[str, MessageSegment, Iterable[MessageSegment]]
    ) -> "Message":
        return super().__iadd__(
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @staticmethod
    @overrides(BaseMessage)
    def _construct(msg: str) -> Iterable[MessageSegment]:
        yield MessageSegment.text(msg)
