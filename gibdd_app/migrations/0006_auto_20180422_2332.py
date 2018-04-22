# Generated by Django 2.0.2 on 2018-04-22 20:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gibdd_app', '0005_auto_20180419_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accidentreport',
            name='accident_number_of_people',
            field=models.IntegerField(verbose_name='Количество взрослых людей в аварии'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='passport_number',
            field=models.CharField(max_length=11, unique=True, verbose_name='Номер паспорта'),
        ),
        migrations.AlterField(
            model_name='license',
            name='date_end_dr_license',
            field=models.DateField(blank=True, default=datetime.date(2028, 4, 22), editable=False, null=True, verbose_name='Дата окончания действия ВУ'),
        ),
    ]
