from django.urls import reverse

from rate.models import Rate


def test_rate_list(client):
    url = reverse('rate:list')
    response = client.get(url)
    assert response.status_code == 200


def test_rate_csv(client):
    url = reverse('rate:download-csv')
    response = client.get(url)
    assert response.status_code == 200
    assert response._headers['content-type'] == ('Content-Type', 'text/csv')


def test_rate_xlsx(client):
    url = reverse('rate:download-xlsx')
    response = client.get(url)
    assert response.status_code == 200
    assert response._headers['content-type'][1] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def test_latest_rates(client):
    url = reverse('rate:latest-rates')
    response = client.get(url)
    assert response.status_code == 200
    assert response.template_name[0] == 'latest-rates.html'


def test_unauthorized_edit_rate(client):
    url = reverse('rate:edit-rate', kwargs={'pk': '0f1cc5db-79d3-4c78-85b6-6ab34a5eb890'})
    response = client.get(url)
    assert response.status_code == 302


def test_unauthorized_delete_rate(client):
    url = reverse('rate:delete-rate', kwargs={'pk': '152c2d3d-6d86-4cf9-8343-5957ea3fa612'})
    response = client.get(url)
    assert response.status_code == 302


def test_authorized_an_admin_edit_rate(admin_client):
    url = reverse('rate:edit-rate', kwargs={'pk': '3f090a33-6073-40fa-9b57-f9e67387a3ac'})
    response = admin_client.get(url)
    assert response.status_code == 200


def test_authorized_an_admin_delete_rate(admin_client):
    count = Rate.objects.all().count()
    url = reverse('rate:delete-rate', kwargs={'pk': '3f5d6cba-7154-403c-81dd-cd0023f8ee86'})
    response = admin_client.get(url)
    assert response.status_code == 200
    assert 'Are you sure you want to delete' in response.content.decode('utf-8')
    response = admin_client.post(url)
    assert response.status_code == 302
    assert response.url == reverse('rate:list')
    assert Rate.objects.all().count() == count - 1
