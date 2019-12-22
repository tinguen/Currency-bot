import requests
from db import *


def check(curr):
    url = 'https://api.exchangeratesapi.io/latest?base={}'.format(curr)
    response = requests.get(url)
    try:
        response.json()["error"]
    except Exception:
        return True
    return False


def start(_, __):
    return 'Greetings from CurrencyBot. You can get more information by pressing on /help.'


def help(a=None, b=None):
    return '/help - get info about commands.\n/setCurrency CURRENCY - set your base currency e.g. USD or ' \
           'UAH\n/getRates CURRENCY2 [..currencies]' + ' - get rates between your base currency and specified ' \
                                                       'currency\n/calcMoney [CURRENCY1] CURRENCY2 - calculate how ' \
                                                       'much money would you get\n' + '/addFav CURRENCY1 CURRENCY2 - ' \
                                                                                      'add favorite currencies ' \
                                                                                      'rates\n/fav - display favorite ' \
                                                                                      'currencies rates\n/currencies ' \
                                                                                      '- display all available ' \
                                                                                      'currencies '


def parseCurrency(symbols=None, base="USD"):
    url = 'https://api.exchangeratesapi.io/latest?base={}'.format(base.upper())
    if symbols is not None:
        url += '&symbols='
        for curr in symbols:
            if url[-1] == '=':
                url = url + curr.upper()
                continue
            url = url + ',' + curr.upper()
    response = requests.get(url)
    print(url)

    r = response.json()["rates"]
    s = ''
    for obj in r:
        s += obj.upper() + ' - ' + str(r[obj.upper()]) + '\n'
    return s


def setCurrency(chat_id, s):
    print("a")
    if len(s) < 2:
        return 'Please specify your base currency.'
    url = 'https://api.exchangeratesapi.io/latest?base={}'.format(s[1].upper())
    response = requests.get(url)
    try:
        response.json()["error"]
    except Exception:
        set_currency(chat_id, s[1].upper())
        return 'Your base currency is now {}.'.format(s[1].upper())
    return 'Please specify valid base currency.'


def addFav(chat_id, s):
    if len(s) < 3:
        return 'Please specify your currencies.'
    url = 'https://api.exchangeratesapi.io/latest?base={}'.format(s[1])
    response = requests.get(url)

    url = 'https://api.exchangeratesapi.io/latest?base={}'.format(s[2])
    response = requests.get(url)
    try:
        response.json()["error"]
    except Exception:
        return 'Please specify currency2.'

    add_fav(chat_id, s[1].upper(), s[2].upper())
    return 'Your favorite rate has been added.'


def getRates(chat_id, s):
    if len(s) < 2:
        return 'Please specify currency.'
    if not check(s[1].upper()):
        return 'Please specify valid currency'

    base = get_currency(chat_id)

    if not base:
        return 'Please set base currency'

    return parseCurrency(s[1:], base)


def calcMoney(chat_id, s):
    if len(s) < 4:
        return 'Please specify currency or amount of money.'
    if not check(s[1].upper()) or not check(s[2].upper()):
        return 'Please specify valid currency'

    url = 'https://api.exchangeratesapi.io/latest?base={}'.format(s[1].upper())
    url += '&symbols={}'.format(s[2].upper())
    response = requests.get(url)
    r = response.json()["rates"][s[2].upper()]
    rate = float(r)
    m = 0.0
    try:
        m = float(s[3])
    except Exception:
        return 'Invalid number'

    print(m)
    print(rate)
    return m * rate


def fav(chat_id, _):
    arr = get_fav(chat_id)
    s = ''
    for curr in arr:
        print(curr)
        s += curr[1].upper() + ' - ' + parseCurrency([curr[2].upper()], curr[1].upper())
    return s


def available_currencies(_, a):
    url = 'https://api.exchangeratesapi.io/latest?base=USD'
    response = requests.get(url)
    r = response.json()["rates"]
    arr = []
    s = ''
    for curr in r:
        arr.append(curr)
        s += curr + ' '
    return s


commands = {
    '/start': start,
    '/help': help,
    '/setCurrency': setCurrency,
    '/getRates': getRates,
    '/calcMoney': calcMoney,
    '/addFav': addFav,
    '/fav': fav,
    '/currencies': available_currencies
}
