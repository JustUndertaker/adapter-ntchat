<h1 align="center">Nonebot Adapter Ntchat</h1>

<p align="center">
    <a href="https://github.com/JustUndertaker/ntchat-client/releases"><img src="https://img.shields.io/badge/release-0.3.4-blue.svg?" alt="release"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-brightgreen.svg?" alt="License"></a>
</p>


## 简介

nonebot2的ntchat适配器，配合 [ntchat-client](https://github.com/JustUndertaker/ntchat-client) 可以实现与微信对接。

## 安装方式

### 使用包管理安装（推荐）

```bash
pip install nonebot-adapter-ntchat
```

### 使用源码（不推荐）

```bash
git clone https://github.com/JustUndertaker/adapter-ntchat.git
```

将目录复制到`site-packages`下

## 已实现连接方式

- [x] 反向ws
- [x] http post
- [ ] ~~正向ws~~

其他的感觉用处不大就...

## 配置内容

```dotenv
access_token = ""
```

可不填，如填写需要与 ntchat-lient 一致。

### 使用反向ws：

默认配置使用反向ws，无需调整

### 使用http post

需要将driver类型设置为：ForwardDriver，同时配置http api地址。

设置方法：[文档](https://v2.nonebot.dev/docs/next/tutorial/choose-driver)

示例：

``` dotenv
DRIVER=~httpx
ntchat_http_api_root="http://127.0.0.1:8000"
```

## 注意事项

由于微信不支持连续不同类型消息发出（比如图文消息，发出来会变成2条），需注意：

- matcher的默认发送支持str，MessageSegment，Message，但是发送Message会同时发送多条消息（每个MessageSegment都会发送一条消息）。

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

### 发送图片

使用MessageSegment.image发送图片（其他消息同理），图片与其他文件支持url、bytes、BytesIO、base64、Path发送，手动发送base64时需要在字符串前面加上"base64://"，下面是发送图片的例子.

```python
from base64 import b64encode
from io import BytesIO
from pathlib import Path

from nonebot import on_regex
from nonebot.adapter.ntchat import MessageSegment,TextMessageEvent

matcher = on_regex(r"^测试$")

@matcher.handle()
async def _(event:TextMessageEvent):
    url = "https://v2.nonebot.dev/logo.png"
    image = MessageSegment.image(url)						# 使用url构造
    await matcher.send(image)

    image_path = Path("./1.png")
    image = MessageSegment.image(image_path)				# 使用Path构造
    await matcher.send(image)

    with open(image_path, mode="rb") as f:
        data = f.read()
    image = MessageSegment.image(data)						# 使用bytes构造
    await matcher.send(image)

    bio = BytesIO(data)
    image = MessageSegment.image(bio)						# 使用BytesIO构造
    await matcher.send(image)

    base64_data = f"base64://{b64encode(data).decode()}"	# 使用base64构造
    image = MessageSegment.image(base64_data)
    await matcher.finish(image)
```



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
- **send_image**：发送图片接口
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

