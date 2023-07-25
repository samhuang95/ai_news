import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from datetime import datetime

# ================================================
def cnn_titles():
    url = "https://edition.cnn.com/business/tech"

    title_list = []

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    title_tag_list = soup.select('div.container__headline')
    for title_tag in title_tag_list:
        title_tag = title_tag.text

        # 因為抓下來的標題頭尾有換行符號，所以排除
        title_tag = title_tag[1:-1]
        if title_tag not in title_list:
            title_list.append(title_tag)
        else:
            pass

    return title_list

# ================================================
def cnn_links():
    url = "https://edition.cnn.com/business/tech"

    link_list = []

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    link_tag_list = soup.select('a.container__link')
    for link_tags in link_tag_list:
        link_tag = link_tags.get("href")
        link_tag = "https://edition.cnn.com" + link_tag
        
        if link_tag not in link_list:
            link_list.append(link_tag)
        else:
            pass

    return link_list

# ================================================    
def merge_lists_to_df(title_list, link_list):
    # 將兩個列表轉換成字典
    today = datetime.today()
    formatted_date = today.strftime("%Y/%m/%d %H")

    data_dict = {
        'news_source':"CNN",
        'update_date':formatted_date,
        'news_title': title_list,
        'news_link': link_list
    }

    # 將字典轉換成 DataFrame，並指定 columns 為 None
    df = pd.DataFrame(data_dict)
    return df

# ================================================  
def insert_data():

    # 每天的資料表
    title_list = cnn_titles()
    link_list = cnn_links()
    merged_df = merge_lists_to_df(title_list, link_list)
    merged_df = merged_df.to_numpy().tolist()


    # 設定 SQLite3 資料庫連接
    # db_file_path = "news.db"

    # for crontab
    db_file_path = "/mnt/d/Program_project/ai_news/news.db"
    conn = sqlite3.connect(db_file_path)

    # 使用 for 迴圈逐行判斷並插入資料
    for data in merged_df:
        # 取得要插入的 PK 值，PK 值在這個 list 的第三個位置(news_title)
        pk_value = data[2]  

        # 確認資料庫中是否已存在相同 PK 值的資料
        existing_data_query = f'''SELECT * FROM news WHERE news_title = "{pk_value}"'''
        existing_data = conn.execute(existing_data_query).fetchone()

        # 如果不存在相同 PK 值的資料，則插入該筆資料到資料庫中
        if not existing_data:
            insert_query = f'''INSERT INTO 
            news (news_source, update_date, news_title, news_link) 
            VALUES (?, ?, ?, ?)'''

            conn.execute(insert_query, data)
            print(f"Added new data: {pk_value}")
        else:
            print(f"Data already exists: {pk_value}")

    # 提交更改並關閉資料庫連接
    conn.commit()
    conn.close()
    
if __name__ == "__main__":

    insert_data()
    print("update finish!")






