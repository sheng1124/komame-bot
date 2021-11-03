# -*- coding: utf-8 -*-
from src.db_operation import *

#欄位名稱
name = "name"
user_id = "user_id"
channel_secret = "channel_secret"
channel_access_token = "channel_access_token"
webhook_dns = "webhook_dns"

field_list = [name, user_id, channel_secret, channel_access_token, webhook_dns]

if __name__ == '__main__':
    #詢問用意
    script = int(input("insert new data:1, update data:2.\n"))
    if script == 1:
        #插入新資料
        print('insert new data')
        insert_new_line_bot()
    elif script == 2:
        #更新資料
        print('update new data')
        update_line_bot_data()
    else:
        print('exit')

#更新資料
def update_line_bot_data():
    #取得要更新哪一個bot
    botname = input("whitch bot you want to update?\n")
    #連接資料庫，更新資料小精靈
    lbdu = Line_bot_db_updater('komame_bot')
    #檢查每個欄位要不要修改
    for field in field_list:
        new_value = input("If {} need to update, type new value or type enter skip.\n".format(field))
        if new_value:
            #需要更新
            print("update value")
            lbdu.update_line_bot_info(field, new_value, botname)

#插入新資料
def insert_new_line_bot():
    #連接資料庫，插入資料小精靈
    lbdi = Line_bot_db_inserter('komame_bot')
    #手動輸入資料
    bot_info = {}
    bot_info[name] = input("名稱\n")
    bot_info[user_id] = input("bot user id\n")
    bot_info[channel_secret] = input("channel secret\n")
    bot_info[channel_access_token] = input("channel access token\n")
    bot_info[webhook_dns] = input("webhook 網域名稱\n")
    #確認輸入資料
    print("check your inputs")
    print("name=", bot_info[name])
    print("user_id=", bot_info[user_id])
    print("channel_secret=", bot_info[channel_secret])
    print("channel_access_token=", bot_info[channel_access_token])
    print("webhook_dns=", bot_info[webhook_dns])

    if input("Is your inputs correct? yes or no.\n") == 'yes':
        #輸入正確插入資料
        lbdi.insert_line_bot_info(bot_info)