# Generated by Django 4.1.4 on 2022-12-27 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_queries_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='queries',
            name='is_resolved',
            field=models.BooleanField(default=False),
        ),
    ]
