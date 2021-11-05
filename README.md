# komame-bot
this is a komame line bot

#安裝說明

#安裝flask
$ pip install flask

#安裝Line Bot SDK
$ pip install line-bot-sdk==1.18.0

#安裝 mysql
$ pip install mysql-connector-python



#使用運行指令

#用 nohup 保留python存在不會被系統關掉
$ nohup python3 komame.py >> log.txt 2>&1 &

#檢查python程式有沒有在系統中執行
$ ps auwx | grep python

#啟動 ngrok
$ ./start_ngrok.sh 5000

#關閉 ngrok
$ ./stop_ngrok.sh 5000