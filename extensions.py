import time

import requests
import json

from config import keys

from APIandTOKEN import API_CURRENCYLAYER

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(currency):
        try:
            currency_ticker = keys[currency]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {currency}')
        r = requests.get(
            f'http://api.currencylayer.com/live?access_key={API_CURRENCYLAYER}&currencies={currency_ticker}&format=1')
        try:
            price_in_usd = json.loads(r.content)['quotes'][f'USD{currency_ticker}']
        except TypeError:
            price_in_usd = 1
        return price_in_usd

    @staticmethod
    def convert(quote, base, amount):
    # Бесплатная подписка данной API поддерживает только курсы валют к доллару, поэтому нужно сделать два запроса
    # и высчитать их курсы друг к другу относительно доллара.
        quote_usd_coast = CurrencyConverter.get_price(quote)

    #Так же бесплатная подписка не поддерживает два запроса одновременно, поэтому приходится выждать между ними 0.5 сек
        time.sleep(0.5)

        base_usd_coast = CurrencyConverter.get_price(base)

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        total_base = base_usd_coast * amount / quote_usd_coast

        return total_base
