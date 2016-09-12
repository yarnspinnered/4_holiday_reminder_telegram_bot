import datetime
import pickle
import telegram
import pandas as pd
import sys

"""
This script is run once a day and checks the list of holidays stored in holiday_reminders.p
holiday_reminders.p is generated once using update_holidays but not rerun daily as the website HTML might change
A reminder is sent via telegram in 7 days before the holiday and 1 day before
"""

def csv_to_dict(cfg_loc, api_name):
    total_dict = pd.read_csv(cfg_loc)
    total_dict.index = total_dict["site"]
    final = total_dict.loc[(api_name)].to_dict()
    return final

def send_message(message):
    api_key = csv_to_dict("C:\\Users\\User\\Documents\\PythonScripts\\config.csv", "telegram")["key"]
    bot = telegram.Bot(api_key)
    chat_id = csv_to_dict("C:\\Users\\User\\Documents\\PythonScripts\\config.csv", "telegram_chat_id")["key"]
    bot.sendMessage(chat_id=chat_id, text=message)

def daily_check():
    holiday_records = pickle.load(open("holiday_reminders.p", "rb"))
    for rec in holiday_records:
        time_to_hol = (rec[0].date[0] - datetime.datetime.now()).days
        if not rec[1] and time_to_hol > 2 and time_to_hol < 7:
            send_message(str(rec[0]) + " This is in less than 7 days.")
            rec[1] = True
        elif not rec[2] and time_to_hol > 0 and time_to_hol < 2:
            send_message(str(rec[0]) + " This is in less than 2 days.")
            rec[2] = True
    pickle.dump(holiday_records, open("save.p", "wb" ))

def main():
    daily_check()

if __name__ == "__main__":
    main(sys.argv)