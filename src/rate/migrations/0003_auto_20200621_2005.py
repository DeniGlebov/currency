# Generated by Django 2.2.13 on 2020-06-21 17:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0002_auto_20200608_0026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rate',
            name='id',
        ),
        migrations.AddField(
            model_name='rate',
            name='rate_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]