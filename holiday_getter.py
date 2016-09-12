import requests
import bs4
import dateutil.parser
import datetime
import pickle


"""
This script is run once a day and checks the list of holidays stored in save.p
save.p is generated once using update_holidays but not rerun daily as the website HTML might change
A reminder is sent via telegram in 7 days before the holiday and 1 day before
"""

#Top half is about scraping data from website
class holiday():
    def __init__(self, name, date, more_info=""):
        self.name = name
        self.more_than_one_day = False
        if date.find("-") > 0:
            date_list =[x.strip() for x in date.partition(",")[0].split("-")]
            self.date = [dateutil.parser.parse(x) for x in date_list]
            self.more_than_one_day = True
        else:
            self.date = [dateutil.parser.parse(date)]
        self.more_info = more_info

    def __repr__(self):
        date_str = str(self.date[0])[:10]
        if self.more_than_one_day:
            date_str = date_str + " to " + str(self.date[1])[:10]
        if self.more_info is not "":
            return self.name + " is on " + date_str + ". Note: " + self.more_info
        else:
            return self.name + " is on " + date_str

        
def update_holidays():
    url = "http://www.mom.gov.sg/employment-practices/public-holidays"
    x = requests.get(url)
    x.raise_for_status()
    parsed_html = bs4.BeautifulSoup(x.content,"lxml")
    td = parsed_html.find_all("td", class_="cell-holiday-name")
    all_hol = []

    for t in td:
        hol_data = []
        for i, x in enumerate(t.strings):
            hol_data.append(x.strip())
        if len(hol_data) == 2:
            all_hol.append([holiday(*hol_data[:2], ""), False, False])
        elif len(hol_data) == 3:
            all_hol.append([holiday(*hol_data[:3]), False, False])
    pickle.dump(all_hol, open("holiday_reminders.p", "wb" ))
    return all_hol

update_holidays()