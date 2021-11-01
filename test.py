# -*- coding: utf-8 -*-
from src.db.sql import *

conn = connect_to_db(database = 'komame_bot')

show_db_info(conn)

x = get_db_info(conn)
print(x)

close_db_connection(conn)

