import requests
from bs4 import BeautifulSoup as BS
# import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt


def dup_remover(original_list):
    temp_list = []
    for i in original_list:
        if i not in temp_list:
            temp_list.append(i)
    print(len(temp_list))
    return temp_list


times = []
dates = []
opens = []
highs = []
lows = []
closes = []
adj_closes = []
volumes = []

num_data = 730

print("Enter valid Stock:")
Stock = input()
Stock = Stock.upper()
while Stock not in ("AAPL", "MSFT", "TSLA"):
    print("Enter valid Stock:")
    Stock = input()


def yahoo_parser():
    temp_ind = 0

    URL = "https://finance.yahoo.com/quote/" + Stock + "/history?p=" + Stock
    Headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/79.0.3945.88 Safari/537.36"}
    page = requests.get(URL, headers=Headers)
    soup = BS(page.content, 'html.parser')

    for row in soup.find_all('tbody'):
        for srow in row.find_all('tr'):
            for date in srow.find_all('td', attrs={'class': "Py(10px) Ta(start) Pend(10px)"}):
                times.append(datetime.now().strftime("%H:%M:%S"))
                dates.append(date)
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
                    volumes.append(data.text)
                temp_ind += 1
                if temp_ind == 6 * num_data:
                    temp_ind = 0
                    return True


yahoo_parser()
# print(len(dates))
# for i in dates:
#     print(dates.count(i))
# dates = dup_remover(dates)
# print(len(dates))
# print(len(opens))
# print(len(highs))
# print(len(lows))
# print(len(closes))
# a = pd.DataFrame({"Dates": dates, "Opens": opens, "Highs": highs, "Lows": lows,
#                   "Closes": closes, "AdjCloses": adj_closes, "Volumes": volumes})
# print(a)
closes.reverse()
opens.reverse()
adj_closes.reverse()
x_axis = range(len(closes))
# plt.plot(x_axis, closes, label='Closes')
plt.plot(x_axis, opens, label='Opens', color='r')
plt.plot(x_axis, adj_closes, label='Adj Closes')
plt.xlabel('Days')
plt.ylabel('Value')
plt.title(Stock + ' Closes Opens values')
plt.legend()
plt.show()
