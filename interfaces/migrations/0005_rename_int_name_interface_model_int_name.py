# Generated by Django 4.0.7 on 2023-07-18 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interfaces', '0004_alter_interface_config_model_router_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interface_model',
            old_name='int_Name',
            new_name='Int_Name',
        ),
    ]
