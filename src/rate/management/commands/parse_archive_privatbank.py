import time
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

import pytz

from rate import model_choices as mch
from rate.models import Rate

import requests
from requests import ConnectTimeout, ConnectionError, HTTPError, ReadTimeout, Timeout


class Command(BaseCommand):
    help = 'Parse Privatbank arhive'  # noqa

    def handle(self, *args, **options):

        path = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
        count_request = 3  # 3 ошибки подключения response по url
        day_parse = 1460  # Скольк деней архива нужно спарсить

        for day in range(day_parse):
            start_date = datetime.today() - timedelta(days=day_parse)
            start_date_str = datetime.strftime(start_date, '%d.%m.%Y')
            url = path + start_date_str

            try:
                response = requests.get(url, timeout=5)
            except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError) as err:
                count_request -= 1
                time.sleep(10)  # Ожидание перед  следующим запросом на url
                if count_request == 0:
                    SystemError(err)
                    break

            currency_type_mapper = {'USD': mch.CURRENCY_TYPE_USD, 'EUR': mch.CURRENCY_TYPE_EUR,
                                    'RUR': mch.CURRENCY_TYPE_RUR, 'RUB': mch.CURRENCY_TYPE_RUR, }
            r = response.json()
            date_str = r.get('date')
            date_rate = datetime.strptime(date_str, '%d.%m.%Y').replace(tzinfo=pytz.timezone('Europe/Kiev'))
            t = r.get('exchangeRate')
            for i in t:
                if i.get('currency') in currency_type_mapper:
                    currency_type = currency_type_mapper[i.get('currency')]
                    amount_sale = i.get('saleRate')
                    amount_buy = i.get('purchaseRate')

                    Rate.objects.create(amount=amount_sale, source=mch.SOURCE_PRIVATBANK,
                                        currency_type=currency_type,
                                        type_rate=mch.RATE_TYPE_SALE, )
                    pk = Rate.objects.last().id
                    Rate.objects.filter(id=pk).update(created=date_rate)
                    Rate.objects.create(amount=amount_buy, source=mch.SOURCE_PRIVATBANK,
                                        currency_type=currency_type,
                                        type_rate=mch.RATE_TYPE_BUY, )
                    pk = Rate.objects.last().id
                    Rate.objects.filter(id=pk).update(created=date_rate)
            time.sleep(5)
            day_parse -= 1
