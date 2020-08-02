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


def test_contact_us_correct_payload(client, settings, fake):
    initial_count = Contact.objects.count()
    assert len(mail.outbox) == 0

    url = reverse('account:contact-us')
    payload = {
        'email_from': fake.email(),
        'title': fake.word(),
        'message': fake.word(),
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


def test_login_get_form(client):
    url = reverse('account:login')
    response = client.get(url)
    assert response.status_code == 200


def test_login_empty_payload(client):
    url = reverse('account:login')
    response = client.post(url, {})
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 2
    assert errors['username'] == ['This field is required.']
    assert errors['password'] == ['This field is required.']


def test_login_incorrect_payload(client):
    url = reverse('account:login')
    payload = {
        'username': 'user1',
        'password': 'password',
    }
    response = client.post(url, payload)
    assert response.status_code == 200
    assert response.context_data['form'].errors['__all__'][
               0] == 'Please enter a correct username and password. Note that both fields may be case-sensitive.'


def test_login_correct_payload(client):
    url = reverse('account:login')
    payload = {
        'username': 'denis',
        'password': 'denis',
    }
    response = client.post(url, payload)
    assert response.status_code == 302


def test_logout_get_form(client):
    url = reverse('account:logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('index')


def test_change_password_unauthorized(client):
    url = reverse('account:change-password')
    response = client.get(url)
    assert response.status_code == 404


def test_singup_form(client, fake):
    url = reverse('account:sign-up')
    password = '123sdf456fgh'
    payload = {
        'email': fake.email(),
        'password1': password,
        'password2': password + 'wrong',
    }
    response = client.post(url, payload)
    assert response.status_code == 200

    payload['password2'] = password
    response = client.post(url, payload)
    assert response.status_code == 302

    response = client.post(url, payload)
    assert response.status_code == 200


def test_ChangePasswordForm(client, fake):
    password = 'denis'
    url = reverse('account:login')
    payload = {
        'username': 'denis',
        'password': password
    }
    response = client.post(url, payload)
    assert response.status_code == 302

    url = reverse('account:change-password')
    response = client.get(url)
    assert response.status_code == 200
    payload = {
        'password_old': fake.word(),
        'password1': password + 'new',
        'password2': password + 'wrong',
    }
    response = client.post(url, payload)
    assert response.status_code == 200
    assert response.context_data['form'].errors['password_old'] == ['Invalid password']

    payload['password_old'] = password
    response = client.post(url, payload)
    assert response.status_code == 200
    assert response.context_data['form'].errors['__all__'][0] == 'Password do not match!'

    payload['password1'] = fake.word()
    payload['password2'] = payload['password1']
    response = client.post(url, payload)
    assert response.status_code == 302
