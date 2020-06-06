from django.urls import path

from rate import views

app_name = 'rate'

urlpatterns = [
    path('list/', views.RateList.as_view(), name='list'),
    path('latest-rates/', views.LatestRatesView.as_view(), name='latest-rates'),
    path('download-csv/', views.RateDownloadCSV.as_view(), name='download-csv'),
]
