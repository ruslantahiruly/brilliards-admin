# Generated by Django 2.2.6 on 2021-09-16 10:26

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0011_club_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='tournaments',
            field=models.BooleanField(default=False, verbose_name='tournaments'),
        ),
        migrations.AlterField(
            model_name='club',
            name='code_number',
            field=models.PositiveIntegerField(default=0, verbose_name='club number'),
        ),
        migrations.AlterField(
            model_name='club',
            name='payment_methods',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('CS', 'Наличный расчет'), ('VS', 'VISA'), ('MC', 'MasterCard'), ('MR', 'МИР')], default='CS', max_length=50, verbose_name='payment methods'),
        ),
        migrations.AlterField(
            model_name='game',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='clubs.Club', verbose_name='club'),
        ),
        migrations.AlterField(
            model_name='game',
            name='hall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='clubs.Hall', verbose_name='hall'),
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(choices=[('RS', 'Русский бильярд'), ('PL', 'Пул'), ('SK', 'Снукер'), ('CR', 'Карамболь')], default='RS', max_length=5, verbose_name='game'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='halls', to='clubs.Club', verbose_name='club'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='clubs.Club', verbose_name='club'),
        ),
        migrations.AlterField(
            model_name='price',
            name='club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='clubs.Club', verbose_name='club'),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_networks', to='clubs.Club', verbose_name='club'),
        ),
        migrations.AlterField(
            model_name='table',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='clubs.Game', verbose_name='game'),
        ),
        migrations.AlterField(
            model_name='workingtime',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_times', to='clubs.Club', verbose_name='club'),
        ),
    ]