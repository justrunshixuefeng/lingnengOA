# Generated by Django 2.0.4 on 2019-11-25 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ln', '0005_remove_announcement_department'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='permission',
            table='permission',
        ),
        migrations.AlterModelTable(
            name='role',
            table='role',
        ),
    ]
