from linebot import LineBotApi
from linebot.models.rich_menu import RichMenu
import configparser
import os

# 設置LINE Channel的Access Token

config = configparser.ConfigParser()
# 取得 config.ini 檔案的絕對路徑
config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
config.read(config_file_path)
ACCESS_TOKEN = config.get('linebot', 'ACCESS_TOKEN')

line_bot_api = LineBotApi(ACCESS_TOKEN)

def get_rich_menu_id():
    try:
        # 使用LineBotApi的get_rich_menu_list方法查詢Rich Menu列表
        rich_menu_list = line_bot_api.get_rich_menu_list()

        # 遍歷Rich Menu列表，獲取每個Rich Menu的ID
        for rich_menu in rich_menu_list:
            rich_menu_id = rich_menu.rich_menu_id
            print("Rich Menu ID:", rich_menu_id)
    
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    get_rich_menu_id()
