import uuid

from django.db import models

from rate import model_choices as mch
from rate.utils import to_decimal


class Rate(models.Model):
    rate_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=5, decimal_places=3)  # 123.456
    source = models.PositiveSmallIntegerField(choices=mch.SOURCE_CHOICES)  # get_{field}_display()
    currency_type = models.PositiveSmallIntegerField(choices=mch.CURRENCY_TYPE_CHOICES)
    type_rate = models.PositiveSmallIntegerField(choices=mch.RATE_TYPE_CHOICES)

    def save(self, *args, **kwargs):
        self.amount = to_decimal(self.amount)
        super().save(*args, **kwargs)
