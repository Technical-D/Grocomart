# Generated by Django 4.1.4 on 2023-01-06 14:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_shippingaddress_zipcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_completed',
            field=models.DateField(default=datetime.date(2023, 1, 6)),
        ),
    ]
