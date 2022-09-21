import nonebot

from nonebot2.adapters.ntchat.adapter import Adapter

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(Adapter)


nonebot.run()
