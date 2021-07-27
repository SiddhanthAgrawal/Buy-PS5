import os
import sys
import requests
from bs4 import BeautifulSoup
import threading
from datetime import datetime
from win10toast import ToastNotifier

import os

URL = 'https://www.target.com/p/playstation-5-console/-/A-81114595'
frequency = 2500
duration = 1000


def setInterval(func, time):
    e = threading.Event()
    while not e.wait(time):
        func()


def _getHTML(searchKey):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content.decode('utf8'), 'html.parser')
    results = soup.find(text=searchKey)
    return results


def _beep():
    sys.stdout.write('\a')
    sys.stdout.flush()


def _sendNotification():
    toaster = ToastNotifier()
    toaster.show_toast("PS5 is in stock!!!",
                       "Buy PS5 now!!! Available on ",
                       duration=10)


def _recordStockStatus(status):
    f = open("stocklog", "a")
    record = status + '\n'
    f.write(record)
    f.close()


def _getNowDate():
    now = datetime.now()
    dateTime = now.strftime("%m/%d/%Y, %H:%M:%S")
    return dateTime


def _checkStock():
    status = ''
    searchResult = _getHTML('Sold Out')
    print(searchResult)
    dateTime = _getNowDate()

    if not searchResult:
        status = ' PS5 is in stock!!!'
        _beep()
        _sendNotification()
        _recordStockStatus(dateTime + status)

    else:
        status = ' Still out of Stock...'

    record = dateTime + status
    print(record)


def _main():
    setInterval(_checkStock, 1)


if __name__ == '__main__':
    _main()
