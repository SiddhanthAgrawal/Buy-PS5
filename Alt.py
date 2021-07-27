import os
import sys
import requests
from bs4 import BeautifulSoup
import threading
from datetime import datetime
from win10toast import ToastNotifier

import os

URL_sony = 'https://direct.playstation.com/en-us/hardware/ps5'
URL_target = 'https://www.target.com/p/playstation-5-console/-/A-81114595'
URL_bestBuy = 'https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149'
URL_GameStop = 'https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html?condition=New'
URL_Walmart = 'https://www.walmart.com/ip/Sony-PlayStation-5-Video-Game-Console/994712501'
frequency = 2500
duration = 1000


def setInterval(func, time):
    e = threading.Event()
    while not e.wait(time):
        func()


def _getHTML_sony(searchKey):
    page = requests.get(URL_sony)
    soup = BeautifulSoup(page.content.decode('utf8'), 'html.parser')
    results = soup.find(text=searchKey)
    return results


def _getHTML_target(searchKey):
    page = requests.get(URL_target)
    soup = BeautifulSoup(page.content.decode('utf8'), 'html.parser')
    results = soup.find(text=searchKey)
    return results


def _getHTML_bestBuy(searchKey):
    page = requests.get(URL_bestBuy)
    soup = BeautifulSoup(page.content.decode('utf8'), 'html.parser')
    results = soup.find(text=searchKey)
    return results


def _getHTML_GameStop(searchKey):
    page = requests.get(URL_GameStop)
    soup = BeautifulSoup(page.content.decode('utf8'), 'html.parser')
    results = soup.find(text=searchKey)
    return results


def _getHTML_Walmart(searchKey):
    page = requests.get(URL_Walmart)
    soup = BeautifulSoup(page.content.decode('utf8'), 'html.parser')
    results = soup.find(text=searchKey)
    return results


def _beep():
    sys.stdout.write('\a')
    sys.stdout.flush()


def _sendNotification(Website):
    toaster = ToastNotifier()
    toaster.show_toast("PS5 is in stock!!!",
                       "Buy PS5 now!!! Available on " + Website,
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
    searchResult_sony = _getHTML_sony('Out of Stock')
    searchResult_target = _getHTML_target('Sold out')
    searchResult_bestBuy = _getHTML_bestBuy('Sold Out')
    searchResult_GameStop = _getHTML_GameStop('NOT AVAILABLE')
    searchResult_Walmart = _getHTML_Walmart('This item is out of stock')
    dateTime = _getNowDate()

    if not searchResult_sony:
        status = ' PS5 is in stock!!!'
        _beep()
        _sendNotification("Sony")
        _recordStockStatus(dateTime + status)

    elif not searchResult_target:
        status = ' PS5 is in stock!!!'
        _beep()
        _sendNotification("Target")
        _recordStockStatus(dateTime + status)

    elif not searchResult_bestBuy:
        status = ' PS5 is in stock!!!'
        _beep()
        _sendNotification("Best Buy")
        _recordStockStatus(dateTime + status)

    elif not searchResult_GameStop:
        status = ' PS5 is in stock!!!'
        _beep()
        _sendNotification("GameStop")
        _recordStockStatus(dateTime + status)

    elif not searchResult_Walmart:
        status = ' PS5 is in stock!!!'
        _beep()
        _sendNotification("Walmart")
        _recordStockStatus(dateTime + status)

    else:
        status = ' Still out of Stock...'

    record = dateTime + status
    print(record)


def _main():
    setInterval(_checkStock, 1)


if __name__ == '__main__':
    _main()