# Generated by Django 2.0.5 on 2018-08-07 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_auto_20180730_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneystats',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='moneystats',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='修改时间'),
        ),
    ]
