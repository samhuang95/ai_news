from datetime import datetime
today = datetime.today()
formatted_date = today.strftime("%Y/%m/%d %H")
curr_date = today.strftime("%Y/%m/%d")

print(formatted_date)    # 2023/07/25 09
print(curr_date)         # 2023/07/25