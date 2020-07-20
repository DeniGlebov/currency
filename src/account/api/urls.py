from account.api import views

from django.urls import path

app_name = 'api-account'

urlpatterns = [
    path('contact/', views.ContactCreateView.as_view(), name='contact'),
]
