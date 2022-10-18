from typing import Dict, Generic, Type, TypeVar

from .event import Event

E = TypeVar("E", bound=Event)


class EventModels(Generic[E]):
    """
    事件创建器
    """

    event_dict: Dict[int, Type[E]]
    """事件模型字典"""

    def add_event_model(self, event: Type[E]):
        """添加事件模型"""
        try:
            event_type = event.type
            self.event_dict[event_type] = event
        except AttributeError:
            pass

    def get_event_model(self, data: Dict) -> Type[E]:
        """获取事件模型"""
        event_type: int = data.get("type")
        event_model = self.event_dict.get(event_type, None)
        return event_model if event_model else Event