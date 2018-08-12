# Generated by Django 2.0.5 on 2018-07-08 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vadmin', '0004_articlemenu_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlemenu',
            name='uuid',
        ),
        migrations.AddField(
            model_name='articlemenu',
            name='guid',
            field=models.CharField(default='', max_length=32, verbose_name='GUID'),
            preserve_default=False,
        ),
    ]
