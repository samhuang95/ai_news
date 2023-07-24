from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction

import sqlite3
import configparser

from datetime import datetime
today = datetime.today()
formatted_date = today.strftime("%Y/%m/%d")

app = Flask(__name__)

# LINE Messaging API 設定

config = configparser.ConfigParser()
config.read('config.ini')
ACCESS_TOKEN = config.get('linebot', 'ACCESS_TOKEN')
CHANNEL_SECRET = config.get('linebot', 'CHANNEL_SECRET')

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 連接至 SQLite 資料庫
conn = sqlite3.connect('news.db')
cursor = conn.cursor()

# 設定選單
menu_template_message = TemplateSendMessage(
    alt_text='選單',
    template=ButtonsTemplate(
        title='功能選單',
        text='請選擇要查詢的項目',
        actions=[
            MessageAction(label='查詢 A', text='A'),
            MessageAction(label='查詢 B', text='B'),
            # 在這裡可以繼續增加其他選單項目
        ]
    )
)

@app.route("/callback", methods=['POST'])
def callback():
    # 當 LINE Messaging API 向你的伺服器發送 POST 請求時，
    # 為了確保該請求的真實性和防止偽造，它會在請求的標頭（headers）中附帶一個特殊的簽名（Signature）。
    # 這個簽名是由 LINE 提供的機密金鑰和請求的內容計算得到的。你的伺服器需要在收到請求時，
    # 使用相同的機密金鑰計算簽名，然後將它和請求中的簽名進行比較，
    # 以確定請求是否合法且來自 LINE 伺服器本身。
    signature = request.headers['X-Line-Signature']

    # 當 LINE Messaging API 向你的伺服器發送 POST 請求時，
    # 其中包含了使用者傳送的訊息或事件資料，這些資料都會被包含在請求的內容（body）中。
    # 在 Flask 中，你可以透過 request 物件來取得這個請求內容。
    body = request.get_data(as_text=True)
    try:
        # handler.handle() 方法會解析 body 中的資料，
        # 並根據使用者傳送的訊息或事件類型來執行相應的處理邏輯
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    if user_message == "選單":
        line_bot_api.reply_message(
            event.reply_token,
            menu_template_message
        )
    elif user_message in ('每日 AI 新聞', '每日產業新聞', '每日新聞'):
        result = query_database(user_message)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="抱歉，我不理解你的指令。請輸入「選單」來查看功能選單。")
        )

def query_database(query_type):
    # 假設你的資料庫有一個名為 table_a 和 table_b 的資料表，並且都有一個名為 data 的欄位
    try:
        if query_type == '每日 AI 新聞':
            cursor.execute(f'''SELECT news_title, news_link FROM news 
                           WHERE 
                           news_title LIKE '% AI %' OR 
                           news_title LIKE '% Artificial %' AND
                           update_date = {formatted_date}
                           ''')
        elif query_type == '每日產業新聞':
            cursor.execute(f'''SELECT news_title, news_link FROM news 
                           WHERE 
                           news_title LIKE '% Apple %' OR 
                           news_title LIKE '% virtual %' OR 
                           news_title LIKE '% nvidia %' AND
                           update_date = {formatted_date}
                           ''')
        elif query_type == '每日新聞':
            cursor.execute(f'''SELECT news_title, news_link FROM news 
                           WHERE 
                           update_date = {formatted_date}
                           ''')

        # 取得查詢結果
        results = cursor.fetchall()

        if len(results) == 0:
            return "查無資料。"

        # 將查詢結果組合成回覆字串
        response = "查詢結果：\n"
        for row in results:
            response += row[0] + "\n"

        return response

    except Exception as e:
        return "發生錯誤：{}".format(str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
