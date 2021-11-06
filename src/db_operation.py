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
    def query_line_bot_info(self, botname, field):
        sql = 'select {} from line_bot_info where name = "{}"'.format(field, botname)
        result = query_db(self.conn, sql)
        return result[0][0]
    
    #抓取 audio_table 欄位資料
    def query_audio_table(self, col_title, value):
        sql = 'select * from audio_table where {} = "{}"'.format(col_title, value)
        result = query_db(self.conn, sql)
        if len(result) != 0:
            return result[0]  #(1,filepath,length,)
        else:
            return []
    #從資料庫抓 channel_access_token
    def get_channel_access_token(self, bot_name):
        channel_access_token = self.query_line_bot_info(bot_name, "channel_access_token")
        return channel_access_token

    #從資料庫抓 channel_secret
    def get_channel_secret(self, bot_name):
        channel_secret = self.query_line_bot_info(bot_name, "channel_secret")
        return channel_secret
    
    #從資料庫抓 webhook_dns
    def get_webhook_dns(self, bot_name):
        webhook_dns = self.query_line_bot_info(bot_name, "webhook_dns")
        return webhook_dns
        
    #從音檔資料表由路徑抓欄位資料
    def get_mp3_row(self, id = None, audio_path = None):
        if id != None:
            row = self.query_audio_table('id', id)
        elif audio_path != None:
            row = self.query_audio_table('filepath', audio_path)
        else:
            row = ()
        return row

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
    
    #新增 audio table 的資料
    def insert_audio_table(self, audio_info):
        sql = 'insert into audio_table (id, filepath, length) \
        values (NULL, "{}", "{}")'.format(
            audio_info['filepath'],
            audio_info['length']
        )
        insert_value(self.conn, sql)

