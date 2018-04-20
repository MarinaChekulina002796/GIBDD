# Generated by Django 2.0.2 on 2018-04-17 09:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gibdd_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspector',
            name='inspector_status',
            field=models.CharField(choices=[('Рядовой полиции', 'Рядовой полиции'), ('Младший сержант', 'Младший сержант'), ('Сержант', 'Сержант'), ('Старший сержант', 'Старший сержант'), ('Старшина полиции', 'Старшина полиции'), ('Прапорщик полиции', 'Прапорщик полиции'), ('Старший прапорщик', 'Старший прапорщик'), ('Младший лейтенант полиции', 'Младший лейтенант полиции'), ('Лейтенант', 'Лейтенант'), ('Старший лейтенант', 'Старший лейтенант'), ('Капитан полиции', 'Капитан полиции'), ('Майор полиции', 'Майор полиции'), ('Подполковник', 'Подполковник'), ('Полковник полиции', 'Полковник полиции'), ('Генерал-майор полиции', 'Генерал-майор полиции'), ('Генерал-лейтенант полиции', 'Генерал-лейтенант полиции'), ('Генерал-полковник полиции', 'Генерал-полковник полиции'), ('Генерал полиции Российской Федерации', 'Генерал полиции Российской Федерации')], max_length=50, verbose_name='Звание инспектора'),
        ),
        migrations.AlterField(
            model_name='license',
            name='date_end_dr_license',
            field=models.DateField(blank=True, default=datetime.date(2028, 4, 17), editable=False, null=True, verbose_name='Дата окончания действия ВУ'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='owner_number',
            field=models.CharField(max_length=11, unique=True, verbose_name='Номер свидетельства собственника'),
        ),
    ]