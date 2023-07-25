from bbc_crawler import insert_data as bbc_insert_data
from cnn_crawler import insert_data as cnn_insert_data

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction
import configparser
import os
from run import query_database

config = configparser.ConfigParser()

# 取得 config.ini 檔案的絕對路徑
config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
config.read(config_file_path)

ACCESS_TOKEN = config.get('linebot', 'ACCESS_TOKEN')
CHANNEL_SECRET = config.get('linebot', 'CHANNEL_SECRET')

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

def update_data():
    # 使用 BBC 新聞的爬蟲程式碼
    bbc_insert_data()

    # 使用 CNN 新聞的爬蟲程式碼
    cnn_insert_data()

    # 在插入完資料後，呼叫 send_news_notification() 函式來推送新聞訊息給 LINEBOT 使用者
    send_news_notification()

def send_news_notification():
    # 取得每日新聞的查詢結果
    daily_news_result = query_database('最近更新')

    # 推送每日新聞訊息給 LINEBOT 使用者
    line_bot_api.broadcast(TextSendMessage(text=daily_news_result))

if __name__ == "__main__":
    update_data()
    print("update finish!")