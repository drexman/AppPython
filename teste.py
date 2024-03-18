from datetime import datetime
today_date = datetime.now()
today_format = today_date.strftime("-%d-%m-%Y-%H:%M:%S")

print(today_format)