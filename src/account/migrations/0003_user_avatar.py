# Generated by Django 2.2.13 on 2020-07-13 19:48

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.FileField(blank=True, null=True, upload_to=account.models.avatar_path),
        ),
    ]
