# Generated by Django 2.0.2 on 2018-04-18 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gibdd_app', '0003_auto_20180418_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accidentreport',
            name='accident_causer_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.Driver', verbose_name='Виновник аварии'),
        ),
    ]
