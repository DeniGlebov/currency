import time
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

import pytz

from rate import model_choices as mch
from rate.models import Rate

import requests


class Command(BaseCommand):
    help = 'Parse Privatbank arhive'  # noqa

    def handle(self, *args, **options):
        path = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
        currency_type_mapper = {'USD': mch.CURRENCY_TYPE_USD, 'EUR': mch.CURRENCY_TYPE_EUR,
                                'RUR': mch.CURRENCY_TYPE_RUR, 'RUB': mch.CURRENCY_TYPE_RUR, }
        day_parse = 30

        for day in range(day_parse):
            start_date = datetime.today() - timedelta(days=day_parse)
            start_date_str = datetime.strftime(start_date, '%d.%m.%Y')
            url = f'{path}{start_date_str}'
            response = requests.get(url, timeout=15)
            time.sleep(5)
            day_parse -= 1
            r = response.json()
            date_str = r.get('date')
            date_rate = datetime.strptime(date_str, '%d.%m.%Y').replace(tzinfo=pytz.timezone('UTC'))
            t = r.get('exchangeRate')
            for i in t:
                if i.get('currency') in currency_type_mapper:
                    currency_type = currency_type_mapper[i.get('currency')]
                    amount_sale = i.get('saleRate')
                    amount_buy = i.get('purchaseRate')
                    Rate.objects.update_or_create(amount=amount_sale, source=mch.SOURCE_PRIVATBANK,
                                                  currency_type=currency_type, type_rate=mch.RATE_TYPE_SALE,
                                                  defaults={'created': date_rate})
                    Rate.objects.update_or_create(amount=amount_buy, source=mch.SOURCE_PRIVATBANK,
                                                  currency_type=currency_type, type_rate=mch.RATE_TYPE_BUY,
                                                  defaults={'created': date_rate})
