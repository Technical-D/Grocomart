# Generated by Django 4.1.4 on 2022-12-27 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_queries_is_resolved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queries',
            name='message',
            field=models.CharField(default='asd', max_length=255),
        ),
    ]