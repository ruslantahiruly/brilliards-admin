# Generated by Django 2.2.6 on 2022-01-12 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0019_auto_20211228_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='entrance',
            field=models.CharField(blank=True, max_length=100, verbose_name='вход'),
        ),
    ]
