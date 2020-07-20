from rate.api.serializers import RateSerializer
from rate.models import Rate

from rest_framework import generics


class RateListCreateView(generics.ListCreateAPIView):
    # permission_classes = []
    # authentication_classes = []
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class RateReadUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer