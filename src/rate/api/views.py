from rate.api.serializers import RateSerializer
from rate.models import Rate
from rate.selectors import get_latest_rates

from rest_framework import generics


class RateListCreateView(generics.ListCreateAPIView):
    # permission_classes = []
    # authentication_classes = []
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class RateReadUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class RateListLatestView(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = RateSerializer

    def get_queryset(self):
        return get_latest_rates()
