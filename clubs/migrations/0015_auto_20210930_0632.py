# Generated by Django 2.2.6 on 2021-09-30 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0014_auto_20210924_0615'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='brand',
            field=models.CharField(blank=True, choices=[('ST', 'Фабрика "Старт"'), ('RP', 'РуптуР'), ('AR', 'Брянская бильярдная фабрик "Арсенал"'), ('IR', 'Московская бильярдная фабрика "Игра"'), ('DN', 'Dynamic'), ('BR', 'Brunswick'), ('OT', 'Другой')], max_length=5, verbose_name='brand'),
        ),
        migrations.AddField(
            model_name='table',
            name='cloth',
            field=models.CharField(blank=True, choices=[('MN', 'Manchester'), ('GL', 'Galaxy'), ('IW', 'Iwan Simonis'), ('ML', 'Milliken')], max_length=5, verbose_name='cloth'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promotions', to='clubs.Club', verbose_name='club'),
        ),
    ]
