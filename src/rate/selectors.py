import hashlib

from django.core.cache import cache

from rate import model_choices as mch
from rate.models import Rate


def rate_cache_key(source, type_rate, currency_type):
    return hashlib.md5(f'RATES - LATEST_{source}_{type_rate}_{currency_type}'.encode()).hexdigest()


def get_latest_rates() -> str:
    object_list = []
    for source in mch.SOURCE_CHOICES:
        source = source[0]
        for currency_type in mch.CURRENCY_TYPE_CHOICES:
            currency_type = currency_type[0]
            for type_rate in mch.RATE_TYPE_CHOICES:
                type_rate = type_rate[0]

                key = rate_cache_key(source, type_rate, currency_type)
                cached_rate = cache.get(key)

                # no rate in cache
                if cached_rate is None:
                    rate = Rate.objects.filter(
                        source=source,
                        type_rate=type_rate,
                        currency_type=currency_type,
                    ).last()

                    if rate is not None:
                        cache.set(key, rate, 30)
                        object_list.append(rate)
                else:  # value in cache
                    object_list.append(cached_rate)

    return object_list
