# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import Error

#建立一個資料庫
def create_db(database, host = '127.0.0.1', port = 3306, user='root', password=''):
    try:
        connection = mysql.connector.connect(host=host, port=port, user=user, password=password)
        sql = "CREATE DATABASE {}".format(database)
        show_db_info(connection)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection = connect_to_db(database)
        return connection
    except Error as e:
        print("資料庫建立失敗：", e)
        return False

# 連接 MySQL/MariaDB 資料庫
def connect_to_db(database, host = '127.0.0.1', port = 3306, user='root', password=''):
    try:
        connection = mysql.connector.connect(host=host, port=port, database=database, user=user, password=password)
        #連接成功顯示訊息
        show_db_info(connection)
        return connection
    except Error as e:
        print("資料庫連接失敗：", e)
        return False

# 顯示資料庫版本、目前使用的資料庫
def show_db_info(connection):
    info = get_db_info(connection)
    if info:
        print("資料庫版本：", info[0])
        print("目前使用的資料庫：", info[1])
    else:
        print('無法顯示資料庫版本、目前使用的資料庫')

#取得資料庫版本、目前使用的資料庫
def get_db_info(connection):
    if connection.is_connected():
        db_Info = connection.get_server_info()
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        connection.commit()
        cursor.close()
        return [db_Info, record]
    else:
        print('無法取得資料庫版本、目前使用的資料庫')
        return False

#取的查詢 db 的 results 基本形式
#回傳值 result = [("xxx", )]
#result => <class 'list'>
#result[0] => <class 'tuple'>
#result[0][0] => <class 'str'>
def query_db(connection, sql):
    #print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return results

#更新表的值
def update_value(connection, sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()

#插入值到表
def insert_value(connection, sql):
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        print('error: ', e)
        print('your sql: ', sql)
        connection.rollback()
    cursor.close()

#關閉db
def close_db_connection(connection):
    if (connection.is_connected()):
        connection.close()
        print("資料庫連線已關閉")
