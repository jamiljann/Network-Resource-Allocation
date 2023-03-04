# Generated by Django 4.1.3 on 2023-01-08 05:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myint', '0004_reserveport1_dayer_alter_reserveport1_newid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserveport1',
            name='newID',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99999999999)]),
        ),
    ]
