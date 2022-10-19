"""
消息类型枚举，参考：https://www.showdoc.com.cn/579570325733136/3417087407035329
"""

from enum import IntEnum


class EventType(IntEnum):
    """消息类型枚举"""

    MT_DEBUG_LOG = 11024
    """DEBUG消息"""
    MT_RECV_QRCODE_MSG = 11087
    """获取用户登录二维码"""
    MT_USER_LOGIN = 11025
    """登录消息"""
    MT_USER_LOGOUT = 11026
    """注销消息"""
    MT_DATA_FRIENDS_MSG = 11030
    """获取好友列表消息"""
    MT_DATA_CHATROOMS_MSG = 11031
    """获取群聊列表消息"""
    MT_DATA_CHATROOM_MEMBERS_MSG = 11032
    """获取群成员消息"""
    MT_DATA_PUBLICS_MSG = 11033
    """获取公众号消息"""
    MT_SEND_TEXTMSG = 11036
    """发送文本消息"""
    MT_SEND_CHATROOM_ATMSG = 11037
    """发送群@消息"""
    MT_SEND_CARDMSG = 11038
    """发送名片消息"""
    MT_SEND_LINKMSG = 11039
    """发送链接消息"""
    MT_SEND_IMGMSG = 11040
    """发送图片消息"""
    MT_SEND_FILEMSG = 11041
    """发送文件消息"""
    MT_SEND_VIDEOMSG = 11042
    """发送视频消息"""
    MT_SEND_GIFMSG = 11043
    """发送GIF消息"""
    MT_RECV_TEXT_MSG = 11046
    """接收文本消息"""
    MT_RECV_PICTURE_MSG = 11047
    """接收图片消息"""
    MT_RECV_VOICE_MSG = 11048
    """接收视频消息"""
    MT_RECV_FRIEND_MSG = 11049
    """接收申请好友消息"""
    MT_RECV_CARD_MSG = 11050
    """接收名片消息"""
    MT_RECV_VIDEO_MSG = 11051
    """接收视频消息"""
    MT_RECV_EMOJI_MSG = 11052
    """接收表情消息"""
    MT_RECV_LOCATION_MSG = 11053
    """接收位置消息"""
    MT_RECV_LINK_MSG = 11054
    """接收链接消息"""
    MT_RECV_FILE_MSG = 11055
    """接收文件消息"""
    MT_RECV_MINIAPP_MSG = 11056
    """接收小程序消息"""
    MT_RECV_WCPAY_MSG = 11057
    """接收好友转账消息"""
    MT_RECV_SYSTEM_MSG = 11058
    """接收系统消息"""
    MT_RECV_REVOKE_MSG = 11059
    """接收撤回消息"""
    MT_RECV_OTHER_MSG = 11060
    """接收其他未知消息"""
    MT_RECV_OTHER_APP_MSG = 11061
    """接收应用类型未知消息"""
    MT_ROOM_ADD_MEMBER_NOTIFY_MSG = 11098
    """群员新增通知"""
    MT_ROOM_DEL_MEMBER_NOTIFY_MSG = 11099
    """群员删除通知"""
    MT_ROOM_INTIVTED_NOTIFY_MSG = 11100
    """被邀请入群通知"""
    MT_FRIEND_ADD_NOTIFY_MSG = 11102
    """好友添加通知"""


class WxType(IntEnum):
    """微信原始类型枚举"""

    WX_MSG_TEXT = 1
    """文本"""
    WX_MSG_PICTURE = 3
    """图片"""
    WX_MSG_VOICE = 34
    """语音"""
    WX_MSG_FRIEND = 37
    """加好友请求"""
    WX_MSG_CARD = 42
    """名片"""
    WX_MSG_VIDEO = 43
    """视频"""
    WX_MSG_EMOJI = 47
    """表情"""
    WX_MSG_LOCATION = 48
    """位置"""
    WX_MSG_APP = 49
    """应用类型"""
    WX_MSG_SYSTEM = 10000
    """系统消息"""
    WX_MSG_REVOKE = 10002
    """撤回消息"""


class SubType(IntEnum):
    """应用子类型枚举"""

    WX_APPMSG_LINK = 5
    """链接（包含群邀请）"""
    WX_APPMSG_FILE = 6
    """文件"""
    WX_APPMSG_EMOJI = 8
    """表情消息"""
    WX_APPMSG_MUTIL = 19
    """合并消息"""
    WX_APPMSG_MINIAPP = 33
    """小程序"""
    WX_APPMSG_QUOTE = 57
    """引用消息"""
    WX_APPMSG_WCPAY = 2000
    """转账"""
