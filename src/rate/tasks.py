from bs4 import BeautifulSoup

from celery import shared_task

from rate import model_choices as mch
from rate.models import Rate
from rate.utils import to_decimal

import requests


@shared_task
def parse_privatbank():
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url, timeout=5)
    currency_type_mapper = {
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
        'RUR': mch.CURRENCY_TYPE_RUR,
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
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url, timeout=5)
    currency_type_mapper = {
        840: mch.CURRENCY_TYPE_USD,
        978: mch.CURRENCY_TYPE_EUR,
        643: mch.CURRENCY_TYPE_RUR,
    }

    for item in response.json():

        if item['currencyCodeA'] not in currency_type_mapper or item['currencyCodeB'] != 980:
            continue

        currency_type = currency_type_mapper[item['currencyCodeA']]

        # buy
        amount = to_decimal(item['rateBuy'])

        last = Rate.objects.filter(
            source=mch.SOURCE_MONOBANK,
            currency_type=currency_type,
            type_rate=mch.RATE_TYPE_BUY,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_MONOBANK,
                currency_type=currency_type,
                type_rate=mch.RATE_TYPE_BUY, )

        # sale
        amount = to_decimal(item['rateSell'])

        last = Rate.objects.filter(
            source=mch.SOURCE_MONOBANK,
            currency_type=currency_type,
            type_rate=mch.RATE_TYPE_SALE,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_MONOBANK,
                currency_type=currency_type,
                type_rate=mch.RATE_TYPE_SALE, )


@shared_task
def parse_nbu():
    response = requests.get('https://bank.gov.ua/NBU_Exchange/exchange?json', timeout=5)

    currency_type_mapper = {'840': mch.CURRENCY_TYPE_USD,
                            '978': mch.CURRENCY_TYPE_EUR,
                            '643': mch.CURRENCY_TYPE_RUR, }

    for item in response.json():
        if item['CurrencyCode'] not in currency_type_mapper:
            continue
        currency_type = currency_type_mapper[item['CurrencyCode']]

        if currency_type == mch.CURRENCY_TYPE_RUR:
            amount = to_decimal(item['Amount'] / 10)
        else:
            amount = to_decimal(item['Amount'])

        # buy
        last = Rate.objects.filter(source=mch.SOURCE_NBU,
                                   currency_type=currency_type,
                                   type_rate=mch.RATE_TYPE_BUY,
                                   ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(amount=amount,
                                source=mch.SOURCE_NBU,
                                currency_type=currency_type,
                                type_rate=mch.RATE_TYPE_BUY, )

        if currency_type == mch.CURRENCY_TYPE_RUR:
            amount = to_decimal(item['Amount'] / 10)
        else:
            amount = to_decimal(item['Amount'])

        # sale
        last = Rate.objects.filter(source=mch.SOURCE_NBU,
                                   currency_type=currency_type,
                                   type_rate=mch.RATE_TYPE_SALE,
                                   ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(amount=amount,
                                source=mch.SOURCE_NBU,
                                currency_type=currency_type,
                                type_rate=mch.RATE_TYPE_SALE, )


@shared_task
def parse_vkurse():
    response = requests.get('http://vkurse.dp.ua/course.json', timeout=5)
    currency_type_mapper = {
        'Dollar': mch.CURRENCY_TYPE_USD,
        'Euro': mch.CURRENCY_TYPE_EUR,
        'Rub': mch.CURRENCY_TYPE_RUR,
    }

    for key, value in response.json().items():
        if key not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[key]

        # buy
        amount = to_decimal(value['buy'])

        last = Rate.objects.filter(
            source=mch.SOURCE_BUD_VSEGDA_V_KURSE,
            currency_type=currency_type,
            type_rate=mch.RATE_TYPE_BUY,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_BUD_VSEGDA_V_KURSE,
                currency_type=currency_type,
                type_rate=mch.RATE_TYPE_BUY, )

        # sale
        amount = to_decimal(value['sale'])
        # amount = to_decimal(value['sale'][0:-1])

        last = Rate.objects.filter(
            source=mch.SOURCE_BUD_VSEGDA_V_KURSE,
            currency_type=currency_type,
            type_rate=mch.RATE_TYPE_SALE,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_BUD_VSEGDA_V_KURSE,
                currency_type=currency_type,
                type_rate=mch.RATE_TYPE_SALE, )


@shared_task
def parse_oschadbank():
    rate = []
    page = requests.get('https://www.oschadbank.ua/ua/private/currency', verify=False, timeout=5)

    currency_type_mapper = {
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
        'RUB': mch.CURRENCY_TYPE_RUR,
    }

    soup = BeautifulSoup(page.text, "html.parser")

    body_currency = soup.findAll('table', class_='table table-striped table-hover table-primary')
    temp = body_currency[0].findAll('td')

    for i in temp:
        rate.append(i.text)

    for item in rate:
        if item not in currency_type_mapper:
            continue
        currency_type = currency_type_mapper[item]
        item = rate.index(item)

        if currency_type == mch.CURRENCY_TYPE_RUR:
            amount = to_decimal(rate[item + 5]) / 10
        else:
            amount = to_decimal(rate[item + 5])

        # buy
        last = Rate.objects.filter(
            source=mch.SOURCE_OSCHADBANK,
            currency_type=currency_type,
            type_rate=mch.RATE_TYPE_BUY,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_OSCHADBANK,
                currency_type=currency_type,
                type_rate=mch.RATE_TYPE_BUY, )

        if currency_type == mch.CURRENCY_TYPE_RUR:
            amount = to_decimal(rate[item + 6]) / 10
        else:
            amount = to_decimal(rate[item + 6])

        # sale
        last = Rate.objects.filter(
            source=mch.SOURCE_OSCHADBANK,
            currency_type=currency_type,
            type_rate=mch.RATE_TYPE_SALE,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_OSCHADBANK,
                currency_type=currency_type,
                type_rate=mch.RATE_TYPE_SALE, )


@shared_task
def parse_aval():
    rate = []
    page = requests.get('https://ex.aval.ua/ru/personal/everyday/exchange/exchange/', timeout=5)
    currency_type_mapper = {
        'Доллары США': mch.CURRENCY_TYPE_USD,
        'Евро': mch.CURRENCY_TYPE_EUR,
        'Рубли': mch.CURRENCY_TYPE_RUR,
    }

    soup = BeautifulSoup(page.text, "html.parser")
    body_currency = soup.findAll('div', class_='body-currency')

    temp = body_currency[0].findAll('td')

    for i in temp:
        rate.append(i.text)

    for item in rate:
        if item not in currency_type_mapper:
            continue
        currency_type = currency_type_mapper[item]
        item = rate.index(item)

        # buy
        amount = to_decimal(rate[item + 1].replace(',', '.'))

        last = Rate.objects.filter(
            source=mch.SOURCE_AVAL,
            currency_type=currency_type,
            type_rate=mch.RATE_TYPE_BUY,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_AVAL,
                currency_type=currency_type,
                type_rate=mch.RATE_TYPE_BUY, )

        # sale
        amount = to_decimal(rate[item + 2].replace(',', '.'))

        last = Rate.objects.filter(
            source=mch.SOURCE_AVAL,
            currency_type=currency_type,
            type_rate=mch.RATE_TYPE_SALE,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_AVAL,
                currency_type=currency_type,
                type_rate=mch.RATE_TYPE_SALE, )


@shared_task
def parse():
    parse_monobank.delay()  # pragma: no cover
    parse_privatbank.delay()  # pragma: no cover
    parse_nbu.delay()  # pragma: no cover
    parse_vkurse.delay()  # pragma: no cover
    parse_oschadbank.delay()  # pragma: no cover
    parse_aval.delay()  # pragma: no cover
