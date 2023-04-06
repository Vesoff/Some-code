import requests
import json
from config import keys, api_key


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно сконвертировать одинаковую валюту {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Данной валюты нет в списке, проверьте /values {quote}.')

        try:
            base_ticker = keys[base]
        except:
            raise ConvertionException(f'Данной валюты нет в списке, проверьте /values {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Введено некорректное значение, попробуйте число {amount}.')

        r = requests.get(f'https://api.fastforex.io/fetch-one?from={quote_ticker}&to={base_ticker}&api_key={api_key}')
        total_base = json.loads(r.content)['result'][keys[base]]
        return total_base
