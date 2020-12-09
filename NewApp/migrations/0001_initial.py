# Generated by Django 3.1.3 on 2020-11-23 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MotoTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MotoVendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Motorcycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moto_model', models.CharField(max_length=50)),
                ('engine', models.CharField(max_length=50)),
                ('max_speed', models.IntegerField()),
                ('power', models.IntegerField()),
                ('description', models.TextField(max_length=300)),
                ('date_release', models.DateField()),
                ('date_adding', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, to='NewApp.motovendor')),
                ('type', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, to='NewApp.mototypes')),
            ],
        ),
    ]
