# Generated by Django 2.0.5 on 2018-08-21 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vadmin', '0016_auto_20180812_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='articleclassify',
            field=models.CharField(max_length=32, verbose_name='所属分类的GUID'),
        ),
    ]
