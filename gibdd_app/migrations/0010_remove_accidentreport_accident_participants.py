# Generated by Django 2.0.2 on 2018-03-24 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gibdd_app', '0009_auto_20180324_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accidentreport',
            name='accident_participants',
        ),
    ]