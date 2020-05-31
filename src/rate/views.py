from django.http import HttpResponse
from django.shortcuts import render

from rate.models import Rate


def rate(request):
    return HttpResponse('Hello from account')


def rate_all(request):
    # parse parameters
    param = [
        'created',
        'amount',
        'source',
        'currency_type'
        'type_rate',
        'id',
    ]

    rate_queryset = Rate.objects.all()

    for param in param:
        value = request.GET.get(param)
        if value:
            rate_queryset = rate_queryset.filter(**{param: value})

    return render(request, 'rate.html', context={'rate': rate_queryset})
