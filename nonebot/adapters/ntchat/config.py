from typing import Optional

from pydantic import AnyUrl, BaseModel, Field


class WSUrl(AnyUrl):
    """ws或wss url"""

    allow_schemes = {"ws", "wss"}


class Config(BaseModel):
    """ntchat 配置类"""

    access_token: Optional[str] = Field(default=None)
    """令牌口令"""
    ntchat_http_api_root: Optional[str] = Field(default=None)
    """http api请求地址"""

    class Config:
        extra = "ignore"
