# Generated by Django 2.2.6 on 2022-01-12 07:29

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0020_club_entrance'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='cues_lockers',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='шкафчики для киев'),
        ),
        migrations.AddField(
            model_name='club',
            name='repair',
            field=models.BooleanField(default=False, verbose_name='мастерская'),
        ),
        migrations.AddField(
            model_name='club',
            name='shop',
            field=models.BooleanField(default=False, verbose_name='shop'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='days_of_the_week',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('MO', 'Пн'), ('TU', 'Вт'), ('WE', 'Ср'), ('TH', 'Чт'), ('FR', 'Пт'), ('SA', 'Сб'), ('SU', 'Вс')], max_length=20, verbose_name='days of the week'),
        ),
    ]
