from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Union

from nonebot.adapters import Bot as BaseBot

from .event import Event, TextMessageEvent
from .message import MessageSegment

def _check_at_me(bot: "Bot", event: TextMessageEvent) -> None: ...
def _check_nickname(bot: "Bot", event: TextMessageEvent) -> None: ...
async def send(
    bot: "Bot",
    event: Event,
    message: Union[str, MessageSegment],
    **params: Any,
) -> Any: ...

class Bot(BaseBot):
    async def call_api(self, api: str, **data) -> Any:
        """调用 ntchat API。

        参数:
            api: API 名称
            data: API 参数

        返回:
            API 调用返回数据

        异常:
            nonebot.adapters.ntchat.exception.NetworkError: 网络错误
            nonebot.adapters.ntchat.exception.ActionFailed: API 调用失败
        """
        ...
    async def handle_event(self, event: Event) -> None:
        """处理收到的事件。"""
        ...
    async def send(
        self,
        event: Event,
        message: Union[str, MessageSegment],
        **kwargs: Any,
    ) -> Any:
        """根据 `event` 向触发事件的主体回复消息。"""
        ...
    async def sql_query(self, sql: str, db: int) -> Dict[str, Any]:
        """
        说明:
            数据库查询

        参数:
            * `sql`：sql地址
            * `db`：数据库名称
        """
        ...
    async def get_login_info(self) -> Dict[str, Any]:
        """
        说明:
            获取登录信息
        """
        ...
    async def get_self_info(self) -> Dict[str, Any]:
        """
        说明:
            获取自己个人信息跟登录信息类似
        """
        ...
    async def get_contacts(self) -> List[Dict[str, Any]]:
        """
        说明:
            获取联系人列表
        """
        ...
    async def get_publics(self) -> List[Dict[str, Any]]:
        """
        说明:
            获取关注公众号列表
        """
        ...
    async def get_contact_detail(self, *, wxid: str) -> Dict[str, Any]:
        """
        说明:
            获取联系人详细信息

        参数:
            * `wxid`：联系人微信id
        """
        ...
    async def search_contacts(
        self,
        *,
        wxid: Union[None, str] = None,
        account: Union[None, str] = None,
        nickname: Union[None, str] = None,
        remark: Union[None, str] = None,
        fuzzy_search: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        说明:
            根据wxid、微信号、昵称和备注模糊搜索联系人

        参数:
            * `wxid`：微信id
            * `account`：微信账号
            * `nickname`：昵称
            * `remark`：备注
            * `fuzzy_search`：是否模糊搜索
        """
        ...
    async def get_rooms(self) -> List[Dict[str, Any]]:
        """
        说明:
            获取群列表
        """
        ...
    async def get_room_detail(self, *, room_wxid: str) -> Dict[str, Any]:
        """
        说明:
            获取指定群详细信息

        参数:
            * `room_wxid`：群id
        """
        ...
    async def get_room_members(self, *, room_wxid: str) -> List[Dict[str, Any]]:
        """
        说明:
            获取群成员列表

        参数:
            * `room_wxid`：群id
        """
        ...
    async def send_text(self, *, to_wxid: str, content: str) -> None:
        """
        说明:
            发送文本消息

        参数:
            * `to_wxid`：接收人id
            * `content`：文本内容
        """
        ...
    async def send_room_at_msg(self, *, to_wxid: str, content: str, at_list: List[str]):
        """
        说明:
            发送群@消息

        参数:
            * `to_wxid`：接收人id
            * `content`：消息内容
            * `at_list`：at列表

        注意:
            - 假如文本为："test,你好{$@},你好{$@}.早上好"
            - 文本消息的content的内容中设置占位字符串 {$@},这些字符的位置就是最终的@符号所在的位置
            - 假设这两个被@的微信号的群昵称分别为aa,bb
            - 则实际发送的内容为 "test,你好@ aa,你好@ bb.早上好"(占位符被替换了)
            - 占位字符串的数量必须和at_list中的微信数量相等.
        """
        ...
    async def send_card(self, *, to_wxid: str, card_wxid: str):
        """
        说明:
            发送名片

        参数:
            * `to_wxid`：接收人id
            * `card_wxid`：卡片人id
        """
        ...
    async def send_link_card(
        self, *, to_wxid: str, title: str, desc: str, url: str, image_url: str
    ):
        """
        说明:
            发送链接卡片

        参数:
            * `to_wxid`：接收人id
            * `title`：新闻标题
            * `desc`：描述
            * `url`：卡片链接地址
            * `image_url`：图片地址
        """
        ...
    async def send_image(
        self, to_wxid: str, file_path: Union[str, bytes, BytesIO, Path]
    ):
        """
        说明:
            发送图片

        参数:
            * `to_wxid`：接收方的wx_id，可以是好友id，也可以是room_id
            * `file_path`：图片内容，支持url，本地路径，bytes，BytesIO
        """
        ...
    async def send_file(
        self, *, to_wxid: str, file_path: Union[str, bytes, BytesIO, Path]
    ):
        """
        说明:
            发送文件

        参数:
            * `to_wxid`：接收人id
            * `file_path`：文件内容，支持url，本地路径，bytes，BytesIO
        """
        ...
    async def send_video(
        self, *, to_wxid: str, file_path: Union[str, bytes, BytesIO, Path]
    ):
        """
        说明:
            发送视频

        参数:
            * `to_wxid`：接收人id
            * `file_path`：视频内容，支持url，本地路径，bytes，BytesIO
        """
        ...
    async def send_gif(self, *, to_wxid: str, file: Union[str, bytes, BytesIO, Path]):
        """
        说明:
            发送gif图片

        参数:
            * `to_wxid`：接收人id
            * `file`：图片内容，支持url，本地路径，bytes，BytesIO
        """
        ...
    async def send_xml(self, *, to_wxid: str, xml: str, app_type: int = 5):
        """
        说明:
            发送xml

        参数:
            * `to_wxid`：接收人id
            * `xml`：xml内容
            * `app_type`：应用id
        """
        ...
    async def send_pat(self, *, room_wxid: str, patted_wxid: str):
        """
        说明:
            发送拍一拍

        参数:
            * `room_wxid`：群id
            * `patted_wxid`：拍一拍目标id
        """
        ...
    async def accept_friend_request(
        self, *, encryptusername: str, ticket: str, scene: int
    ):
        """
        说明:
            同意加好友请求

        参数:
            * `encryptusername`：备注名
            * `ticket`：ticket
            * `scene`scene
        """
        ...
    async def create_room(self, *, member_list: List[str]):
        """
        说明:
            创建群

        参数:
            * `member_list`：邀请成员列表
        """
        ...
    async def add_room_member(self, *, room_wxid: str, member_list: List[str]):
        """
        说明:
            添加好友入群

        参数:
            * `room_wxid`：群id
            * `member_list`：添加id列表
        """
        ...
    async def invite_room_member(self, *, room_wxid: str, member_list: List[str]):
        """
        说明:
            邀请好友入群

        参数:
            * `room_wxid`：群id
            * `member_list`：邀请id列表
        """
        ...
    async def del_room_member(self, *, room_wxid: str, member_list: List[str]):
        """
        说明:
            删除群成员

        参数:
            * `room_wxid`：群id
            * `member_list`：删除id列表
        """
        ...
    async def modify_room_name(self, *, room_wxid: str, name: str):
        """
        说明:
            修改群名

        参数:
            * `room_wxid`：群id
            * `name`：修改后的群名
        """
        ...
    async def modify_room_notice(self, *, room_wxid: str, notice: str):
        """
        说明:
            修改群公告

        参数:
            * `room_wxid`：群id
            * `notice`：修改后的公告
        """
        ...
    async def add_room_friend(self, *, room_wxid: str, wxid: str, verify: str):
        """
        说明:
            添加群成员为好友

        参数:
            * `room_wxid`：群id
            * `wxid`：目标id
            * `verify`：备注名
        """
        ...
    async def quit_room(self, *, room_wxid: str):
        """
        说明:
            退出群

        参数:
            * `room_wxid`：群id
        """
        ...
    async def modify_friend_remark(self, wxid: str, remark: str):
        """
        说明:
            修改好友备注

        参数:
            * `wxid`：好友id
            * `remark`：修改后的备注
        """
        ...
