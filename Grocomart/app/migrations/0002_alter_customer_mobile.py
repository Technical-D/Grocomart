# Generated by Django 4.1.4 on 2022-12-22 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.CharField(max_length=12, verbose_name='mobile no'),
        ),
    ]
