# Generated by Django 2.0.5 on 2018-07-06 02:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('vadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemenu',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 6, 2, 45, 27, 412022, tzinfo=utc), verbose_name='创建日期'),
        ),
    ]
