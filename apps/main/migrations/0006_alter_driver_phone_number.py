# Generated by Django 5.2 on 2025-05-06 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_driver_in_city_alter_driver_to_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='phone_number',
            field=models.CharField(help_text='Нужно через +996', max_length=50, verbose_name='Номер телефона'),
        ),
    ]
