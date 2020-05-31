from bs4 import BeautifulSoup

from celery import shared_task

from rate import model_choices as mch
from rate.models import Rate
from rate.utils import to_decimal

import requests


@shared_task
def parse_privatbank():
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url, timeout=3)
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
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url, timeout=3)
    currency_type_mapper = {
        840: mch.CURRENCY_TYPE_USD,
        978: mch.CURRENCY_TYPE_EUR,
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
    url = 'https://bank.gov.ua/NBU_Exchange/exchange?json'
    response = requests.get(url, timeout=3)
    currency_type_mapper = {
        '840': mch.CURRENCY_TYPE_USD,
        '978': mch.CURRENCY_TYPE_EUR,
    }

    for item in response.json():

        if item['CurrencyCode'] not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[item['CurrencyCode']]

        # Amount NBU
        amount = to_decimal(item['Amount'])

        last = Rate.objects.filter(
            source=mch.SOURCE_NBU,
            currency_type=currency_type,
            type_rate=mch.RATE_TYPE_AMOUNT,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_NBU,
                currency_type=currency_type,
                type_rate=mch.RATE_TYPE_AMOUNT, )


@shared_task
def parse_vkurse():
    response = requests.get('http://vkurse.dp.ua/course.json', timeout=3).json()

    currency_type_mapper = {
        'Dollar': mch.CURRENCY_TYPE_USD,
        'Euro': mch.CURRENCY_TYPE_EUR,
    }

    for key, value in response.items():

        if key == 'Dollar':
            currency_type = currency_type_mapper[key]

            # buy
            if response[key]['buy']:
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
            if response[key]['sale']:
                amount = to_decimal(value['sale'])

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

        if key == 'Euro':
            currency_type = currency_type_mapper[key]

            # buy
            if response[key]['buy']:
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
            if response[key]['sale']:
                amount = to_decimal(value['sale'][0:-1])

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
    page = requests.get('https://www.oschadbank.ua/ua/private/currency', verify=False, timeout=3)

    currency_type_mapper = {
        '840': mch.CURRENCY_TYPE_USD,
        '978': mch.CURRENCY_TYPE_EUR,
    }

    soup = BeautifulSoup(page.text, "html.parser")
    rate = soup.findAll('td', class_='text-right')

    for item in rate:
        if item.text not in currency_type_mapper:
            continue

        if item.text == '840':
            currency_type = currency_type_mapper[item.text]

            # buy
            amount = to_decimal(rate[4].text)

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

            # sale
            amount = to_decimal(rate[5].text)

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

        if item.text == '978':
            currency_type = currency_type_mapper[item.text]

            # buy
            amount = to_decimal(rate[10].text)

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

            # sale
            amount = to_decimal(rate[11].text)

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
def parse():
    parse_monobank.delay()
    parse_privatbank.delay()
    parse_nbu.delay()
    parse_vkurse.delay()
    parse_oschadbank.delay()
