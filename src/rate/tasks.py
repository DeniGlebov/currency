from celery import shared_task

from rate import model_choices as mch
from rate.models import Rate
from rate.utils import to_decimal

import requests


@shared_task
def parse_privatbank():
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    currency_type_mapper = {
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
    }

    for item in response.json():

        if item['ccy'] not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[item['ccy']]

        # buy
        amount = to_decimal(item['buy'])

        last = Rate.objects.filter(
            source=mch.SOURCE_PRIVATBANK,
            currency_type=currency_type,
            type_rate=mch.RATE_TYPE_BUY,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_PRIVATBANK,
                currency_type=currency_type,
                type_rate=mch.RATE_TYPE_BUY, )

        # sale
        amount = to_decimal(item['sale'])

        last = Rate.objects.filter(
            source=mch.SOURCE_PRIVATBANK,
            currency_type=currency_type,
            type_rate=mch.RATE_TYPE_SALE,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_PRIVATBANK,
                currency_type=currency_type,
                type_rate=mch.RATE_TYPE_SALE, )


@shared_task
def parse_monobank():
    pass


@shared_task
def parse():
    parse_monobank.delay()
    parse_privatbank.delay()
