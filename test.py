# -*- coding: utf-8 -*-
from src.db_operation import *



lbdp = Line_bot_db_parser('komame_bot')

bot_name = 'komame-bot'

field = 'channel_secret'

result = lbdp.query_line_bot_info(bot_name, field)

print(result)