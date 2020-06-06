# Generated by Django 2.2.12 on 2020-05-31 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0002_auto_20200530_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='currency_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'USD'), (2, 'EUR'), (3, 'RUR')]),
        ),
        migrations.AlterField(
            model_name='rate',
            name='source',
            field=models.PositiveSmallIntegerField(choices=[(1, 'PrivatBank'), (2, 'MonoBank'), (3, 'NBU'), (4, 'vkurse.dp.ua'), (5, 'Oschadbank'), (6, 'Aval')]),
        ),
        migrations.AlterField(
            model_name='rate',
            name='type_rate',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Sale'), (2, 'Buy'), (3, 'Amount')]),
        ),
    ]
