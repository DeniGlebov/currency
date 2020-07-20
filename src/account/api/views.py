from account.api.serializers import ContactSerializer
from account.models import Contact

from rest_framework import generics


class ContactCreateView(generics.CreateAPIView):
    # permission_classes = []
    # authentication_classes = []
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
