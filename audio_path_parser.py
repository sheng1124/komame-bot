# -*- coding: utf-8 -*-
import os
from src.db_operation import *
from mutagen.mp3 import MP3

#取得mp3路徑
def get_mp3_path():
    #收尋每個資料夾
    for root, folders, files in os.walk("./static/mp3/"):
        #資料表的音組類別名稱
        class_name = os.path.basename(root)
        #資料夾排除
        if class_name == "bad":
            continue
        print('class = ', class_name)
        for filename in files:
            if ".mp3" in filename:
                path = class_name + "/" + filename
                print(path)
                yield path
        print()

#讀取mp3並取得長度資訊
def get_mp3_audio_length(mp3_path):
    try:
        mp3_audio = MP3(mp3_path)
        length = mp3_audio.info.length
        return length
    except:
        return 0

if __name__ == '__main__':
    DATABASE = 'komame_bot'
    #資料從資料庫取得
    lbdp = Line_bot_db_parser(DATABASE)
    lbdi = Line_bot_db_inserter(DATABASE)

    for path in get_mp3_path():
        #取得mp3路徑
        file_path = os.path.join("./static/mp3/" + path)
        
        #檢查mp3路徑資訊有沒有在資料庫
        mp3_rows = lbdp.get_mp3_rows(audio_path = path)
        
        #資料庫沒有資料 要新增資料
        if len(mp3_rows) == 0:
            #讀取mp3並取得長度資訊
            mp3_length = get_mp3_audio_length(file_path)
            audio_info = {'filepath' : path, 'length' : int(mp3_length) + 1}
            #插入資料庫
            lbdi.insert_audio_table(audio_info)
            print(path, 'insert to db')
    
    #整理 words table
    for row in lbdp.get_all_mp3_info():
        print(row)
        id = row[0]
        #檢查 id 有沒有在 word 表裡 
        word_rows = lbdp.get_word_rows(id)
        if len(word_rows) == 0:
            #資料庫沒有資料 要新增資料
            new_group_id = lbdp.get_word_table_count() + 1
            word_info = {'audio_id' : id, 'word_group_id' : new_group_id}
            lbdi.incert_word_table(word_info)