<h1 align="center">Nonebot Adapter Ntchat</h1>

<p align="center">
    <a href="https://github.com/JustUndertaker/ntchat-client/releases"><img src="https://img.shields.io/badge/release-0.1.0-blue.svg?" alt="release"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-brightgreen.svg?" alt="License"></a>
</p>

## 简介

nonebot2的ntchat适配器，配合 [ntchat-client](https://github.com/JustUndertaker/ntchat-client) 可以实现与微信对接。

## 已实现连接方式

- [x] 反向ws
- [ ] ~~http~~
- [ ] ~~正向ws~~

其他的感觉用处不大就...

## 配置

与原nonebot2的配置一样，但是由于拓展了`send_image`接口，所以会有一个缓存图片的文件夹，默认是在`./image_cache`，如需更改，请修改以下配置：

```dotenv
chache_path = "./image_cache"
```

**注意**：目前这个文件夹不会自动清理，如需自动清理，请使用定时插件写一个定时清理程序，比如：

```py
from nonebot import get_driver
from nonebot.log import logger
from nonebot import require

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

@scheduler.scheduled_job(trigger="cron", hour=0, minute=0)
async def clean_cache():
    """清理图片缓存"""
    logger.info("正在清理图片缓存...")
    config = get_driver().config
    path = Path(config.chache_path)
    files = path.rglob("*.image")
    count = 0
    for one in files:
        count += 1
        one.unlink()
    logger.info(f"图片清理完毕，共清理：{count} 个...")
```

这样每天0点就会自动清理图片缓存了

## 注意事项

由于微信不支持连续不同类型消息发出（比如图文消息，发出来会变成2条），所以nonebot2的Message没有具体实现，所需要注意的点如下：

- matcher的默认发送只支持一段消息，因此mather.send，matcher.finish等函数附带的消息只能是str，或者MessageSegment，不能是Message
- 可以构造MessageSegment来使用matcher.send等其他函数
- 或者使用bot.call_api来发送消息，具体参数都在提示中有写

## 已实现事件

### 普通事件

- **TextMessageEvent**：文本消息，事件`type`为："message"，可用于触发on_message等
- **FriendRquestEvent**：好友请求消息，事件`type`为："request"，可触发on_request
- **RevokeMessageEvent**：撤回消息通知，事件`type`为："notice"，可触发on_notice

- **PictureMessageEvent**：图片消息，事件`type`为："WX_MSG_PICTURE"
- **VoiceMessageEvent**：语音消息，事件`type`为："WX_MSG_VOICE"
- **CardMessageEvent**：名片消息，事件`type`为："WX_MSG_CARD"
- **ViedeoMessageEvent**：视频消息，事件`type`为："WX_MSG_VIDEO"
- **EmojiMessageEvent**：表情消息，事件`type`为："WX_MSG_EMOJI"
- **LocationMessageEvent**：位置消息，事件`type`为："WX_MSG_LOCATION"
- **SystemMessageEvent**：系统消息，事件`type`为："WX_MSG_SYSTEM"
- **OtherMessageEvent**：其他消息，事件`type`未知

### APP事件

事件type为：app

- **LinkMessageEvent**：链接消息，字段`wx_sub_type`为："WX_APPMSG_LINK"
- **FileMessageEvent**：文件消息，字段`wx_sub_type`为："WX_APPMSG_FILE"
- **MiniAppMessageEvent**：小程序消息，字段`wx_sub_type`为："WX_APPMSG_MINIAPP"
- **WcpayMessageEvent**：转账消息，字段`wx_sub_type`为："WX_APPMSG_WCPAY"
- **OtherAppMessageEvent**：其他应用消息，字段`wx_sub_type`未知

### 监听事件

除了通用的on_message，on_notice等一般行为，想要监听单独某个事件时，可以使用`on`来注册一个matcher，此函数第一个参数为事件`type`，比如：

```python
from nonebot.plugin import on
from nonebot.adapter.ntchat import PictureMessageEvent

matcher = on("WX_MSG_PICTURE") # rule,permission等参数同样可以加入

@matcher.handle()
async def _(event:PictureMessageEvent):
    pass
```

上述例子会监听所有的图片消息事件。

### Permission

内置2个Permission，为：

- **PRIVATE**：匹配任意私聊消息类型事件
- **GROUP**：匹配任意群聊消息类型事件

## 已实现api

- **get_login_info**：获取登录信息
- **get_self_info**：获取自己个人信息跟登录信息类似
- **get_contacts**：获取联系人列表
- **get_publics**：获取关注公众号列表
- **get_contact_detail**：获取联系人详细信息
- **search_contacts**：根据wxid、微信号、昵称和备注模糊搜索联系人
- **get_rooms**：获取群列表
- **get_room_detail**：获取指定群详细信息
- **get_room_members**：获取群成员列表
- **send_text**：发送文本消息
- **send_room_at_msg**：发送群@消息，需要注意：
  - 假如文本为："test,你好{$@},你好{$@}.早上好"
  - 文本消息的content的内容中设置占位字符串 {$@},这些字符的位置就是最终的@符号所在的位置
  - 假设这两个被@的微信号的群昵称分别为aa,bb
  - 则实际发送的内容为 "test,你好@ aa,你好@ bb.早上好"(占位符被替换了)
  - 占位字符串的数量必须和at_list中的微信数量相等.
- **send_card**：发送名片
- **send_link_card**：发送链接卡片
- **send_image**：发送图片接口，对原有接口进行封装，方便发送，注意：
  - 由于ntchat接口只支持本地路径发送，所以adapter做了一些封装
  - 目前支持str路径，Path路径，url路径，bytes
  - 由于是本地路径，所以nb2和ntchat-client必须在同一台机器上
- **send_file**：发送文件
- **send_video**：发送视频
- **send_gif**：发送gif图片
- **send_xml**：发送xml
- **send_pat**：发送拍一拍
- **accept_friend_request**：同意加好友请求
- **create_room**：创建群
- **add_room_member**：添加好友入群
- **invite_room_member**：邀请好友入群
- **del_room_member**：删除群成员
- **modify_room_name**：修改群名
- **modify_room_notice**：修改群公告
- **add_room_friend**：添加群成员为好友
- **quit_room**：退出群
- **modify_friend_remark**：修改好友备注

