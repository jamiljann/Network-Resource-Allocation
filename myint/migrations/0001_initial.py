# Generated by Django 4.1.3 on 2022-12-30 14:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('int_Name', models.CharField(max_length=50)),
                ('Description', models.CharField(blank=True, max_length=155)),
                ('int_ID', models.CharField(blank=True, max_length=15)),
                ('IP', models.CharField(blank=True, max_length=35)),
                ('Profile', models.CharField(blank=True, max_length=25)),
                ('VPN', models.CharField(blank=True, max_length=50)),
                ('Encapsulation', models.CharField(blank=True, max_length=50)),
                ('Int_type', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Router',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Type', models.CharField(max_length=50)),
                ('IP', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ReservePort',
            fields=[
                ('Newint', models.CharField(max_length=60)),
                ('Encap', models.CharField(max_length=50)),
                ('Peygiri', models.IntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(99999999999)])),
                ('Des', models.CharField(max_length=155)),
                ('IP', models.CharField(blank=True, max_length=35, null=True)),
                ('VLAN', models.IntegerField(validators=[django.core.validators.MinValueValidator(2300), django.core.validators.MaxValueValidator(2999)])),
                ('PE', models.CharField(blank=True, max_length=10)),
                ('Date', models.DateField()),
                ('Dayer', models.BooleanField(default=False)),
                ('Info', models.CharField(blank=True, max_length=25)),
                ('Int', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myint.interface')),
                ('Router', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myint.router')),
                ('Service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myint.servicetype')),
                ('theauthor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IP_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IP', models.CharField(max_length=15)),
                ('Mask', models.CharField(max_length=15)),
                ('VRF', models.CharField(max_length=15)),
                ('Destination', models.CharField(max_length=15, null=True)),
                ('Router', models.CharField(max_length=15)),
                ('Parvande', models.CharField(blank=True, max_length=11)),
                ('Description', models.CharField(default=' ', max_length=155, null=True)),
                ('Type', models.CharField(max_length=10, null=True)),
                ('Int', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myint.interface')),
            ],
        ),
        migrations.AddField(
            model_name='interface',
            name='Router_Name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Int_cross', to='myint.router'),
        ),
    ]
