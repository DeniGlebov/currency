from account.models import Contact

from django.core import mail
from django.urls import reverse


def test_sanity():
    assert 200 == 200


def test_contact_us_get_form(client):
    url = reverse('account:contact-us')
    response = client.get(url)
    assert response.status_code == 200


def test_contact_us_empty_payload(client):
    assert len(mail.outbox) == 0
    initial_count = Contact.objects.count()
    url = reverse('account:contact-us')
    response = client.post(url, {})
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 3
    assert errors['email_from'] == ['This field is required.']
    assert errors['title'] == ['This field is required.']
    assert errors['message'] == ['This field is required.']
    assert Contact.objects.count() == initial_count
    assert len(mail.outbox) == 0


def test_contact_us_incorrect_payload(client):
    initial_count = Contact.objects.count()
    assert len(mail.outbox) == 0

    url = reverse('account:contact-us')
    payload = {
        'email_from': 'mailmail',
        'title': 'hello world',
        'message': 'hello world\n' * 50,
    }
    response = client.post(url, payload)
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 1
    assert errors['email_from'] == ['Enter a valid email address.']
    assert Contact.objects.count() == initial_count
    assert len(mail.outbox) == 0


def test_contact_us_correct_payload(client, settings):
    initial_count = Contact.objects.count()
    assert len(mail.outbox) == 0

    url = reverse('account:contact-us')
    payload = {
        'email_from': 'mailmail@mail.com',
        'title': 'hello world',
        'message': 'hello world' * 50,
    }
    response = client.post(url, payload)
    assert response.status_code == 302
    assert Contact.objects.count() == initial_count + 1

    # check email
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.subject == payload['title']
    assert email.body == payload['message']
    assert email.from_email == payload['email_from']
    assert email.to == [settings.DEFAULT_FROM_EMAIL]
