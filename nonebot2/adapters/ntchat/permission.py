"""
ntchat权限辅助
"""

from nonebot.permission import Permission

from .event import Event


async def _private(event: Event) -> bool:
    return event.room_wxid == ""


PRIVATE: Permission = Permission(_private)
""" 匹配任意私聊消息类型事件"""


async def _group(event: Event) -> bool:
    return event.room_wxid != ""


GROUP: Permission = Permission(_group)
"""匹配任意群聊消息类型事件"""
