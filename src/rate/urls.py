from django.urls import path

from rate import views

app_name = 'rate'

urlpatterns = [
    path('', views.RateList.as_view(), name='rate'),
]
