from django.urls import path

from rate.api import views

app_name = 'api-rate'

urlpatterns = [
    path('rates/', views.RateListCreateView.as_view(), name='rates'),
    path('latestrates/', views.RateListLatestView.as_view(), name='latestrates'),
    path('rate/<uuid:pk>/', views.RateReadUpdateDeleteView.as_view(), name='rate')
]
