"""ntchat适配器
适配ntchat服务
"""
import asyncio
import contextlib
import inspect
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

from nonebot.drivers.fastapi import Driver
from nonebot.exception import WebSocketClosed
from nonebot.internal.driver import (
    URL,
    Request,
    Response,
    WebSocket,
    WebSocketServerSetup,
)
from nonebot.typing import overrides
from nonebot.utils import DataclassEncoder, escape_tag

from nonebot.adapters import Adapter as BaseAdapter

from . import event
from .bot import Bot
from .collator import EventModels
from .config import Config
from .event import Event
from .store import ResultStore
from .utils import handle_api_result, log

event_models = EventModels[Event]()
"""事件模型创建器"""


class Adapter(BaseAdapter):

    _result_store = ResultStore()
    """api回调存储"""

    def __init__(self, driver: Driver, **kwargs):
        super().__init__(driver, **kwargs)
        self.ntchat_config: Config = Config(**self.config.dict())
        self.connections: Dict[str, WebSocket] = {}
        self.tasks: List["asyncio.Task"] = []
        self._search_events()
        self._setup()

    def _search_events(self):
        """搜索事件模型"""
        for model_name in dir(event):
            model = getattr(event, model_name)
            if not inspect.isclass(model) or not issubclass(model, Event):
                continue
            event_models.add_event_model(model)

    def _setup(self) -> None:
        ws_setup = WebSocketServerSetup(
            URL("/ntchat/"), self.get_name(), self._handle_ws
        )
        self.setup_websocket_server(ws_setup)
        ws_setup = WebSocketServerSetup(
            URL("/ntchat/ws"), self.get_name(), self._handle_ws
        )
        self.setup_websocket_server(ws_setup)
        ws_setup = WebSocketServerSetup(
            URL("/ntchat/ws/"), self.get_name(), self._handle_ws
        )
        path = Path(self.ntchat_config.chache_path)
        path.mkdir(parents=True, exist_ok=True)
        self.setup_websocket_server(ws_setup)

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        """适配器名称: `ntchat`"""
        return "ntchat"

    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        websocket = self.connections.get(bot.self_id, None)
        timeout: float = data.get("_timeout", self.config.api_timeout)
        log("DEBUG", f"Calling API <y>{api}</y>")

        if websocket:
            seq = self._result_store.get_seq()
            json_data = json.dumps(
                {"action": api, "params": data, "echo": str(seq)},
                cls=DataclassEncoder,
                ensure_ascii=False,
            )
            await websocket.send(json_data)
            return handle_api_result(
                await self._result_store.fetch(bot.self_id, seq, timeout)
            )

    async def _handle_ws(self, websocket: WebSocket) -> None:
        self_id = websocket.request.headers.get("X-Self-ID")

        # check self_id
        if not self_id:
            log("WARNING", "缺少身份标识头")
            await websocket.close(1008, "缺少身份标识头")
            return
        elif self_id in self.bots:
            log("WARNING", f"There's already a bot {self_id}, ignored")
            await websocket.close(1008, "Duplicate X-Self-ID")
            return

        # check access_token
        response = self._check_access_token(websocket.request)
        if response is not None:
            content = cast(str, response.content)
            await websocket.close(1008, content)
            return

        await websocket.accept()
        bot = Bot(self, self_id)
        self.connections[self_id] = websocket
        self.bot_connect(bot)

        log("INFO", f"<y>Bot {escape_tag(self_id)}</y> connected")

        try:
            while True:
                data = await websocket.receive()
                json_data = json.loads(data)
                event = self.json_to_event(json_data, self_id)
                if event:
                    asyncio.create_task(bot.handle_event(event))
        except WebSocketClosed:
            log("WARNING", f"WebSocket for Bot {escape_tag(self_id)} closed by peer")
        except Exception as e:
            log(
                "ERROR",
                f"<r><bg #f8bbd0>Error while process data from websocketfor bot {escape_tag(self_id)}.</bg #f8bbd0></r>",
                e,
            )
        finally:
            with contextlib.suppress(Exception):
                await websocket.close()
            self.connections.pop(self_id, None)
            self.bot_disconnect(bot)

    def _check_access_token(self, request: Request) -> Optional[Response]:
        token = request.headers.get("access_token")

        access_token = self.ntchat_config.access_token
        if access_token and access_token != token:
            msg = "身份认证失败" if token else "缺少身份认证码"
            log("WARNING", msg)
            return Response(403, content=msg)

    @classmethod
    def json_to_event(
        cls, json_data: Any, self_id: Optional[str] = None
    ) -> Optional[Event]:
        """将 json 数据转换为 Event 对象。

        如果为 API 调用返回数据且提供了 Event 对应 Bot，则将数据存入 ResultStore。

        参数:
            json_data: json 数据
            self_id: 当前 Event 对应的 Bot

        返回:
            Event 对象，如果解析失败或为 API 调用返回数据，则返回 None
        """
        if not isinstance(json_data, dict):
            return None

        # api回调设置结果
        if "type" not in json_data:
            if self_id is not None:
                cls._result_store.add_result(self_id, json_data)
            return

        # 实例化事件
        event_model = event_models.get_event_model(json_data)
        try:
            event = event_model.parse_obj(json_data)
            return event
        except Exception as e:
            log(
                "ERROR",
                "<r><bg #f8bbd0>Failed to parse event. "
                f"Raw: {escape_tag(str(json_data))}</bg #f8bbd0></r>",
                e,
            )
