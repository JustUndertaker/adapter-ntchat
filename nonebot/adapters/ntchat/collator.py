from typing import Dict, Generic, Tuple, Type, TypeVar

from .event import Event

E = TypeVar("E", bound=Event)


class EventModels(Generic[E]):
    """
    事件创建器
    """

    event_dict: Dict[Tuple[int, int], Type[E]] = {}
    """事件模型字典"""

    def add_event_model(self, event: Type[E]) -> None:
        """添加事件模型"""
        event_type = event.__fields__.get("type").default
        sub_type = event.__fields__.get("wx_sub_type")
        if sub_type is None:
            sub_type = 0
        else:
            sub_type = sub_type.default
        if event_type:
            self.event_dict[(event_type, sub_type)] = event

    def get_event_model(self, data: Dict) -> Type[E]:
        """获取事件模型"""
        event_type: int = data.get("type")
        sub_type = data["data"].get("wx_sub_type", 0)
        event_model = self.event_dict.get((event_type, sub_type), None)
        if event_model is None and sub_type != 0:
            event_model = self.event_dict.get((event_type, 0))
        return event_model if event_model else Event
