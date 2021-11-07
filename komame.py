# -*- coding: utf-8 -*-
import os
import numpy as np
import time
import urllib

from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AudioSendMessage

from src.db_operation import *

DATABASE = 'komame_bot'
BOT = 'komame-bot'

#資料從資料庫取得
lbdp = Line_bot_db_parser(DATABASE)

#設置 API 用來串接服務
LINE_API = LineBotApi(lbdp.get_channel_access_token(BOT))

#設置 handler 用來應對客戶端要求
HANDLER = WebhookHandler(lbdp.get_channel_secret(BOT))

#取得 webhook 網域名稱 
WEBHOOK_DNS = lbdp.get_webhook_dns(BOT)

#設置 flask static 路徑
STATIC_MP3_PATH = "https://{}/static/mp3".format(WEBHOOK_DNS)

#取得關鍵字列表
KEYWORDS=[]
load_keyword()

@app.route("/")
def test():
    return "test connect"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        HANDLER.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#定義如何處理訊息
@HANDLER.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #取得使用者的文字訊息
    mtext = event.message.text.strip()
    print(mtext)
    
    #撿查指令
    if mtext in COMMAND_DICT:
        #訊息是指令執行指令
        print('do command')
        execute_command(event.reply_token, mtext)
        return
    
    #查詢符合哪些關鍵字
    keywords = search_keyword(mtext)
    print('keys=', keywords)
    if len(keywords) = 0:
        print('no keyword found use default keyword')
        keywords = ['迷因']
    
    #找 keywords 所有對應的 words_g id
    words = get_all_words(keywords)
    print('words=', words)
    
    #在words隨機選一個word_stack回復
    word_stack = get_rand_wordstack(words)
    print('word_stack', word_stack)
    
    #從word_stack中找一組word
    word = select_word(word_stack)
    print('word', word)
    
    #回傳音訊
    reply_audio(event.reply_token, word)
    #play_audio(event.reply_token, mtext)

#找 keywords 所有對應的 words_g id 
def get_all_words(keywords):
    words = []
    for keyword in keywords: #有多少keyword符合就有多少pack
        #取得在 表 關鍵字對應的 words
        result = lbdp.get_all_words(keyword)
        if len(result) :
            words.append(result) #append([(90,),(91,),(3,),(4,)])
        else:
            print("keyword {} no words".format(keyword))
    return words

#在words隨機選一個word_stack回復
def get_rand_wordstack(words):
    wordstack = []
    for pack in words:# pack = [(90,),(91,),(3,),(4,)] 有多少keyword符合就有多少pack
        rng = int(np.random.rand() * 100)
        index = rng % len(pack)
        wordstack.append(pack[index][0]) # index = 1 pack[1] = (91,) pack[1][0] = 91
    return wordstack

#在words隨機選一個word_stack回復
def select_word(word_stack):
    word = []
    for pack in word_stack: #pack = 91
        #決定stackid的值
        stackid = lbdp.get_max_stackid(pack) + 1
        rng = int(np.random.rand() * 100)
        stackid = rng % stackid
        #取同一個 stackid AND word_group_id 的 word
        result = lbdp.get_word(pack, stackid)
        if len(result) :
            word.append(result)
        else:
            print("gid {} word_stack {} no words".format(pack, stackid))
    return word

#用音訊回應
def reply_audio(token, word):
    audio_msg_list = []
    for pack in word: #pack = [(前面有一隻可愛的狗勾/02.mp, 4, ), (狗勾/01.mp3, 1, ), (被狗嚇/01.mp3, 2,)]
        for row in pack: #row = (前面有一隻可愛的狗勾/02.mp, 4, )
            path = row[0]
            #路徑轉成網路路徑模式
            mp3_path = STATIC_MP3_PATH + "/" + urllib.parse.quote(path)
            mp3_duration = row[1]
            audio_msg = AudioSendMessage(original_content_url = mp3_path, duration = mp3_duration)
            audio_msg_list.append(audio_msg)
    LINE_API.reply_message(token, audio_msg_list)
        
def play_audio(token, mtext):
    mp3_path = ""

    if mtext == "/help":
        cmd_list=""
        for key in METHODS.keys():
            cmd_list += key + "\n"
        msg = TextSendMessage(cmd_list)
        LINE_API.reply_message(token, msg)
        return
    
    replay = False
    message = []
    for key in METHODS.keys():
        if key in mtext:
            mp3_path_list = METHODS[key]
            rng = int(np.random.rand() * 100)
            index = rng % len(mp3_path_list)
            mp3_path = mp3_path_list[index]
            print(mp3_path)
            audio_msg = AudioSendMessage(original_content_url = mp3_path, duration=20000)
            message.append(audio_msg)
            replay = True
    
    if not replay:
        message.append(TextSendMessage("hello"))
    
    LINE_API.reply_message(token, message)
    
#從資料庫查詢所有關鍵字
def load_keyword():
    for (keyword, ) in lbdp.get_keyword_list(): #[(), ()]
        KEYWORDS.append(keyword)

#找尋所有匹配的關鍵子
def search_keyword(text):
    #把關鍵字列表裡的關鍵字一一比對使用者傳的訊息
    keywords = []
    for keyword in KEYWORDS:
        if keyword in text:
            #關鍵字匹配
            keywords.append(keyword)
    return keywords

#指令 傳所有關鍵字給使用者
def reply_keyword(token):
    keyword_list = ''
    for keyword in KEYWORDS:
        keyword_list += keyword + '\n'
    msg = TextSendMessage(keyword_list)
    LINE_API.reply_message(token, msg)

#指令表
COMMAND_DICT={
'/keywords' : reply_keyword
}

#執行指令
def execute_command(token, text):
    command = COMMAND_DICT[text]
    command(token)

if __name__ == '__main__':
    app.run()


