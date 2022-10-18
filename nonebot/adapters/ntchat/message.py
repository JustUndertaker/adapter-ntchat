from base64 import b64encode
from io import BytesIO
from pathlib import Path
from typing import Iterable, List, Type, Union

from nonebot.typing import overrides

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment


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
        if type_ == "text":
            # 用于command检验
            return data.get("content", "")
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
        return self.type == "text" or self.type == "room_at_msg"

    @staticmethod
    def room_at_msg(content: str, at_list: List[str]) -> "MessageSegment":
        """
        说明:
            - 群里发送@消息，文本消息的content的内容中设置占位字符串 {$@},
            - 这些字符的位置就是最终的@符号所在的位置，假设这两个被@的微信号的群昵称分别为aa,bb:
            - 则实际发送的内容为 "test,你好@ aa,你好@ bb.早上好"(占位符被替换了)

        参数:
            * `content`:文字内容
            * `at_list`：at列表
        """
        return MessageSegment(
            "room_at_msg", data={"content": content, "at_list": at_list}
        )

    @staticmethod
    def text(content: str) -> "MessageSegment":
        """文字消息"""
        return MessageSegment("text", data={"content": content})

    @staticmethod
    def card(card_wxid: str) -> "MessageSegment":
        """名片消息"""
        return MessageSegment("card", {"card_wxid": card_wxid})

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
    def image(file_path: Union[str, bytes, BytesIO, Path]) -> "MessageSegment":
        """图片消息"""
        if isinstance(file_path, BytesIO):
            file_path = file_path.getvalue()
        if isinstance(file_path, bytes):
            file_path = f"base64://{b64encode(file_path).decode()}"
        elif isinstance(file_path, Path):
            file_path = file_path.resolve().as_uri()
        return MessageSegment("image", {"file_path": file_path})

    @staticmethod
    def file(file_path: Union[str, bytes, BytesIO, Path]) -> "MessageSegment":
        """文件消息"""
        if isinstance(file_path, BytesIO):
            file_path = file_path.getvalue()
        if isinstance(file_path, bytes):
            file_path = f"base64://{b64encode(file_path).decode()}"
        elif isinstance(file_path, Path):
            file_path = file_path.resolve().as_uri()
        return MessageSegment("file", {"file_path": file_path})

    @staticmethod
    def video(file_path: Union[str, bytes, BytesIO, Path]) -> "MessageSegment":
        """视频消息"""
        if isinstance(file_path, BytesIO):
            file_path = file_path.getvalue()
        if isinstance(file_path, bytes):
            file_path = f"base64://{b64encode(file_path).decode()}"
        elif isinstance(file_path, Path):
            file_path = file_path.resolve().as_uri()
        return MessageSegment("video", {"file_path": file_path})

    @staticmethod
    def gif(file: Union[str, bytes, BytesIO, Path]) -> "MessageSegment":
        """gif消息"""
        if isinstance(file, BytesIO):
            file = file.getvalue()
        if isinstance(file, bytes):
            file = f"base64://{b64encode(file).decode()}"
        elif isinstance(file, Path):
            file = file.resolve().as_uri()
        return MessageSegment("file", {"file": file})

    @staticmethod
    def xml(xml: str, app_type: int = 5) -> "MessageSegment":
        """xml消息"""
        return MessageSegment("xml", {"xml": xml, "app_type": app_type})


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
