# Generated by Django 2.0.5 on 2018-07-06 02:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0004_auto_20180706_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneystats',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='日期'),
        ),
    ]
