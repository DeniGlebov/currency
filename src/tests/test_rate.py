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
    url = reverse('rate:edit-rate', kwargs={'pk': '0199b4aa-11ab-4abe-98c5-7b86aa93b65e'})
    response = client.get(url)
    assert response.status_code == 302


def test_unauthorized_delete_rate(client):
    url = reverse('rate:delete-rate', kwargs={'pk': '0199b4aa-11ab-4abe-98c5-7b86aa93b65e'})
    response = client.get(url)
    assert response.status_code == 302


def test_authorized_an_admin_edit_rate(admin_client):
    url = reverse('rate:edit-rate', kwargs={'pk': '0199b4aa-11ab-4abe-98c5-7b86aa93b65e'})
    response = admin_client.get(url)
    assert response.status_code == 200


def test_authorized_an_admin_delete_rate(admin_client):
    count = Rate.objects.all().count()
    url = reverse('rate:delete-rate', kwargs={'pk': '0199b4aa-11ab-4abe-98c5-7b86aa93b65e'})
    response = admin_client.get(url)
    assert response.status_code == 200
    assert 'Are you sure you want to delete' in response.content.decode('utf-8')
    response = admin_client.post(url)
    assert response.status_code == 302
    assert response.url == reverse('rate:list')
    assert Rate.objects.all().count() == count - 1
