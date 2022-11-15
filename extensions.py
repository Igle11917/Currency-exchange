import json
import requests


class APIException(Exception):
    pass


class MoneyExchange:
    def __init__(self):
        self.url = 'https://currate.ru/api/'
        self.key = 'b806830a9399631b277f22c5d57a1747'
    def get_price(self, base, quote, amount):
        pair = base + quote
        params = {
            'get': 'rates',
            'pairs': pair,
            'key': self.key
        }
        res = requests.get(self.url, params=params)
        result = round(float(res.json()['data'][pair]) * amount, 2)
        return result





