# Generated by Django 4.1.4 on 2022-12-30 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_order_shippingaddress_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='order',
        ),
    ]
