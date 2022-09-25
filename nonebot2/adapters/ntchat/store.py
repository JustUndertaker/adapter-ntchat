"""存储相关，API回调存储，和bot图片发送缓存
"""

import asyncio
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from httpx import AsyncClient
from nonebot.utils import run_sync
from yarl import URL

from .exception import NetworkError


class ResultStore:
    def __init__(self) -> None:
        self._seq: int = 1
        self._futures: Dict[Tuple[str, int], asyncio.Future] = {}

    def get_seq(self) -> int:
        s = self._seq
        self._seq = (self._seq + 1) % sys.maxsize
        return s

    def add_result(self, self_id: str, result: Dict[str, Any]):
        echo = result.get("echo")
        if isinstance(echo, str) and echo.isdecimal():
            future = self._futures.get((self_id, int(echo)))
            if future:
                future.set_result(result)

    async def fetch(
        self, self_id: str, seq: int, timeout: Optional[float]
    ) -> Dict[str, Any]:
        future = asyncio.get_event_loop().create_future()
        self._futures[(self_id, seq)] = future
        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.TimeoutError:
            raise NetworkError("WebSocket API call timeout") from None
        finally:
            del self._futures[(self_id, seq)]


class ImageCache:
    """bot图片缓存"""

    def __init__(self) -> None:
        self._seq: int = 1
        self._client = AsyncClient(
            headers={
                "User-Agent": "Mozilla/5.0(X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"
            }
        )

    def get_seq(self) -> int:
        s = self._seq
        self._seq = (self._seq + 1) % sys.maxsize
        return s

    @run_sync
    def _save(self, image: bytes, path: Path):
        """储存文件"""
        with open(path, mode="wb") as f:
            f.write(image)

    async def get(self, url: URL) -> bytes:
        """请求获取图片"""
        res = await self._client.get(url)
        return res.content

    async def save_image(self, chache_path: Path, image: bytes) -> Path:
        """储存图片，返回路径"""
        seq = self.get_seq()
        path = chache_path / seq
        await self._save(image, path)
        return path
