# Generated by Django 2.0 on 2018-11-23 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedor', '0005_auto_20181122_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='control',
            field=models.BooleanField(default=True),
        ),
    ]