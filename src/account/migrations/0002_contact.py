# Generated by Django 2.2.13 on 2020-06-20 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('email_from', models.EmailField(max_length=254)),
                ('title', models.CharField(max_length=128)),
                ('message', models.TextField()),
            ],
        ),
    ]