from django.urls import reverse


def test_rate_list(client):
    url = reverse('rate:list')
    response = client.get(url)
    assert response.status_code == 200


def test_rate_csv(client):
    url = reverse('rate:download-csv')
    response = client.get(url)
    assert response.status_code == 200
    assert response._headers['content-type'] == ('Content-Type', 'text/csv')
