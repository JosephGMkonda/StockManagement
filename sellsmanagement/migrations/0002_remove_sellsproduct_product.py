# Generated by Django 3.2 on 2024-04-12 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sellsmanagement', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellsproduct',
            name='product',
        ),
    ]
