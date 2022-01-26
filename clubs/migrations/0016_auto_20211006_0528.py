# Generated by Django 2.2.6 on 2021-10-06 05:28

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0015_auto_20210930_0632'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='balls',
            field=models.CharField(blank=True, choices=[('AR', 'Aramith')], max_length=5, verbose_name='balls'),
        ),
        migrations.AddField(
            model_name='table',
            name='cues',
            field=models.CharField(blank=True, choices=[('CT', 'Cuetec')], max_length=5, verbose_name='cues'),
        ),
        migrations.AlterField(
            model_name='club',
            name='payment_methods',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('CS', 'Наличные'), ('VS', 'Карты')], default='CS', max_length=50, verbose_name='payment methods'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='customer_categories',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('AL', 'Всем'), ('RT', 'Пенсионерам'), ('PP', 'Школьникам'), ('ST', 'Студентам'), ('BD', 'Именинникам')], default='AL', max_length=20, verbose_name='customer categories'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='days_of_the_week',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('MO', 'Понедельник'), ('TU', 'Вторник'), ('WE', 'Среда'), ('TH', 'Четверг'), ('FR', 'Пятница'), ('SA', 'Суббота'), ('SU', 'Воскресенье')], max_length=20, verbose_name='days of the week'),
        ),
    ]
