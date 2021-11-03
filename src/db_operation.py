# -*- coding: utf-8 -*-
from src.db.sql import *

class Line_bot_db():
    def __init__(self, db_name):
        #連到db
        self.conn = connect_to_db(database = db_name)


#只負責抓資料
class Line_bot_db_parser(Line_bot_db):
    def __init__(self, db_name):
        super(Line_bot_db_parser, self).__init__(db_name)

    #抓取linebot info特定欄位資料
    def query_line_bot_info(self, name, field):
        sql = 'select {} from line_bot_info where name = "{}"'.format(field, name)
        result = query_db(self.conn, sql)
        return result[0][0]

#只負責更新資料
class Line_bot_db_updater(Line_bot_db):
    def __init__(self, db_name):
        super(Line_bot_db_updater, self).__init__(db_name)

    #更新 linebot 的特定資料
    def update_line_bot_info(self, field, value, name):
        sql = 'update line_bot_info set {}="{}" where name="{}"'.format(field, value, name)
        update_value(self.conn, sql)

#只負責新增資料
class Line_bot_db_inserter(Line_bot_db):
    def __init__(self, db_name):
        super(Line_bot_db_inserter, self).__init__(db_name)

    #新增 linebot 的資料到資料庫
    def insert_line_bot_info(self, bot_info):
        sql = 'insert into line_bot_info (name, user_id, channel_access_token, channel_secret, webhook_dns) \
        VALUES ("{}", "{}", "{}", "{}", "{}")'.format(
            bot_info['name'],
            bot_info['user_id'],
            bot_info['channel_access_token'],
            bot_info['channel_secret'],
            bot_info['webhook_dns'])
        insert_value(self.conn, sql)

