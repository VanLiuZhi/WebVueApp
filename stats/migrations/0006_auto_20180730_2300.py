# Generated by Django 2.0.5 on 2018-07-30 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0005_auto_20180706_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneystats',
            name='created',
            field=models.DateField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='moneystats',
            name='updated',
            field=models.DateField(auto_now=True, verbose_name='修改时间'),
        ),
    ]
