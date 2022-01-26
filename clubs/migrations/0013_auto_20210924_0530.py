# Generated by Django 2.2.6 on 2021-09-24 05:30

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0012_auto_20210916_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='customer_categories',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('AL', 'Все'), ('RT', 'Пенсионер'), ('PP', 'Школьник'), ('ST', 'Студент'), ('BD', 'Именинник')], default='AL', max_length=20, verbose_name='customer categories'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='type',
            field=models.CharField(choices=[('DC', 'Скидка'), ('OT', 'Остальные')], default='DC', max_length=5, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='name',
            field=models.CharField(choices=[('VK', 'Вконтакте'), ('OK', 'Одноклассники'), ('FB', 'Facebook'), ('TW', 'Twitter'), ('TM', 'Telegram'), ('IN', 'Instagram'), ('UT', 'YouTube')], max_length=5, verbose_name='name'),
        ),
    ]
