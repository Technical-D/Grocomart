# Generated by Django 4.1.4 on 2023-01-06 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_shippingaddress_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='zipcode',
            field=models.IntegerField(),
        ),
    ]
