# -*- coding: utf-8 -*-
from src.db_operation import *


lbdi = Line_bot_db_inserter('komame_bot')


bot_info = {}
bot_info['name'] = input("名稱\n")
bot_info['user_id'] = input("bot user id\n")
bot_info['channel_access_token'] = input("channel access token\n")
bot_info['channel_secret'] = input("channel secret\n")
bot_info['webhook_dns'] = input("webhook 網域名稱\n")

lbdi.insert_line_bot_info(bot_info)

