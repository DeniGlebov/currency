from account.models import Contact
from account.tasks import send_email_async

from rest_framework import serializers


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('email_from', 'title', 'message',)

    def create(self, validated_data):
        obj = super().create(validated_data)
        send_email_async().delay(validated_data)
        return obj
