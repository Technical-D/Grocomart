# Generated by Django 4.1.4 on 2022-12-27 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=60, unique=True)),
                ('consent', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Dairy', 'Dairy'), ('Vegetables', 'Vegetables'), ('Fruits', 'Fruits'), ('Grains', 'Grains'), ('Pulses', 'Pulses'), ('Snacks', 'Snacks'), ('Edible Oils', 'Edible Oils'), ('Biscuits', 'Biscuits')], max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='d_price',
            field=models.FloatField(verbose_name='Discounted Price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='o_price',
            field=models.FloatField(verbose_name='Original Price'),
        ),
    ]
