import sqlite3

# 【Create table function】
def create_table():

    db_name = "news.db"
    table_name = "news"

    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                news_source VARCHAR(20),
                update_date VARCHAR(20),
                news_title TEXT,
                news_link TEXT,
                CONSTRAINT unique_stock_data UNIQUE (update_date, news_title, news_link)
                )''')

    con.commit()
    con.close()


# 【Delete table function】
def delete_table():

    db_name = "news.db"
    table_name = "news"

    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.execute(f"DROP TABLE IF EXISTS {table_name}")

    con.commit()
    con.close()


if __name__ == "__main__":
    # databases = get_all_databases()
    # for db in databases:
    #     print(db[1])  # 印出資料庫名稱

    # create_database("twse.db")

    # tables = database_info("twse.db")
    # print(tables)

    # delete_table()

    create_table()