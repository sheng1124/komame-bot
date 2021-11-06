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

    #抓取 欄位資料 回傳所有符合的row
    def __query_table_rows(self, table_name, col_title, value):
        sql = 'select * from {} where {} = "{}"'.format(table_name, col_title, value)
        result = query_db(self.conn, sql)
        if len(result) != 0:
            return result
        else:
            return []
    
    #抓取 欄位資料 回傳第一個row
    def __query_table_row(self, table_name, col_title, value):
        result = self.__query_table_rows(table_name, col_title, value)
        if result != []:
            return result[0]  #(1,filepath,length,)
        else:
            return []
    
    #抓取欄位數量
    def __count_table_row(self, table_name):
        sql = 'select count(row_id) from {}'.format(table_name)
        result = query_db(self.conn, sql)
        if len(result) != 0:
            return result[0][0]
        else:
            return 0
    
    #抓取 audio_table 所有欄位
    def get_all_mp3_info(self):
        sql = 'select * from audio_table where 1'
        result = query_db(self.conn, sql)
        return result
    
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

    #從音檔資料表抓一列欄位資料
    def get_mp3_rows(self, id = None, audio_path = None):
        table_name = 'audio_table'
        if id != None:
            row = self.__query_table_rows(table_name, 'id', id)
        elif audio_path != None:
            row = self.__query_table_rows(table_name, 'filepath', audio_path)
        else:
            row = []
        return row
    
    #從音組資料表抓所有欄位資料
    def get_word_rows(self, audio_id):
        table_name = 'word_table'
        row = self.__query_table_rows(table_name, 'audio_id', audio_id)
        return row
    
    #計算 wordtable有多少行
    def get_word_table_count(self):
        result = self.__count_table_row('word_table')
        return result

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
    
    def incert_word_table(self, world_info):
        sql = 'incert into word_table(row_id, word_group_id, audio_id)\
        values(NULL, "{}", "{}")'.format(
            world_info['word_group_id']
            world_info['audio_id']
        )
        insert_value(self.conn, sql)
