from rate.models import Rate

from rest_framework import serializers


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ('rate_id', 'amount', 'created', 'get_source_display', 'source', 'currency_type', 'type_rate')
