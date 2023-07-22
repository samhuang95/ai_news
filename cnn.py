import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from datetime import datetime

# ================================================
def cnn_titles(url):

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    title_tag_list = soup.select('div.container__headline')

    title_list = []
    for title_tag in title_tag_list:
        title_name = title_tag.select_one('span').text

        title_list.append(title_name)

    return title_list

# ================================================
def cnn_links(url):

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    link_list = []
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
    formatted_date = today.strftime("%Y/%m/%d")

    data_dict = {
        'news_source':"CNN",
        'update_date':formatted_date,
        'title_list': title_list,
        'link_list': link_list
    }

    # 將字典轉換成 DataFrame
    df = pd.DataFrame(data_dict)
    return df

    
if __name__ == "__main__":

    url_list = ["innovate", "foreseeable-future", "mission-ahead", "innovative-cities"]


    for link in url_list:
        url = f"https://edition.cnn.com/business/tech/{link}"

        title_list = cnn_titles(url)
        link_list = cnn_links(url)

        merged_df = merge_lists_to_df(title_list, link_list)
        print('=======================')
        print(link)
        print(merged_df)
