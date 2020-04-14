from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt

DRIVER_LOCATION = '/Users/manavram/Downloads/chromedriver'
AVG_CALC_NUMBER = 20
SCROLLS = 1

def dup_remover(original_list):
    temp_list = []
    for i in original_list:
        if i not in temp_list:
            temp_list.append(i)
    return temp_list


times = []
dates = []
opens = []
highs = []
lows = []
closes = []
adj_closes = []
volumes = []
pvts = []
avg_pvts = []


def generate_pvts(a: list, b: list):
    pvts.append(0)
    i = 1
    while i < len(a):
        pvts.append(round((a[i] - a[i - 1]) * b[i] / a[i - 1] + pvts[i - 1]))
        i += 1


def generate_avg_pvts(a: list):
    Output = [sum(a[i:i + AVG_CALC_NUMBER]) / AVG_CALC_NUMBER
              for i in range(len(a) - AVG_CALC_NUMBER)]
    i = 0
    while i < AVG_CALC_NUMBER:
        avg_pvts.append(0)
        i += 1
    avg_pvts.extend(Output)


num_data = 300

print("Enter valid Stock:")
Stock = input()
Stock = Stock.upper()


def volume_int_converter(s: str):
    return int(s.replace(',', ""))


def yahoo_parser():
    global SCROLLS
    temp_ind = 0
    URL = "https://finance.yahoo.com/quote/" + Stock + "/history?period1=999999999&period2=1584662400&interval=1d&filter=history&frequency=1d"
    browser = webdriver.Chrome(DRIVER_LOCATION)
    browser.get(URL)
    time.sleep(1)
    elem = browser.find_element_by_tag_name("body")
    while SCROLLS:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
        SCROLLS -= 1
    source = browser.page_source
    browser.quit()
    Headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/79.0.3945.88 Safari/537.36"}
    page = requests.get(URL, headers=Headers)
    soup = BS(source, 'html.parser')

    for row in soup.find_all('tbody'):
        for srow in row.find_all('tr'):
            for date in srow.find_all('td', attrs={'class': "Py(10px) Ta(start) Pend(10px)"}):
                times.append(datetime.now().strftime("%H:%M:%S"))
                dates.append(date.text)
            for data in srow.find_all('td', attrs={'class': "Py(10px) Pstart(10px)"}):
                if temp_ind % 6 == 0:
                    opens.append(float(data.text))
                if temp_ind % 6 == 1:
                    highs.append(float(data.text))
                if temp_ind % 6 == 2:
                    lows.append(float(data.text))
                if temp_ind % 6 == 3:
                    closes.append(float(data.text))
                if temp_ind % 6 == 4:
                    adj_closes.append(float(data.text))
                if temp_ind % 6 == 5:
                    volumes.append(volume_int_converter(data.text))
                temp_ind += 1
                # if temp_ind == 6 * num_data:
                #     temp_ind = 0
                # return True


yahoo_parser()
dates = dup_remover(dates)
dates.reverse()
opens.reverse()
adj_closes.reverse()
closes.reverse()
volumes.reverse()
generate_pvts(adj_closes, volumes)
generate_avg_pvts(pvts)
a = pd.DataFrame({"Dates": dates, "Opens": opens, "Highs": highs, "Lows": lows,
                  "Closes": closes, "AdjCloses": adj_closes, "Volumes": volumes, "PVTS": pvts, "Avg PVTs": avg_pvts})
to_plot = str(input("What would you like to plot (Opens,Highs,Lows,Closes,AdjCloses,Volumes,PVTS,Avg PVTs): "))
try :
    plt.plot(a[to_plot], label = to_plot)
except :
    print("Exception Occured")
plt.legend()
plt.show()
