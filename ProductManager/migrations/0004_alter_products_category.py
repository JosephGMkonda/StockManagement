# Generated by Django 4.0.4 on 2022-05-21 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductManager', '0003_remove_products_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.CharField(max_length=100),
        ),
    ]
